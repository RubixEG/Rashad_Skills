#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from orchestrator import run_qa_brain, route
from provider import NoExecutionProvider, ScriptedIndependentTestProvider, QABrainProvider
from red_team import attack_report

results=[]
def add(name,ok,detail): results.append({"name":name,"status":"PASS" if ok else "FAIL","detail":detail})
ctx={"critical":True,"deck_level":True,"rendered":True,"language":"ar"}
det={"status":"PASS","final_verdict":"QA_CANDIDATE_PASS","measured":{"checks":233}}
rt=route(ctx)
add("route_has_13_councils_for_rendered_output",len(rt)==13,rt)
add("red_team_required","Q08_ADVERSARIAL_RED_TEAM" in rt,rt)
add("meta_qa_required","Q09_META_QA_INTEGRITY" in rt,rt)
add("actual_pixel_product_review_required","Q11_ACTUAL_PIXEL_PRODUCT_REVIEW" in rt,rt)
add("artifact_skeptic_required","Q12_EXECUTIVE_SIMPLICITY_ARTIFACT_SKEPTIC" in rt,rt)
add("delivery_integrity_council_required","Q13_DELIVERY_INTEGRITY_REPAIR_CLOSURE" in rt,rt)
gold=route({**ctx,"golden_acceptance":True})
add("golden_acceptance_council_required",len(gold)==14 and "Q14_GOLDEN_REAL_RFP_ACCEPTANCE" in gold,gold)
add("qa_candidate_chair_required","Q10_QA_RELEASE_CANDIDATE" in rt,rt)
no=run_qa_brain(ctx,det,provider=NoExecutionProvider())
add("no_provider_blocks",no.get("final_verdict")=="BLOCKED",no)
ok=run_qa_brain(ctx,det,provider=ScriptedIndependentTestProvider())
add("independent_test_provider_passes",ok.get("final_verdict")=="QA_CANDIDATE_PASS",{"verdict":ok.get("final_verdict"),"executed":ok.get("executed_councils")})
add("qa_never_releases",ok.get("final_verdict")!="RELEASED" and ok.get("qa_authority_ceiling")=="QA_CANDIDATE_PASS",ok.get("qa_authority_ceiling"))
add("all_councils_independent",all(x.get("independent") is True for x in ok.get("invocations",[])),[x.get("council_id") for x in ok.get("invocations",[])])
add("unique_actors",len({x.get("actor_id") for x in ok.get("invocations",[])})==len(ok.get("invocations",[])),None)
add("unique_contexts",len({x.get("isolated_context_id") for x in ok.get("invocations",[])})==len(ok.get("invocations",[])),None)
add("red_team_accepts_clean_candidate",attack_report(ok).get("status")=="PASS",attack_report(ok))
bad=dict(ok); bad["final_verdict"]="RELEASED"
add("red_team_blocks_qa_release_escalation",attack_report(bad).get("status")=="FAIL",attack_report(bad))
faildet=run_qa_brain(ctx,{"status":"FAIL"},provider=ScriptedIndependentTestProvider())
add("deterministic_fail_blocks_brain",faildet.get("final_verdict")=="BLOCKED",faildet)
out={"qa_brain":"1.3.0","status":"PASS" if all(x["status"]=="PASS" for x in results) else "FAIL","passed":sum(x["status"]=="PASS" for x in results),"total":len(results),"tests":results}
Path(__file__).with_name("QA_BRAIN_CERTIFICATION_RESULTS.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(out,ensure_ascii=False,indent=2))
raise SystemExit(0 if out["status"]=="PASS" else 1)
