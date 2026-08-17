# 30 — Operational Schemas & State Authority

STATUS: **HARD AUTHORITY — v2.5**

Purpose: make Rashad governance executable as persistent engagement objects instead of prose-only councils.

Canonical authorities:
- `07_GOVERNANCE_AND_QA/19_UNIFIED_STATE_MACHINE.md`
- `20_COMPLIANCE_REGISTER_SCHEMA.md`
- `21_COMPLIANCE_MATRIX_SCHEMA.md`
- `22_REVERSE_BID_CALENDAR_SCHEMA.md`
- `23_APPROVAL_LEDGER_SCHEMA.md`
- `24_COUNCIL_FINDING_LEDGER_SCHEMA.md`
- `25_DEPENDENCY_SCHEDULING_MODEL.md`
- `26_COUNCIL_SESSION_LEDGER_SCHEMA.md`

Hard rules:
1. Use one node-state vocabulary only.
2. Persist council findings and sessions in the Engagement State.
3. Approval is hash/version-specific; modification invalidates it.
4. Reader order is not a dependency.
5. Parallel work starts whenever dependency readiness permits.
6. No release while required blocking findings remain open.

## v2.3 artifact governance objects
Additional canonical schemas:
- `07_GOVERNANCE_AND_QA/27_ARTIFACT_INTENT_LEDGER_SCHEMA.md`
- `07_GOVERNANCE_AND_QA/28_VISUAL_BLUEPRINT_LEDGER_SCHEMA.md`

Hard rules:
7. Artifact Intent approval is version/hash-specific; modification invalidates dependent Visual Blueprint approval.
8. Visual Blueprint must reference the exact approved Artifact Intent hash before Geometry Handoff or production.

## v2.5 execution/product governance objects
Additional canonical schemas:
- `07_GOVERNANCE_AND_QA/29_GEOMETRY_HANDOFF_LEDGER_SCHEMA.md`
- `07_GOVERNANCE_AND_QA/30_ARCHETYPE_SELECTOR_DECISION_LEDGER_SCHEMA.md`
- `07_GOVERNANCE_AND_QA/31_PRODUCT_DELIVERY_COMPLETION_LEDGER_SCHEMA.md`
- `07_GOVERNANCE_AND_QA/32_CAPABILITY_PREFLIGHT_LEDGER_SCHEMA.md`

Hard rules:
9. Persist selector decisions; expert override requires rationale.
10. Geometry Handoff is a first-class ledgered node with version/hash/status/approval.
11. Artifact product completion is ledgered separately from content completion.
12. Capability Preflight must pass before production; generic render availability is insufficient.
