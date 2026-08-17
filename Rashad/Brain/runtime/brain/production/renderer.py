from __future__ import annotations
from pathlib import Path
import hashlib,os,shutil
from playwright.sync_api import sync_playwright
from .font_preflight import check_brand_fonts
from .composer import compose_html
from .searchable_pdf import build_searchable_image_pdf, logical_text_lines

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def render_composition_page(spec,content_pack,semantic_graph,out_dir,image_asset=None,brand_logo=None,client_logo=None,allow_test_font_fallback=False,emit_pdf=False):
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    fonts=check_brand_fonts((spec.get('typographic_hierarchy') or {}).get('font_family','Montserrat'),allow_test_fallback=allow_test_font_fallback) if False else check_brand_fonts(((spec.get('typographic_hierarchy') or {}).get('font_family','Montserrat'),),allow_test_fallback=allow_test_font_fallback)
    if fonts['status']!='PASS': return {'status':'BLOCKED','reason':'BRAND_FONT_PREFLIGHT_FAILED','font_preflight':fonts}
    hp=out/'production_master.html'; cp=compose_html(spec,content_pack,semantic_graph,hp,image_asset=image_asset,brand_logo=brand_logo,client_logo=client_logo)
    png=out/'production_page.png'; pdf=out/'production_page.pdf'
    exe=os.getenv('RASHAD_CHROMIUM') or shutil.which('chromium') or shutil.which('google-chrome')
    launch={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files']}
    if exe: launch['executable_path']=exe
    render_attempts=[]
    try:
        with sync_playwright() as p:
            last_error=None
            for attempt in (1,2):
                b=None
                try:
                    b=p.chromium.launch(**launch)
                    page=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
                    page.set_content(hp.read_text(encoding='utf-8'),wait_until='load')
                    page.evaluate('()=>document.fonts.ready')
                    page.wait_for_function("document.documentElement.dataset.rashadLayoutReady==='1'")
                    page.wait_for_timeout(80 if attempt==1 else 180)
                    page.screenshot(path=str(png),full_page=False)
                    render_attempts.append({'attempt':attempt,'status':'PASS'})
                    b.close(); b=None
                    last_error=None
                    break
                except Exception as e:
                    last_error=e
                    render_attempts.append({'attempt':attempt,'status':'FAIL','error':repr(e)[:500]})
                    try:
                        if b: b.close()
                    except Exception:
                        pass
                    # Only a bounded second attempt is allowed. No generic fallback renderer.
                    if attempt==2:
                        raise
        # PDF is built from the exact rendered pixels plus a separately governed logical Unicode text layer.
        # Chromium print-to-PDF reverses Arabic logical order/lam-alef in extraction on some hosts.
        if emit_pdf:
            pr=build_searchable_image_pdf(png,pdf,logical_text_lines(content_pack,semantic_graph))
            if pr.get('status')!='PASS': return {'status':'BLOCKED','reason':'SEARCHABLE_PDF_BUILD_FAILED','pdf_result':pr,'html':cp,'render_attempts':render_attempts}
    except Exception as e: return {'status':'BLOCKED','reason':'CHROMIUM_PRODUCTION_RENDER_FAILED','error':repr(e),'html':cp,'render_attempts':render_attempts}
    r={'status':'PASS','render_kind':'PRODUCTION_PAGE_RENDER','production_render_id':'PROD-'+sha(png)[:20].upper(),'render_path':str(png),'actual_render_hash':sha(png),'html_master_path':str(hp),'html_master_sha256':sha(hp),'font_preflight':fonts,'composition_spec_sha256':spec.get('spec_sha256'),'render_attempts':render_attempts}
    if emit_pdf and pdf.exists(): r.update({'pdf_path':str(pdf),'pdf_sha256':sha(pdf)})
    return r
