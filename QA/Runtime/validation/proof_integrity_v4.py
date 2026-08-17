from pathlib import Path
import json, hashlib

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def h(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def validate_proof_integrity(root):
    root=Path(root); checks=[]; blockers=[]
    def add(cid,ok,detail):
        checks.append({'id':cid,'status':'PASS' if ok else 'FAIL','detail':detail})
        if not ok:blockers.append({'id':cid,'detail':detail})
    # 20 product-integrity checks. These are intentionally evidence-oriented.
    pi=root/'proof_index.json'; add('PI-001',pi.exists(),'proof_index exists')
    idx=load(pi) if pi.exists() else {}
    pages=idx.get('pages',[]); add('PI-002',len(pages)>0,f'page_count={len(pages)}')
    for i,x in enumerate(pages):
        p=root/x.get('path',''); add(f'PI-003.{i+1}',p.exists(),str(p))
        m=p/'final_page_master.png'; add(f'PI-004.{i+1}',m.exists(),'master exists')
        if m.exists() and x.get('master_sha256'): add(f'PI-005.{i+1}',h(m)==x['master_sha256'],'master hash bound')
        st=p/'state_transitions.json'; add(f'PI-006.{i+1}',st.exists(),'state transitions exist')
        qa=p/'qa/html_report.json'; add(f'PI-007.{i+1}',qa.exists(),'html QA exists')
        at=p/'artifact_truth.json'; add(f'PI-008.{i+1}',at.exists(),'artifact truth exists')
        ce=p/'ceqs.json'; add(f'PI-009.{i+1}',ce.exists(),'CEQS exists')
        # Repair safety evidence is mandatory only when repair declared.
        rb=p/'repair_before.json'; ra=p/'repair_after.json'
        if rb.exists() or ra.exists(): add(f'PI-010.{i+1}',rb.exists() and ra.exists(),'repair signatures paired')
    # product-wide evidence
    add('PI-011',(root/'firewall.json').exists(),'firewall evidence')
    add('PI-012',(root/'masters').exists(),'common masters directory')
    add('PI-013',(root/'final.pdf').exists(),'PDF artifact')
    add('PI-014',(root/'final.pptx').exists(),'PPTX artifact')
    add('PI-015',(root/'qa_cases').exists(),'case evidence directory')
    add('PI-016',(root/'stress_v7').exists(),'stress evidence directory')
    add('PI-017',(root/'release_state.json').exists(),'release state evidence')
    if (root/'release_state.json').exists():
        rs=load(root/'release_state.json'); add('PI-018',rs.get('status') not in ('RELEASED','PASS') or bool(rs.get('release_evidence_refs')),'no unsupported release state')
    add('PI-019',not (root/'manual_PASS.txt').exists(),'no manual PASS override')
    add('PI-020',not (root/'producer_release.json').exists(),'no producer release authority artifact')
    return {'status':'PASS' if not blockers else 'FAIL','verdict':'PROOF_INTEGRITY_V4_PASS' if not blockers else 'BLOCKED','checks':checks,'blockers':blockers}
