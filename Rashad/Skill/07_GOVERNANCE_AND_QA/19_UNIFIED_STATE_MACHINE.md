# Unified State Machine — v2.2

STATUS: **HARD AUTHORITY — SINGLE STATE VOCABULARY**

## Engagement states
`NEW → INGESTING → FACT_BASE_READY → SUMMARY_DRAFT → SUMMARY_REVIEW → SUMMARY_APPROVED → BID_STRATEGY_ACTIVE → PROPOSAL_IN_PRODUCTION → RED_TEAM → PRODUCTION → RELEASE_READY → SUBMITTED`

Blocking engagement state: `HOLD`.

## Node/content states — canonical and exclusive
`NOT_STARTED | DRAFT | REVIEW_REQUIRED | APPROVED | LOCKED | STALE | BLOCKED | REJECTED | SUPERSEDED`

No other section/page/product state names are permitted in active runtime. Historic terms such as `CONTENT_DRAFT`, `VISUAL_DRAFT`, `READY_TO_DRAFT`, `IN_DRAFT`, `IN_REVIEW`, `CHANGES_REQUIRED`, `FINAL` are **superseded vocabulary**, not aliases to persist.

## Separate attributes — not states
- `READINESS`: `READY | NOT_READY` (derived from dependencies)
- `PRODUCTION_STAGE`: `CONTENT | ARTIFACT_SPEC | VISUAL_COMPOSITION | RELEASE`
- `RELEASE_GATE`: `NOT_RUN | PASS | FAIL | BLOCKED`
- `LOCK_SCOPE`: `NONE | CONTENT | ARTIFACT | VISUAL | FULL_NODE`

## Rules
- A material upstream change marks every dependent `APPROVED` or `LOCKED` node `STALE`.
- `LOCKED` means approved and frozen for the current gate; unlock requires an Approval Ledger record.
- `BLOCKED` means a required dependency, evidence item, council closure, or approval is absent.
- `REVIEW_REQUIRED` covers both review-in-progress and repair-required states; use `REPAIR_REQUIRED=true` when changes are mandatory.
- `REJECTED` cannot enter release.
- `SUPERSEDED` remains in provenance but is excluded from active runtime.
- A node is client-releaseable only when `STATE=LOCKED`, `PRODUCTION_STAGE=RELEASE`, `RELEASE_GATE=PASS`, and all dependent/council findings are closed.
