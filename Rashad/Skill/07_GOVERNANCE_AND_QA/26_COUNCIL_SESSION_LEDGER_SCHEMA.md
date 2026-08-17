# Council Session Ledger Schema — v2.2

| Field | Required |
|---|---|
| council_session_id | Yes |
| council_id | Yes |
| object_id | Yes |
| activation_reason | Yes |
| required_role_ids | Yes |
| executed_role_ids | Yes |
| quorum_rule | Yes |
| quorum_result | Yes — PASS / FAIL |
| opened_at | Yes |
| closed_at | For closed session |
| blocking_findings_open | Yes |
| decision | Yes — PASS / FAIL / PASS_WITH_CONDITIONS / OPEN |
| decision_approver | When closed |
| notes | Optional |

Routing a role name without an executed finding/decision does not count in `executed_role_ids`.
