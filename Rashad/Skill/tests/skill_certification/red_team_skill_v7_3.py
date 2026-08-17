#!/usr/bin/env python3
from pathlib import Path
import json,re,sys,copy
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[2]
att=[]
def record(name,blocked,evidence): att.append((name,bool(blocked),evidence))
def text(rel): return (ROOT/rel).read_text(encoding='utf-8')
def data(rel): return json.loads(text(rel))
# A startup/version split-brain attack
blob='\n'.join(text(x) for x in ['00_START_HERE.md','PROJECT_INSTRUCTIONS.md','00_CHAT_MIRROR_KERNEL/00_RASHAD_BOOTSTRAP.md','00_CHAT_MIRROR_KERNEL/24_VERSION_LAYER_RESOLUTION_AND_RETIREMENT_LEDGER.md'])
record('A01_stale_v622_current_route', 'use only the current v6.2.2' not in blob.lower() and 'unless explicitly exempted' not in blob.lower(), 'current startup mirrors')
# Candidate exemption
record('A02_critical_candidate_exemption', 'no page-family exemption may reduce either count' in text('01_ACTIVE_RUNTIME/65_V6_1_PAGE_EXECUTION_DOSSIER_CONTRACT.md').lower() and 'no critical analytical page-family exemption exists' in text('PROJECT_INSTRUCTIONS.md').lower(), 'dossier+project')
# RFP 24 drift/client derivative
fp=text('01_ACTIVE_RUNTIME/22_RFP_SUMMARY_FINAL_PRODUCT_CONTRACT.md')
record('A03_client_derivative_as_role24','## 24. Client-facing derivative' not in fp and '## 24. BID_DECISION — internal role contract' in fp,'final product contract')
# Role depth missing
rd=text('01_ACTIVE_RUNTIME/40_RFP_SUMMARY_24_ROLE_DEPTH_CONTRACTS.md')
record('A04_role_depth_missing_analysis_evidence',rd.count('**Required analysis:**')==24 and rd.count('**Evidence:**')==24,'24 role depth sections')
# Lens identity attack
lr=data('01_ACTIVE_RUNTIME/council_lens_registry_v7.json'); auth=set(lr['authorized_runtime_role_ids'])
record('A05_lens_invents_runtime_role',all(set(x['authorized_runtime_role_ids'])<=auth and x['lens_type']=='ANALYTICAL_LENS_NOT_RUNTIME_ID' for x in lr['lenses']),'lens registry')
# Cognitive schema attacks
schema=data('schemas/consulting_cognitive_packet_v7.schema.json'); v=Draft202012Validator(schema)
base={'page_id':'P24','role_id':'BID_DECISION','management_question':'Should management pursue this opportunity?','evaluator_question':'What conditions affect award confidence?','decision_supported':'Bid decision','answer_first_thesis':'Proceed only if named conditions are closed.','evidence_for':[{'claim':'Evidence exists','source_ref':'SRC-X','locator':'p.2','confidence':0.8}],'evidence_against':[],'assumptions':[{'statement':'Access assumed','impact':'schedule','validation_owner':'PM'}],'counterarguments':['Could be less attractive'],'relationships':[{'source':'A','relation':'DEPENDS_ON','target':'B'}],'executive_implication':'Management must close blockers before commitment.','council_route':[{'lens_id':'CEO_GM','authorized_runtime_role_ids':['ROLE-PARTNER','ROLE-DIRECTOR'],'challenge_question':'Would management take this risk?','independence_required':True},{'lens_id':'CFO','authorized_runtime_role_ids':['ROLE-COMMERCIAL','ROLE-PARTNER'],'challenge_question':'Is commercial exposure understood?','independence_required':True},{'lens_id':'RED_TEAM_CHALLENGER','authorized_runtime_role_ids':['ROLE-REDTEAM'],'challenge_question':'What would make the recommendation wrong?','independence_required':True}]}
for nm,mut in [('fake_role',('role_id','FAKE_ROLE')),('fake_relation',('relationships',[{'source':'A','relation':'MADE_UP_RELATION','target':'B'}])),('fake_lens',('council_route',[{'lens_id':'FAKE_LENS','authorized_runtime_role_ids':['ROLE-PARTNER'],'challenge_question':'This malicious fake lens should not validate.','independence_required':True}]*3))]:
 q=copy.deepcopy(base); q[mut[0]]=mut[1]; record('A06_'+nm,bool(list(v.iter_errors(q))),str([e.message for e in v.iter_errors(q)][:2]))
