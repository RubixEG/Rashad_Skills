#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import copy, json, tempfile, sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from rfp_summary_runtime import derive_pack_mode,derive_clarification_window,validate_ingestion_state,evaluate_pipeline,canonical_roles
from brain.visual_render import render_low_fidelity_candidates
from brain.provider import OpenAIResponsesProvider, ExternalCallableProvider, Invocation
from rfp_summary_orchestrator import execute_visual_search
from brain.utils import new_id

checks=[]
def ck(name,cond,detail=None): checks.append({'name':name,'status':'PASS' if cond else 'FAIL','detail':detail})
roles=canonical_roles()
manifest=[{'source_id':f'SRC-{i}','file_name':f'f{i}.pdf','category':c,'availability':'AVAILABLE','sha256':None,'authority':'CURRENT_RFP_SOURCE'} for i,c in enumerate(['MAIN_BOOKLET','SCOPE','BOQ','EVALUATION','QUALIFICATION','TEAM','CONTRACT','PAYMENT','SUBMISSION','CYBERSECURITY'],1)]
pm=derive_pack_mode(manifest,[]); ck('pack_mode_persistable_full',pm['source_pack_mode']=='FULL_RFP_PACK',pm)
pm2=derive_pack_mode(manifest[:-2],[{'reference':'Annex X','material':True}]); ck('pack_mode_stricter_partial',pm2['source_pack_mode']=='PARTIAL_RFP_PACK',pm2)
cw=derive_clarification_window({'pack_deadline':{'verified':True,'deadline_source_value':'2026-08-20','deadline_source_calendar':'GREGORIAN','deadline_normalized_gregorian':'2026-08-20T23:59:00+03:00','source_refs':['SRC-1:p1']}},'2026-08-16T15:00:00+03:00'); ck('clarification_window_derived_open',cw['status']=='OPEN',cw)
reg_item={'item_id':'I1','source_ref':'SRC-1','locator':'p.1','excerpt_pointer':'line/block 1','classification':'RFP_REQUIREMENT','owner':'INGESTION','status':'VERIFIED','downstream_refs':['ROLE-01']}
registers={k:([reg_item] if k in ('document_inventory','evidence_ledger','requirement_register') else []) for k in ['document_inventory','requirement_register','evaluation_criteria_register','submission_condition_register','deliverables_register','contract_obligation_register','assumption_exclusion_clarification_register','evidence_ledger','claim_commitment_register','contradiction_register','language_terminology_register']}
ing={'schema_version':'7.0.2','engagement_id':'ENG-TEST','source_manifest':manifest,'source_pack_mode':pm['source_pack_mode'],'source_pack_mode_basis':pm['source_pack_mode_basis'],'current_rfp_language':'ar','source_numeral_style':'ARABIC_INDIC','client_identity':{'status':'VERIFIED','name':'Test Client','evidence_refs':['SRC-1:p1']},'logo_availability':'NOT_INSPECTED','missing_annexes':[],'clarification_evidence':{'pack_deadline':{'verified':True,'deadline_source_value':'2026-08-20','deadline_source_calendar':'GREGORIAN','deadline_normalized_gregorian':'2026-08-20T23:59:00+03:00','source_refs':['SRC-1:p1']}},'clarification_window_state':cw,'registers':registers}
ck('ingestion_schema_machine_complete',not validate_ingestion_state(ing),validate_ingestion_state(ing))
role_plan=[{'role_id':r,'applicability':'REQUIRED','depth':'STANDARD'} for r in roles]
role_outputs={r:{'mandatory_content':['x'],'required_analysis':['analysis'],'evidence_refs':['SRC-1:p1'],'management_implication':'Management implication'} for r in roles}
packet={'page_id':'P08','role_id':'STRATEGIC_READING','management_question':'What decision does management need to make?','evaluator_question':'What must the evaluator believe?','decision_supported':'Bid strategy','answer_first_thesis':'The evidence supports one integrated operating-system interpretation.','evidence_for':[{'claim':'Supported claim','source_ref':'SRC-1','locator':'p.1','confidence':0.9}],'evidence_against':[],'assumptions':[{'statement':'Access is assumed','impact':'Schedule dependency','validation_owner':'PM'}],'counterarguments':['Alternative interpretation could reduce scope.'],'relationships':[{'source':'A','relation':'ENABLES','target':'B'}],'executive_implication':'Prioritize integration and governance.','council_route':[{'lens_id':'ENGAGEMENT_PARTNER','authorized_runtime_role_ids':['ROLE-PARTNER'],'challenge_question':'Is the thesis decision-relevant?','independence_required':False},{'lens_id':'SAUDI_GOVERNMENT_EVALUATOR','authorized_runtime_role_ids':['ROLE-PROCUREMENT','ROLE-REDTEAM','ROLE-SECTOR-SME'],'challenge_question':'Would the evaluator accept this?','independence_required':True},{'lens_id':'RED_TEAM_CHALLENGER','authorized_runtime_role_ids':['ROLE-REDTEAM'],'challenge_question':'What could make this wrong?','independence_required':True}]}
hyp=[{'id':'H1','dominant_form':'RING','reading_path':'CENTER_OUT','structural_signature':'RING|A'},{'id':'H2','dominant_form':'SPINE','reading_path':'RTL_SPINE','structural_signature':'SPINE|B'},{'id':'H3','dominant_form':'HUB','reading_path':'CENTER_OUT','structural_signature':'HUB|C'},{'id':'H4','dominant_form':'STACK','reading_path':'TOP_DOWN_THEN_RTL','structural_signature':'STACK|D'},{'id':'H5','dominant_form':'LANE','reading_path':'RTL_SPINE','structural_signature':'LANE|E'}]
with tempfile.TemporaryDirectory() as td:
    renders=render_low_fidelity_candidates(hyp,Path(td)/'initial'); ck('five_actual_low_fidelity_renders',len(renders)==5 and len({r['actual_render_hash'] for r in renders})==5,renders)
    mut=[dict(hyp[i%2],id=f'M{i+1}',structural_signature=f'MUT{i+1}') for i in range(4)]
    refined=render_low_fidelity_candidates(mut,Path(td)/'refined')
    dims=['OPPORTUNITY_ATTRACTIVENESS','STRATEGIC_FIT','WIN_POSITION','DELIVERY_CONFIDENCE','TEAM_READINESS','EVIDENCE_READINESS','COMMERCIAL_PRICING_CONFIDENCE','SCHEDULE_PRESSURE','PROCUREMENT_MATURITY','RISK_EXPOSURE']
    decision={'decision_id':'DEC-TEST','recommendation':'HOLD','decision_method':'EVIDENCE_SYNTHESIS_NOT_AUTOMATIC_WEIGHTED_SCORE','management_approval_required':True,'dimensions':[{'dimension':d,'assessment':'MIXED','confidence':0.7,'rationale':'Evidence supports a mixed assessment.','evidence_refs':[{'source_ref':'SRC-1','locator':'p.1'}]} for d in dims],'conditions':[],'blockers':['Internal readiness evidence is incomplete'],'required_actions':['Close the evidence gaps before management approval'],'counter_case':'If the missing readiness evidence is strong, the opportunity may justify a conditional go.','evidence_sufficiency':'PARTIAL_REQUIRES_CONDITIONS'}
    state={'schema_version':'7.0.2','engagement_id':'ENG-TEST','engagement_reset':{'status':'PASS'},'source_accountability':{'status':'PASS'},'output_config':{'language':'ar'},'canonical_role_order':roles,'step_evidence':{},'ingestion_state':ing,'role_plan':role_plan,'role_outputs':role_outputs,'analytical_page_ids':['P08'],'critical_page_ids':['P08'],'cognitive_packets':{'P08':packet},'council_sessions':{'P08':{'status':'PASS','producer_actor_id':'ACTOR-PRODUCER','judge_actor_id':'ACTOR-JUDGE','open_p0_p1':0}},'page_content_packs':{'P08':{'thesis':'x','evidence_refs':['SRC-1:p1']}},'semantic_graphs':{'P08':{'nodes':['A','B'],'edges':[{'source':'A','relation':'ENABLES','target':'B'}]}},'visual_search':{'P08':{'hypotheses':hyp,'renders':renders,'initial_independent_judgments':[{'candidate_id':f'H{i}','independent':True,'judge_invocation_id':f'J{i}','previous_response_id':None,'score':90+i,'actual_render_hash':renders[i-1]['actual_render_hash']} for i in range(1,6)],'top_2':['H5','H4'],'refined_renders':refined,'final_independent_judgment':{'independent':True,'judge_invocation_id':'JFINAL','previous_response_id':None,'winner_candidate_id':'M4','score':96,'actual_render_hash':refined[3]['actual_render_hash']}}},'qa_results':{'P08':{'artifact_truth_score':95,'ceqs_score':94,'required_detector_status':'PASS'}},'deck_qa':{'stress':'PASS','repair_safety':'PASS','cross_deck':'PASS'},'decision':decision,'release':{'masters_frozen':True,'pdf_pptx_parity':'PASS','proof_index':'PASS','qa_status':'QA_CANDIDATE_PASS','release_chair_status':'RELEASED'}}
    ok=evaluate_pipeline(state); ck('fifteen_step_machine_pipeline_passes',ok['status']=='PASS' and ok['passed_steps']==15,ok)
    x=copy.deepcopy(state); del x['ingestion_state']['source_pack_mode']; r=evaluate_pipeline(x); ck('missing_pack_mode_blocks_step3',r.get('first_non_pass')=='03',r)
    x=copy.deepcopy(state); x['cognitive_packets']={}; r=evaluate_pipeline(x); ck('missing_cognitive_packet_blocks_step6',r.get('first_non_pass')=='06',r)
    x=copy.deepcopy(state); x['visual_search']['P08']['initial_independent_judgments']=[]; r=evaluate_pipeline(x); ck('missing_independent_judge_blocks_step11',r.get('first_non_pass')=='11',r)
    x=copy.deepcopy(state); x['decision']['dimensions']=x['decision']['dimensions'][:-1]; r=evaluate_pipeline(x); ck('invalid_machine_decision_blocks_step14',r.get('first_non_pass')=='14',r)


