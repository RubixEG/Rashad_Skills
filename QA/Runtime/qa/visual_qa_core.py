#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, math, hashlib, time
from pathlib import Path
from playwright.sync_api import sync_playwright

PASS='PASS'; FAIL='FAIL'; BLOCKED='BLOCKED'

COLLECT=r"""
(pageSel) => {
 const pages=[...document.querySelectorAll(pageSel)];
 const vis=(el,cs,r)=>cs.display!=='none'&&cs.visibility!=='hidden'&&parseFloat(cs.opacity||'1')>0&&r.width>0&&r.height>0;
 const R=r=>({x:r.x,y:r.y,w:r.width,h:r.height,r:r.right,b:r.bottom});
 const out=[];
 pages.forEach((page,pi)=>{
   const pr=page.getBoundingClientRect(); const rec={page:pi+1,rect:R(pr),els:[],texts:[],edges:[],images:[]}; let idx=0;
   page.querySelectorAll('*').forEach(el=>{
     const tag=el.tagName.toLowerCase(); if(['script','style','meta','link','title','br'].includes(tag)) return;
     const cs=getComputedStyle(el), r=el.getBoundingClientRect(); if(!vis(el,cs,r)) return;
     el.dataset.qaIdx=String(idx);
     let own=''; for(const n of el.childNodes) if(n.nodeType===3) own+=n.nodeValue; own=own.replace(/\s+/g,' ').trim();
     let lineRects=[]; if(own){ try{const rg=document.createRange(); rg.selectNodeContents(el); lineRects=[...rg.getClientRects()].map(R);}catch(e){} }
     const num=x=>{const v=parseFloat(x);return Number.isFinite(v)?v:0};
     const a={idx,tag,id:el.id||'',cls:[...el.classList],text:own,rect:R(r),lineRects,
       scroll:{w:el.scrollWidth,h:el.scrollHeight,cw:el.clientWidth,ch:el.clientHeight},
       css:{display:cs.display,position:cs.position,zIndex:cs.zIndex,direction:cs.direction,textAlign:cs.textAlign,fontFamily:cs.fontFamily,fontSize:num(cs.fontSize),lineHeight:cs.lineHeight,overflow:cs.overflow,overflowX:cs.overflowX,overflowY:cs.overflowY,background:cs.backgroundColor,color:cs.color,borderRadius:cs.borderRadius,transform:cs.transform,opacity:num(cs.opacity),clipPath:cs.clipPath,filter:cs.filter,objectFit:cs.objectFit,objectPosition:cs.objectPosition,boxSizing:cs.boxSizing,whiteSpace:cs.whiteSpace,wordBreak:cs.wordBreak,textOverflow:cs.textOverflow,padding:[num(cs.paddingTop),num(cs.paddingRight),num(cs.paddingBottom),num(cs.paddingLeft)],margin:[num(cs.marginTop),num(cs.marginRight),num(cs.marginBottom),num(cs.marginLeft)],gap:num(cs.gap),flexShrink:num(cs.flexShrink),flexGrow:num(cs.flexGrow),letterSpacing:num(cs.letterSpacing)},
       parent:el.parentElement?.dataset?.qaIdx??null,
       data:{pageMode:el.dataset.pageMode||'',pageFamily:el.dataset.pageFamily||'',region:el.dataset.regionId||'',node:el.dataset.nodeId||'',edge:el.dataset.edgeId||el.dataset.edge||'',source:el.dataset.source||'',target:el.dataset.target||'',directionality:el.dataset.directionality||'',label:el.dataset.labelId||'',labelFor:el.dataset.labelFor||'',owner:el.dataset.ownerId||'',anchor:el.dataset.anchor||'',layer:el.dataset.layerId||'',layerOrder:el.dataset.layerOrder||'',divider:el.dataset.dividerId||'',alignGroup:el.dataset.alignGroup||'',alignAxis:el.dataset.alignAxis||'',spacingGroup:el.dataset.spacingGroup||'',seqGroup:el.dataset.seqGroup||'',seq:el.dataset.seq||'',overlap:el.dataset.overlapPolicy||'',asset:el.dataset.assetId||'',headerRole:el.dataset.headerRole||'',tableRole:el.dataset.tableRole||'',artifactType:el.dataset.artifactType||''}}
     if(tag==='img'){a.image={naturalW:el.naturalWidth,naturalH:el.naturalHeight,src:el.currentSrc||el.src||''};rec.images.push(a)}
     rec.els.push(a); if(own)rec.texts.push(a); idx++;
   });
   page.querySelectorAll('[data-edge-id],[data-edge]').forEach(el=>{try{let p0=null,p1=null;if(el instanceof SVGGeometryElement&&el.getTotalLength){const len=el.getTotalLength(),a=el.getPointAtLength(0),b=el.getPointAtLength(len),m=el.getScreenCTM(),svg=el.ownerSVGElement,q0=svg.createSVGPoint(),q1=svg.createSVGPoint();q0.x=a.x;q0.y=a.y;q1.x=b.x;q1.y=b.y;const s0=q0.matrixTransform(m),s1=q1.matrixTransform(m);p0={x:s0.x,y:s0.y};p1={x:s1.x,y:s1.y};}const cs=getComputedStyle(el);let samples=[];let tangent=null;if(el instanceof SVGGeometryElement&&el.getTotalLength){const len=el.getTotalLength(),m=el.getScreenCTM(),svg=el.ownerSVGElement;for(let q=0;q<=len;q+=Math.max(2,len/80)){let a=el.getPointAtLength(Math.min(q,len)),pt=svg.createSVGPoint();pt.x=a.x;pt.y=a.y;let sp=pt.matrixTransform(m);samples.push({x:sp.x,y:sp.y});}if(len>1){let a=el.getPointAtLength(Math.max(0,len-2)),b=el.getPointAtLength(len),q0=svg.createSVGPoint(),q1=svg.createSVGPoint();q0.x=a.x;q0.y=a.y;q1.x=b.x;q1.y=b.y;let s0=q0.matrixTransform(m),s1=q1.matrixTransform(m);tangent={x:s1.x-s0.x,y:s1.y-s0.y};}}rec.edges.push({id:el.dataset.edgeId||el.dataset.edge||'',source:el.dataset.source||'',target:el.dataset.target||'',directionality:el.dataset.directionality||'',p0,p1,samples,tangent,markerStart:cs.markerStart||el.getAttribute('marker-start')||'',markerEnd:cs.markerEnd||el.getAttribute('marker-end')||'',rect:R(el.getBoundingClientRect())});}catch(e){rec.edges.push({id:el.dataset.edgeId||'',error:String(e)})}});
   out.push(rec);
 }); return out;
}
"""

