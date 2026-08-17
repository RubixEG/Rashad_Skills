from __future__ import annotations
import hashlib,json

def deck_style_signature(spec):
    x={'palette':spec.get('palette_role_map'),'type':spec.get('typographic_hierarchy',{}).get('font_family'),'material':spec.get('material_plan')}
    return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:16]

def validate_style_convergence(specs):
    sigs=[deck_style_signature(s) for s in specs]; return {'status':'PASS' if len(set(sigs))<=2 else 'BLOCKED','distinct_style_signatures':len(set(sigs)),'signatures':sigs}
