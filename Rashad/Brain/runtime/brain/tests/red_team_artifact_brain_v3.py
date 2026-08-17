#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve(); RUNTIME=HERE.parents[2]; sys.path.insert(0,str(RUNTIME))
from brain.artifact_brain import generate_communication_hypotheses,partner_skeptic_test,route_artifact_councils,provisional_partner_selection,analyze_page_problem,STRATEGIES
from brain.actual_output_qa import evaluate_page_output,evaluate_deck_output
from brain.artifact_gate import validate_artifact_draft

att=[]
def a(name,blocked,detail=None):att.append({'attack':name,'status':'BLOCKED' if blocked else 'ESCAPED','detail':detail})
# geometry masquerading as hypotheses
state={'content_status':'PASS','evidence_status':'PASS','page_contract':{'x':1},'cognitive_packet':{'x':1},'artifact_intent':{'x':1},'semantic_graph':{'x':1},'hypotheses':[{'communication_strategy':x,'strategy_family':'RELATIONAL','structural_signature':x} for x in ['RING','HUB','SPINE','STACK','LANE']],'render_evidence':[{'actual_render_hash':f'h{i}'} for i in range(5)],'selected_master':{'actual_render_hash':'h0','selection_authority':'POSITIONAL_DEFAULT','selection_reason':'H1_DEFAULT'},'brand_preflight':{'status':'PASS','rubix_asset_status':'VERIFIED'},'qa_state':{'status':'DRAFT_QA_PASS','qa_scope':'ACTUAL_RENDERED_OUTPUT','actual_output_qa_status':'PASS'},'material_claim_ids':['C'],'claim_visual_bindings':[{'claim_id':'C','evidence_refs':['E'],'visual_node_ids':['N']}], 'independent_judgment':{},'release':{}}
r=validate_artifact_draft(state); a('GEOMETRY_PRIMITIVES_AS_HYPOTHESES',r['status']=='BLOCKED',r)
a('POSITIONAL_H1_DEFAULT', r['status']=='BLOCKED' and any('POSITIONAL' in e for e in r.get('errors',[])),r)
# same family only
h=generate_communication_hypotheses({'nodes':[{'id':'A'}],'edges':[]},{'thesis':'One concise decision','language':'AR'})
a('SEARCH_COLLAPSES_TO_DIAGRAM_ONLY',not h.get('diagram_only_search') and h.get('contains_minimal_hypothesis'),[x['communication_strategy'] for x in h['hypotheses']])
# unearned diagram
fake={'communication_strategy':'SYSTEM_LED'}; f={'has_relationships':False,'system_complexity_earned':False,'architecture':False}
a('UNNEEDED_SYSTEM_MAP',partner_skeptic_test(fake,f)['status']=='REJECT',partner_skeptic_test(fake,f))
# page hypotheses all diagrams
p={'page_id':'P1','selected_render_hash':'x','selected_strategy':'SYSTEM_LED','selected_candidate_id':'H1','hypotheses':[{'communication_strategy':x,'strategy_family':'RELATIONAL'} for x in ['SYSTEM_LED','ARCHITECTURE_LED','PROCESS_LED','SEQUENCE_LED','JOURNEY_LED']],'actual_pixel_review':{'status':'NOT_EXECUTED'}}
pr=evaluate_page_output(p); a('PAGE_DIAGRAM_ONLY_SEARCH',pr['status']=='BLOCKED',pr)
# deck attacks
pages=[{'page_id':f'P{i}','selected_render_hash':f'h{i}','selected_strategy':'SYSTEM_LED','selected_candidate_id':'H1','composition_logic':'SAME','hypotheses':[],'actual_pixel_review':{'status':'NOT_EXECUTED'}} for i in range(10)]
dr=evaluate_deck_output(pages); a('DECK_100_PERCENT_DIAGRAMS','DECK_DIAGRAM_OVERUSE' in dr['blockers'],dr); a('ALL_PAGES_H1','POSITIONAL_HYPOTHESIS_WINNER_BIAS' in dr['blockers'],dr); a('SAME_COMPOSITION_GRAMMAR','GENERIC_COMPOSITION_REPETITION' in dr['blockers'],dr)
# hash reuse
pages2=[{'page_id':'P1','selected_render_hash':'same','selected_strategy':'STATEMENT_LED','selected_candidate_id':'H2','composition_logic':'A','hypotheses':[],'actual_pixel_review':{'status':'NOT_EXECUTED'}},{'page_id':'P2','selected_render_hash':'same','selected_strategy':'TABLE_LED','selected_candidate_id':'H3','composition_logic':'B','hypotheses':[],'actual_pixel_review':{'status':'NOT_EXECUTED'}}]
a('CROSS_PAGE_RENDER_REUSE','CROSS_PAGE_RENDER_HASH_REUSE' in evaluate_deck_output(pages2)['blockers'],evaluate_deck_output(pages2))
# missing actual-output scope
s=state.copy(); s['hypotheses']=generate_communication_hypotheses({'nodes':[{'id':'A'},{'id':'B'}],'edges':[{'source':'A','target':'B','relation':'FLOWS_TO'}]},{'thesis':'Decision 20% risk','language':'AR'})['hypotheses']; s['selected_master']={'actual_render_hash':'h0','selection_authority':'PROVISIONAL_PARTNER_HEURISTIC_NOT_INDEPENDENT','selection_reason':'fit then simplicity'}; s['qa_state']={'status':'DRAFT_QA_PASS'}
r=validate_artifact_draft(s); a('FRAMEWORK_QA_MASQUERADES_AS_OUTPUT_QA','QA_MUST_TARGET_ACTUAL_RENDERED_OUTPUT' in r['errors'],r)
# expert universe load attack
route=route_artifact_councils({'nodes':[{'id':'A'}],'edges':[]},{'thesis':'simple statement','language':'AR'}); a('LOAD_ALL_ARTIFACT_EXPERTS',len(route['active_roles'])<route['registered_role_count'] and len(route['active_councils'])<route['registered_council_count'],route)
# same candidate position cannot be sole basis in generated hypotheses selection
hs=generate_communication_hypotheses({'nodes':[{'id':'A'},{'id':'B'}],'edges':[{'source':'A','target':'B','relation':'FLOWS_TO'}]},{'thesis':'24 team roles and 30 POCs','language':'AR'})
a('LEGACY_RING_HUB_SPINE_VOCABULARY_RETURNS',all(x['communication_strategy'] not in {'RING','HUB','SPINE','STACK','LANE'} for x in hs['hypotheses']),[x['communication_strategy'] for x in hs['hypotheses']])

