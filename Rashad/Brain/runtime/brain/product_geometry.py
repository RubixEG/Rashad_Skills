from __future__ import annotations
from pathlib import Path
from collections import Counter
import hashlib,math,re,zipfile,xml.etree.ElementTree as ET
from brain.quality_floors_v7_3 import get as quality_floor

P='http://schemas.openxmlformats.org/presentationml/2006/main'; A='http://schemas.openxmlformats.org/drawingml/2006/main'; C='http://schemas.openxmlformats.org/drawingml/2006/chart'
NS={'p':P,'a':A,'c':C}
AR=re.compile(r'[\u0600-\u06ff]'); LAT=re.compile(r'[A-Za-z]'); ARDIG=re.compile(r'[٠-٩۰-۹]'); EUDIG=re.compile(r'[0-9]')
TECH={'AI','API','SLA','BOQ','ISO','PDF','RFP','UAT','KPI','PMO','ERP','CRM','SOC','SIEM','MFA','PAM','WAF','SQL','HTTP','HTTPS','JSON','XML','GPU','CPU','LLM','ML','NLP','OCR','UX','UI'}
INTERNAL={'READY','NEXT','BLOCKED','NEXT_STEP','PRODUCT_STATUS','Compliance Register v0','P0 Proposal Control Layer','Artifact Draft','internal production metadata','qa harness','v7.7 Test','Rashad OS V7.2.1','Rashad OS V7.3','HOST-NATIVE','ARTIFACT_DRAFT'}

def _sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def _norm(v,total): return float(v)/float(total or 1)
def _bbox(x,y,w,h,sw,sh): return {'x':_norm(x,sw),'y':_norm(y,sh),'w':_norm(w,sw),'h':_norm(h,sh)}
def _area(b): return max(0,b['w'])*max(0,b['h'])
def _inter(a,b): return max(0,min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x']))*max(0,min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y']))

def _mass_grid(elements):
    g=[[0.0]*4 for _ in range(4)]
    for e in elements:
        b=e['bbox']; area=_area(b)
        if area<=0 or area>.92: continue
        for r in range(4):
            for c in range(4):
                cb={'x':c*.25,'y':r*.25,'w':.25,'h':.25}; g[r][c]+=min(1.0,_inter(b,cb)/(.25*.25))
    mx=max([x for row in g for x in row]+[1]); return [[round(min(1,x/mx),3) for x in row] for row in g]

def _gini(vals):
    vals=sorted(max(0,float(x)) for x in vals); n=len(vals)
    if not vals or sum(vals)==0:return 0.0
    return sum((2*i-n-1)*x for i,x in enumerate(vals,1))/(n*sum(vals))

def _fingerprint(page):
    els=[e for e in page['elements'] if _area(e['bbox'])>=.0002 and _area(e['bbox'])<.92]
    boxes=sorted((e['kind'],round(e['bbox']['x'],2),round(e['bbox']['y'],2),round(e['bbox']['w'],2),round(e['bbox']['h'],2)) for e in els)
    areas=[_area(e['bbox']) for e in els]
    return {'box_signature':boxes[:60],'mass':_mass_grid(els),'gini':round(_gini(areas),3),'dominant_mass':round(max(areas) if areas else 0,3),'object_count':len(els)}

def fingerprint_distance(a,b):
    ma=[x for row in a['mass'] for x in row]; mb=[x for row in b['mass'] for x in row]
    l1=sum(abs(x-y) for x,y in zip(ma,mb))/max(1,len(ma))
    dg=abs(a['gini']-b['gini']); dd=abs(a['dominant_mass']-b['dominant_mass']); dc=abs(a['object_count']-b['object_count'])/max(1,max(a['object_count'],b['object_count']))
    return round(min(1,0.55*l1+0.15*dg+0.2*dd+0.1*dc),4)

def _deck_diversity(pages,tau=.12):
    fps=[p['fingerprint'] for p in pages]; twins=[]
    for i,a in enumerate(fps):
        for j,b in enumerate(fps[i+1:],i+1):
            d=fingerprint_distance(a,b)
            if d<tau: twins.append({'a':i+1,'b':j+1,'distance':d})
    unique=[]
    for i,f in enumerate(fps):
        if not any(fingerprint_distance(f,u)<tau for u in unique): unique.append(f)
    return {'distinct_ratio':round(len(unique)/max(1,len(fps)),3),'twin_pairs':twins,'twin_count':len(twins),'tau':tau}

