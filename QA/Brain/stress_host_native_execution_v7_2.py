#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json, random, sys, uuid
ROOT=Path(__file__).resolve().parents[2]
BR=ROOT/'Rashad/Brain/runtime'
sys.path.insert(0,str(BR))
from brain.provider import HostNativeProvider, Invocation
from brain.orchestrator import run_brain
from brain.execution_proof import validate_brain_execution_proof

R=random.Random(72034)
errors=[]; stats={'provider_valid':0,'provider_attack_blocked':0,'brain_runs':0,'brain_proof_pass':0,'unexpected_pass':0,'crashes':0}

def valid_response(req):
    fn=req['function']; ind=fn in ('INDEPENDENT_JUDGE','RELEASE_CHAIR')
    p={'request_key':req['request_key'],'host_session_id':req['host_session_id'],'host_response_id':'HSR-'+uuid.uuid4().hex.upper(),'source':'HOST_NATIVE_MODEL_EXECUTION','independent_context':bool(ind)}
    out={'status':'PASS','host_native_proof':p}
    if fn=='PRODUCER':
        out['output']={'management_question':'Decision?','evaluator_question':'Proof?','decision_supported':'STRESS_DECISION','answer_first_thesis':'Evidence-backed host-native stress thesis','evidence_for':['E1'],'evidence_against':[],'assumptions':[],'risks_counterarguments':['Challenge'],'semantic_relationships':['DEPENDS_ON'],'executive_implication':'Stress implication'}
    elif fn in ('CHALLENGER','COUNCIL_REVIEW','META_REVIEW','SME_REVIEW','EXECUTIVE_SIMULATION','EVALUATOR_SIMULATION','GOVERNOR_REVIEW','ARTIFACT_COUNCIL_REVIEW','ARTIFACT_RED_TEAM','ART_DIRECTION_REVIEW','PRODUCTION_READINESS_REVIEW'):
        out['findings']=[{'status':'NO_MATERIAL_OBJECTION','claim':'Stress review completed','evidence_refs':['E1'],'severity':'INFO'}]
    elif fn in ('INDEPENDENT_JUDGE','RELEASE_CHAIR'):
        out.update({'score':94,'hard_blockers':[],'evidence_refs':['E1']})
    return out

# 2,400 low-level proof trials: half valid, half adversarial.
functions=['PRODUCER','SME_REVIEW','COUNCIL_REVIEW','INDEPENDENT_JUDGE']
for i in range(2400):
    fn=functions[i%len(functions)]
    inv=Invocation(fn,'C-STRESS','A-'+str(i),'CTX-'+str(i),{'case':i,'evidence':['E1'],'noise':R.randint(0,10**9)})
    mode=i%2
    def cb(req, mode=mode):
        out=valid_response(req)
        if mode==0: return out
        mut=R.choice(['key','session','source','missing_response','independence'])
        p=out['host_native_proof']
        if mut=='key': p['request_key']='BAD-'+p['request_key']
        elif mut=='session': p['host_session_id']='BAD-SESSION'
        elif mut=='source': p['source']='FAKE_SOURCE'
        elif mut=='missing_response': p.pop('host_response_id',None)
        elif mut=='independence' and fn=='INDEPENDENT_JUDGE': p['independent_context']=False
        else: p['request_key']='BAD-'+p['request_key']
        return out
    try:
        pr=HostNativeProvider(cb,host_session_id='HS-STRESS-'+str(i))
        r=pr.invoke(inv)
        if mode==0:
            if r.get('status')!='PASS': errors.append({'case':i,'kind':'valid_rejected','result':r})
            else: stats['provider_valid']+=1
        else:
            if r.get('status')=='PASS': stats['unexpected_pass']+=1; errors.append({'case':i,'kind':'attack_escaped','result':r})
            else: stats['provider_attack_blocked']+=1
    except Exception as e:
        stats['crashes']+=1; errors.append({'case':i,'kind':'provider_crash','error':repr(e)})

# 180 full Brain executions spanning major domains. Every one must reach locked cognition
# and recompute executable proof rather than trusting a status label.
roles=['STRATEGIC_READING','COMMERCIAL_EXPOSURE','TECHNICAL_REQUIREMENTS','TEAM_REQUIREMENTS','EVALUATION_MECHANISM','RISK_MAP']
for i in range(180):
    role=roles[i%len(roles)]
    task={'task_id':'HN-STRESS-'+str(i),'rfp_role':role,'critical':bool(i%3==0),'rendered':False,'language':'AR' if i%2==0 else 'EN','evidence':[{'id':'E1'}], 'question':'AI cloud cybersecurity commercial delivery evidence procurement strategy '+str(i)}
    try:
        b=run_brain(task,execution_mode='HOST_NATIVE_MODE',host_invoke_fn=valid_response,host_name='STRESS_HOST')
        stats['brain_runs']+=1
        proof=validate_brain_execution_proof(b)
        if b.get('state')!='COGNITIVE_LOCKED' or proof.get('status')!='PASS':
            errors.append({'case':i,'kind':'brain_not_locked','state':b.get('state'),'proof':proof,'release':b.get('release')})
        else: stats['brain_proof_pass']+=1
    except Exception as e:
        stats['crashes']+=1; errors.append({'case':i,'kind':'brain_crash','error':repr(e)})

status='PASS' if not errors and stats['unexpected_pass']==0 and stats['crashes']==0 else 'FAIL'
out={'suite':'Host-Native Execution Stress v7.2','status':status,'operations':2580,'stats':stats,'error_count':len(errors),'errors':errors[:25]}
Path(__file__).with_name('HOST_NATIVE_EXECUTION_STRESS_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
raise SystemExit(0 if status=='PASS' else 1)
