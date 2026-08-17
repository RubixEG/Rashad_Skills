from pathlib import Path
import json,hashlib
from PIL import Image
STATES=['INGESTED','CONTENT_LOCKED','GRAPH_LOCKED','ARTIFACT_TRUTH_PASS','EXHIBIT_SEARCH_COMPLETE','WINNER_LOCKED','VISUAL_SEARCH_COMPLETE','CEQS_PASS','PAGE_MASTER_LOCKED','PAGE_QA_PASS']
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def fhash(p):
 h=hashlib.sha256(); h.update(Path(p).read_bytes()); return h.hexdigest()
def _need(base,rel,errs):
 p=base/rel
 if not p.exists(): errs.append({'kind':'missing_required_evidence','path':rel}); return None
 return p
def validate_page_dossier(base,critical=True):
 base=Path(base); errs=[]; measured={}
 req=['content_pack.json','relationship_graph.json','artifact_truth.json','exhibit_hypotheses.json','exhibit_selection.json','evidence_pack.json','visual_search/manifest.json','ceqs.json','final_page_master.png','qa/html_report.json','state_transitions.json']
 ps={r:_need(base,r,errs) for r in req}
 if errs: return {'status':'FAIL','verdict':'EXECUTION_CHAIN_BLOCK','errors':errs,'measured':measured}
 objs={r:load(p) for r,p in ps.items() if p and p.suffix=='.json'}
 page_ids=[]
 for r,o in objs.items():
  if isinstance(o,dict) and o.get('page_id'): page_ids.append((r,o['page_id']))
 if page_ids:
  ids={x[1] for x in page_ids}; measured['page_ids']=page_ids
  if len(ids)>1: errs.append({'kind':'page_id_mismatch','values':page_ids})
 at=objs['artifact_truth.json']; score=float(at.get('artifact_truth_score',at.get('score',0))); measured['artifact_truth']=score
 if score<85 or at.get('status') not in ('PASS','PROVEN'): errs.append({'kind':'artifact_truth_below_floor','score':score})
 hyp=objs['exhibit_hypotheses.json']; hs=hyp.get('hypotheses',[]); measured['hypothesis_count']=len(hs)
 if critical and len(hs)!=5: errs.append({'kind':'wrong_hypothesis_count','expected':5,'actual':len(hs)})
 if critical and len(hs)==5:
  sigs={json.dumps({'dominant_form':h.get('dominant_form'),'reading_path':h.get('reading_path'),'relation_carriers':h.get('relation_carriers'),'mass_plan':h.get('mass_plan')},sort_keys=True,ensure_ascii=False) for h in hs}
  measured['hypothesis_distinct_signatures']=len(sigs)
  if len(sigs)<5: errs.append({'kind':'hypotheses_not_materially_distinct','distinct':len(sigs),'required':5})
 sel=objs['exhibit_selection.json'];
 if not sel.get('winner') or len(sel.get('rejected',[])) < (4 if critical else 0): errs.append({'kind':'selection_rationale_incomplete'})
 vm=objs['visual_search/manifest.json']; cands=vm.get('candidates',[]); measured['render_candidate_count']=len(cands)
 if critical and len(cands)<3: errs.append({'kind':'insufficient_render_search','minimum':3,'actual':len(cands)})
 candidate_hashes=[]
 for c in cands:
  rel=c.get('path');
  if not rel or not (base/'visual_search'/rel).exists(): errs.append({'kind':'render_candidate_missing','candidate':c})
  else: candidate_hashes.append(fhash(base/'visual_search'/rel))
 if critical and len(set(candidate_hashes))<3: errs.append({'kind':'render_candidates_not_distinct','distinct':len(set(candidate_hashes)),'required':3})
 measured['render_candidate_distinct_hashes']=len(set(candidate_hashes))
 ce=objs['ceqs.json']; ceqs=float(ce.get('ceqs',ce.get('score',0))); measured['ceqs']=ceqs
 if ceqs<90 or ce.get('status') not in ('PASS','PROVEN'): errs.append({'kind':'ceqs_below_floor','score':ceqs})
 img=Image.open(ps['final_page_master.png']); measured['master_size']=list(img.size)
 if img.width<3840 or img.height<2160: errs.append({'kind':'master_resolution_below_floor','size':list(img.size)})
 hr=objs['qa/html_report.json'];
 if hr.get('release_verdict')!='HTML_PREEXPORT_PASS': errs.append({'kind':'html_qa_not_passed','verdict':hr.get('release_verdict')})
 # pixel evidence must be present in the unified report
 pages=hr.get('pages') or []
 if pages:
  gates=pages[0].get('gates',{}) if isinstance(pages[0],dict) else {}
  pixel=gates.get('C9_PIXEL') or gates.get('pixel')
  if not pixel or pixel.get('status')!='PASS': errs.append({'kind':'pixel_qa_missing_or_failed'})
 # State transitions ordered and complete through PAGE_QA_PASS
 st=objs['state_transitions.json']; seq=[x.get('state') for x in st if isinstance(x,dict)]; measured['states']=seq
 pos=-1
 for s in STATES:
  if s not in seq: errs.append({'kind':'missing_state','state':s}); continue
  i=seq.index(s)
  if i<=pos: errs.append({'kind':'state_order_invalid','state':s})
  pos=i
 # Optional declared hashes in selection/manifest/ceqs/master records are checked where present
 hash_targets={'content_pack':'content_pack.json','relationship_graph':'relationship_graph.json','artifact_truth':'artifact_truth.json','exhibit_hypotheses':'exhibit_hypotheses.json','evidence_pack':'evidence_pack.json'}
 for source in [sel,vm,ce]:
  ih=source.get('input_hashes',{}) if isinstance(source,dict) else {}
  for k,v in ih.items():
   if k in hash_targets:
    actual=fhash(base/hash_targets[k])
    if actual!=v: errs.append({'kind':'stale_hash','object':k,'expected':v,'actual':actual})
 return {'status':'PASS' if not errs else 'FAIL','verdict':'PAGE_DOSSIER_PASS' if not errs else 'EXECUTION_CHAIN_BLOCK','errors':errs,'measured':measured}

def validate_product_index(index_path):
 ip=Path(index_path); idx=load(ip); root=ip.parent; errs=[]; pages=[]
 if idx.get('schema_version')!='6.1': errs.append({'kind':'wrong_schema_version'})
 for x in idx.get('pages',[]):
  r=validate_page_dossier(root/x['path'],bool(x.get('critical',True)));
  # bind proof-index master hash to dossier master
  mp=root/x['path']/'final_page_master.png'
  if mp.exists() and x.get('master_sha256') and fhash(mp)!=x.get('master_sha256'):
   r['status']='FAIL';r['verdict']='EXECUTION_CHAIN_BLOCK';r['errors'].append({'kind':'proof_index_master_hash_mismatch'})
  pages.append({'page_id':x['page_id'],'result':r})
  if r['status']!='PASS': errs.append({'kind':'page_dossier_blocked','page_id':x['page_id']})
 return {'status':'PASS' if not errs else 'FAIL','verdict':'PRODUCT_PROOF_PASS' if not errs else 'EXECUTION_CHAIN_BLOCK','errors':errs,'pages':pages}
