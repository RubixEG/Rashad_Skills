from __future__ import annotations
from pathlib import Path
import re

REQUIRED_MARKERS=(
    'data-page-id=', 'data-page-mode=', 'data-region-id="DOMINANT"',
)
FORBIDDEN_VISIBLE=(
    'READY','NEXT','BLOCKED','NEXT_STEP=','Compliance Register v0','P0 Proposal Control Layer','v7.7 Test'
)

def inspect_semantic_html_master(html_path, composition_spec:dict|None=None)->dict:
    p=Path(html_path or '')
    blockers=[]; warnings=[]
    if not p.exists(): return {'status':'BLOCKED','blockers':['SEMANTIC_HTML_MASTER_MISSING'],'warnings':[]}
    txt=p.read_text(encoding='utf-8',errors='ignore')
    for m in REQUIRED_MARKERS:
        if m not in txt: blockers.append('SEMANTIC_MASTER_INSTRUMENTATION_MISSING:'+m.split('=')[0])
    spec=dict(composition_spec or {})
    if not spec or (spec.get('validation') or {}).get('status')!='PASS': blockers.append('SEMANTIC_MASTER_COMPOSITION_SPEC_INVALID')
    mass=float(spec.get('dominant_mass_target',0) or 0)
    family=str(spec.get('page_family') or '')
    if family not in ('COVER','SECTION_OPENER') and not .32<=mass<=.68: blockers.append('SEMANTIC_MASTER_DOMINANT_MASS_OUT_OF_BAND')
    typo=spec.get('typographic_hierarchy') or spec.get('typography') or {}; levels=typo.get('levels') or []
    if len(levels)<3: blockers.append('SEMANTIC_MASTER_TYPE_HIERARCHY_BELOW_FLOOR')
    ns=spec.get('negative_space_zones') or spec.get('negative_space') or []
    if not ns: blockers.append('SEMANTIC_MASTER_NEGATIVE_SPACE_NOT_TYPED')
    # Do not flag data attributes/code declarations; flag only literal client-facing spans/text nodes crudely.
    visible=re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>',' ',txt,flags=re.I)
    visible=re.sub(r'<[^>]+>',' ',visible)
    visible=' '.join(visible.split())
    for token in FORBIDDEN_VISIBLE:
        if token.lower() in visible.lower(): blockers.append('SEMANTIC_MASTER_INTERNAL_VOCAB_VISIBLE:'+token)
    return {
        'status':'PASS' if not blockers else 'BLOCKED','html_master_path':str(p),
        'blockers':sorted(set(blockers)),'warnings':warnings,
        'measured_object_count':max(1,txt.count('data-node-id=')+txt.count('data-region-id=')),
        'composition_spec_sha256':spec.get('spec_sha256'),'rule':'Semantic master must be instrumented, composition-spec bound, quality-floor compliant and client-safe before pixel review.'
    }
