#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys,subprocess,hashlib,time
sys.path.insert(0,str(Path(__file__).parent))
from validation.schema_validator import validate_graph,validate_schema,validate_firewall
from artifact.artifact_engine_v3 import run as artifact_run
from artifact.exhibit_engine import build as exhibit_build
from qa.unified_html_qa import run as html_run
from validation.execution_dossier import validate_product_index
from validation.execution_dossier_v4 import validate_product_index_v4
from validation.execution_dossier_v41 import validate_product_index_v41
from validation.proof_integrity_v4 import validate_proof_integrity
from qa_v4.taxonomy_runtime import taxonomy_audit,validate_case_results,validate_artifact_family
from qa_v4.stress_runner_final import validate_stress_evidence_final as validate_stress_evidence, run_stress_matrix
from validation.skill_binding_v4 import validate_skill_binding
from qa_v4.arabic_executive_terminology import validate_visible_text

def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(path,obj):Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def parity_run(masters,pdf,pptx,out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);here=Path(__file__).parent;reports={}
 for name,cand,fmt in [('pdf',pdf,'PDF'),('pptx',pptx,'PPTX')]:
  ev=out/name;ev.mkdir(exist_ok=True);cmd=[sys.executable,str(here/'qa/parity_qa.py'),'--reference',masters,'--candidate',cand,'--format-name',fmt,'--out',str(ev),'--mean-max','8','--pixel-ratio-max','0.08','--min-master-width','3840','--min-master-height','2160'];cp=subprocess.run(cmd,capture_output=True,text=True);files=list(ev.rglob('report.json'));reports[name]=load(files[-1]) if files else {'status':'NOT_EXECUTED','verdict':'BLOCKED','stderr':cp.stderr}
 ok=reports['pdf'].get('verdict')=='PDF_PARITY_PASS' and reports['pptx'].get('verdict')=='PPTX_PARITY_PASS';r={'status':'PASS' if ok else 'FAIL','verdict':'PARITY_PASS' if ok else 'BLOCKED','reports':reports};dump(out/'parity_report.json',r);return r

