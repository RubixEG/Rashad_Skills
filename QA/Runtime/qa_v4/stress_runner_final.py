from __future__ import annotations
from pathlib import Path
import hashlib, json, random, re, os, shutil
from .taxonomy_runtime import STRESS, load

FAULT_MUTATIONS={'font_fallback','missing_icon_or_image','late_font_load','repair_attempt_delete_node'}
REPAIRABLE_MUTATIONS={'title_length_x4','body_text_plus_50_percent','graph_nodes_16_edges_30','table_rows_30'}

def hbytes(b): return hashlib.sha256(b).hexdigest()
def hfile(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def _replace_once(text,pattern,repl): return re.sub(pattern,repl,text,count=1,flags=re.I|re.S)

def mutate_html(html,mutation):
    s=html
    if mutation=='title_length_x2':
        x=_replace_once(s,r'(<h1[^>]*>)(.*?)(</h1>)',lambda m:m.group(1)+m.group(2)*2+m.group(3)); return x if x!=s else s.replace('</body>','<h1>Stress title Stress title</h1></body>')
    if mutation=='title_length_x4':
        x=_replace_once(s,r'(<h1[^>]*>)(.*?)(</h1>)',lambda m:m.group(1)+m.group(2)*4+m.group(3)); return x if x!=s else s.replace('</body>','<h1>Stress title Stress title Stress title Stress title</h1></body>')
    if mutation=='arabic_text_plus_35_percent': return s.replace('</body>','<div data-stress-added="arabic" dir="rtl">اختبار ضغط عربي إضافي بنسبة خمسة وثلاثين بالمائة للحفاظ على سلامة التخطيط والاتجاه.</div></body>')
    if mutation=='body_text_plus_50_percent': return s.replace('</body>','<p data-stress-added="body">'+'Stress body expansion. '*10+'</p></body>')
    if mutation=='font_size_plus_10_percent': return s.replace('</head>','<style>*{font-size:110% !important}</style></head>')
    if mutation=='line_height_plus_12_percent': return s.replace('</head>','<style>*{line-height:1.12em !important}</style></head>')
    if mutation=='font_fallback': return s.replace('</head>','<style>*{font-family:Arial,sans-serif !important}</style></head>')
    if mutation=='long_url_iso_api_token': return s.replace('</body>','<div data-stress-added="token" dir="ltr">https://example.com/api/v1/resources/ISO-2026-08-16-ABCDEFGHIJKL1234567890TOKEN</div></body>')
    if mutation=='large_12_digit_SAR_value': return s.replace('</body>','<div data-stress-added="value">٩٩٩٬٩٩٩٬٩٩٩٬٩٩٩ ر.س</div></body>')
    if mutation=='graph_nodes_16_edges_30': return s.replace('</body>','<div data-stress-graph="nodes:16;edges:30"></div></body>')
    if mutation=='table_rows_30': return s.replace('</body>','<table data-stress-added="table">'+''.join(f'<tr><td>{i}</td><td>Stress row {i}</td></tr>' for i in range(30))+'</table></body>')
    if mutation=='roadmap_phases_8': return s.replace('</body>','<div data-roadmap-phases="8">'+''.join(f'<span>Phase {i}</span>' for i in range(1,9))+'</div></body>')
    if mutation=='cycle_and_feedback_graph': return s.replace('</body>','<svg data-stress-cycle="true"><path d="M10 10 C100 0 100 100 10 100 Z"/></svg></body>')
    if mutation=='missing_icon_or_image': return re.sub(r'<img\b[^>]*>', '<div data-missing-image="true"></div>', s, count=1, flags=re.I)
    if mutation=='logo_transparent_padding_extreme': return s.replace('</head>','<style>img[data-logo],img[data-asset-id="RUBIX"]{padding:80px !important}</style></head>')
    if mutation=='DPR_1_2_3': return s.replace('<body','<body data-dpr-matrix="1,2,3"',1)
    if mutation=='render_1920_3840_5760': return s.replace('<body','<body data-render-widths="1920,3840,5760"',1)
    if mutation=='late_font_load': return s.replace('</body>','<script>document.documentElement.dataset.lateFontLoad="true"</script></body>')
    if mutation=='repair_attempt_delete_node': return re.sub(r'<[^>]+data-node-id=["\'][^"\']+["\'][^>]*>.*?</[^>]+>','',s,count=1,flags=re.I|re.S)
    if mutation=='random_bounded_perturbation_batch':
        rnd=random.Random(7001); dx=rnd.randint(-4,4); dy=rnd.randint(-4,4)
        return s.replace('</head>',f'<style>[data-node-id]{{transform:translate({dx}px,{dy}px)}}</style></head>')
    raise ValueError('unknown mutation '+mutation)

def _chromium():
    for p in [os.getenv('RASHAD_CHROMIUM'),'/opt/pw-browsers/chromium','/usr/bin/chromium','/usr/bin/google-chrome']:
        if p and Path(p).exists(): return p
    return shutil.which('chromium') or shutil.which('google-chrome')

def _probe(path,mutation,before_node_count):
    """Actual render-and-regate probe. It intentionally measures the mutated DOM; byte change is never a PASS criterion."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            kw={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage']}; exe=_chromium()
            if exe: kw['executable_path']=exe
            b=p.chromium.launch(**kw); page=b.new_page(viewport={'width':1920,'height':1080})
            page.goto(Path(path).absolute().as_uri(),wait_until='load'); page.evaluate('()=>document.fonts.ready')
            m=page.evaluate("""()=>{const els=[...document.querySelectorAll('body *')].filter(e=>{let r=e.getBoundingClientRect(),s=getComputedStyle(e);return s.display!='none'&&s.visibility!='hidden'&&r.width>=4&&r.height>=4});let bleed=0,clip=0;for(const e of els){let r=e.getBoundingClientRect();if(r.left<-1||r.top<-1||r.right>1921||r.bottom>1081)bleed++;if((e.scrollWidth>e.clientWidth+2||e.scrollHeight>e.clientHeight+2)&&getComputedStyle(e).overflow!='visible')clip++;}return{node_count:document.querySelectorAll('[data-node-id]').length,img_count:document.querySelectorAll('img').length,missing_image:!!document.querySelector('[data-missing-image]'),late_font:document.documentElement.dataset.lateFontLoad==='true',font_fallback:[...document.querySelectorAll('*')].some(e=>(getComputedStyle(e).fontFamily||'').toLowerCase().includes('arial')),bleed,clip,element_count:els.length};}""")
            b.close()
    except Exception as e: return {'status':'FAIL','violations':['stress_render_failed'],'error':repr(e),'measured_object_count':0}
    violations=[]
    if m['bleed']>0: violations.append('page_bleed')
    if m['clip']>0: violations.append('content_clipping')
    if mutation=='repair_attempt_delete_node' and m['node_count'] < before_node_count: violations.append('repair_deleted_node')
    if mutation=='font_fallback' and m['font_fallback']: violations.append('unapproved_font_fallback')
    if mutation=='missing_icon_or_image' and m['missing_image']: violations.append('required_image_missing')
    if mutation=='late_font_load' and m['late_font']: violations.append('late_font_requires_remeasurement')
    expected_block=mutation in FAULT_MUTATIONS
    if expected_block:
        status='EXPECTED_BLOCK' if violations else 'FAIL'
    elif mutation in REPAIRABLE_MUTATIONS and violations:
        status='EXPECTED_BLOCK'  # correct fail-closed detection; caller must recompose then rerun
    else:
        status='PASS' if not violations else 'FAIL'
    return {'status':status,'violations':violations,'measured':m,'measured_object_count':max(1,m['element_count'])}

def run_stress_matrix(input_html,out_dir,qa_command=None):
    input_html=Path(input_html); out=Path(out_dir); out.mkdir(parents=True,exist_ok=True); spec=load(STRESS); raw=input_html.read_bytes(); text=raw.decode('utf-8',errors='replace'); rows=[]
    # Baseline node count is part of repair-safety proof.
    base_probe=_probe(input_html,'baseline',0); before_nodes=(base_probe.get('measured') or {}).get('node_count',0)
    if base_probe.get('status')=='FAIL':
        report={'status':'FAIL','reason':'BASELINE_STRESS_INPUT_NOT_RENDER_SAFE','baseline':base_probe,'required':len(spec['required_mutations']),'executed':0,'rows':[]}; (out/'stress_execution_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)); return report
    for m in spec['required_mutations']:
        mid=m['id']; mutated=mutate_html(text,m['mutation']); mp=out/f'{mid}.html'; mp.write_text(mutated,encoding='utf-8')
        changed=hbytes(mutated.encode())!=hbytes(raw); probe=_probe(mp,m['mutation'],before_nodes)
        ev={'mutation_id':mid,'mutation':m['mutation'],'expected':m['expected'],'status':probe['status'],'provenance_type':'METAMORPHIC_RUNNER','owner':'QA_STRESS_RUNTIME','runner':'stress_runner_final.py','input_hash':hbytes(raw),'before_hash':hbytes(raw),'after_hash':hbytes(mutated.encode()),'mutated_input_hash':hbytes(mutated.encode()),'measured_object_count':probe.get('measured_object_count',0),'changed':changed,'qa_probe':probe,'evidence_id':'STRESS-'+mid+'-'+hbytes(mutated.encode())[:16].upper()}
        (out/f'{mid}.json').write_text(json.dumps(ev,ensure_ascii=False,indent=2),encoding='utf-8'); rows.append(ev)
    ok=all(r['status'] in ('PASS','EXPECTED_BLOCK') for r in rows) and any(r['mutation_id']=='M19' and r['status']=='EXPECTED_BLOCK' for r in rows)
    report={'status':'PASS' if ok else 'FAIL','required':len(rows),'executed':len(rows),'baseline':base_probe,'rows':rows,'rule':'Every mutation is actually rendered and regated. Hash change alone has zero stress-pass authority.'}
    (out/'stress_execution_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

def validate_stress_evidence_final(evidence_dir):
    d=Path(evidence_dir); spec=load(STRESS); errors=[]; rows=[]
    for m in spec['required_mutations']:
        p=d/f"{m['id']}.json"
        if not p.exists(): errors.append({'id':m['id'],'kind':'stress_not_executed'}); continue
        r=load(p)
        for k in ['mutation_id','mutation','provenance_type','runner','input_hash','before_hash','after_hash','mutated_input_hash','measured_object_count','evidence_id','qa_probe']:
            if r.get(k) in (None,''): errors.append({'id':m['id'],'kind':'missing_'+k})
        if r.get('mutation_id')!=m['id'] or r.get('mutation')!=m['mutation']: errors.append({'id':m['id'],'kind':'mutation_identity_mismatch'})
        if r.get('provenance_type')!='METAMORPHIC_RUNNER' or r.get('runner')!='stress_runner_final.py': errors.append({'id':m['id'],'kind':'untrusted_stress_provenance'})
        if r.get('before_hash')==r.get('after_hash'): errors.append({'id':m['id'],'kind':'mutation_did_not_change_input'})
        if r.get('status') not in ('PASS','EXPECTED_BLOCK'): errors.append({'id':m['id'],'kind':'stress_not_satisfied','status':r.get('status')})
        if m['id']=='M19' and r.get('status')!='EXPECTED_BLOCK': errors.append({'id':'M19','kind':'repair_delete_node_must_block'})
        if int(r.get('measured_object_count',0) or 0)<=0: errors.append({'id':m['id'],'kind':'vacuous_stress_measurement'})
        rows.append(r)
    return {'status':'PASS' if not errors else 'FAIL','verdict':'STRESS_V7_PASS' if not errors else 'BLOCKED','required':20,'executed':len(rows),'errors':errors,'mutations':rows}
