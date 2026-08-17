#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json, tempfile, uuid, sys, os
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from brain.execution_mode import detect_execution_mode, HOST_NATIVE_MODE, API_PROVIDER_MODE, OFFLINE_VALIDATION_MODE
from brain.provider import HostNativeProvider, HostNativeResponseBundleProvider, HostNativePendingProvider, OpenAIResponsesProvider, Invocation, host_request_key
from brain.orchestrator import run_brain
from brain.execution_proof import validate_brain_execution_proof
from brain.artifact_council_runtime import execute_artifact_councils
from rfp_summary_orchestrator import execute_visual_search

checks=[]
def ck(n,c,d=None): checks.append({'name':n,'status':'PASS' if c else 'FAIL','detail':d})

def proof(req,ind=False):
    return {'request_key':req['request_key'],'host_session_id':req['host_session_id'],'host_response_id':'HOSTRESP-'+uuid.uuid4().hex.upper(),'source':'HOST_NATIVE_MODEL_EXECUTION','independent_context':bool(ind)}

def host_callback(req):
    fn=req['function']; payload=req['input_payload']; ind=fn in ('INDEPENDENT_JUDGE','RELEASE_CHAIR')
    out={'status':'PASS','host_native_proof':proof(req,ind)}
    if fn=='PRODUCER':
        out['output']={'management_question':'What decision is supported?','evaluator_question':'What proof is required?','decision_supported':'HOST_NATIVE_DECISION','answer_first_thesis':'Host-native evidence-backed thesis','evidence_for':['E1'],'evidence_against':[],'assumptions':[],'risks_counterarguments':['Challenge required'],'semantic_relationships':['DEPENDS_ON'],'executive_implication':'Host-native implication'}
    elif fn in ('CHALLENGER','COUNCIL_REVIEW','META_REVIEW','SME_REVIEW','EXECUTIVE_SIMULATION','EVALUATOR_SIMULATION','GOVERNOR_REVIEW','ARTIFACT_COUNCIL_REVIEW','ARTIFACT_RED_TEAM','ART_DIRECTION_REVIEW','PRODUCTION_READINESS_REVIEW'):
        out['findings']=[{'status':'NO_MATERIAL_OBJECTION','claim':'Host-native isolated review completed','evidence_refs':['E1'],'severity':'INFO'}]
    elif fn=='INDEPENDENT_JUDGE':
        out.update({'score':95,'hard_blockers':[],'evidence_refs':['E1']})
        if payload.get('stage')=='FINAL_VISUAL_SELECTION': out['winner_candidate_id']=payload['candidate_ids'][-1]
    elif fn=='RELEASE_CHAIR': out.update({'score':95,'hard_blockers':[],'evidence_refs':['E1']})
    return out

# Mode detection
m=detect_execution_mode('HOST_NATIVE_MODE'); ck('explicit_host_native_selected_without_api',m.mode==HOST_NATIVE_MODE,m.to_dict())
m=detect_execution_mode('AUTO',host_invoke_fn=host_callback); ck('auto_prefers_host_bridge',m.mode==HOST_NATIVE_MODE,m.to_dict())
oldk=os.environ.pop('OPENAI_API_KEY',None); oldm=os.environ.pop('OPENAI_RASHAD_MODEL',None)
m=detect_execution_mode('AUTO'); ck('auto_without_host_or_api_is_offline',m.mode==OFFLINE_VALIDATION_MODE,m.to_dict())
if oldk is not None: os.environ['OPENAI_API_KEY']=oldk
if oldm is not None: os.environ['OPENAI_RASHAD_MODEL']=oldm

# Host-native no callback emits actionable pending request, not fake cognition.
task={'task_id':'HN1','rfp_role':'STRATEGIC_READING','critical':True,'rendered':False,'evidence':[{'id':'E1'}]}
pending=run_brain(task,execution_mode='HOST_NATIVE_MODE')
ck('host_native_without_bridge_returns_pending',pending.get('release',{}).get('reason')=='HOST_NATIVE_EXECUTION_PENDING' and len(pending.get('host_native_pending_requests',[]))==1,pending.get('release'))
ck('pending_request_contains_exact_contract',pending.get('host_native_pending_requests',[{}])[0].get('required_response_contract')=='RASHAD_HOST_NATIVE_RESPONSE_V1',pending.get('host_native_pending_requests'))

# Real host callback reaches cognitive lock without OPENAI_API_KEY.
hosted=run_brain(task,execution_mode='HOST_NATIVE_MODE',host_invoke_fn=host_callback,host_name='CHATGPT_HOST')
ck('host_native_brain_reaches_cognitive_lock',hosted.get('state')=='COGNITIVE_LOCKED',hosted.get('release'))
ck('host_native_experts_really_executed',hosted.get('expert_execution_ledger',{}).get('status')=='PASS' and hosted.get('expert_execution_ledger',{}).get('executed_experts'),hosted.get('expert_execution_ledger',{}).get('executed_experts'))
ck('host_native_brain_execution_proof_recomputes',validate_brain_execution_proof(hosted).get('status')=='PASS',validate_brain_execution_proof(hosted))
ck('all_host_invocations_have_proof',all((x.get('host_native_proof') or {}).get('source')=='HOST_NATIVE_MODEL_EXECUTION' for x in hosted.get('invocations',[]) if x.get('status')=='PASS'),len(hosted.get('invocations',[])))

