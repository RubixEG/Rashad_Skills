#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from brain.exact_handoff import verify_exact_artifact_handoff,issue_exact_handoff_certificate

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--pptx',required=True); ap.add_argument('--dossier',required=True); ap.add_argument('--trace'); ap.add_argument('--pdf'); ap.add_argument('--certificate-out',required=True); ap.add_argument('--verification-out')
    a=ap.parse_args(); d=json.loads(Path(a.dossier).read_text(encoding='utf-8'))
    v=verify_exact_artifact_handoff(a.pptx,d,trace_path=a.trace,pdf_path=a.pdf)
    if a.verification_out: Path(a.verification_out).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
    c=issue_exact_handoff_certificate(a.pptx,d,trace_path=a.trace,pdf_path=a.pdf)
    Path(a.certificate_out).write_text(json.dumps(c,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'status':c.get('status'),'blockers':c.get('blockers',[]),'pptx_sha256':v.get('pptx_sha256'),'slide_count':v.get('slide_count')},ensure_ascii=False,indent=2))
    return 0 if c.get('status')=='CERTIFIED_FOR_HANDOFF' else 2
if __name__=='__main__': raise SystemExit(main())
