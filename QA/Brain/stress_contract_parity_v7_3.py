#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'QA/Runtime'))
from qa.stress_and_safety import STRESS_MODES
from qa_v4.taxonomy_runtime import load,STRESS

def main():
    profile=json.loads((ROOT/'QA/Runtime/config/profile_v4.json').read_text())
    core=load(STRESS).get('required_mutations',[])
    arabic=profile.get('thresholds',{}).get('stress_arabic_modes',[])
    blockers=[]
    if len(core)!=20:blockers.append({'kind':'CORE_STRESS_MATRIX_NOT_20','actual':len(core)})
    if len(set(x.get('id') for x in core))!=len(core):blockers.append({'kind':'CORE_STRESS_DUPLICATE_IDS'})
    missing=[m for m in arabic if m not in STRESS_MODES]
    if missing:blockers.append({'kind':'ARABIC_STRESS_MODE_NOT_EXECUTABLE','modes':missing})
    if len(arabic)<6:blockers.append({'kind':'ARABIC_STRESS_POLICY_INCOMPLETE','actual':len(arabic),'minimum':6})
    # Release HTML harness iterates profile-required modes plus the executable matrix.
    u=(ROOT/'QA/Runtime/qa/unified_html_qa.py').read_text()
    if "stress_arabic_modes" not in u or "required_profile" not in u:blockers.append({'kind':'RELEASE_HARNESS_NOT_BOUND_TO_ARABIC_STRESS_POLICY'})
    sr=(ROOT/'QA/Runtime/qa_v4/stress_runner_final.py').read_text()
    if 'byte change is never a PASS criterion' not in sr or "repair_deleted_node" not in sr:blockers.append({'kind':'REAL_RENDER_REGATE_STRESS_CONTRACT_MISSING'})
    out={'suite':'Rashad v7.3 Stress Contract Parity','status':'PASS' if not blockers else 'FAIL','core_mutations':len(core),'arabic_required_modes':arabic,'executable_arabic_modes':sorted(STRESS_MODES),'total_governed_stress_surface':len(core)+len(set(arabic)),'blockers':blockers}
    (ROOT/'QA/Certification/STRESS_CONTRACT_PARITY_V7_3.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if out['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
