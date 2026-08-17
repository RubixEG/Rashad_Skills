#!/usr/bin/env python3
from __future__ import annotations
import json,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve(); RUNTIME=HERE.parents[2]; sys.path.insert(0,str(RUNTIME))
from brain.artifact_gate import guard_composer,derive_output_classification,validate_artifact_draft
from brain.knowledge_readiness import detect_knowledge_needs
from brain.ontology import validate_actor_separation,cognitive_job,apply_governor_veto
from brain.confidence import propagate_confidence
from brain.reasoning_pipelines import select_pipelines,pipelines
from brain.dynamic_councils import compose_dynamic_council
from brain.visual_memory import variety_check
from brain.provider import NoExecutionProvider, ScriptedTestProvider
from brain.orchestrator import run_brain
from brain.artifact_council_runtime import execute_artifact_councils
from rfp_summary_orchestrator import execute_visual_search

results=[]
def add(name,ok,detail=None): results.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
def artifact_state():
    strategies=['STATEMENT_LED','NUMBER_LED','EVIDENCE_LED','COMPARISON_LED','SYSTEM_LED']; families=['MINIMAL','MINIMAL','ANALYTICAL','ANALYTICAL','RELATIONAL']
    hs=[{'id':f'H{i}','communication_strategy':strategies[i-1],'strategy_family':families[i-1],'structural_signature':f'{strategies[i-1]}|{families[i-1]}|PAGE|{i}'} for i in range(1,6)]
    rs=[{'candidate_id':f'H{i}','actual_render_hash':f'HASH{i}','render_path':f'/tmp/H{i}.png'} for i in range(1,6)]
    provider=ScriptedTestProvider()
    task={'task_id':'BRAIN-UPGRADE-ARTIFACT','rfp_role':'MANAGEMENT_DECISION','critical':True,'rendered':True,'question':'Executive opportunity decision supported by evidence','evidence':[{'id':'E1','source':'fixture'}]}
    brain=run_brain(task,provider)
    graph={'nodes':[{'id':'N1','label':'Evidence'},{'id':'N2','label':'Decision'}],'edges':[{'source':'N1','target':'N2','relation':'SUPPORTS'}]}
    content={'page_id':'P01','thesis':'Executive opportunity decision supported by evidence','answer_first_thesis':'Executive opportunity decision supported by evidence','evidence':['E1'],'language':'AR'}
    pre=execute_artifact_councils(graph,content,provider,'AR','PRE_CONCEPT')
    return {'content_status':'PASS','evidence_status':'PASS','brain_session':brain,'page_contract':{'page_id':'P01'},'cognitive_packet':{'thesis':'x'},'artifact_intent':{'type':'SYSTEM'},'semantic_graph':graph,'evidence_lineage':[{'evidence':'E1','source':'fixture'}],'artifact_council_execution':pre,'hypotheses':hs,'render_evidence':rs,'selected_master':{'candidate_id':'H1','actual_render_hash':'HASH1','selection_authority':'PROVISIONAL_PARTNER_HEURISTIC_NOT_INDEPENDENT','selection_reason':'fit then simplicity'},'brand_preflight':{'status':'PASS','rubix_asset_status':'VERIFIED','client_logo_status':'VERIFIED_OR_EXPLICITLY_UNAVAILABLE'},'qa_state':{'status':'DRAFT_QA_PASS','qa_scope':'ACTUAL_RENDERED_OUTPUT','actual_output_qa_status':'DRAFT_QA_PARTIAL','actual_pixel_visual_quality_status':'NOT_EXECUTED'},'material_claim_ids':['C1'],'claim_visual_bindings':[{'claim_id':'C1','evidence_refs':['E1'],'visual_node_ids':['N1']}], 'parity_status':'NOT_EXECUTED','proof_index_status':'NOT_EXECUTED','independent_judgment':{'status':'NOT_EXECUTED'},'release':{},'_provider':provider,'_content':content}

