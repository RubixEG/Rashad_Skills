#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib, json, uuid
from brain.actual_output_qa import evaluate_page_output, evaluate_deck_output
from brain.deck_continuity import evaluate_ledger as evaluate_deck_continuity
from brain.product_inspector import inspect_pptx, sha256_file
from brain.delivery_gate import validate_user_visible_delivery
from brain.artifact_council_runtime import execute_artifact_councils
from brain.provider import NoExecutionProvider, resolve_brain_provider, provider_runtime_metadata
from brain.execution_proof import validate_brain_execution_proof, validate_artifact_execution_ledger, validate_expert_execution_ledger
from brain.production.renderer import render_composition_page
from brain.production.image_provider import resolve_image_provider
from brain.imagery_director import build_image_request, validate_image_plate
from brain.semantic_master_gate import inspect_semantic_html_master

MAX_REPAIR_ROUNDS=3

def _hash(path): return sha256_file(path)
def _id(prefix): return prefix+'-'+uuid.uuid4().hex[:12].upper()

def promote_page_to_production(page_search_result, production_renderer=None, pixel_reviewer=None, content_pack=None, semantic_graph=None, out_dir=None,
                               brain_session=None, page_contract=None, artifact_intent=None, evidence_lineage=None,
                               brand_preflight=None, artifact_provider=None, material_claim_ids=None, claim_visual_bindings=None,
                               execution_mode='AUTO', host_invoke_fn=None, host_response_bundle=None, host_name='HOST_MODEL',
                               image_provider=None, image_host_invoke_fn=None, image_response_bundle=None,
                               brand_logo=None, client_logo=None, allow_test_font_fallback=False):
    """Promote a concept-search winner to a user-visible production page.

    production_renderer must create a real final page render and return
    {status:'PASS', render_path, actual_render_hash, render_kind:'PRODUCTION_PAGE_RENDER', production_render_id}.
    pixel_reviewer must inspect the actual pixels and return the complete independent quality scorecard.
    No low-fidelity concept render can cross this boundary.
    """
    content_pack=dict(content_pack or {}); semantic_graph=dict(semantic_graph or {}); out=Path(out_dir or './rashad-production'); out.mkdir(parents=True,exist_ok=True)
    if not callable(pixel_reviewer): return {'status':'BLOCKED','reason':'INDEPENDENT_PIXEL_REVIEWER_REQUIRED'}
    artifact_provider,provider_resolution=resolve_brain_provider(artifact_provider,execution_mode=execution_mode,host_invoke_fn=host_invoke_fn,host_response_bundle=host_response_bundle,host_name=host_name)
    # Hard admission: production cannot be entered from a fabricated search result or content pack.
    bs=brain_session or {}
    brain_proof=validate_brain_execution_proof(bs)
    if brain_proof.get('status')!='PASS':
        return {'status':'BLOCKED','reason':'BRAIN_EXECUTION_PROOF_NOT_PROVEN','brain_execution_proof':brain_proof}
    if not isinstance(page_contract,dict) or not page_contract:
        return {'status':'BLOCKED','reason':'PAGE_CONTRACT_REQUIRED'}
    if not isinstance(artifact_intent,dict) or not artifact_intent:
        return {'status':'BLOCKED','reason':'ARTIFACT_INTENT_REQUIRED'}
    if not isinstance(evidence_lineage,(dict,list)) or not evidence_lineage:
        return {'status':'BLOCKED','reason':'EVIDENCE_LINEAGE_REQUIRED'}
    material=list(material_claim_ids or content_pack.get('material_claim_ids') or [])
    bindings=list(claim_visual_bindings or content_pack.get('claim_visual_bindings') or [])
    by={x.get('claim_id'):x for x in bindings if isinstance(x,dict)}
    missing=[cid for cid in material if not (by.get(cid,{}).get('evidence_refs') and by.get(cid,{}).get('visual_node_ids'))]
    if material and missing:
        return {'status':'BLOCKED','reason':'CLAIM_EVIDENCE_VISUAL_BINDING_INCOMPLETE','missing_claim_ids':missing}
    ac=page_search_result.get('artifact_council_execution') or {}
    ad=page_search_result.get('art_direction_execution') or {}
    ac_proof=validate_artifact_execution_ledger(ac,'PRE_CONCEPT')
    ad_proof=validate_artifact_execution_ledger(ad,'ART_DIRECTION')
    if ac_proof.get('status')!='PASS': return {'status':'BLOCKED','reason':'ARTIFACT_COUNCIL_EXECUTION_NOT_PROVEN','artifact_execution_proof':ac_proof}
    if ad_proof.get('status')!='PASS': return {'status':'BLOCKED','reason':'ART_DIRECTION_COUNCIL_EXECUTION_NOT_PROVEN','art_direction_execution_proof':ad_proof}
    fj=page_search_result.get('final_independent_judgment') or {}
    if not (fj.get('winner_candidate_id') and fj.get('independent') is True and fj.get('judge_invocation_id')):
        return {'status':'BLOCKED','reason':'INDEPENDENT_CONCEPT_SELECTION_NOT_PROVEN'}
    try: concept_score=float(fj.get('score',0) or 0)
    except Exception: concept_score=0
    if concept_score < 90:
        return {'status':'BLOCKED','reason':'INDEPENDENT_CONCEPT_SCORE_BELOW_90','score':concept_score}
    bp=brand_preflight or content_pack.get('brand_preflight') or {}
    if bp.get('status')!='PASS' or bp.get('rubix_asset_status')!='VERIFIED':
        return {'status':'BLOCKED','reason':'BRAND_PREFLIGHT_NOT_PROVEN'}
    production_councils=execute_artifact_councils(semantic_graph,content_pack,artifact_provider,content_pack.get('language','AR'),'PRODUCTION_READINESS',prior={'artifact_intent':artifact_intent,'page_contract':page_contract,'brand_preflight':bp})
    production_proof=validate_artifact_execution_ledger(production_councils,'PRODUCTION_READINESS')
    if production_proof.get('status')!='PASS':
        return {'status':'BLOCKED','reason':'HOST_NATIVE_EXECUTION_PENDING' if provider_runtime_metadata(artifact_provider).get('pending_count') else 'PRODUCTION_READINESS_COUNCILS_NOT_EXECUTED','production_council_execution':production_councils,'production_execution_proof':production_proof,'execution_mode_resolution':provider_resolution,'provider_runtime':provider_runtime_metadata(artifact_provider),'host_native_pending_requests':provider_runtime_metadata(artifact_provider).get('pending_requests',[])}
    winner=fj.get('winner_candidate_id')
    if not winner:
        return {'status':'BLOCKED','reason':'NO_CONCEPT_WINNER_AVAILABLE'}
    hypotheses=page_search_result.get('hypotheses') or []
    concept=next((h for h in (page_search_result.get('mutations') or hypotheses) if h.get('id')==winner),None)
    if not concept:
        concept=next((h for h in hypotheses if h.get('id')==winner),None)
    if not concept: return {'status':'BLOCKED','reason':'WINNING_CONCEPT_NOT_FOUND'}
    spec=concept.get('composition_spec') or {}
    if not spec or (spec.get('validation') or {}).get('status')!='PASS':
        return {'status':'BLOCKED','reason':'PAGE_COMPOSITION_SPEC_REQUIRED_AND_VALID'}
    # Imagery is a governed production dependency, never a silent cards fallback.
    image_asset=None; image_execution=None
    imagery_mode=(spec.get('imagery') or {}).get('mode','NONE')
    if imagery_mode in {'RASTER_AUGMENTED','GOLDEN_VISUAL_MASTER'}:
        reqwrap=build_image_request(spec,content_pack); request=reqwrap.get('request') or {}
        ip=resolve_image_provider(image_provider,host_invoke_fn=image_host_invoke_fn,response_bundle=image_response_bundle,required=True)
        image_execution=ip.generate(request)
        if image_execution.get('status')!='PASS':
            return {'status':'HOST_NATIVE_IMAGE_PENDING' if image_execution.get('status')=='HOST_NATIVE_IMAGE_PENDING' else 'BLOCKED','reason':image_execution.get('reason','IMAGE_PROVIDER_NOT_PASS'),'image_execution':image_execution,'image_provider_runtime':ip.metadata()}
        normalized={**image_execution,'asset_path':image_execution.get('asset_path') or image_execution.get('image_path'),'asset_sha256':image_execution.get('asset_sha256') or image_execution.get('image_sha256'),'proof':image_execution.get('proof') or {'request_sha256':request.get('request_sha256')}}
        admission=validate_image_plate(normalized,request)
        if admission.get('status')!='PASS': return {'status':'BLOCKED','reason':'IMAGE_ADMISSION_QA_FAILED','image_execution':image_execution,'image_admission':admission}
        image_asset=normalized['asset_path']
    if production_renderer is None:
        def production_renderer(payload):
            return render_composition_page(spec,content_pack,semantic_graph,Path(payload['out_dir'])/f"round_{payload['round']:02d}",image_asset=image_asset,brand_logo=brand_logo,client_logo=client_logo,allow_test_font_fallback=allow_test_font_fallback,emit_pdf=True)
    history=[]
    render=None
    for round_no in range(1,MAX_REPAIR_ROUNDS+1):
        rr=production_renderer({
            'round':round_no,'concept':concept,'content_pack':content_pack,'semantic_graph':semantic_graph,
            'prior_qa':history[-1]['qa'] if history else None,'out_dir':str(out)
        })
        if rr.get('status')!='PASS': return {'status':'BLOCKED','reason':'PRODUCTION_RENDERER_NOT_PASSED','provider_result':rr,'repair_history':history}
        if rr.get('render_kind')!='PRODUCTION_PAGE_RENDER': return {'status':'BLOCKED','reason':'LOW_FIDELITY_OR_UNKNOWN_RENDER_KIND_FORBIDDEN','provider_result':rr}
        path=Path(rr.get('render_path',''))
        if not path.exists(): return {'status':'BLOCKED','reason':'PRODUCTION_RENDER_FILE_MISSING'}
        actual=_hash(path)
        if rr.get('actual_render_hash') and rr.get('actual_render_hash')!=actual: return {'status':'BLOCKED','reason':'PRODUCTION_RENDER_HASH_MISMATCH'}
        rr['actual_render_hash']=actual; rr.setdefault('production_render_id',_id('PROD-RENDER'))
        semantic_master_qa=inspect_semantic_html_master(rr.get('html_master_path'),spec)
        if semantic_master_qa.get('status')!='PASS':
            return {'status':'BLOCKED','reason':'SEMANTIC_MASTER_QA_NOT_PASS','semantic_master_qa':semantic_master_qa,'provider_result':rr,'repair_history':history}
        qa=pixel_reviewer({'round':round_no,'render_path':str(path),'actual_render_hash':actual,'concept':concept,'content_pack':content_pack,'semantic_graph':semantic_graph,'composition_spec':spec,'html_master_path':rr.get('html_master_path')})
        try: at=float(qa.get('artifact_truth_score',0) or 0); ceqs=float(qa.get('ceqs_score',qa.get('ceqs',0)) or 0)
        except Exception: at=ceqs=0
        if at < 90 or ceqs < 90:
            history.append({'round':round_no,'render':rr,'qa':qa,'semantic_master_qa':semantic_master_qa,'verdict':{'status':'BLOCKED','blockers':['ARTIFACT_TRUTH_OR_CEQS_BELOW_90']}})
            render=rr
            continue
        page_obj={
            'page_id':content_pack.get('page_id') or page_search_result.get('page_id') or _id('PAGE'),
            'selected_render_hash':actual,'selected_strategy':concept.get('communication_strategy'),'selected_candidate_id':winner,
            'hypotheses':hypotheses,'visual_concept_id':concept.get('visual_concept_id') or concept.get('structural_signature'),
            'production_render_id':rr['production_render_id'],'render_kind':'PRODUCTION_PAGE_RENDER','actual_pixel_review':qa,'artifact_truth_score':at,'ceqs_score':ceqs,'semantic_master_qa':semantic_master_qa,
            'html_master_path':rr.get('html_master_path'),'html_master_sha256':rr.get('html_master_sha256'),'composition_spec_sha256':rr.get('composition_spec_sha256'),
            'brain_session_id':bs.get('session_id'),'brain_cognitive_lock_status':'PASS','expert_execution_status':'PASS',
            'brain_session_execution_evidence':bs,'brain_execution_proof':brain_proof,'expert_execution_ledger':bs.get('expert_execution_ledger'),
            'artifact_council_execution_status':'PASS','art_direction_execution_status':'PASS','production_council_execution_status':'PASS',
            'page_contract':page_contract,'artifact_intent':artifact_intent,'composition_spec':spec,'image_execution':image_execution,'evidence_lineage':evidence_lineage,'material_claim_ids':material,'claim_visual_bindings':bindings,'brand_preflight':bp,
            'artifact_council_execution':ac,'art_direction_execution':ad,'production_council_execution':production_councils,
            'artifact_execution_proof':ac_proof,'art_direction_execution_proof':ad_proof,'production_execution_proof':production_proof,
            'repair_required':round_no>1 or qa.get('status')!='PASS','repair_history':history,'final_qa_round':round_no,
        }
        verdict=evaluate_page_output(page_obj,visibility='USER_VISIBLE_ARTIFACT_DRAFT')
        history.append({'round':round_no,'render':rr,'qa':qa,'verdict':verdict})
        if verdict['status']=='PASS':
            page_obj['repair_history']=history[:-1]
            page_obj['repair_required']=len(history)>1
            return {'status':'PASS','production_page':page_obj,'final_render':rr,'final_qa':qa,'repair_history':history,'concept':concept,'execution_mode_resolution':provider_resolution,'provider_runtime':provider_runtime_metadata(artifact_provider)}
        render=rr
    return {'status':'BLOCKED','reason':'USER_VISIBLE_QUALITY_FLOOR_NOT_REACHED_AFTER_REPAIR_LIMIT','repair_history':history,'last_render':render}


