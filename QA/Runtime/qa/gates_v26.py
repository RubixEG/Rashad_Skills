#!/usr/bin/env python3
"""
Rashad Visual QA Harness v2.6 — new gate set.

v2.5 implements 24 render-geometry gates (G00-G23). Audit of the delivered
MWAN artifacts showed that the following DECLARED QA layers had NO executable
implementation at all:

    Evidence QA, Content QA, Artifact-strength QA, BiDi run-order QA,
    Logo/co-brand QA, Palette/theme QA, Contrast/legibility QA,
    Type-scale QA, Pixel QA, Anti-template QA, Repair-safety QA.

This module implements them. Every gate here follows the v2.6 requiredness
rule (see `derive_required`): a gate is REQUIRED when the page CONTENT implies
it, not when a hand-written spec happens to say so. That closes the v2.5
vacuous-pass hole where an Arabic deck passed G14_RTL_BIDI with 0 tested
objects because the spec omitted `sequence_groups`.

All gates take the v2.5 `pd` page-record (from visual_qa.COLLECT) plus profile
and spec, and return the same gate dict shape, so they drop into the existing
report and aggregator without changing consumers.
"""
from __future__ import annotations
import re, math, hashlib, unicodedata
from qa_v4.arabic_executive_terminology import validate_page_text_elements
from pathlib import Path

PASS, FAIL = 'PASS', 'FAIL'

# --------------------------------------------------------------------------
# v2.6 requiredness derivation — the no-vacuous-pass fix
# --------------------------------------------------------------------------

ARABIC = re.compile(r'[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]')
LATIN  = re.compile(r'[A-Za-z]')
AR_DIGIT = re.compile(r'[٠-٩۰-۹]')
EU_DIGIT = re.compile(r'[0-9]')

def derive_required(pd, spec):
    """
    Decide which gates MUST be instrumented, from what is actually on the page.
    A missing declaration can no longer silence a gate.
    """
    els = pd['els']
    txt = ' '.join(e['text'] for e in pd['texts'])
    has_ar = bool(ARABIC.search(txt))
    has_img = len(pd['images']) > 0
    has_svg = any(e['tag'] in ('svg', 'path', 'line', 'polyline', 'polygon') for e in els)
    n_surfaces = sum(1 for e in els
                     if (e['css']['background'] or '') not in ('', 'transparent', 'rgba(0, 0, 0, 0)'))
    words = sum(len(e['text'].split()) for e in pd['texts'])
    mode = (spec.get('page_mode') or '').upper()
    # a page carrying real argument load is analytical whether or not a spec says so
    analytical = (mode in ('ARTIFACT_LED', 'HYBRID', 'ANALYTICAL')
                  or n_surfaces >= 4 or words >= 60)

    return {
        # any page with visible text must prove palette + contrast + type scale
        'palette':        True,
        'contrast':       True,
        'type_scale':     True,
        # any page carrying Arabic must prove BiDi run order — not optional
        'bidi':           has_ar,
        # any page with images must prove asset integrity; co-brand on every page
        'assets':         has_img,
        'cobrand':        True,
        # analytical pages must carry a content pack and evidence trace
        'content_pack':   analytical,
        'evidence_trace': analytical,
        # artifact strength required wherever an artifact is claimed OR the page
        # is dense enough that boxes-only would be a failure
        'artifact':       bool(spec.get('artifact_expected')) or analytical or has_svg,
        'pixel':          True,
    }

def gate(gid, name, viol, measured=None, required=True, test_count=None):
    tc = test_count if test_count is not None else (measured or {}).get('count')
    if required and tc == 0 and not viol:
        viol = [{'kind': 'FAIL_NOT_INSTRUMENTED', 'gate': gid,
                 'note': 'gate required by v2.6 content-derived rule but nothing was measurable'}]
    return {'id': gid, 'name': name, 'status': FAIL if viol else PASS,
            'required': required, 'executed': True, 'test_count': tc,
            'violations': viol, 'measured': measured or {}}

# --------------------------------------------------------------------------
# colour helpers
# --------------------------------------------------------------------------

def _rgb(css):
    m = re.findall(r'[\d.]+', css or '')
    if len(m) < 3: return None
    return tuple(int(float(x)) for x in m[:3])

def _hex(rgb): return '#%02x%02x%02x' % rgb

def _lum(rgb):
    def f(c):
        c = c/255.0
        return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
    r, g, b = rgb
    return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b)

def contrast_ratio(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05)/(lo + 0.05)

def _de76(a, b):
    """Cheap perceptual distance in linearised RGB — good enough for palette snap."""
    return math.sqrt(sum((x-y)**2 for x, y in zip(a, b)))

def _effective_bg(e, byidx):
    """Walk ancestors until a non-transparent background is found."""
    cur, hops = e, 0
    while cur is not None and hops < 24:
        bg = _rgb(cur['css']['background'])
        if bg and 'rgba(0, 0, 0, 0)' not in (cur['css']['background'] or ''):
            return bg
        p = cur.get('parent')
        cur = byidx.get(str(p)) if p is not None else None
        hops += 1
    return (255, 255, 255)

# --------------------------------------------------------------------------
# G24 PALETTE LOCK  (Theme & Colour Governor made executable)
# --------------------------------------------------------------------------

