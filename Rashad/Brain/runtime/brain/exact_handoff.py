from __future__ import annotations
from pathlib import Path
from collections import Counter
import hashlib, json, re, zipfile, uuid
from .product_inspector import inspect_pptx, inspect_pdf, sha256_file
from .pdf_text_integrity import inspect_pdf_text_layer

IMAGE_REQUIRED_STRATEGIES={'IMAGE_LED'}


def _id(prefix:str)->str:
    return prefix+'-'+uuid.uuid4().hex[:16].upper()


def _media_profile(path:Path, product:dict)->dict:
    media=[]
    try:
        with zipfile.ZipFile(path,'r') as z:
            for n in z.namelist():
                if n.startswith('ppt/media/') and not n.endswith('/'):
                    b=z.read(n); media.append({'name':n,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)})
    except Exception:
        return {'media_count':0,'unique_media_count':0,'unique_media_hashes':[],'likely_logo_only_images':False}
    hashes=[x['sha256'] for x in media]; uniq=sorted(set(hashes))
    total_pictures=sum(int(s.get('pictures',0) or 0) for s in product.get('slides',[]))
    slide_count=max(1,int(product.get('slide_count',0) or 0))
    # A single unique picture repeated across most pages is overwhelmingly likely to be logo/chrome,
    # not actual artifact imagery. A single image used on one page is allowed.
    likely_logo_only=bool(uniq) and len(uniq)==1 and total_pictures>=max(2, round(slide_count*.75))
    return {
        'media_count':len(media),'unique_media_count':len(uniq),'unique_media_hashes':uniq,
        'total_picture_shapes':total_pictures,'picture_slide_ratio':round(total_pictures/slide_count,3),
        'likely_logo_only_images':likely_logo_only,'media':media,
    }


def _trace_claimed_counts(trace_path:Path|None)->list[int]:
    if not trace_path or not Path(trace_path).exists(): return []
    txt=Path(trace_path).read_text(encoding='utf-8',errors='ignore')
    nums=[]
    pats=[r'(\d+)\s*[- ]?page\b',r'actual pixel reviews\s*[:=]\s*(\d+)\s*/\s*(\d+)',r'(\d+)\s*/\s*(\d+)\s*actual pixel',r'page count\s*[:=]\s*(\d+)']
    for pat in pats:
        for m in re.finditer(pat,txt,re.I):
            nums.extend(int(x) for x in m.groups() if x and x.isdigit())
    return nums


