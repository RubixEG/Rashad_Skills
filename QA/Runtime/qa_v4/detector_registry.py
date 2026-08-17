from __future__ import annotations
from pathlib import Path
import json, hashlib, re

ROOT=Path(__file__).resolve().parents[1]
TAXONOMY=ROOT/'contracts/v7/failure_taxonomy_v7_0_1.json'
IMPLEMENTATION_REGISTRY=ROOT/'contracts/v7/detector_implementation_registry_v7_3.json'

LOCAL_DETECTORS={
'DOM_TEXT_GEOMETRY','FONT_AND_TEXT_RENDER_METRICS','COMPUTED_FONT_SIZE','PEER_BBOX_COMPARISON','DOM_SCENE_GEOMETRY',
'PEER_PADDING_COMPARISON','PEER_GAP_COMPARISON','PAIRWISE_VISIBLE_INTERSECTION','CANVAS_BBOX_CONTAINMENT','VISIBLE_AREA_CHECK',
'COMPUTED_VISIBILITY_OPACITY','EDGE_ENDPOINT_DISTANCE','SVG_DOM_CONNECTOR_TOPOLOGY','PATH_TEXT_INTERSECTION','EDGE_VISIBLE_GEOMETRY',
'EDGE_CROSSING_COUNT','BIDI_PHYSICAL_ORDER','PHYSICAL_SEQUENCE_COORDINATES','VISIBLE_TEXT_POLICY_SCAN','IMAGE_ASSET_AND_COMPOSITION',
'ASSET_HASH_MATCH','BRAND_TOKEN_AND_ASSET','CLAIM_EVIDENCE_JOIN','HYPOTHESIS_STRUCTURAL_DIVERGENCE','PAIRWISE_STRUCTURAL_DIVERGENCE',
'BEFORE_AFTER_FONT_METRICS','PROOF_PROVENANCE_GATE','MEASUREMENT_COUNT_GATE','MASTER_HASH_LINEAGE','STATE_AND_PROOF_DEPENDENCY',
'QA_PROOF_AND_SIGNATURE_INTEGRITY'
}
SOURCE_DETECTORS={'EVIDENCE_TRACEABILITY','SOURCE_VALUE_EQUALITY'}
JUDGE_DETECTORS={'HYBRID_ARTIFACT_AND_INDEPENDENT_VISUAL_JUDGE','CROSS_DECK_STRUCTURAL_AND_INDEPENDENT_REVIEW'}
STRESS_DETECTORS={'METAMORPHIC_STRESS_RUNNER'}
ALL_DETECTORS=LOCAL_DETECTORS|SOURCE_DETECTORS|JUDGE_DETECTORS|STRESS_DETECTORS

