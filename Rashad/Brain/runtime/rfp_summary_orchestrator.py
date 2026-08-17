#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import copy
from brain.provider import Invocation, NoExecutionProvider, resolve_brain_provider, provider_runtime_metadata
from brain.utils import new_id
from brain.visual_search import generate_hypotheses
from brain.artifact_brain import provisional_partner_selection, partner_skeptic_test, route_artifact_councils
from brain.artifact_council_runtime import execute_artifact_councils
from brain.visual_render import render_low_fidelity_candidates
from brain.orchestrator import run_brain
from brain.actual_output_qa import evaluate_page_output, evaluate_deck_output
from brain.composition_spec import build_page_composition_spec

REFINEMENT_LOGICS=['SIMPLIFY_HIERARCHY','STRENGTHEN_EVIDENCE','SHIFT_FOCAL_POINT','REDUCE_COGNITIVE_LOAD']

def execute_page_brain(task, provider=None, execution_mode='AUTO', host_invoke_fn=None, host_response_bundle=None, host_name='HOST_MODEL'):
    return run_brain(task,provider=provider,execution_mode=execution_mode,host_invoke_fn=host_invoke_fn,host_response_bundle=host_response_bundle,host_name=host_name)

def _judge_one(provider, council_id, stage, candidate, render, content_pack, graph):
    inv=Invocation(
        'INDEPENDENT_JUDGE', council_id, new_id('ACTOR-INDEPENDENT-VISUAL-JUDGE'), new_id('CTX-VISUAL-JUDGE'),
        {'stage':stage,'candidate_id':candidate['id'],'candidate':candidate,'actual_render_hash':render['actual_render_hash'],'image_paths':[render['render_path']],'content_pack':content_pack,'semantic_graph':graph},
        previous_response_id=None
    )
    rr=provider.invoke(inv)
    if rr.get('status')!='PASS': return {'status':'NOT_EXECUTED','reason':rr.get('reason','INDEPENDENT_JUDGE_NOT_EXECUTED'),'provider_result':rr}
    return {'status':'PASS','candidate_id':candidate['id'],'independent':rr.get('independent',True),'judge_invocation_id':rr.get('judge_invocation_id') or rr.get('invocation_id'),'previous_response_id':rr.get('previous_response_id'),'score':float(rr.get('score',0)),'hard_blockers':rr.get('hard_blockers',[]),'evidence_refs':rr.get('evidence_refs',[]),'actual_render_hash':render['actual_render_hash'],'raw':rr}

def _mutate(top_hypotheses, content_pack=None, graph=None):
    # Refinements must actually move composition, not only relabel a thumbnail.
    out=[]; k=0
    for hi,h in enumerate(top_hypotheses):
        for j in range(2):
            k+=1; m=copy.deepcopy(h); m['parent_id']=h['id']; m['id']=f'M{k}'
            logic_index=(hi*2+j) % len(REFINEMENT_LOGICS)
            m['composition_logic']=REFINEMENT_LOGICS[logic_index]
            m['refinement_goal']='SIMPLER_AND_CLEARER' if j==0 else 'STRONGER_PROOF_AND_HIERARCHY'
            if content_pack is not None:
                spec=build_page_composition_spec(m,content_pack,graph or {},variant_index=7+k,reference_grammar_ids=m.get('reference_grammar_ids'))
                # SHIFT_FOCAL_POINT is required to physically shift the focal anchor.
                if m['composition_logic']=='SHIFT_FOCAL_POINT':
                    spec=build_page_composition_spec(m,content_pack,graph or {},variant_index=17+k,reference_grammar_ids=m.get('reference_grammar_ids'))
                m['composition_spec']=spec; m['structural_signature']=spec['structural_signature']
            else:
                m['structural_signature']=f"{m.get('communication_strategy')}|{m.get('strategy_family')}|{m['composition_logic']}|M{k}"
            out.append(m)
    return out

