from __future__ import annotations
from brain.visual_search import generate_hypotheses

def build(graph, content_pack, reference_grammars=None):
    r=generate_hypotheses(graph,content_pack)
    if r.get('status')!='PASS': return r
    r['reference_grammar_ids']=(reference_grammars or [])[:3]
    pf=r.get('page_features',{}); r['visual_problem']=f"{pf.get('page_family','ANALYTICAL')} | {pf.get('node_count',0)} nodes | {pf.get('edge_count',0)} evidence-linked relationships"
    # Deliberately no winner here. A winner requires actual renders + independent visual judgment.
    r['winner']=None
    return r