PASS_STATES={'PASS','EXPECTED_BLOCK','NOT_APPLICABLE','N_A'}

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha256(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def taxonomy_hash(): return sha256(TAXONOMY)

def _binding_ok(entry):
    if not isinstance(entry,dict) or entry.get('mode')=='UNIMPLEMENTED': return False
    p=ROOT/str(entry.get('path') or '')
    if not p.exists() or not entry.get('symbol'): return False
    # Static symbol check is deliberate here: runtime imports are exercised by the certification suite.
    txt=p.read_text(encoding='utf-8',errors='ignore')
    return bool(re.search(r'\bdef\s+'+re.escape(str(entry['symbol']))+r'\b',txt))

def implementation_map():
    t=load(TAXONOMY); registry=load(IMPLEMENTATION_REGISTRY); bindings=registry.get('detectors',{}); rows=[]; unknown=[]
    for c in t.get('cases',[]):
        d=c['detector']; entry=bindings.get(d) or {'mode':'UNIMPLEMENTED'}; bound=_binding_ok(entry)
        historical=c.get('implementation_status')
        if bound: mode='IMPLEMENTED_V7_3_EXECUTABLE_OVERLAY'
        else: mode='UNIMPLEMENTED'; unknown.append(c['id'])
        rows.append({'case_id':c['id'],'detector':d,'mode':mode,'historical_taxonomy_status':historical,'binding':entry,'binding_verified':bound,'execution_owner':c.get('execution_owner')})
    return {'status':'PASS' if not unknown else 'FAIL','case_count':len(rows),'implemented':sum(r['mode']!='UNIMPLEMENTED' for r in rows),'unimplemented':unknown,'registry_sha256':sha256(IMPLEMENTATION_REGISTRY),'rows':rows,'truth_rule':'Base SPECIFIED_NOT_IMPLEMENTED is preserved; current implementation claims come only from verified overlay bindings.'}

def _case_runtime_implemented(case):
    registry=load(IMPLEMENTATION_REGISTRY); return _binding_ok((registry.get('detectors') or {}).get(case.get('detector')))

def _independent(ev):
    owner=str(ev.get('owner') or ev.get('judge_owner') or '').upper()
    if not owner or any(x in owner for x in ('PRODUCER','AUTHOR','SELF')): return False
    if ev.get('independent') is not True: return False
    if not ev.get('judge_invocation_id'): return False
    if ev.get('previous_response_id') or ev.get('producer_previous_response_id'): return False
    return True

def _base_provenance(case,ev):
    errors=[]
    if ev.get('case_id')!=case['id']: errors.append('case_id_mismatch')
    if ev.get('detector')!=case['detector']: errors.append('detector_mismatch')
    if ev.get('taxonomy_sha256')!=taxonomy_hash(): errors.append('contract_hash_mismatch')
    if not ev.get('input_hash'): errors.append('missing_input_hash')
    if not ev.get('evidence_id'): errors.append('missing_evidence_id')
    if str(ev.get('owner','')).upper() in {'PRODUCER','AUTHOR','SELF'}: errors.append('producer_owned_evidence')
    measured=int(ev.get('measured_object_count',0) or 0)
    minimum=int(case.get('minimum_measured_objects',0) or 0)
    if ev.get('status')=='PASS' and minimum>0 and measured<minimum: errors.append('vacuous_pass')
    return errors

def validate_case_evidence(case,ev,test_mode=False):
    errors=_base_provenance(case,ev); d=case['detector']
    if d not in ALL_DETECTORS or not _case_runtime_implemented(case): errors.append('detector_not_implemented_or_unbound')
    if d in LOCAL_DETECTORS:
        if ev.get('provenance_type')!='LOCAL_RUNTIME_MEASUREMENT': errors.append('wrong_provenance_type')
        if not ev.get('measurement_payload'): errors.append('missing_measurement_payload')
    elif d in SOURCE_DETECTORS:
        if ev.get('provenance_type')!='SOURCE_VERIFICATION': errors.append('wrong_provenance_type')
        required=['claim_id','source_id','source_sha256','locator','excerpt','reverse_check','entailment_status']
        for k in required:
            if ev.get(k) in (None,''): errors.append('missing_'+k)
        if d=='SOURCE_VALUE_EQUALITY' and ev.get('value_match') is not True: errors.append('source_value_not_equal')
        if ev.get('reverse_check') is not True: errors.append('reverse_check_failed')
        if ev.get('entailment_status') not in ('SUPPORTED','EXACT','PASS'): errors.append('entailment_failed')
    elif d in JUDGE_DETECTORS:
        if ev.get('provenance_type')!='INDEPENDENT_JUDGE': errors.append('wrong_provenance_type')
        if not _independent(ev): errors.append('judge_not_independent')
        if not (ev.get('actual_render_hash') or ev.get('deck_hash')): errors.append('judge_not_render_grounded')
        score=float(ev.get('score',0) or 0)
        if score<90: errors.append('judge_score_below_90')
        if test_mode and not str(ev.get('judge_invocation_id','')).startswith('TEST-'): errors.append('test_judge_signature_missing')
    elif d in STRESS_DETECTORS:
        if ev.get('provenance_type')!='METAMORPHIC_RUNNER': errors.append('wrong_provenance_type')
        if not ev.get('mutation_id') or not ev.get('mutated_input_hash'): errors.append('stress_execution_not_proven')
        if not ev.get('before_hash') or not ev.get('after_hash'): errors.append('stress_lineage_missing')
    st='PASS' if not errors and ev.get('status') in PASS_STATES else 'FAIL'
    if ev.get('status') not in PASS_STATES: errors.append('case_not_passed')
    return {'case_id':case['id'],'status':st,'errors':sorted(set(errors)),'detector':d,'evidence_id':ev.get('evidence_id')}

def validate_results_dir(results_dir, applicability=None, test_mode=False):
    results_dir=Path(results_dir); t=load(TAXONOMY); applicability=applicability or {}; rows=[]; blockers=[]
    for c in t.get('cases',[]):
        cid=c['id']
        if applicability.get(cid,True) is False:
            rows.append({'case_id':cid,'status':'NOT_APPLICABLE','errors':[]}); continue
        p=results_dir/f'{cid}.json'
        if not p.exists():
            r={'case_id':cid,'status':'FAIL','errors':['FAIL_NOT_INSTRUMENTED'],'detector':c['detector']}
        else:
            try:r=validate_case_evidence(c,load(p),test_mode=test_mode)
            except Exception as e:r={'case_id':cid,'status':'FAIL','errors':['invalid_evidence:'+str(e)],'detector':c['detector']}
        rows.append(r)
        if r['status']!='PASS': blockers.append(r)
    return {'status':'PASS' if not blockers else 'FAIL','verdict':'TOTAL_QUALITY_CASES_PASS' if not blockers else 'BLOCKED','case_count':len(rows),'passed':sum(r['status']=='PASS' for r in rows),'blockers':blockers,'cases':rows}
