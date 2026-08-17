#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json,re,hashlib,sys
ROOT=Path(__file__).resolve().parents[2]
SKILL=ROOT/'Rashad/Skill'; BRAIN=ROOT/'Rashad/Brain'; QA=ROOT/'QA'
TEXT_EXT={'.md','.txt','.json','.py','.yaml','.yml','.toml','.ini','.csv'}

def readj(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    m=readj(SKILL/'ACTIVE_AUTHORITY_MANIFEST.json'); manifest=set(m.get('global_authorities',[]))
    rex=readj(SKILL/'RETRIEVAL_EXCLUSION_REGISTRY.json')
    explicit={e.get('path') for e in rex.get('entries',[]) if e.get('scope')=='GLOBAL_ROUTE_EXCLUDED'}
    findings=[]; stats={'files_scanned':0,'lines_scanned':0,'bytes_scanned':0,'self_claim_files':0,'nonmanifest_self_claim_files':0}
    self_rx=re.compile(r'(?i)(STATUS\s*:\s*(?:CURRENT|ACTIVE|LATEST|HIGHEST|ALWAYS[- ]ON)|\bCURRENT\s+(?:GLOBAL\s+)?AUTHORITY\b|\bHIGHEST\s+CURRENT\b|\bALWAYS[- ]ON\b)')
    stale_rx=re.compile(r'(?i)(council_lens_registry_v7_0_1|23_V7_0_1_RFP_SUMMARY|rfp_bid_decision_evidence_v7_0_1|CURRENT[^\n]{0,80}v7[._ -]?0[._ -]?1|load V6 Artifact Intelligence|current V6 exhibit|current V6 CEQS)')
    historical_rx=re.compile(r'(?i)(legacy|historical|lineage|inherited|baseline|protected|supersed|compatib|previous|retired|provenance|reference only)')
    unsafe_draft_rx=re.compile(r'(?i)(ARTIFACT_DRAFT.{0,180}(pixel|actual-output|visual).{0,180}(NOT_EXECUTED|may proceed|warning)|pixel.{0,180}NOT_EXECUTED.{0,180}ARTIFACT_DRAFT)')
    relationship_authority_rx=re.compile(r'(?i)(relationship-first\s+Artifact Engine\s+is\s+unchanged|preserve\s+the\s+v6\s+relationship-first\s+engine|artifact/visual\s*=\s*relationship-first)')
    old_hypothesis_semantics_rx=re.compile(r'(?i)(5\s+materially\s+different\s+exhibit\s+hypotheses|five\s+hypotheses\s+must\s+differ\s+in\s+at\s+least\s+two\s+of:\s*topology)')
    count_rx=re.compile(r'(?i)(3\s*[–-]\s*[45]).{0,80}(concept|hypoth|render)|(?:concept|hypoth|render).{0,80}(3\s*[–-]\s*[45])')
    h1_rx=re.compile(r"(?i)(winner\s*[:=]\s*['\"]?H1\b|H1_DEFAULT|POSITIONAL_DEFAULT)")
    global_sensitive_prefix=('00_CHAT_MIRROR_KERNEL/','01_ACTIVE_RUNTIME/','03_ARTIFACT_ENGINE/','05_WORKFLOW_ENGINE/','07_GOVERNANCE_AND_QA/')
    specialist_current_prefix=('02_IMMUTABLE_AUTHORITIES/','08_BRAND_CURRENT/','11_RUBIX_FIRM_KNOWLEDGE/')

    for base,label in [(SKILL,'Skill'),(BRAIN,'Brain'),(QA,'QA')]:
        for p in base.rglob('*'):
            if not p.is_file() or p.suffix.lower() not in TEXT_EXT: continue
            stats['files_scanned']+=1; stats['bytes_scanned']+=p.stat().st_size
            try: lines=p.read_text(encoding='utf-8',errors='ignore').splitlines()
            except Exception: continue
            stats['lines_scanned']+=len(lines)
            rel_skill=p.relative_to(SKILL).as_posix() if base==SKILL else None
            claims=[]
            for i,line in enumerate(lines,1):
                if self_rx.search(line): claims.append((i,line.strip()[:240]))
                if base==SKILL and rel_skill in manifest and stale_rx.search(line) and not historical_rx.search(line) and 'downstream' not in line.lower():
                    findings.append({'severity':'P0','kind':'STALE_VERSION_ROUTE_IN_CURRENT_AUTHORITY','file':rel_skill,'line':i,'text':line.strip()[:300]})
                if base==SKILL and rel_skill in manifest and count_rx.search(line) and not historical_rx.search(line):
                    findings.append({'severity':'P0','kind':'STALE_CONCEPT_COUNT_IN_CURRENT_AUTHORITY','file':rel_skill,'line':i,'text':line.strip()[:300]})
                if base==SKILL and rel_skill in manifest and unsafe_draft_rx.search(line) and not historical_rx.search(line):
                    findings.append({'severity':'P0','kind':'ACTIVE_AUTHORITY_ALLOWS_USER_VISIBLE_PARTIAL_PIXEL_QA','file':rel_skill,'line':i,'text':line.strip()[:300]})
                if base==SKILL and rel_skill in manifest and relationship_authority_rx.search(line) and not historical_rx.search(line) and 'downstream' not in line.lower():
                    findings.append({'severity':'P0','kind':'RELATIONSHIP_ENGINE_REGAINS_VISUAL_DECISION_AUTHORITY','file':rel_skill,'line':i,'text':line.strip()[:300]})
                if base==SKILL and rel_skill in manifest and old_hypothesis_semantics_rx.search(line) and not historical_rx.search(line):
                    findings.append({'severity':'P0','kind':'ACTIVE_AUTHORITY_USES_GEOMETRY_FIRST_HYPOTHESIS_SEMANTICS','file':rel_skill,'line':i,'text':line.strip()[:300]})
                if h1_rx.search(line) and not any(w in line.lower() for w in ('forbid','block','cannot','attack','pattern','regex','h1_rx')) and 'test' not in p.name.lower() and 'Certification' not in p.parts and 'tests' not in p.parts:
                    findings.append({'severity':'P0','kind':'POSITIONAL_H1_AUTHORITY_PATTERN','file':str(p.relative_to(ROOT)),'line':i,'text':line.strip()[:300]})
            if claims:
                stats['self_claim_files']+=1
                if base==SKILL and rel_skill not in manifest and rel_skill not in {'SKILL.md','00_START_HERE.md','ACTIVE_AUTHORITY_MANIFEST.json','RETRIEVAL_EXCLUSION_REGISTRY.json','AUTHORITY_BINDING_CHECK.json','CURRENT_SKILL_STATUS.json','VERSION.md'} and 'tests/' not in rel_skill:
                    stats['nonmanifest_self_claim_files']+=1
                    if rel_skill.startswith(global_sensitive_prefix):
                        # Broad v7.1 retrieval rule quarantines any global self-claim outside manifest.
                        # Explicit entries are still tracked for transparency, but not mandatory one-by-one.
                        pass
                    elif rel_skill.startswith(specialist_current_prefix):
                        pass
                    elif rel_skill.startswith('10_PROVENANCE/'):
                        pass
                    elif rel_skill not in explicit:
                        findings.append({'severity':'P1','kind':'UNSCOPED_NONMANIFEST_CURRENT_CLAIM','file':rel_skill,'line':claims[0][0],'text':claims[0][1]})

    # Current path existence
    for rel in manifest:
        if not (SKILL/rel).exists(): findings.append({'severity':'P0','kind':'MISSING_MANIFEST_AUTHORITY','file':rel})

    # Version binding
    skilltxt=(SKILL/'SKILL.md').read_text(encoding='utf-8'); version=(SKILL/'VERSION.md').read_text(encoding='utf-8'); osj=readj(ROOT/'Rashad/OS_STATUS.json'); bj=readj(BRAIN/'BRAIN_MANIFEST.json')
    expected='7.1.0'
    if expected not in skilltxt: findings.append({'severity':'P0','kind':'SKILL_VERSION_NOT_7_1_0'})
    if expected not in version: findings.append({'severity':'P0','kind':'VERSION_FILE_NOT_7_1_0'})
    if m.get('version')!=expected: findings.append({'severity':'P0','kind':'MANIFEST_VERSION_MISMATCH','value':m.get('version')})
    if osj.get('canonical_skill_version')!=expected: findings.append({'severity':'P0','kind':'OS_SKILL_VERSION_MISMATCH','value':osj.get('canonical_skill_version')})
    if bj.get('bound_skill_version')!=expected: findings.append({'severity':'P0','kind':'BRAIN_SKILL_VERSION_MISMATCH','value':bj.get('bound_skill_version')})
    if m.get('certification_harness')!='tests/skill_certification/verify_skill_v7_1.py': findings.append({'severity':'P0','kind':'STALE_CURRENT_CERTIFICATION_HARNESS','value':m.get('certification_harness')})
    if m.get('rfp_summary_current_workflow')!='05_WORKFLOW_ENGINE/23_V7_RFP_SUMMARY_DECISION_WORKFLOW.md': findings.append({'severity':'P0','kind':'DECISION_WORKFLOW_ROUTE_CONFLATED','value':m.get('rfp_summary_current_workflow')})
    if m.get('rfp_summary_artifact_delivery_workflow')!='05_WORKFLOW_ENGINE/24_V7_1_RFP_SUMMARY_ARTIFACT_DELIVERY_WORKFLOW.md': findings.append({'severity':'P0','kind':'ARTIFACT_DELIVERY_WORKFLOW_ROUTE_MISSING','value':m.get('rfp_summary_artifact_delivery_workflow')})
    if 'tests/skill_certification/red_team_skill_v7_1.py' not in m.get('certification_harnesses',[]): findings.append({'severity':'P0','kind':'STALE_CURRENT_RED_TEAM_HARNESS','value':m.get('certification_harnesses')})
    for idxp in [ROOT/'Rashad/Certification/CURRENT_CERTIFICATION_INDEX.json', ROOT/'QA/Certification/CURRENT_CERTIFICATION_INDEX.json']:
        if idxp.exists():
            ix=readj(idxp)
            expected_versions={'canonical_skill_version':'7.1.0','brain_runtime_version':'3.2.0','artifact_brain_version':'3.2.0','qa_runtime_version':'4.3','qa_brain_version':'1.2.0'}
            for k,v in expected_versions.items():
                if ix.get(k)!=v: findings.append({'severity':'P0','kind':'STALE_CURRENT_CERTIFICATION_INDEX','file':str(idxp.relative_to(ROOT)),'field':k,'value':ix.get(k),'expected':v})

    # Cross-registry Artifact communication-strategy consistency.
    sys.path.insert(0,str(BRAIN/'runtime'))
    from brain.artifact_brain import STRATEGIES
    expert=readj(BRAIN/'config/artifact_brain_expert_universe_v3.json')
    registry_strategies=set(expert.get('communication_strategy_universe',[]))
    runtime_strategies=set(STRATEGIES)
    if len(runtime_strategies)!=24 or registry_strategies!=runtime_strategies:
        findings.append({'severity':'P0','kind':'ARTIFACT_COMMUNICATION_STRATEGY_REGISTRY_DRIFT','runtime_count':len(runtime_strategies),'registry_count':len(registry_strategies),'missing_from_registry':sorted(runtime_strategies-registry_strategies),'extra_in_registry':sorted(registry_strategies-runtime_strategies)})

    # Runtime escape-hatch scans
    ag=(BRAIN/'runtime/brain/artifact_gate.py').read_text(encoding='utf-8')
    ao=(BRAIN/'runtime/brain/actual_output_qa.py').read_text(encoding='utf-8')
    vs=(BRAIN/'runtime/rfp_summary_orchestrator.py').read_text(encoding='utf-8')
    dg=(BRAIN/'runtime/brain/delivery_gate.py').read_text(encoding='utf-8')
    if "'DRAFT_QA_PARTIAL'" in ag or 'DRAFT_QA_PARTIAL\")' in ag: findings.append({'severity':'P0','kind':'USER_VISIBLE_GATE_ACCEPTS_PARTIAL_QA'})
    if 'COMMUNICATION_STRATEGY_CONCEPT_RENDER' not in ag or 'CONCEPT_RENDER_CANNOT_BE_USER_VISIBLE_MASTER' not in ag: findings.append({'severity':'P0','kind':'CONCEPT_RENDER_USER_VISIBLE_BLOCK_MISSING'})
    if 'USER_VISIBLE_REQUIRES_PRODUCTION_PAGE_RENDER' not in ao: findings.append({'severity':'P0','kind':'ACTUAL_QA_PRODUCTION_RENDER_REQUIREMENT_MISSING'})
    if 'PIXEL_REVIEW_HASH_BINDING_MISMATCH' not in ao: findings.append({'severity':'P0','kind':'PIXEL_HASH_BINDING_MISSING'})
    if 'BLOCK_DELIVERY' not in dg: findings.append({'severity':'P0','kind':'EXACT_FILE_DELIVERY_GATE_MISSING'})
    if "'status':'ARTIFACT_DRAFT_READY'" in vs: findings.append({'severity':'P0','kind':'CONCEPT_SEARCH_STILL_CLAIMS_ARTIFACT_DRAFT'})

    # Required v7.1 authorities
    required=[
      '01_ACTIVE_RUNTIME/78_V7_1_ARTIFACT_INTELLIGENCE_BRAIN_EXECUTION_AND_USER_VISIBLE_DELIVERY_LAW.md',
      '05_WORKFLOW_ENGINE/24_V7_1_RFP_SUMMARY_ARTIFACT_DELIVERY_WORKFLOW.md',
      '07_GOVERNANCE_AND_QA/81_V7_1_ACTUAL_PIXEL_QA_CLOSED_LOOP_AND_GOLDEN_ACCEPTANCE.md'
    ]
    for r in required:
        if r not in manifest: findings.append({'severity':'P0','kind':'V7_1_AUTHORITY_NOT_IN_MANIFEST','file':r})

    p0=[f for f in findings if f['severity']=='P0']; p1=[f for f in findings if f['severity']=='P1']
    out={'suite':'Rashad v7.1 Full Line Conflict Audit','status':'PASS' if not p0 and not p1 else 'FAIL','stats':stats,'manifest_authorities':len(manifest),'p0_count':len(p0),'p1_count':len(p1),'findings':findings}
    dest=QA/'Certification/FULL_LINE_CONFLICT_AUDIT_V7_1.json'; dest.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:out[k] for k in ('suite','status','stats','manifest_authorities','p0_count','p1_count')},ensure_ascii=False,indent=2))
    if findings:
        print(json.dumps(findings[:40],ensure_ascii=False,indent=2))
    return 0 if out['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