def rect_inter(a,b):
 x=max(0,min(a['r'],b['r'])-max(a['x'],b['x'])); y=max(0,min(a['b'],b['b'])-max(a['y'],b['y'])); return x*y

def dist_rect(p,r):
 dx=max(r['x']-p['x'],0,p['x']-r['r']); dy=max(r['y']-p['y'],0,p['y']-r['b']); return math.hypot(dx,dy)

def gate(i,n,v,measured=None,required=True,test_count=None):
 tc=test_count if test_count is not None else (measured or {}).get('count',None)
 if required and tc==0 and not v: v=[{'kind':'FAIL_NOT_INSTRUMENTED','gate':i}]
 return {'id':i,'name':n,'status':FAIL if v else PASS,'required':required,'executed':True,'test_count':tc,'violations':v,'measured':measured or {}}

def parse_matrix(s):
 if not s or s=='none': return (1,1,0)
 m=re.match(r'matrix\(([-\d.e]+),[-\d.e]+,[-\d.e]+,([\-\d.e]+),[-\d.e]+,[-\d.e]+\)',s)
 if not m:return (1,1,0)
 try:return (float(m.group(1)),float(m.group(2)),0)
 except:return (1,1,0)

def is_card(e):
 try: rad=float(str(e['css']['borderRadius']).split('px')[0])
 except: rad=0
 bg=(e['css']['background'] or '').replace(' ','').lower()
 return rad>=12 and bg not in ('transparent','rgba(0,0,0,0)') and 80<=e['rect']['w']<=1000 and 45<=e['rect']['h']<=800

def required(spec,key,default=False): return bool(spec.get('required',{}).get(key,default))
def expected_count(spec,key): return spec.get('expected_counts',{}).get(key,None)

