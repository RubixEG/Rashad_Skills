from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
REG=ROOT/'config/knowledge_registry.json'

def registry(): return json.loads(REG.read_text(encoding='utf-8'))

def _text(task):
    if isinstance(task,str): return task
    def flat(obj):
        if obj is None:return ''
        if isinstance(obj,str):return obj
        if isinstance(obj,(int,float,bool)):return str(obj)
        if isinstance(obj,dict):return ' '.join(flat(v) for v in obj.values())
        if isinstance(obj,(list,tuple,set)):return ' '.join(flat(v) for v in obj)
        return str(obj)
    return flat(task)

def detect_knowledge_needs(task):
    t=_text(task).lower(); needs=[]
    def add(pack,sme,trigger,required_output=None):
        if pack not in [x['knowledge_pack'] for x in needs]: needs.append({'knowledge_pack':pack,'sme':sme,'trigger':trigger,'required_output':required_output})
    patterns=[
      (r'\bsap\b','KP-SAP','SME-SAP','SAP','CERTIFIED_SAP_ARCHITECTURE'),
      (r'\bsalesforce\b','KP-SALESFORCE','SME-SALESFORCE','SALESFORCE','CERTIFIED_SALESFORCE_ARCHITECTURE'),
      (r'wcag|accessibil','KP-ACCESSIBILITY-WCAG','SME-ACCESSIBILITY','ACCESSIBILITY','CERTIFIED_ACCESSIBILITY_COMPLIANCE'),
      (r'finops|cloud cost|تكلفة السحابة','KP-CLOUD-COST','SME-FINOPS','CLOUD_FINOPS','CLOUD_COST'),
      (r'\bot\b|\bics\b|industrial control','KP-OT-ICS-SECURITY','SME-OT-ICS','OT_ICS','CERTIFIED_OT_SECURITY_ARCHITECTURE'),
      (r'fixed price|final price|sell price|margin|rate card|هامش|سعر نهائي|سعر ثابت','KP-FIRM-RATES','SME-PRICING','FIRM_RATES','FINAL_PRICE'),
      (r'cv|team capacity|resource capacity|staffing|جاهزية الفريق|السير الذاتية','KP-FIRM-CVS-CAPACITY','SME-DELIVERY','FIRM_CAPACITY','TEAM_READINESS_ASSERTION'),
      (r'case stud|similar project|مشاريع مشابهة|خبرات الشركة','KP-FIRM-CASE-STUDIES','SME-EVIDENCE','FIRM_CASE_STUDIES','SIMILAR_PROJECT_SCORE_ASSERTION'),
      (r'iso|certification|شهادات','KP-FIRM-CREDENTIALS','SME-EVIDENCE','FIRM_CREDENTIALS','CERTIFICATION_ASSERTION')]
    for pat,pack,sme,trig,out in patterns:
        if re.search(pat,t,re.I): add(pack,sme,trig,out)
    by={x['id']:x for x in registry()['knowledge_packs']}; routed=[]; blockers=[]
    for n in needs:
        p=by.get(n['knowledge_pack'],{'status':'KNOWLEDGE_REQUIRED','blocks':[]}); x=dict(n); x['knowledge_status']=p['status']; x['blocked_outputs']=p.get('blocks',[]); routed.append(x)
        if n.get('required_output') in p.get('blocks',[]) and p['status']!='AVAILABLE_VERIFIED': blockers.append({'knowledge_pack':n['knowledge_pack'],'required_output':n['required_output'],'status':p['status']})
    overall='READY' if not blockers else 'KNOWLEDGE_READINESS_BLOCK'
    return {'status':overall,'routed_expertise':routed,'blockers':blockers,'principle':'EXPERTISE_AVAILABILITY_NE_KNOWLEDGE_READINESS'}
