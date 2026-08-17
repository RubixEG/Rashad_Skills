from __future__ import annotations

def resolve(spec,brand_profile=None):
    p=spec.get('palette_role_map') or {}; return {'status':'PASS','palette':p,'font_family':spec.get('typographic_hierarchy',{}).get('font_family'),'material':spec.get('material_plan'),'brand_profile':brand_profile or 'RUBIX_CURRENT'}
