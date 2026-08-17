from __future__ import annotations
import json,re
from pathlib import Path
from .ontology import registry as ontology_registry

ROOT=Path(__file__).resolve().parents[2]
RULES=ROOT/'config'/'brain_expert_routing_rules.json'

def _rules(): return json.loads(RULES.read_text(encoding='utf-8'))
def _flatten_values(obj):
    if obj is None: return ''
    if isinstance(obj,str): return obj
    if isinstance(obj,(int,float,bool)): return str(obj)
    if isinstance(obj,dict): return ' '.join(_flatten_values(v) for v in obj.values())
    if isinstance(obj,(list,tuple,set)): return ' '.join(_flatten_values(v) for v in obj)
    return str(obj)
def _text(task): return _flatten_values(task).lower()

def route_experts(task:dict):
    cfg=_rules(); known={a['id'] for a in ontology_registry()['actors']}; selected=[]; reasons={}; matched=[]; required=[]
    maxn=int(cfg['max_active_experts_per_task'])
    def add(rid,why,required_role=False):
        if rid not in known: return False
        if rid not in selected and len(selected)<maxn:
            selected.append(rid)
        if rid in selected:
            reasons.setdefault(rid,[])
            if why not in reasons[rid]: reasons[rid].append(why)
            if required_role and rid not in required: required.append(rid)
            return True
        return False
    for rid in cfg.get('core_roles',[]): add(rid,'CORE',True)
    role=str(task.get('rfp_role') or task.get('role') or '').upper()
    for rid in cfg.get('role_rules',{}).get(role,[]): add(rid,'RFP_ROLE:'+role,True)
    text=_text(task); matched_rules=[]
    for rule in cfg.get('domain_rules',[]):
        if any(p.lower() in text for p in rule.get('patterns',[])):
            matched.append(rule['id']); matched_rules.append(rule)
    # Coverage first: one lead SME/role per matched domain before any domain can consume the budget.
    for rule in matched_rules:
        roles=rule.get('roles',[])
        if roles: add(roles[0],'DOMAIN_LEAD:'+rule['id'],True)
    # Mandatory governors cannot be truncated by optional specialists.
    if task.get('critical',True):
        for rid in cfg.get('mandatory_governors_for_critical',[]): add(rid,'CRITICAL_GOVERNOR',True)
    # Round-robin secondary expertise keeps multi-domain tasks balanced.
    depth=1
    while len(selected)<maxn:
        progressed=False
        for rule in matched_rules:
            roles=rule.get('roles',[])
            if depth < len(roles):
                before=len(selected); add(roles[depth],'DOMAIN:'+rule['id'],False)
                progressed = progressed or len(selected)>before
                if len(selected)>=maxn: break
        if not progressed: break
        depth+=1
    unknown=[]
    for rid in cfg.get('core_roles',[]):
        if rid not in known: unknown.append(rid)
    missing_required=[r for r in required if r not in selected]
    status='PASS' if selected and not unknown and not missing_required else 'BLOCKED'
    return {
        'status':status,'selected_experts':selected,'required_experts':required,'selected_count':len(selected),
        'max_active_experts':maxn,'matched_domains':matched,
        'selection_reasons':reasons,'unknown_configured_roles':unknown,'missing_required_roles':missing_required,
        'registered_actor_count':len(known),'bounded_activation':True,
        'principle':'REGISTERED_NE_ACTIVE; ROUTED_PLUS_EXECUTED_EQUALS_ACTIVE_INTELLIGENCE'
    }

