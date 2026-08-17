#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import ast, hashlib, json, re, sys, tempfile
ROOT=Path(__file__).resolve().parents[2]; R=ROOT/'Rashad'; Q=ROOT/'QA'; S=R/'Skill'; B=R/'Brain'
sys.path.insert(0,str(B/'runtime')); sys.path.insert(0,str(Q/'Brain'))
from brain.expert_router import route_experts
from brain.expert_runtime import execute_expert_council
from brain.provider import ScriptedTestProvider, NoExecutionProvider
from brain.orchestrator import run_brain
from brain.artifact_brain import STRATEGIES, REGISTRY, generate_communication_hypotheses, route_artifact_councils
from brain.artifact_council_runtime import execute_artifact_councils
from brain.execution_proof import validate_brain_execution_proof, validate_artifact_execution_ledger
from artifact_delivery_orchestrator import promote_page_to_production
from brain.knowledge_readiness import detect_knowledge_needs
from brain.product_inspector import inspect_pptx
from orchestrator import route as qa_route
from pptx import Presentation
from pptx.util import Inches

LETTERS={c:[] for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}
def add(letter,name,ok,detail=None): LETTERS[letter].append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
def J(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def T(p): return Path(p).read_text(encoding='utf-8',errors='ignore')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    ver=J(R/'VERSION.json'); osst=J(R/'OS_STATUS.json'); bm=J(B/'BRAIN_MANIFEST.json'); am=J(S/'ACTIVE_AUTHORITY_MANIFEST.json'); cs=J(S/'CURRENT_SKILL_STATUS.json'); cr=J(S/'CERTIFICATION_REQUIREMENTS.json')
    actors=J(B/'config/actor_ontology.json'); rules=J(B/'config/brain_expert_routing_rules.json'); art=J(B/'config/artifact_brain_expert_universe_v3.json'); qcfg=J(Q/'Brain/councils.json')
    actor_ids={x['id'] for x in actors['actors']}; artifact_role_ids={x['id'] for x in art['roles']}; artifact_cids={x['id'] for x in art['councils']}
    # A — Authority
    add('A','canonical_skill_version_7_2',ver['canonical_skill_version']==osst['canonical_skill_version']==bm['bound_skill_version']==am['version']=='7.2.1',[ver['canonical_skill_version'],osst['canonical_skill_version'],bm['bound_skill_version'],am['version']])
    add('A','brain_version_3_4',ver['brain_runtime_version']==osst['brain_runtime_version']==bm['brain_version']==am['brain_runtime_version']=='3.4.0')
    add('A','global_authorities_exist',all((S/p).is_file() for p in am['global_authorities']))
    add('A','current_cert_harness_v72',am.get('certification_harness')=='tests/skill_certification/verify_skill_v7_2_1.py')
    # B — Brain
    add('B','brain_manifest_bound_to_v72',bm.get('bound_skill_version')=='7.2.1')
    add('B','brain_actor_count_69',len(actor_ids)==69,len(actor_ids))
    add('B','brain_actor_ids_unique',len(actor_ids)==len(actors['actors']))
    add('B','brain_layers_include_expert_execution',all(x in bm['layers'] for x in ['EXPERT_ROUTING','EXPERT_EXECUTION_LEDGER','COUNCIL_OF_COUNCILS','COGNITIVE_LOCK']))
    # C — Councils
    add('C','constitutional_council_count_16',bm.get('council_count')==16,bm.get('council_count'))
    add('C','artifact_council_count_20',len(artifact_cids)==20,len(artifact_cids))
    add('C','qa_council_count_14',len(qcfg.get('councils',[]))==14,len(qcfg.get('councils',[])))
    missing_art_roles=sorted({rid for c in art['councils'] for rid in c.get('roles',[]) if rid not in artifact_role_ids})
    add('C','artifact_council_roles_all_resolve',not missing_art_roles,missing_art_roles)
    # D — Data/evidence
    ph=J(S/'PROTECTED_CORPUS_HASHES.json'); bad=[rel for rel,h in ph['files'].items() if not (S/rel).exists() or sha(S/rel)!=h]
    add('D','protected_corpus_hash_exact',not bad,bad[:10])
    add('D','protected_counts_388_96_96',len(list((S/'02_IMMUTABLE_AUTHORITIES/RETRIEVAL/PROMPTS').glob('R-*.md')))==388 and len(list((S/'02_IMMUTABLE_AUTHORITIES/RETRIEVAL/SCOPES').glob('*.md')))==96 and len(list((S/'02_IMMUTABLE_AUTHORITIES/RETRIEVAL/MAPPINGS').glob('*.md')))==96)
    add('D','evidence_governor_registered','GOV-EVIDENCE' in actor_ids)
    add('D','claim_visual_binding_runtime',(B/'runtime/brain/artifact_gate.py').read_text().find('CLAIM_TO_VISUAL_EVIDENCE_BINDING_INCOMPLETE')>=0)
    # E — Experts executable/reachable
    refs=set(rules.get('core_roles',[]))|set(rules.get('mandatory_governors_for_critical',[]))
    for v in rules.get('role_rules',{}).values(): refs.update(v)
    for x in rules.get('domain_rules',[]): refs.update(x.get('roles',[]))
    add('E','all_registered_brain_actors_reachable',refs==actor_ids,{'unreachable':sorted(actor_ids-refs),'unknown':sorted(refs-actor_ids)})
    tech={'task_id':'A2Z-TECH','rfp_role':'TECHNICAL_REQUIREMENTS','critical':True,'rendered':True,'language':'AR','question':'AI platform architecture APIs data cybersecurity cloud backend frontend mobile UX presentation artifact'}
    rt=route_experts(tech); add('E','technical_route_pass',rt['status']=='PASS',rt)
    led=execute_expert_council(tech,{'answer_first_thesis':'Integrated architecture'},ScriptedTestProvider())
    add('E','expert_execution_ledger_pass',led['status']=='PASS',led.get('errors'))
    add('E','no_execution_provider_blocks',execute_expert_council(tech,{'answer_first_thesis':'x'},NoExecutionProvider())['status']=='BLOCKED')
    # F — Flow/state machines
    wf=(S/'05_WORKFLOW_ENGINE/02_RFP_SUMMARY.md').read_text(); w23=(S/'05_WORKFLOW_ENGINE/23_V7_RFP_SUMMARY_DECISION_WORKFLOW.md').read_text(); w24=(S/'05_WORKFLOW_ENGINE/24_V7_1_RFP_SUMMARY_ARTIFACT_DELIVERY_WORKFLOW.md').read_text()
    add('F','router_binds_decision_and_artifact_workflows','23_V7_RFP_SUMMARY_DECISION_WORKFLOW.md' in wf and '24_V7_1_RFP_SUMMARY_ARTIFACT_DELIVERY_WORKFLOW.md' in wf)
    add('F','decision_workflow_fail_closed','No downstream step may be claimed' in w23)
    add('F','artifact_workflow_forbids_content_direct_to_pptx','content → direct pptx' in w24.lower() and 'forbidden' in w24.lower())
    # G — Governors
    mandatory=set(rules.get('mandatory_governors_for_critical',[])); add('G','critical_governors_present',{'GOV-EVIDENCE','GOV-KNOWLEDGE-READINESS'}<=mandatory,sorted(mandatory))
    add('G','governors_have_veto_runtime','GOVERNOR_VETO' in (B/'runtime/brain/expert_runtime.py').read_text())
    add('G','release_governor_reachable','GOV-RELEASE' in refs)
    add('G','artifact_pipeline_governor_reachable','GOV-ARTIFACT-PIPELINE' in refs)
    # H — Hypotheses/visual cognition
    add('H','strategy_count_24',len(STRATEGIES)==24,len(STRATEGIES))
    add('H','strategy_registry_runtime_parity',set(art.get('communication_strategy_universe',[]))==set(STRATEGIES))
    graph={'nodes':[{'id':'A'},{'id':'B'}],'edges':[{'source':'A','target':'B','relation':'SUPPORTS'}]}; content={'thesis':'قرار الدخول يتطلب إثبات الجاهزية','numbers':[24,30,20],'decision':'HOLD','rfp':'منافسة'}
    hyp=generate_communication_hypotheses(graph,content,5)
    add('H','five_unique_strategies',hyp['status']=='PASS' and hyp['distinct_communication_strategies']==5,hyp)
    add('H','not_diagram_only',not hyp['diagram_only_search'])
    add('H','minimal_candidate_required',hyp['contains_minimal_hypothesis'])
    # XN — Execution mode / host-native coherence
    em=(B/'runtime/brain/execution_mode.py').read_text(); provtxt=(B/'runtime/brain/provider.py').read_text(); qalaw=(S/'07_GOVERNANCE_AND_QA/83_V7_2_HOST_NATIVE_EXECUTION_TRACE_AND_PROVIDER_TRUTHFULNESS.md').read_text()
    add('I','execution_modes_defined',all(x in em for x in ['HOST_NATIVE_MODE','API_PROVIDER_MODE','OFFLINE_VALIDATION_MODE']))
    add('I','host_native_provider_executable','class HostNativeProvider' in provtxt and 'class HostNativeResponseBundleProvider' in provtxt)
    add('I','host_native_proof_hash_bound','HOST_NATIVE_PROOF_INVALID' in provtxt and 'request_key' in provtxt and 'host_session_id' in provtxt)
    add('I','host_native_no_api_key_law','API key' in (S/'01_ACTIVE_RUNTIME/80_V7_2_HOST_NATIVE_EXECUTION_AND_PROVIDER_MODE_LAW.md').read_text() and 'HOST_NATIVE_MODE' in qalaw)
    # I — Independence
    prov=(B/'runtime/brain/provider.py').read_text(); rel=(B/'runtime/brain/release.py').read_text()
    add('I','provider_marks_independent_judges','INDEPENDENT_JUDGE' in prov and "base['independent']=True" in prov)
    add('I','release_requires_independent_judge','INDEPENDENT_JUDGE_MISSING' in rel)
    add('I','qa_ceiling_not_release',osst.get('qa_authority_ceiling')=='QA_CANDIDATE_PASS')
    # J — Judgment
    vs=(B/'runtime/brain/visual_search.py').read_text(); ag=(B/'runtime/brain/artifact_gate.py').read_text()
    add('J','no_h1_positional_winner',not re.search(r"winner\s*[:=]\s*['\"]H1",vs,re.I))
    add('J','provisional_master_blocked_user_visible','USER_VISIBLE_MASTER_CANNOT_USE_PROVISIONAL_OR_POSITIONAL_AUTHORITY' in ag)
    add('J','candidate_position_zero_authority',am.get('artifact_candidate_position_has_selection_authority') is False)
    # K — Knowledge readiness
    kr=detect_knowledge_needs({'question':'Give final fixed price and margin using rate card'})
    add('K','missing_rate_knowledge_blocks_final_price',kr['status']=='KNOWLEDGE_READINESS_BLOCK',kr)
    add('K','knowledge_readiness_governor_registered','GOV-KNOWLEDGE-READINESS' in actor_ids)
    add('K','expertise_not_equal_knowledge','EXPERTISE_AVAILABILITY_NE_KNOWLEDGE_READINESS'==kr.get('principle'))
    # L — Legacy quarantine
    inherited=set(am.get('inherited_artifact_foundations',[])); add('L','legacy_artifact_foundations_not_global',not (inherited & set(am['global_authorities'])),sorted(inherited & set(am['global_authorities'])))
    rex=J(S/'RETRIEVAL_EXCLUSION_REGISTRY.json'); add('L','retrieval_quarantine_v72',rex.get('version')=='7.2.1')
    add('L','provenance_runtime_quarantined',any(e.get('path')=='10_PROVENANCE/' for e in rex.get('entries',[])))
    current_v72_exec_files=[Q/'FINAL_VERIFY.py',Q/'Brain/run_v7_2_user_visible_delivery_certification.py',Q/'Brain/red_team_v7_2_delivery.py',Q/'Brain/golden_redf_acceptance_v7_2.py',Q/'Brain/incident_regression_v7_2.py',Q/'Brain/stress_quality_v7_2.py']
    stale_exec=[]
    for fp in current_v72_exec_files:
        tx=fp.read_text(encoding='utf-8',errors='ignore')
        if re.search(r'(?:from|import|Brain/)[^\n]*v7_1',tx,re.I) or re.search(r"['\"](?:red_team|stress_quality|golden_redf|incident_regression|run_v7_1)[^'\"]*v7_1",tx,re.I): stale_exec.append(str(fp.relative_to(ROOT)))
    add('L','current_v72_execution_has_no_v71_script_dependency',not stale_exec,stale_exec)
    # M — Meta cognition
    acroute=route_artifact_councils(graph,content,'AR','PRE_CONCEPT')
    add('M','artifact_meta_router_activated','META_EXPERTISE_ROUTER' in acroute.get('active_councils',[]),acroute)
    brain=run_brain({'task_id':'A2Z-BRAIN','rfp_role':'TECHNICAL_REQUIREMENTS','critical':True,'rendered':True,'question':tech['question'],'evidence':[{'id':'E1'}]},ScriptedTestProvider())
    add('M','brain_reaches_cognitive_lock',brain.get('state')=='COGNITIVE_LOCKED',brain.get('state'))
    add('M','brain_proof_recomputed',validate_brain_execution_proof(brain).get('status')=='PASS')
    # N — Naming/Arabic/RTL
    rr=J(S/'01_ACTIVE_RUNTIME/rfp_summary_role_registry_v7.json'); r16=[r for r in rr['roles'] if r['canonical_id']=='COMMERCIAL_EXPOSURE'][0]
    add('N','role16_owner_arabic_title',r16['visible_name']['ar']=='الالتزامات والمخاطر التجارية والمالية')
    add('N','arabic_artifact_council_routes','ARABIC_RTL_COUNCIL' in acroute.get('active_councils',[]))
    qr=qa_route({'rendered':True,'user_visible':True,'deck_level':True,'language':'AR'}); add('N','arabic_qa_routes','Q05_ARABIC_RTL_TYPOGRAPHY' in qr,qr)
    # O — Output classification
    add('O','artifact_draft_alias_user_visible',am.get('legacy_artifact_draft_alias')=='ARTIFACT_DRAFT_RESOLVES_TO_USER_VISIBLE_ARTIFACT_DRAFT')
    add('O','concept_render_internal_only','CONCEPT_RENDER_CANNOT_BE_USER_VISIBLE_MASTER' in ag)
    add('O','production_render_required','USER_VISIBLE_MASTER_MUST_BE_PRODUCTION_PAGE_RENDER' in ag)
    # P — Production
    def never(*a,**k): raise AssertionError('renderer must not run')
    badprom=promote_page_to_production({'status':'PASS'},never,never,{'material_claim_ids':['C1']},graph,tempfile.mkdtemp())
    add('P','production_without_brain_proof_blocks',badprom.get('status')=='BLOCKED',badprom)
    add('P','production_requires_art_direction','ART_DIRECTION_EXECUTION_REQUIRED' in ag)
    add('P','production_requires_readiness_council','PRODUCTION_COUNCIL_EXECUTION_REQUIRED' in ag)
    # Q — QA
    ao=(B/'runtime/brain/actual_output_qa.py').read_text(); qids={c['id'] for c in qcfg['councils']}
    add('Q','actual_pixel_qa_council','Q11_ACTUAL_PIXEL_PRODUCT_REVIEW' in qids)
    add('Q','simplicity_artifact_skeptic_qa','Q12_EXECUTIVE_SIMPLICITY_ARTIFACT_SKEPTIC' in qids)
    add('Q','delivery_repair_qa','Q13_DELIVERY_INTEGRITY_REPAIR_CLOSURE' in qids)
    add('Q','quality_floor_defined','MIN_DIMENSION_SCORE=80.0' in ao and 'MIN_MEAN_SCORE=85.0' in ao)
    # R — Repair/release
    add('R','repair_loop_user_visible_required','QA_REPAIR_LOOP_NOT_CLOSED' in ag)
    add('R','release_chair_only',ver.get('release_authority')=='RASHAD_BRAIN_RELEASE_CHAIR' and osst.get('production_release_authority')=='RASHAD_BRAIN_RELEASE_CHAIR')
    add('R','live_release_not_faked',str(osst.get('production_release_status','')).startswith('NOT_RELEASED'))
    # S — Stress/adversarial evidence
    stp=Q/'Certification/V7_2_BRAIN_COHERENCE_STRESS.json'; sta=J(stp) if stp.exists() else {}
    add('S','brain_coherence_stress_pass',sta.get('status')=='PASS',sta.get('counters'))
    add('S','stress_zero_errors',sta.get('error_count')==0,sta.get('error_count'))
    add('S','skill_redteam_current_declared',cr.get('current_red_team')=='tests/skill_certification/red_team_skill_v7_2_1.py')
    # T — Technical/AI
    ts=set(rt.get('selected_experts',[]))
    for rid in ['SME-AI-ENGINEERING','SME-SOLUTION-ARCH','SME-CYBER','SME-CLOUD-INFRA','GOV-TECHNICAL-FEASIBILITY']:
        add('T','technical_routes_'+rid,rid in ts,sorted(ts))
    # U — User-visible delivery
    dg=(B/'runtime/brain/delivery_gate.py').read_text()
    add('U','exact_file_delivery_gate','BLOCK_DELIVERY' in dg and 'sha256' in dg.lower())
    eh=T(B/'runtime/brain/exact_handoff.py'); add('U','exact_handoff_rebinds_delivered_bytes',all(x in eh for x in ['DELIVERED_PPTX_SHA_MISMATCH_DOSSIER','DELIVERED_SLIDE_COUNT_MISMATCH_DOSSIER_PAGES','PIXEL_REVIEW_COUNT_MISMATCH_DELIVERED_SLIDES','PRODUCTION_RENDER_COUNT_MISMATCH_DELIVERED_SLIDES']))
    add('U','handoff_certificate_required_authority','81_V7_2_1_EXACT_ARTIFACT_HANDOFF_LOCK.md' in T(S/'ACTIVE_AUTHORITY_MANIFEST.json'))
    add('U','framework_qa_substitution_forbidden',am.get('framework_qa_substitution')=='FORBIDDEN')
    add('U','user_visible_requires_pixel_pass','ACTUAL_PIXEL_QA_REQUIRED_FOR_USER_VISIBLE' in ag)
    # V — Versions/status
    add('V','skill_status_v72',cs.get('skill_version')=='7.2.1')
    add('V','cert_requirements_v72',cr.get('version')=='7.2.1')
    add('V','artifact_registry_v33',art.get('artifact_brain_version')=='3.3.0')
    add('V','brain_manifest_v34',bm.get('brain_version')=='3.4.0')
    current_docs={
      'Rashad/README.md':R/'README.md',
      'QA/README.md':Q/'README.md',
      'QA/Runtime/VERSION.md':Q/'Runtime/VERSION.md',
      'QA/Runtime/README.md':Q/'Runtime/README.md',
      'Rashad/Docs/HANDOFF.md':R/'Docs/HANDOFF.md',
      'Rashad/Skill/PROJECT_INSTRUCTIONS.md':S/'PROJECT_INSTRUCTIONS.md',
      'Rashad/Skill/00_START_HERE.md':S/'00_START_HERE.md'}
    stale_docs=[]
    for name,fp in current_docs.items():
        tx=fp.read_text(encoding='utf-8',errors='ignore')
        if ('v7.2' not in tx and '7.2.0' not in tx) or re.search(r'canonical[^\n]{0,80}v7\.1|bound skill:[^\n]*v7\.1|current v7\.1 startup route|Rashad OS v7\.1 \/ Brain v3\.2',tx,re.I): stale_docs.append(name)
    add('V','current_facing_docs_are_v72_not_stale_v71',not stale_docs,stale_docs)
    pending_current=[]
    for name,fp in {'Rashad/VERSION.json':R/'VERSION.json','Rashad/OS_STATUS.json':R/'OS_STATUS.json','Rashad/Skill/CURRENT_SKILL_STATUS.json':S/'CURRENT_SKILL_STATUS.json','QA/Certification/CURRENT_CERTIFICATION_INDEX.json':Q/'Certification/CURRENT_CERTIFICATION_INDEX.json'}.items():
        tx=fp.read_text(encoding='utf-8',errors='ignore')
        if re.search(r'PENDING_V7_2|FINAL_CERTIFICATION_PENDING',tx,re.I): pending_current.append(name)
    add('V','current_status_layer_has_no_pending_v72_finalization',not pending_current,pending_current)
    # W — Workflow product
    add('W','rfp_roles_24',len(rr['roles'])==24 and [x['sequence'] for x in rr['roles']]==list(range(1,25)))
    add('W','workflow_machine_state_schema',(S/'schemas/rfp_summary_execution_state_v7.schema.json').exists())
    add('W','decision_and_delivery_workflows_separate',am.get('rfp_summary_current_workflow')!=am.get('rfp_summary_artifact_delivery_workflow'))
    # X — Cross-layer parity
    add('X','strategy_count_field_24',art.get('communication_strategy_count')==24)
    add('X','artifact_registry_counts_match',art.get('registered_role_count')==len(art['roles']) and bm.get('artifact_brain_registered_role_count')==len(art['roles']))
    add('X','artifact_council_counts_match',bm.get('artifact_brain_council_count')==len(art['councils']))
    add('X','brain_actor_count_manifest_match',bm.get('executable_actor_count')==len(actor_ids))
    # Y — Yield/repeatability + source integrity
    py_bad=[]; json_bad=[]; line_count=0; file_count=0
    for p in ROOT.rglob('*'):
        if not p.is_file(): continue
        if '__pycache__' in p.parts: continue
        file_count+=1
        if p.suffix=='.py':
            try: ast.parse(p.read_text(encoding='utf-8',errors='strict'))
            except Exception as e: py_bad.append((str(p.relative_to(ROOT)),str(e)))
        if p.suffix=='.json':
            try: json.loads(p.read_text(encoding='utf-8',errors='strict'))
            except Exception as e: json_bad.append((str(p.relative_to(ROOT)),str(e)))
        if p.suffix.lower() in {'.md','.txt','.json','.py','.yaml','.yml','.csv'}:
            try: line_count+=len(p.read_text(encoding='utf-8',errors='ignore').splitlines())
            except Exception: pass
    add('Y','all_python_syntax_valid',not py_bad,py_bad[:10])
    add('Y','all_json_parse_valid',not json_bad,json_bad[:10])
    add('Y','no_pyc_or_pycache_in_final_worktree',not list(ROOT.rglob('*.pyc')) and not [d for d in ROOT.rglob('__pycache__') if d.is_dir()])
    fv=(Q/'FINAL_VERIFY.py').read_text(); add('Y','final_verifier_single_run_lock',all(x in fv for x in ['LOCK_FD=os.open(str(CERT), os.O_RDONLY)','fcntl.flock(LOCK_FD, fcntl.LOCK_EX | fcntl.LOCK_NB)','FINAL_VERIFY_ALREADY_RUNNING']) and '.final_verify.lock' not in fv)
    add('Y','line_scan_executed',line_count>100000,{'files':file_count,'text_lines':line_count})
    manifest_lines=(S/'MANIFEST.md').read_text(encoding='utf-8').splitlines(); manifest_map={}
    for ln in manifest_lines:
        mm=re.match(r'\| `([^`]+)` \| `([0-9a-f]{64})` \| ([0-9]+) \|',ln)
        if mm: manifest_map[mm.group(1)]=(mm.group(2),int(mm.group(3)))
    actual_skill={}
    for fp in S.rglob('*'):
        if fp.is_file() and fp.name!='MANIFEST.md' and '__pycache__' not in fp.parts and fp.suffix!='.pyc': actual_skill[fp.relative_to(S).as_posix()]=(sha(fp),fp.stat().st_size)
    add('Y','skill_manifest_v72_exact_all_current_bytes',(S/'MANIFEST.md').read_text(encoding='utf-8').startswith('# Rashad Proposal OS v7.2.1') and manifest_map==actual_skill,{'manifest':len(manifest_map),'actual':len(actual_skill),'missing':sorted(set(actual_skill)-set(manifest_map))[:5],'extra':sorted(set(manifest_map)-set(actual_skill))[:5]})
    # Z — Zero bypass / incident closure
    fake={'state':'COGNITIVE_LOCKED','coverage':{'status':'PASS'},'expert_execution_ledger':{'status':'PASS'}}
    fp=promote_page_to_production({'artifact_council_execution':{'status':'PASS'},'art_direction_execution':{'status':'PASS'}},never,never,{'material_claim_ids':[]},graph,tempfile.mkdtemp(),brain_session=fake,page_contract={'page_id':'P'},artifact_intent={'type':'X'},evidence_lineage=[{'evidence':'E1'}],brand_preflight={'status':'PASS','rubix_asset_status':'VERIFIED'})
    add('Z','fake_pass_without_invocations_blocked',fp.get('status')=='BLOCKED',fp)
    add('Z','generic_cards_hard_forbidden','HARD_FORBIDDEN' in am.get('generic_cards_fallback_policy',''))
    add('Z','no_council_execution_no_pptx_law','No Council Execution Proof' in (S/'01_ACTIVE_RUNTIME/79_V7_2_BRAIN_COHERENCE_AND_EXECUTABLE_EXPERT_LAW.md').read_text())
    add('Z','framework_qa_cannot_masquerade',am.get('framework_qa_substitution')=='FORBIDDEN')
    hc=J(Q/'Certification/HANDOFF_LOCK_CERTIFICATION_V7_2_1.json') if (Q/'Certification/HANDOFF_LOCK_CERTIFICATION_V7_2_1.json').exists() else {}
    i16=J(Q/'Certification/INCIDENT_P0_WRONG_ARTIFACT_HANDOFF_20260817_RESULTS.json') if (Q/'Certification/INCIDENT_P0_WRONG_ARTIFACT_HANDOFF_20260817_RESULTS.json').exists() else {}
    ir721=J(Q/'Certification/INCIDENT_REGRESSION_V7_2_1.json') if (Q/'Certification/INCIDENT_REGRESSION_V7_2_1.json').exists() else {}
    add('Z','exact_handoff_certification_pass',hc.get('status')=='PASS' and hc.get('passed')==hc.get('total')==9,hc.get('status'))
    add('Z','real_wrong_handoff_incident_replay_pass',i16.get('status')=='PASS',i16.get('status'))
    add('Z','v721_incident_registry_pass',ir721.get('status')=='PASS' and ir721.get('incident_count')==16,{'status':ir721.get('status'),'incidents':ir721.get('incident_count')})

    categories=[]; total=passed=0
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        cc=LETTERS[letter]; pp=sum(x['status']=='PASS' for x in cc); total+=len(cc); passed+=pp
        categories.append({'letter':letter,'status':'PASS' if pp==len(cc) else 'FAIL','passed':pp,'total':len(cc),'checks':cc})
    out={'suite':'Rashad v7.2.1 Final A-to-Z Brain/Architecture/Workflow/QA Audit','status':'PASS' if passed==total else 'FAIL','passed':passed,'total':total,'categories':categories}
    dest=Q/'Certification/V7_2_1_FINAL_A_TO_Z_AUDIT.json'; dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'suite':out['suite'],'status':out['status'],'passed':passed,'total':total,'categories':[{'letter':x['letter'],'status':x['status'],'passed':x['passed'],'total':x['total']} for x in categories],'failures':[{'letter':x['letter'],'checks':[c for c in x['checks'] if c['status']=='FAIL']} for x in categories if x['status']=='FAIL']},ensure_ascii=False,indent=2))
    return 0 if out['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
