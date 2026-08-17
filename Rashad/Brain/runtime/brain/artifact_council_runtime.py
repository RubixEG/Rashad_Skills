from __future__ import annotations
import json
from pathlib import Path
from .artifact_brain import route_artifact_councils
from .provider import Invocation, NoExecutionProvider, resolve_brain_provider
from .utils import new_id

HERE=Path(__file__).resolve(); REG_PATH=HERE.parents[2]/'config'/'artifact_brain_expert_universe_v3.json'
REG=json.loads(REG_PATH.read_text(encoding='utf-8'))
COUNCILS={c['id']:c for c in REG['councils']}; ROLES={r['id']:r for r in REG['roles']}

STAGE_FUNCTION={
 'PRE_CONCEPT':'ARTIFACT_COUNCIL_REVIEW','ART_DIRECTION':'ART_DIRECTION_REVIEW',
 'PRODUCTION_READINESS':'PRODUCTION_READINESS_REVIEW','DECK_REVIEW':'ARTIFACT_COUNCIL_REVIEW'
}

def _panel_roles(council_id, features, content_pack=None):
    roles=COUNCILS[council_id]['roles']
    content_pack=content_pack or {}; preferred=[]
    # Every registered role is executable when explicitly justified by the page expertise plan.
    requested=[x for x in (content_pack.get('requested_artifact_role_ids') or content_pack.get('artifact_expertise_requirements') or []) if x in roles]
    if council_id=='INFORMATION_DESIGN_COUNCIL':
        preferred=['AR-INFORMATION-DESIGNER','AR-VISUAL-PERCEPTION-EXPERT']
        if features.get('number_count',0)>=2: preferred.insert(1,'AR-DATA-VISUALIZATION-EXPERT')
    elif council_id=='QUANTITATIVE_EXHIBIT_COUNCIL': preferred=['AR-QUANTITATIVE-ANALYST','AR-DATA-VISUALIZATION-EXPERT','AR-CFO-SIMULATOR']
    elif council_id=='SYSTEMS_ARCHITECTURE_COUNCIL': preferred=['AR-SOLUTION-ARCHITECT','AR-ENTERPRISE-ARCHITECT']
    elif council_id=='EXECUTIVE_AUDIENCE_COUNCIL': preferred=['AR-CFO-SIMULATOR'] if features.get('financial') else (['AR-CIO-CTO-SIMULATOR'] if features.get('architecture') else ['AR-CEO-GM-SIMULATOR'])
    elif council_id=='ARTIFACT_RED_TEAM': preferred=['AR-GENERIC-LAYOUT-ATTACKER','AR-DIAGRAM-OVERUSE-ATTACKER']
    elif council_id=='ARABIC_RTL_COUNCIL': preferred=['AR-RTL-INFORMATION-DESIGNER','AR-ARABIC-TYPOGRAPHY-EXPERT','AR-BIDI-SPECIALIST']
    elif council_id=='META_EXPERTISE_ROUTER': preferred=['AR-MISSING-EXPERTISE-DETECTOR','AR-COUNCIL-INTEGRITY-REVIEWER']
    elif council_id=='ART_DIRECTION_COUNCIL': preferred=['AR-ART-DIRECTOR','AR-VISUAL-PERCEPTION-EXPERT','AR-CONSULTING-PRESENTATION-DESIGNER']
    elif council_id=='CREATIVE_VISUAL_COUNCIL':
        preferred=['AR-CREATIVE-DIRECTOR','AR-IMAGE-DIRECTOR','AR-PHOTOGRAPHY-HERO-IMAGE-DIRECTOR'] if features.get('image_cue') else ['AR-ART-DIRECTOR','AR-VISUAL-METAPHOR-SPECIALIST']
    elif council_id=='BRAND_COUNCIL': preferred=['AR-BRAND-DIRECTOR','AR-RUBIX-BRAND-CUSTODIAN','AR-CO-BRANDING-REVIEWER']
    elif council_id=='PRODUCTION_COUNCIL': preferred=['AR-PPTX-PRODUCTION-SPECIALIST','AR-TYPOGRAPHY-ENGINEER','AR-CONNECTOR-ROUTING-ENGINEER']
    elif council_id=='USER_VISIBLE_DELIVERY_COUNCIL': preferred=['AR-INDEPENDENT-VISUAL-QA-JUDGE','AR-PDF-PPTX-PARITY-SPECIALIST']
    elif council_id=='DECK_ARTISTIC_DIRECTOR_COUNCIL': preferred=['AR-VISUAL-RHYTHM-DIRECTOR','AR-CROSS-DECK-VARIETY-REVIEWER']
    preferred=requested+preferred
    out=[]
    for rid in preferred+roles:
        if rid in roles and rid not in out: out.append(rid)
    # one role for ordinary councils, two for visual-critical, three for art/production/RTL
    cap=3 if council_id in {'ART_DIRECTION_COUNCIL','CREATIVE_VISUAL_COUNCIL','PRODUCTION_COUNCIL','ARABIC_RTL_COUNCIL'} else (2 if council_id in {'INFORMATION_DESIGN_COUNCIL','BRAND_COUNCIL','USER_VISIBLE_DELIVERY_COUNCIL','DECK_ARTISTIC_DIRECTOR_COUNCIL','ARTIFACT_RED_TEAM','QUANTITATIVE_EXHIBIT_COUNCIL'} else 1)
    return out[:cap]

