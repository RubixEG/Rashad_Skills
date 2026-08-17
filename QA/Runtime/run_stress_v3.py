#!/usr/bin/env python3
import random,json,sys,copy,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from artifact.artifact_engine_v3 import run
REL=['ENABLES','DEPENDS_ON','FLOWS_TO','CONTROLS','MEASURES','EVIDENCES','RISKS','PRIORITIZES','OWNS','APPROVES','FEEDS_BACK','THRESHOLD_FOR','MAPS_TO','BLOCKS']
T=['ACTOR','CAPABILITY','PROCESS','ASSET','OUTCOME','CONSTRAINT','MEASURE','DECISION','RISK','EVIDENCE']
random.seed(42);runs=500;crashes=0;pass_count=0;budget_viol=0;start=time.time()
for k in range(runs):
 n=random.randint(3,24);m=random.randint(max(1,n-2),min(55,n*3));nodes=[{'id':f'N{i}','type':random.choice(T),'label':f'Node {i}','evidence':['EV-0001']} for i in range(n)];edges=[]
 for i in range(m):
  a,b=random.sample(range(n),2);edges.append({'id':f'E{i+1}','source':f'N{a}','target':f'N{b}','relation':random.choice(REL),'evidence':['EV-0001']})
 g={'schema_version':'6.0','engagement_id':'STRESS','page_id':'P01','nodes':nodes,'edges':edges,'provenance':{'derived_from':['synthetic'],'derived_at':'2026-08-13'}}
 try:
  r=run(g)
  if r['status']=='PASS':
   pass_count+=1
   if len(r['winner']['primitives'])>r['winner']['max_primitives']:budget_viol+=1
 except Exception:crashes+=1
out={'runs':runs,'crashes':crashes,'passes':pass_count,'pass_winner_budget_violations':budget_viol,'graphs_per_sec':round(runs/max(.001,time.time()-start),1),'status':'PASS' if crashes==0 and budget_viol==0 else 'FAIL'}
Path(__file__).with_name('STRESS_V3_RESULTS.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));raise SystemExit(0 if out['status']=='PASS' else 1)
