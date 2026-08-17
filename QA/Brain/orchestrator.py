from __future__ import annotations
from pathlib import Path
import json, uuid
from provider import QAInvocation, NoExecutionProvider, resolve_qa_provider, provider_runtime_metadata

COUNCILS_PATH = Path(__file__).with_name("councils.json")
ALL_COUNCILS = [c["id"] for c in json.loads(COUNCILS_PATH.read_text(encoding="utf-8"))["councils"]]

PASS_LIKE = {
    "PASS", "HTML_PREEXPORT_PASS", "PARITY_PASS", "PRODUCT_PROOF_V41_BRAIN_PASS",
    "QA_CANDIDATE_PASS", "RELEASE_CANDIDATE_PASS"
}

def route(context: dict) -> list[str]:
    ordered = [
        "Q01_MECHANICAL_GEOMETRY",
        "Q02_EVIDENCE_EPISTEMIC",
        "Q03_ARTIFACT_SEMANTICS",
        "Q04_CONSULTING_VISUAL",
        "Q05_ARABIC_RTL_TYPOGRAPHY",
        "Q06_BRAND_PRODUCTION_EXPORT",
    ]
    if context.get("deck_level", True):
        ordered.append("Q07_CROSS_DECK_NARRATIVE")
    # Actual rendered product review is a distinct QA layer; framework certification is not product proof.
    if context.get("rendered", False) or context.get("user_visible", False):
        ordered += ["Q11_ACTUAL_PIXEL_PRODUCT_REVIEW", "Q12_EXECUTIVE_SIMPLICITY_ARTIFACT_SKEPTIC", "Q13_DELIVERY_INTEGRITY_REPAIR_CLOSURE"]
    if context.get("golden_acceptance", False):
        ordered.append("Q14_GOLDEN_REAL_RFP_ACCEPTANCE")
    ordered += ["Q08_ADVERSARIAL_RED_TEAM", "Q09_META_QA_INTEGRITY", "Q10_QA_RELEASE_CANDIDATE"]
    return ordered

def _id(prefix: str) -> str:
    return prefix + "-" + uuid.uuid4().hex[:16].upper()

def run_qa_brain(context: dict, deterministic_report: dict, producer_actor_ids: list[str] | None = None, provider=None, execution_mode='AUTO', host_invoke_fn=None, host_response_bundle=None, host_name='HOST_MODEL') -> dict:
    provider,resolution = resolve_qa_provider(provider,execution_mode=execution_mode,host_invoke_fn=host_invoke_fn,host_response_bundle=host_response_bundle,host_name=host_name)
    producer_actor_ids = set(producer_actor_ids or [])
    deterministic_status = deterministic_report.get("status") or deterministic_report.get("final_verdict") or deterministic_report.get("verdict")
    if deterministic_status not in PASS_LIKE:
        return {
            "status": "BLOCKED",
            "final_verdict": "BLOCKED",
            "reason": "DETERMINISTIC_QA_NOT_PASSED",
            "deterministic_status": deterministic_status,
            "production_release_authority": "RASHAD_BRAIN_RELEASE_CHAIR",
            "execution_mode_resolution": resolution, "provider_runtime": provider_runtime_metadata(provider),
        }

    required = route(context)
    invocations = []
    findings = []
    errors = []
    actor_ids = set()
    context_ids = set()

    for council_id in required:
        actor_id = _id("QA-ACTOR-" + council_id)
        context_id = _id("QA-CTX-" + council_id)
        function = "QA_RED_TEAM" if council_id == "Q08_ADVERSARIAL_RED_TEAM" else ("QA_META_REVIEW" if council_id == "Q09_META_QA_INTEGRITY" else ("QA_CANDIDATE_CHAIR" if council_id == "Q10_QA_RELEASE_CANDIDATE" else "QA_COUNCIL_REVIEW"))
        response = provider.invoke(QAInvocation(
            council_id=council_id,
            function=function,
            actor_id=actor_id,
            isolated_context_id=context_id,
            payload={"context": context, "deterministic_report": deterministic_report, "prior_findings": findings},
        ))
        invocations.append(response)
        if response.get("status") != "PASS":
            errors.append({"kind": "QA_COUNCIL_NOT_EXECUTED", "council_id": council_id, "status": response.get("status")})
            continue
        if response.get("independent") is not True:
            errors.append({"kind": "QA_COUNCIL_NOT_INDEPENDENT", "council_id": council_id})
        if response.get("previous_response_id"):
            errors.append({"kind": "QA_COUNCIL_CHAINED_TO_PRODUCER", "council_id": council_id})
        if response.get("actor_id") in producer_actor_ids:
            errors.append({"kind": "PRODUCER_QA_COLLISION", "council_id": council_id, "actor_id": response.get("actor_id")})
        if response.get("actor_id") in actor_ids:
            errors.append({"kind": "QA_ACTOR_REUSED", "actor_id": response.get("actor_id")})
        if response.get("isolated_context_id") in context_ids:
            errors.append({"kind": "QA_CONTEXT_REUSED", "isolated_context_id": response.get("isolated_context_id")})
        actor_ids.add(response.get("actor_id"))
        context_ids.add(response.get("isolated_context_id"))
        for f in response.get("findings", []):
            ff = dict(f)
            ff["council_id"] = council_id
            findings.append(ff)

    executed = {x.get("council_id") for x in invocations if x.get("status") == "PASS"}
    for council_id in required:
        if council_id not in executed:
            errors.append({"kind": "REQUIRED_QA_COUNCIL_MISSING", "council_id": council_id})
    open_high = [f for f in findings if str(f.get("severity", "")).upper() in {"P0", "P1", "CRITICAL", "HIGH"} and f.get("status") not in {"CLOSED", "RESOLVED", "NO_MATERIAL_OBJECTION"}]
    if open_high:
        errors.append({"kind": "OPEN_HIGH_QA_FINDINGS", "count": len(open_high)})

    # QA Brain may never issue production RELEASED. Its ceiling is QA_CANDIDATE_PASS.
    verdict = "QA_CANDIDATE_PASS" if not errors else "BLOCKED"
    return {
        "status": "PASS" if not errors else "FAIL",
        "final_verdict": verdict,
        "required_councils": required,
        "executed_councils": sorted(executed),
        "invocations": invocations,
        "findings": findings,
        "errors": errors,
        "production_release_authority": "RASHAD_BRAIN_RELEASE_CHAIR",
        "qa_authority_ceiling": "QA_CANDIDATE_PASS",
        "live_provider_status": "TEST_PROVIDER" if any(x.get("test_mode") for x in invocations) else "PRODUCTION_PROVIDER_OR_NONE",
        "execution_mode_resolution": resolution, "provider_runtime": provider_runtime_metadata(provider),
        "host_native_pending_requests": provider_runtime_metadata(provider).get("pending_requests",[]),
    }
