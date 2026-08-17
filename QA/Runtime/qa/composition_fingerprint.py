#!/usr/bin/env python3
"""
Rashad Anti-Template / Composition Repetition Detector  (Gate G26_ANTI_TEMPLATE)

Problem it solves: every page can individually PASS render QA while the DECK is
still a run of near-identical box grids. That reads as a student deck, not a
consulting deck. Individual-page QA is structurally blind to this.

Method: reduce each page to a COMPOSITION FINGERPRINT that captures the
*analytical shape* of the page, not its pixels:

  1. block extraction  - significant rectangles (>=0.8% of live area)
  2. grid signature    - inferred rows x cols from clustered x/y centres
  3. mass profile      - 4x4 ink-mass histogram of the live area
  4. topology signature- node/edge counts and edge-direction entropy
  5. focal signature   - normalised position + area share of the largest block
  6. rhythm signature  - distribution of block area (Gini) and size-mode count

Two pages are TEMPLATE-TWINS when their fingerprint distance is below tau.
The gate fails when template-twins appear within a sliding window, or when the
deck's distinct-composition ratio falls below the floor.
"""
from __future__ import annotations
import json, math, argparse
from pathlib import Path

# ---------- fingerprint construction ----------

def _cluster(vals, tol):
    """1-D single-link clustering; returns list of cluster means."""
    if not vals: return []
    vs = sorted(vals); out = [[vs[0]]]
    for v in vs[1:]:
        if v - out[-1][-1] <= tol: out[-1].append(v)
        else: out.append([v])
    return [sum(c)/len(c) for c in out]

def _gini(xs):
    if not xs: return 0.0
    xs = sorted(xs); n = len(xs); s = sum(xs)
    if s <= 0: return 0.0
    cum = sum((i+1)*x for i, x in enumerate(xs))
    return (2*cum)/(n*s) - (n+1)/n

