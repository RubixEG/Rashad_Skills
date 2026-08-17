from __future__ import annotations
from artifact.artifact_engine_v3 import run as artifact_run
READING=['RTL_SPINE','CENTER_OUT','TOP_DOWN_THEN_RTL','RIGHT_FOCAL_TO_SYSTEM','LOOP_THEN_DECISION']; FOCAL=['RIGHT','CENTER','TOP_RIGHT','CENTER_RIGHT','CENTER']
def generate_hypotheses(graph,content_pack):
    a=artifact_run(graph)
    if a.get('status')!='PASS': return {'status':'FAIL','reason':'ARTIFACT_TRUTH_FAILED','artifact':a}
    cs=a.get('candidates',[])
    if not cs: return {'status':'FAIL','reason':'NO_ARTIFACT_CANDIDATES','artifact':a}
    hs=[]
    for i in range(5):
        c=cs[i%len(cs)]
        hs.append({'id':f'H{i+1}','topology':a['signature']['topology'],'dominant_form':c['dominant'],'primitives':c['primitives'],'reading_path':READING[i],'focal_point':FOCAL[i],'mass_plan':{'dominant':[.50,.44,.56,.48,.52][i],'supporting':[.26,.32,.22,.28,.24][i],'implication':.12,'source':.06},'artifact_truth_score':c['artifact_truth_score'],'visual_thesis':content_pack.get('thesis',''),'structural_signature':f"{c['dominant']}|{','.join(c['primitives'])}|{READING[i]}|{FOCAL[i]}"})
    distinct=len({h['structural_signature'] for h in hs})
    return {'status':'PASS' if distinct==5 else 'FAIL','hypotheses':hs,'distinct_structural_signatures':distinct,'selection_status':'PENDING_ACTUAL_RENDER_AND_INDEPENDENT_JUDGE','winner':None,'artifact':a}
def select_from_independent_judgments(hypotheses,judgments):
    valid=[j for j in judgments if j.get('independent') is True and j.get('judge_invocation_id') and not j.get('previous_response_id') and j.get('candidate_id')]
    by={j['candidate_id']:j for j in valid}; scored=[(float(by[h['id']].get('score',0)),h['id']) for h in hypotheses if h['id'] in by]
    if len(scored)<len(hypotheses): return {'status':'BLOCKED','winner':None,'reason':'ALL_CANDIDATES_REQUIRE_INDEPENDENT_JUDGMENT'}
    scored.sort(reverse=True); return {'status':'PASS','winner':scored[0][1],'ranking':[x[1] for x in scored],'scores':{cid:score for score,cid in scored}}
