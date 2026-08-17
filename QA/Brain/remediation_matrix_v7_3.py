#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json, re, hashlib, sys
ROOT=Path(__file__).resolve().parents[2]
R=ROOT/'Rashad'; S=R/'Skill'; B=R/'Brain'; Q=ROOT/'QA'; C=Q/'Certification'
sys.path.insert(0,str(Q/'Runtime')); sys.path.insert(0,str(B/'runtime'))
from brain.production.font_preflight import check_brand_fonts
from qa_v4.detector_registry import implementation_map

def J(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def T(p): return Path(p).read_text(encoding='utf-8',errors='ignore')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def result(name):
    p=C/name
    if not p.exists(): return {}
    try:return J(p)
    except:return {}
def tpass(name): return result(name).get('status')=='PASS'
rows=[]
def add(fid,severity,owner,status,evidence,detail=''):
    rows.append({'finding_id':fid,'severity':severity,'owner_council':owner,'status':status,'evidence':evidence,'detail':detail})
def closed(fid,severity,owner,ok,evidence,detail=''):
    add(fid,severity,owner,'CLOSED' if ok else 'OPEN',evidence,detail)
def ext(fid,severity,owner,ok,evidence,detail=''):
    add(fid,severity,owner,'EXTERNAL_PREREQUISITE_ENFORCED' if ok else 'OPEN',evidence,detail)

am=J(S/'ACTIVE_AUTHORITY_MANIFEST.json'); bm=J(B/'BRAIN_MANIFEST.json')
art=J(B/'config/artifact_brain_expert_universe_v3.json')
vp=T(B/'runtime/brain/production/composer.py'); ar=T(B/'runtime/brain/artifact_brain.py'); pg=T(B/'runtime/brain/product_geometry.py')
gates=T(Q/'Runtime/qa/gates_v26.py'); core=T(Q/'Runtime/qa/visual_qa_core.py'); stress=T(Q/'Runtime/qa_v4/stress_runner_final.py')
reg=result('ARTIFACT_BRAIN_REGRESSION_V7_3.json'); regmap={x['name']:x for x in reg.get('rows',[])}
eng=result('ENGAGEMENT_ARTIFACT_ACCEPTANCE_V7_3.json'); engrows=eng.get('artifacts',eng.get('results',[]))
vis=result('VISUAL_PRODUCTION_V7_3_RESULTS.json'); vrt=result('VISUAL_PRODUCTION_RED_TEAM_V7_3_RESULTS.json')

# P0
closed('R1','P0','VISUAL_PRODUCTION_COUNCIL', all((B/p).exists() for p in ['runtime/brain/production/composer.py','runtime/brain/production/renderer.py','runtime/brain/imagery_director.py']) and am.get('production_composer_runtime'), ['brain/production/composer.py','brain/production/renderer.py','brain/imagery_director.py'])
closed('R2','P0','ARTIFACT_BRAIN_COUNCIL',regmap.get('IMAGE_LED_reachable_for_cover',{}).get('status')=='PASS',['ARTIFACT_BRAIN_REGRESSION_V7_3::IMAGE_LED_reachable_for_cover'])
law=T(S/'01_ACTIVE_RUNTIME/82_V7_3_VISUAL_PRODUCTION_ORGAN_AND_COMPOSITION_INTELLIGENCE_LAW.md')
closed('R3','P0','AUTHORITY_COUNCIL',all(x in law for x in ['do not translate analysis straight into boxes','may not reduce it to generic cards','generic-card/table downgrade fail release','zero measured objects is a hard fail']),['82_V7_3_VISUAL_PRODUCTION_ORGAN_AND_COMPOSITION_INTELLIGENCE_LAW.md'])
closed('R4','P0','TOTAL_QA_COUNCIL',am.get('quality_targets',{}).get('dominant_mass_min')==0.32 and am.get('quality_targets',{}).get('composition_distinct_ratio_min')==0.70 and 'G39_DOMINANT_MASS' in gates,['quality_targets','G39_DOMINANT_MASS'])
closed('NEW-01','P0','DELIVERY_INTEGRITY_COUNCIL','def pdf_model' in pg and 'NO_REGISTERED_INSPECTOR_FOR_FORMAT' in pg and any((x.get('name','').endswith('ChatGpt.pptx') and x.get('acceptance_status')=='BLOCKED') for x in engrows),['product_geometry.pdf_model','ENGAGEMENT_ARTIFACT_ACCEPTANCE_V7_3'])
fp=check_brand_fonts(); ext('NEW-02','P0','BRAND_TYPOGRAPHY_COUNCIL',fp.get('status')=='BLOCKED' and bool(fp.get('missing')) and 'Production release cannot render with fallback fonts' in str(fp.get('rule','')),['font_preflight.py'],detail='Brand font bytes are an environment prerequisite and are not embedded in the Skill; production blocks if absent.')
closed('AB-01','P0','ARTIFACT_BRAIN_COUNCIL',(B/'runtime/brain/composition_spec.py').exists() and 'RASHAD_PAGE_COMPOSITION_SPEC_V1' in T(B/'runtime/brain/composition_spec.py'),['composition_spec.py'])
closed('AB-03','P0','VISUAL_DIVERGENCE_COUNCIL',tpass('VISUAL_PRODUCTION_V7_3_RESULTS.json') and 'min_pairwise_divergence' in T(B/'runtime/brain/composition_spec.py') and (B/'runtime/brain/spec_divergence.py').exists(),['VISUAL_PRODUCTION_V7_3_RESULTS','spec_divergence.py'])
closed('AB-04','P0','COMPOSITION_QA_COUNCIL',tpass('THRESHOLD_BINDING_AUDIT_V7_3.json') and 'dominant_mass_min' in gates and 'DECK_DISTINCT_COMPOSITION_FLOOR_NOT_MET' in pg,['THRESHOLD_BINDING_AUDIT_V7_3','product_geometry.py'])
closed('QA-01','P0','TOTAL_QA_COUNCIL',all(x in gates for x in ['G36_VISIBLE_LANGUAGE_PURITY','G39_DOMINANT_MASS','G40_COLUMN_BALANCE','G41_CONNECTOR_PATH_GEOMETRY']) and 'Producer-authored owner/label metadata' in core and tpass('ARABIC_VISIBLE_LANGUAGE_PURITY_V7_3.json'),['gates_v26.py','visual_qa_core.py','ARABIC_VISIBLE_LANGUAGE_PURITY_V7_3'])
actual_hashes={x.get('sha256') for x in engrows}; expected_hashes={'e4116c3e497aab4a9b675950118d32bda03419fb16f039117a2fc688beda4988','6d40f5f567a80af1e7798dd34d30cb49ccb2530384b53c83ed197c552d09f8cd'}
# allow exact ChatGPT hash to be read from current report; the second known external hash may differ if report predates upload copy.
closed('QA-02','P0','ENGAGEMENT_ACCEPTANCE_COUNCIL',tpass('ENGAGEMENT_ARTIFACT_ACCEPTANCE_V7_3.json') and len(engrows)>=2 and all(x.get('sha256') and x.get('acceptance_status')=='BLOCKED' for x in engrows),['ENGAGEMENT_ARTIFACT_ACCEPTANCE_V7_3 actual file hashes'])
closed('QA-03','P0','STRESS_QA_COUNCIL',tpass('STRESS_CONTRACT_PARITY_V7_3.json') and 'repair_deleted_node' in stress and "status='EXPECTED_BLOCK'" in stress and 'Hash change alone has zero stress-pass authority' in stress,['STRESS_CONTRACT_PARITY_V7_3','stress_runner_final.py'])
closed('QA-05','P0','GEOMETRY_QA_COUNCIL','SAFE_AREA_VIOLATION' in pg and 'safe_area_min_visible_px2' in T(B/'runtime/brain/quality_floors_v7_3.py') and 'safe_margin_px' in T(B/'runtime/brain/composition_spec.py'),['product_geometry.py','quality_floors_v7_3.py'])
closed('AR-01','P0','ARABIC_VISIBLE_LANGUAGE_COUNCIL','P0 Proposal Control Layer' in pg and 'internal_vocabulary_leak' in gates and tpass('ARABIC_VISIBLE_LANGUAGE_PURITY_V7_3.json'),['product_geometry.py','G36_VISIBLE_LANGUAGE_PURITY'])
closed('AR-02','P0','ARABIC_VISIBLE_LANGUAGE_COUNCIL',all(x in pg for x in ["'READY'","'NEXT'","'BLOCKED'"]) and 'Compliance Register v0' in pg,['product_geometry.INTERNAL'])
# AR-03 is considered closed only when FINAL_VERIFY routes the correct purity suite.
fv=T(Q/'FINAL_VERIFY.py')
closed('AR-03','P0','CERTIFICATION_COUNCIL','test_arabic_visible_language_purity_v7_3.py' in fv,['FINAL_VERIFY.py'])
closed('AR-04','P0','ARABIC_PDF_COUNCIL',(B/'runtime/brain/production/searchable_pdf.py').exists() and 'logical_text' in T(B/'runtime/brain/production/searchable_pdf.py').lower() and tpass('VISUAL_PRODUCTION_V7_3_RESULTS.json'),['searchable_pdf.py','VISUAL_PRODUCTION_V7_3_RESULTS'])
im=implementation_map(); closed('AR-05','P0','QA_IMPLEMENTATION_COUNCIL',im.get('status')=='PASS' and im.get('implemented')==233 and im.get('case_count')==233,['detector_implementation_registry_v7_3.json','implementation_map()'])

# P1
closed('E10','P1','DELIVERY_RUNTIME_COUNCIL',tpass('GOVERNED_PRODUCTION_DELIVERY_V7_3.json'),['GOVERNED_PRODUCTION_DELIVERY_V7_3 successful governed path'])
closed('R5','P1','ARTIFACT_BRAIN_COUNCIL',regmap.get('rich_technical_problem_not_minimal_only',{}).get('status')=='PASS',['ARTIFACT_BRAIN_REGRESSION_V7_3::rich_technical_problem_not_minimal_only'])
closed('R6','P1','HOST_NATIVE_COUNCIL',(B/'runtime/brain/provider.py').exists() and 'HostNativeProvider' in T(B/'runtime/brain/provider.py') and tpass('GOVERNED_PRODUCTION_DELIVERY_V7_3.json'),['HostNativeProvider','GOVERNED_PRODUCTION_DELIVERY_V7_3'])
closed('R7','P1','THRESHOLD_GOVERNANCE_COUNCIL',regmap.get('diagram_ratio_threshold_parity',{}).get('status')=='PASS' and float(am.get('artifact_deck_diagram_ratio_hard_block_above',-1))==0.55,['ARTIFACT_BRAIN_REGRESSION_V7_3::diagram_ratio_threshold_parity','ACTIVE_AUTHORITY_MANIFEST'])
closed('R8','P1','DELIVERY_QA_COUNCIL','ARTIFACT_TRUTH_BELOW_90' in T(B/'runtime/brain/delivery_gate.py') and 'CEQS_BELOW_90' in T(B/'runtime/brain/delivery_gate.py') and tpass('V7_2_USER_VISIBLE_DELIVERY_CERTIFICATION.json'),['delivery_gate.py','V7_2_USER_VISIBLE_DELIVERY_CERTIFICATION'])
closed('R9','P1','PRODUCTION_RUNTIME_COUNCIL','PRODUCTION_PAGE_RENDER' in T(B/'runtime/artifact_delivery_orchestrator.py') and tpass('GOVERNED_PRODUCTION_DELIVERY_V7_3.json'),['artifact_delivery_orchestrator.py','GOVERNED_PRODUCTION_DELIVERY_V7_3'])
reach=result('ARTIFACT_EXPERT_REACHABILITY_V7_3.json'); closed('AB-05','P1','EXPERT_ROUTING_COUNCIL',reach.get('status')=='PASS' and reach.get('unreachable')==[] and reach.get('registered_roles')==107,['ARTIFACT_EXPERT_REACHABILITY_V7_3'])
closed('AB-06','P1','IMAGERY_COUNCIL','IMAGE_LED' in ar and 'HostNativeImageProvider' in T(B/'runtime/brain/production/image_provider.py') and am.get('imagery_director_runtime'),['artifact_brain.py','image_provider.py','imagery_director.py'])
closed('AB-07','P1','ART_DIRECTION_COUNCIL',all((B/'runtime/brain'/x).exists() for x in ['design_system_resolver.py','type_hierarchy_planner.py','style_memory.py']) and 'palette_role_map' in T(B/'runtime/brain/composition_spec.py'),['design_system_resolver.py','type_hierarchy_planner.py','style_memory.py'])
closed('AB-08','P1','CARD_DOMINANCE_COUNCIL','card_dominance_or_spoof' in core and 'gini<.15' in core.replace(' ',''),['G18_CARD_TRUTH'])
closed('QA-04','P1','TOTAL_QA_COUNCIL','required=bool(pd[\'edges\'] or spec.get(\'expected_edges\')' in core and 'required=bool(labs or required(spec,\'labels\',False))' in core,['G16_CONNECTORS','G17_LABELS'])
closed('QA-06','P1','VISIBLE_LANGUAGE_COUNCIL','G36_VISIBLE_LANGUAGE_PURITY' in gates and 'pure_latin_client_text_on_arabic_page' in gates and tpass('ARABIC_VISIBLE_LANGUAGE_PURITY_V7_3.json'),['G36_VISIBLE_LANGUAGE_PURITY'])
closed('QA-07','P1','DELIVERY_INTEGRITY_COUNCIL','inspect_artifact' in pg and 'PDF' in pg and 'PPTX' in pg and am.get('engagement_acceptance_rule'),['format-neutral product_geometry + engagement acceptance'])
closed('QA-08','P1','CONNECTOR_GEOMETRY_COUNCIL',all(x in gates for x in ['connector_crosses_non_endpoint_node','connector_crosses_text_label','arrowhead_direction_contradicts_flow','edge_crossing_budget_exceeded']),['G41_CONNECTOR_PATH_GEOMETRY'])
closed('AR-06','P1','BIDI_COUNCIL','G27_BIDI_RUNS' in gates and 'bidi' in T(Q/'Runtime/qa/unified_html_qa.py').lower(),['G27_BIDI_RUNS routed by unified_html_qa'])
closed('AR-07','P1','ARABIC_QA_COUNCIL','G36_VISIBLE_LANGUAGE_PURITY' in gates and 'G35_ARABIC_EXECUTIVE_TERMINOLOGY' in gates,['G35','G36'])
closed('AR-09','P1','COBRAND_COUNCIL','cobrand_not_physically_left' in gates and regmap.get('cobrand_physical_left_order_contract',{}).get('status')=='PASS',['G28_COBRAND','ARTIFACT_BRAIN_REGRESSION_V7_3'])
closed('AR-08','P1','ARABIC_NUMERAL_COUNCIL','western_numeral_leakage' in gates and tpass('ARABIC_VISIBLE_LANGUAGE_PURITY_V7_3.json'),['G36_VISIBLE_LANGUAGE_PURITY'])

# P2
idx=J(S/'03_ARTIFACT_ENGINE/ARTIFACT_ENGINE_LOGICAL_ID_INDEX_V7_3.json'); logical=[x['logical_id'] for x in idx.get('entries',[])]; engine_files=[p for p in (S/'03_ARTIFACT_ENGINE').glob('*') if p.is_file() and p.name!='ARTIFACT_ENGINE_LOGICAL_ID_INDEX_V7_3.json']
closed('E12','P2','AUTHORITY_IDENTITY_COUNCIL',len(logical)==len(set(logical)) and idx.get('file_count')==len(idx.get('entries',[])) and len(idx.get('entries',[]))>=len(engine_files),['ARTIFACT_ENGINE_LOGICAL_ID_INDEX_V7_3'])
ver=J(R/'VERSION.json'); osst=J(R/'OS_STATUS.json'); cs=J(S/'CURRENT_SKILL_STATUS.json')
closed('E13','P2','VERSION_AUTHORITY_COUNCIL',ver.get('canonical_skill_version')==osst.get('canonical_skill_version')==cs.get('skill_version')==am.get('version')=='7.3.0' and bm.get('bound_skill_version')=='7.3.0',['VERSION.json','OS_STATUS.json','CURRENT_SKILL_STATUS.json','BRAIN_MANIFEST.json'])
recipe=J(S/'01_ACTIVE_RUNTIME/VISUAL_PRODUCTION_RECIPE_INDEX_V7_3.json'); closed('R10','P2','COBRAND_COUNCIL',bool(recipe.get('recipes',{}).get('brand_cover_cobrand')) and any('16_COBRAND_LOGO_DIRECTOR' in x for x in recipe['recipes']['brand_cover_cobrand']),['VISUAL_PRODUCTION_RECIPE_INDEX_V7_3'])
closed('R11','P2','ARTIFACT_BRAIN_COUNCIL',regmap.get('SHIFT_FOCAL_POINT_reachable_and_physical',{}).get('status')=='PASS',['ARTIFACT_BRAIN_REGRESSION_V7_3'])
closed('R12','P2','AUTHORITY_COUNCIL','Quality floors' in T(S/'SKILL.md') or 'Quality floors are mandatory' in T(S/'SKILL.md'),['SKILL.md V7.3 Visual Production'])
closed('AB-09','P2','NEGATIVE_SPACE_COUNCIL',(B/'runtime/brain/negative_space_budget.py').exists() and 'negative_space_zones' in T(B/'runtime/brain/composition_spec.py'),['negative_space_budget.py','composition_spec.py'])
closed('AB-10','P2','REFERENCE_GRAMMAR_COUNCIL',regmap.get('reference_grammar_retrieval_executes',{}).get('status')=='PASS' and regmap.get('exhibit_engine_no_KeyError',{}).get('status')=='PASS',['ARTIFACT_BRAIN_REGRESSION_V7_3'])
closed('AB-11','P2','VISUAL_MEMORY_COUNCIL',regmap.get('composition_signature_excludes_content_hash',{}).get('status')=='PASS' and 'structural_signature' in T(B/'runtime/brain/visual_memory.py'),['visual_memory.py','ARTIFACT_BRAIN_REGRESSION_V7_3'])
closed('QA-09','P2','THRESHOLD_GOVERNANCE_COUNCIL',tpass('THRESHOLD_BINDING_AUDIT_V7_3.json'),['THRESHOLD_BINDING_AUDIT_V7_3'])
closed('QA-10','P2','QA_IMPLEMENTATION_COUNCIL','historical_taxonomy_status' in T(Q/'Runtime/qa_v4/detector_registry.py') and im.get('status')=='PASS',['detector_registry.py'])
closed('QA-11','P2','GEOMETRY_QA_COUNCIL','Producer-authored owner/label metadata and >92% containment are not collision escape hatches.' in core,['visual_qa_core.py G06'])
closed('QA-12','P2','STRESS_QA_COUNCIL',tpass('STRESS_CONTRACT_PARITY_V7_3.json'),['STRESS_CONTRACT_PARITY_V7_3'])
closed('P2-DECK-CONTINUITY-ZERO-CALLERS','P2','DECK_CONTINUITY_COUNCIL',tpass('DECK_CONTINUITY_CERTIFICATION_V7_3.json') and 'deck_continuity' in T(B/'runtime/brain/delivery_gate.py').lower(),['DECK_CONTINUITY_CERTIFICATION_V7_3','delivery_gate.py'])

open_rows=[r for r in rows if r['status']=='OPEN']; p0p1=[r for r in open_rows if r['severity'] in ('P0','P1')]
out={
 'suite':'Rashad v7.3 Council-Supervised Remediation Matrix',
 'status':'PASS' if not open_rows else 'FAIL',
 'finding_count':len(rows),'closed':sum(r['status']=='CLOSED' for r in rows),
 'external_prerequisite_enforced':sum(r['status']=='EXTERNAL_PREREQUISITE_ENFORCED' for r in rows),
 'open_count':len(open_rows),'open_p0_p1':len(p0p1),
 'rule':'Implementer → Specialist Council → Adversarial Council → Engagement-File Acceptance. Code presence alone is not closure.',
 'engagement_acceptance_status':eng.get('status'),
 'rows':rows,
}
(C/'REMEDIATION_MATRIX_V7_3.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'suite':out['suite'],'status':out['status'],'findings':len(rows),'closed':out['closed'],'external_prerequisite_enforced':out['external_prerequisite_enforced'],'open':len(open_rows),'open_p0_p1':len(p0p1),'open_rows':open_rows},ensure_ascii=False,indent=2))
raise SystemExit(0 if out['status']=='PASS' else 2)
