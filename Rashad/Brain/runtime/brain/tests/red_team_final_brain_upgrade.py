#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve(); RUNTIME=HERE.parents[2]; sys.path.insert(0,str(RUNTIME))
from brain.artifact_gate import guard_composer,validate_artifact_draft,derive_output_classification
from brain.knowledge_readiness import detect_knowledge_needs
from brain.ontology import apply_governor_veto
from brain.confidence import propagate_confidence
from brain.visual_memory import variety_check

attacks=[]
def a(name,blocked,detail=None): attacks.append({'attack':name,'status':'BLOCKED' if blocked else 'ESCAPED','detail':detail})
def base():
    strategies=['STATEMENT_LED','NUMBER_LED','EVIDENCE_LED','COMPARISON_LED','SYSTEM_LED']; families=['MINIMAL','MINIMAL','ANALYTICAL','ANALYTICAL','RELATIONAL']; return {'content_status':'PASS','evidence_status':'PASS','page_contract':{'x':1},'cognitive_packet':{'x':1},'artifact_intent':{'x':1},'semantic_graph':{'x':1},'hypotheses':[{'communication_strategy':strategies[i],'strategy_family':families[i],'structural_signature':f'{strategies[i]}|{i}'} for i in range(5)],'render_evidence':[{'actual_render_hash':f'h{i}'} for i in range(5)],'selected_master':{'actual_render_hash':'h0','selection_authority':'PROVISIONAL_PARTNER_HEURISTIC_NOT_INDEPENDENT','selection_reason':'fit then simplicity'},'brand_preflight':{'status':'PASS','rubix_asset_status':'VERIFIED'},'qa_state':{'status':'DRAFT_QA_PASS','qa_scope':'ACTUAL_RENDERED_OUTPUT','actual_output_qa_status':'DRAFT_QA_PARTIAL','actual_pixel_visual_quality_status':'NOT_EXECUTED'},'material_claim_ids':['C1'],'claim_visual_bindings':[{'claim_id':'C1','evidence_refs':['E1'],'visual_node_ids':['N1']}], 'independent_judgment':{'status':'NOT_EXECUTED'},'parity_status':'NOT_EXECUTED','proof_index_status':'NOT_EXECUTED','release':{}}
# 1 direct composer bypass
r=guard_composer({'content_status':'PASS','evidence_status':'PASS'},'ARTIFACT_DRAFT'); a('DIRECT_COMPOSER_BYPASS',r['status']=='BLOCK_RENDER',r)
# 2 fake five renders same hash
s=base(); s['render_evidence']=[{'actual_render_hash':'same'} for _ in range(5)]; a('FIVE_RENDER_HASH_FORGERY',validate_artifact_draft(s)['status']=='BLOCKED',validate_artifact_draft(s))
# 3 cosmetic hypothesis duplicates
s=base(); s['hypotheses']=[{'structural_signature':'same'} for _ in range(5)]; a('COSMETIC_HYPOTHESIS_DUPLICATION',validate_artifact_draft(s)['status']=='BLOCKED',validate_artifact_draft(s))
# 4 missing claim binding
s=base(); s['claim_visual_bindings']=[]; a('CLAIM_WITHOUT_VISUAL_EVIDENCE_BINDING',validate_artifact_draft(s)['status']=='BLOCKED',validate_artifact_draft(s))
# 5 missing verified Rubix asset
s=base(); s['brand_preflight']['rubix_asset_status']='MISSING'; a('BRAND_PREFLIGHT_BYPASS',validate_artifact_draft(s)['status']=='BLOCKED',validate_artifact_draft(s))
# 6 self-assert released
s=base(); s['release']={'release_chair_status':'RELEASED','release_authority':'FAKE'}; a('UNAUTHORIZED_RELEASE_CHAIR',derive_output_classification(s)!='RELEASED',derive_output_classification(s))
# 7 price hallucination with missing rates
kr=detect_knowledge_needs({'question':'Give final price and margin now'}); a('INVENTED_PRICE_WITHOUT_RATE_PACK',kr['status']=='KNOWLEDGE_READINESS_BLOCK',kr)
# 8 expertise name used as fake knowledge
sap=detect_knowledge_needs({'question':'SAP integration'}); a('SME_NAME_IMPERSONATES_KNOWLEDGE',any(x['sme']=='SME-SAP' and x['knowledge_status']=='KNOWLEDGE_REQUIRED' for x in sap['routed_expertise']),sap)
# 9 governor override attempt
v=apply_governor_veto(['COMPOSER_BYPASS']); a('GOVERNOR_VETO_OVERRIDE',v['status']=='BLOCKED' and v['override_allowed'] is False,v)
# 10 confidence inflation
cp=propagate_confidence({'EFFORT':{'confidence':.4},'COST':{'confidence':.95,'depends_on':['EFFORT']},'MARGIN':{'confidence':.99,'depends_on':['COST']}}); a('DOWNSTREAM_CONFIDENCE_INFLATION',cp['MARGIN']['effective_confidence']<=.4,cp)
# 11 repeated visual grammar
cur={'dominant_form':'RING','reading_path':'RTL','focal_point':'RIGHT','topology':'LOOP','structural_signature':'A'}; a('DECK_TEMPLATE_TWIN',variety_check(cur,[cur])['status']=='BLOCKED',variety_check(cur,[cur]))
# 12 artifact draft incorrectly requires live judge (attack is blocked if draft remains admissible without independent)
s=base(); a('LIVE_JUDGE_ABSENCE_CANNOT_AUTHORIZE_USER_VISIBLE_DRAFT',guard_composer(s,'USER_VISIBLE_ARTIFACT_DRAFT')['status']=='BLOCK_RENDER',guard_composer(s,'USER_VISIBLE_ARTIFACT_DRAFT'))
# 13 release candidate without parity/proof
s=base(); s['independent_judgment']={'status':'PASS','independent':True}; s['qa_state']={'status':'QA_CANDIDATE_PASS','qa_scope':'ACTUAL_RENDERED_OUTPUT','actual_output_qa_status':'PASS','actual_pixel_visual_quality_status':'PASS'}; a('RELEASE_CANDIDATE_WITHOUT_PARITY_PROOF',guard_composer(s,'RELEASE_CANDIDATE')['status']=='BLOCK_RENDER',guard_composer(s,'RELEASE_CANDIDATE'))
# 14 fake QA status only
s=base(); s['qa_state']={'status':'QA_CANDIDATE_PASS','qa_scope':'ACTUAL_RENDERED_OUTPUT','actual_output_qa_status':'PASS','actual_pixel_visual_quality_status':'PASS'}; a('QA_PASS_ALONE_CANNOT_ESCALATE_RELEASE',derive_output_classification(s) not in {'RELEASE_CANDIDATE','RELEASED'},derive_output_classification(s))
out={'suite':'Rashad Final Brain Upgrade Red Team','status':'PASS' if all(x['status']=='BLOCKED' for x in attacks) else 'FAIL','blocked':sum(x['status']=='BLOCKED' for x in attacks),'total':len(attacks),'attacks':attacks}
Path(__file__).with_name('FINAL_BRAIN_UPGRADE_RED_TEAM_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 1)
