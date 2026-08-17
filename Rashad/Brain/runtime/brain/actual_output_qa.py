from __future__ import annotations
from collections import Counter
from brain.quality_floors_v7_3 import get as quality_floor

DIAGRAM={'SEQUENCE_LED','PROCESS_LED','SYSTEM_LED','ARCHITECTURE_LED','MAP_LED','JOURNEY_LED','CONTROL_TOWER_LED','CAUSE_EFFECT'}
USER_VISIBLE={'USER_VISIBLE_ARTIFACT_DRAFT','RELEASE_CANDIDATE','RELEASED'}
QUALITY_DIMENSIONS=(
    'message_clarity','five_second_comprehension','visual_form_fitness','simplicity',
    'executive_hierarchy','evidence_legibility','artifact_usefulness','specificity_to_page',
    'rtl_typography','brand_fidelity','production_quality'
)
MIN_DIMENSION_SCORE=80.0
MIN_MEAN_SCORE=85.0


def _quality_review(review, selected_hash):
    blockers=[]
    if not isinstance(review,dict): review={}
    if review.get('status')!='PASS': blockers.append('ACTUAL_PIXEL_VISUAL_QUALITY_REVIEW_REQUIRED')
    if review.get('independent') is not True: blockers.append('PIXEL_REVIEW_MUST_BE_INDEPENDENT')
    if not review.get('review_id'): blockers.append('PIXEL_REVIEW_ID_REQUIRED')
    if not review.get('actor_id'): blockers.append('PIXEL_REVIEW_ACTOR_REQUIRED')
    if review.get('producer_actor_collision') is True: blockers.append('PRODUCER_PIXEL_REVIEW_COLLISION')
    if not selected_hash or review.get('actual_render_hash')!=selected_hash: blockers.append('PIXEL_REVIEW_HASH_BINDING_MISMATCH')
    scores=review.get('scores') or {}
    missing=[k for k in QUALITY_DIMENSIONS if k not in scores]
    if missing: blockers.append('PIXEL_QUALITY_SCORECARD_INCOMPLETE:'+','.join(missing))
    vals=[]
    for k in QUALITY_DIMENSIONS:
        if k not in scores: continue
        try: v=float(scores[k])
        except Exception:
            blockers.append('INVALID_PIXEL_SCORE:'+k); continue
        vals.append(v)
        if v < MIN_DIMENSION_SCORE: blockers.append('PIXEL_QUALITY_DIMENSION_BELOW_FLOOR:'+k)
    mean=(sum(vals)/len(vals)) if vals else 0.0
    if vals and mean < MIN_MEAN_SCORE: blockers.append('PIXEL_QUALITY_MEAN_BELOW_FLOOR')
    if review.get('generic_layout_swap_test')!='PASS': blockers.append('GENERIC_LAYOUT_SWAP_TEST_REQUIRED')
    if review.get('artifact_skeptic_test')!='PASS': blockers.append('ARTIFACT_SKEPTIC_PIXEL_TEST_REQUIRED')
    if review.get('five_second_test')!='PASS': blockers.append('FIVE_SECOND_PIXEL_TEST_REQUIRED')
    if review.get('hard_blockers'): blockers.append('PIXEL_REVIEW_OPEN_HARD_BLOCKERS')
    try: artifact_truth=float(review.get('artifact_truth_score',0) or 0); ceqs=float(review.get('ceqs_score',review.get('ceqs',0)) or 0)
    except Exception: artifact_truth=ceqs=0
    if artifact_truth < float(quality_floor('artifact_truth_min',90)): blockers.append('ARTIFACT_TRUTH_SCORE_BELOW_90')
    if ceqs < float(quality_floor('ceqs_min',90)): blockers.append('CEQS_SCORE_BELOW_90')
    return blockers, round(mean,2)


