#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib,time,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'Rashad/Brain/runtime'))
from brain.deck_continuity import evaluate_ledger

def main():
    ap=argparse.ArgumentParser(description='Deck-level Golden Visual Master continuity QA'); ap.add_argument('ledger',type=Path); ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True); raw=a.ledger.read_text(encoding='utf-8'); obj=json.loads(raw); ts=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    evidence='DCK-'+hashlib.sha256((raw+ts).encode()).hexdigest()[:16].upper(); ev=a.out/evidence; ev.mkdir()
    try:
        core=evaluate_ledger(obj); runtime=None
    except Exception as e:
        core={'status':'NOT_EXECUTED','verdict':'BLOCKED','violations':[],'measurements':[],'thresholds':obj.get('thresholds',{})}; runtime={'type':type(e).__name__,'message':str(e)}
    report={'evidence_id':evidence,'timestamp_utc':ts,'ledger':str(a.ledger),'runtime_error':runtime,**core}
    (ev/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(report,ensure_ascii=False,indent=2)); return 0 if report.get('verdict')=='DECK_CONTINUITY_PASS' else (2 if runtime else 1)
if __name__=='__main__': raise SystemExit(main())
