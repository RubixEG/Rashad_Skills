from __future__ import annotations
from brain.quality_floors_v7_3 import get as quality_floor
from pathlib import Path
import hashlib, json, math, re

FORM_BY_STRATEGY={
 'STATEMENT_LED':'STATEMENT_BLOCK','NUMBER_LED':'STATEMENT_BLOCK','EVIDENCE_LED':'TABLE',
 'TABLE_LED':'TABLE','CHART_LED':'CHART','COMPARISON_LED':'MATRIX','MATRIX_LED':'MATRIX',
 'DECISION_LED':'LADDER','QUESTION_LED':'STATEMENT_BLOCK','SEQUENCE_LED':'SPINE','PROCESS_LED':'LANE',
 'SYSTEM_LED':'HUB','ARCHITECTURE_LED':'STACK','IMAGE_LED':'HERO_IMAGE','HYBRID_EXHIBIT':'FIELD',
 'SCENARIO_LED':'MATRIX','TRADEOFF_LED':'MATRIX','BEFORE_AFTER':'LANE','CAUSE_EFFECT':'SPINE',
 'PORTFOLIO_LED':'FIELD','MAP_LED':'FIELD','JOURNEY_LED':'LANE','CONTROL_TOWER_LED':'HUB','SCORECARD_LED':'MATRIX'
}
FORMS=('SPINE','RING','STACK','HUB','LANE','MATRIX','TREE','FUNNEL','FIELD','LADDER','TABLE','CHART','HERO_IMAGE','STATEMENT_BLOCK')
FOCAL_ZONES=('RIGHT_CENTER','LEFT_CENTER','TOP_RIGHT','TOP_LEFT','CENTER','BOTTOM_RIGHT','BOTTOM_LEFT')


def _h(obj)->str:
    return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()

def _seed(*xs)->int:
    return int(hashlib.sha256('|'.join(str(x) for x in xs).encode()).hexdigest()[:12],16)

def _bbox(x,y,w,h):
    return {'x':round(float(x),4),'y':round(float(y),4),'w':round(float(w),4),'h':round(float(h),4)}

def _center(b): return (b['x']+b['w']/2,b['y']+b['h']/2)

def _page_family(content_pack):
    text=' '.join(str(content_pack.get(k,'') or '') for k in ('page_role','rfp_role','role','page_family','title','eyebrow')).lower()
    if any(k in text for k in ('cover','الغلاف')): return 'COVER'
    if any(k in text for k in ('section','opener','الفصل')): return 'SECTION_OPENER'
    if any(k in text for k in ('decision','قرار الدخول','bid_decision')): return 'DECISION'
    if any(k in text for k in ('architecture','technical','system','معمار','تقني','نطاق')): return 'ARCHITECTURE'
    if any(k in text for k in ('timeline','dates','journey','roadmap','جدول','رحلة','خطة')): return 'SEQUENCE'
    return 'ANALYTICAL'

def _dominant_bbox(form,focal,mass,seed):
    # Normalized 16:9 composition boxes. Area tracks target dominant mass closely.
    if form=='HERO_IMAGE':
        return _bbox(0.0,0.0,1.0,1.0)
    if form in ('STATEMENT_BLOCK','CHART','TABLE'):
        w=min(.82,max(.48,math.sqrt(mass*1.45))); h=min(.72,max(.38,mass/max(.01,w)))
    elif form in ('STACK','SPINE','LANE','LADDER'):
        w=min(.78,max(.45,math.sqrt(mass*1.25))); h=min(.82,max(.48,mass/max(.01,w)))
    else:
        w=min(.72,max(.42,math.sqrt(mass*1.15))); h=min(.72,max(.42,mass/max(.01,w)))
    pad=.055
    if 'RIGHT' in focal: x=1-pad-w
    elif 'LEFT' in focal: x=pad
    else: x=(1-w)/2
    if focal.startswith('TOP'): y=.17
    elif focal.startswith('BOTTOM'): y=1-pad-h
    else: y=max(.19,(1-h)/2+.04)
    return _bbox(x,y,w,h)

