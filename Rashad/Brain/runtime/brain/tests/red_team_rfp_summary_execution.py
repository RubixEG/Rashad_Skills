#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import copy,json,sys,tempfile
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT))
from rfp_summary_runtime import evaluate_pipeline,derive_pack_mode,derive_clarification_window,canonical_roles
from brain.visual_render import render_low_fidelity_candidates

checks=[]
def attack(name,state,expected_step):
 r=evaluate_pipeline(state); ok=r.get('status')=='BLOCKED' and r.get('first_non_pass')==expected_step
 checks.append({'attack':name,'status':'BLOCKED_AS_EXPECTED' if ok else 'BYPASS','expected_step':expected_step,'result':r})
roles=canonical_roles(); cats=['MAIN_BOOKLET','SCOPE','BOQ','EVALUATION','QUALIFICATION','TEAM','CONTRACT','PAYMENT','SUBMISSION','CYBERSECURITY']
manifest=[{'source_id':f'SRC-{i}','file_name':f'f{i}.pdf','category':c,'availability':'AVAILABLE','sha256':None,'authority':'CURRENT_RFP_SOURCE'} for i,c in enumerate(cats,1)]
pm=derive_pack_mode(manifest,[]); ce={'pack_deadline':{'verified':True,'deadline_source_value':'2026-08-20','deadline_source_calendar':'GREGORIAN','deadline_normalized_gregorian':'2026-08-20T23:59:00+03:00','source_refs':['SRC-1:p1']}}; cw=derive_clarification_window(ce,'2026-08-16T15:00:00+03:00')
item={'item_id':'I1','source_ref':'SRC-1','locator':'p.1','excerpt_pointer':'block1','classification':'RFP_REQUIREMENT','owner':'INGESTION','status':'VERIFIED','downstream_refs':['P08']}
regs={k:([item] if k in ('document_inventory','requirement_register','evidence_ledger') else []) for k in ['document_inventory','requirement_register','evaluation_criteria_register','submission_condition_register','deliverables_register','contract_obligation_register','assumption_exclusion_clarification_register','evidence_ledger','claim_commitment_register','contradiction_register','language_terminology_register']}
ing={'schema_version':'7.0.2','engagement_id':'ENG-RT','source_manifest':manifest,'source_pack_mode':pm['source_pack_mode'],'source_pack_mode_basis':pm['source_pack_mode_basis'],'current_rfp_language':'ar','source_numeral_style':'ARABIC_INDIC','client_identity':{'status':'VERIFIED','name':'Client','evidence_refs':['SRC-1:p1']},'logo_availability':'NOT_INSPECTED','missing_annexes':[],'clarification_evidence':ce,'clarification_window_state':cw,'registers':regs}
packet={'page_id':'P08','role_id':'STRATEGIC_READING','management_question':'What decision does management need to make?','evaluator_question':'What must evaluator believe?','decision_supported':'Bid strategy','answer_first_thesis':'Evidence supports integrated interpretation.','evidence_for':[{'claim':'Supported','source_ref':'SRC-1','locator':'p.1','confidence':0.9}],'evidence_against':[],'assumptions':[{'statement':'Assume access','impact':'schedule','validation_owner':'PM'}],'counterarguments':['Alternative exists'],'relationships':[{'source':'A','relation':'ENABLES','target':'B'}],'executive_implication':'Prioritize governance.','council_route':[{'lens_id':'ENGAGEMENT_PARTNER','authorized_runtime_role_ids':['ROLE-PARTNER'],'challenge_question':'Decision relevant?','independence_required':False},{'lens_id':'SAUDI_GOVERNMENT_EVALUATOR','authorized_runtime_role_ids':['ROLE-PROCUREMENT','ROLE-REDTEAM','ROLE-SECTOR-SME'],'challenge_question':'Evaluator accept?','independence_required':True},{'lens_id':'RED_TEAM_CHALLENGER','authorized_runtime_role_ids':['ROLE-REDTEAM'],'challenge_question':'What is wrong?','independence_required':True}]}
hyp=[{'id':'H1','dominant_form':'RING','reading_path':'CENTER_OUT','structural_signature':'R1'},{'id':'H2','dominant_form':'SPINE','reading_path':'RTL_SPINE','structural_signature':'S2'},{'id':'H3','dominant_form':'HUB','reading_path':'CENTER_OUT','structural_signature':'H3'},{'id':'H4','dominant_form':'STACK','reading_path':'TOP_DOWN_THEN_RTL','structural_signature':'T4'},{'id':'H5','dominant_form':'LANE','reading_path':'RTL_SPINE','structural_signature':'L5'}]
with tempfile.TemporaryDirectory() as td:
 renders=render_low_fidelity_candidates(hyp,Path(td)/'i'); mut=[dict(hyp[i%2],id=f'M{i+1}',structural_signature=f'M{i+1}') for i in range(4)]; refined=render_low_fidelity_candidates(mut,Path(td)/'r')
 dims=['OPPORTUNITY_ATTRACTIVENESS','STRATEGIC_FIT','WIN_POSITION','DELIVERY_CONFIDENCE','TEAM_READINESS','EVIDENCE_READINESS','COMMERCIAL_PRICING_CONFIDENCE','SCHEDULE_PRESSURE','PROCUREMENT_MATURITY','RISK_EXPOSURE']
 dec={'decision_id':'DEC-RED','recommendation':'HOLD','decision_method':'EVIDENCE_SYNTHESIS_NOT_AUTOMATIC_WEIGHTED_SCORE','management_approval_required':True,'dimensions':[{'dimension':d,'assessment':'MIXED','confidence':.7,'rationale':'Evidence supports mixed assessment.','evidence_refs':[{'source_ref':'SRC-1','locator':'p.1'}]} for d in dims],'conditions':[],'blockers':['Gap'],'required_actions':['Close gap'],'counter_case':'Could improve if evidence closes.','evidence_sufficiency':'PARTIAL_REQUIRES_CONDITIONS'}
 base={'schema_version':'7.0.2','engagement_id':'ENG-RT','engagement_reset':{'status':'PASS'},'source_accountability':{'status':'PASS'},'output_config':{'language':'ar'},'canonical_role_order':roles,'step_evidence':{'FORGED':'PASS'},'ingestion_state':ing,'role_plan':[{'role_id':r,'applicability':'REQUIRED','depth':'STANDARD'} for r in roles],'role_outputs':{r:{'mandatory_content':['x'],'required_analysis':['x'],'evidence_refs':['SRC-1:p1'],'management_implication':'x'} for r in roles},'analytical_page_ids':['P08'],'critical_page_ids':['P08'],'cognitive_packets':{'P08':packet},'council_sessions':{'P08':{'status':'PASS','producer_actor_id':'P','judge_actor_id':'J','open_p0_p1':0}},'page_content_packs':{'P08':{'x':1}},'semantic_graphs':{'P08':{'nodes':['A','B'],'edges':[{'source':'A','relation':'ENABLES','target':'B'}]}},'visual_search':{'P08':{'hypotheses':hyp,'renders':renders,'initial_independent_judgments':[{'candidate_id':f'H{i}','independent':True,'judge_invocation_id':f'J{i}','previous_response_id':None,'actual_render_hash':renders[i-1]['actual_render_hash']} for i in range(1,6)],'refined_renders':refined,'final_independent_judgment':{'independent':True,'judge_invocation_id':'JF','winner_candidate_id':'M4','actual_render_hash':refined[3]['actual_render_hash']}}},'qa_results':{'P08':{'artifact_truth_score':95,'ceqs_score':95,'required_detector_status':'PASS'}},'deck_qa':{'stress':'PASS','repair_safety':'PASS','cross_deck':'PASS'},'decision':dec,'release':{'masters_frozen':True,'pdf_pptx_parity':'PASS','proof_index':'PASS','qa_status':'QA_CANDIDATE_PASS','release_chair_status':'RELEASED'}}
 # 1 forged full mode
 x=copy.deepcopy(base); x['ingestion_state']['missing_annexes']=[{'reference':'MISSING-MATERIAL','material':True,'source_refs':['SRC-1:p1']}]; x['ingestion_state']['source_pack_mode']='FULL_RFP_PACK'; attack('forged_full_pack_mode',x,'03')
 # 2 forged clarification status
 x=copy.deepcopy(base); x['ingestion_state']['clarification_window_state']['status']='CLOSED'; attack('forged_clarification_window',x,'03')
 # 3 producer judge same
 x=copy.deepcopy(base); x['council_sessions']['P08']['judge_actor_id']='P'; attack('producer_equals_judge',x,'07')
 # 4 duplicate render hashes
 x=copy.deepcopy(base); h=x['visual_search']['P08']['renders'][0]['actual_render_hash']; [r.__setitem__('actual_render_hash',h) for r in x['visual_search']['P08']['renders']]; attack('five_files_same_render_hash',x,'10')
 # 5 judge did not see actual render
 x=copy.deepcopy(base); x['visual_search']['P08']['initial_independent_judgments'][2]['actual_render_hash']='FAKE'; attack('judge_hash_mismatch',x,'11')
 # 6 hard-coded/forged winner without initial judges
 x=copy.deepcopy(base); x['visual_search']['P08']['winner']='H1'; x['visual_search']['P08']['initial_independent_judgments']=[]; attack('hardcoded_h1_without_judges',x,'11')
 # 7 invalid decision
 x=copy.deepcopy(base); x['decision']['counter_case']=''; attack('decision_without_counter_case',x,'14')
 # 8 QA attempts self release
 x=copy.deepcopy(base); x['release']['qa_status']='RELEASED'; attack('qa_self_release_attempt',x,'15')
 # 9 forged step evidence cannot bypass missing packet
 x=copy.deepcopy(base); x['cognitive_packets']={}; x['step_evidence']={str(i).zfill(2):{'status':'PASS'} for i in range(1,16)}; attack('forged_step_evidence_bypass',x,'06')

bad=[c for c in checks if c['status']=='BYPASS']; out={'suite':'RFP Summary Execution Red Team v7.0.2','status':'PASS' if not bad else 'FAIL','blocked':len(checks)-len(bad),'total':len(checks),'attacks':checks}
(Path(__file__).parent/'RFP_SUMMARY_EXECUTION_RED_TEAM_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
for c in checks: print(c['status'],c['attack'],c['result'].get('first_non_pass'))
print(f"SUMMARY {out['blocked']}/{out['total']} BLOCKED")
raise SystemExit(1 if bad else 0)
