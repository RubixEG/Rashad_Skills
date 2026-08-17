#!/usr/bin/env python3
import os
from pathlib import Path
import shutil
import sys,json,copy
sys.path.insert(0,str(Path(__file__).parent))
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Rashad'/'Brain'/'runtime'))
from validation.schema_validator import validate_graph,validate_schema
from validation.r_code_reachability import analyse
from artifact.artifact_engine_v3 import run as artifact_run
from artifact.exhibit_engine import build as exhibit_build
from qa.unified_html_qa import run as html_run
from brain.composition_spec import build_page_composition_spec
from brain.production.renderer import render_composition_page
HERE=Path(__file__).parent;F=HERE/'fixtures'
# Regression output is ephemeral; clean it so repeated certification does not accumulate stale PNGs.
shutil.rmtree(HERE/'_regression', ignore_errors=True)
def load(p):return json.loads(Path(p).read_text())
res=[]
def add(name,ok,detail=''):res.append({'test':name,'pass':bool(ok),'detail':str(detail)[:800]})
g=load(F/'graph.json');add('schema_clean',not validate_graph(g))
for name,mut in [
 ('duplicate_node',lambda x:x['nodes'].append(copy.deepcopy(x['nodes'][0]))),
 ('duplicate_edge',lambda x:x['edges'].append(copy.deepcopy(x['edges'][0]))),
 ('dangling_edge',lambda x:x['edges'].__setitem__(0,{**x['edges'][0],'target':'MISSING'})),
 ('missing_evidence',lambda x:x['edges'][0].__setitem__('evidence',[])),
 ('invalid_relation',lambda x:x['edges'][0].__setitem__('relation','DECORATES'))]:
 x=copy.deepcopy(g);mut(x);add('graph_'+name,bool(validate_graph(x)),validate_graph(x)[:2])
a=artifact_run(g);add('artifact_truth_clean',a['status']=='PASS' and a['winner']['artifact_truth_score']>=85 and len(a['winner']['primitives'])<=a['winner']['max_primitives'],a.get('winner'))
weak=copy.deepcopy(g);weak['edges']=[];aw=artifact_run(weak);add('artifact_weak_fails',aw['status']=='FAIL',aw.get('winner'))
ex=exhibit_build(g,load(F/'content_pack.json'),['CRG-04','CRG-05']);add('five_exhibit_hypotheses',ex['status']=='PASS' and len(ex['hypotheses'])==5)
(F/'exhibit.json').write_text(json.dumps(ex,ensure_ascii=False,indent=2))
# exhibit schema must reject <5 hypotheses
ex_obj={'schema_version':'6.0','engagement_id':'TEST','page_id':'P01','visual_thesis':'A sufficiently long visual thesis for the test','artifact_truth_score':90,'hypotheses':[{'id':f'H{i}','name':'x','dominant_form':'SPINE','reading_path':'RTL','relation_carriers':['x'],'mass_plan':{}} for i in range(1,6)],'winner':'H1','evidence_packing':[{'evidence_id':'EV-0001','target':'N1','reason':'proof'}],'ceqs_floor':90}
add('exhibit_schema_five',not validate_schema(ex_obj,'exhibit-spec.schema.json'))
ex_bad=copy.deepcopy(ex_obj);ex_bad['hypotheses']=ex_bad['hypotheses'][:2];add('exhibit_schema_rejects_two',bool(validate_schema(ex_bad,'exhibit-spec.schema.json')))
# HTML positive control is generated through the current v7.3 production organ.
sp=load(F/'page_spec.json'); sp['artifact_family']='SYSTEM'; sp['artifact_expected']=True
cp={'page_id':'P01','language':'AR','title':'منهجية التنفيذ','thesis':'نحوّل دورة التنفيذ إلى نظام مترابط تحكمه بوابات قرار وتغذية راجعة','proof_points':['كل مرحلة تنتج قرارًا أو دليلًا قابلًا للمراجعة','الحوكمة وضمان الجودة تعبران جميع المراحل','المقيّم يرى نظام تشغيل مغلقًا'],'executive_implication':'المقيّم يرى نظام تشغيل مغلقًا يمكن استمراره بعد انتهاء العقد','source_note':'EV-0001'}
hyp={'id':'H-CLEAN','communication_strategy':'SYSTEM_LED','strategy_family':'SYSTEM','page_fingerprint':'REGRESSION-V73-CLEAN'}
cs=build_page_composition_spec(hyp,cp,g,variant_index=2)
prod=render_composition_page(cs,cp,g,HERE/'_regression/current_composer_clean',allow_test_font_fallback=True,emit_pdf=False,brand_logo=Path(__file__).resolve().parents[2]/'Rashad/Skill/08_BRAND_CURRENT/assets/rubix-consulting-current-light.png',client_logo=F/'client_test.png')
try:
 out=HERE/'_regression/current_composer_clean_qa';out.mkdir(parents=True,exist_ok=True)
 r=html_run(Path(prod['html_master_path']),HERE/'config/profile_test.json',sp,g,ex,out,'.page',False,load(F/'evidence_ledger.json'));ok=(prod.get('status')=='PASS' and r['release_verdict']=='HTML_PREEXPORT_PASS')
