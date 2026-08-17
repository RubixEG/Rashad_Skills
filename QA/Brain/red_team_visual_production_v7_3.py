#!/usr/bin/env python3
from pathlib import Path
import json,sys,tempfile
ROOT=Path(__file__).resolve().parents[2]; BR=ROOT/'Rashad/Brain/runtime'; sys.path.insert(0,str(BR))
from brain.production.image_provider import HostNativeImageProvider
from brain.composition_spec import build_page_composition_spec
from brain.spec_divergence import evaluate_set
from brain.product_inspector import inspect_product
from brain.imagery_director import validate_image_plate

def t(name,blocked,detail=None): return {'name':name,'status':'PASS' if blocked else 'FAIL','detail':detail}
rows=[]
# Forged image proof must fail before use.
def fake(req): return {'status':'PASS','image_path':'/no/such/file.png','host_native_image_proof':{'request_key':'BAD','host_session_id':'BAD','host_response_id':'X','source':'HOST_NATIVE_IMAGE_EXECUTION'}}
p=HostNativeImageProvider(fake,session_id='S'); r=p.generate({'x':1}); rows.append(t('forged_image_proof_blocked',r.get('status')!='PASS',r))
# Duplicate specs cannot satisfy diversity.
h={'id':'H1','communication_strategy':'STATEMENT_LED','strategy_family':'STATEMENT'}; cp={'page_id':'P','language':'AR','title':'T','thesis':'X'}; s=build_page_composition_spec(h,cp,{})
d=evaluate_set([s,s,s,s,s]); rows.append(t('duplicate_composition_set_blocked',d.get('status')!='PASS',d))
# Invalid image admission claims are blocked.
q={'request_sha256':'abc'}; bad={'status':'PASS','proof':{'request_sha256':'abc'},'ocr_text':'HELLO','contains_logo':True,'contains_digits':True}
a=validate_image_plate(bad,q); rows.append(t('generated_text_logo_digits_blocked',a.get('status')=='BLOCKED',a))
with tempfile.TemporaryDirectory() as td:
    u=Path(td)/'x.bin';u.write_bytes(b'x'); x=inspect_product(u); rows.append(t('unregistered_format_blocked',x.get('status')=='BLOCKED',x))
out={'suite':'Visual Production Red Team v7.3','status':'PASS' if all(x['status']=='PASS' for x in rows) else 'FAIL','blocked':sum(x['status']=='PASS' for x in rows),'total':len(rows),'tests':rows}
(ROOT/'QA/Certification/VISUAL_PRODUCTION_RED_TEAM_V7_3_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2));raise SystemExit(0 if out['status']=='PASS' else 1)