# Missing evidence locator
q=copy.deepcopy(base); del q['evidence_for'][0]['locator']; record('A07_missing_evidence_locator',bool(list(v.iter_errors(q))),'schema')
# QA fake pass / zero measurement: spec must define fail
qa=data('07_GOVERNANCE_AND_QA/73_V7_VISUAL_AND_EXECUTIVE_FAILURE_TAXONOMY.json')
zero=[c for c in qa['cases'] if c['minimum_measured_objects']<1 or (c['severity']=='BLOCKING' and c['not_instrumented_result']!='FAIL_NOT_INSTRUMENTED')]
record('A08_zero_measurement_pass',not zero,f'bad={len(zero)}')
# QA unspecified detector bypass
missing=[c['id'] for c in qa['cases'] if not all(c.get(k) for k in ['detector','measurement','threshold','applicability','stress_fixture','test_fixture','evidence_output'])]
record('A09_unspecified_qa_detector',not missing,f'missing={missing[:5]}')
# decision auto weighted formula / missing conditions
bd=data('schemas/rfp_bid_decision_evidence_v7.schema.json'); bv=Draft202012Validator(bd); dims=bd['properties']['dimensions']['items']['properties']['dimension']['enum']
d={'decision_id':'DEC-X01','recommendation':'GO_WITH_CONDITIONS','decision_method':'AUTO_WEIGHTED_SCORE','management_approval_required':True,'dimensions':[{'dimension':x,'assessment':'FAVORABLE','confidence':0.9,'rationale':'Evidence appears favorable for this decision dimension.','evidence_refs':[{'source_ref':'SRC-X','locator':'p.1'}]} for x in dims],'conditions':[],'blockers':[],'required_actions':['Approve'],'counter_case':'There is still a plausible counter-case.','evidence_sufficiency':'SUFFICIENT_FOR_RECOMMENDATION'}
record('A10_auto_formula_bid_decision',bool(list(bv.iter_errors(d))),str([e.message for e in bv.iter_errors(d)][:3]))
# workflow legacy reactivation
wf=text('05_WORKFLOW_ENGINE/02_RFP_SUMMARY.md')
record('A11_legacy_workflow17_reactivation','23_V7_RFP_SUMMARY_DECISION_WORKFLOW.md' in wf and 'executed through `17_A_TO_Z' not in wf,'workflow router')
# legacy 3-4 in current workflow
wf23=text('05_WORKFLOW_ENGINE/23_V7_RFP_SUMMARY_DECISION_WORKFLOW.md'); current_body=wf23.split('Legacy `17_A_TO_Z',1)[0]; record('A12_current_workflow_old_concept_count','3–4 concept' not in current_body and '3-4 concept' not in current_body and '3–5 concept' not in current_body and '3-5 concept' not in current_body and 'exactly 5' in current_body,'workflow23 current body')
# Artifact regression card fallback
art='\n'.join(text(x) for x in ['SKILL.md','00_CHAT_MIRROR_KERNEL/58_V7_GENERATIVE_EXHIBIT_AND_TOTAL_QUALITY_DIRECTOR.md','03_ARTIFACT_ENGINE/143_V7_GENERATIVE_EXHIBIT_SYNTHESIS_BRAIN.md'])
record('A13_artifact_template_card_regression','Cards are supporting surfaces only' in text('SKILL.md') and 'relationship-first' in art.lower(),'artifact authorities')
# Producer judge attack
record('A14_producer_self_certification','Producer-owned estimates have zero release authority' in text('SKILL.md') and 'Producer estimates have zero release authority' in text('07_GOVERNANCE_AND_QA/77_V7_RELEASE_COUNCIL_OF_COUNCILS.md'),'release governance')
# Language drift
lang=text('01_ACTIVE_RUNTIME/70_V7_MONOLINGUAL_OUTPUT_AND_NAMING_AUTHORITY.md')
record('A15_decorative_bilingualism','decorative bilingual' in lang.lower() and 'forbidden' in lang.lower(),'language authority')
# Criticality downgrade
crit=text('01_ACTIVE_RUNTIME/68_V6_2_2_PAGE_CRITICALITY_CLASSIFICATION_CONTRACT.md')
record('A16_producer_criticality_downgrade','producer' in crit.lower() and 'downgrad' in crit.lower(),'criticality authority')
# Prompt injection startup route
man=data('ACTIVE_AUTHORITY_MANIFEST.json')
record('A17_prompt_injection_not_mandatory','01_ACTIVE_RUNTIME/64_V6_DOCUMENT_INSTRUCTION_ISOLATION_AND_PROMPT_INJECTION_FIREWALL.md' in man['global_authorities'],'manifest')
# Version ledger in manifest
record('A18_version_ledger_not_bound','00_CHAT_MIRROR_KERNEL/24_VERSION_LAYER_RESOLUTION_AND_RETIREMENT_LEDGER.md' in man['global_authorities'],'manifest')
# Client derivative separate
record('A19_client_derivative_product_confusion','separate product' in fp.lower() and 'not a logical rfp summary role' in fp.lower(),'final product')
# Truthful QA runtime boundary
record('A20_specification_claimed_implemented','SPECIFIED_NOT_IMPLEMENTED' in text('07_GOVERNANCE_AND_QA/79_V7_QA_DETECTOR_IMPLEMENTATION_CONTRACT.md'),'qa boundary')
# v7.0.2 split-brain / status / visible-label attacks
bind=data('AUTHORITY_BINDING_CHECK.json')
cert=data('CERTIFICATION_REQUIREMENTS.json')
status=data('CURRENT_SKILL_STATUS.json')
manifest=data('ACTIVE_AUTHORITY_MANIFEST.json')
record('A21_binding_current_v71',bind.get('skill_version')=='7.3.0',str(bind.get('skill_version')))
record('A22_certification_stale_701',cert.get('version')=='7.3.0',str(cert.get('version')))
record('A23_current_workflow_stale_701',manifest.get('rfp_summary_current_workflow')=='05_WORKFLOW_ENGINE/23_V7_RFP_SUMMARY_DECISION_WORKFLOW.md',manifest.get('rfp_summary_current_workflow'))
record('A24_current_lens_stale_701',manifest.get('council_lens_registry')=='01_ACTIVE_RUNTIME/council_lens_registry_v7.json',manifest.get('council_lens_registry'))
record('A25_skill_status_misread_as_os',status.get('status_scope')=='SKILL_LAYER_ONLY_NOT_OS_LEVEL_STATUS_AUTHORITY',status.get('status_scope'))
record('A26_internal_contract_label_leak','Internal contract-label law' in fp and '## 24. BID_DECISION — internal role contract' in fp,'final product contract')
record('A27_role23_legacy_visible_title','ماذا تكشف طريقة إعداد المنافسة عن عملية الشراء؟' in fp,'role23 visible mapping')
router=data('01_ACTIVE_RUNTIME/council_of_councils_router_v7.json')
record('A28_router_stale_701',router.get('version') in {'7.0.2','7.1.0'},str(router.get('version')))
qat=data('07_GOVERNANCE_AND_QA/73_V7_VISUAL_AND_EXECUTIVE_FAILURE_TAXONOMY.json')
record('A29_qa_taxonomy_stale_701',qat.get('version') in {'7.0.2','7.1.0'},str(qat.get('version')))
current_blob='\n'.join(text(x) for x in ['SKILL.md','05_WORKFLOW_ENGINE/02_RFP_SUMMARY.md','00_CHAT_MIRROR_KERNEL/12_CONTEXT_ROUTER.md','00_CHAT_MIRROR_KERNEL/14_COMPILED_ALWAYS_ON_CONTEXT.md'])
record('A30_current_router_wording_stale_701','current v7.0.1 decision workflow' not in current_blob.lower() and 'router to v7.0.1' not in current_blob.lower(),'current startup/router files')

