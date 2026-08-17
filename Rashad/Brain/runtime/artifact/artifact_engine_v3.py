from __future__ import annotations
import itertools, math
from validation.schema_validator import validate_graph

RELATIONS={
'ENABLES':['STACK','HUB','SPINE','TREE'],'DEPENDS_ON':['SPINE','TREE','LADDER','MATRIX'],'FLOWS_TO':['SPINE','FUNNEL','LANE','RING'],'CONTROLS':['RING','BAND','LANE','TREE'],'MEASURES':['GAUGE','RAIL','MATRIX','FIELD'],'EVIDENCES':['RAIL','BAND','MATRIX'],'RISKS':['FIELD','MATRIX','RAIL','BAND'],'PRIORITIZES':['FIELD','FUNNEL','LADDER','MATRIX'],'OWNS':['LANE','TREE','STACK'],'APPROVES':['SPINE','LANE','LADDER'],'FEEDS_BACK':['RING','SPINE','LOOP'],'THRESHOLD_FOR':['GAUGE','FIELD','MATRIX'],'MAPS_TO':['MATRIX','LADDER','LANE'],'BLOCKS':['SPINE','LANE','FIELD']}
PRIMS={
'SPINE':('dominant',(3,9),'linear'),'RING':('dominant',(3,8),'cyclic'),'STACK':('dominant',(2,8),'vertical'),'HUB':('dominant',(3,9),'radial'),'LANE':('dominant',(2,10),'parallel'),'MATRIX':('dominant',(4,40),'bi-axial'),'TREE':('dominant',(4,20),'hierarchy'),'FUNNEL':('dominant',(3,8),'narrowing'),'FIELD':('dominant',(3,30),'positional'),'LADDER':('dominant',(3,12),'paired'),'BAND':('supporting',(1,12),'transverse'),'RAIL':('supporting',(1,10),'lateral'),'GAUGE':('supporting',(1,6),'scalar'),'LOOP':('modifier',(1,3),'return'),'ANCHOR':('modifier',(1,2),'focal'),'CARD':('surface',(1,12),'none')}
BANDS=[('AC-1',4,3,2),('AC-2',8,10,3),('AC-3',14,20,4),('AC-4',22,40,5),('AC-5',40,80,6)]

def signature(g):
    n=len(g['nodes']); es=g['edges']; rc={}
    deg={x['id']:0 for x in g['nodes']}
    for e in es:
        rc[e['relation']]=rc.get(e['relation'],0)+1;deg[e['source']]+=1;deg[e['target']]+=1
    cross=[k for k,d in deg.items() if n>3 and d>=.6*(n-1)]
    cyc='FEEDS_BACK' in rc
    maxdeg=max(deg.values()) if deg else 0
    if not es: topo='SET'
    elif cyc: topo='CYCLIC'
    elif maxdeg>=max(4,n*.5): topo='STAR'
    elif all(x<=2 for x in deg.values()): topo='CHAIN'
    else: topo='DAG'
    return {'n_nodes':n,'n_edges':len(es),'relations':rc,'topology':topo,'cross_cutting':cross,'has_feedback':'FEEDS_BACK'in rc,'has_governance':bool({'CONTROLS','OWNS'}&set(rc)),'has_decision':bool({'APPROVES','THRESHOLD_FOR','BLOCKS'}&set(rc))}

def band(sig):
    for name,nmax,emax,pmax in BANDS:
        if sig['n_nodes']<=nmax and sig['n_edges']<=emax:return name,pmax
    return 'AC-5',6

def coverage(prims,rels): return {r for r in rels if any(p in RELATIONS[r] for p in prims)}

def candidates(sig,maxc=5):
    rels=set(sig['relations']); b,pmax=band(sig)
    fit={'CHAIN':['SPINE','LADDER','FUNNEL'],'CYCLIC':['RING','SPINE','HUB'],'STAR':['HUB','RING','STACK'],'DAG':['LANE','MATRIX','SPINE','TREE'],'SET':['MATRIX','FIELD','STACK']}[sig['topology']]
    doms=fit+[p for p,v in PRIMS.items() if v[0]=='dominant' and p not in fit]
    out=[]
    supports=[p for p,v in PRIMS.items() if v[0]!='surface']
    for d in doms:
        base=[d]; missing=rels-coverage(base,rels)
        choices=[]
        # exact minimal set-cover search within complexity budget
        pool=[p for p in supports if p!=d]
        found=None
        for k in range(0,max(0,pmax-1)+1):
            for comb in itertools.combinations(pool,k):
                pp=base+list(comb)
                if sig['has_feedback'] and not ({'LOOP','RING'}&set(pp)): continue
                if sig['cross_cutting'] and not ({'BAND','RING','STACK','LANE'}&set(pp)): continue
                if rels<=coverage(pp,rels): found=pp; break
            if found:break
        if not found: continue
        # hard capacity sanity: dominant may exceed but not more than 1.6x upper bound
        lo,hi=PRIMS[d][1]
        if sig['n_nodes']>hi*1.6:continue
        key=(d,tuple(sorted(PRIMS[p][2] for p in found)))
        if any(x['key']==key for x in out):continue
        out.append({'key':key,'dominant':d,'primitives':found,'covered':sorted(coverage(found,rels)),'complexity_band':b,'max_primitives':pmax})
        if len(out)>=maxc:break
    return out

def truth_score(g,c):
    sig=signature(g); rels=set(sig['relations']); cov=len(set(c['covered']))/max(1,len(rels))
    evidence_ok=sum(bool(e.get('evidence')) for e in g['edges'])/max(1,len(g['edges']))
    topology=1.0 if cov==1 else cov
    cross=1.0 if (not sig['cross_cutting'] or {'BAND','RING','STACK','LANE'}&set(c['primitives'])) else 0
    fb=1.0 if (not sig['has_feedback'] or {'LOOP','RING'}&set(c['primitives'])) else 0
    decision=1.0 if (not sig['has_decision'] or any(p in c['primitives'] for p in ['SPINE','LANE','LADDER','GAUGE','FIELD'])) else .5
    complexity=1.0 if len(c['primitives'])<=c['max_primitives'] else 0
    completeness=1.0
    total=30*cov+15*evidence_ok+15*topology+10*cross+10*complexity+10*((fb+decision)/2)+10*completeness
    return round(total,1)

def run(g):
    errs=validate_graph(g)
    if errs:return {'status':'FAIL','gate':'GRAPH_INVALID','errors':errs,'candidates':[],'winner':None}
    sig=signature(g); cs=candidates(sig,5)
    for c in cs:c['artifact_truth_score']=truth_score(g,c)
    cs=sorted(cs,key=lambda x:-x['artifact_truth_score'])
    winner=cs[0] if cs else None
    ok=winner is not None and winner['artifact_truth_score']>=85 and len(winner['primitives'])<=winner['max_primitives']
    return {'status':'PASS' if ok else 'FAIL','gate':'ARTIFACT_TRUTH','signature':sig,'candidates':cs,'winner':winner}
