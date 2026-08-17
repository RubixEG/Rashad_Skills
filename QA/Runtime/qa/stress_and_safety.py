#!/usr/bin/env python3
"""
Rashad v2.6 — Arabic stress matrix, repair-safety signatures, and pixel evidence.

Closes three declared-but-unimplemented layers:

  * Stress QA (Arabic)  — v2.5 mutates font size and line height only, and its
    text-growth mutation silently does nothing unless the producer opted in with
    `data-stress-grow`. None of the Arabic-specific threats in the doctrine
    (Arabic-Indic numerals, long Latin tokens, 4/5-digit badges, 3-line titles,
    font fallback, node growth) were implemented.

  * Repair Safety — the doctrine requires freezing content / node / edge / label
    / topology / brand / direction signatures before a safety repair and
    comparing after, so that fixing an overflow cannot quietly delete an edge or
    shrink a paragraph away. No code existed.

  * Pixel QA — v2.5 measures the DOM only. It never takes a screenshot. "Final
    pixels prove the artifact survived production" was policy with no proof.
"""
from __future__ import annotations
import re, json, hashlib, math, argparse
from pathlib import Path

# ==========================================================================
# 1. ARABIC STRESS MATRIX
# ==========================================================================

EU2AR = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
LONG_LATIN = 'NCWM-PPP-2025-01-REV-B-ANNEX-VII-SUPPLEMENTARY'

STRESS_MODES = {
    'ARABIC_INDIC_NUMERALS': """(sel)=>{
        const w=document.createTreeWalker(document.querySelector(sel)||document.body,NodeFilter.SHOW_TEXT);
        const map={'0':'٠','1':'١','2':'٢','3':'٣','4':'٤','5':'٥','6':'٦','7':'٧','8':'٨','9':'٩'};
        let n; while(n=w.nextNode()){ if(/[0-9]/.test(n.nodeValue)) n.nodeValue=n.nodeValue.replace(/[0-9]/g,d=>map[d]); }
    }""",
    'FIVE_DIGIT_BADGE': """(sel)=>{
        document.querySelectorAll(sel+' [data-owner-id], '+sel+' .sn, '+sel+' .gnum, '+sel+' .badge').forEach(e=>{
            if(/^[\\s\\d٠-٩]{1,3}$/.test(e.textContent.trim())) e.textContent='١٢٣٤٥';
        });
    }""",
    'LONG_LATIN_TOKEN': """([sel,tok])=>{
        const els=[...document.querySelectorAll(sel+' *')].filter(e=>{
            const t=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.nodeValue).join('').trim();
            return t.length>12 && t.length<160;});
        els.slice(0,6).forEach(e=>{ e.appendChild(document.createTextNode(' '+tok)); });
    }""",
    'TITLE_THREE_LINES': """(sel)=>{
        document.querySelectorAll(sel+' [data-header-role="TITLE"], '+sel+' h1, '+sel+' h2').forEach(e=>{
            e.textContent = e.textContent.trim()+' '+e.textContent.trim()+' '+e.textContent.trim().slice(0,40);
        });
    }""",
    'FONT_FALLBACK': """(sel)=>{
        const s=document.createElement('style');
        s.textContent='*{font-family:"__RASHAD_MISSING_FONT__", serif !important}';
        document.head.appendChild(s);
    }""",
    'NODE_GROWTH': """(sel)=>{
        const nodes=[...document.querySelectorAll(sel+' [data-node-id]')];
        if(!nodes.length) return;
        const proto=nodes[nodes.length-1];
        for(let i=0;i<Math.max(2,Math.ceil(nodes.length*0.3));i++){
            const c=proto.cloneNode(true); c.setAttribute('data-node-id','STRESS-N'+i);
            proto.parentElement.appendChild(c);
        }
    }""",
    'LONG_SOURCE_LINE': """(sel)=>{
        document.querySelectorAll(sel+' [data-content-slot="source"], '+sel+' .source, '+sel+' footer').forEach(e=>{
            e.textContent = (e.textContent||'').trim()+' — المصدر: ملف التأهيل، دراسة الشروط والمواصفات، الملحق السابع، البند ٤-٢-٣، الإصدار المعدل';
        });
    }""",
    'LOGO_CANVAS_PADDING': """(sel)=>{
        document.querySelectorAll(sel+' img').forEach(e=>{ e.style.padding='14px'; e.style.boxSizing='content-box'; });
    }""",
    'FONT_SCALE_108': """(sel)=>{document.querySelectorAll(sel+' *').forEach(e=>{const s=parseFloat(getComputedStyle(e).fontSize);if(s>0)e.style.fontSize=(s*1.08)+'px';});}""",
    'FONT_SCALE_110': """(sel)=>{document.querySelectorAll(sel+' *').forEach(e=>{const s=parseFloat(getComputedStyle(e).fontSize);if(s>0)e.style.fontSize=(s*1.10)+'px';});}""",
    'LINE_HEIGHT_108': """(sel)=>{document.querySelectorAll(sel+' *').forEach(e=>{const s=parseFloat(getComputedStyle(e).lineHeight);if(Number.isFinite(s)&&s>0)e.style.lineHeight=(s*1.08)+'px';});}""",
    'ARABIC_TEXT_GROWTH_120': """(sel)=>{const ar=/[\u0600-\u06FF]/;document.querySelectorAll(sel+' [data-content-slot=\"evidence\"],'+sel+' [data-content-slot=\"implication\"]').forEach(e=>{if(ar.test(e.textContent))e.textContent=e.textContent+' — مع توضيح إضافي مرتبط بالأثر والقرار';});}""",
}


