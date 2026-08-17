from __future__ import annotations
from pathlib import Path
import html,json,hashlib,base64,mimetypes,re


def _px_bbox(b,w=1920,h=1080): return [round(b['x']*w),round(b['y']*h),round(b['w']*w),round(b['h']*h)]
_ARABIC_INDIC_TRANS = str.maketrans('0123456789','٠١٢٣٤٥٦٧٨٩')

def _visible_text(x, *, arabic=False):
    text=str(x or '')
    # Natural-language Arabic fields obey the page numeral policy. Technical/source
    # identifiers are rendered separately as isolated LTR islands and are not passed here.
    if arabic:
        text=text.translate(_ARABIC_INDIC_TRANS)
    return text

def _esc(x, *, arabic=False): return html.escape(_visible_text(x, arabic=arabic))

def _rich_visible(x, *, arabic=False):
    text=_visible_text(x,arabic=arabic)
    if not arabic:
        return html.escape(text)
    # Keep Arabic-Indic numeric islands physically stable inside RTL natural text.
    # The containing text block now has element children, which lets the BiDi QA
    # distinguish an intentional isolated run from browser-created split runs.
    parts=[]; pos=0
    for m in re.finditer(r'[٠-٩]+(?:[./٪%\-–—][٠-٩]+)*',text):
        parts.append(html.escape(text[pos:m.start()]))
        parts.append(f'<bdi class="ltr-island" dir="ltr" data-directionality="ISOLATED">{html.escape(m.group(0))}</bdi>')
        pos=m.end()
    parts.append(html.escape(text[pos:]))
    return ''.join(parts)
def _asset_uri(path):
    p=Path(path); mime=mimetypes.guess_type(p.name)[0] or 'application/octet-stream'; return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"

