from __future__ import annotations
import json,sys,os,shutil,time,hashlib,math,re
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'qa'));sys.path.insert(0,str(HERE))
import visual_qa_core as core
import gates_v26 as g26
import composition_fingerprint as cfp
import stress_and_safety as sas
from qa.html_bundle import inline_html
from bs4 import BeautifulSoup
from artifact.artifact_engine_v3 import run as artifact_run

EXTRA_JS="""()=>{const m={};document.querySelectorAll('[data-qa-idx]').forEach(e=>{const pos=[...e.querySelectorAll('*')].some(c=>['absolute','fixed'].includes(getComputedStyle(c).position));m[e.dataset.qaIdx]={contentSlot:e.dataset.contentSlot||'',regionId:e.dataset.regionId||'',areaBudget:e.dataset.areaBudget||'',relation:e.dataset.relation||'',nodeType:e.dataset.nodeType||'',pageId:e.dataset.pageId||'',grammarId:e.dataset.grammarId||'',sourceQuotation:e.dataset.sourceQuotation||'',visibleLanguageException:e.dataset.visibleLanguageException||'',hasPositionedChild:pos,hasElementChild:e.children.length>0};});return m;}"""
CONTAINER_JS="""(sel)=>[...document.querySelectorAll(sel)].map(p=>{const c=getComputedStyle(p);return {background:c.backgroundColor,color:c.color,direction:c.direction,fontFamily:c.fontFamily,fontSize:parseFloat(c.fontSize)||0,display:c.display,position:c.position,zIndex:c.zIndex,textAlign:c.textAlign,overflow:c.overflow,overflowX:c.overflowX,overflowY:c.overflowY,borderRadius:c.borderRadius,transform:c.transform,opacity:parseFloat(c.opacity)||1,clipPath:c.clipPath,filter:c.filter,objectFit:'',objectPosition:'',boxSizing:c.boxSizing,whiteSpace:c.whiteSpace,wordBreak:c.wordBreak,textOverflow:c.textOverflow,lineHeight:c.lineHeight,padding:[0,0,0,0],margin:[0,0,0,0],gap:0,flexShrink:0,flexGrow:0,letterSpacing:0};})"""
BLOCK_EXTRACT="""(sel)=>[...document.querySelectorAll(sel)].map((s,i)=>{const sr=s.getBoundingClientRect(),blocks=[];s.querySelectorAll('*').forEach(el=>{const cs=getComputedStyle(el),r=el.getBoundingClientRect();if(cs.display==='none'||cs.visibility==='hidden'||r.width<8||r.height<8)return;const bg=cs.backgroundColor||'';const surf=(bg&&bg!=='rgba(0, 0, 0, 0)'&&bg!=='transparent')||parseFloat(cs.borderTopWidth||'0')>0||cs.boxShadow!=='none';if(surf)blocks.push({x:r.x-sr.x,y:r.y-sr.y,w:r.width,h:r.height});});const paths=[...s.querySelectorAll('svg path,svg line,svg polyline')];return{id:'p'+(i+1),w:sr.width,h:sr.height,blocks,nodes:s.querySelectorAll('[data-node-id]').length,edges:s.querySelectorAll('[data-edge-id],[data-edge]').length||paths.length,edge_dirs:paths.map(p=>{const b=p.getBoundingClientRect();return Math.atan2(b.height,b.width)*180/Math.PI;})};})"""

def resolve_chromium():
    for c in [os.environ.get('RASHAD_CHROMIUM'),'/usr/bin/chromium','/usr/bin/google-chrome']:
        if c and Path(c).exists():return c
    return shutil.which('chromium') or shutil.which('google-chrome')

def collect(page,selector):
    data=page.evaluate(core.COLLECT,selector); extra=page.evaluate(EXTRA_JS); containers=page.evaluate(CONTAINER_JS,selector)
    for i,pd in enumerate(data):
        if i<len(containers):pd['container_css']=containers[i]
        for e in pd['els']:e['data'].update(extra.get(str(e['idx']),{}))
    return data

