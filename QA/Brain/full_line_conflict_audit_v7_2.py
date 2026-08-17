#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[2]; SKILL=ROOT/'Rashad/Skill'; BRAIN=ROOT/'Rashad/Brain'; QA=ROOT/'QA'
TEXT_EXT={'.md','.txt','.json','.py','.yaml','.yml','.csv'}
def J(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def main():
    m=J(SKILL/'ACTIVE_AUTHORITY_MANIFEST.json'); globals=set(m.get('global_authorities',[])); rex=J(SKILL/'RETRIEVAL_EXCLUSION_REGISTRY.json')
    explicit={e.get('path') for e in rex.get('entries',[]) if e.get('path')}
    findings=[]; stats={'files_scanned':0,'lines_scanned':0,'bytes_scanned':0,'self_claim_files':0,'nonmanifest_self_claim_files':0}
    self_rx=re.compile(r'\b(?:STATUS\s*:\s*)?(?:CURRENT|ACTIVE|LATEST|HIGHEST|ALWAYS[- ]ON|LOAD[- ]FOR[- ]ALL)\b',re.I)
    stale_current_rx=re.compile(r'(?:STATUS[^\n]*CURRENT[^\n]*V7\.1|CURRENT UNDER RASHAD v7\.1\.0|CURRENT ROUTER TO RASHAD v7\.1)',re.I)
    stale701_rx=re.compile(r'23_V7_0_1_RFP_SUMMARY|73_V7_0_1_COUNCIL|74_V7_0_1_RFP_BID|rfp_bid_decision_evidence_v7_0_1',re.I)
    stale_count_rx=re.compile(r'(?i)(?:3\s*[–-]\s*4|3\s*[–-]\s*5).{0,80}(?:concept|hypoth|render)|(?:concept|hypoth|render).{0,80}(?:3\s*[–-]\s*4|3\s*[–-]\s*5)')
    unsafe_partial_rx=re.compile(r'(?i)user[- ]visible.{0,120}(?:DRAFT_QA_PARTIAL|partial qa|without pixel|pixel.*not executed)')
    h1_rx=re.compile(r"(?i)(winner\s*[:=]\s*['\"]?H1\b|H1_DEFAULT|POSITIONAL_DEFAULT)")
    global_sensitive=('00_CHAT_MIRROR_KERNEL/','01_ACTIVE_RUNTIME/','03_ARTIFACT_ENGINE/','05_WORKFLOW_ENGINE/','07_GOVERNANCE_AND_QA/')
    specialist=('02_IMMUTABLE_AUTHORITIES/','08_BRAND_CURRENT/','11_RUBIX_FIRM_KNOWLEDGE/')
    for base,label in [(SKILL,'Skill'),(BRAIN,'Brain'),(QA,'QA')]:
        for p in base.rglob('*'):
            if not p.is_file() or p.suffix.lower() not in TEXT_EXT or '__pycache__' in p.parts: continue
            stats['files_scanned']+=1; stats['bytes_scanned']+=p.stat().st_size
            lines=p.read_text(encoding='utf-8',errors='ignore').splitlines(); stats['lines_scanned']+=len(lines)
            rel=p.relative_to(SKILL).as_posix() if base==SKILL else None; claims=[]
            for i,line in enumerate(lines,1):
                if self_rx.search(line): claims.append((i,line.strip()[:260]))
                if base==SKILL and rel in globals:
                    if stale701_rx.search(line): findings.append({'severity':'P0','kind':'STALE_V7_0_1_ROUTE_IN_CURRENT_AUTHORITY','file':rel,'line':i,'text':line.strip()[:300]})
                    if stale_current_rx.search(line) and 'FOUNDATION UNDER V7.2' not in line.upper(): findings.append({'severity':'P0','kind':'STALE_V7_1_CURRENT_STATUS_IN_V7_2_AUTHORITY','file':rel,'line':i,'text':line.strip()[:300]})
                    if stale_count_rx.search(line) and not any(w in line.lower() for w in ['legacy','historical','supersed','forbid','old']): findings.append({'severity':'P0','kind':'STALE_CONCEPT_COUNT_IN_CURRENT_AUTHORITY','file':rel,'line':i,'text':line.strip()[:300]})
                    if unsafe_partial_rx.search(line) and not any(w in line.lower() for w in ['forbid','cannot','block']): findings.append({'severity':'P0','kind':'USER_VISIBLE_PARTIAL_QA_ESCAPE','file':rel,'line':i,'text':line.strip()[:300]})
                if h1_rx.search(line) and not any(w in line.lower() for w in ['forbid','block','cannot','attack','pattern','regex','h1_rx']) and 'tests' not in p.parts and 'Certification' not in p.parts:
                    findings.append({'severity':'P0','kind':'POSITIONAL_H1_AUTHORITY_PATTERN','file':str(p.relative_to(ROOT)),'line':i,'text':line.strip()[:300]})
            if claims:
                stats['self_claim_files']+=1
                if base==SKILL and rel not in globals and rel not in {'SKILL.md','00_START_HERE.md','ACTIVE_AUTHORITY_MANIFEST.json','RETRIEVAL_EXCLUSION_REGISTRY.json','AUTHORITY_BINDING_CHECK.json','CURRENT_SKILL_STATUS.json','VERSION.md'} and 'tests/' not in rel:
                    stats['nonmanifest_self_claim_files']+=1
                    if rel.startswith('10_PROVENANCE/'): continue
                    if rel.startswith(specialist): continue
                    if rel in explicit: continue
                    if rel.startswith(global_sensitive):
                        # v7.2 retrieval law: ACTIVE_AUTHORITY_MANIFEST is the only global allowlist.
                        # Non-manifest specialist files may contain historical/local ACTIVE/CURRENT labels; they have zero global authority by construction.
                        # Escalate only an explicit attempt to override the root manifest.
                        head='\n'.join(lines[:12]).upper()
                        if any(x in head for x in ['OVERRIDES ACTIVE_AUTHORITY_MANIFEST','SOLE MACHINE ROUTING SOURCE','GLOBAL AUTHORITY OVERRIDES ROOT MANIFEST']):
                            findings.append({'severity':'P1','kind':'NONMANIFEST_ATTEMPTS_ROOT_AUTHORITY_OVERRIDE','file':rel,'line':claims[0][0],'text':claims[0][1]})
    for rel in globals:
        if not (SKILL/rel).exists(): findings.append({'severity':'P0','kind':'MISSING_GLOBAL_AUTHORITY','file':rel})
    ver=J(ROOT/'Rashad/VERSION.json'); osj=J(ROOT/'Rashad/OS_STATUS.json'); bm=J(BRAIN/'BRAIN_MANIFEST.json')
    expected={'skill':'7.2.0','brain':'3.4.0','artifact':'3.3.0','qa':'4.3','qabrain':'1.3.0'}
    vals=[ver.get('canonical_skill_version'),osj.get('canonical_skill_version'),bm.get('bound_skill_version'),m.get('version')]
    if len(set(vals))!=1 or vals[0]!=expected['skill']: findings.append({'severity':'P0','kind':'SKILL_VERSION_SPLIT_BRAIN','values':vals})
    bvals=[ver.get('brain_runtime_version'),osj.get('brain_runtime_version'),bm.get('brain_version'),m.get('brain_runtime_version')]
    if len(set(bvals))!=1 or bvals[0]!=expected['brain']: findings.append({'severity':'P0','kind':'BRAIN_VERSION_SPLIT_BRAIN','values':bvals})
    avals=[bm.get('artifact_brain_version'),m.get('artifact_brain_version'),J(BRAIN/'config/artifact_brain_expert_universe_v3.json').get('artifact_brain_version')]
    if len(set(avals))!=1 or avals[0]!=expected['artifact']: findings.append({'severity':'P0','kind':'ARTIFACT_VERSION_SPLIT_BRAIN','values':avals})
    if m.get('certification_harness')!='tests/skill_certification/verify_skill_v7_2.py': findings.append({'severity':'P0','kind':'STALE_CURRENT_CERT_HARNESS','value':m.get('certification_harness')})
    if 'tests/skill_certification/red_team_skill_v7_2.py' not in m.get('certification_harnesses',[]): findings.append({'severity':'P0','kind':'STALE_CURRENT_REDTEAM_HARNESS'})
    inherited=set(m.get('inherited_artifact_foundations',[]))
    if inherited & globals: findings.append({'severity':'P0','kind':'LEGACY_ARTIFACT_FOUNDATION_REACTIVATED','files':sorted(inherited&globals)})
    # Brain actor reachability: registered is not enough.
    actors=J(BRAIN/'config/actor_ontology.json'); rules=J(BRAIN/'config/brain_expert_routing_rules.json'); allids={a['id'] for a in actors['actors']}; refs=set(rules.get('core_roles',[]))|set(rules.get('mandatory_governors_for_critical',[]))
    for v in rules.get('role_rules',{}).values(): refs.update(v)
    for r in rules.get('domain_rules',[]): refs.update(r.get('roles',[]))
    if allids!=refs: findings.append({'severity':'P0','kind':'BRAIN_REGISTERED_ACTOR_NOT_EXECUTABLY_ROUTABLE','unreachable':sorted(allids-refs),'unknown':sorted(refs-allids)})
    # Artifact registries/runtime exact parity.
    sys.path.insert(0,str(BRAIN/'runtime')); from brain.artifact_brain import STRATEGIES
    art=J(BRAIN/'config/artifact_brain_expert_universe_v3.json'); reg=set(art.get('communication_strategy_universe',[])); runtime=set(STRATEGIES)
    if reg!=runtime or len(runtime)!=24: findings.append({'severity':'P0','kind':'ARTIFACT_STRATEGY_REGISTRY_DRIFT','runtime':len(runtime),'registry':len(reg),'missing':sorted(runtime-reg),'extra':sorted(reg-runtime)})
    role_ids={r['id'] for r in art['roles']}; missing_roles=sorted({rid for c in art['councils'] for rid in c.get('roles',[]) if rid not in role_ids})
    if missing_roles: findings.append({'severity':'P0','kind':'ARTIFACT_COUNCIL_ROLE_UNRESOLVED','roles':missing_roles})
    # Host-native provider-mode integration must be current and executable.
    provtxt=(BRAIN/'runtime/brain/provider.py').read_text(); emtxt=(BRAIN/'runtime/brain/execution_mode.py').read_text(); qprov=(QA/'Brain/provider.py').read_text()
    for token,kind,src in [('class HostNativeProvider','HOST_NATIVE_PROVIDER_MISSING',provtxt),('class HostNativeResponseBundleProvider','HOST_NATIVE_BUNDLE_PROVIDER_MISSING',provtxt),('HOST_NATIVE_MODE','EXECUTION_MODE_RESOLVER_MISSING',emtxt),('class HostNativeQAProvider','HOST_NATIVE_QA_PROVIDER_MISSING',qprov)]:
        if token not in src: findings.append({'severity':'P0','kind':kind})
    if m.get('execution_modes')!=['HOST_NATIVE_MODE','API_PROVIDER_MODE','OFFLINE_VALIDATION_MODE']: findings.append({'severity':'P0','kind':'EXECUTION_MODE_MANIFEST_DRIFT','value':m.get('execution_modes')})
    if '01_ACTIVE_RUNTIME/80_V7_2_HOST_NATIVE_EXECUTION_AND_PROVIDER_MODE_LAW.md' not in globals: findings.append({'severity':'P0','kind':'HOST_NATIVE_LAW_NOT_GLOBAL'})
    if '07_GOVERNANCE_AND_QA/83_V7_2_HOST_NATIVE_EXECUTION_TRACE_AND_PROVIDER_TRUTHFULNESS.md' not in globals: findings.append({'severity':'P0','kind':'HOST_NATIVE_QA_LAW_NOT_GLOBAL'})
    # Runtime escape hatch signatures required.
    ag=(BRAIN/'runtime/brain/artifact_gate.py').read_text(); ep=(BRAIN/'runtime/brain/execution_proof.py').read_text(); ao=(BRAIN/'runtime/brain/actual_output_qa.py').read_text(); dg=(BRAIN/'runtime/brain/delivery_gate.py').read_text(); pi=(BRAIN/'runtime/brain/product_inspector.py').read_text()
    for token,kind,src in [
      ('BRAIN_EXECUTION_PROOF_REQUIRED','BRAIN_PROOF_GATE_MISSING',ag),('ARTIFACT_COUNCIL_EXECUTION_REQUIRED','ARTIFACT_COUNCIL_GATE_MISSING',ag),('USER_VISIBLE_MASTER_MUST_BE_PRODUCTION_PAGE_RENDER','PRODUCTION_RENDER_GATE_MISSING',ag),('ACTUAL_PIXEL_QA_REQUIRED_FOR_USER_VISIBLE','PIXEL_QA_GATE_MISSING',ag),('QA_REPAIR_LOOP_NOT_CLOSED','REPAIR_GATE_MISSING',ag),('validate_brain_execution_proof','PROOF_RECOMPUTE_MISSING',ep),('PIXEL_REVIEW_HASH_BINDING_MISMATCH','PIXEL_HASH_BINDING_MISSING',ao),('BLOCK_DELIVERY','EXACT_FILE_DELIVERY_GATE_MISSING',dg),('PPTX_EQUAL_CARD_GRID_OVERUSE','CARD_GRID_BLOCK_MISSING',pi),('PPTX_SHAPE_ONLY_ANALYTICAL_DECK_OVERUSE','SHAPE_ONLY_BLOCK_MISSING',pi)]:
        if token not in src: findings.append({'severity':'P0','kind':kind})
    # Current-facing documentation must describe the v7.2/v3.4 route, never present v7.1/v3.2 as current.
    current_facing=[ROOT/'Rashad/README.md',ROOT/'QA/README.md',ROOT/'QA/Runtime/README.md',ROOT/'QA/Runtime/VERSION.md',SKILL/'PROJECT_INSTRUCTIONS.md',SKILL/'00_START_HERE.md',ROOT/'Rashad/Docs/HANDOFF.md']
    stale_doc_rx=re.compile(r'(Canonical Rashad Layer v7\.1|Rashad Proposal OS v7\.1\.0|bound to Rashad Proposal OS v7\.1\.0|Bound Skill:\s*Rashad Proposal OS v7\.1\.0|Rashad Brain:\s*v3\.2\.0|current v7\.1 startup route|Rashad OS v7\.1\s*/\s*Brain v3\.2)',re.I)
    for fp in current_facing:
        tx=fp.read_text(encoding='utf-8',errors='ignore') if fp.exists() else ''
        if not fp.exists(): findings.append({'severity':'P0','kind':'CURRENT_FACING_DOC_MISSING','file':str(fp.relative_to(ROOT))})
        elif stale_doc_rx.search(tx): findings.append({'severity':'P0','kind':'STALE_CURRENT_FACING_VERSION_WORDING','file':str(fp.relative_to(ROOT))})
    # Current v7.2 execution/certification must not depend on v7.1 test harnesses.
    current_exec=[QA/'FINAL_VERIFY.py',QA/'Brain/run_v7_2_user_visible_delivery_certification.py',QA/'Brain/red_team_v7_2_delivery.py',QA/'Brain/golden_redf_acceptance_v7_2.py',QA/'Brain/incident_regression_v7_2.py',QA/'Brain/stress_quality_v7_2.py']
    for fp in current_exec:
        tx=fp.read_text(encoding='utf-8',errors='ignore') if fp.exists() else ''
        if re.search(r'(?:from|import|Brain/)[^\n]*v7_1',tx,re.I): findings.append({'severity':'P0','kind':'CURRENT_V72_DEPENDS_ON_V71_EXECUTION_SCRIPT','file':str(fp.relative_to(ROOT))})

    # Current certification indexes cannot remain v7.1-current.
    for idx in [ROOT/'Rashad/Certification/CURRENT_CERTIFICATION_INDEX.json',ROOT/'QA/Certification/CURRENT_CERTIFICATION_INDEX.json']:
        if idx.exists():
            x=J(idx)
            if x.get('canonical_skill_version') not in (None,'7.2.0') or str(x.get('status','')).startswith('CURRENT_V7_1'):
                findings.append({'severity':'P0','kind':'STALE_CURRENT_CERTIFICATION_INDEX','file':str(idx.relative_to(ROOT)),'status':x.get('status'),'version':x.get('canonical_skill_version')})
    p0=[f for f in findings if f['severity']=='P0']; p1=[f for f in findings if f['severity']=='P1']
    out={'suite':'Rashad v7.2 Full Line Conflict Audit','status':'PASS' if not p0 and not p1 else 'FAIL','stats':stats,'manifest_authorities':len(globals),'p0_count':len(p0),'p1_count':len(p1),'findings':findings}
    dest=QA/'Certification/FULL_LINE_CONFLICT_AUDIT_V7_2.json'; dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:out[k] for k in ['suite','status','stats','manifest_authorities','p0_count','p1_count']},ensure_ascii=False,indent=2))
    if findings: print(json.dumps(findings[:80],ensure_ascii=False,indent=2))
    return 0 if out['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
