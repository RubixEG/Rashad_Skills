#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path
from jsonschema import Draft202012Validator

HERE=Path(__file__).resolve()
RASHAD_ROOT=HERE.parents[2]
SKILL=RASHAD_ROOT/'Skill'
SCHEMAS=SKILL/'schemas'
ROLE_REGISTRY=SKILL/'01_ACTIVE_RUNTIME/rfp_summary_role_registry_v7.json'
STEPS=[f'{i:02d}' for i in range(1,16)]
REQUIRED_REGISTERS=['document_inventory','requirement_register','evaluation_criteria_register','submission_condition_register','deliverables_register','contract_obligation_register','assumption_exclusion_clarification_register','evidence_ledger','claim_commitment_register','contradiction_register','language_terminology_register']
MATERIAL_CATEGORIES={'MAIN_BOOKLET','SCOPE','BOQ','EVALUATION','QUALIFICATION','TEAM','CONTRACT','PAYMENT','SUBMISSION'}
TECH_CATEGORIES={'CYBERSECURITY','TECHNICAL_REQUIREMENTS','SOFTWARE_REQUIREMENTS'}
CLOSED_ROUTING=['CHECK_ETIMAD_QA','CHECK_ADDENDA','BID_ASSUMPTION','DEPENDENCY','COMMERCIAL_PROTECTION','CONTRACT_RECONCILIATION']

def _load(rel): return json.loads((SCHEMAS/rel).read_text(encoding='utf-8'))
def _errors(schema_name,obj):
    return [e.message for e in Draft202012Validator(_load(schema_name)).iter_errors(obj)]
def _iso(s):
    if not s: return None
    try: return datetime.fromisoformat(s.replace('Z','+00:00'))
    except Exception: return None

def derive_pack_mode(source_manifest, missing_annexes):
    cats={x.get('category') for x in source_manifest if x.get('availability')=='AVAILABLE'}
    material_missing=[x.get('reference') for x in missing_annexes if x.get('material')]
    if 'SCOPE' in cats and len(cats-{'MAIN_BOOKLET','SCOPE','OTHER'})==0:
        mode='SCOPE_ONLY'; rationale='Only scope/main-booklet evidence is materially available; downstream commercial/evaluation facts must not be invented.'
    else:
        full=(MATERIAL_CATEGORIES<=cats and bool(cats&TECH_CATEGORIES) and not material_missing)
        mode='FULL_RFP_PACK' if full else 'PARTIAL_RFP_PACK'
        rationale='Material annex categories are sufficiently represented for a full brief.' if full else 'One or more material evidence categories or referenced material sources are absent; stricter partial-pack mode applies.'
    return {'source_pack_mode':mode,'source_pack_mode_basis':{'detected_categories':sorted(c for c in cats if c),'material_missing_sources':material_missing,'rationale':rationale,'stricter_mode_applied':mode!='FULL_RFP_PACK'}}

def derive_clarification_window(evidence, evaluated_at=None):
    evaluated_at=evaluated_at or datetime.now(timezone.utc).isoformat()
    now=_iso(evaluated_at) or datetime.now(timezone.utc)
    conflict=bool(evidence.get('conflict'))
    notes=list(evidence.get('conflict_notes',[]))
    addenda=[x for x in evidence.get('addenda',[]) if x.get('verified')]
    pack=evidence.get('pack_deadline') or {}
    meta=evidence.get('tender_metadata') or {}
    selected=None; method='NO_VERIFIED_DEADLINE'; addrefs=[]
    if addenda:
        selected=sorted(addenda,key=lambda x:x.get('sequence',0))[-1]; method='LATEST_VERIFIED_ADDENDUM'; addrefs=list(selected.get('source_refs',[]))
    elif pack.get('verified'):
        selected=pack; method='VERIFIED_PROCUREMENT_PACK_DEADLINE'
    elif meta.get('verified'):
        selected=meta; method='VERIFIED_TENDER_METADATA_FALLBACK'
    if not selected:
        return {'status':'UNKNOWN','deadline_source_value':None,'deadline_source_calendar':None,'deadline_source_refs':[],'deadline_normalized_gregorian':None,'addendum_source_refs':[], 'evaluated_at':evaluated_at,'derivation_method':method,'confidence':0.0,'conflict':conflict,'conflict_notes':notes,'closed_routing':[]}
    norm=selected.get('deadline_normalized_gregorian'); dt=_iso(norm)
    if dt is None: status='UNKNOWN'
    elif method=='LATEST_VERIFIED_ADDENDUM' and dt>=now: status='EXTENDED'
    else: status='OPEN' if dt>=now else 'CLOSED'
    conf=1.0 if method in ('LATEST_VERIFIED_ADDENDUM','VERIFIED_PROCUREMENT_PACK_DEADLINE') else .65
    return {'status':status,'deadline_source_value':selected.get('deadline_source_value'),'deadline_source_calendar':selected.get('deadline_source_calendar'),'deadline_source_refs':list(selected.get('source_refs',[])),'deadline_normalized_gregorian':norm,'addendum_source_refs':addrefs,'evaluated_at':evaluated_at,'derivation_method':method,'confidence':conf,'conflict':conflict,'conflict_notes':notes,'closed_routing':CLOSED_ROUTING if status=='CLOSED' else []}