def _provisional_draft_master(hypotheses, renders, reason):
    by={r['candidate_id']:r for r in renders}
    sel=provisional_partner_selection(hypotheses)
    h=next(x for x in hypotheses if x['id']==sel['candidate_id']); r=by[h['id']]
    return {
        'candidate_id':h['id'], 'communication_strategy':h.get('communication_strategy'), 'strategy_family':h.get('strategy_family'),
        'actual_render_hash':r['actual_render_hash'], 'render_path':r['render_path'], 'render_kind':r.get('render_kind','COMMUNICATION_STRATEGY_CONCEPT_RENDER_V3'),
        'selection_authority':sel['selection_authority'], 'selection_status':'INTERNAL_CONCEPT_DRAFT_NOT_USER_VISIBLE',
        'selection_reason':f"{reason}; {sel['selection_reason']}", 'independent_judge_complete':False,
        'partner_fit_score':h.get('partner_fit_score'), 'simplicity_score':h.get('simplicity_score')
    }

def execute_visual_search(page_id, graph, content_pack, out_dir, judge_provider=None, council_id='C11_VISUAL_PERCEPTION_INFO_DESIGN', execution_mode='AUTO', host_invoke_fn=None, host_response_bundle=None, host_name='HOST_MODEL'):
    provider,resolution=resolve_brain_provider(judge_provider,execution_mode=execution_mode,host_invoke_fn=host_invoke_fn,host_response_bundle=host_response_bundle,host_name=host_name); out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    language=content_pack.get('language','AR')
    artifact_council_route=route_artifact_councils(graph,content_pack,language,'PRE_CONCEPT')
    artifact_council_execution=execute_artifact_councils(graph,content_pack,provider,language,'PRE_CONCEPT')
    hs=generate_hypotheses(graph,content_pack)
    if hs.get('status')!='PASS' or len(hs.get('hypotheses',[]))!=5:
        return {'status':'BLOCKED','reason':'FIVE_HYPOTHESES_NOT_AVAILABLE','hypothesis_result':hs,'execution_mode_resolution':resolution,'provider_runtime':provider_runtime_metadata(provider)}
    hypotheses=hs['hypotheses']
    skeptic=[{'candidate_id':h['id'],**partner_skeptic_test(h,hs.get('page_features',{}))} for h in hypotheses]
    if all(x['status']!='PASS' for x in skeptic):
        return {'status':'BLOCKED','reason':'ALL_HYPOTHESES_REJECTED_BY_ARTIFACT_SKEPTIC','hypotheses':hypotheses,'skeptic_results':skeptic,'execution_mode_resolution':resolution,'provider_runtime':provider_runtime_metadata(provider)}
    renders=render_low_fidelity_candidates(hypotheses,out/'initial')
    if len(renders)!=5 or len({r['actual_render_hash'] for r in renders})!=5:
        return {'status':'BLOCKED','reason':'FIVE_DISTINCT_ACTUAL_RENDERS_NOT_PROVEN','hypotheses':hypotheses,'renders':renders,'execution_mode_resolution':resolution,'provider_runtime':provider_runtime_metadata(provider)}
    by_render={r['candidate_id']:r for r in renders}; judgments=[]; blocked_judgments=[]
    for h in hypotheses:
        j=_judge_one(provider,council_id,'INITIAL_VISUAL_CRITIQUE',h,by_render[h['id']],content_pack,graph)
        if j.get('status')!='PASS': blocked_judgments.append({'candidate_id':h['id'],'judgment':j})
        else: judgments.append(j)
    if blocked_judgments:
        dm=_provisional_draft_master(hypotheses,renders,'INDEPENDENT_JUDGMENT_INCOMPLETE')
        page_qa=evaluate_page_output({'page_id':page_id,'selected_render_hash':dm['actual_render_hash'],'selected_strategy':dm.get('communication_strategy'),'selected_candidate_id':dm['candidate_id'],'hypotheses':hypotheses,'actual_pixel_review':{'status':'NOT_EXECUTED'}})
        pending=provider_runtime_metadata(provider).get('pending_requests',[])
        return {'status':'HOST_NATIVE_EXECUTION_PENDING' if pending else 'INTERNAL_CONCEPT_DRAFT_READY','reason':'HOST_NATIVE_VISUAL_JUDGMENT_PENDING' if pending else 'LIVE_JUDGE_ABSENT_CONCEPT_SEARCH_ONLY_NOT_USER_VISIBLE','artifact_brain_version':'4.0.0','execution_mode_resolution':resolution,'provider_runtime':provider_runtime_metadata(provider),'artifact_council_route':artifact_council_route,'artifact_council_execution':artifact_council_execution,'hypotheses':hypotheses,'skeptic_results':skeptic,'renders':renders,'initial_independent_judgments':judgments,'blocked_judgments':blocked_judgments,'draft_master':dm,'winner':dm['candidate_id'],'winner_strategy':dm.get('communication_strategy'),'composition_count':5,'selection_status':'PROVISIONAL_CONCEPT_NOT_USER_VISIBLE','draft_actual_output_qa':page_qa,'user_visible_delivery_ready':False,'production_render_required':True,'independent_release_ready':False,'host_native_pending_requests':pending}
    ranked=sorted(judgments,key=lambda x:x.get('score',0),reverse=True); top_ids=[x['candidate_id'] for x in ranked[:2]]; top_h=[next(h for h in hypotheses if h['id']==cid) for cid in top_ids]
    mutations=_mutate(top_h,content_pack,graph); refined=render_low_fidelity_candidates(mutations,out/'refined')
    ref_by={r['candidate_id']:r for r in refined}; refined_j=[]; blocked_refined=[]
    for m in mutations:
        j=_judge_one(provider,council_id,'REFINED_VISUAL_CRITIQUE',m,ref_by[m['id']],content_pack,graph)
        if j.get('status')!='PASS': blocked_refined.append({'candidate_id':m['id'],'judgment':j})
        else: refined_j.append(j)
    if blocked_refined:
        pending=provider_runtime_metadata(provider).get('pending_requests',[])
        return {'status':'HOST_NATIVE_EXECUTION_PENDING' if pending else 'NOT_EXECUTED','reason':'HOST_NATIVE_REFINED_VISUAL_JUDGMENT_PENDING' if pending else 'REFINED_INDEPENDENT_VISUAL_JUDGE_REQUIRED','execution_mode_resolution':resolution,'provider_runtime':provider_runtime_metadata(provider),'hypotheses':hypotheses,'renders':renders,'initial_independent_judgments':judgments,'top_2':top_ids,'refined_renders':refined,'refined_independent_judgments':refined_j,'blocked_judgments':blocked_refined,'host_native_pending_requests':pending}
    final_inv=Invocation('INDEPENDENT_JUDGE',council_id,new_id('ACTOR-FINAL-VISUAL-JUDGE'),new_id('CTX-FINAL-VISUAL-JUDGE'),{'stage':'FINAL_VISUAL_SELECTION','candidate_ids':[m['id'] for m in mutations],'candidates':mutations,'actual_render_hashes':{r['candidate_id']:r['actual_render_hash'] for r in refined},'image_paths':[r['render_path'] for r in refined],'content_pack':content_pack,'semantic_graph':graph},previous_response_id=None)
    fr=provider.invoke(final_inv)
    if fr.get('status')!='PASS' or fr.get('winner_candidate_id') not in {m['id'] for m in mutations}:
        pending=provider_runtime_metadata(provider).get('pending_requests',[]); return {'status':'HOST_NATIVE_EXECUTION_PENDING' if pending else 'NOT_EXECUTED','reason':'HOST_NATIVE_FINAL_VISUAL_SELECTION_PENDING' if pending else 'FINAL_INDEPENDENT_VISUAL_SELECTION_REQUIRED','execution_mode_resolution':resolution,'provider_runtime':provider_runtime_metadata(provider),'hypotheses':hypotheses,'renders':renders,'initial_independent_judgments':judgments,'top_2':top_ids,'refined_renders':refined,'refined_independent_judgments':refined_j,'final_provider_result':fr,'host_native_pending_requests':pending}
    winner=fr['winner_candidate_id']; final_hash=ref_by[winner]['actual_render_hash']
    final={'independent':fr.get('independent',True),'judge_invocation_id':fr.get('judge_invocation_id') or fr.get('invocation_id'),'previous_response_id':fr.get('previous_response_id'),'winner_candidate_id':winner,'score':float(fr.get('score',0)),'hard_blockers':fr.get('hard_blockers',[]),'evidence_refs':fr.get('evidence_refs',[]),'actual_render_hash':final_hash}
    winner_strategy=next((m.get('communication_strategy') for m in mutations if m['id']==winner),None)
    winning_concept=next((m for m in mutations if m.get('id')==winner),None) or {}
    art_direction_execution=execute_artifact_councils(graph,content_pack,provider,language,'ART_DIRECTION',prior={'winning_concept':winning_concept,'final_independent_judgment':final})
    page_qa=evaluate_page_output({'page_id':page_id,'selected_render_hash':final_hash,'selected_strategy':winner_strategy,'selected_candidate_id':winner,'hypotheses':hypotheses,'render_kind':'COMMUNICATION_STRATEGY_CONCEPT_RENDER_V3','actual_pixel_review':{'status':'PASS','judge_invocation_id':final.get('judge_invocation_id')}}, visibility='INTERNAL')
    status='PASS' if artifact_council_execution.get('status')=='PASS' and art_direction_execution.get('status')=='PASS' else 'INTERNAL_CONCEPT_DRAFT_READY'
    reason=None if status=='PASS' else 'ARTIFACT_COUNCIL_OR_ART_DIRECTION_EXECUTION_INCOMPLETE_INTERNAL_ONLY'
    return {'status':status,'reason':reason,'artifact_brain_version':'4.0.0','execution_mode_resolution':resolution,'provider_runtime':provider_runtime_metadata(provider),'artifact_council_route':artifact_council_route,'artifact_council_execution':artifact_council_execution,'art_direction_execution':art_direction_execution,'page_id':page_id,'hypotheses':hypotheses,'skeptic_results':skeptic,'renders':renders,'initial_independent_judgments':judgments,'top_2':top_ids,'mutations':mutations,'refined_renders':refined,'refined_independent_judgments':refined_j,'final_independent_judgment':final,'winner':winner,'winner_strategy':winner_strategy,'composition_count':9,'selection_status':'INDEPENDENT_CONCEPT_WINNER_LOCKED','actual_output_qa':page_qa,'user_visible_delivery_ready':False,'production_render_required':True}


def execute_deck_actual_output_qa(page_visual_results):
    # Concept-search results are not final product pixels. This helper is INTERNAL only.
    # User-visible delivery must go through artifact_delivery_orchestrator + independent pixel QA.
    pages=[]
    for r in page_visual_results or []:
        dm=r.get('draft_master') or {}
        winner=r.get('winner'); final=r.get('final_independent_judgment') or {}
        selected_hash=final.get('actual_render_hash') or dm.get('actual_render_hash')
        selected_strategy=r.get('winner_strategy') or dm.get('communication_strategy')
        selected_candidate=winner or dm.get('candidate_id')
        pages.append({'page_id':r.get('page_id') or r.get('page_id_hint') or f'P{len(pages)+1:02d}','selected_render_hash':selected_hash,'selected_strategy':selected_strategy,'selected_candidate_id':selected_candidate,'composition_logic':(next((m.get('composition_logic') for m in r.get('mutations',[]) if m.get('id')==selected_candidate),None)),'hypotheses':r.get('hypotheses',[]),'render_kind':'COMMUNICATION_STRATEGY_CONCEPT_RENDER_V3','actual_pixel_review':{'status':'NOT_EXECUTED'}})
    return evaluate_deck_output(pages,visibility='INTERNAL')
