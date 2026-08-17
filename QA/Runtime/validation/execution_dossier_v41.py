from pathlib import Path
import json
from validation.execution_dossier_v4 import validate_page_dossier_v4
from brain.coverage import validate_session

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def validate_page_dossier_v41(base,critical=True):
    base=Path(base); r=validate_page_dossier_v4(base,critical); errs=list(r.get('errors',[])); measured=dict(r.get('measured',{}))
    bp=base/'brain_session.json'
    if not bp.exists():
        errs.append({'kind':'brain_session_missing'})
    else:
        b=load(bp); cov=validate_session(b); measured['brain_state']=b.get('state'); measured['brain_route']=b.get('route',[]); measured['brain_coverage']=cov
        if cov.get('status')!='PASS': errs.append({'kind':'brain_council_coverage_failed','errors':cov.get('errors',[])})
        if b.get('state') not in ('COGNITIVE_LOCKED','ARTIFACT_SEARCHED','JUDGED','QA_CANDIDATE_PASS','RELEASED'):
            errs.append({'kind':'brain_state_not_locked','state':b.get('state')})
        if critical:
            for cid in ('C03_EPISTEMIC_TRUTH','C13_ADVERSARIAL_COUNTERFACTUAL','C15_META_COGNITION_INTEGRITY'):
                if cid not in b.get('route',[]): errs.append({'kind':'critical_brain_council_missing','council_id':cid})
    return {'status':'PASS' if not errs else 'FAIL','verdict':'PAGE_DOSSIER_V41_BRAIN_PASS' if not errs else 'EXECUTION_CHAIN_BLOCK','errors':errs,'measured':measured}

def validate_product_index_v41(index_path):
    ip=Path(index_path); idx=load(ip); root=ip.parent; errs=[]; pages=[]
    if str(idx.get('schema_version')) not in ('7.0.2','7.0.1','4.0','6.1'): errs.append({'kind':'unsupported_proof_schema_version','value':idx.get('schema_version')})
    for x in idx.get('pages',[]):
        rr=validate_page_dossier_v41(root/x['path'],bool(x.get('critical',True))); pages.append({'page_id':x.get('page_id'),'result':rr})
        if rr['status']!='PASS': errs.append({'kind':'page_dossier_blocked','page_id':x.get('page_id')})
    if not idx.get('pages'): errs.append({'kind':'zero_page_product_proof'})
    return {'status':'PASS' if not errs else 'FAIL','verdict':'PRODUCT_PROOF_V41_BRAIN_PASS' if not errs else 'EXECUTION_CHAIN_BLOCK','errors':errs,'pages':pages}