def validate_ingestion_state(state): return _errors('rfp_ingestion_state_v7.schema.json',state)
def validate_decision(decision): return _errors('rfp_bid_decision_evidence_v7.schema.json',decision)
def canonical_roles():
    d=json.loads(ROLE_REGISTRY.read_text(encoding='utf-8')); return [x['canonical_id'] for x in sorted(d['roles'],key=lambda x:x['sequence'])]
def _pass(detail=None): return {'status':'PASS','detail':detail or {}}
def _block(reason,detail=None): return {'status':'BLOCKED','reason':reason,'detail':detail or {}}
def _not(reason,detail=None): return {'status':'NOT_EXECUTED','reason':reason,'detail':detail or {}}

def evaluate_step(state, n):
    n=int(n); roles=canonical_roles(); analytical=state.get('analytical_page_ids',[]); critical=state.get('critical_page_ids',[])
    if n==1:
        a=state.get('engagement_reset',{}); b=state.get('source_accountability',{})
        return _pass() if a.get('status')=='PASS' and b.get('status')=='PASS' else _block('ENGAGEMENT_RESET_OR_SOURCE_ACCOUNTABILITY_MISSING')
    if n==2:
        cfg=state.get('output_config',{}); locked=state.get('canonical_role_order',[])
        return _pass({'language':cfg.get('language')}) if cfg.get('language') and locked==roles else _block('LANGUAGE_OR_24_ROLE_LOCK_INVALID',{'role_count':len(locked)})
    if n==3:
        ing=state.get('ingestion_state') or {}; errs=validate_ingestion_state(ing)
        if errs: return _block('INGESTION_MACHINE_STATE_INVALID',{'errors':errs[:20]})
        expected=derive_pack_mode(ing.get('source_manifest',[]),ing.get('missing_annexes',[]))
        if ing.get('source_pack_mode')!=expected.get('source_pack_mode'):
            return _block('SOURCE_PACK_MODE_INCONSISTENT_WITH_EVIDENCE',{'stored':ing.get('source_pack_mode'),'derived':expected.get('source_pack_mode')})
        cw=derive_clarification_window(ing.get('clarification_evidence',{}),ing.get('clarification_window_state',{}).get('evaluated_at'))
        if ing.get('clarification_window_state',{}).get('status')!=cw.get('status'):
            return _block('CLARIFICATION_WINDOW_INCONSISTENT_WITH_VERIFIED_INPUTS',{'stored':ing.get('clarification_window_state',{}).get('status'),'derived':cw.get('status')})
        return _pass({'pack_mode':ing.get('source_pack_mode'),'registers':len(ing.get('registers',{})),'clarification_window':ing.get('clarification_window_state',{}).get('status')})
    if n==4:
        plan=state.get('role_plan',[]); ids=[x.get('role_id') for x in plan]
        ok=ids==roles and all(x.get('applicability') in ('APPLICABLE','REQUIRED','NOT_APPLICABLE_WITH_EVIDENCE') and x.get('depth') in ('STANDARD','EXPANDED','CONDENSED') for x in plan)
        return _pass({'roles':24}) if ok else _block('ROLE_APPLICABILITY_DEPTH_PLAN_INVALID')
    if n==5:
        outs=state.get('role_outputs',{}); missing=[]
        for p in state.get('role_plan',[]):
            if p.get('applicability')=='NOT_APPLICABLE_WITH_EVIDENCE': continue
            o=outs.get(p.get('role_id')) or {}
            if not all(o.get(k) for k in ('mandatory_content','required_analysis','evidence_refs','management_implication')): missing.append(p.get('role_id'))
        return _pass() if not missing else _block('ROLE_CONTRACT_OUTPUTS_INCOMPLETE',{'missing':missing})
    if n==6:
        cps=state.get('cognitive_packets',{}); schema=_load('consulting_cognitive_packet_v7.schema.json'); v=Draft202012Validator(schema); bad=[]
        for pid in analytical:
            if pid not in cps: bad.append({'page_id':pid,'error':'MISSING'})
            else:
                es=list(v.iter_errors(cps[pid]));
                if es: bad.append({'page_id':pid,'error':es[0].message})
        return _pass({'packets':len(analytical)}) if not bad else _block('COGNITIVE_PACKETS_MISSING_OR_INVALID',{'errors':bad})
    if n==7:
        sessions=state.get('council_sessions',{}); bad=[]
        for pid in analytical:
            s=sessions.get(pid) or {}
            if s.get('status')!='PASS': bad.append({'page_id':pid,'reason':'SESSION_NOT_PASS'}); continue
            if not s.get('producer_actor_id') or not s.get('judge_actor_id') or s.get('producer_actor_id')==s.get('judge_actor_id'): bad.append({'page_id':pid,'reason':'INDEPENDENCE_INVALID'})
            if s.get('open_p0_p1',0): bad.append({'page_id':pid,'reason':'OPEN_P0_P1'})
        return _pass({'sessions':len(analytical)}) if not bad else _block('COUNCIL_EXECUTION_INCOMPLETE',{'errors':bad})
    if n==8:
        packs=state.get('page_content_packs',{}); graphs=state.get('semantic_graphs',{}); missing=[pid for pid in analytical if pid not in packs or pid not in graphs]
        return _pass() if not missing else _block('PAGE_PACK_OR_SEMANTIC_GRAPH_MISSING',{'pages':missing})
    if n==9:
        vs=state.get('visual_search',{}); bad=[]
        for pid in critical:
            h=(vs.get(pid) or {}).get('hypotheses',[]); sig={x.get('structural_signature') for x in h}
            if len(h)!=5 or len(sig)!=5: bad.append({'page_id':pid,'hypotheses':len(h),'distinct':len(sig)})
        return _pass() if not bad else _block('FIVE_MATERIAL_HYPOTHESES_NOT_PROVEN',{'errors':bad})
    if n==10:
        vs=state.get('visual_search',{}); bad=[]
        for pid in critical:
            renders=(vs.get(pid) or {}).get('renders',[]); hashes=[r.get('actual_render_hash') for r in renders]
            if len(renders)<5 or any(not r.get('actual_render_hash') or not r.get('render_path') for r in renders) or len(set(hashes))<5: bad.append({'page_id':pid,'renders':len(renders),'distinct_hashes':len(set(hashes))})
        return _pass() if not bad else _not('ALL_FIVE_ACTUAL_RENDERS_REQUIRED',{'errors':bad})
    if n==11:
        vs=state.get('visual_search',{}); bad=[]
        for pid in critical:
            v=vs.get(pid) or {}; js=v.get('initial_independent_judgments',[]); refined=v.get('refined_renders',[]); final=v.get('final_independent_judgment') or {}
            render_by={r.get('candidate_id'):r.get('actual_render_hash') for r in v.get('renders',[])}
            ids={x.get('candidate_id') for x in js if x.get('independent') is True and x.get('judge_invocation_id') and not x.get('previous_response_id') and x.get('actual_render_hash')==render_by.get(x.get('candidate_id'))}
            refined_hashes={r.get('actual_render_hash') for r in refined}
            final_hash=final.get('actual_render_hash')
            if len(ids)<5 or len(refined)!=4 or len(refined_hashes)!=4 or final.get('independent') is not True or not final.get('judge_invocation_id') or not final.get('winner_candidate_id') or final_hash not in refined_hashes:
                bad.append({'page_id':pid,'initial_judged':len(ids),'refined':len(refined),'distinct_refined':len(refined_hashes),'final':bool(final)})
        return _pass() if not bad else _not('INDEPENDENT_5_TO_9_VISUAL_SEARCH_INCOMPLETE',{'errors':bad})
    if n==12:
        qa=state.get('qa_results',{}); bad=[]
        for pid in critical:
            q=qa.get(pid) or {}
            if q.get('artifact_truth_score',0)<90 or q.get('ceqs_score',0)<90 or q.get('required_detector_status')!='PASS': bad.append(pid)
        return _pass() if not bad else _not('ARTIFACT_TRUTH_CEQS_OR_DETECTORS_INCOMPLETE',{'pages':bad})
    if n==13:
        q=state.get('deck_qa',{}); ok=all(q.get(k)=='PASS' for k in ('stress','repair_safety','cross_deck'))
        return _pass() if ok else _not('STRESS_REPAIR_OR_CROSS_DECK_QA_INCOMPLETE')
    if n==14:
        d=state.get('decision'); errs=validate_decision(d) if isinstance(d,dict) else ['decision missing']
        return _pass({'recommendation':d.get('recommendation') if isinstance(d,dict) else None}) if not errs else _block('BID_DECISION_OBJECT_INVALID',{'errors':errs[:20]})
    if n==15:
        r=state.get('release',{}); ok=r.get('masters_frozen') is True and r.get('pdf_pptx_parity')=='PASS' and r.get('proof_index')=='PASS' and r.get('release_chair_status')=='RELEASED' and r.get('qa_status')=='QA_CANDIDATE_PASS'
        return _pass() if ok else _not('FINAL_MASTER_PARITY_PROOF_OR_RELEASE_CHAIR_INCOMPLETE')
    return _block('UNKNOWN_STEP')

