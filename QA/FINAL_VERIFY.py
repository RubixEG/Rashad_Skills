#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import fcntl, hashlib, json, os, signal, subprocess, sys, time

ROOT=Path(__file__).resolve().parents[1]
RASHAD=ROOT/'Rashad'; QA=ROOT/'QA'; CERT=QA/'Certification'; CERT.mkdir(exist_ok=True)
env=dict(os.environ); env['PYTHONDONTWRITEBYTECODE']='1'

# Single-run lock: lock the Certification DIRECTORY inode itself.
# A removable lock file is unsafe because cleanup can unlink it while a process
# still holds the old inode, allowing a second verifier to lock a new file.
LOCK_FD=os.open(str(CERT), os.O_RDONLY)
try:
    fcntl.flock(LOCK_FD, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    print(json.dumps({'suite':'Rashad OS Final Verification v7.3 Production Organ + Council-Supervised Engagement Acceptance + Exact Handoff','status':'BLOCKED','reason':'FINAL_VERIFY_ALREADY_RUNNING'},indent=2))
    os.close(LOCK_FD)
    raise SystemExit(3)

PROGRESS_LOG=CERT/'FINAL_VERIFY_PROGRESS.log'
LOGDIR=CERT/'suite_logs'; LOGDIR.mkdir(exist_ok=True)
CHECKPOINT=CERT/'FINAL_VERIFY_CHECKPOINT.json'
RESUME=os.getenv('RASHAD_FINAL_VERIFY_RESUME','0')=='1'

def source_fingerprint():
    # Bind resume checkpoints to executable/canonical source, not test outputs.
    h=hashlib.sha256(); files=[]
    for base in (RASHAD,QA):
        for f in base.rglob('*'):
            if not f.is_file(): continue
            rel=f.relative_to(ROOT).as_posix()
            parts=f.parts
            if 'Certification' in parts or '__pycache__' in parts or any(x.startswith('_regression') for x in parts): continue
            if f.suffix in {'.pyc','.png','.jpg','.jpeg','.pdf','.pptx'}: continue
            # Runtime-produced result files are evidence outputs, not source inputs.
            up=f.name.upper()
            if up.endswith('_RESULTS.JSON') or up.endswith('_RESULT.JSON') or up.startswith('REGRESSION_') and up.endswith('.JSON'): continue
            if f.suffix.lower() not in {'.py','.md','.json','.html','.js','.css'}: continue
            files.append((rel,f))
    for rel,f in sorted(files):
        h.update(rel.encode()); h.update(b'\0'); h.update(hashlib.sha256(f.read_bytes()).digest())
    return h.hexdigest()

SOURCE_FINGERPRINT=source_fingerprint()
checkpoint={'schema_version':'1.0','source_fingerprint':SOURCE_FINGERPRINT,'completed':{},'active':None}
if RESUME and CHECKPOINT.exists():
    try:
        old=json.loads(CHECKPOINT.read_text(encoding='utf-8'))
        if old.get('source_fingerprint')==SOURCE_FINGERPRINT:
            checkpoint=old
        else:
            RESUME=False
    except Exception:
        RESUME=False
if not RESUME:
    PROGRESS_LOG.write_text('',encoding='utf-8')
    CHECKPOINT.write_text(json.dumps(checkpoint,indent=2),encoding='utf-8')
else:
    # If the host interrupted a suite, kill any stale process group before re-running it.
    active=checkpoint.get('active') or {}
    pid=active.get('pid')
    if isinstance(pid,int) and pid>1:
        try: os.killpg(pid,signal.SIGKILL)
        except (ProcessLookupError,PermissionError): pass

def progress(msg:str):
    with PROGRESS_LOG.open('a',encoding='utf-8') as f:
        f.write(msg+'\n'); f.flush()

def save_checkpoint():
    tmp=CHECKPOINT.with_suffix('.tmp')
    tmp.write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2),encoding='utf-8')
    tmp.replace(CHECKPOINT)

def item(name, cmd, cwd, phase): return {'name':name,'cmd':cmd,'cwd':cwd,'phase':phase}

