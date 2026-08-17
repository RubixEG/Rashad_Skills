#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'QA/Certification/ENGAGEMENT_ARTIFACT_ACCEPTANCE_V7_3.json'
checks=[]
def ck(name,ok,detail=None): checks.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
if not p.exists():
 ck('engagement_acceptance_report_exists',False,str(p))
 d={}
else:
 d=json.loads(p.read_text(encoding='utf-8')); ck('engagement_acceptance_report_exists',True)
rows=d.get('artifacts',[])
ck('suite_status_pass',d.get('status')=='PASS',d.get('status'))
ck('actual_artifact_count_at_least_two',len(rows)>=2,len(rows))
ck('all_rows_hash_bound',len(rows)>=2 and all(len(str(r.get('sha256','')))==64 and r.get('bytes',0)>0 for r in rows),[r.get('sha256') for r in rows])
ck('distinct_actual_artifact_hashes',len({r.get('sha256') for r in rows})==len(rows) and len(rows)>=2,[r.get('sha256') for r in rows])
ck('negative_baselines_correctly_blocked',len(rows)>=2 and all(r.get('acceptance_status')=='BLOCKED' and r.get('blockers') for r in rows),[(r.get('name'),r.get('blockers')) for r in rows])
ck('actual_bytes_rule_present',len(rows)>=2 and all('actual supplied artifact bytes' in r.get('rule','') for r in rows))
# Expected current negative-baseline classes: one semantic/native deck with composition failures, one raster-only projection without semantic master proof.
blockers=[set(r.get('blockers',[])) for r in rows]; blocker_lists=[sorted(x) for x in blockers]
ck('composition_failure_baseline_present',any('DECK_DISTINCT_COMPOSITION_FLOOR_NOT_MET' in b or 'DOMINANT_MASS_FLOOR_NOT_MET' in b or 'EQUAL_CARD_GRID_OVERUSE' in b for b in blockers),blocker_lists)
ck('raster_only_semantic_master_block_present',any('RASTER_ONLY_PROJECTION_WITHOUT_HASH_BOUND_SEMANTIC_MASTER_PROOF' in b for b in blockers),blocker_lists)
out={'suite':'Rashad v7.3 Embedded Actual-Engagement Acceptance Evidence Verifier','status':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL','passed':sum(x['status']=='PASS' for x in checks),'total':len(checks),'checks':checks}
(ROOT/'QA/Certification/ENGAGEMENT_ACCEPTANCE_EVIDENCE_VERIFIER_V7_3.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 2)