def fingerprint(page):
    """page = {'w':..,'h':..,'blocks':[{'x','y','w','h'}..],
               'nodes':int,'edges':int,'edge_dirs':[deg,..]}"""
    W, H = float(page['w']), float(page['h'])
    area = W*H or 1.0
    blocks = [b for b in page.get('blocks', []) if (b['w']*b['h'])/area >= 0.008]

    # grid signature
    cx = [b['x']+b['w']/2 for b in blocks]
    cy = [b['y']+b['h']/2 for b in blocks]
    cols = len(_cluster(cx, W*0.05))
    rows = len(_cluster(cy, H*0.05))

    # 4x4 mass profile
    mass = [0.0]*16
    for b in blocks:
        gx = min(3, int(((b['x']+b['w']/2)/W)*4))
        gy = min(3, int(((b['y']+b['h']/2)/H)*4))
        mass[gy*4+gx] += (b['w']*b['h'])/area
    tot = sum(mass) or 1.0
    mass = [m/tot for m in mass]

    # focal signature
    if blocks:
        big = max(blocks, key=lambda b: b['w']*b['h'])
        focal = [(big['x']+big['w']/2)/W, (big['y']+big['h']/2)/H, (big['w']*big['h'])/area]
    else:
        focal = [0.5, 0.5, 0.0]

    # rhythm: how equal are the blocks? equal boxes == template smell
    areas = [(b['w']*b['h'])/area for b in blocks]
    sizes = [(round(b['w']/(W*0.04)), round(b['h']/(H*0.04))) for b in blocks]
    modal = max((sizes.count(s) for s in set(sizes)), default=0)
    rhythm = [_gini(areas), modal/max(1, len(blocks))]

    # topology
    n, e = int(page.get('nodes', 0)), int(page.get('edges', 0))
    dirs = page.get('edge_dirs', [])
    if dirs:
        buckets = [0]*8
        for d in dirs: buckets[int((d % 360)//45)] += 1
        p = [b/len(dirs) for b in buckets if b]
        ent = -sum(x*math.log(x, 2) for x in p)/3.0
    else:
        ent = 0.0
    topo = [min(n, 12)/12.0, min(e, 16)/16.0, ent]

    return {'grid': [min(rows, 6)/6.0, min(cols, 6)/6.0],
            'mass': mass, 'focal': focal, 'rhythm': rhythm, 'topo': topo,
            'raw': {'rows': rows, 'cols': cols, 'blocks': len(blocks),
                    'nodes': n, 'edges': e, 'modal_size_count': modal}}

# ---------- distance ----------
W_GRID, W_MASS, W_FOCAL, W_RHYTHM, W_TOPO = 0.28, 0.30, 0.14, 0.10, 0.18

def _l1(a, b): return sum(abs(x-y) for x, y in zip(a, b))/max(1, len(a))

def distance(fa, fb):
    return (W_GRID  * _l1(fa['grid'],   fb['grid'])   +
            W_MASS  * _l1(fa['mass'],   fb['mass'])   * 2.0 +
            W_FOCAL * _l1(fa['focal'],  fb['focal'])  +
            W_RHYTHM* _l1(fa['rhythm'], fb['rhythm']) +
            W_TOPO  * _l1(fa['topo'],   fb['topo']))

# ---------- gate ----------
def evaluate(pages, tau=0.085, window=4, distinct_floor=0.70,
             max_consecutive_twins=1):
    fps = [fingerprint(p) for p in pages]
    ids = [p.get('id', f'p{i+1}') for i, p in enumerate(pages)]
    viol, pairs = [], []
    for i in range(len(fps)):
        for j in range(i+1, min(i+1+window, len(fps))):
            d = distance(fps[i], fps[j])
            pairs.append({'a': ids[i], 'b': ids[j], 'distance': round(d, 4),
                          'twin': d < tau})
            if d < tau:
                viol.append({'kind': 'template_twin_pages', 'a': ids[i], 'b': ids[j],
                             'distance': round(d, 4), 'tau': tau,
                             'a_shape': fps[i]['raw'], 'b_shape': fps[j]['raw']})
    # consecutive run detection
    run = 0
    for i in range(len(fps)-1):
        if distance(fps[i], fps[i+1]) < tau:
            run += 1
            if run > max_consecutive_twins:
                viol.append({'kind': 'consecutive_template_run', 'at': ids[i+1],
                             'run_length': run+1})
        else:
            run = 0
    # deck distinctness
    uniq = 0
    for i in range(len(fps)):
        if all(distance(fps[i], fps[j]) >= tau for j in range(i)): uniq += 1
    ratio = uniq/max(1, len(fps))
    if ratio < distinct_floor:
        viol.append({'kind': 'deck_composition_monotony',
                     'distinct_ratio': round(ratio, 3), 'floor': distinct_floor})
    return {'gate': 'G26_ANTI_TEMPLATE', 'required': True,
            'test_count': len(fps),
            'status': 'FAIL' if (viol or len(fps) == 0) else 'PASS',
            'violations': viol if fps else [{'kind': 'FAIL_NOT_INSTRUMENTED',
                                             'gate': 'G26_ANTI_TEMPLATE'}],
            'measured': {'pages': len(fps), 'distinct_ratio': round(ratio, 3),
                         'shapes': [f['raw'] for f in fps]},
            'pairs': pairs}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pages_json', type=Path, help='[{id,w,h,blocks,nodes,edges,edge_dirs}]')
    ap.add_argument('--tau', type=float, default=0.085)
    ap.add_argument('--out', type=Path)
    a = ap.parse_args()
    res = evaluate(json.loads(a.pages_json.read_text()), tau=a.tau)
    txt = json.dumps(res, indent=2, ensure_ascii=False)
    if a.out: a.out.write_text(txt, encoding='utf-8')
    print(txt)
    raise SystemExit(0 if res['status'] == 'PASS' else 1)

if __name__ == '__main__': main()
