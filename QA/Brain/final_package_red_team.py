#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib, json, re, sys, subprocess, os, shutil

ROOT=Path(__file__).resolve().parents[2]
RASHAD=ROOT/'Rashad'; QA=ROOT/'QA'; SK=RASHAD/'Skill'; QB=QA/'Brain'; RT=QA/'Runtime'
sys.path.insert(0,str(RASHAD/'Brain/runtime'))
# Start from a clean source tree; tests are executed with bytecode writes disabled.
for d in ROOT.rglob('__pycache__'):
    if d.is_dir(): shutil.rmtree(d, ignore_errors=True)
for f in ROOT.rglob('*.pyc'):
    try: f.unlink()
    except OSError: pass
SUBENV=dict(os.environ); SUBENV['PYTHONDONTWRITEBYTECODE']='1'
results=[]
def add(name,ok,detail=None): results.append({'attack':name,'status':'PASS' if ok else 'FAIL','detail':detail})
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

skill_manifest=json.loads((SK/'ACTIVE_AUTHORITY_MANIFEST.json').read_text(encoding='utf-8'))

add('top_level_exactly_Rashad_and_QA', {p.name for p in ROOT.iterdir() if p.is_dir()}=={'Rashad','QA'}, sorted(p.name for p in ROOT.iterdir()))
add('skill_v7_1_current', 'v7.1.0' in (SK/'VERSION.md').read_text(encoding='utf-8',errors='ignore'))
add('skill_current_certification_harness_v71', skill_manifest.get('certification_harness')=='tests/skill_certification/verify_skill_v7_1.py' and 'tests/skill_certification/red_team_skill_v7_1.py' in skill_manifest.get('certification_harnesses',[]), {'certification_harness':skill_manifest.get('certification_harness'),'certification_harnesses':skill_manifest.get('certification_harnesses')})
# protected corpus counts
prompts=list((SK/'02_IMMUTABLE_AUTHORITIES/RETRIEVAL/PROMPTS').glob('R-*.md'))
scopes=list((SK/'02_IMMUTABLE_AUTHORITIES/RETRIEVAL/SCOPES').glob('*.md'))
maps=list((SK/'02_IMMUTABLE_AUTHORITIES/RETRIEVAL/MAPPINGS').glob('*.md'))
add('protected_prompt_count_388',len(prompts)==388,len(prompts))
add('protected_scope_count_96',len(scopes)==96,len(scopes))
add('protected_mapping_count_96',len(maps)==96,len(maps))
# protected hashes
ph=json.loads((SK/'PROTECTED_CORPUS_HASHES.json').read_text(encoding='utf-8'))
bad=[]
for rel,expected in ph['files'].items():
    p=SK/rel
    if not p.exists() or sha(p)!=expected: bad.append(rel)
add('protected_hashes_exact',not bad,bad[:10])
# brain councils
bc=json.loads((RASHAD/'Brain/runtime/brain/contracts/cognitive_councils_v1.json').read_text(encoding='utf-8'))
add('rashad_brain_16_councils',len(bc.get('councils',[]))==16,len(bc.get('councils',[])))
qc=json.loads((QB/'councils.json').read_text(encoding='utf-8'))
add('qa_brain_14_councils',len(qc.get('councils',[]))==14,len(qc.get('councils',[])))
add('qa_brain_actual_pixel_council_present',any(c.get('id')=='Q11_ACTUAL_PIXEL_PRODUCT_REVIEW' for c in qc.get('councils',[])))
add('qa_brain_artifact_skeptic_council_present',any(c.get('id')=='Q12_EXECUTIVE_SIMPLICITY_ARTIFACT_SKEPTIC' for c in qc.get('councils',[])))
# no hardcoded H1 winner in canonical production visual search
prod=(RASHAD/'Brain/runtime/brain/visual_search.py').read_text(encoding='utf-8')+'\n'+(RASHAD/'Brain/runtime/artifact/exhibit_engine.py').read_text(encoding='utf-8')
add('no_hardcoded_H1_winner', not re.search(r"winner\s*['\"]?\s*[:=]\s*['\"]H1['\"]",prod), None)
add('winner_requires_independent_judgment','ALL_CANDIDATES_REQUIRE_INDEPENDENT_JUDGMENT' in prod)
# Artifact Brain v3 checks
ab=json.loads((RASHAD/'Brain/config/artifact_brain_expert_universe_v3.json').read_text(encoding='utf-8'))
add('artifact_brain_v3_20_councils',len(ab.get('councils',[]))==20,len(ab.get('councils',[])))
add('artifact_brain_v3_large_expert_universe',len(ab.get('roles',[]))>=70,len(ab.get('roles',[])))
from brain.artifact_brain import STRATEGIES
add('artifact_strategy_registry_matches_runtime',set(ab.get('communication_strategy_universe',[]))==set(STRATEGIES) and len(STRATEGIES)==24,{'registry':sorted(ab.get('communication_strategy_universe',[])),'runtime':sorted(STRATEGIES)})
vs=(RASHAD/'Brain/runtime/brain/visual_search.py').read_text(encoding='utf-8')
add('artifact_search_uses_communication_strategy_brain','generate_communication_hypotheses' in vs and 'artifact_run(' not in vs, None)
add('actual_output_qa_runtime_present',(RASHAD/'Brain/runtime/brain/actual_output_qa.py').exists(),None)
manifest=json.loads((SK/'ACTIVE_AUTHORITY_MANIFEST.json').read_text(encoding='utf-8'))
add('artifact_brain_constitution_is_global','03_ARTIFACT_ENGINE/145_V7_0_2_CONSULTING_ARTIFACT_EXHIBIT_BRAIN_CONSTITUTION.md' in manifest.get('global_authorities',[]),None)
add('v71_delivery_authorities_present',all(x in manifest.get('global_authorities',[]) for x in ['01_ACTIVE_RUNTIME/78_V7_1_ARTIFACT_INTELLIGENCE_BRAIN_EXECUTION_AND_USER_VISIBLE_DELIVERY_LAW.md','05_WORKFLOW_ENGINE/24_V7_1_RFP_SUMMARY_ARTIFACT_DELIVERY_WORKFLOW.md','07_GOVERNANCE_AND_QA/81_V7_1_ACTUAL_PIXEL_QA_CLOSED_LOOP_AND_GOLDEN_ACCEPTANCE.md']),None)

