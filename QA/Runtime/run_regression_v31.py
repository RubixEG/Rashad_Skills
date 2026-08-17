import os
from pathlib import Path
import sys,json,shutil,copy
sys.path.insert(0,str(Path(__file__).parent))
from validation.execution_dossier import validate_product_index
from validation.current_route_audit import audit as route_audit
HERE=Path(__file__).parent;VALID=HERE/'fixtures/proof_valid/proof_index.json'
# Regression output is ephemeral; clear the entire root so repeated certification is deterministic.
shutil.rmtree(HERE/'_regression_v31', ignore_errors=True)
res=[]
def add(n,ok,d=''):res.append({'test':n,'pass':bool(ok),'detail':str(d)[:1000]})
r=validate_product_index(VALID);add('complete_dossier_passes',r['status']=='PASS',r)
# mutators on copied proof tree
cases=[]
def cp_case(name):
 dst=HERE/'_regression_v31'/name
 if dst.exists(): shutil.rmtree(dst)
 shutil.copytree(HERE/'fixtures/proof_valid',dst);return dst
# missing key files
for name,rel in [('missing_content','pages/P01/content_pack.json'),('missing_graph','pages/P01/relationship_graph.json'),('missing_artifact_truth','pages/P01/artifact_truth.json'),('missing_ceqs','pages/P01/ceqs.json'),('missing_master','pages/P01/final_page_master.png'),('missing_html_qa','pages/P01/qa/html_report.json')]:
 d=cp_case(name);(d/rel).unlink();rr=validate_product_index(d/'proof_index.json');add(name,rr['status']=='FAIL',rr['errors'])
# fewer hypotheses
for name,fn in [('two_hypotheses','exhibit_hypotheses.json')]:
 d=cp_case(name);p=d/'pages/P01'/fn;o=json.loads(p.read_text());o['hypotheses']=o['hypotheses'][:2];p.write_text(json.dumps(o));rr=validate_product_index(d/'proof_index.json');add(name,rr['status']=='FAIL',rr['pages'][0]['result']['errors'])
# single render candidate
for name,count in [('one_render_candidate',1),('two_render_candidates',2)]:
 d=cp_case(name);p=d/'pages/P01/visual_search/manifest.json';o=json.loads(p.read_text());o['candidates']=o['candidates'][:count];p.write_text(json.dumps(o));rr=validate_product_index(d/'proof_index.json');add(name,rr['status']=='FAIL',rr['pages'][0]['result']['errors'])
# low scores
for name,fn,key,val in [('artifact_truth_84','artifact_truth.json','artifact_truth_score',84),('ceqs_89','ceqs.json','ceqs',89)]:
 d=cp_case(name);p=d/'pages/P01'/fn;o=json.loads(p.read_text());o[key]=val;p.write_text(json.dumps(o));rr=validate_product_index(d/'proof_index.json');add(name,rr['status']=='FAIL',rr['pages'][0]['result']['errors'])
# missing pixel pass
d=cp_case('pixel_not_proven');p=d/'pages/P01/qa/html_report.json';o=json.loads(p.read_text());o['pages'][0]['gates'].pop('C9_PIXEL');p.write_text(json.dumps(o));rr=validate_product_index(d/'proof_index.json');add('pixel_not_proven',rr['status']=='FAIL',rr['pages'][0]['result']['errors'])
# state skip
d=cp_case('state_skip');p=d/'pages/P01/state_transitions.json';o=json.loads(p.read_text());o=[x for x in o if x['state']!='VISUAL_SEARCH_COMPLETE'];p.write_text(json.dumps(o));rr=validate_product_index(d/'proof_index.json');add('state_skip',rr['status']=='FAIL',rr['pages'][0]['result']['errors'])
# low-res master
from PIL import Image
d=cp_case('lowres_master');Image.new('RGB',(1920,1080),'white').save(d/'pages/P01/final_page_master.png');rr=validate_product_index(d/'proof_index.json');add('lowres_master',rr['status']=='FAIL',rr['pages'][0]['result']['errors'])

# stale content hash
d=cp_case('stale_content_hash');p=d/'pages/P01/content_pack.json';o=json.loads(p.read_text());o['thesis']=str(o.get('thesis',''))+' changed';p.write_text(json.dumps(o));rr=validate_product_index(d/'proof_index.json');add('stale_content_hash',rr['status']=='FAIL',rr['pages'][0]['result']['errors'])
# page id mismatch
d=cp_case('page_id_mismatch');p=d/'pages/P01/ceqs.json';o=json.loads(p.read_text());o['page_id']='P99';p.write_text(json.dumps(o));rr=validate_product_index(d/'proof_index.json');add('page_id_mismatch',rr['status']=='FAIL',rr['pages'][0]['result']['errors'])


# hypotheses same signature should block
d=cp_case('duplicate_hypothesis_signatures');p=d/'pages/P01/exhibit_hypotheses.json';o=json.loads(p.read_text());base=o['hypotheses'][0];o['hypotheses']=[dict(base,id=f'H{i}') for i in range(1,6)];p.write_text(json.dumps(o));rr=validate_product_index(d/'proof_index.json');add('duplicate_hypothesis_signatures',rr['status']=='FAIL',rr['pages'][0]['result']['errors'])
# candidate images identical should block
d=cp_case('duplicate_render_candidates');src=d/'pages/P01/visual_search/candidate_01.png';import shutil as _sh
_sh.copy2(src,d/'pages/P01/visual_search/candidate_02.png');_sh.copy2(src,d/'pages/P01/visual_search/candidate_03.png');rr=validate_product_index(d/'proof_index.json');add('duplicate_render_candidates',rr['status']=='FAIL',rr['pages'][0]['result']['errors'])
# proof index master hash mismatch
d=cp_case('master_hash_mismatch');p=d/'proof_index.json';o=json.loads(p.read_text());o['pages'][0]['master_sha256']='0'*64;p.write_text(json.dumps(o));rr=validate_product_index(d/'proof_index.json');add('master_hash_mismatch',rr['status']=='FAIL',rr['pages'][0]['result']['errors'])

# route audit
skill=Path(os.environ.get('RASHAD_SKILL_ROOT', str(Path(__file__).resolve().parents[2] / 'Rashad' / 'Skill')));ra=route_audit(skill);add('single_current_startup_route',ra['status']=='PASS',ra)
summary={'passed':sum(x['pass'] for x in res),'total':len(res),'status':'PASS' if all(x['pass'] for x in res) else 'FAIL','tests':res};(HERE/'REGRESSION_V31_RESULTS.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));raise SystemExit(0 if summary['status']=='PASS' else 1)
