from pathlib import Path
import re,json
FILES=['SKILL.md','00_START_HERE.md','PROJECT_INSTRUCTIONS.md','00_CHAT_MIRROR_KERNEL/00_RASHAD_BOOTSTRAP.md','00_CHAT_MIRROR_KERNEL/02_CURRENT_AUTHORITY_GRAPH.md','00_CHAT_MIRROR_KERNEL/12_CONTEXT_ROUTER.md']
BANNED=[r'V5\.1.*HIGHEST CURRENT',r'Latest release:\s*\*\*v2',r'Version 4 highest production route',r'v4\.2.*highest current overlay']
def audit(skill):
 skill=Path(skill); errs=[]
 for rel in FILES:
  p=skill/rel
  if not p.exists(): errs.append({'file':rel,'kind':'missing_startup_file'}); continue
  txt=p.read_text(encoding='utf-8',errors='ignore')
  for pat in BANNED:
   if re.search(pat,txt,re.I): errs.append({'file':rel,'kind':'legacy_current_marker','pattern':pat})
 # exactly one current entrypoint phrase across startup files expected in SKILL only
 return {'status':'PASS' if not errs else 'FAIL','errors':errs}
if __name__=='__main__':
 import sys
 r=audit(sys.argv[1]);print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='PASS' else 1)