def _negative_space(dominant,focal):
    # Explicitly typed whitespace must not overlap semantic support/content zones.
    # When the dominant is right-biased, the left band is reserved for SUPPORT;
    # only the physical gutter between support and dominant is typed as separation.
    dx,dy,dw,dh=dominant['x'],dominant['y'],dominant['w'],dominant['h']
    zones=[]
    if dx>.12:
        gutter_x=max(.205,dx-.018)
        zones.append({'type':'SEPARATION','bbox':_bbox(gutter_x,dy,.012,min(.70,dh)),'purpose':'separate evidence rail from dominant form'})
        zones.append({'type':'BREATHING','bbox':_bbox(.02,.82,max(.03,dx-.045),.07),'purpose':'protect lower-left breathing space'})
    if dx+dw<.88: zones.append({'type':'EMPHASIS_HALO','bbox':_bbox(dx+dw+.02,.18,max(.03,.96-(dx+dw+.02)),.65),'purpose':'separate dominant form'})
    zones.append({'type':'GUTTER','bbox':_bbox(.03,.03,.94,.06),'purpose':'header/footer separation'})
    return zones

def _zones(strategy,dominant,focal):
    # Content zones are semantic roles. Composer decides exact internal packing after fonts load.
    zones=[{'id':'DOMINANT','role':'DOMINANT','bbox':dominant,'z':20,'overflow':'BLOCK'}]
    if strategy!='IMAGE_LED':
        if 'RIGHT' in focal:
            # Keep a physical gutter between support evidence and the dominant form.
            sx=.04; sw=max(.14,min(.30,dominant['x']-sx-.020))
            zones.append({'id':'SUPPORT','role':'SUPPORT_EVIDENCE','bbox':_bbox(sx,max(.21,dominant['y']),sw,min(.66,dominant['h'])),'z':18,'overflow':'REFLOW'})
        else:
            right=dominant['x']+dominant['w']; sx=min(.80,right+.035); sw=max(.14,min(.30,.96-sx))
            zones.append({'id':'SUPPORT','role':'SUPPORT_EVIDENCE','bbox':_bbox(sx,max(.21,dominant['y']),sw,min(.66,dominant['h'])),'z':18,'overflow':'REFLOW'})
    zones.extend([
      {'id':'HEADER','role':'HEADER','bbox':_bbox(.055,.045,.89,.12),'z':30,'overflow':'REFLOW'},
      {'id':'FOOTER','role':'FOOTER','bbox':_bbox(.055,.93,.89,.035),'z':30,'overflow':'BLOCK'}
    ])
    return zones

def _topology(graph):
    nodes=[]; edges=[]
    for i,n in enumerate((graph or {}).get('nodes',[]) or []):
        if not isinstance(n,dict): continue
        nid=str(n.get('id') or f'N{i+1}')
        nodes.append({'id':nid,'label':str(n.get('label') or n.get('name') or nid)[:120],'type':str(n.get('type') or 'CLAIM')})
    for i,e in enumerate((graph or {}).get('edges',[]) or []):
        if not isinstance(e,dict): continue
        edges.append({'id':str(e.get('id') or f'E{i+1}'),'source':str(e.get('source') or ''),'target':str(e.get('target') or ''),'relation':str(e.get('relation') or 'RELATES_TO'),'route_hint':'AUTO_MEASURED','label_owner':'EDGE'})
    return {'nodes':nodes,'edges':edges,'crossing_budget':0 if len(edges)<=6 else 2}

