from __future__ import annotations

def attack_report(report: dict) -> dict:
    findings=[]
    if report.get("final_verdict") == "RELEASED":
        findings.append({"kind":"QA_AUTHORITY_ESCALATION","severity":"P0"})
    if report.get("production_release_authority") != "RASHAD_BRAIN_RELEASE_CHAIR":
        findings.append({"kind":"WRONG_PRODUCTION_RELEASE_AUTHORITY","severity":"P0"})
    inv=report.get("invocations",[])
    actors=[x.get("actor_id") for x in inv if x.get("status")=="PASS"]
    contexts=[x.get("isolated_context_id") for x in inv if x.get("status")=="PASS"]
    if len(actors)!=len(set(actors)):
        findings.append({"kind":"QA_ACTOR_REUSE","severity":"P1"})
    if len(contexts)!=len(set(contexts)):
        findings.append({"kind":"QA_CONTEXT_REUSE","severity":"P1"})
    required=set(report.get("required_councils",[])); executed=set(report.get("executed_councils",[]))
    missing=sorted(required-executed)
    if missing:
        findings.append({"kind":"QA_COUNCIL_COVERAGE_GAP","severity":"P1","missing":missing})
    return {"status":"PASS" if not findings else "FAIL","findings":findings}
