# Approval Ledger Schema — v2.2

Every gate/lock/unlock/waiver requiring authority is recorded.

| Field | Required |
|---|---|
| approval_id | Yes |
| object_id | Yes |
| object_version_hash | Yes |
| decision | Yes — APPROVE / REJECT / APPROVE_WITH_CONDITIONS / WAIVE |
| approver_role | Yes |
| approver_identity | When known |
| decision_timestamp | Yes |
| conditions | When applicable |
| evidence_or_reason | Yes |
| supersedes_approval_id | When applicable |

Silence, “next”, or tool execution never counts as approval. Any material modification invalidates the prior object hash approval.
