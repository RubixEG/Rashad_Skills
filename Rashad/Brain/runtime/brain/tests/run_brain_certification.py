from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from brain.router import route
from brain.orchestrator import run_brain
from brain.provider import ScriptedTestProvider, NoExecutionProvider
from brain.coverage import validate_session
from brain.visual_search import generate_hypotheses,select_from_independent_judgments
from brain.release import final_release

tests=[]
def add(name,ok,detail=None): tests.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})

# Routing depth
r=route('COMMERCIAL_EXPOSURE',True,True,False,False)
add('commercial_route_has_cfo_domain', 'C04_COMMERCIAL_FINANCIAL' in r,r)
add('critical_route_has_epistemic_redteam_meta', all(x in r for x in ['C03_EPISTEMIC_TRUTH','C13_ADVERSARIAL_COUNTERFACTUAL','C15_META_COGNITION_INTEGRITY']),r)
add('rendered_route_has_visual_and_production', all(x in r for x in ['C11_VISUAL_PERCEPTION','C12_PRODUCTION_INTEGRITY']),r)

# Fail closed without execution provider
task={'task_id':'T1','rfp_role':'COMMERCIAL_EXPOSURE','critical':True,'rendered':False,'evidence':[{'id':'E1'}]}
no=run_brain(task,NoExecutionProvider())
add('no_provider_is_blocked',no.get('state')=='BLOCKED' and no.get('release',{}).get('reason')=='PRODUCER_NOT_EXECUTED',no.get('release'))

# Structured test execution reaches cognitive lock, not release
t=run_brain(task,ScriptedTestProvider())
add('test_provider_reaches_cognitive_lock',t.get('state')=='COGNITIVE_LOCKED',t.get('state'))
add('brain_does_not_self_release_after_cognition',t.get('release',{}).get('status')=='DRAFT_READY',t.get('release'))
add('council_coverage_passes',validate_session(t)['status']=='PASS',validate_session(t))

# Visual search: no hardcoded H1, five structurally distinct hypotheses
p=ROOT/'fixtures/proof_valid/pages/P01'; g=json.loads((p/'relationship_graph.json').read_text()); c=json.loads((p/'content_pack.json').read_text())
vs=generate_hypotheses(g,c)
add('five_structural_hypotheses',vs.get('status')=='PASS' and vs.get('distinct_structural_signatures')==5,[h['structural_signature'] for h in vs.get('hypotheses',[])])
add('winner_not_hardcoded',vs.get('winner') is None and vs.get('selection_status')=='PENDING_ACTUAL_RENDER_AND_INDEPENDENT_JUDGE',vs.get('selection_status'))

# Judge selection must cover every candidate
partial=[{'candidate_id':'H1','independent':True,'judge_invocation_id':'J1','score':99}]
sel=select_from_independent_judgments(vs['hypotheses'],partial)
add('partial_judgment_blocks_selection',sel['status']=='BLOCKED',sel)
judges=[{'candidate_id':f'H{i}','independent':True,'judge_invocation_id':f'J{i}','score':80+i} for i in range(1,6)]
sel2=select_from_independent_judgments(vs['hypotheses'],judges)
add('independent_scores_choose_actual_winner',sel2['status']=='PASS' and sel2['winner']=='H5',sel2)

# Independence collision is blocked
bad=dict(t); bad['invocations']=list(t['invocations'])+[{ 'status':'PASS','function':'INDEPENDENT_JUDGE','council_id':'C11_VISUAL_PERCEPTION','actor_id':next(x['actor_id'] for x in t['invocations'] if x['function']=='PRODUCER'),'independent':True,'judge_invocation_id':'JX'}]
cv=validate_session(bad)
add('producer_judge_collision_blocked',any(x['kind']=='PRODUCER_JUDGE_COLLISION' for x in cv['errors']),cv)

# Final release cannot happen from QA alone
qa={'final_verdict':'QA_CANDIDATE_PASS'}
fr=final_release(t,qa)
add('qa_candidate_cannot_release_without_judge_and_chair',fr['final_verdict']=='BLOCKED',fr)

out={'runtime':'Rashad Brain 1.0 / QA Runtime 4.2 / QA Brain 1.0','status':'PASS' if all(x['status']=='PASS' for x in tests) else 'FAIL','passed':sum(x['status']=='PASS' for x in tests),'total':len(tests),'tests':tests}
print(json.dumps(out,ensure_ascii=False,indent=2))
(ROOT/'BRAIN_CERTIFICATION_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
raise SystemExit(0 if out['status']=='PASS' else 1)