def build_delivery_dossier(pptx_path, page_promotions, deck_pixel_review, montage_path=None, classification='USER_VISIBLE_ARTIFACT_DRAFT', extra=None, deck_artifact_council_execution=None):
    p=Path(pptx_path); pages=[x['production_page'] for x in page_promotions if x.get('status')=='PASS']
    montage_hash=sha256_file(montage_path) if montage_path and Path(montage_path).exists() else None
    product=inspect_pptx(p,pages)
    deckqa=evaluate_deck_output(pages,visibility=classification,deck_review=deck_pixel_review,deck_sha256=sha256_file(p),montage_sha256=montage_hash,product_inspection=product)
    continuity_pages=[]
    for i,x in enumerate(page_promotions):
        if x.get('status')!='PASS': continue
        rp=(x.get('final_render') or {}).get('render_path') or (x.get('production_page') or {}).get('render_path')
        if not rp: continue
        continuity_pages.append({'page_id':(x.get('production_page') or {}).get('page_id') or f'P{i+1:02d}','master_path':rp,'master_sha256':sha256_file(rp),'previous_page_id':continuity_pages[-1]['page_id'] if continuity_pages else None})
    continuity=evaluate_deck_continuity({'pages':continuity_pages})
    d={
        'schema':'RASHAD_USER_VISIBLE_ARTIFACT_DELIVERY_V1','classification':classification,
        'output_file_sha256':sha256_file(p),'montage_sha256':montage_hash,'pages':pages,
        'artifact_brain_execution_status':'PASS' if len(pages)==len(page_promotions) and pages and all(p.get('artifact_council_execution_status')=='PASS' and p.get('art_direction_execution_status')=='PASS' and p.get('production_council_execution_status')=='PASS' and p.get('expert_execution_status')=='PASS' for p in pages) and isinstance(deck_artifact_council_execution,dict) and deck_artifact_council_execution.get('status')=='PASS' else 'BLOCKED',
        'production_render_status':'PASS' if all(p.get('render_kind')=='PRODUCTION_PAGE_RENDER' for p in pages) else 'BLOCKED',
        'actual_output_qa_closed_loop_status':'PASS' if deckqa.get('status')=='PASS' else 'BLOCKED',
        'deck_pixel_review':deck_pixel_review,'deck_artifact_council_execution':deck_artifact_council_execution or {},'product_inspection':product,'deck_qa':deckqa,'deck_continuity_qa':continuity,
        'framework_certification_substitute':False,'independent_judgment_status':'NOT_EXECUTED',
        'parity_status':'NOT_EXECUTED','proof_index_status':'NOT_EXECUTED','release':{},
    }
    if extra:d.update(extra)
    return d


def authorize_delivery(dossier,pptx_path,requested='USER_VISIBLE_ARTIFACT_DRAFT'):
    return validate_user_visible_delivery(dossier,pptx_path,requested)