# Artifact/output-state hard gate
# v7.2 requires executable Brain + PRE_CONCEPT council proof even for an internal concept draft.
raw=artifact_state(); stripped=dict(raw); stripped.pop('brain_session',None); stripped.pop('artifact_council_execution',None)
add('internal_concept_without_execution_proof_blocked',guard_composer(stripped,'INTERNAL_CONCEPT_DRAFT')['status']=='BLOCK_RENDER',guard_composer(stripped,'INTERNAL_CONCEPT_DRAFT'))
s=artifact_state(); add('internal_concept_draft_admitted_with_execution_proof',guard_composer(s,'INTERNAL_CONCEPT_DRAFT')['status']=='PASS',guard_composer(s,'INTERNAL_CONCEPT_DRAFT'))
add('partial_qa_state_classified_internal_only',derive_output_classification(s)=='INTERNAL_CONCEPT_DRAFT',derive_output_classification(s))
add('release_candidate_blocked_without_independent_judge',guard_composer(s,'RELEASE_CANDIDATE')['status']=='BLOCK_RENDER',guard_composer(s,'RELEASE_CANDIDATE'))
add('direct_composer_bypass_blocked',guard_composer({'content_status':'PASS','evidence_status':'PASS'},'USER_VISIBLE_ARTIFACT_DRAFT')['status']=='BLOCK_RENDER',None)
bad=artifact_state(); bad.pop('_provider',None); bad.pop('_content',None); bad['render_evidence']=[{'candidate_id':f'H{i}','actual_render_hash':'SAME','render_path':f'x{i}'} for i in range(1,6)]
add('duplicate_render_hashes_blocked',validate_artifact_draft(bad)['status']=='BLOCKED',validate_artifact_draft(bad))
bad=artifact_state(); bad.pop('_provider',None); bad.pop('_content',None); bad['claim_visual_bindings']=[]
add('claim_visual_evidence_binding_required',validate_artifact_draft(bad)['status']=='BLOCKED',validate_artifact_draft(bad))
bad=artifact_state(); bad.pop('_provider',None); bad.pop('_content',None); bad['brand_preflight']={'status':'PASS','rubix_asset_status':'MISSING'}
add('rubix_brand_preflight_required',validate_artifact_draft(bad)['status']=='BLOCKED',validate_artifact_draft(bad))
rel=artifact_state(); provider=rel.pop('_provider'); content=rel.pop('_content'); graph=rel['semantic_graph']
rel['art_direction_execution']=execute_artifact_councils(graph,content,provider,'AR','ART_DIRECTION',prior={'strategy':'COMPARISON_LED'})
rel['production_council_execution']=execute_artifact_councils(graph,content,provider,'AR','PRODUCTION_READINESS',prior={'strategy':'COMPARISON_LED'})
rel['selected_master']={'candidate_id':'H2','actual_render_hash':'PRODHASH','selection_authority':'INDEPENDENT_JUDGE','render_kind':'PRODUCTION_PAGE_RENDER','production_render_id':'PROD-1'}; rel['independent_judgment']={'status':'PASS','independent':True}; rel['qa_state']={'status':'QA_CANDIDATE_PASS','qa_scope':'ACTUAL_RENDERED_OUTPUT','actual_output_qa_status':'PASS','actual_pixel_visual_quality_status':'PASS','repair_loop_status':'NOT_REQUIRED_FIRST_PASS_PASS'}; rel['parity_status']='PASS'; rel['proof_index_status']='PASS'
add('release_candidate_after_independent_proof',derive_output_classification(rel)=='RELEASE_CANDIDATE',derive_output_classification(rel))
rel['release']={'release_chair_status':'RELEASED','release_authority':'RASHAD_BRAIN_RELEASE_CHAIR'}
add('released_only_by_release_chair',derive_output_classification(rel)=='RELEASED',derive_output_classification(rel))

# Knowledge readiness and missing expertise
kr=detect_knowledge_needs({'question':'Can we offer a fixed price and what is our margin?','strict_mode':True})
add('firm_rates_missing_blocks_final_price',kr['status']=='KNOWLEDGE_READINESS_BLOCK' and any(x['knowledge_pack']=='KP-FIRM-RATES' for x in kr['blockers']),kr)
sap=detect_knowledge_needs({'question':'Design certified SAP integration architecture'})
add('sap_expertise_routed_but_knowledge_not_ready',any(x['sme']=='SME-SAP' and x['knowledge_status']=='KNOWLEDGE_REQUIRED' for x in sap['routed_expertise']),sap)
brain_block=run_brain({'rfp_role':'COMMERCIAL_EXPOSURE','question':'Give final price and margin','strict_mode':True,'critical':True},ScriptedTestProvider())
add('brain_strict_mode_stops_before_producer_on_missing_rates',brain_block.get('release',{}).get('reason')=='KNOWLEDGE_READINESS_BLOCK' and not brain_block.get('invocations'),brain_block.get('release'))

# Ontology
sep=validate_actor_separation('SIM-CFO','SME-PRICING'); add('cfo_simulator_not_pricing_sme',sep['status']=='PASS' and sep['actor_a_type']=='EXECUTIVE_SIMULATOR' and sep['actor_b_type']=='SME',sep)
add('pricing_sme_quantifies', 'QUANTIFY' in cognitive_job('SME-PRICING').get('functions',[]),cognitive_job('SME-PRICING'))
add('governor_veto_is_non_overridable',apply_governor_veto(['COMPOSER_BYPASS'])['status']=='BLOCKED' and apply_governor_veto(['COMPOSER_BYPASS'])['override_allowed'] is False,apply_governor_veto(['COMPOSER_BYPASS']))

