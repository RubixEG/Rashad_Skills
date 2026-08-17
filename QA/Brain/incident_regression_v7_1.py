#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json,sys,tempfile,copy
ROOT=Path(__file__).resolve().parents[2]
REG=ROOT/'QA/Runtime/fixtures/incidents/INCIDENT_REGISTRY_20260816.json'
sys.path.insert(0,str(ROOT/'Rashad/Brain/runtime'))
sys.path.insert(0,str(ROOT/'QA/Brain'))
from brain.actual_output_qa import evaluate_page_output
from brain.delivery_gate import validate_user_visible_delivery
from brain.product_inspector import inspect_pptx,sha256_file
from run_v7_1_user_visible_delivery_certification import png,good_pptx,bad_pptx,page

OUT=ROOT/'QA/Certification/INCIDENT_REGRESSION_V7_1.json'

def main():
    r=json.loads(REG.read_text(encoding='utf-8')); tests=[]
    incidents=r.get('incidents') or []
    ids=[x.get('id') for x in incidents]
    tests.append({'name':'registry_unique_ids','status':'PASS' if len(ids)==len(set(ids)) and len(ids)>=12 else 'FAIL'})
    tests.append({'name':'every_incident_has_regression_mapping','status':'PASS' if all(x.get('severity')=='P0' and x.get('regression') for x in incidents) else 'FAIL'})
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); hero=td/'h.png'; png(hero,'hero'); ppt=td/'good.pptx'; good_pptx(ppt,hero)
        rp=td/'p.png'; png(rp,'page'); p=page(1,'STATEMENT_LED',rp)
        # I02/I06/I07: concept, missing pixel, missing repair remain blocked
        x=copy.deepcopy(p); x['render_kind']='COMMUNICATION_STRATEGY_CONCEPT_RENDER_V3'
        tests.append({'name':'concept_wireframe_never_user_visible','status':'PASS' if evaluate_page_output(x,'USER_VISIBLE_ARTIFACT_DRAFT')['status']=='BLOCKED' else 'FAIL'})
        x=copy.deepcopy(p); x['actual_pixel_review']={'status':'NOT_EXECUTED'}
        tests.append({'name':'missing_pixel_review_never_user_visible','status':'PASS' if evaluate_page_output(x,'USER_VISIBLE_ARTIFACT_DRAFT')['status']=='BLOCKED' else 'FAIL'})
        x=copy.deepcopy(p); x['repair_required']=True; x['repair_history']=[]
        tests.append({'name':'repair_required_without_history_blocked','status':'PASS' if evaluate_page_output(x,'USER_VISIBLE_ARTIFACT_DRAFT')['status']=='BLOCKED' else 'FAIL'})
        # I03/I08: actual product structure must defeat labels/shape-only collapse
        bad=td/'bad.pptx'; bad_pptx(bad)
        bi=inspect_pptx(bad)
        tests.append({'name':'shape_only_bad_redf_profile_blocked','status':'PASS' if bi['status']=='BLOCKED' and any(b in bi['blockers'] for b in ('PPTX_SHAPE_ONLY_ANALYTICAL_DECK_OVERUSE','PPTX_STRUCTURAL_MONOTONY')) else 'FAIL','detail':bi.get('blockers')})
        exp=[]
        for i,s in enumerate(['IMAGE_LED','CHART_LED','TABLE_LED','NUMBER_LED'],1):
            q=copy.deepcopy(p); q['page_id']=f'P{i:02d}'; q['selected_strategy']=s; q['hero_metric_proven']=(s=='NUMBER_LED'); q['structured_grid_rendered']=False; exp.append(q)
        si=inspect_pptx(bad,exp)
        tests.append({'name':'strategy_label_cannot_fake_actual_product_objects','status':'PASS' if si['status']=='BLOCKED' and any(('WITHOUT_' in b) for b in si['blockers']) else 'FAIL','detail':si.get('blockers')})
        # I01/I05: dossier without actual artifact execution / framework substitution blocked
        dh=sha256_file(ppt)
        dossier={'schema':'RASHAD_USER_VISIBLE_ARTIFACT_DELIVERY_V1','classification':'USER_VISIBLE_ARTIFACT_DRAFT','output_file_sha256':dh,'montage_sha256':'0'*64,'pages':[],'artifact_brain_execution_status':'NOT_EXECUTED','production_render_status':'PASS','actual_output_qa_closed_loop_status':'PASS','deck_pixel_review':{},'framework_certification_substitute':False,'independent_judgment_status':'NOT_EXECUTED','parity_status':'NOT_EXECUTED','proof_index_status':'NOT_EXECUTED','release':{}}
        tests.append({'name':'direct_output_without_artifact_execution_blocked','status':'PASS' if validate_user_visible_delivery(dossier,ppt)['status']=='BLOCK_DELIVERY' else 'FAIL'})
        dossier['artifact_brain_execution_status']='PASS'; dossier['framework_certification_substitute']=True
        tests.append({'name':'framework_qa_substitution_blocked','status':'PASS' if validate_user_visible_delivery(dossier,ppt)['status']=='BLOCK_DELIVERY' else 'FAIL'})
    # I09-I12 static current-policy invariants
    manifest=json.loads((ROOT/'Rashad/Skill/ACTIVE_AUTHORITY_MANIFEST.json').read_text(encoding='utf-8'))
    tests.append({'name':'current_manifest_v7_1','status':'PASS' if manifest.get('version')=='7.1.0' and manifest.get('certification_harness','').endswith('verify_skill_v7_1.py') else 'FAIL'})
    tests.append({'name':'current_decision_workflow_v7','status':'PASS' if manifest.get('rfp_summary_current_workflow','').endswith('23_V7_RFP_SUMMARY_DECISION_WORKFLOW.md') else 'FAIL'})
    tests.append({'name':'current_artifact_delivery_workflow_v7_1','status':'PASS' if manifest.get('rfp_summary_artifact_delivery_workflow','').endswith('24_V7_1_RFP_SUMMARY_ARTIFACT_DELIVERY_WORKFLOW.md') else 'FAIL'})
    tests.append({'name':'concept_internal_only_policy_locked','status':'PASS' if manifest.get('artifact_concept_render_policy')=='INTERNAL_ONLY_NEVER_USER_VISIBLE_MASTER' else 'FAIL'})
    tests.append({'name':'golden_acceptance_required','status':'PASS' if manifest.get('golden_real_rfp_acceptance')=='REQUIRED_FOR_ARTIFACT_QA_INTEGRATION_RELEASE' else 'FAIL'})
    sys.path.insert(0,str(ROOT/'Rashad/Brain/runtime'))
    from brain.artifact_brain import STRATEGIES
    expert=json.loads((ROOT/'Rashad/Brain/config/artifact_brain_expert_universe_v3.json').read_text(encoding='utf-8'))
    tests.append({'name':'artifact_strategy_registry_matches_runtime','status':'PASS' if len(STRATEGIES)==24 and set(expert.get('communication_strategy_universe',[]))==set(STRATEGIES) else 'FAIL','detail':{'runtime':sorted(STRATEGIES),'registry':sorted(expert.get('communication_strategy_universe',[]))}})
    fv=(ROOT/'QA/FINAL_VERIFY.py').read_text(encoding='utf-8')
    tests.append({'name':'final_verifier_orchestration_is_file_logged_locked_and_logdir_resilient','status':'PASS' if all(x in fv for x in ['fcntl.flock','stdout=fo','stderr=fe','LOGDIR.mkdir(parents=True,exist_ok=True)']) and 'capture_output=True' not in fv else 'FAIL'})
    rv3=(ROOT/'QA/Runtime/run_regression_v3.py').read_text(encoding='utf-8')
    rv31=(ROOT/'QA/Runtime/run_regression_v31.py').read_text(encoding='utf-8')
    tests.append({'name':'regression_roots_cleaned_before_each_run','status':'PASS' if "shutil.rmtree(HERE/'_regression', ignore_errors=True)" in rv3 and "shutil.rmtree(HERE/'_regression_v31', ignore_errors=True)" in rv31 else 'FAIL'})
    st='PASS' if all(t['status']=='PASS' for t in tests) else 'FAIL'
    out={'suite':'Rashad v7.1 Incident Regression Registry','status':st,'incident_count':len(incidents),'passed':sum(t['status']=='PASS' for t in tests),'total':len(tests),'tests':tests}
    OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'suite':out['suite'],'status':st,'incident_count':out['incident_count'],'passed':out['passed'],'total':out['total'],'failed':[t for t in tests if t['status']!='PASS']},ensure_ascii=False,indent=2))
    return 0 if st=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
