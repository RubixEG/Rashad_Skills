#!/usr/bin/env python3
from pathlib import Path
import json,sys,tempfile,hashlib
ROOT=Path(__file__).resolve().parents[2]
BR=ROOT/'Rashad/Brain/runtime'; QR=ROOT/'QA/Runtime'
sys.path.insert(0,str(QR)); sys.path.insert(0,str(BR))
from brain.visual_search import generate_hypotheses
from brain.composition_spec import build_page_composition_spec,validate_page_composition_spec
from brain.spec_divergence import evaluate_set
from brain.production.composer import compose_html
from brain.production.renderer import render_composition_page
from brain.production.projector import build_image_master_pptx
from brain.production.font_preflight import check_brand_fonts
from brain.production.image_provider import HostNativeImagePendingProvider
from brain.imagery_director import build_image_request
from brain.product_inspector import inspect_product
from brain.semantic_master_gate import inspect_semantic_html_master
from brain.pdf_text_integrity import inspect_pdf_text_layer
from qa.unified_html_qa import run as unified_html_run

def row(name,ok,detail=None): return {'name':name,'status':'PASS' if ok else 'FAIL','detail':detail}
rows=[]
graph=json.loads((QR/'fixtures/graph.json').read_text(encoding='utf-8'))
cover={'page_id':'P01','language':'AR','page_family':'COVER','title':'منصة ذكاء اصطناعي متكاملة','thesis':'قدرة مؤسسية محكومة','management_question':'الغلاف','image_cue':True}
h=generate_hypotheses(graph,cover); rows.append(row('five_hypotheses_and_composition_specs',h.get('status')=='PASS' and len(h.get('hypotheses',[]))==5 and all(x.get('composition_spec') for x in h.get('hypotheses',[])),h.get('reason')))
rows.append(row('image_led_reachable',any(x.get('communication_strategy')=='IMAGE_LED' for x in h.get('hypotheses',[])),[x.get('communication_strategy') for x in h.get('hypotheses',[])]))
rows.append(row('composition_divergence_floor',(h.get('composition_divergence') or {}).get('status')=='PASS',h.get('composition_divergence')))
# Separate analytical specs guarantee measurable diversity.
strategies=['STATEMENT_LED','SYSTEM_LED','TABLE_LED','TIMELINE_LED','CHART_LED']
specs=[]
for i,st in enumerate(strategies):
    hyp={'id':f'H{i+1}','communication_strategy':st,'strategy_family':'TEST','page_fingerprint':'X'}
    cp={'page_id':f'P{i+2:02d}','language':'AR','title':'قرار تنفيذي','thesis':'لا تتحمل الجهة مخاطر غير محسوبة','proof_points':['دليل أول','دليل ثان','دليل ثالث']}
    specs.append(build_page_composition_spec(hyp,cp,graph,variant_index=i))
