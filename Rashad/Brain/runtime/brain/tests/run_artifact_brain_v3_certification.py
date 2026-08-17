#!/usr/bin/env python3
from __future__ import annotations
import json,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve(); RUNTIME=HERE.parents[2]; sys.path.insert(0,str(RUNTIME))
from brain.artifact_brain import REGISTRY, STRATEGIES, generate_communication_hypotheses, route_artifact_councils, partner_skeptic_test, provisional_partner_selection, DIAGRAM
from brain.visual_render import render_low_fidelity_candidates
from brain.actual_output_qa import evaluate_page_output,evaluate_deck_output
from brain.artifact_gate import validate_artifact_draft,derive_output_classification

results=[]
def add(name,ok,detail=None): results.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})

def graph(relational=True,complexity=False):
    ns=[{'id':f'N{i}'} for i in range(1,7 if complexity else 4)]
    es=[]
    if relational:
        rels=['FLOWS_TO','DEPENDS_ON','ENABLES','CONTROLS','FEEDS_BACK']
        count=5 if complexity else 2
        for i in range(count): es.append({'source':ns[i%len(ns)]['id'],'target':ns[(i+1)%len(ns)]['id'],'relation':rels[i%len(rels)]})
    return {'nodes':ns,'edges':es}

# registry / bounded big brain
add('artifact_brain_20_councils',len(REGISTRY['councils'])==20,len(REGISTRY['councils']))
add('artifact_brain_large_role_universe',len(REGISTRY['roles'])>=100,len(REGISTRY['roles']))
add('communication_strategy_universe_24',len(STRATEGIES)==24,sorted(STRATEGIES))
add('scorecard_strategy_available','SCORECARD_LED' in STRATEGIES,sorted(STRATEGIES))
route=route_artifact_councils(graph(True,True),{'thesis':'AI platform architecture with 30 POCs, commercial risk and RFP evaluation','language':'AR'})
policy=REGISTRY['runtime_activation_policy']
add('artifact_brain_bounded_activation',route['bounded_activation'] and len(route['active_councils'])<=policy['max_active_councils_per_page'] and len(route['active_roles'])<=policy['max_active_roles_per_page'],route)
add('artifact_core_councils_active',all(x in route['active_councils'] for x in ['ARGUMENT_COUNCIL','EVIDENCE_EPISTEMIC_COUNCIL','COMMUNICATION_STRATEGY_COUNCIL','SIMPLICITY_COUNCIL','INFORMATION_DESIGN_COUNCIL','ARTIFACT_RED_TEAM']),route['active_councils'])

# real communication-strategy search
cases=[
 {'thesis':'Five BOQ lines hide 30 POCs and 20 services with major pricing sensitivity','evidence':['BOQ'],'language':'AR'},
 {'thesis':'HOLD until eight management decision gates close','language':'AR'},
 {'thesis':'24 mandatory resources across 12 roles require interviews and security clearance','language':'AR'},
 {'thesis':'The RFP documents conflict and must be reconciled before pricing','evidence':['RFP'],'language':'AR'},
]
win_ids=[]; all_sigs=[]
for idx,c in enumerate(cases,1):
    h=generate_communication_hypotheses(graph(True,idx==1),c)
    add(f'case_{idx}_five_distinct_communication_strategies',h['status']=='PASS' and h['distinct_communication_strategies']==5,h)
    add(f'case_{idx}_three_strategy_families',h['distinct_strategy_families']>=3,h['distinct_strategy_families'])
    add(f'case_{idx}_minimal_candidate_present',h['contains_minimal_hypothesis'] and not h['diagram_only_search'],[x['communication_strategy'] for x in h['hypotheses']])
    add(f'case_{idx}_no_geometry_primitive_as_hypothesis',all(x['communication_strategy'] not in {'RING','HUB','SPINE','STACK','LANE'} for x in h['hypotheses']),None)
    win_ids.append(provisional_partner_selection(h['hypotheses'])['candidate_id']); all_sigs.append([x['structural_signature'] for x in h['hypotheses']])
add('provisional_selection_not_fixed_H1',len(set(win_ids))>1 and not all(x=='H1' for x in win_ids),win_ids)
add('page_specific_hypothesis_signatures',len({s for page in all_sigs for s in page})==sum(map(len,all_sigs)),all_sigs)

# concept renders must differ by page content and strategy
with tempfile.TemporaryDirectory() as td:
    a=generate_communication_hypotheses(graph(True,True),cases[0])['hypotheses']; b=generate_communication_hypotheses(graph(True,True),cases[1])['hypotheses']
    ra=render_low_fidelity_candidates(a,Path(td)/'a'); rb=render_low_fidelity_candidates(b,Path(td)/'b')
    add('five_unique_render_hashes_per_page',len({x['actual_render_hash'] for x in ra})==5 and len({x['actual_render_hash'] for x in rb})==5,None)
    add('candidate_position_not_same_render_across_pages',all(ra[i]['actual_render_hash']!=rb[i]['actual_render_hash'] for i in range(5)),None)