def evaluate_page_output(page, visibility='INTERNAL'):
    blockers=[]; warnings=[]
    if not page.get('page_id'): blockers.append('PAGE_ID_REQUIRED')
    selected_hash=page.get('selected_render_hash')
    if not selected_hash: blockers.append('ACTUAL_RENDER_HASH_REQUIRED')
    if not page.get('selected_strategy'): blockers.append('SELECTED_COMMUNICATION_STRATEGY_REQUIRED')
    hs=page.get('hypotheses',[]) or []
    fams={h.get('strategy_family') for h in hs if h.get('strategy_family')}
    strategies={h.get('communication_strategy') for h in hs if h.get('communication_strategy')}
    if len(strategies)<5: blockers.append('FIVE_DISTINCT_COMMUNICATION_STRATEGIES_REQUIRED')
    if len(fams)<3: blockers.append('AT_LEAST_THREE_COMMUNICATION_FAMILIES_REQUIRED')
    if hs and all((h.get('communication_strategy') in DIAGRAM) for h in hs if h.get('communication_strategy')): blockers.append('DIAGRAM_ONLY_HYPOTHESIS_SEARCH_FORBIDDEN')

    render_kind=page.get('render_kind') or (page.get('selected_render') or {}).get('render_kind')
    if visibility in USER_VISIBLE:
        if render_kind!='PRODUCTION_PAGE_RENDER': blockers.append('USER_VISIBLE_REQUIRES_PRODUCTION_PAGE_RENDER')
        vr=page.get('actual_pixel_review',{}) or {}
        qblocks,qmean=_quality_review(vr,selected_hash); blockers.extend(qblocks)
        if not page.get('visual_concept_id'): blockers.append('VISUAL_CONCEPT_ID_REQUIRED')
        if not page.get('production_render_id'): blockers.append('PRODUCTION_RENDER_ID_REQUIRED')
        if page.get('repair_required') and not page.get('repair_history'): blockers.append('REQUIRED_REPAIR_HISTORY_MISSING')
        if page.get('final_qa_round',0) < 1: blockers.append('FINAL_QA_ROUND_REQUIRED')
        return {'status':'PASS' if not blockers else 'BLOCKED','blockers':blockers,'warnings':warnings,'actual_pixels_seen':vr.get('status')=='PASS','quality_mean':qmean,'visibility':visibility}

    vr=page.get('actual_pixel_review',{}) or {}
    if vr.get('status')!='PASS': warnings.append('ACTUAL_PIXEL_VISUAL_QUALITY_REVIEW_NOT_EXECUTED')
    if render_kind and render_kind.startswith('COMMUNICATION_STRATEGY_CONCEPT_RENDER'):
        warnings.append('CONCEPT_RENDER_INTERNAL_ONLY')
    return {'status':'BLOCKED' if blockers else ('DRAFT_QA_PARTIAL' if warnings else 'PASS'),'blockers':blockers,'warnings':warnings,'actual_pixels_seen':vr.get('status')=='PASS','visibility':visibility}


def _deck_quality_review(review, deck_hash, montage_hash):
    blockers=[]
    if not isinstance(review,dict): review={}
    if review.get('status')!='PASS': blockers.append('DECK_PIXEL_REVIEW_REQUIRED')
    if review.get('independent') is not True: blockers.append('DECK_REVIEW_MUST_BE_INDEPENDENT')
    if not review.get('review_id') or not review.get('actor_id'): blockers.append('DECK_REVIEW_IDENTITY_REQUIRED')
    if deck_hash and review.get('deck_sha256')!=deck_hash: blockers.append('DECK_REVIEW_FILE_HASH_MISMATCH')
    if montage_hash and review.get('montage_sha256')!=montage_hash: blockers.append('DECK_REVIEW_MONTAGE_HASH_MISMATCH')
    scores=review.get('scores') or {}
    required=('narrative_rhythm','visual_variety','executive_coherence','cross_page_specificity','density_rhythm','brand_consistency','rtl_consistency','overall_partner_grade')
    vals=[]
    for k in required:
        if k not in scores: blockers.append('DECK_QUALITY_SCORE_MISSING:'+k); continue
        try: v=float(scores[k])
        except Exception: blockers.append('INVALID_DECK_SCORE:'+k); continue
        vals.append(v)
        if v<MIN_DIMENSION_SCORE: blockers.append('DECK_QUALITY_DIMENSION_BELOW_FLOOR:'+k)
    if vals and sum(vals)/len(vals)<MIN_MEAN_SCORE: blockers.append('DECK_QUALITY_MEAN_BELOW_FLOOR')
    if review.get('generic_deck_swap_test')!='PASS': blockers.append('GENERIC_DECK_SWAP_TEST_REQUIRED')
    if review.get('diagram_overuse_test')!='PASS': blockers.append('DECK_DIAGRAM_OVERUSE_TEST_REQUIRED')
    if review.get('hard_blockers'): blockers.append('DECK_REVIEW_OPEN_HARD_BLOCKERS')
    return blockers