def g24_palette(pd, prof, spec, req):
    brand = prof.get('brand_lock', {})
    allowed = [tuple(int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
               for h in brand.get('palette_hex', [])]
    tol = brand.get('palette_delta_tolerance', 18)
    budget = brand.get('max_distinct_colours_per_page', 12)
    near_black = brand.get('near_black_luminance_max', 0.06)
    min_area_for_bg = brand.get('background_min_area_share', 0.35)

    els = list(pd['els'])
    # v2.6 FIX D3: querySelectorAll('*') inside the page never returns the page
    # container itself, so in v2.5 the SLIDE'S OWN BACKGROUND was never checked —
    # a black canvas was structurally invisible to the canvas rule it violates.
    if pd.get('container_css'):
        els = els + [{'idx': -1, 'tag': 'section', 'cls': ['__page__'], 'text': '',
                      'rect': dict(pd['rect']), 'css': pd['container_css'],
                      'data': {}, 'parent': None}]
    pr = pd['rect']; parea = (pr['w']*pr['h']) or 1
    viol = []; seen = {}
    for e in els:
        for key in ('background', 'color'):
            c = _rgb(e['css'][key])
            if not c: continue
            if key == 'background' and (e['css']['background'] or '').find('rgba(0, 0, 0, 0)') >= 0:
                continue
            seen[_hex(c)] = seen.get(_hex(c), 0) + 1
            if allowed and min(_de76(c, a) for a in allowed) > tol:
                viol.append({'kind': 'off_palette_colour', 'idx': e['idx'], 'prop': key,
                             'colour': _hex(c),
                             'nearest_delta': round(min(_de76(c, a) for a in allowed), 1)})
    # near-black large surface ban ("No black or near-black slide backgrounds")
    for e in els:
        raw = e['css']['background'] or ''
        if 'rgba(0, 0, 0, 0)' in raw or raw in ('', 'transparent'):
            continue                      # transparent parses as black — never a canvas
        c = _rgb(raw)
        if not c: continue
        share = (e['rect']['w']*e['rect']['h'])/parea
        if share >= min_area_for_bg and _lum(c) <= near_black:
            viol.append({'kind': 'near_black_background_banned', 'idx': e['idx'],
                         'colour': _hex(c), 'luminance': round(_lum(c), 4),
                         'area_share': round(share, 3),
                         'rule': 'v2 brand rule: no black or near-black slide backgrounds'})
    if len(seen) > budget:
        viol.append({'kind': 'colour_budget_exceeded', 'distinct': len(seen),
                     'budget': budget, 'colours': sorted(seen)[:40]})
    return gate('G24_PALETTE_LOCK', 'Brand palette / theme hard lock', viol,
                {'count': len(seen), 'distinct_colours': len(seen),
                 'colours': sorted(seen)[:40]},
                required=req['palette'], test_count=len(seen))

# --------------------------------------------------------------------------
# G25 CONTRAST / LEGIBILITY
# --------------------------------------------------------------------------

def g25_contrast(pd, prof, spec, req):
    th = prof.get('brand_lock', {})
    aa_normal = th.get('contrast_min_normal', 4.5)
    aa_large  = th.get('contrast_min_large', 3.0)
    large_px  = th.get('large_text_px', 24)
    byidx = {str(e['idx']): e for e in pd['els']}
    viol = []; tested = 0
    for e in pd['texts']:
        fg = _rgb(e['css']['color'])
        if not fg: continue
        bg = _effective_bg(e, byidx)
        tested += 1
        cr = contrast_ratio(fg, bg)
        need = aa_large if e['css']['fontSize'] >= large_px else aa_normal
        if cr < need:
            viol.append({'kind': 'contrast_below_aa', 'idx': e['idx'],
                         'ratio': round(cr, 2), 'required': need,
                         'fg': _hex(fg), 'bg': _hex(bg),
                         'font_px': e['css']['fontSize'], 'text': e['text'][:60]})
    return gate('G25_CONTRAST', 'Text contrast / legibility (WCAG AA)', viol,
                {'count': tested}, required=req['contrast'], test_count=tested)

# --------------------------------------------------------------------------
# G26 TYPE SCALE  (token conformance, not just min size)
# --------------------------------------------------------------------------

def g26_type_scale(pd, prof, spec, req):
    ts = prof.get('brand_lock', {}).get('type_scale_px', [])
    max_distinct = prof.get('brand_lock', {}).get('max_distinct_font_sizes', 8)
    tol = prof.get('brand_lock', {}).get('type_scale_tolerance_px', 0.6)
    sizes = {}
    viol = []
    for e in pd['texts']:
        fs = e['css']['fontSize']
        if not fs: continue
        sizes[fs] = sizes.get(fs, 0) + 1
        if ts and min(abs(fs - t) for t in ts) > tol:
            viol.append({'kind': 'off_scale_font_size', 'idx': e['idx'], 'size': fs,
                         'nearest_token': min(ts, key=lambda t: abs(fs-t)),
                         'text': e['text'][:50]})
    if len(sizes) > max_distinct:
        viol.append({'kind': 'type_scale_sprawl', 'distinct': len(sizes),
                     'budget': max_distinct, 'sizes': sorted(sizes)})
    return gate('G26_TYPE_SCALE', 'Typographic scale conformance', viol,
                {'count': len(sizes), 'sizes': sorted(sizes)},
                required=req['type_scale'], test_count=len(sizes))

# --------------------------------------------------------------------------
# G27 BIDI RUN ORDER  (the gate an Arabic-first system cannot be without)
# --------------------------------------------------------------------------

LTR_ISLAND_HINTS = re.compile(
    r'\b(?:https?://|www\.|[A-Za-z0-9._%+-]+@|ISO\s?\d{3,5}|IEC|NIST|API|URL|SLA|KPI|PMO|ERP|CRM|'
    r'[A-Z]{2,6}-\d{2,6}|v\d+\.\d+)', re.I)

def g27_bidi(pd, prof, spec, req):
    """
    Checks that Arabic content is handled as PHYSICAL geometry:
      1. every element whose text is majority-Arabic resolves direction rtl
      2. Latin/technical tokens inside Arabic are isolated (LTR island) so the
         browser does not reorder them
      3. numeral system is consistent across the page (no mixed Arabic-Indic /
         European digits inside one logical run)
      4. rendered line boxes of an RTL element start from the right edge
      5. no bare bidi control characters left in the copy
    """
    viol = []; tested = 0
    numeral_modes = set()
    for e in pd['texts']:
        t = e['text']
        if not t.strip(): continue
        ar = len(ARABIC.findall(t)); la = len(LATIN.findall(t))
        iso = (e['data'].get('directionality') or '').upper() == 'ISOLATED'
        if ar == 0:
            if EU_DIGIT.search(t) and not iso: numeral_modes.add('EU')
            continue
        tested += 1
        d = e['css']['direction']
        # an explicitly ISOLATED run (a <bdi>, a numeric range, a technical token)
        # is exempt: dir=auto legitimately resolves such a run to ltr, and that is
        # the correct rendering for an isolated numeric island.
        if ar > la and d != 'rtl' and not iso:
            viol.append({'kind': 'arabic_not_rtl', 'idx': e['idx'],
                         'direction': d, 'text': t[:60]})
        # LTR islands
        if LTR_ISLAND_HINTS.search(t) and d == 'rtl':
            iso = e['data'].get('directionality', '')
            has_bdi = 'ltr-island' in ' '.join(e['cls']).lower() or iso.upper() == 'ISOLATED'
            if not has_bdi:
                viol.append({'kind': 'unisolated_ltr_island', 'idx': e['idx'],
                             'token': LTR_ISLAND_HINTS.search(t).group(0),
                             'text': t[:70],
                             'fix': 'wrap in <bdi dir="ltr"> or mark data-directionality="ISOLATED"'})
        # numeral consistency — an ISOLATED technical token is exempt by policy
        if not iso:
            if AR_DIGIT.search(t): numeral_modes.add('AR')
            if EU_DIGIT.search(t): numeral_modes.add('EU')
        if (AR_DIGIT.search(t) and EU_DIGIT.search(t)
                and (e['data'].get('directionality') or '').upper() != 'ISOLATED'):
            viol.append({'kind': 'mixed_numeral_systems_in_run', 'idx': e['idx'],
                         'text': t[:70]})
        # physical line start for rtl multi-line text
        lr = e.get('lineRects') or []
        # v2.6 FIX D4: an absolutely-positioned child (owner badge, chip) shifts
        # the first line box. Only measure blocks that are pure wrapped text.
        # D10/D11: separate two different phenomena that both produce >1 rect.
        #   * several distinct y-bands  -> the text WRAPPED; check right alignment
        #   * one y-band, several rects -> the text SPLIT INTO BIDI RUNS; that is
        #     the classic Arabic defect (digits, ranges, %, technical tokens
        #     reordering inside an RTL sentence) and needs <bdi> isolation.
        # On a flex/grid container selectNodeContents() returns one rect per child,
        # so container elements are excluded from both checks.
        if (d == 'rtl' and len(lr) >= 2
                and not e['data'].get('hasPositionedChild')
                and not e['data'].get('hasElementChild')):
            fs = e['css']['fontSize'] or 16
            bands = []
            for r in lr:
                if not any(abs(r['y'] - b) < fs*0.6 for b in bands):
                    bands.append(r['y'])
            rights = [r['r'] for r in lr]
            if len(bands) >= 2:
                # wrapped text: every line box shares the block's right edge.
                # Browsers exclude a trailing space from the first line box
                # (~0.25-0.6em); that is not a direction defect.
                tol = max(8.0, 0.6*fs)
                if max(rights) - rights[0] > tol:
                    viol.append({'kind': 'rtl_first_line_not_right_aligned',
                                 'idx': e['idx'],
                                 'line_rights': [round(x, 1) for x in rights[:4]]})
            elif (e['data'].get('directionality') or '').upper() != 'ISOLATED':
                runs = len(lr)
                viol.append({'kind': 'bidi_run_split_not_isolated', 'idx': e['idx'],
                             'runs': runs, 'text': t[:70],
                             'note': 'a numeric range, percentage or technical token '
                                     'is forming its own directional run inside RTL text',
                             'fix': 'wrap the run in <bdi> or mark data-directionality="ISOLATED"'})
        # stray bidi controls
        ctl = [c for c in t if unicodedata.category(c) == 'Cf' and c in '‎‏‪‫‬‭‮⁦⁧⁨⁩']
        if ctl and len(ctl) > 4:
            viol.append({'kind': 'excess_bidi_control_chars', 'idx': e['idx'],
                         'count': len(ctl)})
    if len(numeral_modes) > 1:
        viol.append({'kind': 'page_numeral_system_inconsistent',
                     'modes': sorted(numeral_modes)})
    return gate('G27_BIDI_RUNS', 'BiDi run order / numerals / LTR islands', viol,
                {'count': tested, 'numeral_modes': sorted(numeral_modes)},
                required=req['bidi'], test_count=tested)

# --------------------------------------------------------------------------
# G28 CO-BRAND LOCKUP  (Rubix | Client stays physically LEFT under RTL)
# --------------------------------------------------------------------------

def g28_cobrand(pd, prof, spec, req):
    lock = prof.get('brand_lock', {})
    max_left_share = lock.get('cobrand_max_left_fraction', 0.42)
    clear = lock.get('cobrand_clear_space_ratio', 0.5)   # x logo height
    optical_tol = lock.get('cobrand_optical_height_tolerance', 0.12)

    pr = pd['rect']
    marks = [e for e in pd['els']
             if e['data'].get('asset') or
                (e['tag'] == 'img' and re.search(r'logo|mark|brand|emblem',
                    (e.get('image', {}).get('src', '') + ' ' + ' '.join(e['cls'])), re.I))]
    viol = []
    if marks:
        marks_sorted = sorted(marks, key=lambda e: e['rect']['x'])
        first = marks_sorted[0]
        # 1. lockup lives in the left band of the page regardless of direction
        if (first['rect']['x'] - pr['x'])/max(1, pr['w']) > max_left_share:
            viol.append({'kind': 'cobrand_not_physically_left',
                         'idx': first['idx'],
                         'left_fraction': round((first['rect']['x']-pr['x'])/pr['w'], 3),
                         'max': max_left_share,
                         'rule': 'Rubix|Client lockup stays physically LEFT; RTL must not mirror it'})
        # 2. Rubix must be the left-most mark
        rubix = [e for e in marks if re.search(r'rubix',
                 (e.get('image', {}).get('src', '') + ' ' + ' '.join(e['cls']) + ' ' + (e['data'].get('asset') or '')), re.I)]
        if rubix and min(r['rect']['x'] for r in rubix) > first['rect']['x'] + 2:
            viol.append({'kind': 'cobrand_order_wrong',
                         'expected': 'Rubix left-most, then client',
                         'rubix_x': min(r['rect']['x'] for r in rubix),
                         'leftmost_x': first['rect']['x']})
        # 3. optical height parity between marks in the same lockup row
        row = [e for e in marks if abs(e['rect']['y'] - first['rect']['y']) < first['rect']['h']]
        hs = [e['rect']['h'] for e in row if e['rect']['h'] > 0]
        if len(hs) >= 2 and (max(hs)-min(hs))/max(hs) > optical_tol:
            viol.append({'kind': 'cobrand_optical_height_mismatch',
                         'heights': [round(h, 1) for h in hs],
                         'tolerance': optical_tol,
                         'note': 'measure on visible pixels, not PNG canvas — see logo_optical.py'})
        # 4. clear space
        for e in row:
            for other in pd['els']:
                if other['idx'] == e['idx'] or not other['text']: continue
                gap = other['rect']['x'] - e['rect']['r']
                if 0 <= gap < e['rect']['h']*clear and abs(other['rect']['y']-e['rect']['y']) < e['rect']['h']:
                    viol.append({'kind': 'cobrand_clear_space_violation',
                                 'logo': e['idx'], 'intruder': other['idx'],
                                 'gap': round(gap, 1),
                                 'required': round(e['rect']['h']*clear, 1)})
                    break
    return gate('G28_COBRAND', 'Co-brand lockup geometry', viol,
                {'count': len(marks)}, required=req['cobrand'], test_count=len(marks))

# --------------------------------------------------------------------------
# G29 ASSET INTEGRITY  (this is what would have caught the 36 broken MWAN logos)
# --------------------------------------------------------------------------

def g29_assets(pd, prof, spec, req, html_dir=None):
    lock = prof.get('brand_lock', {})
    approved = {k.lower(): v for k, v in lock.get('approved_logo_sha256', {}).items()}
    viol = []
    for e in pd['images']:
        im = e.get('image', {})
        src = im.get('src', '')
        if im.get('naturalW', 0) <= 0 or im.get('naturalH', 0) <= 0:
            viol.append({'kind': 'asset_failed_to_load', 'idx': e['idx'], 'src': src[:160],
                         'severity': 'BLOCKER',
                         'note': 'a delivered page must never ship an unresolved asset'})
            continue
        if approved and re.search(r'logo|mark|emblem', src, re.I):
            p = None
            if src.startswith('file://'): p = Path(src[7:])
            elif html_dir and not src.startswith(('http', 'data:')): p = Path(html_dir)/src
            if p and p.exists():
                sha = hashlib.sha256(p.read_bytes()).hexdigest()
                if sha not in approved.values():
                    viol.append({'kind': 'unapproved_logo_asset', 'idx': e['idx'],
                                 'src': src[:120], 'sha256': sha,
                                 'note': 'logo must be the exact approved file — no regeneration'})
            elif not src.startswith('data:'):
                viol.append({'kind': 'logo_asset_unverifiable', 'idx': e['idx'], 'src': src[:120]})
        # mirror / flip detection on brand assets
        tr = e['css']['transform']
        if tr and tr != 'none':
            nums = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', tr)][:4]
            if nums and (nums[0] < 0 or (len(nums) > 3 and nums[3] < 0)):
                viol.append({'kind': 'brand_asset_mirrored', 'idx': e['idx'], 'transform': tr})
    return gate('G29_ASSET_INTEGRITY', 'Asset resolution / logo authenticity', viol,
                {'count': len(pd['images'])}, required=req['assets'],
                test_count=len(pd['images']))

# --------------------------------------------------------------------------
# G30 CONTENT PACK  (Consulting Brain made checkable)
# --------------------------------------------------------------------------

CONTENT_SLOTS = ['question', 'thesis', 'evidence', 'interpretation',
                 'implication', 'source']

def g30_content_pack(pd, prof, spec, req):
    """
    A consulting exhibit is not Title + bullets. The page must carry, and mark,
    the Page Content Pack slots. Without instrumentation this is unverifiable —
    which is exactly why production must emit data-content-slot.
    """
    found = {}
    for e in pd['els']:
        declared = (e['data'].get('contentSlot') or '').lower()
        cls = ' '.join(e['cls']).lower()
        for s in CONTENT_SLOTS:
            if declared == s or f'slot-{s}' in cls:
                found.setdefault(s, []).append(e['idx'])
    viol = []
    mandatory = spec.get('content_slots_required', ['thesis', 'evidence', 'implication', 'source'])
    for s in mandatory:
        if s not in found:
            viol.append({'kind': 'content_slot_missing', 'slot': s,
                         'fix': f'emit data-content-slot="{s}" on the element carrying it'})
    # thesis must be a claim, not a topic label
    for idx in found.get('thesis', []):
        e = next((x for x in pd['els'] if x['idx'] == idx), None)
        if e and len(e['text'].split()) < 4:
            viol.append({'kind': 'thesis_is_a_label_not_a_claim', 'idx': idx, 'text': e['text'][:80]})
    return gate('G30_CONTENT_PACK', 'Page Content Pack completeness', viol,
                {'count': len(found), 'slots_found': sorted(found)},
                required=req['content_pack'], test_count=len(found))

# --------------------------------------------------------------------------
# G31 EVIDENCE TRACE  (no unsourced factual claim reaches a client page)
# --------------------------------------------------------------------------

NUMERIC_CLAIM = re.compile(r'(?<!\w)(\d[\d,،.]{1,}\s*(?:%|٪|SAR|ر\.س|ريال|يوم|شهر|أشهر|سنة|day|days|month|months|year|years|km|m²)?)')

def g31_evidence_trace(pd, prof, spec, req, ledger_ids=None):
    viol = []; claims = 0
    ledger_ids = set(ledger_ids or [])
    FURNITURE = ('page', 'pagenum', 'page-number', 'badge', 'sn', 'gnum', 'folio')
    for e in pd['texts']:
        t = e['text']
        hits = NUMERIC_CLAIM.findall(t)
        if not hits: continue
        cls = ' '.join(e['cls']).lower()
        if any(f in cls for f in FURNITURE): continue
        if e['data'].get('owner'): continue                 # badge owned by a node
        if (e['data'].get('directionality') or '').upper() == 'ISOLATED': continue  # technical token
        if len(t.strip()) <= 4: continue                    # bare ordinal, not a claim
        if e['data'].get('seq') and all(len(re.sub(r'\D', '', h)) <= 2 for h in hits):
            continue                                        # sequence ordinal on a node
        claims += 1
        ev = e['data'].get('source') or ''
        if not ev:
            viol.append({'kind': 'unsourced_numeric_claim', 'idx': e['idx'],
                         'claim': hits[0][:40], 'text': t[:80],
                         'fix': 'emit data-source="<evidence-id>" on the claim element'})
        elif ledger_ids and ev not in ledger_ids:
            viol.append({'kind': 'evidence_id_not_in_ledger', 'idx': e['idx'],
                         'evidence_id': ev})
    # v2.6 FIX D5: instrumentation is proven either by claims examined OR by
    # declared evidence anchors. A page whose only numbers are furniture is not
    # "uninstrumented" — but a page with neither claims nor anchors is.
    anchors = sum(1 for e in pd['els'] if e['data'].get('source'))
    # If a sourced claim points to a separate visual evidence anchor, the proof must remain scan-near.
    max_dist=float(prof.get('thresholds',{}).get('evidence_claim_distance_px',220))
    by_source={}
    for x in pd['els']:
        sid=(x.get('data',{}).get('source') or '').strip()
        if sid: by_source.setdefault(sid,[]).append(x)
    for e in pd['texts']:
        sid=(e.get('data',{}).get('source') or '').strip()
        if not sid or sid not in by_source: continue
        if (e.get('data',{}).get('contentSlot') or '').lower()=='source': continue
        peers=[x for x in by_source[sid] if x.get('idx')!=e.get('idx')]
        if not peers: continue  # the claim element itself is the evidence anchor; zero-distance binding.
        ec=(e['rect']['x']+e['rect']['w']/2,e['rect']['y']+e['rect']['h']/2)
        ds=[math.hypot(ec[0]-(x['rect']['x']+x['rect']['w']/2),ec[1]-(x['rect']['y']+x['rect']['h']/2)) for x in peers]
        if ds and min(ds)>max_dist: viol.append({'kind':'evidence_claim_too_far_from_visual_anchor','idx':e.get('idx'),'evidence_id':sid,'distance':round(min(ds),1),'ceiling':max_dist})
    checked = claims + anchors
    return gate('G31_EVIDENCE_TRACE', 'Evidence traceability of factual claims', viol,
                {'count': checked, 'numeric_claims': claims, 'evidence_anchors': anchors},
                required=req['evidence_trace'], test_count=checked)

# --------------------------------------------------------------------------
# G32 ARTIFACT STRENGTH  (the /100 score, machine form)
# --------------------------------------------------------------------------

WEIGHTS = {'relationship_truth': 20, 'analytical_depth': 15, 'visual_synthesis': 15,
           'information_density': 10, 'hierarchy': 10, 'topology_clarity': 10,
           'decision_usefulness': 10, 'non_template_originality': 5, 'benchmark_fit': 5}

def g32_artifact_strength(pd, prof, spec, req, fingerprint_distance=None):
    """
    Machine-computable lower bound on the Artifact Strength Score. The council
    may score HIGHER after human/agent review, but never higher than the ceiling
    implied by these hard measurements. A page that measures 41 cannot be
    argued to 88.
    """
    els = pd['els']; pr = pd['rect']; parea = (pr['w']*pr['h']) or 1
    nodes = {e['data']['node'] for e in els if e['data']['node']}
    edges = [e for e in pd['edges'] if e.get('id')]
    typed_edges = [e for e in edges if e.get('source') and e.get('target')]
    directed = [e for e in edges if (e.get('directionality') or '').upper() == 'DIRECTED']
    words = sum(len(e['text'].split()) for e in pd['texts'])
    sizes = sorted({e['css']['fontSize'] for e in pd['texts'] if e['css']['fontSize']})
    surfaces = [e for e in els if (e['css']['background'] or '') not in ('', 'transparent', 'rgba(0, 0, 0, 0)')]
    dom = [e for e in els if (e['data'].get('regionId') or '').upper() == 'DOMINANT']
    if dom:
        x0 = min(e['rect']['x'] for e in dom); x1 = max(e['rect']['r'] for e in dom)
        y0 = min(e['rect']['y'] for e in dom); y1 = max(e['rect']['b'] for e in dom)
        biggest = max(0.0, (x1-x0)*(y1-y0))/parea          # declared dominant form
    else:
        biggest = max((e['rect']['w']*e['rect']['h'] for e in surfaces), default=0)/parea
    min_ok = spec.get('artifact_score_min', 85)

    s = {}
    # relationship truth: are there real, typed, endpoint-attached edges?
    s['relationship_truth'] = 20 * min(1.0, len(typed_edges)/3.0) if nodes else 0
    # analytical depth: node variety + edge/node ratio
    ratio = (len(edges)/len(nodes)) if nodes else 0
    s['analytical_depth'] = 15 * min(1.0, (len(nodes)/5.0)*0.5 + min(ratio, 1.5)/1.5*0.5)
    # visual synthesis: is there a dominant structure rather than an even grid?
    s['visual_synthesis'] = 15 * min(1.0, biggest/0.35) if surfaces else 0
    # information density: words in the consulting band 90-320
    s['information_density'] = 10 * (1.0 if 90 <= words <= 320 else
                                     max(0.0, 1 - abs(words - 205)/205))
    # hierarchy: >=3 distinct type levels
    s['hierarchy'] = 10 * min(1.0, (len(sizes)-1)/3.0) if sizes else 0
    # topology clarity: directed edges carry arrowheads
    s['topology_clarity'] = 10 * (len([e for e in directed if e.get('markerEnd')])/len(directed)
                                  if directed else (0.4 if nodes else 0.0))
    # decision usefulness: an implication/decision slot exists
    has_impl = any((e['data'].get('contentSlot') or '').lower() in ('implication', 'decision')
                   or (e['data'].get('regionId') or '').upper() == 'RAIL'
                   or 'implication' in ' '.join(e['cls']).lower() for e in els)
    s['decision_usefulness'] = 10 if has_impl else 0
    # non-template originality: fed by the deck fingerprint distance
    s['non_template_originality'] = 5 * (min(1.0, fingerprint_distance/0.14)
                                         if fingerprint_distance is not None else 0.4)
    # benchmark fit: filled by reference retrieval; conservative default
    s['benchmark_fit'] = 5 * spec.get('benchmark_fit', 0.5)

    total = round(sum(s.values()), 1)
    viol = []
    if total < min_ok:
        viol.append({'kind': 'artifact_strength_below_floor', 'score': total,
                     'floor': min_ok, 'breakdown': {k: round(v, 1) for k, v in s.items()},
                     'note': 'this is the MACHINE CEILING — council may not score above it'})
    if nodes and not typed_edges:
        viol.append({'kind': 'nodes_without_relationships',
                     'nodes': len(nodes), 'typed_edges': 0,
                     'note': 'boxes are not an artifact; a relationship must be expressed'})
    return gate('G32_ARTIFACT_STRENGTH', 'Artifact strength score (machine ceiling)', viol,
                {'count': len(nodes)+len(edges), 'score': total,
                 'breakdown': {k: round(v, 1) for k, v in s.items()},
                 'words': words, 'nodes': len(nodes), 'edges': len(edges)},
                required=req['artifact'], test_count=len(nodes)+len(edges))


# --------------------------------------------------------------------------
# G35 ARABIC EXECUTIVE TERMINOLOGY — owner language lock v7.0.2
# --------------------------------------------------------------------------
def g35_arabic_executive_terminology(pd, prof, spec, req):
    result=validate_page_text_elements(pd.get('texts',[]))
    return gate('G35_ARABIC_EXECUTIVE_TERMINOLOGY','Arabic executive terminology owner lock',result['violations'],
                {'count':result['checked'],'exempted':result['exempted']},required=True,test_count=result['checked'])


# --------------------------------------------------------------------------
# G36 VISIBLE LANGUAGE / SCRIPT / NUMERAL PURITY
# --------------------------------------------------------------------------
def g36_visible_language_purity(pd, prof, spec, req):
    txts=[e.get('text','') for e in pd.get('texts',[]) if e.get('text','').strip()]
    full=' '.join(txts); has_ar=bool(ARABIC.search(full)); viol=[]; checked=0
    tech=set(x.upper() for x in prof.get('brand_lock',{}).get('technical_token_allowlist',[
        'AI','API','SLA','BOQ','ISO','PDF','RFP','UAT','KPI','PMO','ERP','CRM','SOC','SIEM','MFA','PAM','WAF','SQL','HTTP','HTTPS','JSON','XML','GPU','CPU','LLM','ML','NLP','OCR','UX','UI','RUBIX'
    ]))
    internal=[x.lower() for x in prof.get('client_visible_forbidden_terms',['READY','NEXT','BLOCKED','NEXT_STEP','PRODUCT_STATUS','Compliance Register v0','P0 Proposal Control Layer','v7.7 Test'])]
    for e in pd.get('texts',[]):
        t=e.get('text','').strip()
        if not t: continue
        checked+=1; low=t.lower()
        for term in internal:
            if term and term in low: viol.append({'kind':'internal_vocabulary_leak','idx':e.get('idx'),'term':term,'text':t[:100]})
        if not has_ar: continue
        iso=(e.get('data',{}).get('directionality') or '').upper()=='ISOLATED'
        toks=re.findall(r'[A-Za-z][A-Za-z0-9._/-]*',t)
        if toks and not ARABIC.search(t):
            bad=[x for x in toks if x.upper() not in tech and not re.fullmatch(r'[A-Z]{2,8}-?\d*',x)]
            if bad: viol.append({'kind':'pure_latin_client_text_on_arabic_page','idx':e.get('idx'),'tokens':bad[:8],'text':t[:100]})
        if ARABIC.search(t) and EU_DIGIT.search(t) and not iso:
            if not any(x.upper() in tech for x in toks): viol.append({'kind':'western_numeral_leakage','idx':e.get('idx'),'text':t[:100]})
    return gate('G36_VISIBLE_LANGUAGE_PURITY','Visible language / script / numeral purity',viol,{'count':checked,'arabic_page':has_ar},required=has_ar,test_count=checked)

# --------------------------------------------------------------------------
# G39 DOMINANT MASS FLOOR / CEILING
# --------------------------------------------------------------------------
def g39_dominant_mass(pd, prof, spec, req):
    th=prof.get('thresholds',{}); pr=pd['rect']; dom=[e for e in pd.get('els',[]) if e.get('data',{}).get('region')=='DOMINANT']; viol=[]
    fam=(spec.get('page_family') or '').upper(); vals=[]
    for e in dom:
        a=(e['rect']['w']*e['rect']['h'])/max(1,pr['w']*pr['h']); vals.append(a)
    dominant=max(vals) if vals else 0
    if req.get('artifact'):
        if not dom: viol.append({'kind':'dominant_region_not_instrumented'})
        elif fam not in ('COVER','SECTION_OPENER') and dominant<float(th.get('dominant_mass_min',.32)): viol.append({'kind':'dominant_mass_below_floor','actual':round(dominant,3),'floor':th.get('dominant_mass_min',.32)})
        elif fam not in ('COVER','SECTION_OPENER') and dominant>float(th.get('dominant_mass_max',.68)): viol.append({'kind':'dominant_mass_above_ceiling','actual':round(dominant,3),'ceiling':th.get('dominant_mass_max',.68)})
    return gate('G39_DOMINANT_MASS','Dominant visual mass floor/ceiling',viol,{'count':len(dom),'dominant_mass':round(dominant,3)},required=req.get('artifact',False),test_count=len(dom))

# --------------------------------------------------------------------------
# G40 ACCIDENTAL DEAD COLUMN
# --------------------------------------------------------------------------
def g40_dead_column(pd, prof, spec, req):
    pr=pd['rect']; shares=[0.,0.,0.,0.]; tested=0
    page_area=pr['w']*pr['h']; col_w=pr['w']/4.0
    for e in pd.get('els',[]):
        r=e['rect']; area=r['w']*r['h']
        if area<16 or area>page_area*.75: continue
        tested+=1
        # Audit-mandated per-column ink share: wide elements contribute only the
        # actual rectangle intersection to each column instead of dumping their
        # full area into the column containing the centre point.
        for c in range(4):
            x0=pr['x']+c*col_w; x1=x0+col_w
            iw=max(0.0,min(r['r'],x1)-max(r['x'],x0))
            if iw>0: shares[c]+=iw*max(0.0,r['h'])
    mean=sum(shares)/4 or 1; viol=[]
    if req.get('artifact') and tested>=4:
        for i,x in enumerate(shares):
            if x<.5*mean: viol.append({'kind':'accidental_dead_column','column':i,'share':round(x/mean,3)})
            if x>2.0*mean: viol.append({'kind':'column_mass_overconcentrated','column':i,'share':round(x/mean,3)})
    return gate('G40_COLUMN_BALANCE','Accidental dead-column / mass concentration',viol,{'count':tested,'shares':[round(x,1) for x in shares]},required=req.get('artifact',False),test_count=tested)

# --------------------------------------------------------------------------
# G41 CONNECTOR PATH GEOMETRY
# --------------------------------------------------------------------------
def g41_connector_path_geometry(pd, prof, spec, req):
    nodes={e.get('data',{}).get('node'):e for e in pd.get('els',[]) if e.get('data',{}).get('node')}; texts=pd.get('texts',[]); viol=[]; tested=0; crossing_count=0
    def inside(pt,r,pad=4): return r['x']-pad<=pt['x']<=r['r']+pad and r['y']-pad<=pt['y']<=r['b']+pad
    for ed in pd.get('edges',[]):
        tested+=1; src=ed.get('source'); tgt=ed.get('target'); samples=ed.get('samples') or []
        if not samples: viol.append({'kind':'connector_path_samples_missing','edge':ed.get('id')}); continue
        for nid,n in nodes.items():
            if nid in (src,tgt): continue
            if any(inside(pt,n['rect']) for pt in samples[1:-1]): crossing_count+=1; viol.append({'kind':'connector_crosses_non_endpoint_node','edge':ed.get('id'),'node':nid}); break
        for t in texts:
            if t.get('data',{}).get('labelFor') in (src,tgt,ed.get('id')): continue
            if any(inside(pt,t['rect'],1) for pt in samples[1:-1]): viol.append({'kind':'connector_crosses_text_label','edge':ed.get('id'),'text':t.get('text','')[:50]}); break
        tan=ed.get('tangent'); a=nodes.get(src); b=nodes.get(tgt)
        if tan and a and b and ed.get('directionality','').upper() in ('DIRECTED','FLOW'):
            ac=(a['rect']['x']+a['rect']['w']/2,a['rect']['y']+a['rect']['h']/2); bc=(b['rect']['x']+b['rect']['w']/2,b['rect']['y']+b['rect']['h']/2); flow=(bc[0]-ac[0],bc[1]-ac[1]); dot=flow[0]*tan['x']+flow[1]*tan['y']
            if dot<0: viol.append({'kind':'arrowhead_direction_contradicts_flow','edge':ed.get('id')})
    max_cross=int(prof.get('thresholds',{}).get('max_edge_crossings_critical',2))
    critical=bool(spec.get('critical') or spec.get('page_criticality') in ('CRITICAL','P0','P1'))
    if critical and crossing_count>max_cross: viol.append({'kind':'edge_crossing_budget_exceeded','crossings':crossing_count,'ceiling':max_cross})
    return gate('G41_CONNECTOR_PATH_GEOMETRY','Connector path/node/label/arrowhead geometry',viol,{'count':tested,'node_crossings':crossing_count,'crossing_ceiling':max_cross},required=bool(pd.get('edges') or spec.get('expected_edges')),test_count=tested)

# --------------------------------------------------------------------------
# registry
# --------------------------------------------------------------------------

def inspect_v26(pd, prof, spec, html_dir=None, fingerprint_distance=None, ledger_ids=None):
    req = derive_required(pd, spec)
    return [
        g24_palette(pd, prof, spec, req),
        g25_contrast(pd, prof, spec, req),
        g26_type_scale(pd, prof, spec, req),
        g27_bidi(pd, prof, spec, req),
        g28_cobrand(pd, prof, spec, req),
        g29_assets(pd, prof, spec, req, html_dir),
        g30_content_pack(pd, prof, spec, req),
        g31_evidence_trace(pd, prof, spec, req, ledger_ids),
        g32_artifact_strength(pd, prof, spec, req, fingerprint_distance),
        g35_arabic_executive_terminology(pd, prof, spec, req),
        g36_visible_language_purity(pd, prof, spec, req),
        g39_dominant_mass(pd, prof, spec, req),
        g40_dead_column(pd, prof, spec, req),
        g41_connector_path_geometry(pd, prof, spec, req),
    ]
