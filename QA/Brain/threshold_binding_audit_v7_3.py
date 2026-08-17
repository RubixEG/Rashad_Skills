#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[2]
PROFILE=ROOT/'QA/Runtime/config/profile_v4.json'
BRAIN=ROOT/'Rashad/Brain/runtime/brain/quality_floors_v7_3.py'
EXCLUDE={Path(__file__).resolve(),PROFILE.resolve()}

def sources():
    for root in [ROOT/'Rashad',ROOT/'QA']:
        for p in root.rglob('*.py'):
            if p.resolve() not in EXCLUDE: yield p

def main():
    prof=json.loads(PROFILE.read_text()); active=prof.get('thresholds',{}); retired=prof.get('retired_thresholds',{})
    corpus=[(p,p.read_text(encoding='utf-8',errors='ignore')) for p in sources()]
    rows=[]; blockers=[]
    for k,v in active.items():
        hits=[str(p.relative_to(ROOT)) for p,s in corpus if re.search(rf"(?<![A-Za-z0-9_]){re.escape(k)}(?![A-Za-z0-9_])",s)]
        ok=bool(hits)
        rows.append({'threshold':k,'value':v,'status':'BOUND' if ok else 'UNBOUND','consumers':hits[:20]})
        if not ok:blockers.append({'kind':'ACTIVE_THRESHOLD_HAS_NO_EXECUTABLE_CONSUMER','threshold':k})
    for k,v in retired.items():
        if v.get('status')!='RETIRED_SUPERSEDED' or not v.get('superseded_by'):
            blockers.append({'kind':'RETIRED_THRESHOLD_WITHOUT_SUPERSESSION_PROOF','threshold':k})
    # Cross-layer parity: these values control both artifact construction and QA/release.
    sys.path.insert(0,str(ROOT/'Rashad/Brain/runtime'))
    from brain.quality_floors_v7_3 import QUALITY_FLOORS
    parity_keys=['dominant_mass_min','dominant_mass_max','artifact_truth_min','ceqs_min','min_pairwise_structural_divergence_critical','target_pairwise_structural_divergence','diagram_ratio_hard_block','safe_area_min_visible_px2','min_type_hierarchy_levels','min_exhibit_hypotheses','min_actual_render_candidates_critical']
    parity=[]
    for k in parity_keys:
        pv=active.get(k); bv=QUALITY_FLOORS.get(k); ok=pv==bv
        parity.append({'threshold':k,'qa_profile':pv,'brain_floor':bv,'status':'PASS' if ok else 'FAIL'})
        if not ok:blockers.append({'kind':'BRAIN_QA_THRESHOLD_SPLIT_BRAIN','threshold':k,'qa':pv,'brain':bv})
    out={'suite':'Rashad v7.3 Active Threshold Binding Audit','status':'PASS' if not blockers else 'FAIL','active_thresholds':len(active),'retired_thresholds':len(retired),'bound':sum(r['status']=='BOUND' for r in rows),'rows':rows,'parity':parity,'blockers':blockers}
    (ROOT/'QA/Certification/THRESHOLD_BINDING_AUDIT_V7_3.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if out['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
