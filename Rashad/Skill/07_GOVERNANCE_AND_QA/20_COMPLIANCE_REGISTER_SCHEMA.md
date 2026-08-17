# Compliance Register Schema — v2.2

One row per atomic obligation.

| Field | Required | Meaning |
|---|---|---|
| requirement_id | Yes | Stable engagement-local ID |
| source_file | Yes | Exact source |
| source_locator | Yes | Page/section/line |
| requirement_text | Yes | Faithful atomic requirement |
| requirement_type | Yes | TECHNICAL / ADMIN / TEAM / LEGAL / CYBER / COMMERCIAL / SUBMISSION / OTHER |
| mandatory_level | Yes | MANDATORY / SCORED / INFORMATIONAL / UNKNOWN |
| evaluator_criterion | When applicable | Criterion/weight link |
| proposal_response_owner | Yes | Workstream/role owner |
| response_location | Later | Section/page/artifact locator |
| evidence_required | Yes | Evidence needed |
| evidence_status | Yes | AVAILABLE / GAP / NOT_APPLICABLE / UNKNOWN |
| compliance_status | Yes | OPEN / COMPLIANT / PARTIAL / NON_COMPLIANT / BLOCKED |
| dependency_ids | When applicable | Linked dependencies |
| clarification_id | When applicable | Material clarification |
| risk_id | When applicable | Exposure if unresolved |
| approver | For closure | Closure authority |

Hard gate: no final Compliance Matrix row may exist without a source locator and a mapped proposal response/evidence disposition.
