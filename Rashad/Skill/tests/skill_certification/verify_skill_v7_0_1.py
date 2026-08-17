#!/usr/bin/env python3
from pathlib import Path
import json,re,hashlib,sys
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[2]
checks=[]
def ck(name,cond,detail=''):
 checks.append((name,bool(cond),detail));
def text(rel): return (ROOT/rel).read_text(encoding='utf-8')
def data(rel): return json.loads(text(rel))
# Identity/startup
ck('version_current_701','Current release: v7.0.1' in text('VERSION.md'))
for rel in ['SKILL.md','00_START_HERE.md','PROJECT_INSTRUCTIONS.md','00_CHAT_MIRROR_KERNEL/00_RASHAD_BOOTSTRAP.md','00_CHAT_MIRROR_KERNEL/24_VERSION_LAYER_RESOLUTION_AND_RETIREMENT_LEDGER.md']:
 ck('current_route_'+rel, 'v7.0.1' in text(rel), rel)
ck('start_no_candidate_exemption','unless explicitly exempted' not in text('00_START_HERE.md'))
ck('project_no_candidate_exemption','unless explicitly exempted' not in text('PROJECT_INSTRUCTIONS.md'))
# Manifest/mirror/hash targets exist
m=data('ACTIVE_AUTHORITY_MANIFEST.json')
ck('manifest_version',m['version']=='7.0.1')
ck('manifest_globals_exist',all((ROOT/p).is_file() for p in m['global_authorities']))
mirror=text('00_CHAT_MIRROR_KERNEL/53_V6_2_ACTIVE_AUTHORITY_REGISTRY.md')
ck('mirror_contains_all_globals',all(f'`{p}`' in mirror for p in m['global_authorities']))
# RFP role registry
rr=data('01_ACTIVE_RUNTIME/rfp_summary_role_registry_v7.json')
ck('rfp_role_count',len(rr['roles'])==24)
ck('rfp_sequence', [r['sequence'] for r in rr['roles']]==list(range(1,25)))
ck('rfp_depth_fields', all(r.get('required_analysis',{}).get('en') and r.get('evidence_requirements',{}).get('en') for r in rr['roles']))
# depth doc explicit fields 24/24
rd=text('01_ACTIVE_RUNTIME/40_RFP_SUMMARY_24_ROLE_DEPTH_CONTRACTS.md')
sections=re.split(r'(?=^## \d{2}\. )',rd,flags=re.M)[1:]
ck('role_depth_sections_24',len(sections)==24,str(len(sections)))
ck('role_depth_required_analysis_24',sum('**Required analysis:**' in s for s in sections)==24)
ck('role_depth_evidence_24',sum('**Evidence:**' in s for s in sections)==24)
# detailed product sequence
fp=text('01_ACTIVE_RUNTIME/22_RFP_SUMMARY_FINAL_PRODUCT_CONTRACT.md')
heads=[(int(n),h.strip()) for n,h in re.findall(r'^## (\d+)\. (.+)$',fp,flags=re.M) if int(n)>=17]
expected=[17,18,19,20,21,22,23,24]
ck('final_product_sequence_17_24',[n for n,_ in heads[:8]]==expected,str(heads[:9]))
ck('client_derivative_not_numbered', '## 24. Client-facing derivative' not in fp and '## Client-facing derivative — separate product' in fp)
# lens mapping
roles=set(re.findall(r'\| (ROLE-[A-Z0-9-]+) \|',text('01_ACTIVE_RUNTIME/09_COUNCILS_AND_ROLES.md')))
lr=data('01_ACTIVE_RUNTIME/council_lens_registry_v7_0_1.json')
ck('authorized_roles_29',len(roles)==29)
ck('lens_mapping_all_valid',all(set(x['authorized_runtime_role_ids'])<=roles for x in lr['lenses']))
router=data('01_ACTIVE_RUNTIME/council_of_councils_router_v7.json')
used=set()
for arr in router['role_families'].values(): used.update(arr)
for rdct in router['routing_by_rfp_role'].values():
 for arr in rdct.values(): used.update(arr)