def verify_exact_artifact_handoff(pptx_path, dossier, trace_path=None, certificate=None, pdf_path=None)->dict:
    p=Path(pptx_path); blockers=[]; warnings=[]
    if not p.exists():
        return {'schema':'RASHAD_EXACT_ARTIFACT_HANDOFF_V7_2_1','status':'BLOCK_HANDOFF','blockers':['DELIVERED_PPTX_NOT_FOUND']}
    if isinstance(dossier,(str,Path)):
        dossier=json.loads(Path(dossier).read_text(encoding='utf-8'))
    dossier=dict(dossier or {})
    product=inspect_pptx(p,dossier.get('pages') or [])
    actual_sha=sha256_file(p); actual_slides=product.get('slide_count',0)
    media=_media_profile(p,product)

    # Exact file identity: every artifact-level QA record must point to the delivered bytes.
    expected=dossier.get('output_file_sha256')
    if not expected: blockers.append('DELIVERY_DOSSIER_OUTPUT_SHA_MISSING')
    elif expected!=actual_sha: blockers.append('DELIVERED_PPTX_SHA_MISMATCH_DOSSIER')
    deck_review=dossier.get('deck_pixel_review') or {}
    if deck_review.get('status')!='PASS': blockers.append('DECK_PIXEL_REVIEW_NOT_PASS')
    if deck_review.get('independent') is not True: blockers.append('DECK_PIXEL_REVIEW_NOT_INDEPENDENT')
    if deck_review.get('deck_sha256')!=actual_sha: blockers.append('DELIVERED_PPTX_SHA_MISMATCH_DECK_PIXEL_REVIEW')
    recorded_product=dossier.get('product_inspection') or {}
    if recorded_product.get('pptx_sha256')!=actual_sha: blockers.append('DELIVERED_PPTX_SHA_MISMATCH_PRODUCT_INSPECTION')
    if recorded_product.get('slide_count') is not None and recorded_product.get('slide_count')!=actual_slides:
        blockers.append('DELIVERED_SLIDE_COUNT_MISMATCH_PRODUCT_INSPECTION')

    pages=list(dossier.get('pages') or [])
    if not pages: blockers.append('DELIVERY_DOSSIER_PAGES_MISSING')
    if len(pages)!=actual_slides: blockers.append('DELIVERED_SLIDE_COUNT_MISMATCH_DOSSIER_PAGES')
    pixel_pass=sum(1 for pg in pages if (pg.get('actual_pixel_review') or {}).get('status')=='PASS')
    production_count=sum(1 for pg in pages if pg.get('render_kind')=='PRODUCTION_PAGE_RENDER' and pg.get('production_render_id'))
    if pixel_pass!=actual_slides: blockers.append('PIXEL_REVIEW_COUNT_MISMATCH_DELIVERED_SLIDES')
    if production_count!=actual_slides: blockers.append('PRODUCTION_RENDER_COUNT_MISMATCH_DELIVERED_SLIDES')
    for idx,pg in enumerate(pages,1):
        review=pg.get('actual_pixel_review') or {}; sel=pg.get('selected_render_hash')
        if review.get('status')=='PASS' and review.get('actual_render_hash')!=sel:
            blockers.append(f'PAGE_{idx}_PIXEL_REVIEW_RENDER_HASH_MISMATCH')

    # Strategy truth must be visible in the actual product, not just metadata.
    image_led=[i for i,pg in enumerate(pages,1) if pg.get('selected_strategy') in IMAGE_REQUIRED_STRATEGIES]
    slides=product.get('slides') or []
    for idx in image_led:
        slide=slides[idx-1] if idx-1<len(slides) else {}
        if int(slide.get('pictures',0) or 0)<1: blockers.append(f'SLIDE_{idx}_IMAGE_LED_WITHOUT_IMAGE')
    if image_led and media.get('likely_logo_only_images'):
        blockers.append('IMAGE_LED_DECLARED_BUT_IMAGES_APPEAR_LOGO_ONLY')

    # Raster projections are permitted only as projections of independently QA'd semantic HTML masters.
    if (product.get('stats') or {}).get('raster_only'):
        if any(not pg.get('html_master_sha256') or not pg.get('composition_spec_sha256') or not pg.get('composition_spec') for pg in pages):
            blockers.append('RASTER_PROJECTION_WITHOUT_SEMANTIC_HTML_MASTER_PROOF')
        specs=[pg.get('composition_spec') or {} for pg in pages]
        sigs=[x.get('structural_signature') for x in specs if x.get('structural_signature')]
        if len(pages)>=6 and len(set(sigs))/max(1,len(pages)) < .70:
            blockers.append('RASTER_PROJECTION_COMPOSITION_SPEC_DIVERSITY_FLOOR_NOT_MET')
        for i,x in enumerate(specs,1):
            if i>1 and x and x.get('page_family') not in ('COVER','SECTION_OPENER'):
                m=float(x.get('dominant_mass_target',0) or 0)
                if not .32<=m<=.68: blockers.append(f'PAGE_{i}_COMPOSITION_SPEC_DOMINANT_MASS_OUT_OF_BAND')

    # Generic composer / product quality failures are handoff blockers too.
    if product.get('status')!='PASS':
        blockers.append('DELIVERED_PPTX_PRODUCT_INSPECTION_NOT_PASS')
        blockers.extend('PRODUCT_INSPECTION::'+str(x) for x in product.get('blockers',[]))

    # Final trace may only describe the actual delivered deck.
    trace_counts=_trace_claimed_counts(Path(trace_path) if trace_path else None)
    if trace_counts and any(n!=actual_slides and n>=8 for n in trace_counts):
        blockers.append('FINAL_TRACE_DESCRIBES_DIFFERENT_PAGE_COUNT_THAN_DELIVERED_FILE')

    pdf_info=None
    if pdf_path:
        q=Path(pdf_path)
        if not q.exists(): blockers.append('DELIVERED_PDF_NOT_FOUND')
        else:
            pdf_sha=sha256_file(q); pdf_product=inspect_pdf(q,pages); expected_text=[]
            for pg in pages:
                expected_text.extend(pg.get('visible_text_samples') or [])
            text_layer=inspect_pdf_text_layer(q,expected_text)
            pdf_info={'path':str(q),'sha256':pdf_sha,'bytes':q.stat().st_size,'product_inspection':pdf_product,'text_layer_integrity':text_layer}
            expected_pdf=dossier.get('pdf_file_sha256')
            if not expected_pdf: blockers.append('DELIVERY_DOSSIER_PDF_SHA_MISSING')
            elif expected_pdf!=pdf_sha: blockers.append('DELIVERED_PDF_SHA_MISMATCH_DOSSIER')
            if pdf_product.get('page_count')!=actual_slides: blockers.append('PDF_PPTX_PAGE_COUNT_MISMATCH')
            if pdf_product.get('status')!='PASS': blockers.append('DELIVERED_PDF_PRODUCT_INSPECTION_NOT_PASS')
            if text_layer.get('status')!='PASS': blockers.append('DELIVERED_PDF_TEXT_LAYER_INTEGRITY_NOT_PASS')

    # If a previously issued certificate is supplied, it must bind these exact bytes.
    if certificate:
        if isinstance(certificate,(str,Path)): certificate=json.loads(Path(certificate).read_text(encoding='utf-8'))
        if certificate.get('pptx_sha256')!=actual_sha: blockers.append('HANDOFF_CERTIFICATE_PPTX_SHA_MISMATCH')
        if certificate.get('slide_count')!=actual_slides: blockers.append('HANDOFF_CERTIFICATE_SLIDE_COUNT_MISMATCH')
        if pdf_info and certificate.get('pdf_sha256') and certificate.get('pdf_sha256')!=pdf_info['sha256']:
            blockers.append('HANDOFF_CERTIFICATE_PDF_SHA_MISMATCH')

    return {
        'schema':'RASHAD_EXACT_ARTIFACT_HANDOFF_V7_2_1',
        'status':'HANDOFF_ALLOWED' if not blockers else 'BLOCK_HANDOFF',
        'pptx_path':str(p),'pptx_sha256':actual_sha,'pptx_bytes':p.stat().st_size,'slide_count':actual_slides,
        'dossier_page_count':len(pages),'pixel_review_pass_count':pixel_pass,'production_render_count':production_count,
        'image_led_pages':image_led,'media_profile':media,'product_inspection':product,'trace_claimed_counts':trace_counts,
        'pdf':pdf_info,'blockers':sorted(set(blockers)),'warnings':warnings,
        'rule':'The exact delivered bytes, page count, production renders, pixel reviews, product structure and final trace must all describe one artifact. Otherwise BLOCK_HANDOFF.'
    }


def issue_exact_handoff_certificate(pptx_path,dossier,trace_path=None,pdf_path=None)->dict:
    check=verify_exact_artifact_handoff(pptx_path,dossier,trace_path=trace_path,pdf_path=pdf_path)
    if check.get('status')!='HANDOFF_ALLOWED':
        return {'schema':'RASHAD_EXACT_HANDOFF_CERTIFICATE_V7_2_1','status':'BLOCK_HANDOFF','blockers':check.get('blockers',[]),'verification':check}
    return {
        'schema':'RASHAD_EXACT_HANDOFF_CERTIFICATE_V7_2_1','status':'CERTIFIED_FOR_HANDOFF','certificate_id':_id('HANDOFF'),
        'pptx_sha256':check['pptx_sha256'],'pptx_bytes':check['pptx_bytes'],'slide_count':check['slide_count'],
        'pdf_sha256':(check.get('pdf') or {}).get('sha256'),'dossier_page_count':check['dossier_page_count'],
        'pixel_review_pass_count':check['pixel_review_pass_count'],'production_render_count':check['production_render_count'],
        'image_led_pages':check['image_led_pages'],'product_inspection_status':check['product_inspection'].get('status'),
        'verification':check,
    }
