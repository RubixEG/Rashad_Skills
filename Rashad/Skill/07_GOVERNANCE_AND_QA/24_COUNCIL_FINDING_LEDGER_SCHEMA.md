# Council Finding Ledger Schema — v2.2

| Field | Required |
|---|---|
| finding_id | Yes |
| council_session_id | Yes |
| council_id | Yes |
| role_id | Yes |
| object_id | Yes |
| severity | Yes — CRITICAL / HIGH / MEDIUM / LOW / NOTE |
| blocking | Yes — TRUE / FALSE |
| finding | Yes |
| evidence_locator | For factual finding |
| owner | Yes |
| due_gate | Yes |
| due_date | When calendar supports it |
| status | Yes — OPEN / IN_REPAIR / CLOSED / ACCEPTED_RISK / SUPERSEDED |
| closure_evidence | For CLOSED |
| closure_approver | For CLOSED |
| closed_at | For CLOSED |

A governed gate cannot pass while a required blocking finding is OPEN or IN_REPAIR.
