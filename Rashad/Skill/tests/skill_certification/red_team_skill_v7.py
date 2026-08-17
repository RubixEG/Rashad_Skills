#!/usr/bin/env python3
from pathlib import Path
import json,sys,re
root=Path(__file__).resolve().parents[2]
def t(rel):return (root/rel).read_text(encoding='utf-8',errors='ignore')
def j(rel):return json.loads(t(rel))
att=[]
def a(name,cond,evidence):att.append({'attack':name,'result':'PASS' if cond else 'FAIL','evidence':evidence})
sk=t('SKILL.md'); lang=t('01_ACTIVE_RUNTIME/70_V7_MONOLINGUAL_OUTPUT_AND_NAMING_AUTHORITY.md'); arch=t('01_ACTIVE_RUNTIME/69_V7_RFP_SUMMARY_CANONICAL_DECISION_ARCHITECTURE.md'); art=t('03_ARTIFACT_ENGINE/142_V7_CONSULTING_INTELLIGENCE_BRAIN.md'); qa=j('07_GOVERNANCE_AND_QA/73_V7_VISUAL_AND_EXECUTIVE_FAILURE_TAXONOMY.json')
keys={x['key'] for x in qa['cases']}
# RFP product attacks
a('Model renames canonical RFP section', 'Do not invent or cosmetically rename' in arch,'canonical architecture')
a('Arabic summary adds English consulting subtitle', 'decorative bilingual' in lang.lower(),'language authority')
a('English summary adds decorative Arabic labels', 'English RFP / English selected output' in lang,'language authority')
a('RFP Summary changes to fixed 24 slides','physical page count is dynamic' in arch.lower(),'logical roles')
a('Model adds 25th flashy AI section','Exactly **24 logical roles**' in arch,'role count')
a('GM decision issued without evidence','The decision is evidence-backed' in arch,'decision contract')
a('Named consulting firm inferred as author','Never identify a named advisor/person' in sk,'authorship boundary')
a('Single internal author case impossible to represent','SINGLE_INTERNAL_AUTHOR_OR_OWNER_LIKELY' in t('01_ACTIVE_RUNTIME/73_V7_RFP_AUTHORSHIP_FINGERPRINT_EXTENSION.md'),'authorship extension')
# Council/cognition attacks
c=j('01_ACTIVE_RUNTIME/council_of_councils_router_v7.json')
a('All personas loaded on every page','Do not activate all roles' in c['principle'],'conditional routing')
a('CFO missing from commercial exposure','CFO' in c['routing_by_rfp_role']['COMMERCIAL_EXPOSURE']['producer_challenge_council'],'CFO route')
a('COO missing from delivery journey','COO' in c['routing_by_rfp_role']['DELIVERY_JOURNEY']['producer_challenge_council'],'COO route')
a('CEO missing from final bid decision','CEO_GM' in c['routing_by_rfp_role']['BID_DECISION']['producer_challenge_council'],'CEO route')
a('Producer skips management question','management_question' in j('schemas/consulting_cognitive_packet_v7.schema.json')['required'],'packet schema')
a('Producer omits counterargument','counterarguments' in j('schemas/consulting_cognitive_packet_v7.schema.json')['required'],'packet schema')
# Artifact attacks
a('Page type selects fixed template','never maps role name directly to a template' in art,'artifact brain')
a('Generic cards accepted','collection of boxes' in art and 'fails' in art,'consulting grade test')
a('Cards treated as page architecture','Cards are supporting surfaces only' in sk,'skill')
a('One rendered candidate accepted','≥3 actual rendered candidates' in sk,'render floor')
a('3-4 hypotheses accepted','exactly 5 materially different hypotheses' in sk,'hypothesis lock')
a('Producer self-scores release','Producer-owned estimates have zero release authority' in sk,'producer judge')
a('Repair deletes evidence','delete material evidence' in t('03_ARTIFACT_ENGINE/144_V7_EXECUTIVE_COMPRESSION_AND_ARTIFACT_SKEPTIC.md'),'compression law')
a('GP01 imperfect demo becomes fixed template','candidate exemplar only' in t('03_ARTIFACT_ENGINE/145_V7_GOLDEN_REFERENCE_GRAMMAR_CONTRACT.md'),'golden reference')
# QA attacks via registry
for attack,key in [
('Overflow hidden masks text','hidden_by_overflow'),('Floating arrow','floating_connector'),('Wrong connector endpoint','wrong_target_anchor'),('Card bigger accidentally','peer_height_mismatch'),('Intentional hierarchy incorrectly equalized','intentional_hierarchy_lost'),('Arabic RTL sequence reversed','rtl_sequence_inversion'),('Western numerals leak','western_numeral_leak'),('Long URL bidi break','url_bidi_break'),('Font fallback silently changes layout','silent_font_fallback'),('Text outside canvas','canvas_overflow'),('Card behind card/occlusion','occlusion'),('Off-canvas node','off_canvas_object'),('Opacity-zero node','opacity_hidden'),('Metadata-only edge','metadata_only_edge'),('White/hidden QA evasion','opacity_hidden'),('Generated text in hero','generated_text_pixels'),('Old client image','old_client_image'),('Wrong logo order','logo_order'),('Unsupported claim','unsupported_claim'),('Wrong BOQ quantity','boq_mismatch'),('Inference displayed as fact','inference_as_fact'),('Generic cards across deck','card_monotony'),('Same topology repeated','topology_monotony'),('Repair deletes node','repair_deletes_node'),('Tiny-font repair','repair_shrinks_unreadable'),('Fake PASS file','fake_pass_file'),('Zero measurement PASS','zero_measurement_pass'),('Stale screenshot','stale_screenshot'),('PDF/PPTX diverge','pdf_pptx_parity'),('Title x4 stress','title_x4'),('30-row table stress','table_30_rows'),('16-node graph stress','nodes_16')]: a(attack,key in keys,'QA taxonomy '+key)
# Unknown-failure learning
a('New unknown defect disappears after discovery','random_perturbation' in keys and 'permanent regression fixture' in t('07_GOVERNANCE_AND_QA/72_V7_TOTAL_QUALITY_OPERATING_MODEL.md'),'metamorphic learning')
# Runtime truthfulness
a('Static taxonomy claims detectors executed','never self-certify runtime QA execution' in sk.lower() or 'Missing runtime measurement' in sk,'truthfulness')
a('Skill claims code is already fixed','runtime detector implementation remains a separate code-remediation phase' in sk,'runtime boundary')
failed=[x for x in att if x['result']=='FAIL']
print(json.dumps({'version':(root/'VERSION.md').read_text(encoding='utf-8').split('Current release: v',1)[1].splitlines()[0].strip(),'attacks_run':len(att),'passed':len(att)-len(failed),'failed':len(failed),'attacks':att},ensure_ascii=False,indent=2));sys.exit(1 if failed else 0)
