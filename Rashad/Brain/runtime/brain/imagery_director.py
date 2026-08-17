from __future__ import annotations
from pathlib import Path
import hashlib,json,uuid

def _sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def build_image_request(spec,content_pack):
    im=spec.get('imagery') or {}; mode=im.get('mode','NONE')
    if mode=='NONE': return {'status':'NOT_REQUIRED','mode':mode}
    payload={'schema':'RASHAD_HOST_NATIVE_IMAGE_REQUEST_V1','request_id':'IMGREQ-'+uuid.uuid4().hex[:12].upper(),'page_id':spec.get('page_id'),'mode':mode,'scene':spec.get('scene_metaphor'),'negative_space_zones':spec.get('negative_space_zones'),'dominant_bbox':spec.get('dominant_bbox'),'forbidden':['legible text','logos','digits','official seals'],'style':'premium consulting editorial, restrained, institutional, photoreal or materially sophisticated as appropriate','content_theme':str(content_pack.get('title') or content_pack.get('thesis') or '')[:300]}
    payload['request_sha256']=hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    return {'status':'HOST_NATIVE_IMAGE_PENDING','mode':mode,'request':payload}

def validate_image_plate(result,request):
    if not isinstance(result,dict): return {'status':'BLOCKED','reason':'IMAGE_RESULT_REQUIRED'}
    proof=result.get('proof') or {}; blockers=[]
    if result.get('status')!='PASS': blockers.append('IMAGE_PROVIDER_NOT_PASS')
    if proof.get('request_sha256')!=request.get('request_sha256'): blockers.append('IMAGE_REQUEST_BINDING_MISMATCH')
    if result.get('ocr_text','').strip(): blockers.append('GENERATED_IMAGE_CONTAINS_TEXT')
    if result.get('contains_logo') is not False: blockers.append('GENERATED_IMAGE_LOGO_NOT_PROVEN_ABSENT')
    if result.get('contains_digits') is not False: blockers.append('GENERATED_IMAGE_DIGITS_NOT_PROVEN_ABSENT')
    asset=result.get('asset_path') or result.get('image_path'); expected=result.get('asset_sha256') or result.get('image_sha256')
    if not asset or not Path(asset).exists() or not expected: blockers.append('IMAGE_ASSET_PROOF_REQUIRED')
    elif _sha(asset)!=expected: blockers.append('IMAGE_ASSET_HASH_MISMATCH')
    return {'status':'PASS' if not blockers else 'BLOCKED','blockers':blockers,'asset_path':asset,'asset_sha256':expected,'rule':'Generated visual plates are non-authoritative: text, logos, numerals and official seals are forbidden; native verified overlays own factual content.'}
