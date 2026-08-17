import re
from pathlib import Path

def analyse(skill_root):
    r=Path(skill_root)/'02_IMMUTABLE_AUTHORITIES/RETRIEVAL'
    allr=set(re.findall(r'R-(?:E\d{2}|\d{3})',(r/'R_CODE_INDEX.md').read_text(errors='ignore')))
    mapped=set()
    for p in (r/'MAPPINGS').glob('*.md'):mapped |= set(re.findall(r'R-(?:E\d{2}|\d{3})',p.read_text(errors='ignore')))
    return {'all':len(allr),'mapped':len(mapped),'direct_only':len(allr-mapped),'effective_reachable':len(allr),'direct_only_ids':sorted(allr-mapped)}
