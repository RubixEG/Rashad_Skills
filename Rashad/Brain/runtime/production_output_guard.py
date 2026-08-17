#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from brain.artifact_gate import guard_composer

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--state',required=True); ap.add_argument('--requested',default='USER_VISIBLE_ARTIFACT_DRAFT',choices=['CONTENT_DRAFT','INTERNAL_CONCEPT_DRAFT','ARTIFACT_DRAFT','USER_VISIBLE_ARTIFACT_DRAFT','RELEASE_CANDIDATE','RELEASED']); ap.add_argument('--out'); a=ap.parse_args()
    s=json.loads(Path(a.state).read_text(encoding='utf-8')); r=guard_composer(s,a.requested)
    if a.out: Path(a.out).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(r,ensure_ascii=False,indent=2)); return 0 if r['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
