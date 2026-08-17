from pathlib import Path
import json, hashlib
from PIL import Image

STATES=['INGESTED','CONTENT_LOCKED','GRAPH_LOCKED','ARTIFACT_TRUTH_PASS','EXHIBIT_SEARCH_COMPLETE','WINNER_LOCKED','VISUAL_SEARCH_COMPLETE','CEQS_PASS','PAGE_MASTER_LOCKED','PAGE_QA_PASS']

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def fhash(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def _need(base,rel,errs):
    p=base/rel
    if not p.exists(): errs.append({'kind':'missing_required_evidence','path':rel}); return None
    return p

def _owner(o):
    return str(o.get('owner') or o.get('judge_owner') or o.get('authority_owner') or '').upper()

def _independent(o):
    own=_owner(o)
    if not own: return False
    if any(x in own for x in ['PRODUCER','SELF','AUTHOR']): return False
    if o.get('independent') is not True: return False
    if not o.get('judge_invocation_id'): return False
    if o.get('previous_response_id') or o.get('producer_previous_response_id'): return False
    return True

def _gate_lookup(hr,gid):
    for p in hr.get('pages') or []:
        gs=p.get('gates') or []
        if isinstance(gs,dict):
            g=gs.get(gid) or gs.get(gid.replace('C9_','').lower())
            if g:return g
        else:
            for g in gs:
                if g.get('id')==gid:return g
    return None

def validate_page_dossier_v4(base,critical=True):
    base=Path(base); errs=[]; measured={}
    req=['content_pack.json','relationship_graph.json','artifact_truth.json','exhibit_hypotheses.json','exhibit_selection.json','evidence_pack.json','visual_search/manifest.json','ceqs.json','final_page_master.png','qa/html_report.json','state_transitions.json']
    ps={r:_need(base,r,errs) for r in req}
    if errs:return {'status':'FAIL','verdict':'EXECUTION_CHAIN_BLOCK','errors':errs,'measured':measured}
    objs={r:load(p) for r,p in ps.items() if p and p.suffix=='.json'}
    # Cross-object page identity must be consistent.
    page_ids={r:o.get('page_id') for r,o in objs.items() if isinstance(o,dict) and o.get('page_id')}
    if page_ids and len(set(page_ids.values()))>1: errs.append({'kind':'page_id_mismatch','values':page_ids})
    # Artifact Truth: independent, render-grounded, >=90
    at=objs['artifact_truth.json']; score=float(at.get('artifact_truth_score',at.get('score',0)) or 0); measured['artifact_truth']=score
    if score<90 or at.get('status') not in ('PASS','PROVEN'): errs.append({'kind':'artifact_truth_below_floor','score':score,'floor':90})
    if not _independent(at): errs.append({'kind':'artifact_truth_not_independent','owner':_owner(at)})
    if not (at.get('render_evidence') or at.get('dom_evidence') or at.get('actual_render_hash')): errs.append({'kind':'artifact_truth_not_render_grounded'})
    # Exactly five hypotheses for critical analytical pages
    hyp=objs['exhibit_hypotheses.json']; hs=hyp.get('hypotheses',[]); measured['hypothesis_count']=len(hs)
    if critical and len(hs)!=5: errs.append({'kind':'wrong_hypothesis_count','expected':5,'actual':len(hs)})
    if critical and len(hs)==5:
        sigs={json.dumps({'topology':h.get('topology') or h.get('dominant_form'),'reading_path':h.get('reading_path'),'relation_carriers':h.get('relation_carriers'),'mass_plan':h.get('mass_plan'),'focal_point':h.get('focal_point')},sort_keys=True,ensure_ascii=False) for h in hs}
        measured['hypothesis_distinct_signatures']=len(sigs)
        if len(sigs)<5: errs.append({'kind':'hypotheses_not_materially_distinct','distinct':len(sigs),'required':5})
    sel=objs['exhibit_selection.json']
    if not sel.get('winner') or (critical and len(sel.get('rejected',[]))<4): errs.append({'kind':'selection_rationale_incomplete'})
    # Actual render search and structural diversity
    vm=objs['visual_search/manifest.json']; cands=vm.get('candidates',[]); measured['render_candidate_count']=len(cands)
    if critical and len(cands)<3: errs.append({'kind':'insufficient_render_search','minimum':3,'actual':len(cands)})
    hashes=[]
    for c in cands:
        rel=c.get('path'); p=(base/'visual_search'/rel) if rel else None
        if not p or not p.exists(): errs.append({'kind':'render_candidate_missing','candidate':c})
        else: hashes.append(fhash(p))
    if critical and len(set(hashes))<3: errs.append({'kind':'render_candidates_not_distinct_by_bytes','distinct':len(set(hashes)),'required':3})
    if at.get('actual_render_hash') and hashes and at.get('actual_render_hash') not in hashes:
        errs.append({'kind':'artifact_truth_render_hash_not_bound','actual_render_hash':at.get('actual_render_hash')})
    # Machine-computed render divergence; producer-declared values are not trusted alone.
    pixel_diffs=[]
    try:
        ims=[]
        for c in cands:
            pp=base/'visual_search'/c.get('path','')
            if pp.exists(): ims.append(Image.open(pp).convert('L').resize((128,72)))
        import itertools
        for a,b in itertools.combinations(ims,2):
            pa=list(a.getdata()); pb=list(b.getdata()); pixel_diffs.append(sum(abs(x-y) for x,y in zip(pa,pb))/(255*len(pa)))
    except Exception: pixel_diffs=[]
    machine_min=min(pixel_diffs) if pixel_diffs else 0.0; machine_avg=(sum(pixel_diffs)/len(pixel_diffs)) if pixel_diffs else 0.0
    measured['machine_render_divergence']={'min_pairwise':machine_min,'average_pairwise':machine_avg}
    div=vm.get('structural_divergence') or vm.get('divergence_matrix') or {}
    min_pair=float(div.get('min_pairwise',0) or 0); avg=float(div.get('average_pairwise',0) or 0); measured['structural_divergence']={'min_pairwise':min_pair,'average_pairwise':avg}
    effective_min=min(min_pair,machine_min) if pixel_diffs else min_pair
    effective_avg=min(avg,machine_avg) if pixel_diffs else avg
    if critical and pixel_diffs and (min_pair-machine_min>0.10 or avg-machine_avg>0.10): errs.append({'kind':'declared_divergence_not_supported_by_render','declared':{'min':min_pair,'avg':avg},'machine':{'min':machine_min,'avg':machine_avg}})
    if critical and effective_min<0.12: errs.append({'kind':'structural_divergence_below_critical_floor','actual':effective_min,'floor':0.12})
    if critical and effective_avg<0.18: errs.append({'kind':'structural_divergence_below_target','actual':effective_avg,'target':0.18})
    # CEQS: independent >=90
    ce=objs['ceqs.json']; ceqs=float(ce.get('ceqs',ce.get('score',0)) or 0); measured['ceqs']=ceqs
    if ceqs<90 or ce.get('status') not in ('PASS','PROVEN'): errs.append({'kind':'ceqs_below_floor','score':ceqs,'floor':90})
    if not _independent(ce): errs.append({'kind':'ceqs_not_independent','owner':_owner(ce)})
    if not (ce.get('render_evidence') or ce.get('actual_render_hash') or ce.get('visual_evidence')): errs.append({'kind':'ceqs_not_render_grounded'})
    # Final master
    img=Image.open(ps['final_page_master.png']); measured['master_size']=list(img.size)
    master_hash=fhash(ps['final_page_master.png']); measured['master_sha256']=master_hash
    if ce.get('actual_render_hash') and ce.get('actual_render_hash')!=master_hash: errs.append({'kind':'ceqs_render_hash_not_final_master','declared':ce.get('actual_render_hash'),'actual':master_hash})
    if img.width<3840 or img.height<2160: errs.append({'kind':'master_resolution_below_floor','size':list(img.size),'minimum':[3840,2160]})
    # HTML QA + pixel evidence
    hr=objs['qa/html_report.json']
    if hr.get('release_verdict')!='HTML_PREEXPORT_PASS': errs.append({'kind':'html_qa_not_passed','verdict':hr.get('release_verdict')})
    pixel=_gate_lookup(hr,'C9_PIXEL') or _gate_lookup(hr,'G33_PIXEL')
    if not pixel or pixel.get('status')!='PASS': errs.append({'kind':'pixel_qa_missing_or_failed'})
    elif int(pixel.get('test_count',pixel.get('measured',{}).get('count',0)) or 0)<=0: errs.append({'kind':'pixel_qa_vacuous_pass'})
    # State order
    st=objs['state_transitions.json']; seq=[x.get('state') for x in st if isinstance(x,dict)]; measured['states']=seq; pos=-1
    for s in STATES:
        if s not in seq: errs.append({'kind':'missing_state','state':s}); continue
        i=seq.index(s)
        if i<=pos: errs.append({'kind':'state_order_invalid','state':s})
        pos=i
    # stale hash validation
    hash_targets={'content_pack':'content_pack.json','relationship_graph':'relationship_graph.json','artifact_truth':'artifact_truth.json','exhibit_hypotheses':'exhibit_hypotheses.json','evidence_pack':'evidence_pack.json'}
    for source in [sel,vm,ce,at]:
        for k,v in (source.get('input_hashes',{}) if isinstance(source,dict) else {}).items():
            if k in hash_targets:
                actual=fhash(base/hash_targets[k])
                if actual!=v: errs.append({'kind':'stale_hash','object':k,'expected':v,'actual':actual})
    return {'status':'PASS' if not errs else 'FAIL','verdict':'PAGE_DOSSIER_V4_PASS' if not errs else 'EXECUTION_CHAIN_BLOCK','errors':errs,'measured':measured}

def validate_product_index_v4(index_path):
    ip=Path(index_path); idx=load(ip); root=ip.parent; errs=[]; pages=[]
    if str(idx.get('schema_version')) not in ('7.0.2','7.0.1','4.0','6.1'):
        errs.append({'kind':'unsupported_proof_schema_version','value':idx.get('schema_version')})
    for x in idx.get('pages',[]):
        r=validate_page_dossier_v4(root/x['path'],bool(x.get('critical',True)))
        mp=root/x['path']/'final_page_master.png'
        if mp.exists() and x.get('master_sha256') and fhash(mp)!=x.get('master_sha256'):
            r['status']='FAIL';r['verdict']='EXECUTION_CHAIN_BLOCK';r['errors'].append({'kind':'proof_index_master_hash_mismatch'})
        pages.append({'page_id':x.get('page_id'),'result':r})
        if r['status']!='PASS': errs.append({'kind':'page_dossier_blocked','page_id':x.get('page_id')})
    if not idx.get('pages'): errs.append({'kind':'zero_page_product_proof'})
    return {'status':'PASS' if not errs else 'FAIL','verdict':'PRODUCT_PROOF_V4_PASS' if not errs else 'EXECUTION_CHAIN_BLOCK','errors':errs,'pages':pages}
