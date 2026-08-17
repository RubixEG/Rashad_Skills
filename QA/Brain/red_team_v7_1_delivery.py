#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys,json,tempfile,copy
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Rashad/Brain/runtime'))
sys.path.insert(0,str(Path(__file__).parent))
from brain.actual_output_qa import evaluate_page_output,evaluate_deck_output
from brain.delivery_gate import validate_user_visible_delivery
from brain.product_inspector import inspect_pptx,sha256_file
from run_v7_1_user_visible_delivery_certification import png,review,hyps,good_pptx,bad_pptx,page
OUT=ROOT/'QA/Certification'

def blocked_page(p): return evaluate_page_output(p,'USER_VISIBLE_ARTIFACT_DRAFT')['status']=='BLOCKED'
def record(a,n,ok,d=''): a.append({'attack':n,'status':'BLOCKED' if ok else 'ESCAPED','detail':d})

def main():
    a=[]
    with tempfile.TemporaryDirectory() as td:
      td=Path(td); hero=td/'hero.png'; png(hero,'hero'); ppt=td/'g.pptx'; good_pptx(ppt,hero)
      strategies=['IMAGE_LED','STATEMENT_LED','NUMBER_LED','TABLE_LED','CHART_LED','PROCESS_LED','COMPARISON_LED','DECISION_LED']
      pages=[]
      for i,s in enumerate(strategies,1):
        rp=td/f'{i}.png'; png(rp,s); pages.append(page(i,s,rp))
      montage=td/'m.png'; png(montage,'montage'); dh=sha256_file(ppt); mh=sha256_file(montage)
      dr={'status':'PASS','independent':True,'review_id':'D','actor_id':'QA-D','deck_sha256':dh,'montage_sha256':mh,'scores':{k:92 for k in ['narrative_rhythm','visual_variety','executive_coherence','cross_page_specificity','density_rhythm','brand_consistency','rtl_consistency','overall_partner_grade']},'generic_deck_swap_test':'PASS','diagram_overuse_test':'PASS','hard_blockers':[]}
      dossier={'schema':'RASHAD_USER_VISIBLE_ARTIFACT_DELIVERY_V1','classification':'USER_VISIBLE_ARTIFACT_DRAFT','output_file_sha256':dh,'montage_sha256':mh,'pages':pages,'artifact_brain_execution_status':'PASS','production_render_status':'PASS','actual_output_qa_closed_loop_status':'PASS','deck_pixel_review':dr,'framework_certification_substitute':False,'independent_judgment_status':'NOT_EXECUTED','parity_status':'NOT_EXECUTED','proof_index_status':'NOT_EXECUTED','release':{}}
      # Page attacks
      x=copy.deepcopy(pages[1]); x['render_kind']='COMMUNICATION_STRATEGY_CONCEPT_RENDER_V3'; record(a,'concept_wireframe_as_user_visible',blocked_page(x))
      x=copy.deepcopy(pages[1]); x['actual_pixel_review']={'status':'NOT_EXECUTED'}; record(a,'no_pixel_review',blocked_page(x))
      x=copy.deepcopy(pages[1]); x['actual_pixel_review']['independent']=False; record(a,'producer_reviews_own_pixels',blocked_page(x))
      x=copy.deepcopy(pages[1]); x['actual_pixel_review']['producer_actor_collision']=True; record(a,'producer_actor_collision',blocked_page(x))
      x=copy.deepcopy(pages[1]); x['actual_pixel_review']['actual_render_hash']='a'*64; record(a,'review_wrong_render_hash',blocked_page(x))
      x=copy.deepcopy(pages[1]); x['actual_pixel_review']['scores']['simplicity']=40; record(a,'low_simplicity_hidden_by_high_average',blocked_page(x))
      x=copy.deepcopy(pages[1]); x['actual_pixel_review']['generic_layout_swap_test']='FAIL'; record(a,'generic_label_swap_page',blocked_page(x))
      x=copy.deepcopy(pages[1]); x['actual_pixel_review']['artifact_skeptic_test']='FAIL'; record(a,'decoration_only_artifact',blocked_page(x))
      x=copy.deepcopy(pages[1]); x['actual_pixel_review']['five_second_test']='FAIL'; record(a,'fails_five_second_test',blocked_page(x))
      x=copy.deepcopy(pages[1]); x['actual_pixel_review']['hard_blockers']=['WEAK']; record(a,'hard_blocker_averaged_away',blocked_page(x))
      x=copy.deepcopy(pages[1]); x['repair_required']=True; x['repair_history']=[]; record(a,'failed_round_without_repair',blocked_page(x))
      x=copy.deepcopy(pages[1]); x.pop('production_render_id',None); record(a,'missing_production_render_identity',blocked_page(x))
      # Deck attacks
      pi=inspect_pptx(ppt,pages)
      dup=copy.deepcopy(pages); dup[2]['selected_render_hash']=dup[1]['selected_render_hash']; dup[2]['actual_pixel_review']['actual_render_hash']=dup[1]['selected_render_hash']; q=evaluate_deck_output(dup,'USER_VISIBLE_ARTIFACT_DRAFT',dr,dh,mh,pi); record(a,'cross_page_render_hash_reuse',q['status']=='BLOCKED')
      diag=copy.deepcopy(pages); 
      for p in diag[:6]: p['selected_strategy']='SYSTEM_LED'
      q=evaluate_deck_output(diag,'USER_VISIBLE_ARTIFACT_DRAFT',dr,dh,mh,pi); record(a,'diagram_overuse',q['status']=='BLOCKED')
      same=copy.deepcopy(pages); 
      for p in same[:4]: p['selected_strategy']='STATEMENT_LED'
      q=evaluate_deck_output(same,'USER_VISIBLE_ARTIFACT_DRAFT',dr,dh,mh,pi); record(a,'four_same_strategy_run',q['status']=='BLOCKED')
      lowvar=copy.deepcopy(pages); 
      for i,p in enumerate(lowvar): p['selected_strategy']='STATEMENT_LED' if i%2==0 else 'NUMBER_LED'
      q=evaluate_deck_output(lowvar,'USER_VISIBLE_ARTIFACT_DRAFT',dr,dh,mh,pi); record(a,'insufficient_deck_strategy_variety',q['status']=='BLOCKED')
      norev=copy.deepcopy(dossier); norev['deck_pixel_review']={}; record(a,'no_deck_pixel_review',validate_user_visible_delivery(norev,ppt)['status']=='BLOCK_DELIVERY')
      badhash=copy.deepcopy(dossier); badhash['deck_pixel_review']['deck_sha256']='b'*64; record(a,'deck_review_wrong_file_hash',validate_user_visible_delivery(badhash,ppt)['status']=='BLOCK_DELIVERY')
      badmont=copy.deepcopy(dossier); badmont['deck_pixel_review']['montage_sha256']='c'*64; record(a,'deck_review_wrong_montage_hash',validate_user_visible_delivery(badmont,ppt)['status']=='BLOCK_DELIVERY')
      sub=copy.deepcopy(dossier); sub['framework_certification_substitute']=True; record(a,'framework_qa_substitution',validate_user_visible_delivery(sub,ppt)['status']=='BLOCK_DELIVERY')
      noart=copy.deepcopy(dossier); noart['artifact_brain_execution_status']='PASS_FROM_FRAMEWORK_TEST'; record(a,'no_artifact_execution_proof',validate_user_visible_delivery(noart,ppt)['status']=='BLOCK_DELIVERY')
      noprod=copy.deepcopy(dossier); noprod['production_render_status']='NOT_EXECUTED'; record(a,'no_production_render_proof',validate_user_visible_delivery(noprod,ppt)['status']=='BLOCK_DELIVERY')
      noqaloop=copy.deepcopy(dossier); noqaloop['actual_output_qa_closed_loop_status']='DRAFT_QA_PARTIAL'; record(a,'partial_qa_called_delivery_ready',validate_user_visible_delivery(noqaloop,ppt)['status']=='BLOCK_DELIVERY')
      filem=copy.deepcopy(dossier); filem['output_file_sha256']='d'*64; record(a,'dossier_bound_to_different_pptx',validate_user_visible_delivery(filem,ppt)['status']=='BLOCK_DELIVERY')
      # real incident shape-only profile
      bad=td/'bad.pptx'; bad_pptx(bad); bi=inspect_pptx(bad); record(a,'shape_only_template_deck',bi['status']=='BLOCKED',str(bi['blockers']))
      # IMAGE/TABLE/CHART semantic lie against actual product
      exp=copy.deepcopy(pages); plain=td/'plain.pptx'; bad_pptx(plain); ip=inspect_pptx(plain,exp); record(a,'strategy_label_lies_about_actual_objects',ip['status']=='BLOCKED',str(ip['blockers']))
    escaped=[x for x in a if x['status']!='BLOCKED']; out={'suite':'V7.1 User-Visible Artifact Delivery Red Team','status':'PASS' if not escaped else 'FAIL','blocked':len(a)-len(escaped),'total':len(a),'attacks':a}
    (OUT/'V7_1_USER_VISIBLE_DELIVERY_RED_TEAM.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'suite':out['suite'],'status':out['status'],'blocked':out['blocked'],'total':out['total'],'escaped':escaped},ensure_ascii=False,indent=2)); return 0 if not escaped else 2
if __name__=='__main__': raise SystemExit(main())
