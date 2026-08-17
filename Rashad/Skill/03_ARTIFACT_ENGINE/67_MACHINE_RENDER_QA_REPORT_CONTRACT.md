# Machine Render QA Report Contract

STATUS: REQUIRED PRODUCTION RECORD — v2.6.4.2

## Per-page record
A final-format render should produce a structured record containing at least:
- Page ID / format / source spec hash;
- gate status using `GATE_DEFINED | NOT_EXECUTED | PASS | FAIL | BLOCKED | N_A`;
- Margins PASS/FAIL;
- Overflow PASS/FAIL;
- Collision/Overlap PASS/FAIL;
- Typography PASS/FAIL;
- Font Preflight PASS/FAIL;
- RTL/Bidi PASS/FAIL;
- Directional Structure PASS/FAIL;
- Nodes `rendered/expected`;
- Edges `rendered/expected`;
- Images PASS/FAIL;
- Rubix Logo PASS/FAIL/NOT_APPLICABLE;
- Client Logo PASS/FAIL/NOT_APPLICABLE;
- Format Fidelity score where executed;
- Parity score where executed;
- Stress QA status;
- Council status;
- `RELEASE = PASS | BLOCKED`. Final `PASS` requires an execution `evidence_id`.

## Failure record
Every failure must include:
- exact zone/object/edge ID;
- root cause;
- severity;
- whether auto-repair is allowed;
- approved next action: `MICRO_FIX | RE_RENDER | REGENERATE | REDESIGN | RETURN_UPSTREAM`.

## Truthfulness
If the machine test was not run, report `NOT_EXECUTED`; never write an invented numeric fidelity score.


## v2.6.4.3 evidence invariant
See `07_GOVERNANCE_AND_QA/42_EVIDENCE_BACKED_GATE_STATUS_TAXONOMY.md`. Policy existence is `GATE_DEFINED`, not PASS.