registered={x['lens_id'] for x in lr['lenses']}
ck('router_all_lenses_registered',used==registered,f'used={len(used)} registered={len(registered)}')
# cognitive schema positive + negative validation
schema=data('schemas/consulting_cognitive_packet_v7.schema.json'); val=Draft202012Validator(schema)
valid={'page_id':'P01','role_id':'STRATEGIC_READING','management_question':'What does management need to know?','evaluator_question':'What must evaluator believe here?','decision_supported':'Bid strategy','answer_first_thesis':'The requirements form one operating system.','evidence_for':[{'claim':'Supported claim','source_ref':'SRC-ABC','locator':'p.1','confidence':0.9}],'evidence_against':[],'assumptions':[{'statement':'Assume access','impact':'affects schedule','validation_owner':'PM'}],'counterarguments':['Alternative interpretation exists'],'relationships':[{'source':'A','relation':'ENABLES','target':'B'}],'executive_implication':'Prioritize integration and governance.','council_route':[{'lens_id':'ENGAGEMENT_PARTNER','authorized_runtime_role_ids':['ROLE-PARTNER'],'challenge_question':'Is the thesis decision-relevant?','independence_required':False},{'lens_id':'SAUDI_GOVERNMENT_EVALUATOR','authorized_runtime_role_ids':['ROLE-PROCUREMENT','ROLE-REDTEAM','ROLE-SECTOR-SME'],'challenge_question':'Would this satisfy the evaluator?','independence_required':True},{'lens_id':'RED_TEAM_CHALLENGER','authorized_runtime_role_ids':['ROLE-REDTEAM'],'challenge_question':'What could make this wrong?','independence_required':True}]}
ck('cognitive_valid_packet',not list(val.iter_errors(valid)))
for name,mut in [('fake_role',{'role_id':'FAKE_ROLE'}),('fake_relation',{'relationships':[{'source':'A','relation':'MADE_UP_RELATION','target':'B'}]}),('fake_lens',{'council_route':[{'lens_id':'FAKE_LENS','authorized_runtime_role_ids':['ROLE-PARTNER'],'challenge_question':'This should definitely fail schema validation','independence_required':True}]*3})]:
 q=json.loads(json.dumps(valid)); q.update(mut); ck('cognitive_reject_'+name,bool(list(val.iter_errors(q))))
# QA taxonomy all detector fields
qa=data('07_GOVERNANCE_AND_QA/73_V7_VISUAL_AND_EXECUTIVE_FAILURE_TAXONOMY.json'); req=qa['detector_contract_fields']
ck('qa_count_233',len(qa['cases'])==233)
ck('qa_all_detector_fields',all(all(k in c and c[k] not in (None,'',[]) for k in req) for c in qa['cases']))
ck('qa_min_measured_positive',all(c['minimum_measured_objects']>=1 for c in qa['cases']))
ck('qa_truthful_not_implemented',all(c['implementation_status']=='SPECIFIED_NOT_IMPLEMENTED' for c in qa['cases']))
# current workflow
wf=text('05_WORKFLOW_ENGINE/02_RFP_SUMMARY.md')
ck('workflow_routes_23','23_V7_0_1_RFP_SUMMARY_DECISION_WORKFLOW.md' in wf)
ck('workflow_not_routes_17','executed through `17_A_TO_Z' not in wf)
# Decision schema structural
bd=data('schemas/rfp_bid_decision_evidence_v7_0_1.schema.json'); bv=Draft202012Validator(bd)
dims=bd['properties']['dimensions']['items']['properties']['dimension']['enum']
validd={'decision_id':'DEC-PILOT','recommendation':'GO_WITH_CONDITIONS','decision_method':'EVIDENCE_SYNTHESIS_NOT_AUTOMATIC_WEIGHTED_SCORE','management_approval_required':True,'dimensions':[{'dimension':x,'assessment':'MIXED','confidence':0.7,'rationale':'Evidence supports a mixed assessment.','evidence_refs':[{'source_ref':'SRC-ABC','locator':'p.1'}]} for x in dims],'conditions':['Close evidence gap'],'blockers':[],'required_actions':['Obtain management approval'],'counter_case':'The opportunity may be weaker if unresolved dependencies remain.','evidence_sufficiency':'PARTIAL_REQUIRES_CONDITIONS'}
ck('bid_decision_valid',not list(bv.iter_errors(validd)))
q=json.loads(json.dumps(validd)); q['conditions']=[]; ck('bid_decision_reject_conditionless',bool(list(bv.iter_errors(q))))
q=json.loads(json.dumps(validd)); q['decision_method']='AUTO_WEIGHTED_SCORE'; ck('bid_decision_reject_auto_formula',bool(list(bv.iter_errors(q))))
q=json.loads(json.dumps(validd)); q['dimensions'][1]['dimension']=q['dimensions'][0]['dimension']; ck('bid_decision_reject_duplicate_dimension',bool(list(bv.iter_errors(q))))
# authority binding and global authority hash integrity
bind=data('AUTHORITY_BINDING_CHECK.json'); bm=[]
for rel,h in bind.get('files',{}).items():
 pth=ROOT/rel
 if not pth.exists() or hashlib.sha256(pth.read_bytes()).hexdigest()!=h: bm.append(rel)
ck('authority_binding_hashes',not bm,str(bm[:5]))
gh=data('GLOBAL_AUTHORITY_HASHES.json'); gm=[]
for rel,h in gh.get('files',{}).items():
 pth=ROOT/rel
 if not pth.exists() or hashlib.sha256(pth.read_bytes()).hexdigest()!=h: gm.append(rel)
ck('global_authority_hashes',not gm,str(gm[:5]))
# protected corpus ledger verifies current bytes for every ledger entry
ph=data('PROTECTED_CORPUS_HASHES.json'); mism=[]
files=ph.get('files',{})
for rel,h in files.items():
 p=ROOT/rel
 if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=h: mism.append(rel)
ck('protected_corpus_hashes',not mism,str(mism[:5]))
# output
fail=[x for x in checks if not x[1]]
for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n,d)
print(f'SUMMARY {len(checks)-len(fail)}/{len(checks)} PASS')
sys.exit(1 if fail else 0)
