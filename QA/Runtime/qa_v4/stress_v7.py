from pathlib import Path
import json, hashlib
from .taxonomy_runtime import STRESS, load

def sha256(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def validate_stress_evidence(evidence_dir):
    evidence_dir=Path(evidence_dir); spec=load(STRESS); errors=[]; rows=[]
    for m in spec.get('required_mutations',[]):
        mid=m['id']; p=evidence_dir/f'{mid}.json'
        if not p.exists():
            errors.append({'id':mid,'kind':'stress_not_executed'}); rows.append({'id':mid,'status':'NOT_EXECUTED'}); continue
        try:r=load(p)
        except Exception as e:
            errors.append({'id':mid,'kind':'invalid_stress_evidence','error':str(e)}); rows.append({'id':mid,'status':'INVALID'}); continue
        st=r.get('status'); measured=r.get('measured_object_count',r.get('measured',{}).get('count',0))
        if st=='PASS' and not r.get('input_hash'):
            errors.append({'id':mid,'kind':'stress_missing_input_hash'})
        if st not in ('PASS','EXPECTED_BLOCK'):
            errors.append({'id':mid,'kind':'stress_not_satisfied','status':st})
        rows.append({'id':mid,'status':st,'measured_object_count':measured,'sha256':sha256(p)})
    return {'status':'PASS' if not errors else 'FAIL','verdict':'STRESS_V7_PASS' if not errors else 'BLOCKED','required':len(spec.get('required_mutations',[])),'errors':errors,'mutations':rows}
