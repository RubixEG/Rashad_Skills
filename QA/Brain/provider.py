from __future__ import annotations
from dataclasses import dataclass
import hashlib, json, uuid, os

HOST_NATIVE_MODE='HOST_NATIVE_MODE'
API_PROVIDER_MODE='API_PROVIDER_MODE'
OFFLINE_VALIDATION_MODE='OFFLINE_VALIDATION_MODE'

@dataclass(frozen=True)
class QAInvocation:
    council_id: str
    function: str
    actor_id: str
    isolated_context_id: str
    payload: dict
    previous_response_id: str | None = None

def _hash(obj: dict) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()

def _request_key(invocation:QAInvocation)->str:
    return _hash({'function':invocation.function,'council_id':invocation.council_id,'input_hash':_hash(invocation.payload),'previous_response_id':invocation.previous_response_id})

class QABrainProvider:
    execution_mode='UNSPECIFIED'
    def invoke(self, invocation: QAInvocation) -> dict: raise NotImplementedError
    def runtime_metadata(self): return {'execution_mode':self.execution_mode,'provider':self.__class__.__name__}

class NoExecutionProvider(QABrainProvider):
    execution_mode=OFFLINE_VALIDATION_MODE
    def invoke(self, invocation: QAInvocation) -> dict:
        return {"status":"NOT_EXECUTED","reason":"OFFLINE_VALIDATION_MODE_NO_INDEPENDENT_QA","council_id":invocation.council_id,"function":invocation.function,"actor_id":invocation.actor_id,"isolated_context_id":invocation.isolated_context_id,"input_hash":_hash(invocation.payload),"invocation_id":"QAINV-"+uuid.uuid4().hex[:16].upper(),"execution_mode":self.execution_mode}

class ScriptedIndependentTestProvider(QABrainProvider):
    execution_mode='CERTIFICATION_TEST_MODE'
    def invoke(self, invocation: QAInvocation) -> dict:
        return {"status":"PASS","test_mode":True,"independent":True,"council_id":invocation.council_id,"function":invocation.function,"actor_id":invocation.actor_id,"isolated_context_id":invocation.isolated_context_id,"input_hash":_hash(invocation.payload),"invocation_id":"QA-TEST-"+uuid.uuid4().hex[:16].upper(),"execution_mode":self.execution_mode,"findings":[{"severity":"INFO","status":"NO_MATERIAL_OBJECTION","claim":"Certification-only independent council execution completed.","evidence_refs":["TEST-EVIDENCE"]}]}

