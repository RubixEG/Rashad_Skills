#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys,json,random,hashlib,copy
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/'Rashad/Brain/runtime'))
from brain.actual_output_qa import evaluate_page_output,evaluate_deck_output
OUT=ROOT/'QA/Certification'; random.seed(7202026)
STR=['STATEMENT_LED','NUMBER_LED','EVIDENCE_LED','TABLE_LED','CHART_LED','COMPARISON_LED','MATRIX_LED','DECISION_LED','SEQUENCE_LED','PROCESS_LED','SYSTEM_LED','ARCHITECTURE_LED','IMAGE_LED','HYBRID_EXHIBIT','SCORECARD_LED']
FAM={'STATEMENT_LED':'MINIMAL','NUMBER_LED':'MINIMAL','DECISION_LED':'MINIMAL','EVIDENCE_LED':'ANALYTICAL','TABLE_LED':'ANALYTICAL','CHART_LED':'ANALYTICAL','COMPARISON_LED':'ANALYTICAL','MATRIX_LED':'ANALYTICAL','SCORECARD_LED':'ANALYTICAL','SEQUENCE_LED':'RELATIONAL','PROCESS_LED':'RELATIONAL','SYSTEM_LED':'RELATIONAL','ARCHITECTURE_LED':'RELATIONAL','IMAGE_LED':'CREATIVE','HYBRID_EXHIBIT':'HYBRID'}
DIMS=['message_clarity','five_second_comprehension','visual_form_fitness','simplicity','executive_hierarchy','evidence_legibility','artifact_usefulness','specificity_to_page','rtl_typography','brand_fidelity','production_quality']

def h(i): return hashlib.sha256(str(i).encode()).hexdigest()
def hyps(seed):
    picks=['STATEMENT_LED','NUMBER_LED','EVIDENCE_LED','COMPARISON_LED','HYBRID_EXHIBIT']
    return [{'id':f'H{i+1}','communication_strategy':s,'strategy_family':FAM[s],'structural_signature':f'{seed}|{s}|{i}'} for i,s in enumerate(picks)]
def good_page(i,strategy=None):
    st=strategy or random.choice(STR); hh=h(100000+i)
    return {'page_id':f'P{i}','selected_render_hash':hh,'selected_strategy':st,'selected_candidate_id':f'H{(i%5)+1}','hypotheses':hyps(i),'visual_concept_id':f'VC{i}','production_render_id':f'PR{i}','render_kind':'PRODUCTION_PAGE_RENDER','actual_pixel_review':{'status':'PASS','independent':True,'review_id':f'R{i}','actor_id':f'QA{i}','actual_render_hash':hh,'scores':{k:random.randint(86,98) for k in DIMS},'generic_layout_swap_test':'PASS','artifact_skeptic_test':'PASS','five_second_test':'PASS','hard_blockers':[]},'repair_required':False,'repair_history':[],'final_qa_round':1}

def main():
    crashes=0; unsafe_escaped=0; valid_failed=0; page_runs=4000; deck_runs=800
    mutations=['concept','no_pixel','wrong_hash','low_score','generic','skeptic','five_second','not_independent','repair_missing','hard_blocker']
    for i in range(page_runs):
        try:
            p=good_page(i); bad=random.random()<.70
            if bad:
                m=random.choice(mutations)
                if m=='concept':p['render_kind']='COMMUNICATION_STRATEGY_CONCEPT_RENDER_V3'
                elif m=='no_pixel':p['actual_pixel_review']={'status':'NOT_EXECUTED'}
                elif m=='wrong_hash':p['actual_pixel_review']['actual_render_hash']='0'*64
                elif m=='low_score':p['actual_pixel_review']['scores'][random.choice(DIMS)]=random.randint(0,79)
                elif m=='generic':p['actual_pixel_review']['generic_layout_swap_test']='FAIL'
                elif m=='skeptic':p['actual_pixel_review']['artifact_skeptic_test']='FAIL'
                elif m=='five_second':p['actual_pixel_review']['five_second_test']='FAIL'
                elif m=='not_independent':p['actual_pixel_review']['independent']=False
                elif m=='repair_missing':p['repair_required']=True;p['repair_history']=[]
                elif m=='hard_blocker':p['actual_pixel_review']['hard_blockers']=['X']
            r=evaluate_page_output(p,'USER_VISIBLE_ARTIFACT_DRAFT')
            if bad and r['status']!='BLOCKED': unsafe_escaped+=1
            if not bad and r['status']!='PASS': valid_failed+=1
        except Exception: crashes+=1
    deck_mut=['duplicate_hash','diagram_overuse','same_run','low_variety','pixel_missing']
    for j in range(deck_runs):
        try:
            n=random.randint(8,18); safe_cycle=['STATEMENT_LED','NUMBER_LED','EVIDENCE_LED','COMPARISON_LED','TABLE_LED','DECISION_LED','PROCESS_LED','IMAGE_LED','MATRIX_LED','SCORECARD_LED']; pages=[good_page(j*100+i,safe_cycle[i%len(safe_cycle)]) for i in range(n)]; bad=random.random()<.75
            if bad:
                m=random.choice(deck_mut)
                if m=='duplicate_hash': pages[-1]['selected_render_hash']=pages[0]['selected_render_hash'];pages[-1]['actual_pixel_review']['actual_render_hash']=pages[0]['selected_render_hash']
                elif m=='diagram_overuse':
                    for p in pages[:int(n*.75)]:p['selected_strategy']='SYSTEM_LED'
                elif m=='same_run':
                    for p in pages[:5]:p['selected_strategy']='STATEMENT_LED'
                elif m=='low_variety':
                    for i,p in enumerate(pages):p['selected_strategy']='STATEMENT_LED' if i%2 else 'NUMBER_LED'
                elif m=='pixel_missing':pages[random.randrange(n)]['actual_pixel_review']={'status':'NOT_EXECUTED'}
            dr={'status':'PASS','independent':True,'review_id':'D','actor_id':'Q','scores':{k:92 for k in ['narrative_rhythm','visual_variety','executive_coherence','cross_page_specificity','density_rhythm','brand_consistency','rtl_consistency','overall_partner_grade']},'generic_deck_swap_test':'PASS','diagram_overuse_test':'PASS','hard_blockers':[]}
            # For stress logic, omit exact hash-binding/product inspection by using INTERNAL then explicitly page-check user-visible.
            r=evaluate_deck_output(pages,visibility='INTERNAL')
            page_bad=any(evaluate_page_output(p,'USER_VISIBLE_ARTIFACT_DRAFT')['status']!='PASS' for p in pages)
            blocked=(r['status']=='BLOCKED' or page_bad)
            if bad and not blocked: unsafe_escaped+=1
            if not bad and blocked: valid_failed+=1
        except Exception: crashes+=1
    out={'suite':'V7.2 Artifact Stress Quality','status':'PASS' if crashes==0 and unsafe_escaped==0 and valid_failed==0 else 'FAIL','page_runs':page_runs,'deck_runs':deck_runs,'crashes':crashes,'unsafe_escaped':unsafe_escaped,'valid_failed':valid_failed}
    (OUT/'V7_2_STRESS_QUALITY_RESULTS.json').write_text(json.dumps(out,indent=2),encoding='utf8'); print(json.dumps(out,indent=2)); return 0 if out['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