def apply_stress(page, selector, mode):
    js = STRESS_MODES[mode]
    if mode == 'LONG_LATIN_TOKEN':
        page.evaluate(js, [selector, LONG_LATIN])
    else:
        page.evaluate(js, selector)


def stress_gate(results, required_modes=None):
    required_modes = required_modes or list(STRESS_MODES)
    ran = {r['mode'] for r in results}
    viol = [{'kind': 'stress_mode_not_executed', 'mode': m}
            for m in required_modes if m not in ran]
    viol += [{'kind': 'fragile_under_stress', 'mode': r['mode'],
              'failed_gates': r['failed_gates']}
             for r in results if r['failed_gates']]
    return {'id': 'C9_STRESS', 'name': 'Arabic + structural stress matrix',
            'required': True, 'executed': True, 'test_count': len(results),
            'status': 'FAIL' if (viol or not results) else 'PASS',
            'violations': viol or ([{'kind': 'FAIL_NOT_INSTRUMENTED', 'gate': 'C9_STRESS'}] if not results else []),
            'measured': {'count': len(results), 'modes_run': sorted(ran)}}

# ==========================================================================
# 2. REPAIR SAFETY SIGNATURES
# ==========================================================================

SIGNATURE_JS = """(sel)=>{
 const pages=[...document.querySelectorAll(sel)];
 const norm=s=>(s||'').replace(/\\s+/g,' ').trim();
 return pages.map((p,i)=>{
   const texts=[]; const w=document.createTreeWalker(p,NodeFilter.SHOW_TEXT);
   let n; while(n=w.nextNode()){ const t=norm(n.nodeValue); if(t) texts.push(t); }
   const nodes=[...p.querySelectorAll('[data-node-id]')].map(e=>e.dataset.nodeId).sort();
   const edges=[...p.querySelectorAll('[data-edge-id],[data-edge]')].map(e=>
       [e.dataset.edgeId||e.dataset.edge, e.dataset.source||'', e.dataset.target||'', e.dataset.relation||''].join('>')).sort();
   const labels=[...p.querySelectorAll('[data-label-for]')].map(e=>e.dataset.labelFor+':'+norm(e.textContent)).sort();
   const assets=[...p.querySelectorAll('img,[data-asset-id]')].map(e=>e.dataset.assetId||e.getAttribute('src')||'').sort();
   const dirs=[...p.querySelectorAll('[data-seq-group]')].map(e=>e.dataset.seqGroup+'#'+(e.dataset.seq||'')).sort();
   const colours=[...new Set([...p.querySelectorAll('*')].flatMap(e=>{const c=getComputedStyle(e);return [c.color,c.backgroundColor];}))].sort();
   return {page:i+1, texts, nodes, edges, labels, assets, dirs, colours,
           word_count: texts.join(' ').split(/\\s+/).filter(Boolean).length};
 });
}"""

SIG_PARTS = ['content', 'nodes', 'edges', 'labels', 'assets', 'direction', 'brand']

def _h(x): return hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:24]