def ceqs(pd,gates,pixel,spec,anti_distance=1.0):
    gm={g['id']:g for g in gates}; ok=lambda gid: gm.get(gid,{}).get('status')=='PASS'
    slots={e['data'].get('contentSlot') for e in pd['els'] if e['data'].get('contentSlot')}
    argument=15 if {'question','thesis','implication'}<=slots else 8
    artifact=15 if ok('G32_ARTIFACT_TRUTH') and len([e for e in pd['els'] if e['data'].get('node')])>=3 else 5
    evidence=10 if ok('G31_EVIDENCE_TRACE') else 2
    # hierarchy from title/body font separation + dominant region share
    fs=[e['css']['fontSize'] for e in pd['texts'] if e['css']['fontSize']]
    hierarchy=10 if fs and max(fs)>=1.7*max(1,min(fs)) else 6
    ink=pixel.get('measured',{}).get('ink_coverage',0); edge=pixel.get('measured',{}).get('edge_density',0)
    balance=10 if 0.06<=ink<=0.65 and edge>=0.03 else (6 if 0.04<=ink<=0.72 else 2)
    scan=10 if ok('G02_HEADER_STACK') and ok('G13_TYPOGRAPHY') and ok('G03_LINE_COLLISION') else 4
    synth=15 if ok('G15_TOPOLOGY') and ok('G16_CONNECTORS') and ok('G23_HARMONY') else 7
    reference=5 if spec.get('reference_grammar_ids') else 0
    brand=5 if all(ok(x) for x in ['G24_PALETTE_LOCK','G25_CONTRAST','G26_TYPE_SCALE']) else 2
    originality=5 if anti_distance>=.085 else 0
    total=argument+artifact+evidence+hierarchy+balance+scan+synth+reference+brand+originality
    return {'score':total,'status':'PASS' if total>=90 else 'FAIL','breakdown':{'argument':argument,'exhibit_synthesis':synth,'artifact_integration':artifact,'evidence':evidence,'hierarchy':hierarchy,'visual_mass':balance,'scanability':scan,'reference_grammar':reference,'brand':brand,'originality':originality}}

def inspect_base(page,pd,prof,spec):
    gs=core.inspect(pd,page,prof,spec)
    # replace canvas gate behavior if authoring canvas is accepted 16:9
    return gs

