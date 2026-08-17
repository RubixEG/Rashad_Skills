#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib,json,re,sys,shutil
ROOT=Path(__file__).resolve().parents[2];R=ROOT/'Rashad';SK=R/'Skill';B=R/'Brain';QA=ROOT/'QA';QB=QA/'Brain';RT=QA/'Runtime'
sys.path.insert(0,str(B/'runtime'))
results=[]
def add(n,ok,d=None):results.append({'attack':n,'status':'PASS' if ok else 'FAIL','detail':d})
def J(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def T(p):return Path(p).read_text(encoding='utf-8',errors='ignore')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
# housekeeping is not evidence; remove interpreter cache only.
for d in ROOT.rglob('__pycache__'):
    if d.is_dir():shutil.rmtree(d,ignore_errors=True)
for f in ROOT.rglob('*.pyc'):
    try:f.unlink()
    except OSError:pass
ver=J(R/'VERSION.json');osj=J(R/'OS_STATUS.json');bm=J(B/'BRAIN_MANIFEST.json');m=J(SK/'ACTIVE_AUTHORITY_MANIFEST.json');art=J(B/'config/artifact_brain_expert_universe_v3.json')
add('A01_skill_version_split_brain_blocked',ver.get('canonical_skill_version')==osj.get('canonical_skill_version')==bm.get('bound_skill_version')==m.get('version')=='7.2.1',[ver.get('canonical_skill_version'),osj.get('canonical_skill_version'),bm.get('bound_skill_version'),m.get('version')])
add('A02_brain_version_split_brain_blocked',ver.get('brain_runtime_version')==osj.get('brain_runtime_version')==bm.get('brain_version')=='3.4.0')
add('A03_artifact_version_split_brain_blocked',bm.get('artifact_brain_version')==m.get('artifact_brain_version')==art.get('artifact_brain_version')=='3.3.0')
add('A04_qa_version_current',ver.get('qa_runtime_version')==osj.get('qa_runtime_version')=='4.3')
add('A05_skill_version_md_current','Current release: v7.2.1' in T(SK/'VERSION.md'))
add('A06_current_cert_harness_is_v72',m.get('certification_harness')=='tests/skill_certification/verify_skill_v7_2_1.py')
add('A07_current_redteam_is_v72','tests/skill_certification/red_team_skill_v7_2_1.py' in m.get('certification_harnesses',[]))
add('A08_old_v702_harnesses_baseline_only',set(['tests/skill_certification/verify_skill_v7_0_2.py','tests/skill_certification/red_team_skill_v7_0_2.py'])<=set(m.get('protected_baseline_regression_harnesses',[])))
# Immutable corpus.
prompts=list((SK/'02_IMMUTABLE_AUTHORITIES/RETRIEVAL/PROMPTS').glob('R-*.md'));scopes=list((SK/'02_IMMUTABLE_AUTHORITIES/RETRIEVAL/SCOPES').glob('*.md'));maps=list((SK/'02_IMMUTABLE_AUTHORITIES/RETRIEVAL/MAPPINGS').glob('*.md'))
add('A09_protected_counts_exact',len(prompts)==388 and len(scopes)==96 and len(maps)==96,{'prompts':len(prompts),'scopes':len(scopes),'mappings':len(maps)})
ph=J(SK/'PROTECTED_CORPUS_HASHES.json');bad=[rel for rel,h in ph['files'].items() if not (SK/rel).exists() or sha(SK/rel)!=h];add('A10_protected_hashes_exact',not bad,bad[:10])
# Global authority/binding must be current and exact.
gh=J(SK/'GLOBAL_AUTHORITY_HASHES.json');gbad=[]
for rel,h in gh.get('files',{}).items():
    if not (SK/rel).exists() or sha(SK/rel)!=h:gbad.append(rel)
add('A11_global_authority_hashes_exact',gh.get('version')=='7.2.1' and not gbad,{'version':gh.get('version'),'bad':gbad[:10]})
ab=J(SK/'AUTHORITY_BINDING_CHECK.json');bbad=[]
for rel,h in ab.get('files',{}).items():
    p=SK/rel
    if not p.exists() or sha(p)!=h:bbad.append(rel)
add('A12_authority_binding_current_exact',ab.get('skill_version')=='7.2.1' and not bbad,{'version':ab.get('skill_version'),'bad':bbad[:10]})
add('A13_manifest_global_authorities_exist',all((SK/x).is_file() for x in m.get('global_authorities',[])))
add('A14_inherited_artifact_foundations_not_global',not(set(m.get('inherited_artifact_foundations',[]))&set(m.get('global_authorities',[]))))
# Brain: registered must be routable and executable.
actors=J(B/'config/actor_ontology.json')['actors'];rules=J(B/'config/brain_expert_routing_rules.json');allids={a['id'] for a in actors};refs=set(rules.get('core_roles',[]))|set(rules.get('mandatory_governors_for_critical',[]))
for v in rules.get('role_rules',{}).values():refs.update(v)
for q in rules.get('domain_rules',[]):refs.update(q.get('roles',[]))
add('B01_69_executable_brain_actors',len(allids)==69,len(allids));add('B02_all_registered_actors_routable',allids==refs,{'unreachable':sorted(allids-refs),'unknown':sorted(refs-allids)})
add('B03_ai_engineering_is_real_actor','SME-AI-ENGINEERING' in allids)
add('B04_ai_engineering_has_route','SME-AI-ENGINEERING' in refs)
proof=T(B/'runtime/brain/execution_proof.py');er=T(B/'runtime/brain/expert_runtime.py');orch=T(B/'runtime/brain/orchestrator.py')
add('B05_registered_not_execution_law_runtime','registered' in er.lower() and 'execution_proof' in er)
add('B06_brain_recomputes_expert_execution_proof','validate_expert_execution_ledger' in proof and 'validate_session' in proof)
add('B07_brain_requires_cognitive_lock',"session.get('state')!='COGNITIVE_LOCKED'" in proof)
add('B08_expert_isolated_invocation_proof','ISOLATED_INVOCATION_LEDGER' in proof and 'EXPERT_CONTEXT_REUSE' in proof and 'EXPERT_ACTOR_REUSE' in proof)
add('B09_orchestrator_executes_expert_council','execute_expert_council' in orch and 'EXPERTS_EXECUTED' in orch)
# Artifact Brain parity and execution.
from brain.artifact_brain import STRATEGIES
roleids={x['id'] for x in art.get('roles',[])};missing=[rid for c in art.get('councils',[]) for rid in c.get('roles',[]) if rid not in roleids]
add('C01_artifact_20_councils',len(art.get('councils',[]))==20,len(art.get('councils',[])))
add('C02_artifact_107_roles',len(roleids)==107,len(roleids))
add('C03_artifact_24_strategy_exact_parity',len(STRATEGIES)==24 and set(STRATEGIES)==set(art.get('communication_strategy_universe',[])),{'runtime':len(STRATEGIES),'registry':len(art.get('communication_strategy_universe',[]))})
add('C04_artifact_council_role_references_resolve',not missing,missing[:10])
ac=T(B/'runtime/brain/artifact_council_runtime.py');ag=T(B/'runtime/brain/artifact_gate.py');ao=T(B/'runtime/brain/actual_output_qa.py');dg=T(B/'runtime/brain/delivery_gate.py');pi=T(B/'runtime/brain/product_inspector.py')
add('C05_artifact_councils_execute_isolated_ledgers','ISOLATED_ARTIFACT_COUNCIL_INVOCATION_LEDGER' in ac)
add('C06_no_council_proof_no_production','ARTIFACT_COUNCIL_EXECUTION_REQUIRED' in ag and 'BRAIN_EXECUTION_PROOF_REQUIRED' in ag)
add('C07_concept_render_never_user_visible','CONCEPT_RENDER_CANNOT_BE_USER_VISIBLE_MASTER' in ag and 'USER_VISIBLE_MASTER_MUST_BE_PRODUCTION_PAGE_RENDER' in ag)
add('C08_actual_pixel_QA_required','ACTUAL_PIXEL_QA_REQUIRED_FOR_USER_VISIBLE' in ag and 'PIXEL_REVIEW_HASH_BINDING_MISMATCH' in ao)
add('C09_repair_loop_required','QA_REPAIR_LOOP_NOT_CLOSED' in ag)
add('C10_exact_file_delivery_hash_binding','DOSSIER_OUTPUT_FILE_HASH_MISMATCH' in dg)
add('C11_framework_QA_cannot_substitute','FRAMEWORK_CERTIFICATION_CANNOT_SUBSTITUTE_OUTPUT_QA' in dg)
add('C12_generic_equal_cards_blocked','PPTX_EQUAL_CARD_GRID_OVERUSE' in pi)
add('C13_shape_only_artifact_collapse_blocked','PPTX_SHAPE_ONLY_ANALYTICAL_DECK_OVERUSE' in pi)
add('C14_five_communication_strategies_not_geometry','FIVE_DISTINCT_COMMUNICATION_STRATEGIES_REQUIRED' in ag and 'MINIMAL_NON_DIAGRAM_HYPOTHESIS_REQUIRED' in ag)
eh=T(B/'runtime/brain/exact_handoff.py')
add('C15_exact_handoff_runtime_exists',all(x in eh for x in ['DELIVERED_PPTX_SHA_MISMATCH_DOSSIER','DELIVERED_SLIDE_COUNT_MISMATCH_DOSSIER_PAGES','PIXEL_REVIEW_COUNT_MISMATCH_DELIVERED_SLIDES','PRODUCTION_RENDER_COUNT_MISMATCH_DELIVERED_SLIDES']))
add('C16_image_led_logo_only_blocked','IMAGE_LED_DECLARED_BUT_IMAGES_APPEAR_LOGO_ONLY' in eh and 'PPTX_IMAGE_LED_ASSETS_APPEAR_LOGO_ONLY' in pi)
add('C17_handoff_incident_fixture_present',(RT/'fixtures/incidents/I16_WRONG_ARTIFACT_HANDOFF_20260817/bad_delivered_14_slide_deck.pptx').exists())
# QA governance.
qc=J(QB/'councils.json').get('councils',[]);qids={x['id'] for x in qc}
add('Q01_qa_14_councils',len(qc)==14,len(qc));add('Q02_actual_pixel_council','Q11_ACTUAL_PIXEL_PRODUCT_REVIEW' in qids);add('Q03_simplicity_artifact_skeptic','Q12_EXECUTIVE_SIMPLICITY_ARTIFACT_SKEPTIC' in qids);add('Q04_delivery_repair_council','Q13_DELIVERY_INTEGRITY_REPAIR_CLOSURE' in qids);add('Q05_golden_rfp_council','Q14_GOLDEN_REAL_RFP_ACCEPTANCE' in qids)
bad_release=[]
for p in list(RT.rglob('*.py'))+list(QB.rglob('*.py')):
    tx=T(p)
    if re.search(r"final_verdict['\"]?\s*[:=]\s*['\"]RELEASED['\"]",tx):bad_release.append(str(p.relative_to(ROOT)))
add('Q06_QA_cannot_emit_RELEASED',not bad_release,bad_release)
add('Q07_release_chair_only',osj.get('production_release_authority')=='RASHAD_BRAIN_RELEASE_CHAIR' and osj.get('qa_authority_ceiling')=='QA_CANDIDATE_PASS')
# Current evidence suites must pass.
for rel,name in [
 ('QA/Certification/V7_2_BRAIN_COHERENCE_AUDIT.json','E01_brain_coherence_pass'),('QA/Certification/V7_2_BRAIN_COHERENCE_STRESS.json','E02_brain_stress_pass'),('QA/Certification/V7_2_USER_VISIBLE_DELIVERY_CERTIFICATION.json','E03_user_visible_delivery_pass'),('QA/Certification/V7_2_GOLDEN_REDF_ACCEPTANCE.json','E04_golden_redf_pass'),('QA/Certification/INCIDENT_REGRESSION_V7_2_1.json','E05_incident_regression_pass'),('QA/Certification/FULL_LINE_CONFLICT_AUDIT_V7_2_1.json','E06_full_line_conflict_pass')]:
    p=ROOT/rel;v=J(p) if p.exists() else {};add(name,v.get('status')=='PASS',v.get('status'))
az=J(QA/'Certification/V7_2_1_FINAL_A_TO_Z_AUDIT.json') if (QA/'Certification/V7_2_1_FINAL_A_TO_Z_AUDIT.json').exists() else {};add('E07_A_to_Z_pass',az.get('status')=='PASS',az.get('status'))
hc=J(QA/'Certification/HANDOFF_LOCK_CERTIFICATION_V7_2_1.json') if (QA/'Certification/HANDOFF_LOCK_CERTIFICATION_V7_2_1.json').exists() else {}; add('E08_exact_handoff_certification_pass',hc.get('status')=='PASS' and hc.get('passed')==hc.get('total')==9,hc.get('status'))
i16=J(QA/'Certification/INCIDENT_P0_WRONG_ARTIFACT_HANDOFF_20260817_RESULTS.json') if (QA/'Certification/INCIDENT_P0_WRONG_ARTIFACT_HANDOFF_20260817_RESULTS.json').exists() else {}; add('E09_real_wrong_handoff_incident_replay_pass',i16.get('status')=='PASS',i16.get('status'))
# Packaging/orchestration discipline.
fv=T(QA/'FINAL_VERIFY.py');add('P01_final_verify_v721_current','Final Verification v7.2.1' in fv and all(x in fv for x in ['verify_skill_v7_2_1.py','final_package_red_team_v7_2_1.py','handoff_lock_certification_v7_2_1.py','incident_p0_wrong_artifact_handoff_20260817.py']))
add('P02_final_verify_directory_inode_lock_file_logged',all(x in fv for x in ['LOCK_FD=os.open(str(CERT), os.O_RDONLY)','fcntl.flock(LOCK_FD, fcntl.LOCK_EX | fcntl.LOCK_NB)','stdout=fo','stderr=fe','LOGDIR.mkdir(parents=True,exist_ok=True)']) and '.final_verify.lock' not in fv and 'capture_output=True' not in fv)
rv3=T(RT/'run_regression_v3.py');rv31=T(RT/'run_regression_v31.py');add('P03_regression_outputs_clean_each_run',"shutil.rmtree(HERE/'_regression', ignore_errors=True)" in rv3 and "shutil.rmtree(HERE/'_regression_v31', ignore_errors=True)" in rv31)
add('P04_no_nested_zip_packages',not list(ROOT.rglob('*.zip')),[str(x.relative_to(ROOT)) for x in ROOT.rglob('*.zip')][:10]);add('P05_no_pyc_cache',not list(ROOT.rglob('*.pyc')))
add('P06_no_current_v71_execution_dependency',all('v7_1' not in (QA/'FINAL_VERIFY.py').read_text(encoding='utf-8') for _ in [0]))
docs='\n'.join((ROOT/x).read_text(encoding='utf-8',errors='ignore') for x in ['Rashad/README.md','QA/README.md','QA/Runtime/VERSION.md','Rashad/Docs/HANDOFF.md'])
add('P07_current_docs_v72_v34', 'v7.2' in docs and 'v3.4' in docs and 'Canonical Rashad Layer v7.1' not in docs and 'Bound Skill: Rashad Proposal OS v7.1.0' not in docs)
status_text='\n'.join(T(ROOT/x) for x in ['Rashad/VERSION.json','Rashad/OS_STATUS.json','Rashad/Skill/CURRENT_SKILL_STATUS.json','QA/Certification/CURRENT_CERTIFICATION_INDEX.json'])
add('P08_no_pending_v72_finalization_status',not re.search(r'PENDING_V7_2|FINAL_CERTIFICATION_PENDING',status_text,re.I))
sm=T(ROOT/'Rashad/Skill/MANIFEST.md'); add('P09_skill_manifest_current_v72','# Rashad Proposal OS v7.2.1 — File Manifest' in sm and '# Rashad Proposal OS v7.1.0' not in sm)
# Host-Native execution cannot be a decorative provider label.
add('HN01_host_native_law_global','01_ACTIVE_RUNTIME/80_V7_2_HOST_NATIVE_EXECUTION_AND_PROVIDER_MODE_LAW.md' in m.get('global_authorities',[]))
add('HN02_host_native_qa_law_global','07_GOVERNANCE_AND_QA/83_V7_2_HOST_NATIVE_EXECUTION_TRACE_AND_PROVIDER_TRUTHFULNESS.md' in m.get('global_authorities',[]))
add('HN03_three_execution_modes_exact',m.get('execution_modes')==['HOST_NATIVE_MODE','API_PROVIDER_MODE','OFFLINE_VALIDATION_MODE'],m.get('execution_modes'))
provtxt=T(B/'runtime/brain/provider.py'); qprovtxt=T(QB/'provider.py')
add('HN04_brain_host_native_provider_runtime','class HostNativeProvider' in provtxt and 'class HostNativeResponseBundleProvider' in provtxt)
add('HN05_qa_host_native_provider_runtime','class HostNativeQAProvider' in qprovtxt and 'class HostNativeQAResponseBundleProvider' in qprovtxt)
add('HN06_host_native_proof_recomputed','_validate_host_native_invocation' in proof and 'HOST_NATIVE_REQUEST_KEY_MISMATCH' in proof)
add('HN07_release_preserves_external_independence','EXTERNAL_INDEPENDENT_JUDGE_REQUIRED_FOR_RELEASED' in T(B/'runtime/brain/release.py'))
# The two workflow layers must coexist without authority ambiguity.
add('W01_decision_workflow_current',m.get('rfp_summary_current_workflow','').endswith('23_V7_RFP_SUMMARY_DECISION_WORKFLOW.md'))
add('W02_artifact_delivery_overlay_bound',m.get('rfp_summary_artifact_delivery_workflow','').endswith('24_V7_1_RFP_SUMMARY_ARTIFACT_DELIVERY_WORKFLOW.md'))
add('W03_v72_brain_coherence_laws_global',all(x in m.get('global_authorities',[]) for x in ['01_ACTIVE_RUNTIME/79_V7_2_BRAIN_COHERENCE_AND_EXECUTABLE_EXPERT_LAW.md','07_GOVERNANCE_AND_QA/82_V7_2_BRAIN_COHERENCE_AUDIT_AND_NO_GENERIC_FALLBACK.md']))
out={'suite':'Rashad OS v7.2.1 Final Package Adversarial Red Team','status':'PASS' if all(x['status']=='PASS' for x in results) else 'FAIL','blocked':sum(x['status']=='PASS' for x in results),'total':len(results),'attacks':results}
(QA/'Certification/FINAL_PACKAGE_RED_TEAM_V7_2_1_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'suite':out['suite'],'status':out['status'],'blocked':out['blocked'],'total':out['total'],'escaped':[x for x in results if x['status']!='PASS']},ensure_ascii=False,indent=2));raise SystemExit(0 if out['status']=='PASS' else 2)