def freeze(raw):
    """Turn the raw DOM capture into the frozen signature set."""
    return [{
        'page': p['page'],
        'content': _h(p['texts']), 'nodes': _h(p['nodes']), 'edges': _h(p['edges']),
        'labels': _h(p['labels']), 'assets': _h(p['assets']),
        'direction': _h(p['dirs']), 'brand': _h(p['colours']),
        '_counts': {'words': p['word_count'], 'nodes': len(p['nodes']),
                    'edges': len(p['edges']), 'labels': len(p['labels'])},
        '_raw': {k: p[k] for k in ('nodes', 'edges', 'labels')},
    } for p in raw]


def compare(before, after, word_loss_tolerance=0.0):
    """
    Geometry may change. Meaning may not.
    A repair that fixes an overflow by deleting an edge or shrinking a paragraph
    away is a REPAIR FAIL even though the page now renders cleanly.
    """
    viol = []
    bi = {p['page']: p for p in before}
    for a in after:
        b = bi.get(a['page'])
        if not b:
            viol.append({'kind': 'page_disappeared_during_repair', 'page': a['page']})
            continue
        for part in SIG_PARTS:
            if b[part] != a[part]:
                d = {'kind': f'{part}_signature_changed', 'page': a['page'],
                     'before': b[part], 'after': a[part]}
                if part in ('nodes', 'edges', 'labels'):
                    lost = sorted(set(b['_raw'][part]) - set(a['_raw'][part]))
                    added = sorted(set(a['_raw'][part]) - set(b['_raw'][part]))
                    d['lost'] = lost[:12]; d['added'] = added[:12]
                    d['severity'] = 'BLOCKER' if lost else 'HIGH'
                elif part == 'content':
                    wb, wa = b['_counts']['words'], a['_counts']['words']
                    d['words_before'], d['words_after'] = wb, wa
                    d['severity'] = 'BLOCKER' if wa < wb*(1-word_loss_tolerance) else 'MEDIUM'
                else:
                    d['severity'] = 'HIGH'
                viol.append(d)
    return {'id': 'C10_REPAIR_SAFE', 'name': 'Repair without semantic loss',
            'required': True, 'executed': True, 'test_count': len(after),
            'status': 'FAIL' if any(v.get('severity')!='ADVISORY' for v in viol) else 'PASS', 'violations': viol,
            'measured': {'count': len(after), 'parts_compared': SIG_PARTS}}

# ==========================================================================
# 3. PIXEL EVIDENCE
# ==========================================================================

