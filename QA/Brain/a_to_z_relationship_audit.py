#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib, json, re, sys
ROOT=Path(__file__).resolve().parents[2]; R=ROOT/'Rashad'; Q=ROOT/'QA'; S=R/'Skill'; B=R/'Brain'
sys.path.insert(0,str(B/'runtime'))
from brain.artifact_brain import REGISTRY, STRATEGIES
checks=[]
def add(name,ok,detail=None): checks.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
def j(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

ver=j(R/'VERSION.json'); osst=j(R/'OS_STATUS.json'); bm=j(B/'BRAIN_MANIFEST.json'); am=j(S/'ACTIVE_AUTHORITY_MANIFEST.json'); qs=j(Q/'Brain/councils.json')
add('top_level_exactly_Rashad_QA',{p.name for p in ROOT.iterdir() if p.is_dir()}=={'Rashad','QA'})
add('canonical_skill_version_consistent',ver['canonical_skill_version']==osst['canonical_skill_version']==bm['bound_skill_version']==am['version']=='7.1.0',[ver['canonical_skill_version'],osst['canonical_skill_version'],bm['bound_skill_version'],am['version']])
add('brain_runtime_version_consistent',ver['brain_runtime_version']==osst['brain_runtime_version']==bm['brain_version']=='3.2.0',[ver['brain_runtime_version'],osst['brain_runtime_version'],bm['brain_version']])
add('artifact_brain_version_consistent',bm['artifact_brain_version']==am['artifact_brain_version']==REGISTRY['artifact_brain_version']=='3.2.0',[bm['artifact_brain_version'],am['artifact_brain_version'],REGISTRY['artifact_brain_version']])
add('qa_brain_version_consistent',ver['qa_brain_version']==osst['qa_brain_version']==bm['qa_brain_version']==qs['qa_brain_version']=='1.2.0',[ver['qa_brain_version'],osst['qa_brain_version'],bm['qa_brain_version'],qs['qa_brain_version']])
add('qa_runtime_version_consistent',ver['qa_runtime_version']==osst['qa_runtime_version']==bm['qa_runtime_version']=='4.3')

# Active authorities exist.
missing=[x for x in am.get('global_authorities',[]) if not (S/x).exists()]
add('all_global_authority_paths_exist',not missing,missing)
add('artifact_brain_constitution_active',am.get('artifact_brain_constitution') in am.get('global_authorities',[]),am.get('artifact_brain_constitution'))

# Current authority mirrors must not route to version-numbered v7.0.1 compatibility files.
auth_graph=(S/'00_CHAT_MIRROR_KERNEL/02_CURRENT_AUTHORITY_GRAPH.md').read_text(encoding='utf-8')
product_registry=(S/'00_CHAT_MIRROR_KERNEL/03_PRODUCT_REGISTRY.md').read_text(encoding='utf-8')
version_ledger=(S/'00_CHAT_MIRROR_KERNEL/24_VERSION_LAYER_RESOLUTION_AND_RETIREMENT_LEDGER.md').read_text(encoding='utf-8')
add('current_authority_graph_uses_v7_aliases', all(x not in auth_graph for x in ['23_V7_0_1_RFP_SUMMARY_DECISION_WORKFLOW','73_V7_0_1_COUNCIL_LENS_AND_AUTHORIZED_ROLE_MAPPING','74_V7_0_1_RFP_BID_DECISION_EVIDENCE_CONTRACT']), None)
add('active_product_registry_uses_v7_aliases', all(x not in product_registry for x in ['23_V7_0_1_RFP_SUMMARY_DECISION_WORKFLOW','74_V7_0_1_RFP_BID_DECISION_EVIDENCE_CONTRACT']), None)
add('version_retirement_ledger_uses_v7_workflow_alias','Current RFP Summary workflow is `05_WORKFLOW_ENGINE/23_V7_RFP_SUMMARY_DECISION_WORKFLOW.md`' in version_ledger, None)

# Protected corpus exact.
ph=j(S/'PROTECTED_CORPUS_HASHES.json'); bad=[]
for rel,expected in ph['files'].items():
    p=S/rel
    if not p.exists() or sha(p)!=expected: bad.append(rel)
add('protected_corpus_hashes_exact',not bad,bad[:10])
add('protected_prompt_count_388',len(list((S/'02_IMMUTABLE_AUTHORITIES/RETRIEVAL/PROMPTS').glob('R-*.md')))==388)
add('protected_scope_count_96',len(list((S/'02_IMMUTABLE_AUTHORITIES/RETRIEVAL/SCOPES').glob('*.md')))==96)
add('protected_mapping_count_96',len(list((S/'02_IMMUTABLE_AUTHORITIES/RETRIEVAL/MAPPINGS').glob('*.md')))==96)

# Artifact Brain ontology integrity.
councils=REGISTRY['councils']; roles=REGISTRY['roles']; cids=[c['id'] for c in councils]; rids=[r['id'] for r in roles]
add('artifact_brain_20_councils',len(councils)==20,len(councils))
add('artifact_expert_universe_at_least_100_roles',len(roles)>=100,len(roles))
add('artifact_council_ids_unique',len(cids)==len(set(cids)))
add('artifact_role_ids_unique',len(rids)==len(set(rids)))
missing_roles=sorted({rid for c in councils for rid in c.get('roles',[]) if rid not in set(rids)})
add('all_council_role_references_resolve',not missing_roles,missing_roles)
bad_home=[r['id'] for r in roles if r.get('home_council') and r.get('home_council') not in set(cids)]
add('all_role_home_councils_resolve',not bad_home,bad_home)
add('bounded_runtime_activation',REGISTRY['runtime_activation_policy']['max_active_councils_per_page']<=12 and REGISTRY['runtime_activation_policy']['max_active_roles_per_page']<=18,REGISTRY['runtime_activation_policy'])

# Communication strategy integrity.
add('communication_strategy_count_24',len(STRATEGIES)==24,sorted(STRATEGIES))
registry_strategies=set(REGISTRY.get('communication_strategy_universe',[]))
add('expert_universe_strategy_count_24',len(registry_strategies)==24,sorted(registry_strategies))
add('expert_universe_matches_runtime_strategies',registry_strategies==set(STRATEGIES),{'missing_from_registry':sorted(set(STRATEGIES)-registry_strategies),'extra_in_registry':sorted(registry_strategies-set(STRATEGIES))})
add('geometry_primitives_not_communication_strategies',not ({'RING','HUB','SPINE','STACK','LANE'} & set(STRATEGIES)),sorted(STRATEGIES))
constitution=(S/am['artifact_brain_constitution']).read_text(encoding='utf-8')
missing_strategy=[x for x in STRATEGIES if x not in constitution]
add('constitution_covers_runtime_strategies',not missing_strategy,missing_strategy)
add('artifact_not_diagram_law_present','An artifact is not a diagram.' in constitution)
add('simplest_valid_form_law_present','The simplest valid form must win' in constitution)

# Runtime wiring.
for key in ['rfp_summary_execution_runtime','deterministic_search_renderer','presentation_output_guard','artifact_gate','knowledge_readiness','knowledge_registry','actor_ontology','firm_model','reasoning_pipelines','artifact_expert_universe','artifact_brain_runtime','actual_output_qa_runtime','artifact_brain_stress_quality']:
    rel=bm.get(key); p=(B/rel) if rel else None; add('brain_manifest_path_'+key,bool(rel and p.exists()),rel)
vs=(B/'runtime/brain/visual_search.py').read_text(encoding='utf-8'); ao=(B/'runtime/brain/actual_output_qa.py').read_text(encoding='utf-8'); guard=(B/'runtime/production_output_guard.py').read_text(encoding='utf-8'); gate=(B/'runtime/brain/artifact_gate.py').read_text(encoding='utf-8')
add('visual_search_uses_communication_strategy_brain','generate_communication_hypotheses' in vs)
add('visual_search_has_no_hardcoded_H1_winner',not re.search(r"winner\s*['\"]?\s*[:=]\s*['\"]H1['\"]",vs))
add('actual_output_qa_has_diagram_overuse_block','DECK_DIAGRAM_OVERUSE' in ao)
add('actual_output_qa_has_position_bias_block','POSITIONAL_HYPOTHESIS_WINNER_BIAS' in ao)
add('actual_output_qa_requires_actual_pixel_review','ACTUAL_PIXEL_QA_INCOMPLETE' in ao)
add('direct_composer_bypass_hard_blocked','guard_composer' in guard and 'BLOCK_RENDER' in gate and 'ARTIFACT_PIPELINE_OR_USER_VISIBLE_QA_INCOMPLETE' in gate)

# QA Brain integration.
qids=[c['id'] for c in qs['councils']]
add('qa_brain_14_councils',len(qids)==14,qids)
add('qa_actual_pixel_product_council_present','Q11_ACTUAL_PIXEL_PRODUCT_REVIEW' in qids,qids)
add('qa_artifact_skeptic_council_present','Q12_EXECUTIVE_SIMPLICITY_ARTIFACT_SKEPTIC' in qids,qids)
add('qa_delivery_integrity_council_present','Q13_DELIVERY_INTEGRITY_REPAIR_CLOSURE' in qids,qids)
add('qa_golden_rfp_council_present','Q14_GOLDEN_REAL_RFP_ACCEPTANCE' in qids,qids)
orch=(Q/'Brain/orchestrator.py').read_text(encoding='utf-8')
add('qa_route_wires_actual_pixel_council','Q11_ACTUAL_PIXEL_PRODUCT_REVIEW' in orch)
add('qa_route_wires_artifact_skeptic','Q12_EXECUTIVE_SIMPLICITY_ARTIFACT_SKEPTIC' in orch)
add('qa_authority_ceiling_consistent',osst['qa_authority_ceiling']=='QA_CANDIDATE_PASS' and ver['release_authority']=='RASHAD_BRAIN_RELEASE_CHAIR')

# Readme/current status coherence (exclude historical evidence files by design).
rread=(R/'README.md').read_text(encoding='utf-8'); qread=(Q/'README.md').read_text(encoding='utf-8'); cs=j(S/'CURRENT_SKILL_STATUS.json')
add('rashad_readme_current_brain_v3_2','Brain Runtime v2.0' not in rread and 'v3.2' in rread,rread[:500])
add('qa_readme_lists_actual_product_reviews','Actual Pixel / Product Review' in qread and 'Executive Simplicity & Artifact Skeptic' in qread)
brain_doc=(B/'BRAIN_RUNTIME_INTEGRATION.md').read_text(encoding='utf-8'); handoff=(R/'Docs/HANDOFF.md').read_text(encoding='utf-8')
add('brain_integration_doc_current_versions','v3.2' in brain_doc and ('QA Brain v1.2' in brain_doc or 'QA Brain**: v1.2' in brain_doc) and 'v2.0' not in brain_doc,brain_doc[:400])
add('handoff_uses_single_canonical_os','Rashad_OS.zip' in handoff and 'canonical package' in handoff and 'v3.2.0' in handoff and 'v1.2.0 / 14 councils' in handoff,handoff[:500])
add('skill_current_status_artifact_brain_authority','V7_1_ARTIFACT_INTELLIGENCE_BRAIN_CURRENT' in cs.get('artifact_brain_policy',''),cs.get('artifact_brain_policy'))
add('production_boundaries_truthful','live' in ' '.join(osst.get('known_remaining_production_requirements',[])).lower() and osst['production_release_status'].startswith('NOT_RELEASED'))

# Final verifier wiring.
fv=(Q/'FINAL_VERIFY.py').read_text(encoding='utf-8')
for token in ['artifact_brain_v3_2','artifact_brain_v3_2_red_team','artifact_brain_v3_2_stress_quality','a_to_z_relationship_audit','qa_brain','v7_1_incident_regression','final_red_team']:
    add('final_verifier_includes_'+token,token in fv)

out={'suite':'Rashad OS A-to-Z Relationship & Authority Audit','status':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL','passed':sum(x['status']=='PASS' for x in checks),'total':len(checks),'checks':checks}
(Q/'Certification/A_TO_Z_RELATIONSHIP_AUDIT_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'suite':out['suite'],'status':out['status'],'passed':out['passed'],'total':out['total'],'failed':[x for x in checks if x['status']=='FAIL']},ensure_ascii=False,indent=2))
raise SystemExit(0 if out['status']=='PASS' else 1)
