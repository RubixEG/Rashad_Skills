#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from qa.gates_v26 import g36_visible_language_purity
prof=json.loads((ROOT/'config/profile_v4.json').read_text())

def pd(texts):
    return {'texts':[{'idx':i,'text':t,'data':{'directionality':'ISOLATED' if iso else ''}} for i,(t,iso) in enumerate(texts)],'els':[],'rect':{'x':0,'y':0,'w':1920,'h':1080,'r':1920,'b':1080}}

def chk(name,texts,expect):
    r=g36_visible_language_purity(pd(texts),prof,{},{}); ok=r['status']==expect
    return {'name':name,'status':'PASS' if ok else 'FAIL','observed':r['status'],'violations':r.get('violations')}
rows=[
 chk('arabic_technical_tokens_allowed',[('متطلبات ISO و API و SLA',False),('١٢ شهرًا',False)],'PASS'),
 chk('internal_ready_blocked',[('الحالة READY والخطوة NEXT',False)],'FAIL'),
 chk('debug_string_blocked',[('اختبار v7.7 Test',False)],'FAIL'),
 chk('pure_latin_client_prose_blocked',[('Executive Summary Draft',False),('ملخص تنفيذي',False)],'FAIL'),
 chk('western_numeral_in_arabic_blocked',[('مدة التنفيذ 24 شهرًا',False)],'FAIL'),
 chk('isolated_technical_numeric_allowed',[('مرجع API-2026',True),('تفاصيل فنية',False)],'PASS'),
]
out={'suite':'Arabic Visible Language Purity v7.3','status':'PASS' if all(x['status']=='PASS' for x in rows) else 'FAIL','passed':sum(x['status']=='PASS' for x in rows),'total':len(rows),'tests':rows}
(ROOT.parent/'Certification/ARABIC_VISIBLE_LANGUAGE_PURITY_V7_3.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 1)
