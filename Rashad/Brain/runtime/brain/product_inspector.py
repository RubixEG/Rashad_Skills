from __future__ import annotations
from pathlib import Path
import hashlib,zipfile
from .product_geometry import inspect_artifact

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def _compat(model):
    slides=[]
    for p in model.get('pages',[]):
        kinds={k:0 for k in ('shape','text_shape','picture','table','chart','graphic')}
        for e in p.get('elements',[]): kinds[e['kind']]=kinds.get(e['kind'],0)+1
        slides.append({'slide':p['page'],'shapes':kinds.get('shape',0)+kinds.get('text_shape',0),'pictures':kinds.get('picture',0),'tables':kinds.get('table',0),'charts':kinds.get('chart',0),'graphic_frames':kinds.get('graphic',0)+kinds.get('table',0)+kinds.get('chart',0),'connectors':0,'text_runs':len(p.get('texts',[])),'text_chars':sum(len(x) for x in p.get('texts',[])),'max_equal_text_shape_count':p.get('max_equal_box_count',0),'equal_card_grid_like':p.get('equal_card_grid_like',False),'structural_fingerprint':p.get('fingerprint')})
    return slides

def inspect_pptx(path,expected_pages=None):
    m=inspect_artifact(path,expected_pages)
    # Backward-compatible blocker aliases for inherited v7.2 regression harnesses; current format-neutral blocker IDs remain authoritative.
    bs=list(m.get('blockers',[]))
    if 'EQUAL_CARD_GRID_OVERUSE' in bs and 'PPTX_EQUAL_CARD_GRID_OVERUSE' not in bs: bs.append('PPTX_EQUAL_CARD_GRID_OVERUSE')
    if 'SHAPE_ONLY_ANALYTICAL_DECK_OVERUSE' in bs and 'PPTX_SHAPE_ONLY_ANALYTICAL_DECK_OVERUSE' not in bs: bs.append('PPTX_SHAPE_ONLY_ANALYTICAL_DECK_OVERUSE')
    m['blockers']=bs
    m['pptx_sha256']=m.get('file_sha256'); m['slide_count']=m.get('page_count',0); m['slides']=_compat(m)
    try:
        with zipfile.ZipFile(path) as z:
            media=[n for n in z.namelist() if n.startswith('ppt/media/') and not n.endswith('/')]; hs=[hashlib.sha256(z.read(n)).hexdigest() for n in media]
        m['media_count']=len(hs); m['unique_media_count']=len(set(hs)); m['unique_media_hashes']=sorted(set(hs)); m['total_picture_shapes']=sum(x['pictures'] for x in m['slides']); m['likely_logo_only_images']=bool(hs) and len(set(hs))==1 and m['total_picture_shapes']>=max(2,round(max(1,m['slide_count'])*.75))
    except Exception:
        m.update({'media_count':0,'unique_media_count':0,'unique_media_hashes':[],'total_picture_shapes':0,'likely_logo_only_images':False})
    return m

def inspect_pdf(path,expected_pages=None): return inspect_artifact(path,expected_pages)
def inspect_product(path,expected_pages=None): return inspect_artifact(path,expected_pages)
