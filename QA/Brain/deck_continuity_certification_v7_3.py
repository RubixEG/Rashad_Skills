#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json,sys,tempfile
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Rashad/Brain/runtime')); sys.path.insert(0,str(ROOT/'QA/Brain'))
from brain.deck_continuity import evaluate_ledger
from production_test_fixtures_v7_3 import build_production_projection,sha256_file

def main():
  with tempfile.TemporaryDirectory() as td:
    pr=build_production_projection(Path(td),['DECISION_LED','CHART_LED','SEQUENCE_LED','ARCHITECTURE_LED'])
    if pr.get('status')!='PASS': raise RuntimeError(pr)
    pages=[]
    for i,p in enumerate(pr['page_images']): pages.append({'page_id':f'P{i+1:02d}','master_path':p,'master_sha256':sha256_file(p),'previous_page_id':f'P{i:02d}' if i else None})
    good=evaluate_ledger({'pages':pages}); bad_hash=[dict(x) for x in pages]; bad_hash[1]['master_sha256']='0'*64; bad1=evaluate_ledger({'pages':bad_hash})
    bad_link=[dict(x) for x in pages]; bad_link[2]['previous_page_id']='WRONG'; bad2=evaluate_ledger({'pages':bad_link})
    checks={'good_sequence_passes':good['status']=='PASS','hash_mutation_blocks':bad1['status']=='FAIL','link_mutation_blocks':bad2['status']=='FAIL'}
    out={'suite':'Rashad v7.3 Deck Continuity Certification','status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'good':good,'hash_attack':bad1,'link_attack':bad2}
    (ROOT/'QA/Certification/DECK_CONTINUITY_CERTIFICATION_V7_3.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if out['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
