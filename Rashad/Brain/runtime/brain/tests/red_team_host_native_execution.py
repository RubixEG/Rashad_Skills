#!/usr/bin/env python3
from pathlib import Path
import sys,uuid,json
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from brain.provider import HostNativeProvider,HostNativeResponseBundleProvider,Invocation
from brain.orchestrator import run_brain
from brain.execution_proof import validate_brain_execution_proof
att=[]
def add(n,blocked,d=None): att.append({'attack':n,'status':'BLOCKED' if blocked else 'BYPASS','detail':d})

inv=Invocation('PRODUCER','C01','A','CTX',{'x':1})
# A1 missing proof
p=HostNativeProvider(lambda req:{'status':'PASS','output':{'x':1}},host_session_id='HS')
r=p.invoke(inv); add('A1_missing_host_proof',r.get('status')!='PASS',r)
# A2 wrong request key
p=HostNativeProvider(lambda req:{'status':'PASS','host_native_proof':{'request_key':'WRONG','host_session_id':'HS','host_response_id':'R1','source':'HOST_NATIVE_MODEL_EXECUTION','independent_context':False},'output':{'x':1}},host_session_id='HS')
r=p.invoke(inv); add('A2_wrong_request_key',r.get('status')!='PASS',r)
# A3 wrong session
p=HostNativeProvider(lambda req:{'status':'PASS','host_native_proof':{'request_key':req['request_key'],'host_session_id':'OTHER','host_response_id':'R1','source':'HOST_NATIVE_MODEL_EXECUTION','independent_context':False},'output':{'x':1}},host_session_id='HS')
r=p.invoke(inv); add('A3_wrong_host_session',r.get('status')!='PASS',r)
# A4 fake source
p=HostNativeProvider(lambda req:{'status':'PASS','host_native_proof':{'request_key':req['request_key'],'host_session_id':'HS','host_response_id':'R1','source':'SCRIPTED_TEST','independent_context':False},'output':{'x':1}},host_session_id='HS')
r=p.invoke(inv); add('A4_fake_host_source',r.get('status')!='PASS',r)
# A5 judge without independent context
jinv=Invocation('INDEPENDENT_JUDGE','C11','A','CTX',{'actual_render_hash':'H'})
p=HostNativeProvider(lambda req:{'status':'PASS','host_native_proof':{'request_key':req['request_key'],'host_session_id':'HS','host_response_id':'J1','source':'HOST_NATIVE_MODEL_EXECUTION','independent_context':False},'score':100},host_session_id='HS')
r=p.invoke(jinv); add('A5_judge_not_independent',r.get('status')!='PASS',r)
# A6 replay response id
cnt={'n':0}
def replay(req): return {'status':'PASS','host_native_proof':{'request_key':req['request_key'],'host_session_id':'HS','host_response_id':'SAME','source':'HOST_NATIVE_MODEL_EXECUTION','independent_context':False},'findings':[],'output':{'x':1}}
p=HostNativeProvider(replay,host_session_id='HS'); r1=p.invoke(inv); r2=p.invoke(Invocation('COUNCIL_REVIEW','C02','B','CTX2',{'y':2})); add('A6_response_id_replay',r1.get('status')=='PASS' and r2.get('reason')=='HOST_NATIVE_RESPONSE_REUSED',[r1,r2])
# A7 bundle keyed to different input cannot execute
bundle={'host_session_id':'HS','responses':{'bad':{'status':'PASS'}}}; p=HostNativeResponseBundleProvider(bundle); r=p.invoke(inv); add('A7_bundle_input_hash_substitution',r.get('status')=='HOST_NATIVE_PENDING',r)
# A8 explicit host mode with no bridge must not silently fall back to API/offline cognition
t=run_brain({'rfp_role':'STRATEGIC_READING','critical':True,'evidence':['E1']},execution_mode='HOST_NATIVE_MODE'); add('A8_host_mode_no_bridge_fails_pending',t.get('release',{}).get('reason')=='HOST_NATIVE_EXECUTION_PENDING',t.get('release'))
# A9 fabricated locked session with fake host proof fails recompute
fake={'state':'COGNITIVE_LOCKED','task':{'critical':True},'route':['C01_STRATEGIC_THESIS'],'findings':[],'invocations':[{'status':'PASS','function':'PRODUCER','council_id':'C01_STRATEGIC_THESIS','actor_id':'A','isolated_context_id':'CTX','invocation_id':'R','execution_mode':'HOST_NATIVE_MODE','host_native':True,'request_key':'K','host_native_proof':{'request_key':'BAD','host_session_id':'HS','host_response_id':'R','source':'HOST_NATIVE_MODEL_EXECUTION'}}], 'expert_execution_ledger':{'status':'PASS','execution_proof':'ISOLATED_INVOCATION_LEDGER','required_experts':['X'],'executed_experts':['X'],'invocations':[{'status':'PASS','expert_role_id':'X','function':'SME_REVIEW','actor_id':'EA','isolated_context_id':'EC','invocation_id':'ER','execution_mode':'HOST_NATIVE_MODE','host_native':True,'request_key':'K2','host_native_proof':{'request_key':'BAD','host_session_id':'HS','host_response_id':'ER','source':'HOST_NATIVE_MODEL_EXECUTION'}}], 'errors':[]}}
vr=validate_brain_execution_proof(fake); add('A9_fabricated_host_locked_session',vr.get('status')!='PASS',vr)

out={'suite':'Host-Native Execution Red Team','status':'PASS' if all(x['status']=='BLOCKED' for x in att) else 'FAIL','blocked':sum(x['status']=='BLOCKED' for x in att),'total':len(att),'attacks':att}
Path(__file__).with_name('HOST_NATIVE_EXECUTION_RED_TEAM_RESULTS.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
for x in att: print(x['status'],x['attack'])
print('SUMMARY',out['blocked'],'/',out['total'],'BLOCKED')
raise SystemExit(0 if out['status']=='PASS' else 1)
