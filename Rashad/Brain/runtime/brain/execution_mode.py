from __future__ import annotations
from dataclasses import dataclass, asdict
import os

HOST_NATIVE_MODE='HOST_NATIVE_MODE'
API_PROVIDER_MODE='API_PROVIDER_MODE'
OFFLINE_VALIDATION_MODE='OFFLINE_VALIDATION_MODE'
AUTO_MODE='AUTO'

ALIASES={
    'HOST':'HOST_NATIVE_MODE','HOST_NATIVE':'HOST_NATIVE_MODE','HOST_NATIVE_MODE':'HOST_NATIVE_MODE',
    'API':'API_PROVIDER_MODE','API_PROVIDER':'API_PROVIDER_MODE','API_PROVIDER_MODE':'API_PROVIDER_MODE',
    'OFFLINE':'OFFLINE_VALIDATION_MODE','OFFLINE_VALIDATION':'OFFLINE_VALIDATION_MODE','OFFLINE_VALIDATION_MODE':'OFFLINE_VALIDATION_MODE',
    'AUTO':'AUTO','': 'AUTO', None:'AUTO'
}

@dataclass(frozen=True)
class ExecutionModeDecision:
    mode:str
    reason:str
    host_bridge_available:bool
    api_provider_configured:bool
    explicit:bool=False
    def to_dict(self): return asdict(self)

def normalize_mode(value):
    key=str(value).strip().upper() if value is not None else None
    if key not in ALIASES:
        raise ValueError(f'UNKNOWN_RASHAD_EXECUTION_MODE:{value}')
    return ALIASES[key]

def detect_execution_mode(explicit=None, *, host_invoke_fn=None, host_response_bundle=None, api_key=None, model=None):
    """Select cognition execution mode without pretending the Python runtime can call its host model.

    HOST_NATIVE_MODE is selected only when the host explicitly requests it or injects a host callback/
    response bundle. API_PROVIDER_MODE requires actual API configuration. Otherwise AUTO safely resolves
    to OFFLINE_VALIDATION_MODE.
    """
    raw=explicit if explicit is not None else os.getenv('RASHAD_EXECUTION_MODE','AUTO')
    mode=normalize_mode(raw)
    host_available=callable(host_invoke_fn) or bool(host_response_bundle)
    api_ok=bool(api_key or os.getenv('OPENAI_API_KEY')) and bool(model or os.getenv('OPENAI_RASHAD_MODEL'))
    is_explicit=normalize_mode(raw)!='AUTO'
    if mode==HOST_NATIVE_MODE:
        return ExecutionModeDecision(HOST_NATIVE_MODE,'EXPLICIT_HOST_NATIVE_MODE',host_available,api_ok,True)
    if mode==API_PROVIDER_MODE:
        return ExecutionModeDecision(API_PROVIDER_MODE,'EXPLICIT_API_PROVIDER_MODE',host_available,api_ok,True)
    if mode==OFFLINE_VALIDATION_MODE:
        return ExecutionModeDecision(OFFLINE_VALIDATION_MODE,'EXPLICIT_OFFLINE_VALIDATION_MODE',host_available,api_ok,True)
    if host_available:
        return ExecutionModeDecision(HOST_NATIVE_MODE,'AUTO_HOST_BRIDGE_AVAILABLE',True,api_ok,False)
    if api_ok:
        return ExecutionModeDecision(API_PROVIDER_MODE,'AUTO_API_PROVIDER_CONFIGURED',False,True,False)
    return ExecutionModeDecision(OFFLINE_VALIDATION_MODE,'AUTO_NO_HOST_BRIDGE_OR_API_PROVIDER',False,False,False)
