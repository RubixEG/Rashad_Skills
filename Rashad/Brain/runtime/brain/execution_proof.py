from __future__ import annotations
from .coverage import validate_session

EXPERT_FUNCTIONS={'SME_REVIEW','EXECUTIVE_SIMULATION','EVALUATOR_SIMULATION','GOVERNOR_REVIEW'}
ARTIFACT_STAGE_FUNCTIONS={
 'PRE_CONCEPT':'ARTIFACT_COUNCIL_REVIEW',
 'ART_DIRECTION':'ART_DIRECTION_REVIEW',
 'PRODUCTION_READINESS':'PRODUCTION_READINESS_REVIEW',
 'DECK_REVIEW':'ARTIFACT_COUNCIL_REVIEW',
}

def _validate_host_native_invocation(x):
    errors=[]
    if not isinstance(x,dict): return ['HOST_NATIVE_INVOCATION_NOT_OBJECT']
    if x.get('execution_mode')!='HOST_NATIVE_MODE' and x.get('host_native') is not True: return errors
    proof=x.get('host_native_proof') or {}
    if x.get('host_native') is not True: errors.append('HOST_NATIVE_FLAG_MISSING')
    if proof.get('source')!='HOST_NATIVE_MODEL_EXECUTION': errors.append('HOST_NATIVE_SOURCE_INVALID')
    if not proof.get('host_session_id'): errors.append('HOST_NATIVE_SESSION_ID_MISSING')
    if not proof.get('host_response_id'): errors.append('HOST_NATIVE_RESPONSE_ID_MISSING')
    if proof.get('request_key')!=x.get('request_key'): errors.append('HOST_NATIVE_REQUEST_KEY_MISMATCH')
    if x.get('invocation_id')!=proof.get('host_response_id'): errors.append('HOST_NATIVE_INVOCATION_RESPONSE_ID_MISMATCH')
    if x.get('function') in ('INDEPENDENT_JUDGE','RELEASE_CHAIR') and proof.get('independent_context') is not True: errors.append('HOST_NATIVE_INDEPENDENCE_CONTEXT_MISSING')
    return errors

def validate_expert_execution_ledger(ledger):
    errors=[]
    if not isinstance(ledger,dict): return {'status':'BLOCKED','errors':['EXPERT_LEDGER_REQUIRED']}
    if ledger.get('execution_proof')!='ISOLATED_INVOCATION_LEDGER': errors.append('EXPERT_LEDGER_PROOF_KIND_INVALID')
    required=list(ledger.get('required_experts') or [])
    inv=list(ledger.get('invocations') or [])
    if not required: errors.append('EXPERT_REQUIRED_SET_EMPTY')
    if not inv: errors.append('EXPERT_INVOCATIONS_EMPTY')
    passed=[x for x in inv if isinstance(x,dict) and x.get('status')=='PASS']
    executed={x.get('expert_role_id') for x in passed if x.get('expert_role_id')}
    missing=sorted(set(required)-executed)
    if missing: errors.append('EXPERT_REQUIRED_NOT_EXECUTED:'+','.join(missing))
    for x in passed:
        if x.get('function') not in EXPERT_FUNCTIONS: errors.append('EXPERT_FUNCTION_INVALID:'+str(x.get('function')))
        if not x.get('invocation_id') or not x.get('actor_id') or not x.get('isolated_context_id'): errors.append('EXPERT_INVOCATION_IDENTITY_INCOMPLETE')
        errors.extend('EXPERT_'+e for e in _validate_host_native_invocation(x))
    actors=[x.get('actor_id') for x in passed if x.get('actor_id')]
    contexts=[x.get('isolated_context_id') for x in passed if x.get('isolated_context_id')]
    if len(actors)!=len(set(actors)): errors.append('EXPERT_ACTOR_REUSE')
    if len(contexts)!=len(set(contexts)): errors.append('EXPERT_CONTEXT_REUSE')
    if ledger.get('errors'): errors.append('EXPERT_LEDGER_CONTAINS_ERRORS')
    if ledger.get('status')!='PASS': errors.append('EXPERT_LEDGER_STATUS_NOT_PASS')
    return {'status':'PASS' if not errors else 'BLOCKED','errors':errors,'required':required,'executed':sorted(executed)}