# v7.0.2 RFP Summary machine-execution attacks
arch=text('01_ACTIVE_RUNTIME/69_V7_RFP_SUMMARY_CANONICAL_DECISION_ARCHITECTURE.md')
wf23=text('05_WORKFLOW_ENGINE/23_V7_RFP_SUMMARY_DECISION_WORKFLOW.md')
record('A31_active_authority_stale_v701_workflow','23_V7_0_1_RFP_SUMMARY_DECISION_WORKFLOW' not in arch,'69 current architecture')
record('A32_active_authority_stale_v701_decision_schema','rfp_bid_decision_evidence_v7_0_1.schema.json' not in arch,'69 current architecture')
record('A33_machine_ingestion_state_missing',manifest.get('rfp_ingestion_state_schema')=='schemas/rfp_ingestion_state_v7.schema.json','manifest')
record('A34_machine_execution_state_missing',manifest.get('rfp_summary_execution_state_schema')=='schemas/rfp_summary_execution_state_v7.schema.json','manifest')
record('A35_rfp_summary_only_three_renders',manifest.get('rfp_summary_minimum_rendered_candidates_critical')==5 and 'Render **all 5**' in wf23,'manifest+workflow')
record('A36_rfp_summary_hardcoded_winner_path','No hard-coded H1 or positional winner is permitted' in wf23,'workflow')
record('A37_startup_stale_v701_rfp_workflow','23_V7_0_1_RFP_SUMMARY_DECISION_WORKFLOW' not in text('00_CHAT_MIRROR_KERNEL/14_COMPILED_ALWAYS_ON_CONTEXT.md'),'compiled always-on')