class HostNativeQAPendingProvider(QABrainProvider):
    execution_mode=HOST_NATIVE_MODE
    def __init__(self,host_name='HOST_MODEL',host_session_id=None): self.host_name=host_name; self.host_session_id=host_session_id or 'QA-HOST-'+uuid.uuid4().hex[:16].upper(); self.pending_requests=[]
    def invoke(self,invocation):
        key=_request_key(invocation); req={'schema':'RASHAD_HOST_NATIVE_QA_INVOCATION_V1','request_key':key,'host_session_id':self.host_session_id,'host_name':self.host_name,'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'previous_response_id':invocation.previous_response_id,'input_hash':_hash(invocation.payload),'payload':invocation.payload,'required_response_contract':'RASHAD_HOST_NATIVE_QA_RESPONSE_V1'}; self.pending_requests.append(req)
        return {'status':'HOST_NATIVE_PENDING','reason':'HOST_NATIVE_QA_RESPONSE_REQUIRED','request_key':key,'host_session_id':self.host_session_id,'council_id':invocation.council_id,'function':invocation.function,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':req['input_hash'],'invocation_id':'QA-PENDING-'+uuid.uuid4().hex[:16].upper(),'execution_mode':self.execution_mode}
    def runtime_metadata(self): return {'execution_mode':self.execution_mode,'provider':self.__class__.__name__,'host_session_id':self.host_session_id,'host_name':self.host_name,'pending_count':len(self.pending_requests),'pending_requests':self.pending_requests}

class HostNativeQAProvider(QABrainProvider):
    execution_mode=HOST_NATIVE_MODE
    def __init__(self,invoke_fn,host_name='HOST_MODEL',host_session_id=None):
        if not callable(invoke_fn): raise TypeError('host QA invoke_fn must be callable')
        self.invoke_fn=invoke_fn; self.host_name=host_name; self.host_session_id=host_session_id or 'QA-HOST-'+uuid.uuid4().hex[:16].upper(); self.seen=set()
    def invoke(self,invocation):
        key=_request_key(invocation); req={'schema':'RASHAD_HOST_NATIVE_QA_INVOCATION_V1','request_key':key,'host_session_id':self.host_session_id,'host_name':self.host_name,'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'previous_response_id':invocation.previous_response_id,'input_hash':_hash(invocation.payload),'payload':invocation.payload}
        try: out=self.invoke_fn(req)
        except Exception as e: out=None; err=str(e)[:500]
        if not isinstance(out,dict): return {'status':'NOT_EXECUTED','reason':'HOST_NATIVE_QA_CALLBACK_FAILED_OR_NON_OBJECT','error':locals().get('err'),'request_key':key,'council_id':invocation.council_id,'function':invocation.function,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':req['input_hash'],'invocation_id':'QAINV-'+uuid.uuid4().hex[:16].upper(),'execution_mode':self.execution_mode}
        out=dict(out); proof=out.get('host_native_proof') or {}
        if out.get('status')=='PASS':
            valid=proof.get('request_key')==key and proof.get('host_session_id')==self.host_session_id and proof.get('source')=='HOST_NATIVE_MODEL_EXECUTION' and proof.get('independent_context') is True and proof.get('host_response_id') and not invocation.previous_response_id
            if not valid: return {'status':'NOT_EXECUTED','reason':'HOST_NATIVE_QA_PROOF_INVALID','request_key':key,'council_id':invocation.council_id,'function':invocation.function,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':req['input_hash'],'invocation_id':'QAINV-'+uuid.uuid4().hex[:16].upper(),'execution_mode':self.execution_mode}
            if proof['host_response_id'] in self.seen: return {'status':'NOT_EXECUTED','reason':'HOST_NATIVE_QA_RESPONSE_REUSED','request_key':key,'council_id':invocation.council_id,'function':invocation.function,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':req['input_hash'],'invocation_id':'QAINV-'+uuid.uuid4().hex[:16].upper(),'execution_mode':self.execution_mode}
            self.seen.add(proof['host_response_id'])
        out.update({'council_id':invocation.council_id,'function':invocation.function,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':req['input_hash'],'request_key':key,'execution_mode':self.execution_mode,'provider':'HOST_NATIVE_MODEL','host_native':True,'independent':True,'independence_scope':'HOST_ISOLATED_CONTEXT','external_independent':False,'previous_response_id':None}); out.setdefault('invocation_id',proof.get('host_response_id') or 'QAHOST-'+uuid.uuid4().hex[:16].upper()); return out
    def runtime_metadata(self): return {'execution_mode':self.execution_mode,'provider':self.__class__.__name__,'host_session_id':self.host_session_id,'host_name':self.host_name}

class HostNativeQAResponseBundleProvider(HostNativeQAProvider):
    def __init__(self,bundle,host_name='HOST_MODEL'):
        if isinstance(bundle,(str,os.PathLike)): bundle=json.loads(open(bundle,'r',encoding='utf-8').read())
        self.bundle=bundle; self.responses=bundle.get('responses',{}); self.pending_requests=[]
        super().__init__(lambda req:self.responses.get(req['request_key']),host_name=bundle.get('host_name',host_name),host_session_id=bundle.get('host_session_id'))
    def invoke(self,invocation):
        key=_request_key(invocation)
        if key not in self.responses:
            req={'schema':'RASHAD_HOST_NATIVE_QA_INVOCATION_V1','request_key':key,'host_session_id':self.host_session_id,'host_name':self.host_name,'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'previous_response_id':invocation.previous_response_id,'input_hash':_hash(invocation.payload),'payload':invocation.payload,'required_response_contract':'RASHAD_HOST_NATIVE_QA_RESPONSE_V1'}; self.pending_requests.append(req)
            return {'status':'HOST_NATIVE_PENDING','reason':'HOST_NATIVE_QA_RESPONSE_REQUIRED','request_key':key,'host_session_id':self.host_session_id,'council_id':invocation.council_id,'function':invocation.function,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':req['input_hash'],'invocation_id':'QA-PENDING-'+uuid.uuid4().hex[:16].upper(),'execution_mode':self.execution_mode}
        return super().invoke(invocation)
    def runtime_metadata(self): d=super().runtime_metadata(); d.update({'bundle_response_count':len(self.responses),'pending_count':len(self.pending_requests),'pending_requests':self.pending_requests}); return d

class OpenAIQAResponsesProvider(QABrainProvider):
    execution_mode=API_PROVIDER_MODE
    def __init__(self,api_key=None,model=None,base_url=None,timeout=120): self.api_key=api_key or os.getenv('OPENAI_API_KEY'); self.model=model or os.getenv('OPENAI_RASHAD_MODEL'); self.base_url=(base_url or os.getenv('OPENAI_BASE_URL') or 'https://api.openai.com').rstrip('/'); self.timeout=timeout
    @property
    def configured(self): return bool(self.api_key and self.model)
    def invoke(self,invocation):
        if not self.configured: return {'status':'NOT_EXECUTED','reason':'OPENAI_QA_PROVIDER_NOT_CONFIGURED','council_id':invocation.council_id,'function':invocation.function,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':_hash(invocation.payload),'invocation_id':'QAINV-'+uuid.uuid4().hex[:16].upper(),'execution_mode':self.execution_mode}
        import urllib.request
        developer='You are an independent Rashad QA council. Return JSON only with findings. Inspect the supplied deterministic report and actual rendered-product evidence when present. Never self-certify, never reuse producer context, and never issue RELEASED.'
        body={'model':self.model,'input':[{'role':'developer','content':[{'type':'input_text','text':developer}]},{'role':'user','content':[{'type':'input_text','text':json.dumps({'function':invocation.function,'council_id':invocation.council_id,'payload':invocation.payload},ensure_ascii=False)}]}]}
        req=urllib.request.Request(self.base_url+'/v1/responses',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+self.api_key,'Content-Type':'application/json'},method='POST')
        try:
            with urllib.request.urlopen(req,timeout=self.timeout) as r: raw=json.loads(r.read().decode())
            txt=''
            for item in raw.get('output',[]):
                for c in item.get('content',[]):
                    if c.get('type') in ('output_text','text') and c.get('text'): txt=c['text']; break
            parsed=json.loads(txt); parsed.update({'status':'PASS','independent':True,'independence_scope':'EXTERNAL_PROVIDER_CONTEXT','external_independent':True,'council_id':invocation.council_id,'function':invocation.function,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':_hash(invocation.payload),'invocation_id':raw.get('id') or 'QAINV-'+uuid.uuid4().hex[:16].upper(),'execution_mode':self.execution_mode,'previous_response_id':None}); return parsed
        except Exception as e: return {'status':'NOT_EXECUTED','reason':'OPENAI_QA_PROVIDER_CALL_FAILED','error':str(e)[:500],'council_id':invocation.council_id,'function':invocation.function,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':_hash(invocation.payload),'invocation_id':'QAINV-'+uuid.uuid4().hex[:16].upper(),'execution_mode':self.execution_mode}

def resolve_qa_provider(provider=None,*,execution_mode='AUTO',host_invoke_fn=None,host_response_bundle=None,host_name='HOST_MODEL'):
    if provider is not None: return provider,{'mode':getattr(provider,'execution_mode','EXPLICIT_PROVIDER'),'reason':'EXPLICIT_PROVIDER_OBJECT','provider':provider.__class__.__name__}
    raw=(execution_mode or os.getenv('RASHAD_QA_EXECUTION_MODE') or os.getenv('RASHAD_EXECUTION_MODE') or 'AUTO').upper()
    if raw in ('HOST','HOST_NATIVE','HOST_NATIVE_MODE') or (raw=='AUTO' and (callable(host_invoke_fn) or host_response_bundle)):
        if callable(host_invoke_fn): p=HostNativeQAProvider(host_invoke_fn,host_name=host_name)
        elif host_response_bundle: p=HostNativeQAResponseBundleProvider(host_response_bundle,host_name=host_name)
        else: p=HostNativeQAPendingProvider(host_name=host_name)
        return p,{'mode':HOST_NATIVE_MODE,'reason':'HOST_NATIVE_SELECTED','provider':p.__class__.__name__}
    if raw in ('API','API_PROVIDER','API_PROVIDER_MODE') or (raw=='AUTO' and os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_RASHAD_MODEL')):
        p=OpenAIQAResponsesProvider(); return p,{'mode':API_PROVIDER_MODE,'reason':'API_SELECTED','provider':p.__class__.__name__}
    p=NoExecutionProvider(); return p,{'mode':OFFLINE_VALIDATION_MODE,'reason':'NO_HOST_BRIDGE_OR_API','provider':p.__class__.__name__}

def provider_runtime_metadata(provider):
    try:return provider.runtime_metadata()
    except Exception:return {'execution_mode':getattr(provider,'execution_mode','UNKNOWN'),'provider':provider.__class__.__name__}
