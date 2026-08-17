#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys,json,random,time
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/'Rashad/Brain/runtime'))
from brain.expert_router import route_experts
from brain.orchestrator import run_brain
from brain.provider import ScriptedTestProvider
from brain.artifact_brain import generate_communication_hypotheses,route_artifact_councils
from brain.artifact_council_runtime import execute_artifact_councils
from brain.execution_proof import validate_brain_execution_proof,validate_artifact_execution_ledger
random.seed(7202026)
roles=['MANAGEMENT_DECISION','COMMERCIAL_EXPOSURE','BOQ_INTELLIGENCE','TEAM_CAPACITY','TECHNICAL_REQUIREMENTS','QUALIFICATION_EVIDENCE','EVALUATION_WIN','CLARIFICATIONS','RISKS','SCOPE_ARCHITECTURE','DELIVERY_JOURNEY']
domains=[
 ('AI platform data APIs machine learning','AI_DATA'),('cybersecurity privacy IAM SIEM','CYBER_PRIVACY'),('cloud kubernetes docker devops','CLOUD_DEVOPS'),
 ('backend frontend mobile API software','SOFTWARE_ENGINEERING'),('UX accessibility WCAG','UX_ACCESSIBILITY'),('fixed price margin payment working capital','FINANCIAL_COMMERCIAL'),
 ('contract procurement tender penalty','LEGAL_PROCUREMENT'),('SAP integration','SAP'),('Oracle integration','ORACLE'),('Salesforce CRM','SALESFORCE'),('OT ICS industrial control','OT_ICS')]
errors=[]; counters={'route_cases':0,'brain_runs':0,'key_name_attacks':0,'artifact_cases':0,'artifact_execution_runs':0}
start=time.monotonic()
# Routing chaos
for i in range(3000):
    role=random.choice(roles); parts=random.sample(domains,k=random.randint(0,4)); text='; '.join(x[0] for x in parts) or 'general strategy and management decision'
    t={'task_id':f'R{i}','rfp_role':role,'critical':random.random()>.05,'question':text,'nested':{'content':text}}
    try:r=route_experts(t)
    except Exception as e: errors.append(['ROUTE_CRASH',i,repr(e)]); continue
    counters['route_cases']+=1
    if r.get('status')!='PASS':errors.append(['ROUTE_BLOCK',i,r])
    if r.get('selected_count',99)>r.get('max_active_experts',0):errors.append(['ROUTE_BUDGET_ESCAPE',i,r.get('selected_count')])
    if r.get('unknown_configured_roles'):errors.append(['UNKNOWN_ROLE',i,r.get('unknown_configured_roles')])
    if set(r.get('required_experts',[]))-set(r.get('selected_experts',[])):errors.append(['REQUIRED_NOT_SELECTED',i,r])
# Metadata key-name attacks
for i in range(1000):
    key=random.choice(['sap_procurement_key','cyber_cloud_key','oracle_ai_key','salesforce_rfp_key','finops_margin_key'])
    t={'task_id':f'K{i}','rfp_role':'MANAGEMENT_DECISION','critical':True,key:'ordinary strategy only','payload':{'another_fake_procurement_key':'management only'}}
    r=route_experts(t); counters['key_name_attacks']+=1
    forbidden={'SAP','CYBER_PRIVACY','ORACLE','SALESFORCE','FINANCIAL_COMMERCIAL','CLOUD_DEVOPS'}
    if forbidden & set(r.get('matched_domains',[])):errors.append(['KEY_NAME_FALSE_TRIGGER',i,key,r.get('matched_domains')])
# Full executable Brain runs with evidence; skip knowledge-blocking price final-output wording.
for i in range(250):
    role=random.choice(roles); text=random.choice(domains)[0]
    t={'task_id':f'B{i}','rfp_role':role,'critical':True,'rendered':bool(i%2),'question':text,'evidence':[{'id':'E1','source':'fixture'}]}
    try:b=run_brain(t,ScriptedTestProvider())
    except Exception as e: errors.append(['BRAIN_CRASH',i,repr(e)]); continue
    counters['brain_runs']+=1
    if b.get('state')!='COGNITIVE_LOCKED':errors.append(['BRAIN_NOT_LOCKED',i,b.get('state'),b.get('release')])
    pr=validate_brain_execution_proof(b)
    if pr.get('status')!='PASS':errors.append(['BRAIN_PROOF_FAIL',i,pr.get('errors')])
# Artifact search chaos: multiple information types, every search must remain diverse and non-diagram-only.
texts=['87.5% technical threshold and 70/80 required','compare option A versus option B tradeoff','evidence from 16 documents supports HOLD decision','timeline submission award start','AI architecture APIs data cyber infrastructure','team of 24 across 12 roles','decision gates GO HOLD conditions','customer journey from idea to POC to service']
for i in range(1500):
    txt=random.choice(texts); graph={'nodes':[{'id':'N1','label':'A'},{'id':'N2','label':'B'}],'edges':[] if i%3==0 else [{'source':'N1','target':'N2','relation':'SUPPORTS'}]}
    content={'page_id':f'P{i}','thesis':txt,'answer_first_thesis':txt,'evidence':['E1'],'numbers':[87.5,70,80] if '%' in txt else [],'language':'AR','decision':'HOLD' if 'decision' in txt or 'HOLD' in txt else ''}
    try:h=generate_communication_hypotheses(graph,content,5); rt=route_artifact_councils(graph,content,'AR','PRE_CONCEPT')
    except Exception as e: errors.append(['ARTIFACT_CRASH',i,repr(e)]); continue
    counters['artifact_cases']+=1
    if h.get('status')!='PASS' or h.get('distinct_communication_strategies')!=5 or h.get('distinct_strategy_families',0)<3:errors.append(['ARTIFACT_DIVERSITY_FAIL',i,h])
    if h.get('diagram_only_search'):errors.append(['DIAGRAM_ONLY_COLLAPSE',i,h])
    if not h.get('contains_minimal_hypothesis'):errors.append(['NO_MINIMAL_CANDIDATE',i,h])
    if rt.get('status')!='PASS' or 'ARABIC_RTL_COUNCIL' not in rt.get('active_councils',[]):errors.append(['ARABIC_ARTIFACT_ROUTE_FAIL',i,rt])
# Executable artifact council stress
for i in range(200):
    graph={'nodes':[{'id':'N1'},{'id':'N2'}],'edges':[{'source':'N1','target':'N2','relation':'ENABLES'}]}; content={'page_id':f'E{i}','thesis':random.choice(texts),'evidence':['E1'],'language':'AR'}
    a=execute_artifact_councils(graph,content,ScriptedTestProvider(),'AR','PRE_CONCEPT'); counters['artifact_execution_runs']+=1
    pr=validate_artifact_execution_ledger(a,'PRE_CONCEPT')
    if pr.get('status')!='PASS':errors.append(['ARTIFACT_EXECUTION_PROOF_FAIL',i,pr.get('errors')])

out={'suite':'Rashad v7.2 Brain Coherence Stress & Quality','status':'PASS' if not errors else 'FAIL','counters':counters,'error_count':len(errors),'errors':errors[:50],'duration_sec':round(time.monotonic()-start,3),'quality_assertions':['bounded expert activation','no unknown configured roles','all required roles selected','semantic values not key names','full Brain cognitive lock with recomputed proof','five distinct artifact strategies','three+ strategy families','non-diagram candidate required','Arabic RTL Artifact council routed','artifact councils actually executed']}
path=ROOT/'QA/Certification/V7_2_BRAIN_COHERENCE_STRESS.json'; path.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 1)
