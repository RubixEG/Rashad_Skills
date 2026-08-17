#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[2]
registry=json.loads((ROOT/'01_ACTIVE_RUNTIME/rfp_summary_role_registry_v7.json').read_text(encoding='utf-8'))
role16=[r for r in registry['roles'] if r['canonical_id']=='COMMERCIAL_EXPOSURE'][0]
assert role16['visible_name']['ar']=='الالتزامات والمخاطر التجارية والمالية'
assert role16['canonical_id']=='COMMERCIAL_EXPOSURE'
assert registry['prohibited_visible_terms_ar']==['التعرّض','التعرض']
assert len(registry['roles'])==24
assert [r['sequence'] for r in registry['roles']]==list(range(1,25))
for rel in ['01_ACTIVE_RUNTIME/22_RFP_SUMMARY_FINAL_PRODUCT_CONTRACT.md','01_ACTIVE_RUNTIME/33_ARABIC_VISIBLE_LANGUAGE_PURITY_GATE.md','01_ACTIVE_RUNTIME/69_V7_RFP_SUMMARY_CANONICAL_DECISION_ARCHITECTURE.md','01_ACTIVE_RUNTIME/76_V7_0_2_RFP_SUMMARY_EXECUTIVE_DECISION_DOSSIER_SKELETON.md']:
    txt=(ROOT/rel).read_text(encoding='utf-8')
    # visible-generation authorities must not contain the rejected unvocalized form after stripping explicitly governed law/test docs
    assert 'التعرض' not in txt, rel
print('PASS owner Arabic executive naming v7.0.2')
