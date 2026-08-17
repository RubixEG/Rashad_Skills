#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys,json,tempfile,copy
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Rashad/Brain/runtime')); sys.path.insert(0,str(Path(__file__).parent))
from brain.orchestrator import run_brain
from brain.provider import ScriptedTestProvider
from brain.execution_proof import validate_brain_execution_proof, validate_artifact_execution_ledger
from brain.artifact_council_runtime import execute_artifact_councils
from brain.actual_output_qa import evaluate_page_output,evaluate_deck_output
from brain.product_inspector import inspect_pptx,sha256_file
from brain.delivery_gate import validate_user_visible_delivery
from brain.artifact_gate import guard_composer
from delivery_test_fixtures_v7_2 import png,review,hyps,bad_pptx,page
from production_test_fixtures_v7_3 import build_production_projection
OUT=ROOT/'QA/Certification'; OUT.mkdir(exist_ok=True)

def rec(arr,name,ok,detail=None): arr.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})

def executable_page(i,strategy,render_path):
    pg=page(i,strategy,render_path)
    question=f'REDF page {i}: {strategy} decision evidence AI cybersecurity commercial delivery'
    task={'task_id':f'V72-P{i:02d}','rfp_role':'MANAGEMENT_DECISION','critical':True,'rendered':True,'deck_level':False,'question':question,'evidence':[{'id':'E1','source':'golden-fixture'}]}
    provider=ScriptedTestProvider(); brain=run_brain(task,provider)
    graph={'nodes':[{'id':'N1','label':'Evidence'},{'id':'N2','label':'Decision'}],'edges':[{'source':'N1','target':'N2','relation':'SUPPORTS'}]}
    content={'page_id':pg['page_id'],'thesis':question,'answer_first_thesis':question,'evidence':['E1'],'language':'AR','numbers':[87.5,70,80] if strategy in {'NUMBER_LED','CHART_LED','SCORECARD_LED'} else []}
    pre=execute_artifact_councils(graph,content,provider,'AR','PRE_CONCEPT')
    art=execute_artifact_councils(graph,content,provider,'AR','ART_DIRECTION',prior={'strategy':strategy})
    prod=execute_artifact_councils(graph,content,provider,'AR','PRODUCTION_READINESS',prior={'strategy':strategy})
    pg.update({
      'brain_session_execution_evidence':brain,
      'expert_execution_ledger':brain.get('expert_execution_ledger'),
      'brain_cognitive_lock_status':'PASS' if brain.get('state')=='COGNITIVE_LOCKED' else 'BLOCKED',
      'expert_execution_status':'PASS' if (brain.get('expert_execution_ledger') or {}).get('status')=='PASS' else 'BLOCKED',
      'artifact_council_execution':pre,'artifact_council_execution_status':pre.get('status'),
      'art_direction_execution':art,'art_direction_execution_status':art.get('status'),
      'production_council_execution':prod,'production_council_execution_status':prod.get('status'),
      'material_claim_ids':[],'claim_visual_bindings':[]
    })
    return pg,graph,content

