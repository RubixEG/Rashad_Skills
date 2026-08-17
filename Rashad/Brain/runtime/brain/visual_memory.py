from __future__ import annotations
import hashlib,json

def _struct(obj):
    fa=obj.get('focal_anchor') or {}
    return {
      'dominant_form':obj.get('dominant_form'),
      'dominant_bbox':obj.get('dominant_bbox'),
      'focal_zone':fa.get('zone') or obj.get('focal_point'),
      'eye_path':obj.get('eye_path') or obj.get('reading_path'),
      'mass_plan':obj.get('mass_plan'),
      'imagery_mode':(obj.get('imagery') or {}).get('mode') if isinstance(obj.get('imagery'),dict) else None,
      'structural_signature':obj.get('structural_signature'),
    }

def fingerprint(obj):
    return hashlib.sha256(json.dumps(_struct(obj),sort_keys=True,separators=(',',':')).encode()).hexdigest()

def variety_check(current, history, max_consecutive_same=1, min_structural_distance=0.12):
    fp=fingerprint(current); hist=[fingerprint(x) for x in history]
    consecutive=0
    for x in reversed(hist):
        if x==fp: consecutive+=1
        else: break
    repeated=consecutive>=max_consecutive_same
    return {'status':'BLOCKED' if repeated else 'PASS','fingerprint':fp,'prior_consecutive_same':consecutive,'reason':'REPEATED_VISUAL_GRAMMAR' if repeated else None,'content_fields_excluded':True}
