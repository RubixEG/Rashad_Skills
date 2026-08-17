# 30 — Archetype Selector Decision Ledger Schema

STATUS: OPERATIONAL SCHEMA — v2.5

Persist for every analytical artifact:
`selector_decision_id | artifact_id | dominant_relationship | secondary_relationship | candidate_scores | selected_archetype | composite_flag | confidence | tie_break_path | rejected_candidates | council_override | override_rationale | created_utc`

Council override is allowed only with recorded rationale and cannot choose a candidate rejected for semantic-node/edge loss, invented data, or mandatory-contract conflict.
