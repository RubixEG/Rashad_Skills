#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/'Rashad/Brain/runtime'))
from brain.exact_handoff import verify_exact_artifact_handoff
F=ROOT/'QA/Runtime/fixtures/incidents/I16_WRONG_ARTIFACT_HANDOFF_20260817'; OUT=ROOT/'QA/Certification/INCIDENT_P0_WRONG_ARTIFACT_HANDOFF_20260817_RESULTS.json'
def main():
    r=verify_exact_artifact_handoff(F/'bad_delivered_14_slide_deck.pptx',F/'bad_delivery_dossier_24_page.json',trace_path=F/'bad_trace_24_page_claim.md')
    required={'DELIVERED_PPTX_SHA_MISMATCH_DOSSIER','DELIVERED_SLIDE_COUNT_MISMATCH_DOSSIER_PAGES','PIXEL_REVIEW_COUNT_MISMATCH_DELIVERED_SLIDES','PRODUCTION_RENDER_COUNT_MISMATCH_DELIVERED_SLIDES','FINAL_TRACE_DESCRIBES_DIFFERENT_PAGE_COUNT_THAN_DELIVERED_FILE','IMAGE_LED_DECLARED_BUT_IMAGES_APPEAR_LOGO_ONLY'}
    ok=r.get('status')=='BLOCK_HANDOFF' and required<=set(r.get('blockers',[])) and r.get('slide_count')==14 and r.get('dossier_page_count')==24
    out={'suite':'I16 WRONG_ARTIFACT_HANDOFF_AFTER_QA Permanent Regression','status':'PASS' if ok else 'FAIL','incident':'14-slide delivered file vs 24-page QA dossier + wrong SHA + logo-only image path','required_blockers':sorted(required),'actual_blockers':r.get('blockers',[]),'verification':r}; OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps({'suite':out['suite'],'status':out['status'],'actual_blockers':out['actual_blockers']},ensure_ascii=False,indent=2)); return 0 if ok else 2
if __name__=='__main__': raise SystemExit(main())
