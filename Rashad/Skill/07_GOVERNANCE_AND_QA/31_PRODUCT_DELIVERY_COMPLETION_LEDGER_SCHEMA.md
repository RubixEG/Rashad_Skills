# 31 — Product Delivery & Completion Ledger Schema

STATUS: OPERATIONAL SCHEMA — v2.5

| Field | Required | Meaning |
|---|---|---|
| delivery_contract_id | yes | Stable product contract instance |
| product_id | yes | Routed Rashad product |
| delivery_mode | yes | ARTIFACT / CONTENT / ARTIFACT_SPEC |
| product_state | yes | Canonical node state |
| required_stages | yes | Ordered mandatory stage IDs |
| completed_stages | yes | Completed stage IDs with evidence refs |
| blocked_stage | conditional | First unresolved mandatory stage |
| capability_preflight_id | conditional | Runtime capability result |
| final_artifact_refs | required for artifact completion | Released files/objects |
| release_gate | yes | NOT_RUN / PASS / FAIL / BLOCKED |
| completion_claim_allowed | yes | TRUE only when contract satisfied |
| approval_id | yes for release | Release approval |
