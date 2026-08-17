from __future__ import annotations
from pathlib import Path
import json, hashlib

ROOT=Path(__file__).resolve().parents[1]
TAXONOMY=ROOT/'contracts/v7/failure_taxonomy_v7_0_1.json'
FAMILIES=ROOT/'contracts/v7/artifact_family_qa_matrix_v7.json'
STRESS=ROOT/'contracts/v7/stress_chaos_matrix_v7.json'

PASS_STATES={'PASS','N_A','NOT_APPLICABLE'}
BLOCK_STATES={'FAIL','BLOCKED','FAIL_NOT_INSTRUMENTED','NOT_EXECUTED','STALE','INVALID'}

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha256(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def taxonomy_audit():
    t=load(TAXONOMY); cases=t.get('cases',[]); errors=[]
    ids=[]
    required=['id','category','description','severity','detector','measurement','threshold','applicability','minimum_measured_objects','test_fixture','evidence_output','execution_owner','not_instrumented_result','implementation_status']
    for c in cases:
        ids.append(c.get('id'))
        miss=[k for k in required if k not in c or c.get(k) in (None,'')]
        if miss: errors.append({'case':c.get('id'),'kind':'missing_detector_contract_fields','fields':miss})
        if c.get('not_instrumented_result')!='FAIL_NOT_INSTRUMENTED':
            errors.append({'case':c.get('id'),'kind':'unsafe_not_instrumented_result','value':c.get('not_instrumented_result')})
    if len(set(ids))!=len(ids): errors.append({'kind':'duplicate_case_ids'})
    if len(cases)!=t.get('case_count'): errors.append({'kind':'case_count_mismatch','declared':t.get('case_count'),'actual':len(cases)})
    f=load(FAMILIES); s=load(STRESS)
    if len(f.get('families',{}))!=f.get('family_count'): errors.append({'kind':'family_count_mismatch'})
    if len(s.get('required_mutations',[]))!=20: errors.append({'kind':'stress_mutation_count_mismatch','actual':len(s.get('required_mutations',[]))})
    from .detector_registry import implementation_map
    impl=implementation_map()
    if impl.get('status')!='PASS': errors.append({'kind':'detector_implementation_overlay_incomplete','unimplemented_count':len(impl.get('unimplemented',[]))})
    return {'status':'PASS' if not errors else 'FAIL','verdict':'TAXONOMY_CONTRACT_PASS' if not errors else 'BLOCKED','counts':{'cases':len(cases),'families':len(f.get('families',{})),'stress_mutations':len(s.get('required_mutations',[])),'implemented_overlay':impl.get('implemented',0),'unimplemented_overlay':len(impl.get('unimplemented',[]))},'implementation_overlay_status':impl.get('status'),'errors':errors,'contract_hashes':{'taxonomy':sha256(TAXONOMY),'families':sha256(FAMILIES),'stress':sha256(STRESS)}}

def validate_case_results_legacy(results_dir: str|Path, applicability: dict|None=None):
    """Fail-closed aggregator for the 233 case contracts.
    Runtime detectors may live in different modules, but every applicable case must emit evidence.
    A case cannot PASS with fewer measured objects than its contract minimum.
    """
    results_dir=Path(results_dir); t=load(TAXONOMY); applicability=applicability or {}
    rows=[]; blockers=[]
    for c in t.get('cases',[]):
        cid=c['id']; p=results_dir/f'{cid}.json'; app=applicability.get(cid, True)
        if not app:
            rows.append({'id':cid,'status':'NOT_APPLICABLE','evidence':None}); continue
        if not p.exists():
            st='FAIL_NOT_INSTRUMENTED'; rows.append({'id':cid,'status':st,'evidence':None}); blockers.append({'id':cid,'kind':'missing_case_evidence'}); continue
        try: r=load(p)
        except Exception as e:
            rows.append({'id':cid,'status':'INVALID','evidence':str(p)}); blockers.append({'id':cid,'kind':'invalid_case_evidence','error':str(e)}); continue
        st=r.get('status','INVALID'); measured=int(r.get('measured_object_count',r.get('measured',{}).get('count',0)) or 0)
        min_m=int(c.get('minimum_measured_objects',0) or 0)
        if st=='PASS' and min_m>0 and measured<min_m:
            st='FAIL_NOT_INSTRUMENTED'; blockers.append({'id':cid,'kind':'vacuous_pass','measured':measured,'required':min_m})
        if st not in PASS_STATES:
            blockers.append({'id':cid,'kind':'case_not_passed','status':st})
        rows.append({'id':cid,'status':st,'measured_object_count':measured,'evidence':str(p),'sha256':sha256(p)})
    return {'status':'PASS' if not blockers else 'FAIL','verdict':'TOTAL_QUALITY_CASES_PASS' if not blockers else 'BLOCKED','case_count':len(rows),'blockers':blockers,'cases':rows}

def validate_artifact_family(family: str, evidence_file: str|Path):
    m=load(FAMILIES); fam=m.get('families',{}).get(family)
    if not fam: return {'status':'FAIL','verdict':'BLOCKED','errors':[{'kind':'unknown_artifact_family','family':family}]}
    r=load(evidence_file); executed=set(r.get('checks_executed',[])); expected=set(fam.get('checks',[]))
    missing=sorted(expected-executed); errors=[]
    if missing: errors.append({'kind':'family_checks_not_executed','missing':missing})
    if r.get('status')!='PASS': errors.append({'kind':'family_evidence_not_passed','status':r.get('status')})
    return {'status':'PASS' if not errors else 'FAIL','verdict':'ARTIFACT_FAMILY_PASS' if not errors else 'BLOCKED','family':family,'required_checks':sorted(expected),'errors':errors}


# FINAL runtime validator: provenance-bound detector registry, no bare PASS JSON.
def validate_case_results(results_dir: str|Path, applicability: dict|None=None, test_mode=False):
    from .detector_registry import validate_results_dir
    return validate_results_dir(results_dir,applicability,test_mode=test_mode)
