#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse,json,sys,hashlib
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Rashad/Brain/runtime'))
from brain.product_inspector import inspect_product

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def one(path):
    p=Path(path)
    if not p.exists(): return {'path':str(p),'status':'NOT_FOUND','blockers':['ENGAGEMENT_ARTIFACT_NOT_FOUND']}
    r=inspect_product(p)
    return {
      'path':str(p),'name':p.name,'sha256':sha(p),'bytes':p.stat().st_size,
      'acceptance_status':r.get('status'),'page_count':r.get('page_count'),
      'format':r.get('format'),'blockers':r.get('blockers',[]),'warnings':r.get('warnings',[]),
      'stats':r.get('stats'),'diversity':r.get('diversity'),
      'rule':'Engagement acceptance is measured on the actual supplied artifact bytes, never inferred from framework fixtures.'
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('artifacts',nargs='+'); ap.add_argument('--expect',choices=['PASS','BLOCKED','ANY'],default='ANY'); ap.add_argument('--out')
    a=ap.parse_args(); rows=[one(x) for x in a.artifacts]
    ok=all(r.get('acceptance_status') in ({a.expect} if a.expect!='ANY' else {'PASS','BLOCKED'}) for r in rows)
    out={'suite':'Rashad v7.3 Actual Engagement Artifact Acceptance','status':'PASS' if ok else 'FAIL','expected':a.expect,'artifact_count':len(rows),'artifacts':rows}
    target=Path(a.out) if a.out else ROOT/'QA/Certification/ENGAGEMENT_ARTIFACT_ACCEPTANCE_V7_3.json'; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if ok else 2
if __name__=='__main__': raise SystemExit(main())