def execute_artifact_councils(graph,content_pack,provider=None,language='AR',stage='PRE_CONCEPT',prior=None,execution_mode='AUTO',host_invoke_fn=None,host_response_bundle=None,host_name='HOST_MODEL'):
    provider,_=resolve_brain_provider(provider,execution_mode=execution_mode,host_invoke_fn=host_invoke_fn,host_response_bundle=host_response_bundle,host_name=host_name); route=route_artifact_councils(graph,content_pack,language,stage)
    if route.get('status')!='PASS': return {'status':'BLOCKED','route':route,'reason':'ARTIFACT_COUNCIL_ROUTING_INVALID'}
    inv=[]; errors=[]; findings=[]; actor_ids=set(); context_ids=set(); required=[]
    fn=STAGE_FUNCTION.get(route['stage'],'ARTIFACT_COUNCIL_REVIEW')
    role_budget=int(REG['runtime_activation_policy']['max_active_roles_per_page'])
    for cid in route['active_councils']:
        panel=_panel_roles(cid,route.get('page_features',{}),content_pack)
        if not panel: errors.append({'kind':'ARTIFACT_COUNCIL_HAS_NO_EXECUTABLE_ROLE','council_id':cid}); continue
        remaining=max(0,role_budget-len(required)); panel=panel[:remaining]
        for rid in panel:
            required.append({'council_id':cid,'role_id':rid})
            if not rid or rid not in ROLES:
                errors.append({'kind':'ARTIFACT_COUNCIL_HAS_NO_EXECUTABLE_ROLE','council_id':cid,'role_id':rid}); continue
            aid=new_id('ACTOR-'+rid); ctx=new_id('CTX-'+cid+'-'+rid)
            rr=provider.invoke(Invocation(fn,cid,aid,ctx,{
                'artifact_role_id':rid,'artifact_role_name':ROLES[rid].get('name'),
                'stage':route['stage'],'content_pack':content_pack,'semantic_graph':graph,
                'page_features':route.get('page_features',{}),'prior':prior or {}
            }))
            rr=dict(rr); rr['artifact_role_id']=rid; inv.append(rr)
            if rr.get('status')!='PASS': errors.append({'kind':'ARTIFACT_COUNCIL_NOT_EXECUTED','council_id':cid,'role_id':rid,'status':rr.get('status')}); continue
            if aid in actor_ids or ctx in context_ids: errors.append({'kind':'ARTIFACT_COUNCIL_CONTEXT_REUSED','council_id':cid,'role_id':rid})
            actor_ids.add(aid); context_ids.add(ctx)
            for f in rr.get('findings',[]) or []:
                ff=dict(f); ff['council_id']=cid; ff['artifact_role_id']=rid; findings.append(ff)
            if rr.get('veto'): errors.append({'kind':'ARTIFACT_COUNCIL_VETO','council_id':cid,'role_id':rid,'veto':rr.get('veto')})
    executed={(x.get('council_id'),x.get('artifact_role_id')) for x in inv if x.get('status')=='PASS'}
    missing=[x for x in required if (x['council_id'],x['role_id']) not in executed]
    if missing: errors.append({'kind':'ARTIFACT_COUNCIL_COVERAGE_GAP','missing':missing})
    return {
      'status':'PASS' if not errors else 'BLOCKED','stage':route['stage'],'route':route,
      'required_executions':required,'executed_councils':sorted({x[0] for x in executed}),'executed_role_pairs':sorted([list(x) for x in executed]),'invocations':inv,
      'findings':findings,'errors':errors,'execution_proof':'ISOLATED_ARTIFACT_COUNCIL_INVOCATION_LEDGER',
      'registered_roles_are_not_execution':True
    }
