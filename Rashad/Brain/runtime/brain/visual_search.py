from __future__ import annotations
from brain.artifact_brain import generate_communication_hypotheses
from brain.composition_hypothesizer import build_composition_candidates
from brain.reference_grammar_library import retrieve as retrieve_reference_grammars
from brain.quality_floors_v7_3 import get as quality_floor


def generate_hypotheses(graph,content_pack):
    """Canonical v3 visual search.

    The search space is communication strategy, not geometry primitive. Legacy
    RING/HUB/SPINE/STACK/LANE primitives remain available downstream as optional
    geometry techniques, but they are no longer hypotheses and carry no winner
    authority.
    """
    r=generate_communication_hypotheses(graph,content_pack,int(quality_floor('min_exhibit_hypotheses',5)))
    if r.get('status')!='PASS':
        return {'status':'FAIL','reason':'COMMUNICATION_HYPOTHESIS_DIVERSITY_FAILED',**r}
    refs=retrieve_reference_grammars(r.get('page_features',{}).get('page_family','ANALYTICAL'),r['hypotheses'][0].get('communication_strategy') if r.get('hypotheses') else 'STATEMENT_LED')
    comp=build_composition_candidates(r.get('hypotheses',[]),content_pack,graph,[x['id'] for x in refs])
    if comp.get('status')!='PASS': return {'status':'FAIL','reason':'COMPOSITION_SPEC_DIVERSITY_FAILED',**r,'composition':comp}
    for h,spec in zip(r['hypotheses'],comp['composition_specs']):
        h['composition_spec']=spec; h['structural_signature']=spec['structural_signature']; h['reference_grammar_ids']=spec.get('reference_grammar_ids',[])
    r['composition_divergence']=comp['divergence']
    r['distinct_structural_signatures']=len({h.get('structural_signature') for h in r.get('hypotheses',[])})
    r['selection_status']='PENDING_ACTUAL_RENDER_AND_INDEPENDENT_JUDGE'
    r['winner']=None
    r['artifact_brain_version']='4.0.0'
    return r


def select_from_independent_judgments(hypotheses,judgments):
    valid=[j for j in judgments if j.get('independent') is True and j.get('judge_invocation_id') and not j.get('previous_response_id') and j.get('candidate_id')]
    by={j['candidate_id']:j for j in valid}
    scored=[(float(by[h['id']].get('score',0)),h['id']) for h in hypotheses if h['id'] in by]
    if len(scored)<len(hypotheses):
        return {'status':'BLOCKED','winner':None,'reason':'ALL_CANDIDATES_REQUIRE_INDEPENDENT_JUDGMENT'}
    scored.sort(reverse=True)
    return {'status':'PASS','winner':scored[0][1],'ranking':[x[1] for x in scored],'scores':{cid:score for score,cid in scored}}
