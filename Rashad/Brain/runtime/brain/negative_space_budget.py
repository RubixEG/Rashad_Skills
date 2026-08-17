from __future__ import annotations

def validate_negative_space(spec):
    zones=spec.get('negative_space_zones') or []; errs=[]
    for z in zones:
        b=z.get('bbox') or {}; area=float(b.get('w',0))*float(b.get('h',0))
        if z.get('type') not in {'BREATHING','SEPARATION','EMPHASIS_HALO','GUTTER'}: errs.append('UNTYPED_NEGATIVE_SPACE')
        if area<=0: errs.append('ZERO_AREA_NEGATIVE_SPACE')
    return {'status':'PASS' if zones and not errs else 'BLOCKED','errors':errs,'zone_count':len(zones)}
