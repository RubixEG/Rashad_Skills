from __future__ import annotations
import math
from brain.quality_floors_v7_3 import get as quality_floor

def _centroid(spec):
    b=spec.get('dominant_bbox') or {}; return (float(b.get('x',0))+float(b.get('w',0))/2,float(b.get('y',0))+float(b.get('h',0))/2)

def distance(a,b):
    score=0.0
    if a.get('dominant_form')!=b.get('dominant_form'): score+=.28
    if (a.get('focal_anchor') or {}).get('zone')!=(b.get('focal_anchor') or {}).get('zone'): score+=.18
    ax,ay=_centroid(a); bx,by=_centroid(b); score+=min(.22,math.hypot(ax-bx,ay-by)*.22/.5)
    score+=min(.12,abs(float(a.get('dominant_mass_target',0))-float(b.get('dominant_mass_target',0)))*.6)
    if (a.get('imagery') or {}).get('mode')!=(b.get('imagery') or {}).get('mode'): score+=.10
    if (a.get('communication_strategy') or '')!=(b.get('communication_strategy') or ''): score+=.10
    return round(min(1.0,score),4)

def evaluate_set(specs,min_pair=None,target_mean=None):
    min_pair=quality_floor('min_pairwise_structural_divergence_critical',.12) if min_pair is None else min_pair
    target_mean=quality_floor('target_pairwise_structural_divergence',.18) if target_mean is None else target_mean
    pairs=[]
    for i,a in enumerate(specs):
        for j,b in enumerate(specs[i+1:],i+1): pairs.append({'a':i,'b':j,'distance':distance(a,b)})
    vals=[p['distance'] for p in pairs]
    mn=min(vals) if vals else 0; mean=sum(vals)/len(vals) if vals else 0
    return {'status':'PASS' if vals and mn>=min_pair and mean>=target_mean else 'BLOCKED','min_pairwise':round(mn,4),'mean_pairwise':round(mean,4),'required_min':min_pair,'target_mean':target_mean,'pairs':pairs}