def main():
 ap=argparse.ArgumentParser(description='Rashad Unified QA Runtime v4.3 — Actual Product Inspection & Closed-Loop Delivery Lock')
 sub=ap.add_subparsers(dest='cmd',required=True)
 g=sub.add_parser('validate-graph');g.add_argument('graph')
 ar=sub.add_parser('artifact');ar.add_argument('graph')
 ex=sub.add_parser('exhibit');ex.add_argument('graph');ex.add_argument('--content-pack',required=True)
 h=sub.add_parser('html');h.add_argument('html');h.add_argument('--spec',required=True);h.add_argument('--graph');h.add_argument('--exhibit');h.add_argument('--profile',default=str(Path(__file__).parent/'config/profile_v4.json'));h.add_argument('--out',required=True);h.add_argument('--page-selector',default='.page');h.add_argument('--stress',action='store_true');h.add_argument('--evidence-ledger',required=True);h.add_argument('--repair-before')
 p=sub.add_parser('parity');p.add_argument('--masters',required=True);p.add_argument('--pdf',required=True);p.add_argument('--pptx',required=True);p.add_argument('--out',required=True)
 d=sub.add_parser('dossier');d.add_argument('proof_index');d.add_argument('--out',required=True)
 d4=sub.add_parser('dossier-v4');d4.add_argument('proof_index');d4.add_argument('--out',required=True)
 db=sub.add_parser('dossier-brain');db.add_argument('proof_index');db.add_argument('--out',required=True)
 tx=sub.add_parser('taxonomy-audit');tx.add_argument('--out')
 tc=sub.add_parser('total-cases');tc.add_argument('--results-dir',required=True);tc.add_argument('--applicability');tc.add_argument('--out',required=True)
 af=sub.add_parser('artifact-family');af.add_argument('--family',required=True);af.add_argument('--evidence',required=True);af.add_argument('--out')
 st=sub.add_parser('stress-v7-validate');st.add_argument('--evidence-dir',required=True);st.add_argument('--out',required=True)
 sr=sub.add_parser('stress-v7-run');sr.add_argument('--html',required=True);sr.add_argument('--out',required=True)
 pi=sub.add_parser('proof-integrity-v4');pi.add_argument('--product-root',required=True);pi.add_argument('--out',required=True)
 rp=sub.add_parser('release-product');rp.add_argument('--proof-index',required=True);rp.add_argument('--masters',required=True);rp.add_argument('--pdf',required=True);rp.add_argument('--pptx',required=True);rp.add_argument('--firewall',required=True);rp.add_argument('--out',required=True)
 term=sub.add_parser('arabic-visible-term');term.add_argument('--text',required=True);term.add_argument('--exception')
 r4=sub.add_parser('release-product-v4');r4.add_argument('--product-root',required=True);r4.add_argument('--proof-index',required=True);r4.add_argument('--masters',required=True);r4.add_argument('--pdf',required=True);r4.add_argument('--pptx',required=True);r4.add_argument('--firewall',required=True);r4.add_argument('--case-results',required=True);r4.add_argument('--stress-evidence',required=True);r4.add_argument('--skill-root',required=True);r4.add_argument('--out',required=True)
 a=ap.parse_args()
 if a.cmd=='validate-graph':
  e=validate_graph(load(a.graph));r={'status':'PASS' if not e else 'FAIL','errors':e};print(json.dumps(r,indent=2));return 0 if not e else 1
 if a.cmd=='artifact':
  r=artifact_run(load(a.graph));print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['status']=='PASS' else 1
 if a.cmd=='exhibit':
  r=exhibit_build(load(a.graph),load(a.content_pack),['CRG-04','CRG-05']);print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['status']=='PASS' else 1
 if a.cmd=='html':
  sp=load(a.spec);r=html_run(a.html,a.profile,sp,load(a.graph) if a.graph else None,load(a.exhibit) if a.exhibit else None,a.out,a.page_selector,a.stress,load(a.evidence_ledger),load(a.repair_before) if a.repair_before else None);print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['release_verdict']=='HTML_PREEXPORT_PASS' else 1
 if a.cmd=='parity':
  r=parity_run(a.masters,a.pdf,a.pptx,a.out);print(json.dumps(r,indent=2));return 0 if r['status']=='PASS' else 1
 if a.cmd=='dossier':
  r=validate_product_index(a.proof_index);Path(a.out).mkdir(parents=True,exist_ok=True);dump(Path(a.out)/'dossier_report.json',r);print(json.dumps(r,indent=2));return 0 if r['status']=='PASS' else 1
 if a.cmd=='dossier-v4':
  r=validate_product_index_v4(a.proof_index);Path(a.out).mkdir(parents=True,exist_ok=True);dump(Path(a.out)/'dossier_v4_report.json',r);print(json.dumps(r,indent=2));return 0 if r['status']=='PASS' else 1
 if a.cmd=='dossier-brain':
  r=validate_product_index_v41(a.proof_index);Path(a.out).mkdir(parents=True,exist_ok=True);dump(Path(a.out)/'dossier_brain_report.json',r);print(json.dumps(r,indent=2));return 0 if r['status']=='PASS' else 1
 if a.cmd=='taxonomy-audit':
  r=taxonomy_audit();
  if a.out: Path(a.out).mkdir(parents=True,exist_ok=True);dump(Path(a.out)/'taxonomy_audit.json',r)
  print(json.dumps(r,indent=2));return 0 if r['status']=='PASS' else 1
 if a.cmd=='total-cases':
  app=load(a.applicability) if a.applicability else None;r=validate_case_results(a.results_dir,app);Path(a.out).mkdir(parents=True,exist_ok=True);dump(Path(a.out)/'total_cases_report.json',r);print(json.dumps(r,indent=2));return 0 if r['status']=='PASS' else 1
 if a.cmd=='artifact-family':
  r=validate_artifact_family(a.family,a.evidence)
  if a.out:Path(a.out).mkdir(parents=True,exist_ok=True);dump(Path(a.out)/'artifact_family_report.json',r)
  print(json.dumps(r,indent=2));return 0 if r['status']=='PASS' else 1
 if a.cmd=='stress-v7-run':
  r=run_stress_matrix(a.html,a.out);print(json.dumps(r,indent=2));return 0 if r['status']=='PASS' else 1
 if a.cmd=='stress-v7-validate':
  r=validate_stress_evidence(a.evidence_dir);Path(a.out).mkdir(parents=True,exist_ok=True);dump(Path(a.out)/'stress_v7_report.json',r);print(json.dumps(r,indent=2));return 0 if r['status']=='PASS' else 1
 if a.cmd=='arabic-visible-term':
  r=validate_visible_text(a.text,a.exception);print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['status']=='PASS' else 1
 if a.cmd=='proof-integrity-v4':
  r=validate_proof_integrity(a.product_root);Path(a.out).mkdir(parents=True,exist_ok=True);dump(Path(a.out)/'proof_integrity_v4.json',r);print(json.dumps(r,indent=2));return 0 if r['status']=='PASS' else 1
 if a.cmd=='release-product':
  out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
  r={'release_scope':'LEGACY_V3_1_COMPAT','final_verdict':'BLOCKED','reason':'LEGACY_RELEASE_AUTHORITY_DISABLED_USE_BRAIN_RELEASE','production_release_authority':'RASHAD_BRAIN_RELEASE_CHAIR'}
  dump(out/'release_report.json',r);print(json.dumps(r,indent=2));return 2
 if a.cmd=='release-product-v4':
  out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
  d=validate_product_index_v4(a.proof_index);cases=validate_case_results(a.case_results);stress=validate_stress_evidence(a.stress_evidence);proof=validate_proof_integrity(a.product_root);skill=validate_skill_binding(a.skill_root);fwerr=validate_firewall(load(a.firewall));par=parity_run(a.masters,a.pdf,a.pptx,out/'parity')
  ok=all([d['status']=='PASS',cases['status']=='PASS',stress['status']=='PASS',proof['status']=='PASS',skill['status']=='PASS',not fwerr,par['status']=='PASS'])
  rid='REL4-'+hashlib.sha256((str(time.time())+json.dumps(d,sort_keys=True)).encode()).hexdigest()[:16].upper()
  r={'evidence_id':rid,'runtime':'4.3-actual-product-delivery-lock','dossier':d['verdict'],'total_quality_cases':cases['verdict'],'stress':stress['verdict'],'proof_integrity':proof['verdict'],'skill_binding':skill['verdict'],'firewall':'PASS' if not fwerr else 'FAIL','parity':par['verdict'],'final_verdict':'QA_CANDIDATE_PASS' if ok else 'BLOCKED','reports':{'dossier':d,'cases':cases,'stress':stress,'proof':proof,'skill':skill,'firewall_errors':fwerr,'parity':par}}
  r['production_release_authority']='RASHAD_BRAIN_RELEASE_CHAIR';dump(out/'release_report_v4.json',r);print(json.dumps(r,indent=2));return 0 if ok else 1
 return 1
if __name__=='__main__': raise SystemExit(main())
