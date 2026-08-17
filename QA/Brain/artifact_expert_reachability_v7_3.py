#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/'Rashad/Brain/runtime'))
from brain.artifact_council_runtime import REG,COUNCILS,_panel_roles
miss=[]; tested=0
for r in REG['roles']:
    rid=r['id']; councils=[r['home_council']]+list(r.get('secondary_councils') or []); ok=False
    for cid in councils:
        if cid in COUNCILS and rid in COUNCILS[cid]['roles']:
            panel=_panel_roles(cid,{}, {'requested_artifact_role_ids':[rid]}); tested+=1
            if rid in panel: ok=True; break
    if not ok: miss.append(rid)
out={'suite':'Artifact Expert Reachability v7.3','status':'PASS' if not miss else 'FAIL','registered_roles':len(REG['roles']),'tested_routes':tested,'unreachable':miss}
(ROOT/'QA/Certification/ARTIFACT_EXPERT_REACHABILITY_V7_3.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)); print(json.dumps(out,ensure_ascii=False,indent=2));raise SystemExit(0 if out['status']=='PASS' else 1)
