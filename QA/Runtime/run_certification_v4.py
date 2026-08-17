#!/usr/bin/env python3
from pathlib import Path
import tempfile,json,hashlib,shutil,sys
from PIL import Image
sys.path.insert(0,str(Path(__file__).parent))
from qa_v4.taxonomy_runtime import taxonomy_audit,validate_case_results
from validation.execution_dossier_v4 import validate_page_dossier_v4

STATES=['INGESTED','CONTENT_LOCKED','GRAPH_LOCKED','ARTIFACT_TRUTH_PASS','EXHIBIT_SEARCH_COMPLETE','WINNER_LOCKED','VISUAL_SEARCH_COMPLETE','CEQS_PASS','PAGE_MASTER_LOCKED','PAGE_QA_PASS']
def dump(p,o):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(o,indent=2),encoding='utf-8')
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def make_valid(root):
 p=Path(root);(p/'visual_search').mkdir(parents=True);(p/'qa').mkdir(parents=True)
 dump(p/'content_pack.json',{'page_id':'P1','claims':['c1']})
 dump(p/'relationship_graph.json',{'page_id':'P1','nodes':[{'id':'N1'}],'edges':[]})
 # artifact truth is written after candidate hashes exist so it can be render-bound.
 hs=[]
 for i in range(5): hs.append({'id':f'H{i+1}','topology':f'T{i+1}','reading_path':f'R{i+1}','relation_carriers':[f'C{i+1}'],'mass_plan':f'M{i+1}','focal_point':f'F{i+1}'})
 dump(p/'exhibit_hypotheses.json',{'page_id':'P1','hypotheses':hs})
 dump(p/'exhibit_selection.json',{'page_id':'P1','winner':'H1','rejected':['H2','H3','H4','H5']})
 dump(p/'evidence_pack.json',{'page_id':'P1','claims':[{'id':'c1','source_id':'SRC1','locator':'p1'}]})
 cands=[]
 for i in range(3):
  q=p/'visual_search'/f'c{i+1}.png';q.write_bytes((f'candidate-{i}').encode());cands.append({'id':f'C{i+1}','path':q.name})
 dump(p/'visual_search/manifest.json',{'page_id':'P1','candidates':cands,'structural_divergence':{'min_pairwise':0.2,'average_pairwise':0.24}})
 candidate_hash=h(p/'visual_search/c1.png')
 dump(p/'artifact_truth.json',{'page_id':'P1','status':'PASS','artifact_truth_score':94,'owner':'INDEPENDENT_ARTIFACT_JUDGE','independent':True,'judge_invocation_id':'TEST-ARTIFACT-001','render_evidence':['DOM:N1'],'actual_render_hash':candidate_hash})
 Image.new('RGB',(3840,2160),'white').save(p/'final_page_master.png')
 master_hash=h(p/'final_page_master.png')
 dump(p/'ceqs.json',{'page_id':'P1','status':'PASS','ceqs':93,'owner':'INDEPENDENT_VISUAL_CRITIC','independent':True,'judge_invocation_id':'TEST-VISUAL-001','visual_evidence':['master'],'actual_render_hash':master_hash})
 dump(p/'qa/html_report.json',{'release_verdict':'HTML_PREEXPORT_PASS','pages':[{'gates':[{'id':'C9_PIXEL','status':'PASS','test_count':1,'measured':{'count':1}}]}]})
 dump(p/'state_transitions.json',[{'state':s} for s in STATES])

def attack(base,name,mutator,expect_kind):
 d=Path(base)/name;shutil.copytree(Path(base)/'valid',d);mutator(d);r=validate_page_dossier_v4(d,True);kinds={e['kind'] for e in r['errors']};return {'name':name,'status':'PASS' if r['status']=='FAIL' and expect_kind in kinds else 'FAIL','expected_block':expect_kind,'observed':sorted(kinds)}

def main():
 results=[];tax=taxonomy_audit();results.append({'name':'taxonomy_contract','status':tax['status'],'detail':tax.get('counts')})
 with tempfile.TemporaryDirectory() as td:
  td=Path(td);v=td/'valid';make_valid(v);vr=validate_page_dossier_v4(v,True);results.append({'name':'valid_synthetic_dossier','status':vr['status'],'detail':vr.get('errors')})
  def modjson(path,fn):
   o=json.loads(path.read_text());fn(o);dump(path,o)
  attacks=[
   ('producer_artifact_truth',lambda d:modjson(d/'artifact_truth.json',lambda o:o.update(owner='PRODUCER',artifact_truth_score=100)),'artifact_truth_not_independent'),
   ('artifact_truth_89',lambda d:modjson(d/'artifact_truth.json',lambda o:o.update(artifact_truth_score=89)),'artifact_truth_below_floor'),
   ('producer_ceqs',lambda d:modjson(d/'ceqs.json',lambda o:o.update(owner='PRODUCER',ceqs=100)),'ceqs_not_independent'),
   ('ceqs_89',lambda d:modjson(d/'ceqs.json',lambda o:o.update(ceqs=89)),'ceqs_below_floor'),
   ('four_hypotheses',lambda d:modjson(d/'exhibit_hypotheses.json',lambda o:o.update(hypotheses=o['hypotheses'][:4])),'wrong_hypothesis_count'),
   ('duplicate_hypotheses',lambda d:modjson(d/'exhibit_hypotheses.json',lambda o:o.update(hypotheses=[o['hypotheses'][0]]*5)),'hypotheses_not_materially_distinct'),
   ('two_candidates',lambda d:modjson(d/'visual_search/manifest.json',lambda o:o.update(candidates=o['candidates'][:2])),'insufficient_render_search'),
   ('weak_divergence',lambda d:modjson(d/'visual_search/manifest.json',lambda o:o.update(structural_divergence={'min_pairwise':0.01,'average_pairwise':0.02})),'structural_divergence_below_critical_floor'),
   ('master_1080p',lambda d:Image.new('RGB',(1920,1080),'white').save(d/'final_page_master.png'),'master_resolution_below_floor'),
   ('pixel_vacuous',lambda d:modjson(d/'qa/html_report.json',lambda o:o['pages'][0]['gates'][0].update(test_count=0,measured={'count':0})),'pixel_qa_vacuous_pass'),
   ('state_skip',lambda d:modjson(d/'state_transitions.json',lambda o:o.pop(2)),'missing_state'),
  ]
  for a in attacks: results.append(attack(td,*a))
 ok=all(x['status']=='PASS' for x in results);report={'runtime':'4.0-rc1','status':'PASS' if ok else 'FAIL','tests':results,'passed':sum(x['status']=='PASS' for x in results),'total':len(results)}
 out=Path(__file__).parent/'certification/V4_RC1_SELF_CERTIFICATION.json';dump(out,report);print(json.dumps(report,indent=2));return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
