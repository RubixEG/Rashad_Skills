#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
sys.path.insert(0,str(Path(__file__).parent))
from brain.router import route
from brain.orchestrator import run_brain
from brain.provider import NoExecutionProvider,ScriptedTestProvider,OpenAIResponsesProvider
from brain.coverage import validate_session
from brain.release import final_release
from brain.utils import load,dump

def main():
 ap=argparse.ArgumentParser(description='Rashad Consulting Brain Runtime v3.4 bound to Skill v7.2'); sub=ap.add_subparsers(dest='cmd',required=True)
 r=sub.add_parser('route'); r.add_argument('--role',required=True); r.add_argument('--critical',action='store_true'); r.add_argument('--rendered',action='store_true'); r.add_argument('--deck',action='store_true')
 x=sub.add_parser('run'); x.add_argument('--task',required=True); x.add_argument('--out',required=True); x.add_argument('--test-provider',action='store_true'); x.add_argument('--openai-provider',action='store_true'); x.add_argument('--execution-mode',choices=['AUTO','HOST_NATIVE_MODE','API_PROVIDER_MODE','OFFLINE_VALIDATION_MODE'],default='AUTO'); x.add_argument('--host-response-bundle'); x.add_argument('--host-name',default='HOST_MODEL')
 v=sub.add_parser('validate'); v.add_argument('--session',required=True)
 rel=sub.add_parser('release'); rel.add_argument('--session',required=True); rel.add_argument('--qa-release-report',required=True); rel.add_argument('--out',required=True)
 a=ap.parse_args()
 if a.cmd=='route': print(json.dumps({'role':a.role,'route':route(a.role,a.critical,a.rendered,a.deck,False)},ensure_ascii=False,indent=2)); return 0
 if a.cmd=='run':
  provider=ScriptedTestProvider() if a.test_provider else (OpenAIResponsesProvider() if a.openai_provider else None)
  bundle=load(a.host_response_bundle) if a.host_response_bundle else None
  o=run_brain(load(a.task),provider=provider,execution_mode=a.execution_mode,host_response_bundle=bundle,host_name=a.host_name); dump(a.out,o); print(json.dumps(o,ensure_ascii=False,indent=2));
  if o.get('state')=='BLOCKED' and o.get('release',{}).get('reason')=='HOST_NATIVE_EXECUTION_PENDING': return 4
  return 0 if o.get('state')!='BLOCKED' else 2
 if a.cmd=='validate':
  o=validate_session(load(a.session)); print(json.dumps(o,ensure_ascii=False,indent=2)); return 0 if o['status']=='PASS' else 2
 if a.cmd=='release':
  o=final_release(load(a.session),load(a.qa_release_report)); dump(a.out,o); print(json.dumps(o,ensure_ascii=False,indent=2)); return 0 if o['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