# Confidence propagation
cp=propagate_confidence({'EFFORT':{'confidence':0.55},'COST':{'confidence':0.90,'depends_on':['EFFORT']},'MARGIN':{'confidence':0.95,'depends_on':['COST']}})
add('cost_confidence_capped_by_effort',cp['COST']['effective_confidence']==0.55,cp)
add('margin_confidence_capped_by_cost',cp['MARGIN']['effective_confidence']==0.55,cp)

# Reasoning pipelines and dynamic councils
sel=select_pipelines({'question':'AI platform APIs data integration cyber cloud plus BOQ price margin payment'})
add('technical_pipeline_selected','TECHNICAL_SOLUTION' in sel['selected'],sel['selected'])
add('financial_pipeline_selected','FINANCIAL_COMMERCIAL' in sel['selected'],sel['selected'])
add('technical_pipeline_has_tradeoffs_and_acceptance','TRADE_OFF_ANALYSIS' in pipelines()['TECHNICAL_SOLUTION'] and 'ACCEPTANCE' in pipelines()['TECHNICAL_SOLUTION'],None)
add('financial_pipeline_has_working_capital_and_sensitivity','WORKING_CAPITAL' in pipelines()['FINANCIAL_COMMERCIAL'] and 'SENSITIVITY' in pipelines()['FINANCIAL_COMMERCIAL'],None)
dc=compose_dynamic_council({'question':'AI architecture fixed price margin and delivery capacity'})
add('dynamic_council_bounded',dc['actor_count']<=dc.get('max_actors',14)<=14 and dc['constitutional_councils_replaced'] is False,dc)
add('dynamic_council_cross_functional','SIM-CFO' in dc['actors'] and ('SME-TECH-ARCH' in dc['actors'] or 'SME-PRICING' in dc['actors']),dc)

# Visual memory
cur={'dominant_form':'RING','reading_path':'RTL_SPINE','focal_point':'RIGHT','topology':'LOOP','structural_signature':'A'}
add('visual_variety_memory_blocks_immediate_twin',variety_check(cur,[cur])['status']=='BLOCKED',variety_check(cur,[cur]))
add('visual_variety_memory_allows_change',variety_check(cur,[{'dominant_form':'SPINE','reading_path':'CENTER_OUT','focal_point':'CENTER','topology':'CHAIN','structural_signature':'B'}])['status']=='PASS',None)

# Critical fix: missing live judge must not suppress actual artifact draft generation
graph=json.loads((RUNTIME.parents[2]/'QA/Runtime/fixtures/graph.json').read_text(encoding='utf-8')) if (RUNTIME.parents[2]/'QA/Runtime/fixtures/graph.json').exists() else None
# package-relative fallback
if graph is None:
    graph={'schema_version':'6.0','engagement_id':'TEST','page_id':'P01','nodes':[{'id':'N1','type':'PROCESS','label':'A','evidence':['E1'],'importance':.8},{'id':'N2','type':'DECISION','label':'B','evidence':['E1'],'importance':1.0},{'id':'N3','type':'PROCESS','label':'C','evidence':['E1'],'importance':.8}], 'edges':[{'id':'E1','source':'N1','target':'N2','relation':'FLOWS_TO','evidence':['E1']},{'id':'E2','source':'N2','target':'N3','relation':'APPROVES','evidence':['E1']}], 'provenance':{'derived_from':['fixture'],'derived_at':'2026-08-16T00:00:00Z'}}
content={'thesis':'One integrated operating system','evidence':['E1'],'sources':['E1']}
with tempfile.TemporaryDirectory() as td:
    vr=execute_visual_search('P01',graph,content,td,judge_provider=NoExecutionProvider())
add('visual_search_without_live_judge_returns_internal_concept_draft',vr.get('status')=='INTERNAL_CONCEPT_DRAFT_READY' and len(vr.get('renders',[]))==5 and vr.get('draft_master',{}).get('actual_render_hash'),{'status':vr.get('status'),'renders':len(vr.get('renders',[])),'selection_status':vr.get('selection_status')})
add('visual_search_concept_truthfully_not_user_visible',vr.get('independent_release_ready') is False and vr.get('selection_status')=='PROVISIONAL_CONCEPT_NOT_USER_VISIBLE',vr.get('selection_status'))

# Firm model truth
firm=json.loads((RUNTIME.parent/'config/firm_model.json').read_text(encoding='utf-8'))
add('firm_model_is_not_hallucinated',firm['status']=='KNOWLEDGE_REQUIRED' and all(v['status']=='KNOWLEDGE_REQUIRED' for v in firm['cells'].values()),firm['status'])

out={'suite':'Rashad Final Brain + Artifact Admission Upgrade','brain_version':'3.3.0','status':'PASS' if all(x['status']=='PASS' for x in results) else 'FAIL','passed':sum(x['status']=='PASS' for x in results),'total':len(results),'tests':results}
Path(__file__).with_name('FINAL_BRAIN_UPGRADE_CERTIFICATION_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 1)
