from __future__ import annotations
from .coverage import validate_session
def final_release(brain_session,qa_release_report):
    errs=[]; cov=validate_session(brain_session)
    if cov['status']!='PASS': errs.extend(cov['errors'])
    if brain_session.get('state') not in ('JUDGED','QA_CANDIDATE_PASS','RELEASED'): errs.append({'kind':'BRAIN_NOT_JUDGED','state':brain_session.get('state')})
    inv=brain_session.get('invocations',[]); judges=[x for x in inv if x.get('function')=='INDEPENDENT_JUDGE' and x.get('status')=='PASS']; chairs=[x for x in inv if x.get('function')=='RELEASE_CHAIR' and x.get('status')=='PASS']
    if not judges: errs.append({'kind':'INDEPENDENT_JUDGE_MISSING'})
    elif not any(x.get('external_independent') is True for x in judges): errs.append({'kind':'EXTERNAL_INDEPENDENT_JUDGE_REQUIRED_FOR_RELEASED'})
    if not chairs: errs.append({'kind':'RELEASE_CHAIR_MISSING'})
    elif not any(x.get('external_independent') is True for x in chairs): errs.append({'kind':'EXTERNAL_RELEASE_CHAIR_CONTEXT_REQUIRED_FOR_RELEASED'})
    if qa_release_report.get('final_verdict') not in ('QA_CANDIDATE_PASS','RELEASE_CANDIDATE_PASS'): errs.append({'kind':'QA_RELEASE_CANDIDATE_NOT_PASSED','value':qa_release_report.get('final_verdict')})
    return {'status':'PASS' if not errs else 'FAIL','final_verdict':'RELEASED' if not errs else 'BLOCKED','release_authority':'RASHAD_BRAIN_RELEASE_CHAIR','errors':errs}