def main():
    tests=[]
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        strategies=['IMAGE_LED','STATEMENT_LED','NUMBER_LED','TABLE_LED','CHART_LED','PROCESS_LED','COMPARISON_LED','DECISION_LED']
        projection=build_production_projection(td/'production',strategies)
        if projection.get('status')!='PASS':
            raise RuntimeError('v7.3 production fixture failed: '+repr(projection))
        ppt=Path(projection['pptx_path']); montage=Path(projection['montage_path'])
        pages=[]; all_proofs=[]
        for i,s in enumerate(strategies,1):
            rp=Path(projection['page_images'][i-1]); pg,g,c=executable_page(i,s,rp)
            proof=projection['pages'][i-1]; render=projection['renders'][i-1]
            pg.update(proof)
            pg.update({
              'selected_render_hash':render['actual_render_hash'],
              'production_render_id':render['production_render_id'],
              'render_kind':'PRODUCTION_PAGE_RENDER',
              'actual_pixel_review':review(render['actual_render_hash'],score=94),
            })
            pages.append(pg); all_proofs.append((pg,g,c))
        dh=sha256_file(ppt); mh=sha256_file(montage)
        deck_graph={'nodes':[{'id':'D1'},{'id':'D2'}],'edges':[{'source':'D1','target':'D2','relation':'SEQUENCES'}]}
        deck_content={'page_id':'DECK','thesis':'REDF executive decision narrative','evidence':['E1'],'language':'AR'}
        deck_exec=execute_artifact_councils(deck_graph,deck_content,ScriptedTestProvider(),'AR','DECK_REVIEW')
        deck_review={'status':'PASS','independent':True,'review_id':'DECK-V72','actor_id':'QA-DECK-INDEPENDENT','deck_sha256':dh,'montage_sha256':mh,'scores':{k:94 for k in ['narrative_rhythm','visual_variety','executive_coherence','cross_page_specificity','density_rhythm','brand_consistency','rtl_consistency','overall_partner_grade']},'generic_deck_swap_test':'PASS','diagram_overuse_test':'PASS','hard_blockers':[]}
        product=inspect_pptx(ppt,pages); rec(tests,'good_varied_pptx_product_inspection',product['status']=='PASS',product.get('blockers'))
        rec(tests,'all_pages_have_recomputed_brain_proof',all(validate_brain_execution_proof(p['brain_session_execution_evidence'])['status']=='PASS' for p in pages))
        rec(tests,'all_pages_have_executed_preconcept_councils',all(validate_artifact_execution_ledger(p['artifact_council_execution'],'PRE_CONCEPT')['status']=='PASS' for p in pages))
        rec(tests,'all_pages_have_executed_art_direction_councils',all(validate_artifact_execution_ledger(p['art_direction_execution'],'ART_DIRECTION')['status']=='PASS' for p in pages))
        rec(tests,'all_pages_have_executed_production_councils',all(validate_artifact_execution_ledger(p['production_council_execution'],'PRODUCTION_READINESS')['status']=='PASS' for p in pages))
        rec(tests,'deck_review_council_executed',validate_artifact_execution_ledger(deck_exec,'DECK_REVIEW')['status']=='PASS')
        dq=evaluate_deck_output(pages,'USER_VISIBLE_ARTIFACT_DRAFT',deck_review,dh,mh,product); rec(tests,'good_actual_output_qa_pass',dq['status']=='PASS',dq.get('blockers'))
        dossier={'schema':'RASHAD_USER_VISIBLE_ARTIFACT_DELIVERY_V2','classification':'USER_VISIBLE_ARTIFACT_DRAFT','output_file_sha256':dh,'montage_sha256':mh,'pages':pages,'artifact_brain_execution_status':'PASS','deck_artifact_council_execution':deck_exec,'production_render_status':'PASS','actual_output_qa_closed_loop_status':'PASS','deck_pixel_review':deck_review,'product_inspection':product,'framework_certification_substitute':False,'independent_judgment_status':'NOT_EXECUTED','parity_status':'NOT_EXECUTED','proof_index_status':'NOT_EXECUTED','release':{}}
        dg=validate_user_visible_delivery(dossier,ppt); rec(tests,'good_exact_file_delivery_allowed',dg['status']=='DELIVERY_ALLOWED',dg.get('blockers'))
        # Proof-forgery and bypass attacks.
        bad=copy.deepcopy(dossier); bad['pages'][0]['brain_session_execution_evidence']={'state':'COGNITIVE_LOCKED','coverage':{'status':'PASS'},'expert_execution_ledger':{'status':'PASS'}}
        rec(tests,'fake_brain_pass_string_cannot_substitute_invocations',validate_user_visible_delivery(bad,ppt)['status']=='BLOCK_DELIVERY')
        bad=copy.deepcopy(dossier); bad['pages'][0]['artifact_council_execution']={'status':'PASS','stage':'PRE_CONCEPT'}
        rec(tests,'fake_artifact_council_pass_string_blocked',validate_user_visible_delivery(bad,ppt)['status']=='BLOCK_DELIVERY')
        bad=copy.deepcopy(dossier); bad['pages'][0]['art_direction_execution']={'status':'PASS','stage':'ART_DIRECTION'}
        rec(tests,'fake_art_direction_pass_string_blocked',validate_user_visible_delivery(bad,ppt)['status']=='BLOCK_DELIVERY')
        bad=copy.deepcopy(dossier); bad['pages'][0]['production_council_execution']={'status':'PASS','stage':'PRODUCTION_READINESS'}
        rec(tests,'fake_production_council_pass_string_blocked',validate_user_visible_delivery(bad,ppt)['status']=='BLOCK_DELIVERY')
        bad=copy.deepcopy(dossier); bad['deck_artifact_council_execution']={'status':'NOT_EXECUTED'}
        rec(tests,'missing_deck_artifact_council_blocks',validate_user_visible_delivery(bad,ppt)['status']=='BLOCK_DELIVERY')
        bad=copy.deepcopy(dossier); bad['framework_certification_substitute']=True
        rec(tests,'framework_certification_cannot_substitute_output_qa',validate_user_visible_delivery(bad,ppt)['status']=='BLOCK_DELIVERY')
        bad=copy.deepcopy(dossier); bad['output_file_sha256']='0'*64
        rec(tests,'exact_file_hash_mismatch_blocks',validate_user_visible_delivery(bad,ppt)['status']=='BLOCK_DELIVERY')
        bad=copy.deepcopy(dossier); bad['pages'][0]['artifact_truth_score']=89; bad['pages'][0]['actual_pixel_review']['artifact_truth_score']=89
        rec(tests,'artifact_truth_89_blocks_delivery',validate_user_visible_delivery(bad,ppt)['status']=='BLOCK_DELIVERY')
        bad=copy.deepcopy(dossier); bad['pages'][0]['ceqs_score']=89; bad['pages'][0]['actual_pixel_review']['ceqs_score']=89; bad['pages'][0]['actual_pixel_review']['ceqs']=89
        rec(tests,'ceqs_89_blocks_delivery',validate_user_visible_delivery(bad,ppt)['status']=='BLOCK_DELIVERY')
        # Pixel / concept / repair protections remain active.
        x=copy.deepcopy(pages[1]); x['render_kind']='COMMUNICATION_STRATEGY_CONCEPT_RENDER_V3'; rec(tests,'concept_render_never_user_visible',evaluate_page_output(x,'USER_VISIBLE_ARTIFACT_DRAFT')['status']=='BLOCKED')
        x=copy.deepcopy(pages[1]); x['actual_pixel_review']={'status':'NOT_EXECUTED'}; rec(tests,'missing_pixel_review_blocks',evaluate_page_output(x,'USER_VISIBLE_ARTIFACT_DRAFT')['status']=='BLOCKED')
        x=copy.deepcopy(pages[1]); x['repair_required']=True; x['repair_history']=[]; rec(tests,'repair_not_closed_blocks',evaluate_page_output(x,'USER_VISIBLE_ARTIFACT_DRAFT')['status']=='BLOCKED')
        bp=td/'bad.pptx'; bad_pptx(bp); insp=inspect_pptx(bp); rec(tests,'generic_shape_card_deck_blocked',insp['status']=='BLOCKED',insp.get('blockers'))
        # Internal concept may exist, but direct user-visible promotion remains forbidden.
        state={'content_status':'PASS','evidence_status':'PASS','page_contract':{'page_id':'P'},'cognitive_packet':{'x':1},'artifact_intent':{'x':1},'semantic_graph':{'x':1},'hypotheses':hyps(),'render_evidence':[{'actual_render_hash':str(i)*64} for i in range(1,6)]}
        rec(tests,'internal_concept_stage_is_not_user_visible',guard_composer(state,'USER_VISIBLE_ARTIFACT_DRAFT')['status']=='BLOCK_RENDER')
    out={'suite':'Rashad v7.2 User-Visible Artifact Delivery Certification','status':'PASS' if all(x['status']=='PASS' for x in tests) else 'FAIL','passed':sum(x['status']=='PASS' for x in tests),'total':len(tests),'tests':tests}
    (OUT/'V7_2_USER_VISIBLE_DELIVERY_CERTIFICATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'suite':out['suite'],'status':out['status'],'passed':out['passed'],'total':out['total'],'failed':[x for x in tests if x['status']!='PASS']},ensure_ascii=False,indent=2))
    return 0 if out['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