ITEMS=[
 # P1 — current static/authority truth
 item('skill_v7_3',[sys.executable,str(RASHAD/'Skill/tests/skill_certification/verify_skill_v7_3.py')],RASHAD/'Skill','P1_STATIC_AUTHORITY'),
 item('skill_red_team_v7_3',[sys.executable,str(RASHAD/'Skill/tests/skill_certification/red_team_skill_v7_3.py')],RASHAD/'Skill','P1_STATIC_AUTHORITY'),
 item('owner_language_red_team',[sys.executable,str(RASHAD/'Skill/tests/skill_certification/red_team_owner_arabic_language_v7_0_2.py')],RASHAD/'Skill','P1_STATIC_AUTHORITY'),
 item('a_to_z_final_v7_3',[sys.executable,str(QA/'Brain/a_to_z_final_brain_audit_v7_3.py')],QA/'Brain','P1_STATIC_AUTHORITY'),
 item('full_line_conflict_v7_3',[sys.executable,str(QA/'Brain/full_line_conflict_audit_v7_3.py')],QA/'Brain','P1_STATIC_AUTHORITY'),

 # P2 — Brain, councils, Host-Native, Artifact cognition
 item('rashad_brain',[sys.executable,str(RASHAD/'Brain/runtime/brain/tests/run_brain_certification.py')],RASHAD/'Brain/runtime','P2_BRAIN'),
 item('rfp_summary_execution',[sys.executable,str(RASHAD/'Brain/runtime/brain/tests/run_rfp_summary_execution_certification.py')],RASHAD/'Brain/runtime','P2_BRAIN'),
 item('rfp_summary_red_team',[sys.executable,str(RASHAD/'Brain/runtime/brain/tests/red_team_rfp_summary_execution.py')],RASHAD/'Brain/runtime','P2_BRAIN'),
 item('brain_v3_3_artifact_admission_regression',[sys.executable,str(RASHAD/'Brain/runtime/brain/tests/run_final_brain_upgrade_certification.py')],RASHAD/'Brain/runtime','P2_BRAIN'),
 item('brain_v3_3_artifact_red_team_regression',[sys.executable,str(RASHAD/'Brain/runtime/brain/tests/red_team_final_brain_upgrade.py')],RASHAD/'Brain/runtime','P2_BRAIN'),
 # v3.3 full certification is lineage-only because its content-hash structural-signature expectation is intentionally superseded by v4 visual-memory anti-template logic.
 item('artifact_brain_v3_3_red_team_regression',[sys.executable,str(RASHAD/'Brain/runtime/brain/tests/red_team_artifact_brain_v3.py')],RASHAD/'Brain/runtime','P2_BRAIN'),
 item('artifact_brain_v3_3_stress_regression',[sys.executable,str(RASHAD/'Brain/runtime/brain/tests/run_artifact_brain_v3_stress_quality.py')],RASHAD/'Brain/runtime','P2_BRAIN'),
 item('brain_coherence_v7_2_inherited',[sys.executable,str(QA/'Brain/brain_coherence_audit_v7_2.py')],QA/'Brain','P2_BRAIN'),
 item('brain_coherence_stress_v7_2_inherited',[sys.executable,str(QA/'Brain/stress_brain_coherence_v7_2.py')],QA/'Brain','P2_BRAIN'),
 item('host_native_brain_execution',[sys.executable,str(RASHAD/'Brain/runtime/brain/tests/run_host_native_execution_certification.py')],RASHAD/'Brain/runtime','P2_BRAIN'),
 item('host_native_brain_red_team',[sys.executable,str(RASHAD/'Brain/runtime/brain/tests/red_team_host_native_execution.py')],RASHAD/'Brain/runtime','P2_BRAIN'),
 item('host_native_execution_stress',[sys.executable,str(QA/'Brain/stress_host_native_execution_v7_2.py')],QA/'Brain','P2_BRAIN'),
 item('artifact_brain_v7_3_regression',[sys.executable,str(QA/'Brain/artifact_brain_regression_v7_3.py')],QA/'Brain','P2_BRAIN'),
 item('artifact_expert_reachability_v7_3',[sys.executable,str(QA/'Brain/artifact_expert_reachability_v7_3.py')],QA/'Brain','P2_BRAIN'),

 # P3 — deterministic QA + Arabic + threshold/stress governance
 item('qa_deterministic',[sys.executable,str(QA/'Runtime/run_certification_v4.py')],QA/'Runtime','P3_QA_RUNTIME'),
 item('qa_regression_v3',[sys.executable,str(QA/'Runtime/run_regression_v3.py')],QA/'Runtime','P3_QA_RUNTIME'),
 item('qa_regression_v31',[sys.executable,str(QA/'Runtime/run_regression_v31.py')],QA/'Runtime','P3_QA_RUNTIME'),
 item('qa_arabic_visible_language_v7_3',[sys.executable,str(QA/'Runtime/qa_v4/test_arabic_visible_language_purity_v7_3.py')],QA/'Runtime','P3_QA_RUNTIME'),
 item('qa_stress_legacy',[sys.executable,str(QA/'Runtime/run_stress_v3.py')],QA/'Runtime','P3_QA_RUNTIME'),
 item('threshold_binding_v7_3',[sys.executable,str(QA/'Brain/threshold_binding_audit_v7_3.py')],QA/'Brain','P3_QA_RUNTIME'),
 item('stress_contract_parity_v7_3',[sys.executable,str(QA/'Brain/stress_contract_parity_v7_3.py')],QA/'Brain','P3_QA_RUNTIME'),

 # P4 — production organ, actual-output QA, delivery closure
 item('qa_brain',[sys.executable,str(QA/'Brain/run_certification.py')],QA/'Brain','P4_PRODUCTION_DELIVERY'),
 item('host_native_qa',[sys.executable,str(QA/'Brain/host_native_qa_certification.py')],QA/'Brain','P4_PRODUCTION_DELIVERY'),
 item('user_visible_delivery',[sys.executable,str(QA/'Brain/run_v7_2_user_visible_delivery_certification.py')],QA/'Brain','P4_PRODUCTION_DELIVERY'),
 item('delivery_red_team',[sys.executable,str(QA/'Brain/red_team_v7_2_delivery.py')],QA/'Brain','P4_PRODUCTION_DELIVERY'),
 item('exact_handoff_lock',[sys.executable,str(QA/'Brain/handoff_lock_certification_v7_2_1.py')],QA/'Brain','P4_PRODUCTION_DELIVERY'),
 item('wrong_handoff_real_incident',[sys.executable,str(QA/'Brain/incident_p0_wrong_artifact_handoff_20260817.py')],QA/'Brain','P4_PRODUCTION_DELIVERY'),
 item('artifact_stress_quality_v7_3',[sys.executable,str(QA/'Brain/stress_quality_v7_3.py')],QA/'Brain','P4_PRODUCTION_DELIVERY'),
 item('golden_redf_acceptance_inherited',[sys.executable,str(QA/'Brain/golden_redf_acceptance_v7_2.py')],QA/'Brain','P4_PRODUCTION_DELIVERY'),
 item('visual_production_v7_3',[sys.executable,str(QA/'Brain/visual_production_certification_v7_3.py')],QA/'Brain','P4_PRODUCTION_DELIVERY'),
 item('visual_production_red_team_v7_3',[sys.executable,str(QA/'Brain/red_team_visual_production_v7_3.py')],QA/'Brain','P4_PRODUCTION_DELIVERY'),
 item('deck_continuity_v7_3',[sys.executable,str(QA/'Brain/deck_continuity_certification_v7_3.py')],QA/'Brain','P4_PRODUCTION_DELIVERY'),
 item('governed_production_delivery_v7_3',[sys.executable,str(QA/'Brain/governed_production_delivery_v7_3.py')],QA/'Brain','P4_PRODUCTION_DELIVERY'),

 # P5 — incidents, actual-engagement evidence, remediation and package attacks
 item('incident_regression_v7_3',[sys.executable,str(QA/'Brain/incident_regression_v7_3.py')],QA/'Brain','P5_INCIDENT_PACKAGE'),
 item('engagement_acceptance_evidence_v7_3',[sys.executable,str(QA/'Brain/engagement_acceptance_evidence_verifier_v7_3.py')],QA/'Brain','P5_INCIDENT_PACKAGE'),
 item('remediation_matrix_v7_3',[sys.executable,str(QA/'Brain/remediation_matrix_v7_3.py')],QA/'Brain','P5_INCIDENT_PACKAGE'),
 item('final_red_team_v7_3',[sys.executable,str(QA/'Brain/final_package_red_team_v7_3.py')],QA/'Brain','P5_INCIDENT_PACKAGE'),
]