# Current authority-mirror stale-lineage routing attacks
auth_graph=text('00_CHAT_MIRROR_KERNEL/02_CURRENT_AUTHORITY_GRAPH.md')
product_registry=text('00_CHAT_MIRROR_KERNEL/03_PRODUCT_REGISTRY.md')
version_ledger=text('00_CHAT_MIRROR_KERNEL/24_VERSION_LAYER_RESOLUTION_AND_RETIREMENT_LEDGER.md')
record('A38_current_authority_graph_routes_current_v7_aliases',
       '23_V7_0_1_RFP_SUMMARY_DECISION_WORKFLOW' not in auth_graph and
       '73_V7_0_1_COUNCIL_LENS_AND_AUTHORIZED_ROLE_MAPPING' not in auth_graph and
       '74_V7_0_1_RFP_BID_DECISION_EVIDENCE_CONTRACT' not in auth_graph,
       '02 current authority graph')
record('A39_active_product_registry_routes_current_v7_aliases',
       '23_V7_0_1_RFP_SUMMARY_DECISION_WORKFLOW' not in product_registry and
       '74_V7_0_1_RFP_BID_DECISION_EVIDENCE_CONTRACT' not in product_registry,
       '03 active product registry')
record('A40_version_retirement_ledger_routes_current_v7_workflow',
       'Current RFP Summary workflow is `05_WORKFLOW_ENGINE/23_V7_RFP_SUMMARY_DECISION_WORKFLOW.md`' in version_ledger,
       '24 version retirement ledger')

# v7.1 user-visible artifact delivery attacks
wf71=text('05_WORKFLOW_ENGINE/24_V7_1_RFP_SUMMARY_ARTIFACT_DELIVERY_WORKFLOW.md')
law71=text('01_ACTIVE_RUNTIME/78_V7_1_ARTIFACT_INTELLIGENCE_BRAIN_EXECUTION_AND_USER_VISIBLE_DELIVERY_LAW.md')
qa71=text('07_GOVERNANCE_AND_QA/81_V7_1_ACTUAL_PIXEL_QA_CLOSED_LOOP_AND_GOLDEN_ACCEPTANCE.md')
record('A41_content_direct_to_pptx_forbidden','direct PPTX is forbidden' in wf71,'v7.1 workflow')
record('A42_concept_render_cannot_be_user_visible','Concept renders cannot be user-visible masters' in wf71,'v7.1 workflow')
record('A43_production_render_required','PRODUCTION_PAGE_RENDER' in wf71 and 'PRODUCTION_PAGE_RENDER' in law71,'v7.1 production render')
record('A44_partial_qa_cannot_be_user_visible','DRAFT_QA_PARTIAL' in wf71 and 'internal only' in wf71.lower(),'v7.1 QA')
record('A45_actual_pixel_qa_required','actual-pixel' in wf71.lower() and ('exact production-render hash' in qa71.lower() or 'exact production-render hash' in wf71.lower()),'pixel QA')
record('A46_repair_loop_required','Repair Brief' in wf71 and 're-render' in wf71,'repair loop')
record('A47_exact_file_delivery_gate','exact-file Delivery Dossier' in wf71 and 'Delivery Gate' in wf71,'delivery integrity')
record('A48_framework_qa_substitution_forbidden','framework qa cannot substitute' in wf71.lower(),'QA truthfulness')
record('A49_golden_real_rfp_required','Golden' in qa71 and 'RFP' in qa71,'golden acceptance')
record('A50_manifest_v71_current',manifest.get('version')=='7.3.0' and manifest.get('artifact_brain_version')=='4.0.0','manifest current')
record('A51_manifest_certification_harness_stale',manifest.get('certification_harness')=='tests/skill_certification/verify_skill_v7_3.py',str(manifest.get('certification_harness')))
record('A52_manifest_red_team_harness_stale','tests/skill_certification/red_team_skill_v7_3.py' in manifest.get('certification_harnesses',[]),str(manifest.get('certification_harnesses')))
record('A53_decision_and_artifact_workflow_conflation_blocked',manifest.get('rfp_summary_current_workflow')=='05_WORKFLOW_ENGINE/23_V7_RFP_SUMMARY_DECISION_WORKFLOW.md' and manifest.get('rfp_summary_artifact_delivery_workflow')=='05_WORKFLOW_ENGINE/24_V7_1_RFP_SUMMARY_ARTIFACT_DELIVERY_WORKFLOW.md',{'decision':manifest.get('rfp_summary_current_workflow'),'artifact':manifest.get('rfp_summary_artifact_delivery_workflow')})