except Exception as e:ok=False;r={'error':str(e)}
add('html_current_composer_clean',ok,(r.get('pages') or [{}])[0].get('blocking_gates',r.get('error','')))
# The former legacy positive control is intentionally no longer accepted: the stronger
# floors catch its unsafe footer, weak dominant mass and connector/text geometry.
try:
 out=HERE/'_regression/legacy_clean_negative';out.mkdir(parents=True,exist_ok=True)
 lr=html_run(F/'clean_legacy.html',HERE/'config/profile_test.json',sp,g,ex,out,'.page',False,load(F/'evidence_ledger.json')); lbs=(lr.get('pages') or [{}])[0].get('blocking_gates',[])
 legacy_ok=lr['release_verdict']=='BLOCKED' and bool(set(lbs)&{'G05_CONTAINMENT','G39_DOMINANT_MASS','G40_COLUMN_BALANCE','G41_CONNECTOR_PATH_GEOMETRY'})
except Exception as e: legacy_ok=False; lbs=[str(e)]
add('legacy_clean_fixture_rejected_by_v73_floors',legacy_ok,lbs)
# Broken historical controls remain negative fixtures.
cases=[('broken_overflow.html',False),('broken_asset.html',False),('broken_overlap.html',False),('broken_bidi.html',False),('broken_card_only.html',False)]
for file,expect in cases:
 out=HERE/'_regression'/file.replace('.html','');out.mkdir(parents=True,exist_ok=True)
 try:r=html_run(F/file,HERE/'config/profile_test.json',sp,g,ex,out,'.page',False,load(F/'evidence_ledger.json'));ok=(r['release_verdict']=='HTML_PREEXPORT_PASS')
 except Exception as e:ok=False;r={'error':str(e)}
 add('html_'+file,ok==expect,(r.get('pages') or [{}])[0].get('blocking_gates',r.get('error','')))
# deck template twins: two identical pages must be blocked
sp2=copy.deepcopy(sp);sp2['page_id']='P02';sp2['pending_product_state']['resume_token']='test-p02'
try:
 out=HERE/'_regression/template_twins';out.mkdir(parents=True,exist_ok=True);r=html_run(F/'broken_template_twins.html',HERE/'config/profile_test.json',[sp,sp2],g,ex,out,'.page',False,load(F/'evidence_ledger.json'));add('deck_template_twins_blocked',r['release_verdict']=='BLOCKED',r['deck'])
except Exception as e:add('deck_template_twins_blocked',False,e)
# R-code effective reachability using consolidated v6 skill (path sibling in /mnt/data)
skill=Path(os.environ.get('RASHAD_SKILL_ROOT', str(Path(__file__).resolve().parents[2] / 'Rashad' / 'Skill')));rr=analyse(skill);add('r_code_effective_reachability',rr['all']==388 and rr['effective_reachable']==388 and rr['direct_only']==139,rr)
summary={'passed':sum(x['pass'] for x in res),'total':len(res),'status':'PASS' if all(x['pass'] for x in res) else 'FAIL','tests':res}
(HERE/'REGRESSION_V3_RESULTS.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False,indent=2));raise SystemExit(0 if summary['status']=='PASS' else 1)