def evaluate_deck_output(pages, visibility='INTERNAL', deck_review=None, deck_sha256=None, montage_sha256=None, product_inspection=None):
    blockers=[]; warnings=[]; pages=list(pages or [])
    if not pages:return {'status':'BLOCKED','blockers':['NO_PAGES'],'warnings':[]}
    hashes=[p.get('selected_render_hash') for p in pages if p.get('selected_render_hash')]
    if len(hashes)!=len(set(hashes)): blockers.append('CROSS_PAGE_RENDER_HASH_REUSE')
    strategies=[p.get('selected_strategy') for p in pages]
    n=len(strategies); diag=sum(s in DIAGRAM for s in strategies if s)
    if n>=6 and diag/max(1,n)>float(quality_floor('diagram_ratio_hard_block',.55)): blockers.append('DECK_DIAGRAM_OVERUSE')
    run=1; maxrun=1
    for a,b in zip(strategies,strategies[1:]):
        run=run+1 if a==b and a else 1; maxrun=max(maxrun,run)
    if maxrun>=4: blockers.append('FOUR_CONSECUTIVE_SAME_COMMUNICATION_STRATEGY')
    if n>=8 and len({s for s in strategies if s}) < min(5,max(3,round(n*.35))): blockers.append('INSUFFICIENT_DECK_COMMUNICATION_VARIETY')
    ids=[p.get('selected_candidate_id') for p in pages if p.get('selected_candidate_id')]
    if len(ids)>=6:
        most=Counter(ids).most_common(1)[0]
        if most[1]/len(ids)>.70: blockers.append('POSITIONAL_HYPOTHESIS_WINNER_BIAS')
    comp=[(p.get('selected_strategy'),p.get('composition_logic')) for p in pages]
    if n>=6 and comp and Counter(comp).most_common(1)[0][1]>3: blockers.append('GENERIC_COMPOSITION_REPETITION')
    comp_logic=[p.get('composition_logic') for p in pages if p.get('composition_logic')]
    if n>=6 and comp_logic and Counter(comp_logic).most_common(1)[0][1]>3 and 'GENERIC_COMPOSITION_REPETITION' not in blockers:
        blockers.append('GENERIC_COMPOSITION_REPETITION')

    seen_pixels=sum(bool((p.get('actual_pixel_review') or {}).get('status')=='PASS') for p in pages)
    if visibility in USER_VISIBLE:
        for p in pages:
            pr=evaluate_page_output(p,visibility=visibility)
            blockers.extend([f"{p.get('page_id','PAGE')}::{x}" for x in pr.get('blockers',[])])
        blockers.extend(_deck_quality_review(deck_review or {},deck_sha256,montage_sha256))
        pi=product_inspection or {}
        if pi.get('status')!='PASS': blockers.append('PPTX_PRODUCT_INSPECTION_NOT_PASSED')
        for x in pi.get('blockers',[]) or []: blockers.append('PRODUCT_INSPECTION::'+str(x))
    elif seen_pixels<len(pages):
        warnings.append(f'ACTUAL_PIXEL_QA_INCOMPLETE_{seen_pixels}_OF_{len(pages)}')

    return {'status':'BLOCKED' if blockers else ('DRAFT_QA_PARTIAL' if warnings else 'PASS'),'blockers':blockers,'warnings':warnings,'page_count':n,'diagram_ratio':round(diag/max(1,n),3),'max_same_strategy_run':maxrun,'actual_pixel_reviews':seen_pixels,'visibility':visibility}