def validate_artifact_execution_ledger(ledger,expected_stage=None):
    errors=[]
    if not isinstance(ledger,dict): return {'status':'BLOCKED','errors':['ARTIFACT_LEDGER_REQUIRED']}
    stage=ledger.get('stage')
    if expected_stage and stage!=expected_stage: errors.append(f'ARTIFACT_STAGE_MISMATCH:{stage}!={expected_stage}')
    if ledger.get('execution_proof')!='ISOLATED_ARTIFACT_COUNCIL_INVOCATION_LEDGER': errors.append('ARTIFACT_LEDGER_PROOF_KIND_INVALID')
    req=list(ledger.get('required_executions') or [])
    inv=list(ledger.get('invocations') or [])
    if not req: errors.append('ARTIFACT_REQUIRED_SET_EMPTY')
    if not inv: errors.append('ARTIFACT_INVOCATIONS_EMPTY')
    passed=[x for x in inv if isinstance(x,dict) and x.get('status')=='PASS']
    by_pair={(x.get('council_id'),x.get('artifact_role_id')):x for x in passed if x.get('council_id')}
    by_council={x.get('council_id'):x for x in passed if x.get('council_id')}
    expected_fn=ARTIFACT_STAGE_FUNCTIONS.get(stage)
    for r in req:
        cid=r.get('council_id'); rid=r.get('role_id'); x=by_pair.get((cid,rid)) if rid else by_council.get(cid)
        if not x: errors.append('ARTIFACT_REQUIRED_ROLE_NOT_EXECUTED:'+str(cid)+':'+str(rid)); continue
        if expected_fn and x.get('function')!=expected_fn: errors.append('ARTIFACT_FUNCTION_MISMATCH:'+str(cid))
        if not x.get('invocation_id') or not x.get('actor_id') or not x.get('isolated_context_id'): errors.append('ARTIFACT_INVOCATION_IDENTITY_INCOMPLETE:'+str(cid))
        errors.extend('ARTIFACT_'+e+':'+str(cid) for e in _validate_host_native_invocation(x))
    actors=[x.get('actor_id') for x in passed if x.get('actor_id')]
    contexts=[x.get('isolated_context_id') for x in passed if x.get('isolated_context_id')]
    if len(actors)!=len(set(actors)): errors.append('ARTIFACT_ACTOR_REUSE')
    if len(contexts)!=len(set(contexts)): errors.append('ARTIFACT_CONTEXT_REUSE')
    if ledger.get('errors'): errors.append('ARTIFACT_LEDGER_CONTAINS_ERRORS')
    if ledger.get('status')!='PASS': errors.append('ARTIFACT_LEDGER_STATUS_NOT_PASS')
    return {'status':'PASS' if not errors else 'BLOCKED','errors':errors,'stage':stage,'executed':sorted(by_council)}

def validate_brain_execution_proof(session):
    errors=[]
    if not isinstance(session,dict): return {'status':'BLOCKED','errors':['BRAIN_SESSION_REQUIRED']}
    if session.get('state')!='COGNITIVE_LOCKED': errors.append('BRAIN_NOT_COGNITIVE_LOCKED')
    cov=validate_session(session)
    if cov.get('status')!='PASS': errors.append('BRAIN_COVERAGE_RECOMPUTE_FAILED')
    for x in session.get('invocations',[]) or []:
        errors.extend('BRAIN_'+e for e in _validate_host_native_invocation(x))
    exp=validate_expert_execution_ledger(session.get('expert_execution_ledger'))
    if exp.get('status')!='PASS': errors.extend('BRAIN_'+x for x in exp.get('errors',[]))
    return {'status':'PASS' if not errors else 'BLOCKED','errors':errors,'coverage_recomputed':cov,'expert_proof':exp}