def inspect(pd,page,prof,spec):
 th=prof['thresholds']; pr=pd['rect']; els=pd['els']; texts=pd['texts']; bynode={e['data']['node']:e for e in els if e['data']['node']}; byidx={str(e['idx']):e for e in els}; gs=[]
 # G00 instrumentation
 v=[]
 classes={'headers':sum(bool(e['data']['headerRole']) for e in els),'nodes':len(bynode),'edges':len([e for e in pd['edges'] if e.get('id')]),'labels':sum(bool(e['data']['labelFor']) for e in els),'owners':sum(bool(e['data']['owner']) for e in els),'alignment_groups':len(set(e['data']['alignGroup'] for e in els if e['data']['alignGroup'])),'spacing_groups':len(set(e['data']['spacingGroup'] for e in els if e['data']['spacingGroup'])),'sequence_groups':len(set(e['data']['seqGroup'] for e in els if e['data']['seqGroup'])),'dividers':sum(bool(e['data']['divider']) or e['tag']=='hr' for e in els),'images':len(pd['images']),'tables':sum(bool(e['tag']=='table' or e['data']['tableRole']) for e in els)}
 for k,exp in spec.get('expected_counts',{}).items():
  if exp is not None and classes.get(k,0)<exp:v.append({'kind':'instrumentation_count_below_expected','class':k,'expected_min':exp,'actual':classes.get(k,0)})
 for k,on in spec.get('required',{}).items():
  if on and classes.get(k,0)==0:v.append({'kind':'FAIL_NOT_INSTRUMENTED','class':k})
 gs.append(gate('G00_INSTRUMENTATION','Required instrumentation',v,classes,required=True,test_count=sum(classes.values())))
 # canvas
 v=[]; c=prof['canvas'];
 if abs(pr['w']-c['width'])>1 or abs(pr['h']-c['height'])>1:v.append({'kind':'canvas_size','actual':[pr['w'],pr['h']],'expected':[c['width'],c['height']]})
 gs.append(gate('G01_CANVAS','Canvas',v,{'count':1},test_count=1))
 # header stack
 hdr=[e for e in els if e['data']['headerRole']]; v=[]; roles={e['data']['headerRole']:e for e in hdr}; order=['EYEBROW','TITLE','SUBTITLE','ACCENT','ARTIFACT_START']; prev=None
 for role in order:
  e=roles.get(role)
  if not e: continue
  if prev and e['rect']['y'] < prev['rect']['b'] + (th['header_artifact_gap_px'] if role=='ARTIFACT_START' else th['header_gap_px']):v.append({'kind':'header_stack_collision','a':prev['data']['headerRole'],'b':role,'gap':e['rect']['y']-prev['rect']['b']})
  prev=e
 gs.append(gate('G02_HEADER_STACK','Header stack / reflow',v,{'count':len(hdr)},required=required(spec,'headers',False),test_count=len(hdr)))
 # line fragments inter-element
 v=[]; frag=[]
 for e in texts:
  for j,r in enumerate(e.get('lineRects',[])): frag.append((e,j,r))
 # v2.6 FIX D1: an owner-anchored badge legitimately sits inside its owner's
 # text block. v2.5 flagged every such pair as a rendered-line collision.
 def _related(x,y,byi):
  if x['data'].get('owner') and x['data']['owner']==y['data'].get('node'): return True
  if y['data'].get('owner') and y['data']['owner']==x['data'].get('node'): return True
  for a_,b_ in ((x,y),(y,x)):
   cur=a_; hops=0
   while cur is not None and hops<24:
    pp=cur.get('parent')
    if pp is not None and str(pp)==str(b_['idx']): return True
    cur=byi.get(str(pp)) if pp is not None else None; hops+=1
  return False
 for i,(a,ja,ra) in enumerate(frag):
  for b,jb,rb in frag[i+1:]:
   if a['idx']==b['idx']: continue
   if _related(a,b,byidx): continue
   # ignore ancestors by containment
   inter=rect_inter(ra,rb)
   if inter>th['line_overlap_px2']:v.append({'kind':'rendered_line_collision','a':a['idx'],'b':b['idx'],'area':round(inter,1),'aText':a['text'][:60],'bText':b['text'][:60]})
 gs.append(gate('G03_LINE_COLLISION','Rendered line-fragment collision',v,{'count':len(frag)},required=True,test_count=len(frag)))
 # overflow + clipping/ellipsis
 v=[]
 for e in texts:
  s=e['scroll']; ov=(e['css']['overflow']+e['css']['overflowX']+e['css']['overflowY']).lower(); dx=s['w']-s['cw'];dy=s['h']-s['ch']
  if (dx>th['overflow_px'] or dy>th['overflow_px']) and any(x in ov for x in ['hidden','clip','scroll','auto']):v.append({'kind':'text_overflow','idx':e['idx'],'dx':dx,'dy':dy,'text':e['text'][:80]})
  if e['css']['textOverflow']=='ellipsis':v.append({'kind':'ellipsis_not_allowed_in_production','idx':e['idx'],'text':e['text'][:80]})
 gs.append(gate('G04_TEXT_FIT','Text overflow / clipping / ellipsis',v,{'count':len(texts)},test_count=len(texts)))
 # containment + safe area / corners: every visible element >=16 px2 is measured.
 v=[]; safe=float(prof.get('canvas',{}).get('safe_margin',36)); tested_cont=0
 for e in els:
  r=e['rect']; area=r['w']*r['h']
  if area<float(th.get('safe_area_min_visible_px2',16)): continue
  tested_cont+=1; cls=' '.join(e.get('cls',[])).lower(); intentional=('bleed' in cls or e['data'].get('region') in ('BACKGROUND','FULL_BLEED'))
  if r['x']<pr['x']-1 or r['r']>pr['r']+1 or r['y']<pr['y']-1 or r['b']>pr['b']+1: v.append({'kind':'off_canvas','idx':e['idx'],'rect':r})
  if not intentional and (r['x']<pr['x']+safe or r['r']>pr['r']-safe or r['y']<pr['y']+safe or r['b']>pr['b']-safe):
   # backgrounds/large dominant regions are exempt; text and ordinary objects are not.
   if area < pr['w']*pr['h']*.30 and e['data'].get('region')!='DOMINANT': v.append({'kind':'safe_area_violation','idx':e['idx'],'rect':r,'safe_margin':safe})
  if e.get('text'):
   corners=[(pr['x'],pr['y']),(pr['r'],pr['y']),(pr['x'],pr['b']),(pr['r'],pr['b'])]; rad=1.5*safe
   cx=r['x']+r['w']/2;cy=r['y']+r['h']/2
   if any(math.hypot(cx-x,cy-y)<rad for x,y in corners): v.append({'kind':'corner_keepout_violation','idx':e['idx']})
 gs.append(gate('G05_CONTAINMENT','Canvas containment + safe area',v,{'count':tested_cont},test_count=tested_cont))
 # semantic collisions structural + text owner
 v=[]; structs=[e for e in els if e['data']['node'] or e['data']['label'] or e['data']['owner'] or e['data']['headerRole'] or e['data']['divider'] or any(c in e['cls'] for c in ['box','card','panel','q','co','foot'])]
 def _ancestor_related(a,b):
  # Only real DOM containment or explicit overlap intent may exempt an overlap.
  # Producer-authored owner/label metadata and >92% containment are not collision escape hatches.
  for x,y in ((a,b),(b,a)):
   cur=x; hops=0
   while cur is not None and hops<32:
    pp=cur.get('parent')
    if pp is not None and str(pp)==str(y['idx']): return True
    cur=byidx.get(str(pp)) if pp is not None else None; hops+=1
  return False
 for i,a in enumerate(structs):
  for b in structs[i+1:]:
   if a['data'].get('overlap')=='ALLOW' or b['data'].get('overlap')=='ALLOW':continue
   if _ancestor_related(a,b): continue
   inter=rect_inter(a['rect'],b['rect'])
   if inter<=th['overlap_area_px']:continue
   v.append({'kind':'structural_collision','a':a['idx'],'b':b['idx'],'area':round(inter,1)})
 gs.append(gate('G06_COLLISION','Structural collision',v,{'count':len(structs)},test_count=len(structs)))
 # z-index / occlusion hit tests
 v=[]
 for e in texts:
  r=e['rect']; pts=[(r['x']+r['w']/2,r['y']+r['h']/2),(r['x']+3,r['y']+r['h']/2),(r['r']-3,r['y']+r['h']/2)]
  for x,y in pts:
   hit=page.evaluate("([x,y])=>{const h=document.elementFromPoint(x,y);return h?{idx:h.dataset.qaIdx||'',tag:h.tagName,txt:(h.innerText||'').slice(0,40)}:null}",[x,y])
   if hit and str(hit.get('idx','')) not in ('',str(e['idx'])) and hit.get('tag','').lower() not in ('svg','path'):
    # allow ancestor hits
    cur=e;anc=set()
    while cur and cur.get('parent') is not None:
     anc.add(str(cur['parent']));cur=byidx.get(str(cur['parent']))
    # v2.6 FIX D2: also allow DESCENDANT hits — a parent's own text being
    # "occluded" by its own child span is not an occlusion defect.
    hid=str(hit.get('idx',''));h=byidx.get(hid);desc=False;hops=0
    while h is not None and hops<24:
     pp=h.get('parent')
     if pp is not None and str(pp)==str(e['idx']):desc=True;break
     h=byidx.get(str(pp)) if pp is not None else None;hops+=1
    if hid not in anc and not desc:v.append({'kind':'text_occluded','idx':e['idx'],'hit':hit});break
 gs.append(gate('G07_OCCLUSION','Z-index / occlusion',v,{'count':len(texts)},test_count=len(texts)))
 # alignment
 groups={};v=[]
 for e in els:
  if e['data']['alignGroup']:groups.setdefault(e['data']['alignGroup'],[]).append(e)
 if not groups:
  # infer horizontal peer groups geometrically instead of rewarding missing instrumentation
  cand=[e for e in els if (e['data']['node'] or is_card(e)) and e['rect']['w']>40 and e['rect']['h']>30]
  for e in cand:
   key='AUTOY-'+str(round((e['rect']['y']+e['rect']['h']/2)/20)); groups.setdefault(key,[]).append(e)
 for g,arr in groups.items():
  if len(arr)<2:continue
  axis=arr[0]['data']['alignAxis'] or 'CENTER_Y';vals=[]
  for e in arr:
   r=e['rect'];vals.append({'X':r['x'],'Y':r['y'],'CENTER_X':r['x']+r['w']/2,'CENTER_Y':r['y']+r['h']/2,'RIGHT':r['r'],'BOTTOM':r['b']}.get(axis,r['y']))
  if max(vals)-min(vals)>th['align_px']:v.append({'kind':'alignment_drift','group':g,'spread':round(max(vals)-min(vals),1),'axis':axis})
 gs.append(gate('G08_ALIGNMENT','Alignment groups',v,{'count':len(groups)},required=bool(groups),test_count=len(groups)))
 # spacing
 groups={};v=[]
 for e in els:
  if e['data']['spacingGroup']:groups.setdefault(e['data']['spacingGroup'],[]).append(e)
 if not groups:
  cand=[e for e in els if (e['data']['node'] or is_card(e)) and e['rect']['w']>40 and e['rect']['h']>30]
  for e in cand:
   key='AUTOY-'+str(round((e['rect']['y']+e['rect']['h']/2)/20)); groups.setdefault(key,[]).append(e)
 for g,arr in groups.items():
  axis=arr[0]['data']['alignAxis'] or 'X';arr=sorted(arr,key=lambda e:e['rect']['y'] if axis=='Y' else e['rect']['x']);gaps=[]
  for i in range(len(arr)-1):gaps.append((arr[i+1]['rect']['y']-arr[i]['rect']['b']) if axis=='Y' else (arr[i+1]['rect']['x']-arr[i]['rect']['r']))
  if any(x<0 for x in gaps) or (len(gaps)>1 and max(gaps)-min(gaps)>th['spacing_variance_px']):v.append({'kind':'spacing_drift','group':g,'gaps':[round(x,1) for x in gaps]})
 gs.append(gate('G09_SPACING','Spacing rhythm',v,{'count':len(groups)},required=bool(groups),test_count=len(groups)))
 # padding / scale
 v=[]; tested=0
 for e in els:
  if e['data']['node'] or e['data']['owner'] or any(c in e['cls'] for c in ['card','box','panel']):
   tested+=1; pads=e['css']['padding']
   if any(p<0 for p in pads):v.append({'kind':'negative_padding','idx':e['idx'],'padding':pads})
   if e['text'] and min(pads)<th['padding_min_px'] and e['rect']['w']>80 and e['rect']['h']>40:v.append({'kind':'padding_too_small','idx':e['idx'],'padding':pads})
   if e['text'] and max(pads)>th['padding_max_px'] and e['rect']['w']>80 and e['rect']['h']>40:v.append({'kind':'padding_too_large','idx':e['idx'],'padding':pads,'ceiling':th['padding_max_px']})
   tr=e['css']['transform']
   if tr!='none':
    nums=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',tr)]
    if nums and (min(nums[:4])<0 or max(abs(x) for x in nums[:4])>th['max_transform_scale_ratio']):v.append({'kind':'unexpected_transform_scale_or_mirror','idx':e['idx'],'transform':tr})
    if len(nums)>=4:
     # CSS matrix(a,b,c,d,tx,ty): rotation = atan2(b,a). Translation is irrelevant.
     import math as _math
     rot=abs(_math.degrees(_math.atan2(nums[1],nums[0])))
     rot=min(rot,abs(180-rot))
     if rot>th['max_rotation_deg']:v.append({'kind':'unexpected_rotation','idx':e['idx'],'rotation_deg':round(rot,2),'ceiling':th['max_rotation_deg']})
 gs.append(gate('G10_PADDING_SCALE','Padding / scale',v,{'count':tested},required=bool(tested),test_count=tested))
 # owner/anchor
 v=[]; owners=[e for e in els if e['data']['owner']]
 anchors={'TOP_CENTER':lambda r:{'x':r['x']+r['w']/2,'y':r['y']},'CENTER':lambda r:{'x':r['x']+r['w']/2,'y':r['y']+r['h']/2},'TOP_RIGHT':lambda r:{'x':r['r'],'y':r['y']},'TOP_LEFT':lambda r:{'x':r['x'],'y':r['y']},'BOTTOM_CENTER':lambda r:{'x':r['x']+r['w']/2,'y':r['b']}}
 for e in owners:
  o=bynode.get(e['data']['owner'])
  if not o:v.append({'kind':'owner_missing','idx':e['idx'],'owner':e['data']['owner']});continue
  c={'x':e['rect']['x']+e['rect']['w']/2,'y':e['rect']['y']+e['rect']['h']/2};an=e['data']['anchor'] or 'CENTER';target=anchors.get(an,anchors['CENTER'])(o['rect']);d=math.hypot(c['x']-target['x'],c['y']-target['y'])
  allowed=max(o['rect']['w'],o['rect']['h'])*.65+th['owner_anchor_tolerance_px']
  if d>allowed:v.append({'kind':'owner_anchor_drift','idx':e['idx'],'owner':e['data']['owner'],'anchor':an,'distance':round(d,1),'allowed':round(allowed,1)})
 gs.append(gate('G11_OWNER_ANCHOR','Owner/anchor containment',v,{'count':len(owners)},required=required(spec,'owners',False),test_count=len(owners)))
 # dividers
 v=[]; divs=[e for e in els if e['data']['divider'] or e['tag']=='hr']
 for e in divs:
  r=e['rect'];thin=min(r['w'],r['h']);long=max(r['w'],r['h'])
  if thin>6 or long<40:v.append({'kind':'bad_divider_geometry','idx':e['idx'],'rect':r})
 gs.append(gate('G12_DIVIDERS','Dividers',v,{'count':len(divs)},required=required(spec,'dividers',False),test_count=len(divs)))
 # fonts/glyph
 v=[];allowed=[x.lower() for x in prof['allowed_fonts']]
 for e in texts:
  fam=e['css']['fontFamily'].lower();fs=e['css']['fontSize'];txt=e['text']
  if not any(a in fam for a in allowed):v.append({'kind':'unexpected_font','idx':e['idx'],'family':e['css']['fontFamily']})
  cls=' '.join(e['cls']).lower(); is_title=e.get('tag') in ('h1','h2') or 'title' in cls or (e.get('data',{}).get('headerRole') or '').upper()=='TITLE'
  minfs=th['min_source_font_px'] if 'source' in cls else (th['min_title_font_px'] if is_title else th['min_body_font_px'])
  if fs and fs<minfs:v.append({'kind':'font_too_small','idx':e['idx'],'size':fs,'floor':minfs,'text':txt[:60]})
  if is_title and fs and fs>th['max_title_font_px']:v.append({'kind':'title_font_too_large','idx':e['idx'],'size':fs,'ceiling':th['max_title_font_px'],'text':txt[:60]})
  if '\ufffd' in txt or '□□' in txt or '�' in txt:v.append({'kind':'tofu_or_replacement','idx':e['idx'],'text':txt[:80]})
  ok=page.evaluate("([sz,fam,txt])=>document.fonts.check(`${sz}px ${fam}`,txt)",[max(fs,12),e['css']['fontFamily'].split(',')[0],txt[:200]])
  if not ok:v.append({'kind':'font_not_ready','idx':e['idx'],'family':e['css']['fontFamily']})
 gs.append(gate('G13_TYPOGRAPHY','Font / glyph / readability',v,{'count':len(texts)},test_count=len(texts)))
 # rtl sequence
 seq={};v=[]
 for e in els:
  if e['data']['seqGroup'] and e['data']['seq']!='':
   try:n=float(e['data']['seq'])
   except:continue
   seq.setdefault(e['data']['seqGroup'],[]).append((n,e))
 for g,arr in seq.items():
  arr=sorted(arr,key=lambda t:t[0]); xs=[e['rect']['x'] for _,e in arr]; rtl=arr[0][1]['css']['direction']=='rtl'
  if rtl and any(xs[i]<=xs[i+1] for i in range(len(xs)-1)):v.append({'kind':'rtl_sequence_wrong','group':g,'xs':xs})
  if not rtl and any(xs[i]>=xs[i+1] for i in range(len(xs)-1)):v.append({'kind':'ltr_sequence_wrong','group':g,'xs':xs})
 gs.append(gate('G14_RTL_BIDI','Legacy physical sequence direction (BiDi run truth is owned by G27)',v,{'count':len(seq)},required=required(spec,'sequence_groups',False),test_count=len(seq)))
 # topology inventory
 expn=spec.get('expected_nodes',[]);expe=spec.get('expected_edges',[]);domn=set(bynode);dome=set(e.get('id') for e in pd['edges'] if e.get('id'));v=[]
 for n in expn:
  if n not in domn:v.append({'kind':'missing_node','id':n})
 for e in expe:
  eid=e['id'] if isinstance(e,dict) else e
  if eid not in dome:v.append({'kind':'missing_edge','id':eid})
 if spec.get('artifact_expected') and not domn:v.append({'kind':'artifact_expected_but_no_nodes'})
 gs.append(gate('G15_TOPOLOGY','Topology inventory truth',v,{'count':len(domn)+len(dome),'nodes':len(domn),'edges':len(dome)},required=bool(spec.get('artifact_expected')),test_count=len(domn)+len(dome)))
 # connectors
 v=[]
 for ed in pd['edges']:
  src=bynode.get(ed.get('source'));tgt=bynode.get(ed.get('target'))
  if not src or not tgt:v.append({'kind':'missing_endpoint_node','edge':ed.get('id')});continue
  if not ed.get('p0') or not ed.get('p1'):v.append({'kind':'no_rendered_endpoints','edge':ed.get('id')});continue
  d0=dist_rect(ed['p0'],src['rect']);d1=dist_rect(ed['p1'],tgt['rect'])
  if d0>th['connector_attach_px']:v.append({'kind':'source_detached','edge':ed['id'],'distance':round(d0,1)})
  if d1>th['connector_attach_px']:v.append({'kind':'target_detached','edge':ed['id'],'distance':round(d1,1)})
  if ed.get('directionality','').upper()=='DIRECTED' and not ed.get('markerEnd'):v.append({'kind':'missing_arrowhead','edge':ed['id']})
 gs.append(gate('G16_CONNECTORS','Connector geometry',v,{'count':len(pd['edges'])},required=bool(pd['edges'] or spec.get('expected_edges') or required(spec,'edges',False)),test_count=len(pd['edges'])))
 # labels
 v=[];labs=[e for e in els if e['data']['labelFor']]
 for e in labs:
  t=bynode.get(e['data']['labelFor'])
  if not t:v.append({'kind':'orphan_label','idx':e['idx'],'for':e['data']['labelFor']});continue
  c={'x':e['rect']['x']+e['rect']['w']/2,'y':e['rect']['y']+e['rect']['h']/2};d=dist_rect(c,t['rect'])
  if d>th['label_attach_px']:v.append({'kind':'detached_label','idx':e['idx'],'distance':round(d,1)})
 gs.append(gate('G17_LABELS','Label ownership/attachment',v,{'count':len(labs)},required=bool(labs or required(spec,'labels',False)),test_count=len(labs)))
 # card dominance truth
 cards=[e for e in els if is_card(e)];pagearea=pr['w']*pr['h'];ratio=sum(e['rect']['w']*e['rect']['h'] for e in cards)/pagearea if pagearea else 0;sizes=[(round(e['rect']['w']/20)*20,round(e['rect']['h']/20)*20) for e in cards];common=max((sizes.count(x) for x in set(sizes)),default=0);mode=(spec.get('page_mode') or '').upper();art=(spec.get('artifact_family') or '').upper();higher=False
 if art in ('SYSTEM','NETWORK','PROCESS','ARCHITECTURE'):higher=len(domn)>=3 and len(dome)>=2
 elif art in ('TIMELINE','JOURNEY','ROADMAP'):higher=len(seq)>=1 and (len(dome)>=1 or sum(len(vv) for vv in seq.values())>=3)
 elif art in ('MATRIX','TABLE'):higher=classes['tables']>=1
 else:higher=len(dome)>=2 or classes['tables']>=1
 v=[]
 analytical=mode in ('ARTIFACT_LED','HYBRID','ANALYTICAL') or len(cards)>=4 or len(texts)>=8
 areas=[e['rect']['w']*e['rect']['h'] for e in cards]
 def _gini(vs):
  vs=sorted(max(0,float(x)) for x in vs); n=len(vs)
  return 0 if not vs or sum(vs)==0 else sum((2*i-n-1)*x for i,x in enumerate(vs,1))/(n*sum(vs))
 gini=_gini(areas)
 # a table or a couple of fake edges no longer exempts an equal-card grid.
 if analytical and (ratio>th['card_dominance_ratio'] or common>=4 or (len(cards)>=4 and gini<.15)):
  typed_edges=sum(bool(e.get('source') and e.get('target') and e.get('id')) for e in pd['edges'])
  genuine_higher=higher and (typed_edges>=max(1,len(pd['edges'])) or classes['tables']>=1)
  if not genuine_higher or (len(cards)>=4 and gini<.15): v.append({'kind':'card_dominance_or_spoof','cards':len(cards),'ratio':round(ratio,3),'similar':common,'gini':round(gini,3),'artifact_family':art})
 gs.append(gate('G18_CARD_TRUTH','Card dominance / topology truth',v,{'count':len(cards),'ratio':round(ratio,3),'higherOrder':higher,'gini':round(gini,3)},required=analytical,test_count=1))
 # transforms clip opacity
 v=[];tested=0
 for e in els:
  if e['data']['node'] or e['data']['asset'] or e['tag']=='img':
   tested+=1;tr=e['css']['transform'];clip=e['css']['clipPath'];op=e['css']['opacity']
   if clip not in ('none','auto') and not spec.get('allow_clip_path'):v.append({'kind':'unexpected_clip_path','idx':e['idx'],'clip':clip})
   if op<.97 and not spec.get('allow_opacity'):v.append({'kind':'unexpected_opacity','idx':e['idx'],'opacity':op})
   if tr!='none' and not spec.get('allow_transforms'):v.append({'kind':'unexpected_transform','idx':e['idx'],'transform':tr})
 gs.append(gate('G19_TRANSFORM_LAYER','Transform / clip / opacity integrity',v,{'count':tested},test_count=tested))
 # images/assets
 v=[]
 for e in pd['images']:
  im=e.get('image',{});nw=im.get('naturalW',0);nh=im.get('naturalH',0);r=e['rect']
  if nw<=0 or nh<=0:v.append({'kind':'image_not_loaded','idx':e['idx']});continue
  nat=nw/nh;ren=r['w']/r['h'] if r['h'] else 0
  if e['css']['objectFit'] in ('fill','') and abs(nat-ren)/max(nat,.001)>.025:v.append({'kind':'image_aspect_distortion','idx':e['idx'],'natural':nat,'rendered':ren})
 gs.append(gate('G20_ASSETS','Image / asset geometry',v,{'count':len(pd['images'])},required=required(spec,'images',False),test_count=len(pd['images'])))
 # tables / dense evidence
 tables=[e for e in els if e['tag']=='table'];v=[]
 for t in tables:
  if t['scroll']['w']-t['scroll']['cw']>th['overflow_px'] or t['scroll']['h']-t['scroll']['ch']>th['overflow_px']:v.append({'kind':'table_overflow','idx':t['idx']})
 gs.append(gate('G21_DENSE_EVIDENCE','Tables / dense evidence',v,{'count':len(tables)},required=required(spec,'tables',False),test_count=len(tables)))
 # debug leakage
 v=[];full=' '.join(e['text'] for e in texts)
 for term in prof.get('debug_terms',[]):
  if term.lower() in full.lower():v.append({'kind':'debug_leak','term':term})
 gs.append(gate('G22_DEBUG','Internal metadata leakage',v,{'count':1},test_count=1))
 # harmony
 ink=[e for e in els if (e['text'] or e['data']['node'] or e['tag']=='img') and e['rect']['w']*e['rect']['h']>60];left=sum(e['rect']['w']*e['rect']['h'] for e in ink if e['rect']['x']+e['rect']['w']/2<pr['x']+pr['w']/2);right=sum(e['rect']['w']*e['rect']['h'] for e in ink if e['rect']['x']+e['rect']['w']/2>=pr['x']+pr['w']/2);total=left+right or 1;v=[]
 if (spec.get('page_family') or '').upper() not in ('COVER','ASYMMETRIC_COVER') and max(left,right)/total>th['balance_extreme_ratio']:v.append({'kind':'extreme_visual_mass_imbalance','leftShare':round(left/total,3),'rightShare':round(right/total,3)})
 gs.append(gate('G23_HARMONY','Whole-page harmony proxy',v,{'count':len(ink),'leftShare':round(left/total,3),'rightShare':round(right/total,3)},test_count=len(ink)))
 return gs

