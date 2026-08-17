from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib, json, os
from .utils import new_id, obj_hash
from .execution_mode import (
    HOST_NATIVE_MODE, API_PROVIDER_MODE, OFFLINE_VALIDATION_MODE,
    detect_execution_mode,
)

@dataclass
class Invocation:
    function:str; council_id:str; actor_id:str; isolated_context_id:str; input_payload:dict; previous_response_id:str|None=None

class BrainProvider:
    execution_mode='UNSPECIFIED'
    def invoke(self, invocation:Invocation)->dict: raise NotImplementedError
    def runtime_metadata(self): return {'execution_mode':self.execution_mode,'provider':self.__class__.__name__}

class NoExecutionProvider(BrainProvider):
    execution_mode=OFFLINE_VALIDATION_MODE
    def invoke(self, invocation:Invocation)->dict:
        return {'status':'NOT_EXECUTED','reason':'OFFLINE_VALIDATION_MODE_NO_COGNITION','invocation_id':new_id('INV'),'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':obj_hash(invocation.input_payload),'execution_mode':self.execution_mode}

OfflineValidationProvider=NoExecutionProvider

class ScriptedTestProvider(BrainProvider):
    execution_mode='CERTIFICATION_TEST_MODE'
    def invoke(self, invocation:Invocation)->dict:
        fn=invocation.function
        base={'status':'PASS','invocation_id':new_id('TESTINV'),'function':fn,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':obj_hash(invocation.input_payload),'test_mode':True,'execution_mode':self.execution_mode}
        if fn=='PRODUCER':
            base['output']={'management_question':'What decision is supported?','evaluator_question':'What proof is required?','decision_supported':'TEST_DECISION','answer_first_thesis':'Evidence-backed test thesis','evidence_for':['E1'],'evidence_against':[],'assumptions':[],'risks_counterarguments':['Challenge required'],'semantic_relationships':['DEPENDS_ON'],'executive_implication':'Test implication'}
        elif fn in ('CHALLENGER','COUNCIL_REVIEW','META_REVIEW','SME_REVIEW','EXECUTIVE_SIMULATION','EVALUATOR_SIMULATION','GOVERNOR_REVIEW','ARTIFACT_COUNCIL_REVIEW','ARTIFACT_RED_TEAM','ART_DIRECTION_REVIEW','PRODUCTION_READINESS_REVIEW'):
            base['findings']=[{'status':'NO_MATERIAL_OBJECTION','claim':'Test-only structured challenge completed','evidence_refs':['E1'],'severity':'INFO'}]
        elif fn in ('INDEPENDENT_JUDGE','RELEASE_CHAIR'):
            base.update({'independent':True,'judge_invocation_id':new_id('TEST-JUDGE'),'score':95,'hard_blockers':[],'evidence_refs':['E1'],'actual_render_hash':invocation.input_payload.get('actual_render_hash','TEST_RENDER_HASH')})
        return base

class ExternalCallableProvider(BrainProvider):
    """Application integration boundary. The callable must execute one isolated invocation and return a dict."""
    execution_mode='EXTERNAL_CALLABLE_PROVIDER'
    def __init__(self, invoke_fn):
        if not callable(invoke_fn): raise TypeError('invoke_fn must be callable')
        self.invoke_fn=invoke_fn
    def invoke(self, invocation:Invocation)->dict:
        out=self.invoke_fn(invocation)
        if not isinstance(out,dict):
            return {'status':'NOT_EXECUTED','reason':'EXTERNAL_PROVIDER_RETURNED_NON_OBJECT','invocation_id':new_id('INV'),'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':obj_hash(invocation.input_payload),'execution_mode':self.execution_mode}
        out=dict(out); out.setdefault('invocation_id',new_id('INV')); out.setdefault('function',invocation.function); out.setdefault('council_id',invocation.council_id); out.setdefault('actor_id',invocation.actor_id); out.setdefault('isolated_context_id',invocation.isolated_context_id); out.setdefault('input_hash',obj_hash(invocation.input_payload)); out.setdefault('execution_mode',self.execution_mode); return out


def host_request_key(invocation:Invocation)->str:
    payload={
        'function':invocation.function,'council_id':invocation.council_id,
        'input_hash':obj_hash(invocation.input_payload),
        'previous_response_id':invocation.previous_response_id,
    }
    return hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

class HostNativePendingProvider(BrainProvider):
    """Fail-closed request collector for ChatGPT/Claude/Codex-style host orchestration.

    This provider NEVER fabricates cognition. It emits exact host-native invocation contracts that the
    surrounding host model must execute and return through HostNativeResponseBundleProvider or a callback.
    """
    execution_mode=HOST_NATIVE_MODE
    def __init__(self, host_name='HOST_MODEL', host_session_id=None):
        self.host_name=host_name; self.host_session_id=host_session_id or new_id('HOST-SESSION'); self.pending_requests=[]
    def invoke(self, invocation:Invocation)->dict:
        key=host_request_key(invocation)
        req={'request_key':key,'host_session_id':self.host_session_id,'host_name':self.host_name,'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'previous_response_id':invocation.previous_response_id,'input_hash':obj_hash(invocation.input_payload),'input_payload':invocation.input_payload,'required_response_contract':'RASHAD_HOST_NATIVE_RESPONSE_V1'}
        self.pending_requests.append(req)
        return {'status':'HOST_NATIVE_PENDING','reason':'HOST_NATIVE_RESPONSE_REQUIRED','request_key':key,'host_session_id':self.host_session_id,'invocation_id':new_id('HOST-PENDING'),'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':req['input_hash'],'execution_mode':self.execution_mode}
    def runtime_metadata(self):
        return {'execution_mode':self.execution_mode,'provider':self.__class__.__name__,'host_session_id':self.host_session_id,'host_name':self.host_name,'pending_count':len(self.pending_requests),'pending_requests':self.pending_requests}

class HostNativeProvider(BrainProvider):
    """Synchronous host-native bridge. The host injects a callable; no API key or network call is required."""
    execution_mode=HOST_NATIVE_MODE
    def __init__(self, invoke_fn, host_name='HOST_MODEL', host_session_id=None):
        if not callable(invoke_fn): raise TypeError('host invoke_fn must be callable')
        self.invoke_fn=invoke_fn; self.host_name=host_name; self.host_session_id=host_session_id or new_id('HOST-SESSION'); self.seen_response_ids=set()
    def invoke(self, invocation:Invocation)->dict:
        key=host_request_key(invocation)
        req={'schema':'RASHAD_HOST_NATIVE_INVOCATION_V1','request_key':key,'host_session_id':self.host_session_id,'host_name':self.host_name,'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'previous_response_id':invocation.previous_response_id,'input_hash':obj_hash(invocation.input_payload),'input_payload':invocation.input_payload}
        try: out=self.invoke_fn(req)
        except Exception as e:
            return {'status':'NOT_EXECUTED','reason':'HOST_NATIVE_CALLBACK_FAILED','error':str(e)[:500],'request_key':key,'invocation_id':new_id('INV'),'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':req['input_hash'],'execution_mode':self.execution_mode}
        return self._normalize(invocation,key,out)
    def _normalize(self,invocation,key,out):
        if not isinstance(out,dict): return {'status':'NOT_EXECUTED','reason':'HOST_NATIVE_RETURNED_NON_OBJECT','request_key':key,'invocation_id':new_id('INV'),'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':obj_hash(invocation.input_payload),'execution_mode':self.execution_mode}
        out=dict(out); proof=out.get('host_native_proof') or {}
        if out.get('status')=='PASS':
            if proof.get('request_key')!=key or proof.get('host_session_id')!=self.host_session_id or proof.get('source')!='HOST_NATIVE_MODEL_EXECUTION' or not proof.get('host_response_id'):
                return {'status':'NOT_EXECUTED','reason':'HOST_NATIVE_PROOF_INVALID','request_key':key,'invocation_id':new_id('INV'),'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':obj_hash(invocation.input_payload),'execution_mode':self.execution_mode}
            if proof['host_response_id'] in self.seen_response_ids:
                return {'status':'NOT_EXECUTED','reason':'HOST_NATIVE_RESPONSE_REUSED','request_key':key,'invocation_id':new_id('INV'),'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':obj_hash(invocation.input_payload),'execution_mode':self.execution_mode}
            self.seen_response_ids.add(proof['host_response_id'])
        out.setdefault('invocation_id',proof.get('host_response_id') or new_id('HOSTINV')); out['function']=invocation.function; out['council_id']=invocation.council_id; out['actor_id']=invocation.actor_id; out['isolated_context_id']=invocation.isolated_context_id; out['input_hash']=obj_hash(invocation.input_payload); out['request_key']=key; out['execution_mode']=self.execution_mode; out['provider']='HOST_NATIVE_MODEL'; out['host_native']=True
        if invocation.function in ('INDEPENDENT_JUDGE','RELEASE_CHAIR') and out.get('status')=='PASS':
            if proof.get('independent_context') is not True or invocation.previous_response_id:
                return {'status':'NOT_EXECUTED','reason':'HOST_NATIVE_INDEPENDENCE_PROOF_INVALID','request_key':key,'invocation_id':new_id('INV'),'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':obj_hash(invocation.input_payload),'execution_mode':self.execution_mode}
            out['independent']=True; out['independence_scope']='HOST_ISOLATED_CONTEXT'; out['external_independent']=False; out['judge_invocation_id']=out['invocation_id']; out['previous_response_id']=None
        return out
    def runtime_metadata(self): return {'execution_mode':self.execution_mode,'provider':self.__class__.__name__,'host_session_id':self.host_session_id,'host_name':self.host_name}

class HostNativeResponseBundleProvider(HostNativeProvider):
    """Replay/continuation bridge for chat hosts that cannot expose a synchronous model callback.

    Bundle shape: {"host_session_id":"...","responses": {request_key: response_object}}
    Every response is bound to the exact request key and input hash. Missing entries become HOST_NATIVE_PENDING.
    """
    def __init__(self,bundle,host_name='HOST_MODEL'):
        if isinstance(bundle,(str,os.PathLike)):
            bundle=json.loads(open(bundle,'r',encoding='utf-8').read())
        if not isinstance(bundle,dict): raise TypeError('host response bundle must be object/path')
        self.bundle=bundle; self.responses=bundle.get('responses',{}); self.pending_requests=[]
        sid=bundle.get('host_session_id') or new_id('HOST-SESSION')
        super().__init__(lambda req:self.responses.get(req['request_key']),host_name=bundle.get('host_name',host_name),host_session_id=sid)
    def invoke(self,invocation):
        key=host_request_key(invocation)
        if key not in self.responses:
            req={'schema':'RASHAD_HOST_NATIVE_INVOCATION_V1','request_key':key,'host_session_id':self.host_session_id,'host_name':self.host_name,'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'previous_response_id':invocation.previous_response_id,'input_hash':obj_hash(invocation.input_payload),'input_payload':invocation.input_payload,'required_response_contract':'RASHAD_HOST_NATIVE_RESPONSE_V1'}
            self.pending_requests.append(req)
            return {'status':'HOST_NATIVE_PENDING','reason':'HOST_NATIVE_RESPONSE_REQUIRED','request_key':key,'host_session_id':self.host_session_id,'invocation_id':new_id('HOST-PENDING'),'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':req['input_hash'],'execution_mode':self.execution_mode}
        return super().invoke(invocation)
    def runtime_metadata(self):
        d=super().runtime_metadata(); d.update({'bundle_response_count':len(self.responses),'pending_count':len(self.pending_requests),'pending_requests':self.pending_requests}); return d

class OpenAIResponsesProvider(BrainProvider):
    """Live adapter for the OpenAI Responses API. Requires OPENAI_API_KEY and OPENAI_RASHAD_MODEL."""
    execution_mode=API_PROVIDER_MODE
    def __init__(self, api_key=None, model=None, base_url=None, timeout=120):
        self.api_key=api_key or os.getenv('OPENAI_API_KEY'); self.model=model or os.getenv('OPENAI_RASHAD_MODEL'); self.base_url=(base_url or os.getenv('OPENAI_BASE_URL') or 'https://api.openai.com').rstrip('/'); self.timeout=timeout
    @property
    def configured(self): return bool(self.api_key and self.model)
    def _extract_text(self, raw):
        for item in raw.get('output',[]):
            for c in item.get('content',[]):
                if c.get('type') in ('output_text','text') and c.get('text'): return c['text']
        return raw.get('output_text') or ''
    def invoke(self, invocation:Invocation)->dict:
        if not self.configured:
            return {'status':'NOT_EXECUTED','reason':'OPENAI_PROVIDER_NOT_CONFIGURED','invocation_id':new_id('INV'),'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':obj_hash(invocation.input_payload),'execution_mode':self.execution_mode}
        import urllib.request, json as _json, base64, mimetypes
        developer=('You are one isolated Rashad Brain council invocation. Return JSON only. Do not claim execution you did not perform. Use only supplied evidence. For PRODUCER return an object suitable as a cognitive packet. For review functions return findings and include a veto only when a hard governor violation is proven. For INDEPENDENT_JUDGE return score, hard_blockers, evidence_refs and winner_candidate_id when applicable. Never reuse another actor context and never self-certify.')
        content=[{'type':'input_text','text':_json.dumps({'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'payload':invocation.input_payload},ensure_ascii=False)}]
        for p in invocation.input_payload.get('image_paths',[]) if isinstance(invocation.input_payload,dict) else []:
            try:
                data=base64.b64encode(open(p,'rb').read()).decode(); mime=mimetypes.guess_type(p)[0] or 'image/png'; content.append({'type':'input_image','image_url':f'data:{mime};base64,{data}','detail':'high'})
            except Exception: pass
        body={'model':self.model,'input':[{'role':'developer','content':[{'type':'input_text','text':developer}]},{'role':'user','content':content}]}
        req=urllib.request.Request(self.base_url+'/v1/responses',data=_json.dumps(body).encode(),headers={'Authorization':'Bearer '+self.api_key,'Content-Type':'application/json'},method='POST')
        try:
            with urllib.request.urlopen(req,timeout=self.timeout) as r: raw=_json.loads(r.read().decode())
            parsed=_json.loads(self._extract_text(raw).strip()); base={'status':'PASS','invocation_id':raw.get('id') or new_id('INV'),'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':obj_hash(invocation.input_payload),'provider':'OPENAI_RESPONSES_API','execution_mode':self.execution_mode}
            if invocation.function=='PRODUCER': base['output']=parsed
            else: base.update(parsed)
            if invocation.function in ('INDEPENDENT_JUDGE','RELEASE_CHAIR'): base['independent']=True; base['independence_scope']='EXTERNAL_PROVIDER_CONTEXT'; base['external_independent']=True; base['judge_invocation_id']=base['invocation_id']; base['previous_response_id']=None
            return base
        except Exception as e:
            return {'status':'NOT_EXECUTED','reason':'OPENAI_PROVIDER_CALL_FAILED','error':str(e)[:500],'invocation_id':new_id('INV'),'function':invocation.function,'council_id':invocation.council_id,'actor_id':invocation.actor_id,'isolated_context_id':invocation.isolated_context_id,'input_hash':obj_hash(invocation.input_payload),'execution_mode':self.execution_mode}


def resolve_brain_provider(provider=None, *, execution_mode='AUTO', host_invoke_fn=None, host_response_bundle=None, host_name='HOST_MODEL', api_key=None, model=None):
    if provider is not None:
        return provider, {'mode':getattr(provider,'execution_mode','EXPLICIT_PROVIDER'),'reason':'EXPLICIT_PROVIDER_OBJECT','provider':provider.__class__.__name__}
    decision=detect_execution_mode(execution_mode,host_invoke_fn=host_invoke_fn,host_response_bundle=host_response_bundle,api_key=api_key,model=model)
    if decision.mode==HOST_NATIVE_MODE:
        if callable(host_invoke_fn): p=HostNativeProvider(host_invoke_fn,host_name=host_name)
        elif host_response_bundle: p=HostNativeResponseBundleProvider(host_response_bundle,host_name=host_name)
        else: p=HostNativePendingProvider(host_name=host_name)
    elif decision.mode==API_PROVIDER_MODE:
        p=OpenAIResponsesProvider(api_key=api_key,model=model)
    else:
        p=OfflineValidationProvider()
    meta=decision.to_dict(); meta['provider']=p.__class__.__name__; return p,meta


def provider_runtime_metadata(provider):
    try: return provider.runtime_metadata()
    except Exception: return {'execution_mode':getattr(provider,'execution_mode','UNKNOWN'),'provider':provider.__class__.__name__}