div=evaluate_set(specs); rows.append(row('spec_diversity_is_structural',div['status']=='PASS' and div['min_pairwise']>=.12 and div['mean_pairwise']>=.18,div))
rows.append(row('composition_specs_validate',all(validate_page_composition_spec(x)['status']=='PASS' for x in specs)))
# Missing brand font must never silently pass production.
fp=check_brand_fonts(('Montserrat Arabic','Montserrat')); rows.append(row('brand_font_preflight_truthful',fp['status'] in ('PASS','BLOCKED') and (fp['status']=='PASS' or bool(fp['missing'])),fp))
# Host-native image path must pend instead of degrading to cards.
imgspec=next((x['composition_spec'] for x in h['hypotheses'] if x['communication_strategy']=='IMAGE_LED'),None)
req=build_image_request(imgspec,cover); pend=HostNativeImagePendingProvider().generate(req.get('request') or {}); rows.append(row('image_provider_pending_fail_closed',pend.get('status')=='HOST_NATIVE_IMAGE_PENDING',pend.get('status')))
brand_logo=ROOT/'Rashad/Skill/08_BRAND_CURRENT/assets/rubix-consulting-current-light.png'
client_logo=QR/'fixtures/client_test.png'
with tempfile.TemporaryDirectory() as td:
    td=Path(td); pngs=[]; expected=[]
    for i,spec in enumerate(specs[:3]):
        if i==1:
            cp={'page_id':spec['page_id'],'language':'AR','title':'منهجية التنفيذ','thesis':'نحوّل دورة التنفيذ إلى نظام مترابط تحكمه بوابات قرار وتغذية راجعة','proof_points':['كل مرحلة تنتج قرارًا أو دليلًا قابلًا للمراجعة','الحوكمة وضمان الجودة تعبران جميع المراحل','المقيّم يرى نظام تشغيل مغلقًا'],'executive_implication':'المقيّم يرى نظام تشغيل مترابطًا يمكن استمراره بعد انتهاء العقد','source_note':'EV-0001'}
        else:
            cp={'page_id':spec['page_id'],'language':'AR','title':f'صفحة {i+1}','thesis':'لا تتحمل الجهة مخاطر غير محسوبة','proof_points':['إثبات واحد','إثبات ثان','إثبات ثالث'],'source_note':'EV-0001'}
        r=render_composition_page(spec,cp,graph,td/f'r{i}',allow_test_font_fallback=True,emit_pdf=True,brand_logo=brand_logo,client_logo=client_logo)
        rows.append(row(f'production_render_{i+1}',r.get('status')=='PASS' and r.get('render_kind')=='PRODUCTION_PAGE_RENDER',r.get('reason')))
        if r.get('status')=='PASS':
            sm=inspect_semantic_html_master(r['html_master_path'],spec)
            pngs.append(r['render_path'])
            expected.append({
                'selected_strategy':spec['communication_strategy'],
                'html_master_sha256':r.get('html_master_sha256'),
                'composition_spec_sha256':r.get('composition_spec_sha256'),
                'composition_spec':spec,
                'semantic_master_qa':sm,
            })
            html=Path(r['html_master_path']).read_text(encoding='utf-8')
            rows.append(row(f'semantic_master_gate_{i+1}',sm.get('status')=='PASS',sm))
            rows.append(row(f'composer_instrumentation_{i+1}',all(x in html for x in ['data-region-id="DOMINANT"','data-node-id','data-page-mode="ARTIFACT_LED"','document.fonts.ready'])))
            if i==0:
                rows.append(row('arabic_numeral_island_composer','صفحة ' in html and '>١</bdi>' in html and 'data-directionality="ISOLATED"' in html and '>1</bdi>' not in html,{'arabic_indic':('>١</bdi>' in html),'isolated_bdi':('data-directionality="ISOLATED"' in html)}))
                ti=inspect_pdf_text_layer(r['pdf_path'],['لا تتحمل الجهة مخاطر غير محسوبة'])
                rows.append(row('pdf_text_layer_integrity_good',ti['status']=='PASS',ti))
            if i==1:  # SYSTEM_LED analytical page must pass the complete production QA, not only semantic inspection.
                qspec=json.loads((QR/'fixtures/page_spec.json').read_text()); qspec['artifact_family']='SYSTEM'; qspec['artifact_expected']=True; qspec['content_pack']['sources']=['EV-0001']
                qout=td/'full_qa'; qout.mkdir(exist_ok=True)
                ledger=json.loads((QR/'fixtures/evidence_ledger.json').read_text(encoding='utf-8'))
                exhibit=json.loads((QR/'fixtures/exhibit.json').read_text(encoding='utf-8'))
                uq=unified_html_run(Path(r['html_master_path']),QR/'config/profile_test.json',qspec,graph,exhibit,qout,'.page',False,ledger)
                ce=(uq.get('pages') or [{}])[0].get('ceqs',{})
                rows.append(row('composer_full_unified_qa',uq.get('release_verdict')=='HTML_PREEXPORT_PASS' and float(ce.get('score',0))>=90,{'verdict':uq.get('release_verdict'),'ceqs':ce,'blockers':(uq.get('pages') or [{}])[0].get('blocking_gates',[])}))
    if len(pngs)==3:
        pr=build_image_master_pptx(pngs,td/'projection.pptx'); pi=inspect_product(pr['pptx_path'],expected)
        rows.append(row('raster_projection_format_inspection',pi.get('status')=='PASS' and (pi.get('stats') or {}).get('raster_only') is True,{'status':pi.get('status'),'warnings':pi.get('warnings'),'blockers':pi.get('blockers')}))
    bad=inspect_product(td/'unknown.xyz'); rows.append(row('unknown_format_refused',bad.get('status')=='BLOCKED' and 'NO_REGISTERED_INSPECTOR_FOR_FORMAT' in bad.get('blockers',[]),bad))
out={'suite':'Visual Production Organ v7.3','status':'PASS' if all(x['status']=='PASS' for x in rows) else 'FAIL','passed':sum(x['status']=='PASS' for x in rows),'total':len(rows),'tests':rows}
(ROOT/'QA/Certification/VISUAL_PRODUCTION_V7_3_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 1)
