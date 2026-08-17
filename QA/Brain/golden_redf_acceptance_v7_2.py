#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys,json,tempfile
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Rashad/Brain/runtime')); sys.path.insert(0,str(Path(__file__).parent))
from brain.provider import ScriptedTestProvider
from brain.artifact_council_runtime import execute_artifact_councils
from brain.execution_proof import validate_artifact_execution_ledger,validate_brain_execution_proof
from brain.product_inspector import inspect_pptx,sha256_file
from brain.actual_output_qa import evaluate_deck_output
from brain.delivery_gate import validate_user_visible_delivery
from golden_redf_fixture_v7_2 import build,bad_pptx
from delivery_test_fixtures_v7_2 import png,review
from production_test_fixtures_v7_3 import build_production_projection
from run_v7_2_user_visible_delivery_certification import executable_page
OUT=ROOT/'QA/Certification'

def main():
  with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    strategies=['IMAGE_LED','DECISION_LED','NUMBER_LED','SYSTEM_LED','EVIDENCE_LED','ARCHITECTURE_LED','TABLE_LED','JOURNEY_LED','STATEMENT_LED','CHART_LED','COMPARISON_LED','MATRIX_LED','SCORECARD_LED','PROCESS_LED']
    projection=build_production_projection(td/'production',strategies)
    if projection.get('status')!='PASS': raise RuntimeError('golden v7.3 production fixture failed: '+repr(projection))
    ppt=Path(projection['pptx_path']); montage=Path(projection['montage_path'])
    pages=[]
    for i,st in enumerate(strategies,1):
      rp=Path(projection['page_images'][i-1]); pg,_,_=executable_page(i,st,rp)
      proof=projection['pages'][i-1]; render=projection['renders'][i-1]
      pg.update(proof); pg.update({'selected_render_hash':render['actual_render_hash'],'production_render_id':render['production_render_id'],'render_kind':'PRODUCTION_PAGE_RENDER','actual_pixel_review':review(render['actual_render_hash'],score=95),'structured_grid_rendered':st=='MATRIX_LED'})
      pages.append(pg)
    dh=sha256_file(ppt);mh=sha256_file(montage)
    deck_graph={'nodes':[{'id':'D1'},{'id':'D2'}],'edges':[{'source':'D1','target':'D2','relation':'SEQUENCES'}]}
    deck_content={'page_id':'DECK','thesis':'REDF executive opportunity decision narrative','evidence':['E1'],'language':'AR'}
    deck_exec=execute_artifact_councils(deck_graph,deck_content,ScriptedTestProvider(),'AR','DECK_REVIEW')
    dr={'status':'PASS','independent':True,'review_id':'GOLDEN-V72-DECK','actor_id':'QA-GOLDEN-INDEPENDENT','deck_sha256':dh,'montage_sha256':mh,'scores':{k:95 for k in ['narrative_rhythm','visual_variety','executive_coherence','cross_page_specificity','density_rhythm','brand_consistency','rtl_consistency','overall_partner_grade']},'generic_deck_swap_test':'PASS','diagram_overuse_test':'PASS','hard_blockers':[]}
    product=inspect_pptx(ppt,pages); deckqa=evaluate_deck_output(pages,'USER_VISIBLE_ARTIFACT_DRAFT',dr,dh,mh,product)
    dossier={'schema':'RASHAD_USER_VISIBLE_ARTIFACT_DELIVERY_V2','classification':'USER_VISIBLE_ARTIFACT_DRAFT','output_file_sha256':dh,'montage_sha256':mh,'pages':pages,'artifact_brain_execution_status':'PASS','deck_artifact_council_execution':deck_exec,'production_render_status':'PASS','actual_output_qa_closed_loop_status':'PASS','deck_pixel_review':dr,'product_inspection':product,'framework_certification_substitute':False,'independent_judgment_status':'NOT_EXECUTED','parity_status':'NOT_EXECUTED','proof_index_status':'NOT_EXECUTED','release':{}}
    delivery=validate_user_visible_delivery(dossier,ppt)
    inc=json.load(open(ROOT/'QA/Runtime/fixtures/incidents/INCIDENT_REDF_20260816_SHAPE_ONLY_ARTIFACT_COLLAPSE.json',encoding='utf-8'))
    bad=td/'incident_bad.pptx';bad_pptx(bad);neg=inspect_pptx(bad)
    checks={
      'golden_page_count_14':product.get('slide_count')==14,
      'all_14_pages_have_real_brain_execution':len(pages)==14 and all(validate_brain_execution_proof(p['brain_session_execution_evidence'])['status']=='PASS' for p in pages),
      'all_14_pages_have_all_three_artifact_execution_stages':all(validate_artifact_execution_ledger(p['artifact_council_execution'],'PRE_CONCEPT')['status']=='PASS' and validate_artifact_execution_ledger(p['art_direction_execution'],'ART_DIRECTION')['status']=='PASS' and validate_artifact_execution_ledger(p['production_council_execution'],'PRODUCTION_READINESS')['status']=='PASS' for p in pages),
      'deck_review_council_execution_pass':validate_artifact_execution_ledger(deck_exec,'DECK_REVIEW')['status']=='PASS',
      'golden_product_inspection_pass':product.get('status')=='PASS',
      'golden_actual_output_qa_pass':deckqa.get('status')=='PASS',
      'golden_exact_file_delivery_allowed':delivery.get('status')=='DELIVERY_ALLOWED',
      'strategy_variety_at_least_8':len(set(strategies))>=8,
      'not_diagram_dominated':deckqa.get('diagram_ratio',1)<=.55,
      'incident_profile_still_blocked':inc.get('status')=='BLOCKED',
      'incident_shape_only_signature_locked':'PPTX_SHAPE_ONLY_ANALYTICAL_DECK_OVERUSE' in inc.get('blockers',[]),
      'synthetic_bad_deck_still_blocked':neg.get('status')=='BLOCKED'
    }
    out={'suite':'Rashad v7.2 Golden REDF End-to-End Brain→Artifact→Pixel-QA Acceptance','status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'strategy_count':len(set(strategies)),'diagram_ratio':deckqa.get('diagram_ratio'),'golden_product_blockers':product.get('blockers'),'golden_qa_blockers':deckqa.get('blockers'),'delivery_blockers':delivery.get('blockers'),'incident_blockers':inc.get('blockers')}
    (OUT/'V7_2_GOLDEN_REDF_ACCEPTANCE.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if out['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
