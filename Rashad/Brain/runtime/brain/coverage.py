from __future__ import annotations

def validate_session(session):
    errs=[]; inv=session.get('invocations',[]); route=session.get('route',[]); findings=session.get('findings',[])
    executed={x.get('council_id') for x in inv if x.get('status')=='PASS'}
    for c in route:
        if c not in executed: errs.append({'kind':'COUNCIL_NOT_EXECUTED','council_id':c})
    if not any(x.get('function')=='PRODUCER' and x.get('status')=='PASS' for x in inv): errs.append({'kind':'PRODUCER_NOT_EXECUTED'})
    expert=session.get('expert_execution_ledger')
    if session.get('task',{}).get('critical',True):
        if not isinstance(expert,dict) or expert.get('status')!='PASS': errs.append({'kind':'EXPERT_COUNCIL_EXECUTION_NOT_PROVEN'})
        else:
            required=set(expert.get('required_experts',[])); executed=set(expert.get('executed_experts',[]))
            if required-executed: errs.append({'kind':'EXPERT_EXECUTION_COVERAGE_GAP','missing':sorted(required-executed)})
    if 'C13_ADVERSARIAL_COUNTERFACTUAL' in route and not any(f.get('council_id')=='C13_ADVERSARIAL_COUNTERFACTUAL' for f in findings): errs.append({'kind':'NO_ADVERSARIAL_FINDING'})
    open_high=[f for f in findings if f.get('disposition')=='OPEN' and f.get('severity') in ('HIGH','CRITICAL','P0','P1')]
    if open_high: errs.append({'kind':'OPEN_HIGH_FINDINGS','count':len(open_high)})
    producers={x.get('actor_id') for x in inv if x.get('function')=='PRODUCER'}
    for x in inv:
        if x.get('function') in ('INDEPENDENT_JUDGE','RELEASE_CHAIR'):
            if x.get('actor_id') in producers: errs.append({'kind':'PRODUCER_JUDGE_COLLISION','actor_id':x.get('actor_id')})
            if x.get('previous_response_id'): errs.append({'kind':'JUDGE_CHAINED_TO_PRODUCER_RESPONSE'})
            if x.get('independent') is not True: errs.append({'kind':'JUDGE_NOT_INDEPENDENT'})
            if not x.get('judge_invocation_id'): errs.append({'kind':'JUDGE_INVOCATION_ID_MISSING'})
    return {'status':'PASS' if not errs else 'FAIL','errors':errs,'executed_councils':sorted(x for x in executed if x)}
