# Reverse Bid Calendar Schema — v2.2

Build backward from the verified submission deadline using local working-calendar assumptions recorded in the engagement.

Required gates: `SUBMISSION_UPLOAD`, `UPLOAD_BUFFER`, `FINAL_RELEASE`, `PRODUCTION_FREEZE`, `RED_TEAM`, `TRANSLATION_EDITORIAL_LOCK`, `PRICING_LOCK`, `CV_EVIDENCE_LOCK`, `CONTENT_FREEZE`, `CLARIFICATION_DEADLINE` when verified.

| Field | Required | Meaning |
|---|---|---|
| calendar_item_id | Yes | Stable ID |
| gate_or_task | Yes | Named gate/task |
| workstream | Yes | Owner workstream |
| owner | Yes | Accountable role/person when known |
| due_datetime | Yes or UNKNOWN | Exact local date/time |
| derivation_basis | Yes | RFP fact / approved assumption / derived offset |
| predecessor_ids | When applicable | Scheduling dependencies |
| buffer_days | When applicable | Explicit buffer |
| status | Yes | NOT_STARTED / DRAFT / REVIEW_REQUIRED / APPROVED / LOCKED / BLOCKED |
| escalation_trigger | Yes | When to escalate |

Never invent a submission date. Unknown dates stay `UNKNOWN`.
