from pathlib import Path
import hashlib,re,json

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def validate_skill_binding(skill_root):
    r=Path(skill_root); errors=[]; measured={}
    if not r.exists(): return {'status':'FAIL','errors':[{'kind':'skill_root_missing'}]}
    v=r/'VERSION.md'; s=r/'SKILL.md'
    if not v.exists() or not s.exists(): errors.append({'kind':'startup_authority_missing'})
    txt=v.read_text(encoding='utf-8',errors='replace') if v.exists() else ''
    if '7.0.2' not in txt: errors.append({'kind':'unexpected_skill_version','observed':txt[:100]})
    startup=['SKILL.md','00_START_HERE.md','PROJECT_INSTRUCTIONS.md']
    measured['startup_files_present']={x:(r/x).exists() for x in startup}
    if not all(measured['startup_files_present'].values()): errors.append({'kind':'current_startup_route_incomplete','files':measured['startup_files_present']})
    return {'status':'PASS' if not errors else 'FAIL','verdict':'SKILL_V7_0_2_BINDING_PASS' if not errors else 'BLOCKED','errors':errors,'measured':measured}