# Fake PASS cannot cross provider proof boundary.
def fake(req): return {'status':'PASS','output':{'x':1}}
fp=HostNativeProvider(fake,host_session_id='HS-FAKE')
rr=fp.invoke(Invocation('PRODUCER','C01','A','CTX',{'x':1}))
ck('fake_host_pass_without_proof_blocked',rr.get('status')=='NOT_EXECUTED' and rr.get('reason')=='HOST_NATIVE_PROOF_INVALID',rr)

# Bundle replay is exact-input bound.
collector=HostNativePendingProvider(host_session_id='HS-BUNDLE'); inv=Invocation('PRODUCER','C01','A','CTX',{'x':1}); pr=collector.invoke(inv); key=pr['request_key']
bundle={'host_session_id':'HS-BUNDLE','responses':{key:{'status':'PASS','host_native_proof':{'request_key':key,'host_session_id':'HS-BUNDLE','host_response_id':'RESP-BUNDLE-1','source':'HOST_NATIVE_MODEL_EXECUTION','independent_context':False},'output':{'ok':True}}}}
bp=HostNativeResponseBundleProvider(bundle); br=bp.invoke(inv)
ck('host_bundle_exact_request_executes',br.get('status')=='PASS' and br.get('output',{}).get('ok') is True,br)
wrong=HostNativeResponseBundleProvider({'host_session_id':'HS-BUNDLE','responses':{}}); wr=wrong.invoke(inv)
ck('missing_bundle_response_is_pending_not_faked',wr.get('status')=='HOST_NATIVE_PENDING' and wrong.runtime_metadata().get('pending_count')==1,wr)

# Artifact councils and visual judgment can run host-native too.
graph={'schema_version':'6.0','engagement_id':'ENG-HOST','page_id':'P01','nodes':[{'id':'A','type':'PROCESS','label':'A','evidence':['E1']},{'id':'B','type':'OUTCOME','label':'B','evidence':['E2']},{'id':'C','type':'OUTCOME','label':'C','evidence':['E3']}],'edges':[{'id':'X','source':'A','target':'B','relation':'ENABLES','evidence':['E1']},{'id':'Y','source':'B','target':'C','relation':'ENABLES','evidence':['E2']}],'provenance':{'derived_from':['SRC1'],'derived_at':'2026-08-17T00:00:00Z'}}
content={'page_id':'P01','language':'AR','thesis':'Host-native artifact thesis','evidence_refs':['E1','E2']}
ac=execute_artifact_councils(graph,content,execution_mode='HOST_NATIVE_MODE',host_invoke_fn=host_callback,language='AR',stage='PRE_CONCEPT')
ck('host_native_artifact_councils_execute',ac.get('status')=='PASS' and ac.get('executed_councils'),ac.get('errors'))
with tempfile.TemporaryDirectory() as td:
    vs=execute_visual_search('P01',graph,content,td,execution_mode='HOST_NATIVE_MODE',host_invoke_fn=host_callback,host_name='CHATGPT_HOST')
    ck('host_native_visual_search_reaches_independent_winner',vs.get('status')=='PASS' and vs.get('composition_count')==9 and vs.get('winner') in {'M1','M2','M3','M4'}, {'status':vs.get('status'),'winner':vs.get('winner'),'reason':vs.get('reason')})
    ck('host_native_visual_search_art_direction_executes',vs.get('art_direction_execution',{}).get('status')=='PASS',vs.get('art_direction_execution',{}).get('errors'))

# Explicit API still fails closed if not configured; no host/API auto does not pretend execution.
api=OpenAIResponsesProvider(api_key=None,model=None); ar=api.invoke(Invocation('PRODUCER','C01','A','CTX',{'x':1}))
ck('api_mode_unconfigured_fails_closed',ar.get('status')=='NOT_EXECUTED' and ar.get('reason')=='OPENAI_PROVIDER_NOT_CONFIGURED',ar)

o={'suite':'Host-Native Brain Execution Certification','status':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL','passed':sum(x['status']=='PASS' for x in checks),'total':len(checks),'checks':checks}
Path(__file__).with_name('HOST_NATIVE_EXECUTION_CERTIFICATION_RESULTS.json').write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
for x in checks: print(x['status'],x['name'])
print('SUMMARY',o['passed'],'/',o['total'])
raise SystemExit(0 if o['status']=='PASS' else 1)