# executable 5→9 orchestration with an isolated certification judge
def _cert_judge(inv):
    payload=inv.input_payload
    if payload.get('stage')=='FINAL_VISUAL_SELECTION':
        winner=payload['candidate_ids'][-1]
        return {'status':'PASS','independent':True,'judge_invocation_id':new_id('CERT-FINAL-JUDGE'),'previous_response_id':None,'winner_candidate_id':winner,'score':97,'hard_blockers':[],'evidence_refs':['SRC-1:p1']}
    cid=payload.get('candidate_id','H1'); digits=''.join(ch for ch in cid if ch.isdigit()) or '1'
    return {'status':'PASS','independent':True,'judge_invocation_id':new_id('CERT-JUDGE'),'previous_response_id':None,'score':90+int(digits),'hard_blockers':[],'evidence_refs':['SRC-1:p1']}
cert_provider=ExternalCallableProvider(_cert_judge)
valid_graph={'schema_version':'6.0','engagement_id':'ENG-TEST','page_id':'P08','nodes':[{'id':'A','type':'PROCESS','label':'Stage A','evidence':['EV-0001']},{'id':'B','type':'PROCESS','label':'Stage B','evidence':['EV-0002']},{'id':'C','type':'OUTCOME','label':'Outcome C','evidence':['EV-0003']}],'edges':[{'id':'E1','source':'A','target':'B','relation':'ENABLES','evidence':['EV-0001']},{'id':'E2','source':'B','target':'C','relation':'ENABLES','evidence':['EV-0002']}],'provenance':{'derived_from':['SRC-1'],'derived_at':'2026-08-16T12:00:00Z'}}
with tempfile.TemporaryDirectory() as td2:
    vo=execute_visual_search('P08',valid_graph,{'thesis':'Integrated system thesis'},td2,cert_provider)
    ck('executable_5_to_9_visual_search_orchestrator',vo.get('status')=='PASS' and vo.get('composition_count')==9 and len(vo.get('renders',[]))==5 and len(vo.get('refined_renders',[]))==4 and vo.get('winner') in {'M1','M2','M3','M4'},vo)