# v7.2 Brain-coherence attacks
legacy=set(manifest.get('inherited_artifact_foundations',[]))
record('A54_legacy_artifact_foundation_reactivated_globally',not bool(legacy & set(manifest.get('global_authorities',[]))),str(sorted(legacy & set(manifest.get('global_authorities',[])))))
record('A55_brain_coherence_law_missing','01_ACTIVE_RUNTIME/79_V7_2_BRAIN_COHERENCE_AND_EXECUTABLE_EXPERT_LAW.md' in manifest.get('global_authorities',[]),'manifest')
record('A56_generic_cards_fallback_reenabled','HARD_FORBIDDEN' in str(manifest.get('generic_cards_fallback_policy','')),'manifest')
record('A57_old_v71_harness_reactivated',manifest.get('certification_harness')=='tests/skill_certification/verify_skill_v7_3.py' and 'tests/skill_certification/verify_skill_v7_1.py' not in manifest.get('certification_harnesses',[]),str(manifest.get('certification_harnesses')))
record('A58_expert_registry_without_runtime',manifest.get('brain_expert_runtime')=='../Brain/runtime/brain/expert_runtime.py' and manifest.get('brain_expert_routing_rules')=='../Brain/config/brain_expert_routing_rules.json','manifest')
record('A59_artifact_councils_metadata_only',manifest.get('artifact_council_runtime')=='../Brain/runtime/brain/artifact_council_runtime.py','manifest')
record('A60_brain_version_current',manifest.get('brain_runtime_version')=='3.5.0' and manifest.get('artifact_brain_version')=='4.0.0','manifest')
record('A61_no_execution_proof_can_render','No Council Execution Proof' in text('01_ACTIVE_RUNTIME/79_V7_2_BRAIN_COHERENCE_AND_EXECUTABLE_EXPERT_LAW.md'),'v7.2 law')
record('A62_ai_engineer_missing_from_brain','SME-AI-ENGINEERING' in (ROOT.parent/'Brain/config/actor_ontology.json').read_text(encoding='utf-8'),'actor ontology')
record('A63_equal_card_grid_not_forbidden','equal-card' in text('07_GOVERNANCE_AND_QA/82_V7_2_BRAIN_COHERENCE_AUDIT_AND_NO_GENERIC_FALLBACK.md').lower() or 'card-grid' in text('07_GOVERNANCE_AND_QA/82_V7_2_BRAIN_COHERENCE_AUDIT_AND_NO_GENERIC_FALLBACK.md').lower(),'v7.2 QA law')