# QA cannot own release
add('qa_has_no_rashad_release_module',not (RT/'brain/release.py').exists())
qapy='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in QA.rglob('*.py') if 'Certification' not in p.parts)
# allowed string references for detecting forbidden output; reject actual assignment patterns in QA runtime/brain
bad_release=[]
for p in list((RT).rglob('*.py'))+list(QB.rglob('*.py')):
    txt=p.read_text(encoding='utf-8',errors='ignore')
    if re.search(r"final_verdict['\"]?\s*[:=]\s*['\"]RELEASED['\"]",txt): bad_release.append(str(p.relative_to(ROOT)))
add('qa_cannot_emit_RELEASED',not bad_release,bad_release)
add('legacy_release_blocked','LEGACY_RELEASE_AUTHORITY_DISABLED_USE_BRAIN_RELEASE' in (RT/'rashad_qa.py').read_text(encoding='utf-8'))
# no stale absolute build path in production sources
abs_hits=[]
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.py','.md','.json'}:
        txt=p.read_text(encoding='utf-8',errors='ignore')
        stale='/mnt/data/'+'rashad_brain_build'
        if stale in txt: abs_hits.append(str(p.relative_to(ROOT)))
add('no_stale_absolute_runtime_path',not abs_hits,abs_hits[:20])
# owner terminology executable test
cp=subprocess.run([sys.executable,str(SK/'tests/skill_certification/test_owner_arabic_executive_language_v7_0_2.py')],cwd=SK,capture_output=True,text=True,env=SUBENV)
add('owner_arabic_language_gate',cp.returncode==0,cp.stdout.strip()[-300:])
# QA brain fail closed / ceiling
cp=subprocess.run([sys.executable,str(QB/'run_certification.py')],cwd=QB,capture_output=True,text=True,env=SUBENV)
add('qa_brain_certification',cp.returncode==0,cp.stdout.strip()[-300:])
# Brain certification
cp=subprocess.run([sys.executable,str(RASHAD/'Brain/runtime/brain/tests/run_brain_certification.py')],cwd=RASHAD/'Brain/runtime',capture_output=True,text=True,env=SUBENV)
add('rashad_brain_certification',cp.returncode==0,cp.stdout.strip()[-300:])
# no generated caches or nested zips
cache=[str(p.relative_to(ROOT)) for p in ROOT.rglob('*.pyc')]
add('no_pyc_cache',not cache,cache[:20])
nested=[str(p.relative_to(ROOT)) for p in ROOT.rglob('*.zip')]
fv=(QA/'FINAL_VERIFY.py').read_text(encoding='utf-8')
add('final_verifier_file_logged_single_run_resilient',all(x in fv for x in ['fcntl.flock','stdout=fo','stderr=fe','LOGDIR.mkdir(parents=True,exist_ok=True)']) and 'capture_output=True' not in fv,None)
rv3=(RT/'run_regression_v3.py').read_text(encoding='utf-8'); rv31=(RT/'run_regression_v31.py').read_text(encoding='utf-8')
add('regression_outputs_cleaned_each_run',"shutil.rmtree(HERE/'_regression', ignore_errors=True)" in rv3 and "shutil.rmtree(HERE/'_regression_v31', ignore_errors=True)" in rv31,None)
add('no_nested_zip_packages',not nested,nested[:20])

out={'suite':'Rashad OS Final Package Adversarial Red Team','status':'PASS' if all(x['status']=='PASS' for x in results) else 'FAIL','passed':sum(x['status']=='PASS' for x in results),'total':len(results),'attacks':results}
(Path(__file__).resolve().parents[1]/'Certification/FINAL_PACKAGE_RED_TEAM_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
raise SystemExit(0 if out['status']=='PASS' else 1)
