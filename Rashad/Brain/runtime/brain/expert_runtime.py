from __future__ import annotations
from .expert_router import route_experts
from .ontology import actor
from .provider import Invocation, NoExecutionProvider, resolve_brain_provider
from .utils import new_id

FUNCTION_BY_TYPE={
    'SME':'SME_REVIEW','EXECUTIVE_SIMULATOR':'EXECUTIVE_SIMULATION',
    'EVALUATOR_SIMULATOR':'EVALUATOR_SIMULATION','GOVERNOR':'GOVERNOR_REVIEW'
}

def execute_expert_council(task:dict,cognitive_packet:dict,provider=None,execution_mode='AUTO',host_invoke_fn=None,host_response_bundle=None,host_name='HOST_MODEL'):
    provider,_=resolve_brain_provider(provider,execution_mode=execution_mode,host_invoke_fn=host_invoke_fn,host_response_bundle=host_response_bundle,host_name=host_name); route=route_experts(task)
    if route.get('status')!='PASS': return {'status':'BLOCKED','route':route,'reason':'EXPERT_ROUTING_INVALID'}
    inv=[]; findings=[]; errors=[]; actor_ids=set(); context_ids=set()
    for rid in route['selected_experts']:
        a=actor(rid)
        if not a:
            errors.append({'kind':'UNKNOWN_EXPERT','actor_id':rid}); continue
        fn=FUNCTION_BY_TYPE.get(a['type'],'SME_REVIEW')
        ctx=new_id('CTX-EXPERT-'+rid); aid=new_id('ACTOR-'+rid)
        rr=provider.invoke(Invocation(fn,'EXPERT_COUNCIL',aid,ctx,{
            'expert_role_id':rid,'expert_type':a['type'],'cognitive_functions':a.get('functions',[]),
            'task':task,'cognitive_packet':cognitive_packet,'knowledge_pack':a.get('knowledge_pack')
        }))
        rr=dict(rr); rr['expert_role_id']=rid; rr['expert_type']=a['type']; inv.append(rr)
        if rr.get('status')!='PASS': errors.append({'kind':'EXPERT_NOT_EXECUTED','expert_role_id':rid,'status':rr.get('status')}); continue
        if aid in actor_ids or ctx in context_ids: errors.append({'kind':'EXPERT_CONTEXT_OR_ACTOR_REUSED','expert_role_id':rid})
        actor_ids.add(aid); context_ids.add(ctx)
        for f in rr.get('findings',[]) or []:
            ff=dict(f); ff['expert_role_id']=rid; findings.append(ff)
        if a['type']=='GOVERNOR' and rr.get('veto'):
            errors.append({'kind':'GOVERNOR_VETO','expert_role_id':rid,'veto':rr.get('veto')})
    executed={x.get('expert_role_id') for x in inv if x.get('status')=='PASS'}
    missing=[x for x in route['selected_experts'] if x not in executed]
    if missing: errors.append({'kind':'REQUIRED_EXPERT_EXECUTION_MISSING','roles':missing})
    return {
        'status':'PASS' if not errors else 'BLOCKED','route':route,'required_experts':route['selected_experts'],
        'executed_experts':sorted(executed),'invocations':inv,'findings':findings,'errors':errors,
        'execution_proof':'ISOLATED_INVOCATION_LEDGER','registered_is_not_executed':True
    }
