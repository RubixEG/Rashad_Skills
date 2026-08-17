#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from orchestrator import run_qa_brain, route
from provider import NoExecutionProvider, ScriptedIndependentTestProvider, OpenAIQAResponsesProvider
from red_team import attack_report

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def dump(p,o): Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding="utf-8")

def main():
    ap=argparse.ArgumentParser(description="Rashad Independent QA Brain v1.3 host-native capable")
    sub=ap.add_subparsers(dest="cmd",required=True)
    rr=sub.add_parser("route"); rr.add_argument("--context",required=True)
    run=sub.add_parser("run"); run.add_argument("--context",required=True); run.add_argument("--deterministic-report",required=True); run.add_argument("--out",required=True); run.add_argument("--test-provider",action="store_true"); run.add_argument("--execution-mode",choices=['AUTO','HOST_NATIVE_MODE','API_PROVIDER_MODE','OFFLINE_VALIDATION_MODE'],default='AUTO'); run.add_argument('--host-response-bundle'); run.add_argument('--host-name',default='HOST_MODEL')
    rt=sub.add_parser("red-team"); rt.add_argument("--report",required=True)
    a=ap.parse_args()
    if a.cmd=="route": print(json.dumps({"route":route(load(a.context))},indent=2)); return 0
    if a.cmd=="run":
        provider=ScriptedIndependentTestProvider() if a.test_provider else None
        bundle=load(a.host_response_bundle) if a.host_response_bundle else None
        r=run_qa_brain(load(a.context),load(a.deterministic_report),provider=provider,execution_mode=a.execution_mode,host_response_bundle=bundle,host_name=a.host_name); dump(a.out,r); print(json.dumps(r,ensure_ascii=False,indent=2));
        if r.get('provider_runtime',{}).get('pending_count'): return 4
        return 0 if r.get("status")=="PASS" else 2
    if a.cmd=="red-team":
        r=attack_report(load(a.report)); print(json.dumps(r,indent=2)); return 0 if r["status"]=="PASS" else 2
    return 1
if __name__=="__main__": raise SystemExit(main())
