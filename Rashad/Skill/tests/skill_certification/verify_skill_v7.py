#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,re,sys
root=Path(__file__).resolve().parents[2]
P=[];F=[]
def ok(name,cond,detail=''):(P if cond else F).append((name,detail))
def txt(rel):return (root/rel).read_text(encoding='utf-8',errors='ignore')
def js(rel):return json.loads(txt(rel))
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
man=js('ACTIVE_AUTHORITY_MANIFEST.json')
ok('version',man['version'].startswith('7.0'),man['version'])
ok('global_paths_unique',len(man['global_authorities'])==len(set(man['global_authorities'])))
ok('global_paths_exist',all((root/p).is_file() for p in man['global_authorities']))
reg=js('01_ACTIVE_RUNTIME/rfp_summary_role_registry_v7.json')
ok('rfp_role_count',reg['role_count']==24 and len(reg['roles'])==24)
ok('rfp_sequence', [r['sequence'] for r in reg['roles']]==list(range(1,25)))
ok('rfp_visible_names_nonempty',all(r['visible_name']['ar'] and r['visible_name']['en'] for r in reg['roles']))
ok('canonical_aliases',any('EVIDENCE_READINESS' in r['legacy_aliases'] for r in reg['roles'] if r['canonical_id']=='QUALIFICATION_READINESS'))
ok('monolingual_rule','decorative bilingual' in txt('SKILL.md').lower() and 'Arabic selected output' in txt('SKILL.md'))
ok('cognitive_schema', (root/'schemas/consulting_cognitive_packet_v7.schema.json').is_file())
c=js('01_ACTIVE_RUNTIME/council_of_councils_router_v7.json')
ok('conditional_council','Do not activate all roles' in c['principle'])
ok('management_decision_lenses',all(x in c['routing_by_rfp_role']['BID_DECISION']['producer_challenge_council'] for x in ['CEO_GM','CFO','COO']))
qa=js('07_GOVERNANCE_AND_QA/73_V7_VISUAL_AND_EXECUTIVE_FAILURE_TAXONOMY.json')
ok('qa_case_count',qa['case_count']>=200,qa['case_count'])
for cat in ['TXT','GEO','EDG','RTL','TYP','IMG','BRD','EVD','ART','DECK','QAI','STR']:
 ok('qa_category_'+cat,any(x['category']==cat for x in qa['cases']))
ok('family_matrix',js('07_GOVERNANCE_AND_QA/74_V7_ARTIFACT_FAMILY_QA_MATRIX.json')['family_count']>=20)
ok('stress_matrix',len(js('07_GOVERNANCE_AND_QA/75_V7_STRESS_CHAOS_AND_METAMORPHIC_MATRIX.json')['required_mutations'])>=20)
sk=txt('SKILL.md')
for phrase in ['exactly 5 materially different hypotheses','≥3 actual rendered candidates','Artifact Truth ≥90','CEQS ≥90','Producer-owned estimates have zero release authority']:
 ok('skill_lock_'+phrase,phrase in sk)
ok('cards_support','Cards are supporting surfaces only' in sk)
ok('art_overlay','does not replace the existing' in txt('03_ARTIFACT_ENGINE/142_V7_CONSULTING_INTELLIGENCE_BRAIN.md'))
ok('authors_fp','SINGLE_INTERNAL_AUTHOR_OR_OWNER_LIKELY' in txt('01_ACTIVE_RUNTIME/73_V7_RFP_AUTHORSHIP_FINGERPRINT_EXTENSION.md'))
ok('no_named_author_inference','Never identify a named advisor/person' in sk)
# Protected ledger remains valid
ph=js('PROTECTED_CORPUS_HASHES.json')
for rel,h in ph['files'].items():ok('protected:'+rel,(root/rel).is_file() and sha(root/rel)==h)
print(json.dumps({'version':man['version'],'passed':len(P),'failed':len(F),'failures':F},ensure_ascii=False,indent=2))
sys.exit(1 if F else 0)