def clean_transient_python_caches():
    # Certification suites may import package modules that emit interpreter caches
    # despite caller hygiene. These files are reproducible execution by-products,
    # never package evidence. Remove them immediately before cleanliness/package audits.
    for d in list(ROOT.rglob('__pycache__')):
        if d.is_dir():
            import shutil
            shutil.rmtree(d, ignore_errors=True)
    for f in list(ROOT.rglob('*.pyc')):
        try: f.unlink()
        except FileNotFoundError: pass

def tail(path:Path,n=2600):
    try: return path.read_text(encoding='utf-8',errors='ignore')[-n:]
    except Exception: return ''

def run_one(it):
    start=time.monotonic(); name=it['name']
    if name in {'a_to_z_final_v7_3','full_line_conflict_v7_3','final_red_team_v7_3'}:
        clean_transient_python_caches()
    progress(f"TEST_START {it['phase']} {name}")
    LOGDIR.mkdir(parents=True,exist_ok=True)
    outp=LOGDIR/(name+'.stdout.txt'); errp=LOGDIR/(name+'.stderr.txt')
    try:
        with outp.open('w',encoding='utf-8') as fo, errp.open('w',encoding='utf-8') as fe:
            proc=subprocess.Popen(it['cmd'],cwd=it['cwd'],env=env,stdout=fo,stderr=fe,text=True,start_new_session=True)
            checkpoint['active']={'name':name,'phase':it['phase'],'pid':proc.pid,'started_monotonic':start}
            save_checkpoint()
            try:
                returncode=proc.wait(timeout=180)
            except subprocess.TimeoutExpired:
                try: os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError: pass
                proc.wait(timeout=5)
                raise
            finally:
                # A suite may spawn grandchildren (browser/render workers) that outlive the parent.
                # Kill the isolated process group after the suite returns so no descendant can contaminate the next suite.
                try: os.killpg(proc.pid, signal.SIGTERM)
                except ProcessLookupError: pass
        status='PASS' if returncode==0 else 'FAIL'
        r={'name':name,'phase':it['phase'],'status':status,'exit_code':returncode,'duration_sec':round(time.monotonic()-start,3),'stdout_tail':tail(outp),'stderr_tail':tail(errp),'stdout_log':str(outp.relative_to(ROOT)),'stderr_log':str(errp.relative_to(ROOT))}
    except subprocess.TimeoutExpired:
        r={'name':name,'phase':it['phase'],'status':'FAIL','exit_code':124,'duration_sec':round(time.monotonic()-start,3),'stdout_tail':tail(outp),'stderr_tail':'SUITE_TIMEOUT_180_SECONDS','stdout_log':str(outp.relative_to(ROOT)),'stderr_log':str(errp.relative_to(ROOT))}
    progress(f"TEST_END {it['phase']} {name} {r['status']} {r['duration_sec']}s")
    checkpoint['active']=None
    checkpoint.setdefault('completed',{})[name]=r
    save_checkpoint()
    return r

