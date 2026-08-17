from __future__ import annotations

def propagate_confidence(nodes):
    """nodes: {id:{confidence:0..1, depends_on:[ids]}}. Derived confidence cannot exceed weakest dependency."""
    out={}; visiting=set()
    def solve(k):
        if k in out: return out[k]
        if k in visiting: raise ValueError('CONFIDENCE_DEPENDENCY_CYCLE')
        if k not in nodes: raise KeyError(k)
        visiting.add(k); n=nodes[k]; own=float(n.get('confidence',1.0)); deps=n.get('depends_on',[])
        cap=min([solve(d)['effective_confidence'] for d in deps],default=1.0)
        eff=max(0.0,min(1.0,min(own,cap))); out[k]={'declared_confidence':own,'dependency_cap':cap,'effective_confidence':eff,'depends_on':list(deps),'capped':eff<own}
        visiting.remove(k); return out[k]
    for k in nodes: solve(k)
    return out