def _text_policy(texts,arabic_page):
    blockers=[]; alltext='\n'.join(texts)
    for term in INTERNAL:
        if term.lower() in alltext.lower(): blockers.append('INTERNAL_OR_DEBUG_VOCABULARY:'+term)
    if arabic_page:
        for t in texts:
            # pure latin natural-language strings are not allowed unless all tokens are known technical tokens
            toks=re.findall(r'[A-Za-z][A-Za-z0-9._/-]*',t)
            technical_identifier=bool(re.fullmatch(r'[A-Z]{2,10}(?:-[A-Z0-9]{1,12}){1,5}',t.strip(),re.I))
            if toks and not AR.search(t) and not technical_identifier:
                bad=[x for x in toks if x.upper() not in TECH and not re.fullmatch(r'[A-Z]{2,8}-?\d*',x)]
                if bad: blockers.append('ARABIC_PAGE_PURE_LATIN_VISIBLE_TEXT:'+','.join(bad[:5]))
            # Western numerals in Arabic natural language are prohibited unless adjacent to a technical token/identifier.
            if AR.search(t) and EUDIG.search(t):
                if not any(tok.upper() in TECH for tok in toks) and not re.search(r'\b[A-Z]{2,10}(?:-[A-Z0-9]{1,12})+\b',t,re.I): blockers.append('WESTERN_NUMERAL_IN_ARABIC_NATURAL_LANGUAGE:'+t[:60])
    return sorted(set(blockers))