results=[]
for it in ITEMS:
    prev=(checkpoint.get('completed') or {}).get(it['name'])
    if RESUME and prev and prev.get('status')=='PASS':
        r=prev
        progress(f"TEST_RESUME_SKIP {it['phase']} {it['name']} PASS source={SOURCE_FINGERPRINT[:12]}")
    else:
        r=run_one(it)
    results.append(r)
    if r['status']!='PASS':
        progress('FAIL_CLOSED_STOP '+r['name'])
        break
seen={r['name'] for r in results}
for it in ITEMS:
    if it['name'] not in seen:
        results.append({'name':it['name'],'phase':it['phase'],'status':'NOT_RUN_AFTER_FAILURE','exit_code':None,'duration_sec':0,'stdout_tail':'','stderr_tail':''})
passed=sum(r['status']=='PASS' for r in results); all_pass=passed==len(ITEMS)
phase_names=[]
for it in ITEMS:
    if it['phase'] not in phase_names: phase_names.append(it['phase'])
phases=[]
for ph in phase_names:
    rr=[r for r in results if r['phase']==ph]
    phases.append({'phase':ph,'status':'PASS' if rr and all(r['status']=='PASS' for r in rr) else 'FAIL','passed':sum(r['status']=='PASS' for r in rr),'total':len(rr)})
out={'suite':'Rashad OS Final Verification v7.3 Production Organ + Council-Supervised Engagement Acceptance + Exact Handoff','status':'PASS' if all_pass else 'FAIL','passed':passed,'total':len(ITEMS),'execution':'PROCESS_GROUP_ISOLATED_ORDERED_FILE_LOGGED_FAIL_CLOSED','suite_timeout_seconds':180,'source_fingerprint':SOURCE_FINGERPRINT,'resumed':RESUME,'phases':phases,'results':results}
(CERT/'FINAL_VERIFY_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'suite':out['suite'],'status':out['status'],'passed':out['passed'],'total':out['total'],'execution':out['execution'],'duration_sec':round(sum(r['duration_sec'] for r in results),3),'phases':phases,'tests':[{'name':r['name'],'status':r['status'],'sec':r['duration_sec']} for r in results]},ensure_ascii=False,indent=2))
raise SystemExit(0 if all_pass else 1)