def mutate(page,pageSel,kind,factor=None):
 if kind=='font':page.evaluate("([s,f])=>document.querySelectorAll(s+' *').forEach(e=>{const c=getComputedStyle(e);if(e.innerText&&parseFloat(c.fontSize)>0)e.style.fontSize=(parseFloat(c.fontSize)*f)+'px'})",[pageSel,factor])
 elif kind=='line':page.evaluate("([s,f])=>document.querySelectorAll(s+' *').forEach(e=>{const c=getComputedStyle(e);if(e.innerText&&c.lineHeight!=='normal')e.style.lineHeight=(parseFloat(c.lineHeight)*f)+'px'})",[pageSel,factor])
 elif kind=='textgrow':page.evaluate("([s,f])=>document.querySelectorAll(s+' [data-stress-grow],'+s+' .stress-grow').forEach(e=>{e.textContent=(e.textContent+' ').repeat(f).trim()})",[pageSel,int(factor)])

def main():
 ap=argparse.ArgumentParser();ap.add_argument('html');ap.add_argument('--profile',default=str(Path(__file__).parent/'config/profile.json'));ap.add_argument('--spec');ap.add_argument('--out',default='evidence');ap.add_argument('--page-selector',default='.page');ap.add_argument('--stress',action='store_true');ap.add_argument('--repeat',type=int,default=3);a=ap.parse_args()
 hp=Path(a.html).resolve();prof=json.loads(Path(a.profile).read_text());spec=json.loads(Path(a.spec).read_text()) if a.spec else {};out=Path(a.out);out.mkdir(parents=True,exist_ok=True);html=hp.read_text(encoding='utf-8');base=f'<base href="file://{hp.parent.as_posix()}/">';html=html.replace('<head>','<head>'+base,1) if '<head>' in html else base+html
 rep={'file':str(hp),'status':BLOCKED,'pages':[],'stress':[],'repeat':{},'runtime':{}}
 try:
  with sync_playwright() as p:
   b=p.chromium.launch(headless=True,executable_path=(__import__('os').environ.get('RASHAD_CHROMIUM') or '/opt/pw-browsers/chromium'),args=['--no-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files']);page=b.new_page(viewport={'width':1920,'height':1080});page.set_content(html,wait_until='load');page.evaluate('()=>document.fonts.ready');time.sleep(.1);cnt=page.locator(a.page_selector).count();
   if 1<cnt<=10:page.set_viewport_size({'width':1920,'height':1080*cnt})
   data=page.evaluate(COLLECT,a.page_selector);specs=spec.get('pages',{}) if isinstance(spec,dict) else {};allpass=True
   for pd in data:
    ps=specs.get(str(pd['page']),spec);g=inspect(pd,page,prof,ps);status=PASS if all(x['status']==PASS for x in g if x['required']) else FAIL;allpass &= status==PASS;rep['pages'].append({'page':pd['page'],'status':status,'gates':g})
   if a.stress:
    modes=[('font',x) for x in prof['thresholds']['stress_font_scales']]+[('line',x) for x in prof['thresholds']['stress_line_height_scales']]+[('textgrow',2)]
    for kind,f in modes:
     page.set_content(html,wait_until='load');page.evaluate('()=>document.fonts.ready');mutate(page,a.page_selector,kind,f);page.evaluate('()=>document.fonts.ready');time.sleep(.05);dd=page.evaluate(COLLECT,a.page_selector);viol=[]
     for pd in dd:
      ps=specs.get(str(pd['page']),spec);gg=inspect(pd,page,prof,ps)
      for x in gg:
       if x['required'] and x['status']==FAIL:viol.append({'page':pd['page'],'gate':x['id'],'count':len(x['violations'])})
     rep['stress'].append({'mode':f'{kind.upper()}_{f}','status':PASS if not viol else FAIL,'violations':viol});allpass &= not viol
   fps=[]
   for _ in range(max(1,a.repeat)):
    page.set_content(html,wait_until='load');page.evaluate('()=>document.fonts.ready');time.sleep(.05);d=page.evaluate(COLLECT,a.page_selector);geom=json.dumps([[(round(e['rect']['x'],1),round(e['rect']['y'],1),round(e['rect']['w'],1),round(e['rect']['h'],1)) for e in q['els']] for q in d]).encode();fps.append(hashlib.sha256(geom).hexdigest())
   stable=len(set(fps))==1;rep['repeat']={'runs':len(fps),'stable':stable,'fingerprints':fps};allpass &= stable;rep['status']='HTML_PREEXPORT_PASS' if allpass else BLOCKED;b.close()
 except Exception as e:rep['runtime']={'error':repr(e)};rep['status']=BLOCKED
 op=out/(hp.stem+'.visual_qa_v25.json');op.write_text(json.dumps(rep,ensure_ascii=False,indent=2));print(op);print(rep['status']);raise SystemExit(0 if rep['status']=='HTML_PREEXPORT_PASS' else 1)
if __name__=='__main__':main()
