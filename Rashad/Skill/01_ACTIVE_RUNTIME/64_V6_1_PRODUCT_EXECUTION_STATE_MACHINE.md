# V6.1 Product Execution State Machine

Allowed ordered states for a critical analytical page:
`INGESTED → CONTENT_LOCKED → GRAPH_LOCKED → ARTIFACT_TRUTH_PASS → EXHIBIT_SEARCH_COMPLETE → WINNER_LOCKED → VISUAL_SEARCH_COMPLETE → CEQS_PASS → PAGE_MASTER_LOCKED → PAGE_QA_PASS → EXPORT_PARITY_PASS → RELEASED`.

Rules:
- transitions are monotonic;
- a stage cannot be inferred from a later file;
- each transition records `page_id`, `evidence_id`, timestamp, input hashes, output hashes and authority;
- any changed upstream hash makes downstream stages stale;
- `RELEASED` is illegal until product-level Proof Index verifies all released pages.

Blocked statuses include:
`FAIL`, `BLOCKED`, `NOT_EXECUTED`, `FAIL_NOT_INSTRUMENTED`, `STALE_EVIDENCE`, `EXECUTION_CHAIN_BLOCK`, `VERSION_CONFLICT_BLOCK`.
