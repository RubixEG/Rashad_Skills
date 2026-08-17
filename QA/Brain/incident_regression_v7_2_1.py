#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json,sys,tempfile,copy
ROOT=Path(__file__).resolve().parents[2]; REG=ROOT/'QA/Runtime/fixtures/incidents/INCIDENT_REGISTRY_20260816.json'
sys.path.insert(0,str(ROOT/'Rashad/Brain/runtime'));sys.path.insert(0,str(ROOT/'QA/Brain'))
from brain.actual_output_qa import evaluate_page_output
from brain.delivery_gate import validate_user_visible_delivery
from brain.product_inspector import inspect_pptx,sha256_file
from brain.exact_handoff import verify_exact_artifact_handoff
from brain.expert_router import route_experts
from brain.artifact_brain import STRATEGIES
from delivery_test_fixtures_v7_2 import png,bad_pptx
from run_v7_2_user_visible_delivery_certification import executable_page
OUT=ROOT/'QA/Certification/INCIDENT_REGRESSION_V7_2_1.json'

def add(t,n,ok,d=None): t.append({'name':n,'status':'PASS' if ok else 'FAIL','detail':d})
def main():
 r=json.loads(REG.read_text(encoding='utf-8')); incidents=r.get('incidents') or []; tests=[]; ids=[x.get('id') for x in incidents]
 add(tests,'incident_registry_unique_and_complete',len(ids)==len(set(ids)) and len(ids)>=16,len(ids))
 add(tests,'every_incident_is_P0_with_regression_mapping',all(x.get('severity')=='P0' and x.get('regression') for x in incidents))
 with tempfile.TemporaryDirectory() as td:
  td=Path(td); rp=td/'p.png';png(rp,'page'); p,_,_=executable_page(1,'STATEMENT_LED',rp)
  x=copy.deepcopy(p);x['render_kind']='COMMUNICATION_STRATEGY_CONCEPT_RENDER_V3';add(tests,'concept_wireframe_never_user_visible',evaluate_page_output(x,'USER_VISIBLE_ARTIFACT_DRAFT')['status']=='BLOCKED')
  x=copy.deepcopy(p);x['actual_pixel_review']={'status':'NOT_EXECUTED'};add(tests,'missing_pixel_review_never_user_visible',evaluate_page_output(x,'USER_VISIBLE_ARTIFACT_DRAFT')['status']=='BLOCKED')
  x=copy.deepcopy(p);x['repair_required']=True;x['repair_history']=[];add(tests,'unclosed_repair_never_user_visible',evaluate_page_output(x,'USER_VISIBLE_ARTIFACT_DRAFT')['status']=='BLOCKED')
  bad=td/'bad.pptx';bad_pptx(bad);bi=inspect_pptx(bad);add(tests,'shape_only_card_output_blocked',bi['status']=='BLOCKED',bi.get('blockers'))
  # A dossier with labels but no executable proof must never deliver.
  dh=sha256_file(bad);d={'classification':'USER_VISIBLE_ARTIFACT_DRAFT','output_file_sha256':dh,'montage_sha256':'0'*64,'pages':[{'page_id':'P1','brain_cognitive_lock_status':'PASS','expert_execution_status':'PASS','artifact_council_execution_status':'PASS','art_direction_execution_status':'PASS','production_council_execution_status':'PASS'}],'artifact_brain_execution_status':'PASS','deck_artifact_council_execution':{'status':'PASS'},'production_render_status':'PASS','actual_output_qa_closed_loop_status':'PASS','deck_pixel_review':{},'framework_certification_substitute':False}
  add(tests,'labels_without_execution_proof_never_deliver',validate_user_visible_delivery(d,bad)['status']=='BLOCK_DELIVERY')
 # I16 exact wrong-artifact handoff regression using the preserved real incident fixture.
 f=ROOT/'QA/Runtime/fixtures/incidents/I16_WRONG_ARTIFACT_HANDOFF_20260817'
 hv=verify_exact_artifact_handoff(f/'bad_delivered_14_slide_deck.pptx',f/'bad_delivery_dossier_24_page.json',trace_path=f/'bad_trace_24_page_claim.md')
 req={'DELIVERED_PPTX_SHA_MISMATCH_DOSSIER','DELIVERED_SLIDE_COUNT_MISMATCH_DOSSIER_PAGES','FINAL_TRACE_DESCRIBES_DIFFERENT_PAGE_COUNT_THAN_DELIVERED_FILE','IMAGE_LED_DECLARED_BUT_IMAGES_APPEAR_LOGO_ONLY'}
 add(tests,'i16_wrong_artifact_handoff_permanently_blocked',hv.get('status')=='BLOCK_HANDOFF' and req<=set(hv.get('blockers',[])),hv.get('blockers'))
 # Semantic key-name false routing incident.
 rr=route_experts({'task_id':'K','rfp_role':'MANAGEMENT_DECISION','critical':True,'sap_procurement_cyber_key':'ordinary management strategy only','payload':{'oracle_ai_key':'management only'}})
 forbidden={'SAP','ORACLE','CYBER_PRIVACY','AI_DATA'}
 add(tests,'metadata_key_names_do_not_trigger_expertise',not(forbidden & set(rr.get('matched_domains',[]))),rr.get('matched_domains'))
 # Current governance invariants.
 m=json.loads((ROOT/'Rashad/Skill/ACTIVE_AUTHORITY_MANIFEST.json').read_text(encoding='utf-8'))
 add(tests,'current_manifest_v7_2',m.get('version')=='7.2.1' and m.get('certification_harness','').endswith('verify_skill_v7_2_1.py'))
 add(tests,'decision_and_artifact_workflows_both_bound',m.get('rfp_summary_current_workflow','').endswith('23_V7_RFP_SUMMARY_DECISION_WORKFLOW.md') and m.get('rfp_summary_artifact_delivery_workflow','').endswith('24_V7_1_RFP_SUMMARY_ARTIFACT_DELIVERY_WORKFLOW.md'))
 add(tests,'concept_render_internal_only',m.get('artifact_concept_render_policy')=='INTERNAL_ONLY_NEVER_USER_VISIBLE_MASTER')
 add(tests,'golden_acceptance_required',m.get('golden_real_rfp_acceptance')=='REQUIRED_FOR_ARTIFACT_QA_INTEGRATION_RELEASE')
 art=json.loads((ROOT/'Rashad/Brain/config/artifact_brain_expert_universe_v3.json').read_text(encoding='utf-8'))
 add(tests,'strategy_registry_exact_24_runtime_parity',len(STRATEGIES)==24 and set(art.get('communication_strategy_universe',[]))==set(STRATEGIES),{'runtime':len(STRATEGIES),'registry':len(art.get('communication_strategy_universe',[]))})
 actors=json.loads((ROOT/'Rashad/Brain/config/actor_ontology.json').read_text(encoding='utf-8'))['actors'];rules=json.loads((ROOT/'Rashad/Brain/config/brain_expert_routing_rules.json').read_text(encoding='utf-8'))
 allids={a['id'] for a in actors};refs=set(rules.get('core_roles',[]))|set(rules.get('mandatory_governors_for_critical',[]));
 for v in rules.get('role_rules',{}).values():refs.update(v)
 for q in rules.get('domain_rules',[]):refs.update(q.get('roles',[]))
 add(tests,'all_69_registered_brain_actors_reachable',len(allids)==69 and allids==refs,{'actors':len(allids),'reachable':len(refs),'unreachable':sorted(allids-refs)})
 add(tests,'artifact_20_councils_107_roles_24_strategies',len(art.get('councils',[]))==20 and len(art.get('roles',[]))==107 and len(art.get('communication_strategy_universe',[]))==24)
 qa=json.loads((ROOT/'QA/Brain/councils.json').read_text(encoding='utf-8'));add(tests,'qa_14_councils',len(qa.get('councils',[]))==14)
 fv=(ROOT/'QA/FINAL_VERIFY.py').read_text(encoding='utf-8');add(tests,'final_verifier_directory_inode_lock_file_logged_fail_closed',all(x in fv for x in ['LOCK_FD=os.open(str(CERT), os.O_RDONLY)','fcntl.flock(LOCK_FD, fcntl.LOCK_EX | fcntl.LOCK_NB)','stdout=fo','stderr=fe','LOGDIR.mkdir(parents=True,exist_ok=True)']) and '.final_verify.lock' not in fv and 'capture_output=True' not in fv)
 # Current dedicated evidence files must be present and PASS when this suite runs near package close.
 for rel,nm in [('QA/Certification/V7_2_BRAIN_COHERENCE_AUDIT.json','brain_coherence_evidence_pass'),('QA/Certification/V7_2_BRAIN_COHERENCE_STRESS.json','brain_stress_evidence_pass'),('QA/Certification/V7_2_GOLDEN_REDF_ACCEPTANCE.json','golden_redf_evidence_pass')]:
  p=ROOT/rel;ok=p.exists() and json.loads(p.read_text(encoding='utf-8')).get('status')=='PASS';add(tests,nm,ok)
 st='PASS' if all(x['status']=='PASS' for x in tests) else 'FAIL';out={'suite':'Rashad v7.2.1 Incident Regression Registry','status':st,'incident_count':len(incidents),'passed':sum(x['status']=='PASS' for x in tests),'total':len(tests),'tests':tests};OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'suite':out['suite'],'status':st,'incident_count':len(incidents),'passed':out['passed'],'total':out['total'],'failed':[x for x in tests if x['status']!='PASS']},ensure_ascii=False,indent=2));return 0 if st=='PASS' else 2
if __name__=='__main__':raise SystemExit(main())