def build_page_composition_spec(hypothesis, content_pack, graph, *, variant_index=0, reference_grammar_ids=None):
    strategy=str(hypothesis.get('communication_strategy') or 'STATEMENT_LED')
    family=_page_family(content_pack)
    form=FORM_BY_STRATEGY.get(strategy,'FIELD')
    seed=_seed(hypothesis.get('page_fingerprint'),strategy,variant_index,family)
    # use multiple focal anchors, deterministically, not strategy-only geometry
    focal=FOCAL_ZONES[(seed+variant_index*3)%len(FOCAL_ZONES)]
    if family=='COVER': focal='RIGHT_CENTER' if seed%2 else 'LEFT_CENTER'
    mass=.32 + ((seed>>8)%33)/100.0  # 0.32..0.64
    if form=='HERO_IMAGE': mass=.62
    dominant=_dominant_bbox(form,focal,mass,seed)
    direction='RTL' if str(content_pack.get('language','AR')).upper().startswith('AR') else 'LTR'
    title=str(content_pack.get('title') or content_pack.get('management_question') or '')
    thesis=str(content_pack.get('thesis') or content_pack.get('answer_first_thesis') or content_pack.get('answer') or '')
    spec={
      'schema':'RASHAD_PAGE_COMPOSITION_SPEC_V1','version':'1.0','page_id':content_pack.get('page_id'),
      'page_family':family,'communication_strategy':strategy,'strategy_family':hypothesis.get('strategy_family'),
      'dominant_form':form,'dominant_mass_target':round(mass,3),'dominant_bbox':dominant,
      'focal_anchor':{'zone':focal,'bbox':dominant,'salience_rank':1},
      'focal_chain':['DOMINANT','SUPPORT','HEADER'],'eye_path':{'direction':direction,'waypoints':[focal,'SUPPORT','HEADER']},
      'salience_budget':{'rank_1':.55,'rank_2':.28,'rank_3':.17},
      'mass_plan':_mass_grid(dominant),
      'negative_space_zones':_negative_space(dominant,focal),
      'content_zones':_zones(strategy,dominant,focal),
      'typographic_hierarchy':{
        'font_family':'Montserrat Arabic' if direction=='RTL' else 'Montserrat',
        'levels':[{'role':'TITLE','px':46},{'role':'THESIS','px':30},{'role':'BODY','px':21},{'role':'SOURCE','px':13}],
        'numeral_system':'ARABIC_INDIC' if direction=='RTL' else 'EUROPEAN','latin_token_policy':'TECHNICAL_ISLANDS_ONLY','max_title_lines':2
      },
      'palette_role_map':{'canvas':'#FFFFFF','ink':'#1A1A1A','muted':'#6F6F73','accent_primary':'#A42365','accent_secondary':'#077381','surface':'#FAF9FA'},
      'material_plan':{'surface':'MATTE_EDITORIAL','corner_radius_px':18,'line_weight_px':2,'shadow':'NONE_OR_SUBTLE'},
      'contrast_pairs':[{'fg':'ink','bg':'canvas','target':4.5},{'fg':'ink','bg':'surface','target':4.5}],
      'imagery':_imagery(strategy,family,content_pack),
      'scene_metaphor':_scene(strategy,family,title,thesis),
      'topology':_topology(graph),
      'reference_grammar_ids':list(reference_grammar_ids or hypothesis.get('reference_grammar_ids') or [])[:4],
      'acceptance':{'dominant_mass_min':quality_floor('dominant_mass_min',.32),'dominant_mass_max':quality_floor('dominant_mass_max',.68),'min_pairwise_divergence':quality_floor('min_pairwise_structural_divergence_critical',.12),'target_pairwise_divergence':quality_floor('target_pairwise_structural_divergence',.18),'safe_margin_px':36,'min_type_levels':quality_floor('min_type_hierarchy_levels',3),'generic_card_fallback_forbidden':True},
      'source_hypothesis_id':hypothesis.get('id'),'visual_concept_id':hypothesis.get('visual_concept_id'),
      'content_digest':_h({'title':title,'thesis':thesis})[:16]
    }
    # Structural signature intentionally EXCLUDES content digest and page fingerprint.
    structural={k:spec[k] for k in ('page_family','communication_strategy','dominant_form','dominant_bbox','focal_anchor','mass_plan','negative_space_zones','imagery')}
    spec['structural_signature']='PCS-'+_h(structural)[:20].upper()
    spec['spec_sha256']=_h({k:v for k,v in spec.items() if k!='spec_sha256'})
    v=validate_page_composition_spec(spec)
    spec['validation']=v
    return spec