# grounded evidence metadata must not force every page into evidence/table communication
meta=generate_communication_hypotheses({'nodes':[{'id':'A'}],'edges':[]},{'thesis':'The client is buying an integrated operating model, not a standalone platform.','evidence':['DOC-1 p.4'],'language':'AR'})
ms=provisional_partner_selection(meta['hypotheses'])
a('EVIDENCE_METADATA_FORCES_TABLE_BIAS',ms['communication_strategy']=='STATEMENT_LED',{'winner':ms,'hypotheses':[x['communication_strategy'] for x in meta['hypotheses']]})
# governance contains the letters "go" but is not a GO decision
feat=analyze_page_problem({'nodes':[{'id':'A'},{'id':'B'}],'edges':[{'source':'A','target':'B','relation':'ENABLES'},{'source':'B','target':'A','relation':'FEEDS_BACK'},{'source':'A','target':'B','relation':'CONTROLS'},{'source':'B','target':'A','relation':'DEPENDS_ON'}]},{'thesis':'An operating system connects strategy, governance, delivery and measurement through feedback.'})
a('GOVERNANCE_SUBSTRING_FALSE_GO_DECISION',feat['decision'] is False,feat)
a('COMMUNICATION_STRATEGY_UNIVERSE_NOT_COLLAPSED',len(STRATEGIES)>=24 and 'SCORECARD_LED' in STRATEGIES,sorted(STRATEGIES))

out={'suite':'Rashad Artifact Intelligence Brain v3.3 Adversarial Red Team','status':'PASS' if all(x['status']=='BLOCKED' for x in att) else 'FAIL','blocked':sum(x['status']=='BLOCKED' for x in att),'total':len(att),'attacks':att}
Path(__file__).with_name('ARTIFACT_BRAIN_V3_RED_TEAM_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 1)