# v7.2 Host-Native provider-mode attacks
record('A64_host_native_law_global','01_ACTIVE_RUNTIME/80_V7_2_HOST_NATIVE_EXECUTION_AND_PROVIDER_MODE_LAW.md' in manifest.get('global_authorities',[]),'manifest')
record('A65_host_native_qa_law_global','07_GOVERNANCE_AND_QA/83_V7_2_HOST_NATIVE_EXECUTION_TRACE_AND_PROVIDER_TRUTHFULNESS.md' in manifest.get('global_authorities',[]),'manifest')
record('A66_host_native_workflow_bound',manifest.get('rfp_summary_host_native_workflow')=='05_WORKFLOW_ENGINE/25_V7_2_HOST_NATIVE_RFP_SUMMARY_EXECUTION_WORKFLOW.md',manifest.get('rfp_summary_host_native_workflow'))
record('A67_three_execution_modes_exact',manifest.get('execution_modes')==['HOST_NATIVE_MODE','API_PROVIDER_MODE','OFFLINE_VALIDATION_MODE'],manifest.get('execution_modes'))
record('A68_host_native_provider_adapter_bound','HostNativeProvider' in manifest.get('rfp_summary_live_provider_adapter','') and 'HostNativeResponseBundleProvider' in manifest.get('rfp_summary_live_provider_adapter',''),manifest.get('rfp_summary_live_provider_adapter'))
record('A69_no_api_key_only_host_block','MODEL_CAPABLE_HOST_MUST_NOT_FALL_OFFLINE' in manifest.get('host_native_provider_policy',''),manifest.get('host_native_provider_policy'))

# v7.2.1 exact-handoff attacks
record('A70_exact_handoff_authority_removed','01_ACTIVE_RUNTIME/81_V7_2_1_EXACT_ARTIFACT_HANDOFF_LOCK.md' in manifest.get('global_authorities',[]),'manifest')
record('A71_delivered_file_binding_qa_removed','07_GOVERNANCE_AND_QA/84_V7_2_1_DELIVERED_FILE_BINDING_QA.md' in manifest.get('global_authorities',[]),'manifest')
record('A72_exact_handoff_runtime_unbound',manifest.get('exact_artifact_handoff_runtime')=='../Brain/runtime/brain/exact_handoff.py',manifest.get('exact_artifact_handoff_runtime'))
record('A73_wrong_artifact_incident_not_permanent',manifest.get('wrong_artifact_handoff_incident')=='I16_WRONG_ARTIFACT_HANDOFF_AFTER_QA',manifest.get('wrong_artifact_handoff_incident'))


# v7.3 visual-production/remediation bypass attacks
record('A74_v73_visual_law_removed','01_ACTIVE_RUNTIME/82_V7_3_VISUAL_PRODUCTION_ORGAN_AND_COMPOSITION_INTELLIGENCE_LAW.md' in manifest.get('global_authorities',[]),'manifest')
record('A75_v73_remediation_law_removed','07_GOVERNANCE_AND_QA/85_V7_3_COUNCIL_SUPERVISED_REMEDIATION_AND_ENGAGEMENT_ACCEPTANCE.md' in manifest.get('global_authorities',[]),'manifest')
record('A76_v73_composer_unbound',manifest.get('production_composer_runtime')=='../Brain/runtime/brain/production/composer.py',manifest.get('production_composer_runtime'))
record('A77_v73_pdf_inspector_unbound',manifest.get('format_neutral_product_inspector')=='../Brain/runtime/brain/product_geometry.py',manifest.get('format_neutral_product_inspector'))
record('A78_v73_image_path_unbound',manifest.get('imagery_director_runtime')=='../Brain/runtime/brain/imagery_director.py',manifest.get('imagery_director_runtime'))
record('A79_v73_quality_floor_deleted',manifest.get('quality_targets',{}).get('dominant_mass_min')==0.32 and manifest.get('quality_targets',{}).get('composition_distinct_ratio_min')==0.7,manifest.get('quality_targets'))
record('A80_fixture_can_certify_engagement','FIXTURE_CERTIFICATION_NEVER_SUBSTITUTES' in manifest.get('engagement_acceptance_rule',''),manifest.get('engagement_acceptance_rule'))
# summary
fails=[a for a in att if not a[1]]
for n,b,e in att: print(('BLOCKED' if b else 'BYPASS'),n,e)
print(f'SUMMARY {len(att)-len(fails)}/{len(att)} ATTACKS BLOCKED')
sys.exit(1 if fails else 0)