def _analyze_pages(pages,expected_pages=None,source_format='PPTX'):
    blockers=[]; warnings=[]; exp=expected_pages or []
    for p in pages: p['fingerprint']=_fingerprint(p)
    raster_only=bool(pages) and all(sum(e['kind']=='picture' for e in p['elements'])==1 and len([e for e in p['elements'] if e['kind']!='picture'])==0 for p in pages)
    analytic=pages[1:] if len(pages)>1 else pages
    div=_deck_diversity(analytic,float(quality_floor('min_pairwise_structural_divergence_critical',.12))) if not raster_only else {'distinct_ratio':None,'twin_pairs':[],'twin_count':0,'tau':.12,'status':'NOT_APPLICABLE_TO_RASTER_PROJECTION'}
    if not raster_only and len(analytic)>=6 and div['distinct_ratio']<.70: blockers.append('DECK_DISTINCT_COMPOSITION_FLOOR_NOT_MET')
    equal=0; shape_only=0
    for i,p in enumerate(pages,1):
        areas=[]; dims=[]; kinds=Counter(e['kind'] for e in p['elements']); texts=p.get('texts',[]); arabic=any(AR.search(t) for t in texts)
        blockers.extend(f'PAGE_{i}::{x}' for x in _text_policy(texts,arabic))
        fonts=p.get('fonts') or []
        if fonts and not any('montserrat' in x.lower() for x in fonts): blockers.append(f'PAGE_{i}::BRAND_FONT_MISSING')
        for e in p['elements']:
            a=_area(e['bbox']);
            if a>float(quality_floor('safe_area_min_visible_px2',16))/(1920*1080) and a<.92: areas.append(a)
            if e['kind'] in {'shape','text_shape'} and a>.002: dims.append((round(e['bbox']['w'],2),round(e['bbox']['h'],2)))
            b=e['bbox']; margin=36/1920
            if a>float(quality_floor('safe_area_min_visible_px2',16))/(1920*1080) and e.get('intentional_bleed') is not True and (b['x']<0 or b['y']<0 or b['x']+b['w']>1 or b['y']+b['h']>1): blockers.append(f'PAGE_{i}::ELEMENT_OFF_CANVAS')
            # Format-neutral safe area: ordinary text/objects cannot hug the page edge. Large backgrounds/dominant plates are exempt.
            safe=36/1920
            if a>float(quality_floor('safe_area_min_visible_px2',16))/(1920*1080) and a<.30 and e.get('intentional_bleed') is not True and (b['x']<safe or b['y']<safe or b['x']+b['w']>1-safe or b['y']+b['h']>1-safe):
                blockers.append(f'PAGE_{i}::SAFE_AREA_VIOLATION')
        maxeq=max(Counter(dims).values()) if dims else 0
        card=maxeq>=4 and kinds['picture']==0 and kinds['table']==0 and kinds['chart']==0 and len(dims)>=6
        if i>1 and card: equal+=1
        if i>1 and kinds['picture']==0 and kinds['table']==0 and kinds['chart']==0 and (kinds['shape']+kinds['text_shape'])>=8: shape_only+=1
        p['equal_card_grid_like']=card; p['max_equal_box_count']=maxeq
        expected=exp[i-1] if i-1<len(exp) else {}
        st=expected.get('selected_strategy') or expected.get('communication_strategy')
        dm=p['fingerprint']['dominant_mass']
        if raster_only:
            pass  # structural/mass truth comes from hash-bound PageCompositionSpec + semantic HTML master.
        elif st=='IMAGE_LED':
            if kinds['picture']<1: blockers.append(f'PAGE_{i}::IMAGE_LED_WITHOUT_SUBSTANTIVE_IMAGE')
        elif i>1 and dm<float(quality_floor('dominant_mass_min',.32)): blockers.append(f'PAGE_{i}::DOMINANT_MASS_BELOW_FLOOR')
        elif i>1 and dm>float(quality_floor('dominant_mass_max',.68)): warnings.append(f'PAGE_{i}::DOMINANT_MASS_ABOVE_TARGET')
        if st=='CHART_LED' and kinds['chart']<1 and source_format=='PPTX': warnings.append(f'PAGE_{i}::CHART_LED_PROJECTED_AS_NON_NATIVE')
    denom=max(1,len(pages)-1)
    if equal/denom>.50: blockers.append('EQUAL_CARD_GRID_OVERUSE')
    if shape_only/denom>.70: blockers.append('SHAPE_ONLY_ANALYTICAL_DECK_OVERUSE')
    if raster_only:
        semantic_ok=bool(exp) and len(exp)==len(pages) and all(
            isinstance(pg,dict) and pg.get('html_master_sha256') and pg.get('composition_spec_sha256') and
            isinstance(pg.get('composition_spec'),dict) and (pg.get('semantic_master_qa') or {}).get('status')=='PASS'
            for pg in exp
        )
        if not semantic_ok: blockers.append('RASTER_ONLY_PROJECTION_WITHOUT_HASH_BOUND_SEMANTIC_MASTER_PROOF')
        else: warnings.append('RASTER_ONLY_PROJECTION_SEMANTIC_MASTER_PROOF_BOUND')
    return blockers,warnings,div,{'equal_card_pages':equal,'shape_only_pages':shape_only,'raster_only':raster_only}

def pptx_model(path,expected_pages=None):
    path=Path(path); z=zipfile.ZipFile(path); pres=ET.fromstring(z.read('ppt/presentation.xml'))
    sldsz=pres.find('.//p:sldSz',NS); sw=int(sldsz.get('cx')) if sldsz is not None else 12192000; sh=int(sldsz.get('cy')) if sldsz is not None else 6858000
    names=sorted([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)],key=lambda n:int(re.search(r'(\d+)',Path(n).stem).group(1)))
    pages=[]
    for i,n in enumerate(names,1):
        root=ET.fromstring(z.read(n)); els=[]; texts=[]; fonts=[]
        for shp in root.findall('.//p:sp',NS):
            xfrm=shp.find('./p:spPr/a:xfrm',NS); off=xfrm.find('./a:off',NS) if xfrm is not None else None; ext=xfrm.find('./a:ext',NS) if xfrm is not None else None
            tx=[(t.text or '') for t in shp.findall('.//a:t',NS) if (t.text or '').strip()]
            for rpr in shp.findall('.//a:rPr',NS)+shp.findall('.//a:defRPr',NS):
                tf=rpr.get('typeface');
                if tf: fonts.append(tf)
            if off is not None and ext is not None:
                b=_bbox(int(off.get('x','0')),int(off.get('y','0')),int(ext.get('cx','0')),int(ext.get('cy','0')),sw,sh); els.append({'kind':'text_shape' if tx else 'shape','bbox':b,'text':' '.join(tx)})
            texts.extend(tx)
        for pic in root.findall('.//p:pic',NS):
            xfrm=pic.find('./p:spPr/a:xfrm',NS); off=xfrm.find('./a:off',NS) if xfrm is not None else None; ext=xfrm.find('./a:ext',NS) if xfrm is not None else None
            if off is not None and ext is not None: els.append({'kind':'picture','bbox':_bbox(int(off.get('x','0')),int(off.get('y','0')),int(ext.get('cx','0')),int(ext.get('cy','0')),sw,sh)})
        for gf in root.findall('.//p:graphicFrame',NS):
            xfrm=gf.find('./p:xfrm',NS); off=xfrm.find('./a:off',NS) if xfrm is not None else None; ext=xfrm.find('./a:ext',NS) if xfrm is not None else None
            kind='table' if gf.find('.//a:tbl',NS) is not None else ('chart' if gf.find('.//c:chart',NS) is not None else 'graphic')
            if off is not None and ext is not None: els.append({'kind':kind,'bbox':_bbox(int(off.get('x','0')),int(off.get('y','0')),int(ext.get('cx','0')),int(ext.get('cy','0')),sw,sh)})
        pages.append({'page':i,'elements':els,'texts':texts,'fonts':sorted(set(fonts))})
    blockers,warnings,div,stats=_analyze_pages(pages,expected_pages,'PPTX')
    return {'format':'PPTX','file_sha256':_sha(path),'page_count':len(pages),'pages':pages,'blockers':sorted(set(blockers)),'warnings':sorted(set(warnings)),'diversity':div,'stats':stats}