prov=OpenAIResponsesProvider(api_key=None,model=None); rr=prov.invoke(Invocation('PRODUCER','C01','A','CTX',{'x':1})); ck('live_provider_adapter_fails_closed_unconfigured',rr.get('status')=='NOT_EXECUTED' and rr.get('reason')=='OPENAI_PROVIDER_NOT_CONFIGURED',rr)
ext=ExternalCallableProvider(lambda inv:{'status':'PASS','output':{'ok':True}}); rr=ext.invoke(Invocation('PRODUCER','C01','A','CTX',{'x':1})); ck('external_provider_injection_executable',rr.get('status')=='PASS' and rr.get('output',{}).get('ok') is True,rr)

skill=ROOT.parents[1]/'Skill'
a=(skill/'01_ACTIVE_RUNTIME/69_V7_RFP_SUMMARY_CANONICAL_DECISION_ARCHITECTURE.md').read_text(encoding='utf-8')
wf=(skill/'05_WORKFLOW_ENGINE/23_V7_RFP_SUMMARY_DECISION_WORKFLOW.md').read_text(encoding='utf-8')
rrtxt=(skill/'01_ACTIVE_RUNTIME/rfp_summary_role_registry_v7.json').read_text(encoding='utf-8')
ck('active_authority_no_stale_workflow_ref','23_V7_0_1_RFP_SUMMARY_DECISION_WORKFLOW' not in a)
ck('active_authority_current_decision_schema','rfp_bid_decision_evidence_v7_0_1.schema.json' not in a)
ck('role_registry_current_decision_schema','rfp_bid_decision_evidence_v7_0_1.schema.json' not in rrtxt)
ck('workflow_requires_all_five_actual_renders','Render **all 5**' in wf)
ck('workflow_requires_5_to_9_search','9 actual compositions' in wf)

failed=[x for x in checks if x['status']=='FAIL']
out={'suite':'RFP Summary Execution Certification v7.0.2','status':'PASS' if not failed else 'FAIL','passed':len(checks)-len(failed),'total':len(checks),'checks':checks}
(Path(__file__).parent/'RFP_SUMMARY_EXECUTION_CERTIFICATION_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
for x in checks: print(x['status'],x['name'])
print(f"SUMMARY {out['passed']}/{out['total']} PASS")
raise SystemExit(1 if failed else 0)
