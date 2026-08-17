from __future__ import annotations
from .blackboard import Blackboard
from .provider import Invocation,NoExecutionProvider,resolve_brain_provider,provider_runtime_metadata
from .router import route
from .coverage import validate_session
from .utils import new_id,obj_hash
from .knowledge_readiness import detect_knowledge_needs
from .dynamic_councils import compose_dynamic_council
from .reasoning_pipelines import select_pipelines
from .expert_runtime import execute_expert_council
FUNCTION_BY_COUNCIL={'C13_ADVERSARIAL_COUNTERFACTUAL':'CHALLENGER','C15_META_COGNITION_INTEGRITY':'META_REVIEW','C16_RELEASE_TRUTHFULNESS':'RELEASE_CHAIR'}
def run_brain(task,provider=None,execution_mode='AUTO',host_invoke_fn=None,host_response_bundle=None,host_name='HOST_MODEL'):
    provider,resolution=resolve_brain_provider(provider,execution_mode=execution_mode,host_invoke_fn=host_invoke_fn,host_response_bundle=host_response_bundle,host_name=host_name)
    bb=Blackboard(task); bb.data['execution_mode_resolution']=resolution; bb.state('GROUNDED')
    def attach_provider_state():
        bb.data['provider_runtime']=provider_runtime_metadata(provider)
        pending=bb.data['provider_runtime'].get('pending_requests',[])
        if pending: bb.data['host_native_pending_requests']=pending
    # Runtime intelligence preflight: expertise routing, knowledge truth, working council, and reasoning pipeline selection.
    knowledge=detect_knowledge_needs(task); bb.data['knowledge_readiness']=knowledge
    bb.data['dynamic_working_council']=compose_dynamic_council(task)
    bb.data['reasoning_pipelines']=select_pipelines(task)
    strict=bool(task.get('strict_knowledge') or task.get('strict_mode') or task.get('requires_final_commercial_output'))
    if strict and knowledge.get('status')=='KNOWLEDGE_READINESS_BLOCK':
        bb.state('BLOCKED'); bb.data['release']={'status':'BLOCKED','reason':'KNOWLEDGE_READINESS_BLOCK','blockers':knowledge.get('blockers',[])}; attach_provider_state(); return bb.data
    role=task.get('rfp_role','UNKNOWN'); routed=route(role,bool(task.get('critical',True)),bool(task.get('rendered',False)),bool(task.get('deck_level',False)),False); bb.data['route']=routed; bb.state('ROUTED')
    pr=provider.invoke(Invocation('PRODUCER','C01_STRATEGIC_THESIS',new_id('ACTOR-PRODUCER'),new_id('CTX-PRODUCER'),{'task':task,'evidence':task.get('evidence',[]),'knowledge_readiness':knowledge,'dynamic_working_council':bb.data['dynamic_working_council'],'reasoning_pipelines':bb.data['reasoning_pipelines']})); bb.add_invocation(pr)
    if pr.get('status')!='PASS':
        bb.state('BLOCKED'); pending=pr.get('status')=='HOST_NATIVE_PENDING' or pr.get('reason')=='HOST_NATIVE_RESPONSE_REQUIRED'; bb.data['release']={'status':'BLOCKED','reason':'HOST_NATIVE_EXECUTION_PENDING' if pending else 'PRODUCER_NOT_EXECUTED'}; attach_provider_state(); return bb.data
    bb.data['cognitive_packet']=pr.get('output',{}); bb.state('PRODUCED')
    # Registered SMEs/simulators/governors are not decorative metadata. The routed expert council
    # must actually execute in isolated contexts before constitutional councils may lock cognition.
    expert=execute_expert_council(task,bb.data['cognitive_packet'],provider)
    bb.data['expert_execution_ledger']=expert
    for rr in expert.get('invocations',[]):
        bb.add_invocation(rr); bb.add_findings(rr.get('council_id','EXPERT_COUNCIL'),rr.get('function','SME_REVIEW'),rr)
    if expert.get('status')!='PASS':
        bb.state('BLOCKED'); bb.data['release']={'status':'BLOCKED','reason':'HOST_NATIVE_EXECUTION_PENDING' if provider_runtime_metadata(provider).get('pending_count') else 'EXPERT_COUNCIL_EXECUTION_INCOMPLETE','errors':expert.get('errors',[])}; attach_provider_state(); return bb.data
    bb.state('EXPERTS_EXECUTED')
    for cid in routed:
        fn=FUNCTION_BY_COUNCIL.get(cid,'COUNCIL_REVIEW'); rr=provider.invoke(Invocation(fn,cid,new_id('ACTOR-'+cid),new_id('CTX-'+cid),{'task':task,'cognitive_packet':bb.data['cognitive_packet'],'expert_execution_ledger':expert,'existing_findings':bb.data['findings']})); bb.add_invocation(rr); bb.add_findings(cid,fn,rr)
    bb.state('CHALLENGED'); cov=validate_session(bb.data); bb.data['coverage']=cov
    if cov['status']!='PASS': bb.state('BLOCKED'); bb.data['release']={'status':'BLOCKED','reason':'HOST_NATIVE_EXECUTION_PENDING' if provider_runtime_metadata(provider).get('pending_count') else 'COUNCIL_EXECUTION_INCOMPLETE','errors':cov['errors']}; attach_provider_state(); return bb.data
    open_findings=[f for f in bb.data['findings'] if f['disposition']=='OPEN' and f['severity'] in ('HIGH','CRITICAL','P0','P1')]
    if open_findings: bb.state('BLOCKED'); bb.data['release']={'status':'BLOCKED','reason':'UNRESOLVED_DISSENT'}; attach_provider_state(); return bb.data
    bb.state('DISSENT_RESOLVED'); bb.state('COGNITIVE_LOCKED'); bb.data['cognitive_packet_hash']=obj_hash(bb.data['cognitive_packet']); bb.data['release']={'status':'DRAFT_READY','reason':'ARTIFACT_RENDER_JUDGE_QA_RELEASE_STILL_REQUIRED'}; attach_provider_state(); return bb.data