# skeptic / complexity
simple=generate_communication_hypotheses(graph(False),{'thesis':'One decision statement','language':'AR'})
for h in simple['hypotheses']:
    if h['communication_strategy'] in DIAGRAM:
        add('skeptic_rejects_unearned_diagram',partner_skeptic_test(h,simple['page_features'])['status']=='REJECT',h); break
else: add('simple_page_need_not_generate_diagram',True,[h['communication_strategy'] for h in simple['hypotheses']])

# actual output QA blocks deck pathologies
varied=[]
strategies=['STATEMENT_LED','SYSTEM_LED','TABLE_LED','NUMBER_LED','ARCHITECTURE_LED','COMPARISON_LED','DECISION_LED','CHART_LED']
for i,s in enumerate(strategies):
    hs=[{'communication_strategy':x,'strategy_family':('RELATIONAL' if x in DIAGRAM else 'MINIMAL' if x in {'STATEMENT_LED','NUMBER_LED','DECISION_LED'} else 'ANALYTICAL')} for x in ['STATEMENT_LED','NUMBER_LED','EVIDENCE_LED','COMPARISON_LED','SYSTEM_LED']]
    varied.append({'page_id':f'P{i+1}','selected_render_hash':f'HASH{i+1}','selected_strategy':s,'selected_candidate_id':f'H{(i%5)+1}','composition_logic':f'C{i%4}','hypotheses':hs,'actual_pixel_review':{'status':'NOT_EXECUTED'}})
vd=evaluate_deck_output(varied)
add('varied_deck_not_blocked',vd['status']!='BLOCKED',vd)
bad=[]
for i in range(12):
    bad.append({'page_id':f'P{i+1}','selected_render_hash':f'X{i}','selected_strategy':'SYSTEM_LED' if i<10 else 'TABLE_LED','selected_candidate_id':'H1','composition_logic':'SAME','hypotheses':[{'communication_strategy':x,'strategy_family':'RELATIONAL' if x in DIAGRAM else 'MINIMAL'} for x in ['SYSTEM_LED','ARCHITECTURE_LED','PROCESS_LED','SEQUENCE_LED','JOURNEY_LED']],'actual_pixel_review':{'status':'NOT_EXECUTED'}})
bd=evaluate_deck_output(bad)
add('diagram_overuse_blocked','DECK_DIAGRAM_OVERUSE' in bd['blockers'],bd)
add('positional_winner_bias_blocked','POSITIONAL_HYPOTHESIS_WINNER_BIAS' in bd['blockers'],bd)

# actual-output QA and release truthfulness
good_h=generate_communication_hypotheses(graph(True,True),cases[0])['hypotheses']
state={'content_status':'PASS','evidence_status':'PASS','page_contract':{'page_id':'P01'},'cognitive_packet':{'thesis':'x'},'artifact_intent':{'type':'EXECUTIVE_COMMUNICATION'},'semantic_graph':graph(True,True),'hypotheses':good_h,'render_evidence':[{'candidate_id':h['id'],'actual_render_hash':f'RH{i}','render_path':f'/tmp/{i}.png'} for i,h in enumerate(good_h)],'selected_master':{'candidate_id':good_h[0]['id'],'actual_render_hash':'RH0','selection_authority':'PROVISIONAL_PARTNER_HEURISTIC_NOT_INDEPENDENT','selection_reason':'fit then simplicity'},'brand_preflight':{'status':'PASS','rubix_asset_status':'VERIFIED'},'qa_state':{'status':'DRAFT_QA_PASS','qa_scope':'ACTUAL_RENDERED_OUTPUT','actual_output_qa_status':'DRAFT_QA_PARTIAL','actual_pixel_visual_quality_status':'NOT_EXECUTED'},'material_claim_ids':['C1'],'claim_visual_bindings':[{'claim_id':'C1','evidence_refs':['E1'],'visual_node_ids':['N1']}],'independent_judgment':{'status':'NOT_EXECUTED'},'parity_status':'NOT_EXECUTED','proof_index_status':'NOT_EXECUTED','release':{}}
add('user_visible_gate_blocks_actual_output_partial_qa',validate_artifact_draft(state)['status']=='BLOCKED',validate_artifact_draft(state))

classification=derive_output_classification(state)
add('partial_qa_never_user_visible_or_release_candidate',classification in {'CONTENT_DRAFT','INTERNAL_CONCEPT_DRAFT'} and classification not in {'USER_VISIBLE_ARTIFACT_DRAFT','RELEASE_CANDIDATE','RELEASED'},classification)
add('missing_execution_proof_cannot_claim_internal_concept_ready',classification=='CONTENT_DRAFT',classification)

out={'suite':'Rashad Consulting Artifact Intelligence Brain v3.3 Certification','artifact_brain_version':'3.3.0','status':'PASS' if all(x['status']=='PASS' for x in results) else 'FAIL','passed':sum(x['status']=='PASS' for x in results),'total':len(results),'tests':results}
Path(__file__).with_name('ARTIFACT_BRAIN_V3_CERTIFICATION_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 1)