def pixel_gate(png_path, prof, spec=None):
    """
    DOM-clean is not pixel-clean. This inspects what was actually rasterised:
      * ink coverage inside the live area (blank page / over-full page)
      * dead-zone detection (a declared region that rendered empty)
      * banned near-black dominant background, measured on pixels not CSS
      * edge density as a proxy for structure actually being drawn
      * uniform-tile detection: a page that is 6 identical rectangles
    """
    from PIL import Image, ImageFilter, ImageStat
    import numpy as np
    spec = spec or {}
    im = Image.open(png_path).convert('RGB')
    W, H = im.size
    a = np.asarray(im).astype(float)
    lum = (0.2126*a[..., 0] + 0.7152*a[..., 1] + 0.0722*a[..., 2])/255.0
    viol = []

    # dominant background luminance on real pixels.
    # NOTE: binning must be fine at the dark end or a #121216 canvas reads as
    # 0.0625 and slips past a 0.04 near-black threshold. Bin, then take the
    # ACTUAL mean of the winning cluster rather than the bin centre.
    BINS = 256
    idx = np.clip((lum*(BINS-1)).astype(int), 0, BINS-1)
    counts = np.bincount(idx.ravel(), minlength=BINS)
    dom_bin = int(counts.argmax()); dom_share = counts.max()/lum.size
    dom_lum = float(lum[idx == dom_bin].mean())
    nb = prof.get('brand_lock', {}).get('near_black_luminance_max', 0.04)
    if dom_share >= 0.35 and dom_lum <= nb:
        viol.append({'kind': 'pixel_near_black_dominant_canvas',
                     'luminance': round(dom_lum, 4), 'share': round(dom_share, 3)})

    # ink coverage: how much of the page differs from the dominant background
    ink = float((np.abs(lum - dom_lum) > 0.06).mean())
    if ink < 0.04:
        viol.append({'kind': 'page_effectively_blank', 'ink_coverage': round(ink, 4)})
    if ink > 0.72:
        viol.append({'kind': 'page_over_full', 'ink_coverage': round(ink, 4),
                     'note': 'no whitespace left for the eye to rest — clutter, not density'})

    # dead zones: 6x4 grid cells with no ink at all
    gy, gx = 4, 6
    dead = []
    for j in range(gy):
        for i in range(gx):
            cell = lum[int(j*H/gy):int((j+1)*H/gy), int(i*W/gx):int((i+1)*W/gx)]
            if float((np.abs(cell - dom_lum) > 0.06).mean()) < 0.004:
                dead.append([i, j])
    if len(dead) >= gx*gy*0.5:
        viol.append({'kind': 'excessive_dead_area', 'empty_cells': len(dead),
                     'of': gx*gy})

    # structure proxy: edge density
    edges = np.asarray(im.convert('L').filter(ImageFilter.FIND_EDGES)).astype(float)/255.0
    edge_density = float((edges > 0.20).mean())
    if edge_density < 0.010 and ink > 0.05:
        viol.append({'kind': 'no_drawn_structure',
                     'edge_density': round(edge_density, 5),
                     'note': 'content present but almost no drawn structure — text slab, not an exhibit'})
    # VISUAL FILL floor for artifact-led pages.
    #
    # IMPORTANT — what this does and does not measure. Edge density measures how
    # much of the page is visually occupied by drawn boundaries. It is a FILL
    # metric, not an analytical-structure metric: a grid of equal cards scores
    # HIGH on it because card borders are edges. It is therefore useful for
    # catching an under-filled or over-full page, and useless for judging whether
    # the page explains a relationship. That judgement belongs to G32.
    #
    # Calibrated on the real corpus: native HTML route 0.027-0.054,
    # AI Golden-Visual route 0.056-0.117. The two populations separate cleanly,
    # but the separation is about visual density, not about analysis.
    #
    # Use both: G32 (>=85) proves the page explains its relationships; this gate
    # proves the page is neither sparse nor cluttered. A page can pass one and
    # fail the other, and both failures are real.
    floor = prof.get('thresholds', {}).get('min_visual_fill_density', 0.030)
    target = prof.get('thresholds', {}).get('target_visual_fill_density', 0.055)
    ceiling = prof.get('thresholds', {}).get('max_visual_fill_density', 0.72)
    mode = (spec.get('page_mode') or '').upper()
    if mode in ('ARTIFACT_LED', 'HYBRID'):
        if edge_density < floor:
            viol.append({'kind': 'page_visually_underfilled',
                         'edge_density': round(edge_density, 5), 'floor': floor,
                         'note': 'large areas carry no content; add evidence, not decoration'})
        elif edge_density < target:
            viol.append({'kind': 'visual_fill_below_target', 'severity': 'ADVISORY',
                         'edge_density': round(edge_density, 5), 'target': target,
                         'note': 'structurally sound but sparse against the reference corpus'})
        if edge_density > ceiling:
            viol.append({'kind':'page_visually_overfilled','edge_density':round(edge_density,5),'ceiling':ceiling,'note':'visual density exceeds the governed readability ceiling'})

    # uniform-tile detection (pixel-level card grid smell)
    rowsig = [_h(np.round(lum[int(j*H/24):int((j+1)*H/24)].mean(axis=0), 2).tolist()) for j in range(24)]
    rep = max(rowsig.count(x) for x in set(rowsig))
    if rep >= 8:
        viol.append({'kind': 'uniform_tiling_detected', 'repeated_row_bands': rep,
                     'note': 'large blocks of identical horizontal structure — grid of equal boxes'})

    return {'id': 'C9_PIXEL', 'name': 'Final rendered pixel evidence',
            'required': True, 'executed': True, 'test_count': 1,
            'status': 'FAIL' if any(v.get('severity')!='ADVISORY' for v in viol) else 'PASS', 'violations': viol,
            'measured': {'count': 1, 'size': [W, H],
                         'dominant_luminance': round(dom_lum, 4),
                         'dominant_share': round(dom_share, 3),
                         'ink_coverage': round(ink, 4),
                         'edge_density': round(edge_density, 5),
                         'dead_cells': len(dead)}}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('pixel'); p.add_argument('png'); p.add_argument('--profile', required=True)
    c = sub.add_parser('compare'); c.add_argument('before'); c.add_argument('after')
    a = ap.parse_args()
    if a.cmd == 'pixel':
        r = pixel_gate(a.png, json.loads(Path(a.profile).read_text()))
    else:
        r = compare(json.loads(Path(a.before).read_text()),
                    json.loads(Path(a.after).read_text()))
    print(json.dumps(r, indent=2, ensure_ascii=False))
    raise SystemExit(0 if r['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
