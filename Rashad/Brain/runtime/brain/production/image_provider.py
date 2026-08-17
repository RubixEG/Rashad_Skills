from __future__ import annotations
from pathlib import Path
import hashlib, json, os, uuid

HOST_NATIVE_IMAGE_MODE='HOST_NATIVE_IMAGE_MODE'
EXTERNAL_IMAGE_MODE='EXTERNAL_IMAGE_MODE'
NO_IMAGE_PROVIDER='NO_IMAGE_PROVIDER'

def _h(x):
    if isinstance(x,(str,Path)) and Path(x).exists(): return hashlib.sha256(Path(x).read_bytes()).hexdigest()
    return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

class ImageProvider:
    mode='UNSPECIFIED'
    def generate(self,request:dict)->dict: raise NotImplementedError
    def metadata(self): return {'mode':self.mode,'provider':self.__class__.__name__}

class HostNativeImagePendingProvider(ImageProvider):
    mode=HOST_NATIVE_IMAGE_MODE
    def __init__(self,host_name='HOST_IMAGE_MODEL',session_id=None):
        self.host_name=host_name; self.session_id=session_id or 'IMG-HOST-'+uuid.uuid4().hex[:16].upper(); self.pending=[]
    def generate(self,request):
        key='IMGREQ-'+_h({'session':self.session_id,'request':request})[:24].upper()
        req={'schema':'RASHAD_HOST_NATIVE_IMAGE_REQUEST_V1','request_key':key,'host_session_id':self.session_id,'host_name':self.host_name,'request':request,'required_response_contract':'RASHAD_HOST_NATIVE_IMAGE_RESPONSE_V1'}
        self.pending.append(req)
        return {'status':'HOST_NATIVE_IMAGE_PENDING','reason':'HOST_NATIVE_IMAGE_RESPONSE_REQUIRED','request_key':key,'host_session_id':self.session_id,'request':request}
    def metadata(self): return {'mode':self.mode,'provider':self.__class__.__name__,'pending_count':len(self.pending),'pending_requests':self.pending,'host_session_id':self.session_id,'host_name':self.host_name}

class HostNativeImageProvider(ImageProvider):
    mode=HOST_NATIVE_IMAGE_MODE
    def __init__(self,invoke_fn,host_name='HOST_IMAGE_MODEL',session_id=None):
        if not callable(invoke_fn): raise TypeError('image invoke_fn must be callable')
        self.invoke_fn=invoke_fn; self.host_name=host_name; self.session_id=session_id or 'IMG-HOST-'+uuid.uuid4().hex[:16].upper(); self.seen=set()
    def generate(self,request):
        key='IMGREQ-'+_h({'session':self.session_id,'request':request})[:24].upper()
        req={'schema':'RASHAD_HOST_NATIVE_IMAGE_REQUEST_V1','request_key':key,'host_session_id':self.session_id,'host_name':self.host_name,'request':request}
        try: out=self.invoke_fn(req)
        except Exception as e: return {'status':'BLOCKED','reason':'HOST_NATIVE_IMAGE_CALLBACK_FAILED','error':repr(e),'request_key':key}
        if not isinstance(out,dict): return {'status':'BLOCKED','reason':'HOST_NATIVE_IMAGE_RESPONSE_NOT_OBJECT','request_key':key}
        proof=out.get('host_native_image_proof') or {}; path=Path(out.get('image_path',''))
        valid=(proof.get('request_key')==key and proof.get('host_session_id')==self.session_id and proof.get('source')=='HOST_NATIVE_IMAGE_EXECUTION' and proof.get('host_response_id') and path.exists())
        if not valid: return {'status':'BLOCKED','reason':'HOST_NATIVE_IMAGE_PROOF_INVALID','request_key':key}
        if proof['host_response_id'] in self.seen: return {'status':'BLOCKED','reason':'HOST_NATIVE_IMAGE_RESPONSE_REUSED','request_key':key}
        actual=_h(path)
        if out.get('image_sha256') and out.get('image_sha256')!=actual: return {'status':'BLOCKED','reason':'HOST_NATIVE_IMAGE_HASH_MISMATCH','request_key':key}
        self.seen.add(proof['host_response_id']); return {**out,'status':'PASS','image_sha256':actual,'request_key':key,'provider':'HOST_NATIVE_IMAGE_MODEL','mode':self.mode}
    def metadata(self): return {'mode':self.mode,'provider':self.__class__.__name__,'host_session_id':self.session_id,'host_name':self.host_name}

class ImageResponseBundleProvider(HostNativeImageProvider):
    def __init__(self,bundle,host_name='HOST_IMAGE_MODEL'):
        if isinstance(bundle,(str,os.PathLike)): bundle=json.loads(Path(bundle).read_text(encoding='utf-8'))
        self.bundle=bundle; self.responses=bundle.get('responses',{}); self.pending=[]
        super().__init__(lambda req:self.responses.get(req['request_key']),host_name=bundle.get('host_name',host_name),session_id=bundle.get('host_session_id'))
    def generate(self,request):
        key='IMGREQ-'+_h({'session':self.session_id,'request':request})[:24].upper()
        if key not in self.responses:
            req={'schema':'RASHAD_HOST_NATIVE_IMAGE_REQUEST_V1','request_key':key,'host_session_id':self.session_id,'host_name':self.host_name,'request':request,'required_response_contract':'RASHAD_HOST_NATIVE_IMAGE_RESPONSE_V1'}; self.pending.append(req)
            return {'status':'HOST_NATIVE_IMAGE_PENDING','reason':'HOST_NATIVE_IMAGE_RESPONSE_REQUIRED','request_key':key,'host_session_id':self.session_id,'request':request}
        return super().generate(request)
    def metadata(self):
        d=super().metadata(); d.update({'bundle_response_count':len(self.responses),'pending_count':len(self.pending),'pending_requests':self.pending}); return d

class ExternalCallableImageProvider(HostNativeImageProvider):
    mode=EXTERNAL_IMAGE_MODE
    def __init__(self,invoke_fn): super().__init__(invoke_fn,host_name='EXTERNAL_IMAGE_PROVIDER',session_id='EXT-IMG-'+uuid.uuid4().hex[:16].upper())

def resolve_image_provider(provider=None,*,host_invoke_fn=None,response_bundle=None,host_name='HOST_IMAGE_MODEL',required=False):
    if provider is not None: return provider
    if callable(host_invoke_fn): return HostNativeImageProvider(host_invoke_fn,host_name=host_name)
    if response_bundle: return ImageResponseBundleProvider(response_bundle,host_name=host_name)
    return HostNativeImagePendingProvider(host_name=host_name) if required else None
