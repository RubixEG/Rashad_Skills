from __future__ import annotations
from .composition_spec import build_page_composition_spec
from .spec_divergence import evaluate_set

def build_composition_candidates(hypotheses,content_pack,graph,reference_grammar_ids=None):
    specs=[]
    for i,h in enumerate(hypotheses):
        s=build_page_composition_spec(h,content_pack,graph,variant_index=i,reference_grammar_ids=reference_grammar_ids)
        if s['validation']['status']!='PASS': return {'status':'BLOCKED','reason':'COMPOSITION_SPEC_INVALID','spec':s}
        specs.append(s)
    div=evaluate_set(specs)
    if div['status']!='PASS':
        # deterministic repair: rotate focal anchors by rebuilding with a large variant stride.
        specs=[build_page_composition_spec(h,content_pack,graph,variant_index=i+11,reference_grammar_ids=reference_grammar_ids) for i,h in enumerate(hypotheses)]
        div=evaluate_set(specs)
    return {'status':'PASS' if div['status']=='PASS' else 'BLOCKED','composition_specs':specs,'divergence':div,'count':len(specs)}