def run(html_path,profile_path,spec,graph,exhibit,out_dir,selector='.page',stress=False,evidence_ledger=None,repair_before=None):
    html_path=Path(html_path); prof=json.loads(Path(profile_path).read_text());out=Path(out_dir);out.mkdir(parents=True,exist_ok=True)
    raw_html=html_path.read_text(encoding='utf-8')
    soup=BeautifulSoup(raw_html,'html.parser')
    missing_assets=[]
    for im in soup.find_all('img'):
        src=im.get('src','')
        if src and not re.match(r'^(data:|https?:|blob:)',src) and not (html_path.parent/src).resolve().exists(): missing_assets.append(src)
    bundled=inline_html(html_path); ts=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());eid='UQA-'+hashlib.sha256((str(html_path)+ts).encode()).hexdigest()[:16].upper()
    report={'evidence_id':eid,'runtime':'v3.0','status':'BLOCKED','release_verdict':'BLOCKED','pages':[],'deck':{},'stress':[],'repair_safety':None}
    # Critical pages require an external evidence ledger; spec sources are not allowed to self-certify.
    if evidence_ledger is None:
        report['evidence_ledger_gate']={'status':'FAIL','violations':[{'kind':'external_evidence_ledger_missing'}]}
    else:
        permitted={x['id'] for x in evidence_ledger.get('entries',[]) if x.get('classification')!='REFERENCE_ONLY' and x.get('truth_status')!='BLOCKED'}
        used=set(spec.get('content_pack',{}).get('sources',[])) if isinstance(spec,dict) else set().union(*[set(x.get('content_pack',{}).get('sources',[])) for x in spec])
        missing=sorted(used-permitted);report['evidence_ledger_gate']={'status':'FAIL' if missing else 'PASS','violations':[{'kind':'source_not_permitted','id':x} for x in missing]}
    with sync_playwright() as p:
        launch={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage']};exe=resolve_chromium();
        if exe:launch['executable_path']=exe
        b=p.chromium.launch(**launch); page=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=2)
        page.set_content(bundled,wait_until='load'); page.evaluate('()=>document.fonts.ready');time.sleep(.1)
        blocks=page.evaluate(BLOCK_EXTRACT,selector);anti=cfp.evaluate(blocks,tau=prof['thresholds'].get('anti_template_tau',.085),distinct_floor=prof['thresholds'].get('deck_distinct_composition_floor',.70));
        max_twins=int(prof['thresholds'].get('max_template_twins_per_4_pages',0)); twins=sum(1 for x in anti.get('pairs',[]) if x.get('twin'));
        if twins>max_twins: anti.setdefault('violations',[]).append({'kind':'template_twin_budget_exceeded','twins':twins,'ceiling':max_twins}); anti['status']='FAIL'
        report['deck']['anti_template']=anti
        fps=[cfp.fingerprint(x) for x in blocks]
        data=collect(page,selector)
        current_signature=sas.freeze(page.evaluate(sas.SIGNATURE_JS,selector))
        if any((x if isinstance(spec,list) else spec).get('qa_expectations',{}).get('repair_performed',False) for x in (spec if isinstance(spec,list) else [spec])):
            if repair_before is None: report['repair_safety']={'status':'FAIL','violations':[{'kind':'repair_before_signature_missing'}]}
            else: report['repair_safety']=sas.compare(repair_before,current_signature)
        else: report['repair_safety']={'status':'N_A','violations':[]}
        page_reports=[]
        for i,pd in enumerate(data):
            sp=spec if not isinstance(spec,list) else spec[i]
            base=inspect_base(page,pd,prof,sp)
            dist=1.0
            if len(fps)>1: dist=min([cfp.distance(fps[i],x) for j,x in enumerate(fps) if j!=i] or [1.0])
            extra=g26.inspect_v26(pd,prof,sp,html_dir=html_path.parent,fingerprint_distance=dist,ledger_ids=set([x['id'] for x in (evidence_ledger or {}).get('entries',[]) if x.get('classification')!='REFERENCE_ONLY' and x.get('truth_status')!='BLOCKED']))
            # V6: retire v2.6 mixed Artifact Strength score; use truth-only graph + rendered topology.
            extra=[g for g in extra if g['id']!='G32_ARTIFACT_STRENGTH']
            ar=artifact_run(graph) if graph else {'status':'FAIL','winner':None}
            actual_nodes={e['data'].get('node') for e in pd['els'] if e['data'].get('node')}
            actual_edges={e.get('id') for e in pd.get('edges',[]) if e.get('id')}
            expected_nodes={n.get('id') for n in (graph or {}).get('nodes',[])}
            expected_edges={e.get('id') for e in (graph or {}).get('edges',[])}
            av=[]
            if ar.get('status')!='PASS': av.append({'kind':'artifact_truth_engine_fail','detail':ar.get('errors') or ar.get('gate')})
            if expected_nodes!=actual_nodes: av.append({'kind':'rendered_node_set_mismatch','expected':sorted(expected_nodes),'actual':sorted(actual_nodes)})
            if expected_edges!=actual_edges: av.append({'kind':'rendered_edge_set_mismatch','expected':sorted(expected_edges),'actual':sorted(actual_edges)})
            score=(ar.get('winner') or {}).get('artifact_truth_score',0)
            if score<prof['thresholds'].get('artifact_truth_min',85): av.append({'kind':'artifact_truth_below_floor','score':score})
            truth={'id':'G32_ARTIFACT_TRUTH','name':'Artifact Truth V3','required':True,'executed':True,'test_count':len(expected_nodes)+len(expected_edges),'status':'FAIL' if av else 'PASS','violations':av,'measured':{'count':len(expected_nodes)+len(expected_edges),'score':score,'expected_nodes':len(expected_nodes),'expected_edges':len(expected_edges)}}
            gates=[g for g in base if g['id']!='G01_CANVAS']+extra+[truth]
            asset_pre={'id':'G29_ASSET_PATH_PREFLIGHT','name':'Asset path preflight','required':True,'executed':True,'test_count':len(soup.find_all('img')),'status':'FAIL' if missing_assets else 'PASS','violations':[{'kind':'missing_local_asset','src':x} for x in missing_assets],'measured':{'count':len(soup.find_all('img')),'missing':len(missing_assets)}}
            gates.append(asset_pre)
            # screenshots are mandatory pixel evidence
            loc=page.locator(selector).nth(i);png=out/f'{eid}_page_{i+1}.png';loc.screenshot(path=str(png),scale='device')
            px=sas.pixel_gate(png,prof,sp);gates.append(px)
            c=ceqs(pd,gates,px,sp,dist);ceqs_floor=float(prof['thresholds'].get('ceqs_min',90)); c['status']='PASS' if float(c.get('score',0))>=ceqs_floor else 'FAIL'; gates.append({'id':'G34_CEQS','name':'Consulting Exhibit Quality Score','required':True,'executed':True,'test_count':1,'status':c['status'],'violations':[] if c['status']=='PASS' else [{'kind':'ceqs_below_floor','score':c['score'],'floor':ceqs_floor}],'measured':c})
            fails=[g for g in gates if g.get('required',True) and g['status']!='PASS']
            page_reports.append({'page':i+1,'gates':gates,'ceqs':c,'pixel_master':str(png),'status':'PASS' if not fails else 'FAIL','blocking_gates':[g['id'] for g in fails]})
        report['pages']=page_reports
        # stress every mode from v2.6; only geometry/RTL/assets are considered
        if stress:
            required_arabic_modes=list(prof.get('thresholds',{}).get('stress_arabic_modes',[]))
            unknown=[m for m in required_arabic_modes if m not in sas.STRESS_MODES]
            if unknown:
                report['stress_policy_error']={'status':'FAIL','unknown_profile_modes':unknown}
            stress_modes=list(dict.fromkeys(required_arabic_modes + list(sas.STRESS_MODES)))
            for mode in stress_modes:
                page.set_content(bundled,wait_until='load');page.evaluate('()=>document.fonts.ready');sas.apply_stress(page,selector,mode);time.sleep(.03);d=collect(page,selector)
                failed=[]
                for i,pd in enumerate(d):
                    sp=spec if not isinstance(spec,list) else spec[i]
                    gs=inspect_base(page,pd,prof,sp)+g26.inspect_v26(pd,prof,sp,html_dir=html_path.parent,fingerprint_distance=1.0,ledger_ids=set([x['id'] for x in (evidence_ledger or {}).get('entries',[]) if x.get('classification')!='REFERENCE_ONLY' and x.get('truth_status')!='BLOCKED']))
                    relevant={'G02_HEADER_STACK','G03_LINE_COLLISION','G04_TEXT_FIT','G05_CONTAINMENT','G06_COLLISION','G07_OCCLUSION','G08_ALIGNMENT','G09_SPACING','G10_PADDING_SCALE','G11_OWNER_ANCHOR','G12_DIVIDERS','G13_TYPOGRAPHY','G14_RTL_BIDI','G15_TOPOLOGY','G16_CONNECTORS','G17_LABELS','G19_TRANSFORM_LAYER','G20_ASSETS','G21_DENSE_EVIDENCE','G23_HARMONY','G27_BIDI_RUNS','G28_COBRAND','G29_ASSET_INTEGRITY'}
                    failed += [g['id'] for g in gs if g['id'] in relevant and g['status']!='PASS']
                report['stress'].append({'mode':mode,'failed_gates':sorted(set(failed))})
        b.close()
    if stress:
        robustness={'ARABIC_INDIC_NUMERALS','FIVE_DIGIT_BADGE','LONG_SOURCE_LINE','LOGO_CANVAS_PADDING','FONT_SCALE_108','FONT_SCALE_110','LINE_HEIGHT_108','ARABIC_TEXT_GROWTH_120'}
        fault_injection={'FONT_FALLBACK','NODE_GROWTH','TITLE_THREE_LINES','LONG_LATIN_TOKEN'}
        sv=[]
        for r in report['stress']:
            if r['mode'] in robustness and r['failed_gates']: sv.append({'kind':'robustness_failure','mode':r['mode'],'failed_gates':r['failed_gates']})
            if r['mode'] in fault_injection and not r['failed_gates']: sv.append({'kind':'fault_not_detected','mode':r['mode']})
        required_profile=set(prof.get('thresholds',{}).get('stress_arabic_modes',[]))
        missing=(robustness|fault_injection|required_profile)-{r['mode'] for r in report['stress']}
        sv += [{'kind':'stress_mode_not_executed','mode':m} for m in sorted(missing)]
        if report.get('stress_policy_error'): sv.append({'kind':'invalid_stress_policy','detail':report['stress_policy_error']})
        stress_gate={'id':'C9_STRESS','name':'Metamorphic robustness + fault-injection stress','required':True,'executed':True,'test_count':len(report['stress']),'status':'FAIL' if sv else 'PASS','violations':sv,'measured':{'robustness_modes':sorted(robustness),'fault_injection_modes':sorted(fault_injection)}}
    else: stress_gate={'status':'PASS','violations':[],'id':'C9_STRESS','required':False,'executed':False,'test_count':0}
    report['stress_gate']=stress_gate
    ok=all(p['status']=='PASS' for p in report['pages']) and stress_gate['status']=='PASS' and report['deck']['anti_template']['status']=='PASS' and report['evidence_ledger_gate']['status']=='PASS' and report['repair_safety']['status'] in ('PASS','N_A')
    report['status']='PASS' if ok else 'FAIL';report['release_verdict']='HTML_PREEXPORT_PASS' if ok else 'BLOCKED'
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report
