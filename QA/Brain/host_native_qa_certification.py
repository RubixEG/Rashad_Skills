#!/usr/bin/env python3
from pathlib import Path
import json,uuid,sys,os
HERE=Path(__file__).resolve().parent; sys.path.insert(0,str(HERE))
from provider import HostNativeQAProvider,HostNativeQAResponseBundleProvider,HostNativeQAPendingProvider,QAInvocation
from orchestrator import run_qa_brain
checks=[]
def ck(n,c,d=None): checks.append({'name':n,'status':'PASS' if c else 'FAIL','detail':d})
def cb(req):
    return {'status':'PASS','host_native_proof':{'request_key':req['request_key'],'host_session_id':req['host_session_id'],'host_response_id':'QAHOST-'+uuid.uuid4().hex.upper(),'source':'HOST_NATIVE_MODEL_EXECUTION','independent_context':True},'findings':[{'severity':'INFO','status':'NO_MATERIAL_OBJECTION','claim':'Host-native independent QA review completed','evidence_refs':['PIXEL-HASH']} ]}
ctx={'deck_level':True,'rendered':True,'user_visible':True,'language':'AR'}; det={'status':'PASS'}
pending=run_qa_brain(ctx,det,execution_mode='HOST_NATIVE_MODE')
ck('qa_host_native_no_bridge_returns_pending',pending.get('status')=='FAIL' and pending.get('provider_runtime',{}).get('pending_count',0)>0,pending.get('provider_runtime'))
hosted=run_qa_brain(ctx,det,execution_mode='HOST_NATIVE_MODE',host_invoke_fn=cb,host_name='CHATGPT_HOST')
ck('qa_host_native_reaches_candidate_pass',hosted.get('status')=='PASS' and hosted.get('final_verdict')=='QA_CANDIDATE_PASS',hosted.get('errors'))
ck('qa_host_native_executes_all_required',set(hosted.get('required_councils',[]))==set(hosted.get('executed_councils',[])),hosted.get('executed_councils'))
ck('qa_host_native_all_independent',all(x.get('independent') is True and (x.get('host_native_proof') or {}).get('independent_context') is True for x in hosted.get('invocations',[])),len(hosted.get('invocations',[])))
# fake proof blocked
def fake(req): return {'status':'PASS','findings':[],'host_native_proof':{'request_key':'BAD','host_session_id':req['host_session_id'],'host_response_id':'X','source':'HOST_NATIVE_MODEL_EXECUTION','independent_context':True}}
p=HostNativeQAProvider(fake,host_session_id='HS'); r=p.invoke(QAInvocation('Q01','QA_COUNCIL_REVIEW','A','C',{})); ck('qa_fake_host_proof_blocked',r.get('status')!='PASS',r)
# missing bundle response pending
b=HostNativeQAResponseBundleProvider({'host_session_id':'HS','responses':{}}); r=b.invoke(QAInvocation('Q01','QA_COUNCIL_REVIEW','A','C',{})); ck('qa_bundle_missing_response_pending',r.get('status')=='HOST_NATIVE_PENDING' and b.runtime_metadata().get('pending_count')==1,r)
out={'suite':'Host-Native QA Certification','status':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL','passed':sum(x['status']=='PASS' for x in checks),'total':len(checks),'checks':checks}
(HERE/'HOST_NATIVE_QA_CERTIFICATION_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
for x in checks: print(x['status'],x['name'])
print('SUMMARY',out['passed'],'/',out['total'])
raise SystemExit(0 if out['status']=='PASS' else 1)
