# 29 — Geometry Handoff Ledger Schema

STATUS: **OPERATIONAL SCHEMA — v2.5**

| Field | Required | Meaning |
|---|---|---|
| contract_id | yes | Stable Geometry Handoff ID |
| artifact_id | yes | Parent Artifact Intent |
| visual_blueprint_id | yes | Parent Blueprint |
| version | yes | Contract version |
| source_visual_blueprint_hash | yes | Exact approved Blueprint dependency |
| status | yes | Canonical node state |
| council_session_id | yes for approval | Artifact/production review session |
| approval_id | yes for lock | Approval Ledger record |
| lock_hash | yes for lock | Hash of approved geometry contract |
| composer_requirements | yes | Required deterministic capabilities |
| capability_preflight_id | yes before production | Runtime capability decision |
| created_utc | yes | Creation timestamp |
| updated_utc | yes | Last update timestamp |

Any upstream Artifact Intent or Visual Blueprint hash change marks this record `STALE` automatically. Production requires `status=LOCKED` plus matching hashes and capability preflight PASS.
