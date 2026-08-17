# Evidence-Backed Gate Status Taxonomy

STATUS: HARD TRUTHFULNESS AUTHORITY — v2.6.4.3

Machine-verifiable gates use only:
- `GATE_DEFINED` — policy/test exists but has not run in this environment;
- `NOT_EXECUTED` — execution was applicable but did not run;
- `PASS` — executed successfully and `evidence_id` exists;
- `FAIL` — executed and failed, with evidence;
- `BLOCKED` — required precondition/runtime unavailable or hard failure prevents release;
- `N_A` — genuinely not applicable.

## PASS invariant
`status=PASS` requires:
`executed=true` AND `evidence_id != null` AND `evidence_timestamp != null`.

Conceptual council-to-CI mappings must use `GATE_DEFINED`, never example PASS values that could be misread as executed evidence.

For final production release, any required gate in `GATE_DEFINED | NOT_EXECUTED | BLOCKED | FAIL` prevents `RELEASED`.

## v2.6.4.6 stage-verdict clarification
`N_A` is valid only when the compiled Page Spec proves the gate is genuinely irrelevant. HTML browser QA returns `HTML_PREEXPORT_PASS`; it must never return final `RELEASED`. Final release evidence aggregates HTML, PDF parity, PPTX parity and deck continuity results.