def compose_html(spec,content_pack,semantic_graph,out_path,image_asset=None,brand_logo=None,client_logo=None):
    """Build an instrumented semantic HTML master. Authoritative text remains native HTML.
    Connectors are resolved after document.fonts.ready from measured DOM boxes.
    """
    out=Path(out_path); out.parent.mkdir(parents=True,exist_ok=True)
    pal=spec['palette_role_map']; font=spec['typographic_hierarchy']['font_family']; lang='ar' if spec['eye_path']['direction']=='RTL' else 'en'; direction='rtl' if lang=='ar' else 'ltr'; arvis=(lang=='ar' and spec.get('typographic_hierarchy',{}).get('numeral_system')=='ARABIC_INDIC')
    title=_rich_visible(content_pack.get('title') or content_pack.get('management_question') or '', arabic=arvis)
    thesis=_rich_visible(content_pack.get('thesis') or content_pack.get('answer_first_thesis') or content_pack.get('answer') or '', arabic=arvis)
    proofs=content_pack.get('proof_points') or content_pack.get('evidence_points') or content_pack.get('bullets') or []
    if not isinstance(proofs,list): proofs=[str(proofs)]
    proofs=[_rich_visible(x.get('text') if isinstance(x,dict) else x, arabic=arvis) for x in proofs[:6]]
    if not proofs and content_pack.get('executive_implication'): proofs=[_rich_visible(content_pack.get('executive_implication'), arabic=arvis)]
    source_id=str(content_pack.get('source_id') or content_pack.get('evidence_id') or content_pack.get('source_note') or '').strip()
    if not source_id or len(source_id)>96: source_id='EVIDENCE-BOUND'
    implication=_rich_visible(content_pack.get('executive_implication') or content_pack.get('implication') or '', arabic=arvis) if (content_pack.get('executive_implication') or content_pack.get('implication')) else (proofs[-1] if proofs else thesis)
    db=_px_bbox(spec['dominant_bbox']); zones={z['id']:_px_bbox(z['bbox']) for z in spec['content_zones']}
    strategy=spec['communication_strategy']; form=spec['dominant_form']; topo=spec.get('topology') or {}; nodes=topo.get('nodes') or []
    relation_labels_ar={'ENABLES':'يمكّن','DEPENDS_ON':'يعتمد على','FLOWS_TO':'ينتقل إلى','CONTROLS':'يضبط','MEASURES':'يقيس','EVIDENCES':'يثبت','RISKS':'يهدد','PRIORITIZES':'يرتّب','OWNS':'يملك','APPROVES':'يعتمد','FEEDS_BACK':'يغذّي التحسين','THRESHOLD_FOR':'شرط لـ','MAPS_TO':'يرتبط بـ','BLOCKS':'يمنع'}
    relation_labels_en={'ENABLES':'enables','DEPENDS_ON':'depends on','FLOWS_TO':'flows to','CONTROLS':'controls','MEASURES':'measures','EVIDENCES':'evidences','RISKS':'risks','PRIORITIZES':'prioritizes','OWNS':'owns','APPROVES':'approves','FEEDS_BACK':'feeds back','THRESHOLD_FOR':'threshold for','MAPS_TO':'maps to','BLOCKS':'blocks'}
    edge_labels=relation_labels_ar if arvis else relation_labels_en
    # If graph is thin, create page-specific support nodes from proof points; labels remain content-derived.
    if not nodes:
        nodes=[{'id':f'N{i+1}','label':p,'type':'PROOF'} for i,p in enumerate(proofs[:5])]
    node_html=''.join(f'<div class="node node-rank-{i+1}" data-node-id="{_esc(n["id"])}" data-node-type="{_esc(n.get("type","CLAIM"))}" data-content-slot="evidence">{_rich_visible(n.get("label",n["id"]), arabic=arvis)}</div>' for i,n in enumerate(nodes[:8]))
    img=''
    if image_asset:
        img=f'<img class="hero-plate" data-asset-id="PRIMARY_VISUAL" src="{html.escape(_asset_uri(image_asset))}" alt="" />'
    logo=''
    if brand_logo:
        logo=f'<img class="brand-logo" data-asset-id="RUBIX" src="{html.escape(_asset_uri(brand_logo))}" alt="Rubix" />'
    client=''
    if client_logo:
        client=f'<img class="client-logo" data-asset-id="CLIENT" src="{html.escape(_asset_uri(client_logo))}" alt="Client" />'
    support=''.join(f'<li data-content-slot="evidence" data-source="{_esc(source_id)}">{p}</li>' for p in proofs)
    # native visual structures vary by dominant form; the overall mass/focal plan comes from the spec.
    structure=f'<div class="dominant-inner form-{form.lower()}" data-artifact-type="{_esc(strategy)}">{node_html}</div>'
    if form=='CHART':
        vals=content_pack.get('chart_values') or [72,54,38,83]; structure='<div class="chart" data-artifact-type="CHART_LED">'+''.join(f'<div class="bar" style="height:{max(8,min(100,float(v)))}%"><span>{_esc(v)}</span></div>' for v in vals[:6])+'</div>'
    elif form=='TABLE':
        structure='<table data-table-role="EVIDENCE"><tbody>'+''.join(f'<tr><td>{i+1}</td><td>{p}</td></tr>' for i,p in enumerate(proofs or ['—']))+'</tbody></table>'
    elif form=='HERO_IMAGE': structure=img or '<div class="image-pending">HOST-NATIVE IMAGE PLATE REQUIRED</div>'
    elif form=='STATEMENT_BLOCK': structure=f'<div class="hero-statement">{thesis or title}</div><div class="proof-strip">{support}</div>'
    html_txt=f'''<!doctype html><html lang="{lang}" dir="{direction}"><head><meta charset="utf-8"><style>
    *{{box-sizing:border-box}} html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:{pal['canvas']};font-family:"{font}",sans-serif;color:{pal['ink']}}}
    .page{{position:relative;width:1920px;height:1080px;overflow:hidden;background:{pal['canvas']};direction:{direction}}}
    .header{{position:absolute;left:{zones['HEADER'][0]}px;top:{zones['HEADER'][1]}px;width:{zones['HEADER'][2]}px;height:{zones['HEADER'][3]}px;z-index:30}}
    .eyebrow{{font-size:16px;color:{pal['accent_primary']};font-weight:700}} h1{{font-size:48px;line-height:1.08;margin:6px 0 0;font-weight:700;max-width:1420px}}
    .thesis{{font-size:28px;line-height:1.25;color:{pal['muted']};margin-top:10px;max-width:1350px}}
    .dominant{{position:absolute;left:{db[0]}px;top:{db[1]}px;width:{db[2]}px;height:{db[3]}px;z-index:20;background:{'transparent' if form=='HERO_IMAGE' else '#F1DEE8'};border-radius:18px;overflow:hidden;display:flex;align-items:stretch;justify-content:stretch}}
    .dominant-inner{{width:100%;height:100%;padding:38px;display:flex;gap:22px;align-items:stretch;justify-content:center}}
    .node{{background:#fff;border:3px solid #E6E2E4;border-radius:18px;padding:20px;min-width:130px;min-height:80px;font-size:20px;line-height:1.25;display:flex;align-items:center;justify-content:center;text-align:center;flex:1;position:relative;z-index:23}}
    .node-rank-1{{background:#F8EDF3;border:4px solid {pal['accent_primary']};font-size:22px;font-weight:700}}
    .form-hub .node-rank-1,.form-field .node-rank-1{{grid-column:span 2;grid-row:span 1}}
    .form-matrix .node-rank-1{{grid-row:span 2}}
    .form-lane .node-rank-1{{flex:1.65}} .form-spine .node-rank-1{{flex:1.55}} .form-stack .node-rank-1{{flex:1.5}}
    .form-hub{{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr)}} .form-stack{{display:grid;grid-template-rows:repeat(5,1fr)}} .form-lane{{display:flex;flex-direction:row-reverse}} .form-spine{{display:flex;flex-direction:column}} .form-matrix{{display:grid;grid-template-columns:repeat(2,1fr);grid-auto-rows:1fr}} .form-field{{display:grid;grid-template-columns:repeat(3,1fr)}} .form-ladder{{display:flex;flex-direction:column-reverse}}
    .support{{position:absolute;left:{zones.get('SUPPORT',[90,300,400,500])[0]}px;top:{zones.get('SUPPORT',[90,300,400,500])[1]}px;width:{zones.get('SUPPORT',[90,300,400,500])[2]}px;height:{zones.get('SUPPORT',[90,300,400,500])[3]}px;z-index:22;padding:22px;border-right:6px solid {pal['accent_primary']};background:#F0F4FA;border-radius:8px}}
    .support ul{{margin:0;padding:0 24px 0 0}} .support li{{font-size:20px;line-height:1.35;margin-bottom:16px}} .hero-statement{{font-size:40px;line-height:1.15;font-weight:700;align-self:center;padding:50px}} .proof-strip{{font-size:18px}}
    .implication{{position:absolute;left:220px;right:360px;bottom:82px;min-height:58px;padding:14px 22px;border-top:3px solid {pal['accent_primary']};font-size:18px;line-height:1.35;text-align:center;background:#F1DEE8;z-index:25;font-weight:700}}
    table{{width:100%;height:100%;border-collapse:collapse;font-size:20px}}td{{border-bottom:1px solid #E6E2E4;padding:14px}} td:first-child{{color:{pal['accent_primary']};font-weight:700;width:64px}}
    .chart{{display:flex;align-items:flex-end;gap:24px;width:100%;height:100%;padding:55px}} .bar{{flex:1;background:{pal['accent_primary']};border-radius:12px 12px 0 0;position:relative;min-height:8%}}.bar span{{position:absolute;top:-32px;width:100%;text-align:center;font-weight:700}}
    .hero-plate{{width:100%;height:100%;object-fit:cover}} .image-pending{{width:100%;height:100%;display:flex;align-items:center;justify-content:center;border:3px dashed #D32A45;color:#D32A45;font-size:22px}}
    .cobrand{{position:absolute;left:58px;top:40px;width:300px;height:56px;display:flex;direction:ltr;align-items:center;gap:18px;z-index:40}} .brand-logo{{width:150px;height:52px;object-fit:contain;object-position:left center}} .client-logo{{width:120px;height:52px;object-fit:contain;object-position:left center;border-left:1px solid #D9D5D7;padding-left:16px}} .footer{{position:absolute;left:58px;right:58px;bottom:38px;font-size:14px;color:{pal['muted']};z-index:30}}
    #edge-layer{{position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:22;pointer-events:none;overflow:visible}} path{{stroke:{pal['accent_primary']};stroke-width:4;fill:none;opacity:.94}} .edge-label{{font-size:15px;font-weight:700;fill:{pal['accent_primary']};paint-order:stroke;stroke:{pal['canvas']};stroke-width:7px;stroke-linejoin:round}}
    </style></head><body><div class="page" data-page-mode="ARTIFACT_LED" data-page-family="{_esc(spec['page_family'])}" data-page-id="{_esc(spec.get('page_id') or 'PAGE')}" data-grammar-id="{_esc((spec.get('reference_grammar_ids') or ['NONE'])[0])}">
    <div class="cobrand" data-region-id="COBRAND">{logo}{client}</div><div class="header" data-header-role="TITLE"><div class="eyebrow">{_rich_visible(content_pack.get('eyebrow') or '', arabic=arvis)}</div><h1 data-content-slot="question">{title}</h1><div class="thesis" data-content-slot="thesis">{thesis}</div></div>
    <svg id="edge-layer"><defs><marker id="rashad-arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="{pal['accent_primary']}" stroke="none"/></marker></defs></svg><div class="dominant" data-region-id="DOMINANT" data-area-budget="{spec['dominant_mass_target']}">{structure}</div>
    <div class="support" data-region-id="SUPPORT"><ul>{support}</ul></div><div class="implication" data-content-slot="implication">{implication}</div><div class="footer" data-header-role="FOOTER" data-content-slot="source" data-source="{_esc(source_id)}" data-directionality="ISOLATED">{_esc(content_pack.get('footer') or content_pack.get('source_note') or source_id)}</div>
    </div><script>
    async function layout(){{await document.fonts.ready; const svg=document.getElementById('edge-layer'); const defs=svg.querySelector('defs'); svg.querySelectorAll('path[data-edge-id]').forEach(x=>x.remove()); const nodes=[...document.querySelectorAll('[data-node-id]')]; const by=Object.fromEntries(nodes.map(n=>[n.dataset.nodeId,n])); const edges={json.dumps(topo.get('edges') or [],ensure_ascii=False)}; const edgeLabels={json.dumps(edge_labels,ensure_ascii=False)}; function anchor(a,b){{const acx=a.left+a.width/2,acy=a.top+a.height/2,bcx=b.left+b.width/2,bcy=b.top+b.height/2,dx=bcx-acx,dy=bcy-acy;if(Math.abs(dx)>=Math.abs(dy))return{{x:dx>=0?a.right:a.left,y:acy}};return{{x:acx,y:dy>=0?a.bottom:a.top}}}} for(const e of edges){{let s=by[e.source],t=by[e.target]; if(!s||!t)continue; let a=s.getBoundingClientRect(),b=t.getBoundingClientRect(); let p=document.createElementNS('http://www.w3.org/2000/svg','path'); let d; const acx=a.left+a.width/2,acy=a.top+a.height/2,bcx=b.left+b.width/2,bcy=b.top+b.height/2; const vGapDown=b.top-a.bottom, vGapUp=a.top-b.bottom, hGapRight=b.left-a.right, hGapLeft=a.left-b.right; if(vGapDown>8){{const y=(a.bottom+b.top)/2;d=`M ${{acx}} ${{a.bottom}} L ${{acx}} ${{y}} L ${{bcx}} ${{y}} L ${{bcx}} ${{b.top}}`;}} else if(vGapUp>8){{const y=(b.bottom+a.top)/2;d=`M ${{acx}} ${{a.top}} L ${{acx}} ${{y}} L ${{bcx}} ${{y}} L ${{bcx}} ${{b.bottom}}`;}} else if(hGapRight>8){{const x=(a.right+b.left)/2;d=`M ${{a.right}} ${{acy}} L ${{x}} ${{acy}} L ${{x}} ${{bcy}} L ${{b.left}} ${{bcy}}`;}} else if(hGapLeft>8){{const x=(b.right+a.left)/2;d=`M ${{a.left}} ${{acy}} L ${{x}} ${{acy}} L ${{x}} ${{bcy}} L ${{b.right}} ${{bcy}}`;}} else {{let p0=anchor(a,b),p1=anchor(b,a),mx=(p0.x+p1.x)/2;d=`M ${{p0.x}} ${{p0.y}} C ${{mx}} ${{p0.y}}, ${{mx}} ${{p1.y}}, ${{p1.x}} ${{p1.y}}`;}} p.setAttribute('d',d);p.setAttribute('marker-end','url(#rashad-arrow)'); p.dataset.edgeId=e.id;p.dataset.source=e.source;p.dataset.target=e.target;p.dataset.directionality='DIRECTED';p.dataset.labelOwner=e.label_owner||'EDGE'; const rel=edgeLabels[e.relation]||''; if(rel){{p.dataset.relationLabel=rel;p.setAttribute('aria-label',rel);}} svg.appendChild(p); }} document.documentElement.dataset.rashadLayoutReady='1';}}
    layout();</script></body></html>'''
    out.write_text(html_txt,encoding='utf-8')
    return {'status':'PASS','html_path':str(out),'html_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'composition_spec_sha256':spec.get('spec_sha256'),'instrumented':True}
