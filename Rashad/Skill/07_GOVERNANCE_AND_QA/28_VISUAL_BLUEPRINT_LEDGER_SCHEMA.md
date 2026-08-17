# 28 — Visual Blueprint Ledger Schema

STATUS: OPERATIONAL SCHEMA — v2.5

| Field | Required | Meaning |
|---|---|---|
| blueprint_id | yes | Stable blueprint ID |
| artifact_id | yes | Parent Artifact Intent |
| artifact_intent_hash | yes | Exact approved intent dependency |
| version | yes | Blueprint version |
| selector_decision_id | yes | Deterministic selector dependency |
| editability_class | yes | FULLY_NATIVE / VECTOR_HYBRID / RASTER_AUGMENTED |
| geometry_contract_ref | yes before production | Geometry handoff object |
| page_direction | yes | RTL/LTR only; mixed content is recorded in directional_islands |
| directional_islands | conditional | zone-level LTR/RTL/PRESERVE islands; page-level MIXED is invalid |
| brand_asset_ids | yes for branded page | Exact current assets |
| image_brief_id | conditional | Only when image mode enabled |
| composer_requirements | yes | Native capabilities required |
| qa_assertions | yes | Release assertions |
| status | yes | Canonical state vocabulary |
| council_session_id | yes for approval | Review session |
| approval_id | yes for lock | Approval Ledger reference |
| lock_hash | yes for lock | Blueprint hash |

If the Artifact Intent hash changes, dependent blueprint becomes `STALE` automatically.