def pdf_model(path,expected_pages=None):
    import fitz
    path=Path(path); doc=fitz.open(path); pages=[]
    for i,page in enumerate(doc,1):
        r=page.rect; sw,sh=r.width,r.height; els=[]; texts=[]; fonts=[]
        td=page.get_text('dict')
        for block in td.get('blocks',[]):
            if block.get('type')==0:
                for line in block.get('lines',[]):
                    for sp in line.get('spans',[]):
                        txt=sp.get('text',''); b=sp.get('bbox');
                        if txt.strip(): texts.append(txt)
                        if sp.get('font'): fonts.append(sp['font'])
                        if b: els.append({'kind':'text_shape','bbox':_bbox(b[0],b[1],b[2]-b[0],b[3]-b[1],sw,sh),'text':txt})
            elif block.get('type')==1 and block.get('bbox'):
                b=block['bbox']; els.append({'kind':'picture','bbox':_bbox(b[0],b[1],b[2]-b[0],b[3]-b[1],sw,sh)})
        for d in page.get_drawings():
            b=d.get('rect')
            if b: els.append({'kind':'shape','bbox':_bbox(b.x0,b.y0,b.width,b.height,sw,sh)})
        pages.append({'page':i,'elements':els,'texts':texts,'fonts':sorted(set(fonts))})
    blockers,warnings,div,stats=_analyze_pages(pages,expected_pages,'PDF')
    # text layer integrity: suspicious reversed lam-alef patterns and malformed "ال " before verbs are blocked.
    full='\n'.join(t for p in pages for t in p['texts'])
    malformed=len(re.findall(r'\bال\s+(?:ت|ي|ن|س|أ|ا)[\u0600-\u06ff]+',full))
    if malformed: blockers.append('PDF_ARABIC_TEXT_LAYER_SUSPECT_NEGATION_REVERSAL')
    return {'format':'PDF','file_sha256':_sha(path),'page_count':len(pages),'pages':pages,'blockers':sorted(set(blockers)),'warnings':sorted(set(warnings)),'diversity':div,'stats':stats,'text_layer_suspicious_sequences':malformed}

def inspect_artifact(path,expected_pages=None):
    p=Path(path); ext=p.suffix.lower()
    try:
        m=pptx_model(p,expected_pages) if ext=='.pptx' else (pdf_model(p,expected_pages) if ext=='.pdf' else None)
    except Exception as e: return {'status':'BLOCKED','format':ext,'blockers':['ARTIFACT_INSPECTION_FAILED:'+repr(e)],'warnings':[]}
    if m is None: return {'status':'BLOCKED','format':ext,'blockers':['NO_REGISTERED_INSPECTOR_FOR_FORMAT'],'warnings':[]}
    m['status']='PASS' if not m['blockers'] else 'BLOCKED'; return m