def _mass_grid(b):
    grid=[]
    for r in range(4):
        row=[]
        for c in range(4):
            cell=_bbox(c*.25,r*.25,.25,.25)
            ix=max(0,min(b['x']+b['w'],cell['x']+cell['w'])-max(b['x'],cell['x']))
            iy=max(0,min(b['y']+b['h'],cell['y']+cell['h'])-max(b['y'],cell['y']))
            row.append(round((ix*iy)/(.25*.25),3))
        grid.append(row)
    return grid

def _imagery(strategy,family,cp):
    requested=str(cp.get('imagery_mode') or '').upper()
    if requested in {'NONE','VECTOR_HYBRID','RASTER_AUGMENTED','GOLDEN_VISUAL_MASTER'}: mode=requested
    elif strategy=='IMAGE_LED' and family in {'COVER','SECTION_OPENER'}: mode='GOLDEN_VISUAL_MASTER'
    elif strategy=='IMAGE_LED': mode='RASTER_AUGMENTED'
    else: mode='VECTOR_HYBRID' if strategy in {'HYBRID_EXHIBIT','ARCHITECTURE_LED','SYSTEM_LED'} else 'NONE'
    return {'mode':mode,'asset_role':'PRIMARY_VISUAL' if mode!='NONE' else None,'mask_spec':'CROP_TO_DOMINANT_BBOX','forbidden_semantic_classes':['TEXT','LOGO','NUMERAL','OFFICIAL_SEAL'] if mode!='NONE' else [],'overlay_layers':['NATIVE_TEXT','VERIFIED_LOGOS'] if mode!='NONE' else []}

def _scene(strategy,family,title,thesis):
    if strategy!='IMAGE_LED': return {'concept':None,'sector_frame':None,'justification':'NOT_IMAGE_LED','literalism_guard':True}
    concept='institutional capability made tangible through an abstract operational scene'
    if family=='COVER': concept='premium institutional scene expressing the project theme with deliberate negative space for native title'
    return {'concept':concept,'sector_frame':(title or thesis)[:180],'justification':'image carries the idea while authoritative text remains native','literalism_guard':True}

def validate_page_composition_spec(spec):
    errors=[]
    if spec.get('schema')!='RASHAD_PAGE_COMPOSITION_SPEC_V1': errors.append('SCHEMA')
    if spec.get('dominant_form') not in FORMS: errors.append('DOMINANT_FORM')
    m=float(spec.get('dominant_mass_target',0) or 0)
    if not .32<=m<=.68: errors.append('DOMINANT_MASS_OUT_OF_BAND')
    b=spec.get('dominant_bbox') or {}
    if any(float(b.get(k,-1))<0 for k in ('x','y','w','h')) or b.get('x',0)+b.get('w',0)>1.001 or b.get('y',0)+b.get('h',0)>1.001: errors.append('DOMINANT_BBOX_INVALID')
    if len(spec.get('typographic_hierarchy',{}).get('levels',[]))<3: errors.append('TYPE_HIERARCHY_TOO_SHALLOW')
    if not spec.get('content_zones'): errors.append('CONTENT_ZONES_REQUIRED')
    if not spec.get('negative_space_zones'): errors.append('NEGATIVE_SPACE_REQUIRED')
    if spec.get('imagery',{}).get('mode')!='NONE' and not spec.get('imagery',{}).get('forbidden_semantic_classes'): errors.append('IMAGE_ISOLATION_POLICY_REQUIRED')
    return {'status':'PASS' if not errors else 'BLOCKED','errors':errors}
