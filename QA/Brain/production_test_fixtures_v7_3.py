from __future__ import annotations
from pathlib import Path
import hashlib
from PIL import Image,ImageDraw

from brain.composition_spec import build_page_composition_spec
from brain.production.renderer import render_composition_page
from brain.production.projector import build_image_master_pptx
from brain.semantic_master_gate import inspect_semantic_html_master


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def make_visual_plate(path, seed=1):
    """Certification-only text/logo/number-free visual plate."""
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    im=Image.new('RGB',(1920,1080),(246,244,243)); d=ImageDraw.Draw(im)
    # Deliberately asymmetric large masses; no text/glyphs/logos/numerals.
    x=120+((seed*137)%380); y=170+((seed*83)%220)
    d.rounded_rectangle((x,y,x+820,y+620),radius=80,fill=(226,218,222),outline=(164,35,101),width=8)
    d.ellipse((x+520,y+160,x+1120,y+760),fill=(224,239,239),outline=(7,115,129),width=7)
    d.line((x+100,y+510,x+1150,y+210),fill=(164,35,101),width=10)
    im.save(p)
    return p


def make_montage(images,path,cols=4):
    imgs=[Image.open(x).convert('RGB') for x in images]
    thumb=(480,270); rows=(len(imgs)+cols-1)//cols
    out=Image.new('RGB',(thumb[0]*cols,thumb[1]*rows),'white')
    for i,im in enumerate(imgs):
        c=i%cols; r=i//cols; im.thumbnail(thumb); out.paste(im,(c*thumb[0],r*thumb[1]))
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); out.save(p)
    return p


def graph_for(i:int):
    return {
      'nodes':[
        {'id':f'N{i}A','label':'الدليل','type':'EVIDENCE'},
        {'id':f'N{i}B','label':'القرار','type':'DECISION'},
        {'id':f'N{i}C','label':'التنفيذ','type':'PROCESS'},
      ],
      'edges':[
        {'id':f'E{i}1','source':f'N{i}A','target':f'N{i}B','relation':'SUPPORTS'},
        {'id':f'E{i}2','source':f'N{i}B','target':f'N{i}C','relation':'ENABLES'},
      ]
    }


def content_for(i:int,strategy:str):
    return {
      'page_id':f'P{i:02d}','language':'AR','page_role':'ANALYTICAL',
      'title':f'قرار تنفيذي {i}',
      'thesis':'لا تتحمل الجهة مخاطر غير محسوبة؛ القرار يرتبط بالدليل والقبول.',
      'proof_points':['دليل مثبت من المصدر','أثر واضح على القرار','إجراء مطلوب قبل الاعتماد'],
      'source_note':'SRC-CERTIFICATION','chart_values':[82,64,47,91],
      'numbers':[82,64,47,91] if strategy in {'NUMBER_LED','CHART_LED','SCORECARD_LED'} else [],
    }


def hypothesis_for(i:int,strategy:str):
    family={
      'STATEMENT_LED':'MINIMAL','NUMBER_LED':'MINIMAL','EVIDENCE_LED':'ANALYTICAL','TABLE_LED':'ANALYTICAL',
      'CHART_LED':'QUANTITATIVE','COMPARISON_LED':'ANALYTICAL','MATRIX_LED':'ANALYTICAL','DECISION_LED':'DECISION',
      'PROCESS_LED':'RELATIONAL','SEQUENCE_LED':'RELATIONAL','SYSTEM_LED':'RELATIONAL','ARCHITECTURE_LED':'RELATIONAL',
      'JOURNEY_LED':'RELATIONAL','IMAGE_LED':'IMAGE','SCORECARD_LED':'QUANTITATIVE','HYBRID_EXHIBIT':'HYBRID'
    }.get(strategy,'ANALYTICAL')
    return {'id':f'HSEL-{i}','communication_strategy':strategy,'strategy_family':family,'page_fingerprint':f'CERT-V73-P{i}-{strategy}'}


def build_production_projection(td:Path, strategies:list[str]):
    """Build a certification-only but fully governed semantic-master -> pixel -> PPTX projection.
    Returns production evidence sufficient for current exact-handoff/product gates.
    """
    td=Path(td); td.mkdir(parents=True,exist_ok=True)
    pngs=[]; page_proofs=[]; renders=[]
    for i,strategy in enumerate(strategies,1):
        cp=content_for(i,strategy); graph=graph_for(i); hyp=hypothesis_for(i,strategy)
        spec=build_page_composition_spec(hyp,cp,graph,variant_index=i)
        asset=None
        if strategy=='IMAGE_LED': asset=make_visual_plate(td/f'plate_{i}.png',i)
        r=render_composition_page(spec,cp,graph,td/f'page_{i:02d}',image_asset=asset,allow_test_font_fallback=True,emit_pdf=True)
        if r.get('status')!='PASS':
            return {'status':'BLOCKED','reason':'PRODUCTION_RENDER_FAILED','page':i,'render':r}
        sm=inspect_semantic_html_master(r['html_master_path'],spec)
        if sm.get('status')!='PASS':
            return {'status':'BLOCKED','reason':'SEMANTIC_MASTER_FAILED','page':i,'semantic_master_qa':sm}
        pngs.append(Path(r['render_path'])); renders.append(r)
        page_proofs.append({
          'page_id':cp['page_id'],'selected_strategy':strategy,
          'html_master_sha256':r['html_master_sha256'],'composition_spec_sha256':r['composition_spec_sha256'],
          'composition_spec':spec,'semantic_master_qa':sm,
          'composition_logic':spec.get('structural_signature'),
          'visible_text_samples':['لا تتحمل الجهة مخاطر غير محسوبة'],
        })
    pr=build_image_master_pptx(pngs,td/'governed_projection.pptx')
    montage=make_montage(pngs,td/'montage.png')
    return {
      'status':'PASS','pptx_path':pr['pptx_path'],'pptx_sha256':pr['pptx_sha256'],'page_count':len(pngs),
      'page_images':[str(x) for x in pngs],'pages':page_proofs,'renders':renders,
      'montage_path':str(montage),'montage_sha256':sha256_file(montage)
    }
