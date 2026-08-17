#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2]
rr=json.loads((ROOT/'01_ACTIVE_RUNTIME/rfp_summary_role_registry_v7.json').read_text(encoding='utf-8'))
role16=[r for r in rr['roles'] if r['canonical_id']=='COMMERCIAL_EXPOSURE'][0]
attacks=[
('visible_title_block','التعرّض التجاري والمالي' in (ROOT/'01_ACTIVE_RUNTIME/75_V7_0_2_OWNER_ARABIC_EXECUTIVE_TERMINOLOGY_AND_NAMING_LAW.md').read_text(encoding='utf-8')),
('visible_subsection_block','مصادر التعرّض' in (ROOT/'01_ACTIVE_RUNTIME/75_V7_0_2_OWNER_ARABIC_EXECUTIVE_TERMINOLOGY_AND_NAMING_LAW.md').read_text(encoding='utf-8')),
('internal_id_pass',role16['canonical_id']=='COMMERCIAL_EXPOSURE'),
('approved_default_pass',role16['visible_name']['ar']=='الالتزامات والمخاطر التجارية والمالية'),
('profitability_conditional',any(x['condition']=='ONLY_IF_PROFITABILITY_IMPLICATIONS_SUPPORTED' for x in role16['topic_adaptive_visible_title_ar'])),
('cfo_test_present',len(role16['cfo_language_test_ar'])==7),
]
for n,ok in attacks: print(('PASS' if ok else 'FAIL'),n)
sys.exit(0 if all(ok for _,ok in attacks) else 1)