def evaluate_pipeline(state):
    top=_errors('rfp_summary_execution_state_v7.schema.json',state)
    if top: return {'status':'BLOCKED','reason':'EXECUTION_STATE_SCHEMA_INVALID','errors':top[:20],'steps':{}}
    out={}; upstream=True
    for sid in STEPS:
        if not upstream:
            out[sid]=_not('UPSTREAM_STEP_NOT_PASS')
            continue
        out[sid]=evaluate_step(state,sid)
        if out[sid]['status']!='PASS': upstream=False
    passed=sum(1 for x in out.values() if x['status']=='PASS')
    payload={'status':'PASS' if passed==15 else 'BLOCKED','passed_steps':passed,'total_steps':15,'first_non_pass':next((k for k,v in out.items() if v['status']!='PASS'),None),'steps':out}
    payload['execution_evidence_hash']=hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return payload

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    p=sub.add_parser('validate'); p.add_argument('--state',required=True); p.add_argument('--out')
    p=sub.add_parser('derive-pack-mode'); p.add_argument('--input',required=True)
    p=sub.add_parser('derive-clarification-window'); p.add_argument('--input',required=True); p.add_argument('--evaluated-at')
    a=ap.parse_args()
    if a.cmd=='validate':
        s=json.loads(Path(a.state).read_text(encoding='utf-8')); r=evaluate_pipeline(s)
        if a.out: Path(a.out).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(r,ensure_ascii=False,indent=2)); raise SystemExit(0 if r['status']=='PASS' else 2)
    d=json.loads(Path(a.input).read_text(encoding='utf-8'))
    if a.cmd=='derive-pack-mode': r=derive_pack_mode(d.get('source_manifest',[]),d.get('missing_annexes',[]))
    else: r=derive_clarification_window(d,a.evaluated_at)
    print(json.dumps(r,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
