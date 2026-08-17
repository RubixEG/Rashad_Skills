from __future__ import annotations
from pathlib import Path
import hashlib
from PIL import Image,ImageFilter,ImageStat

def sha256_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fingerprint(p):
    im=Image.open(p).convert('RGB'); im.thumbnail((320,180)); mean=ImageStat.Stat(im).mean
    edges=im.convert('L').filter(ImageFilter.FIND_EDGES); edge=sum(ImageStat.Stat(edges).mean)
    h=im.histogram(); vec=[]
    for ch in range(3):
        arr=h[ch*256:(ch+1)*256]; total=max(1,sum(arr)); vec.extend([sum(arr[i:i+32])/total for i in range(0,256,32)])
    return {'mean_rgb':mean,'edge_density':edge,'hist':vec}
def distance(a,b):
    return {'lightness_delta':abs(sum(a['mean_rgb'])/3-sum(b['mean_rgb'])/3),'edge_density_delta':abs(a['edge_density']-b['edge_density']),'hist_l1':sum(abs(x-y) for x,y in zip(a['hist'],b['hist']))}
def evaluate_ledger(obj):
    pages=list(obj.get('pages') or []); th=obj.get('thresholds') or {'lightness_delta_max':75,'edge_density_delta_max':45,'hist_l1_max':1.8}
    viol=[]; measured=[]; fps={}; ids=[p.get('page_id') for p in pages]
    if not pages: viol.append({'problem':'zero_pages'})
    for i,p in enumerate(pages):
        mp=Path(p.get('master_path','')); expected=p.get('master_sha256')
        if not mp.exists(): viol.append({'page_id':p.get('page_id'),'problem':'master missing','path':str(mp)}); continue
        actual=sha256_file(mp)
        if expected and actual.lower()!=str(expected).lower(): viol.append({'page_id':p.get('page_id'),'problem':'master hash mismatch','expected':expected,'actual':actual})
        if i>0 and p.get('previous_page_id') not in (None,ids[i-1]): viol.append({'page_id':p.get('page_id'),'problem':'previous-page continuity link mismatch','expected':ids[i-1],'actual':p.get('previous_page_id')})
        fps[i]=fingerprint(mp)
        anchor=Path(p.get('style_anchor_path','')) if p.get('style_anchor_path') else None
        if anchor and anchor.exists():
            d=distance(fingerprint(anchor),fps[i]); measured.append({'page_id':p.get('page_id'),'comparison':'declared_style_anchor','anchor':str(anchor),**d})
            if d['lightness_delta']>th['lightness_delta_max'] or d['edge_density_delta']>th['edge_density_delta_max'] or d['hist_l1']>th['hist_l1_max']:
                viol.append({'page_id':p.get('page_id'),'problem':'visual fingerprint drift beyond approved anchor tolerance',**d})
        elif i>0 and i-1 in fps:
            d=distance(fps[i-1],fps[i]); measured.append({'page_id':p.get('page_id'),'comparison':'adjacent_page_style_continuity','anchor_page_id':ids[i-1],**d})
            # Adjacent pages may intentionally differ; only catastrophic style discontinuity blocks.
            if d['lightness_delta']>th['lightness_delta_max']*1.35 or d['edge_density_delta']>th['edge_density_delta_max']*1.35 or d['hist_l1']>th['hist_l1_max']*1.35:
                viol.append({'page_id':p.get('page_id'),'problem':'catastrophic_adjacent_style_discontinuity',**d})
    return {'status':'PASS' if not viol else 'FAIL','verdict':'DECK_CONTINUITY_PASS' if not viol else 'BLOCKED','violations':viol,'measurements':measured,'thresholds':th,'page_count':len(pages)}
