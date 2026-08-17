# 42 — Production Release & Truthfulness Contract

STATUS: HARD RELEASE CONTRACT — v2.6.4.2

## Not sufficient for completion
None of the following proves production release:
- PDF file created;
- PPTX file created;
- HTML file created;
- file opens successfully;
- render command exits without error;
- visual inspection says "looks okay";
- written QA checklist exists;
- council policy is present in knowledge.

## Required release evidence
Where the corresponding runtime capability exists, completion requires evidence for:
- content/evidence validation;
- Consulting Visual Excellence;
- Canonical Page Spec lock;
- geometry validation;
- text-fit validation;
- font preflight;
- structural RTL/LTR validation;
- topology validation;
- brand/asset preflight;
- overflow/collision/clipping validation;
- format-specific render inspection;
- required parity thresholds;
- Stress QA;
- post-render council approval.

## Truth labels
Every QA claim must be one of:
- `PROVEN` — supported by actual runtime/test evidence;
- `VISUALLY_INSPECTED` — inspected from final rendered pixels but not machine-verified;
- `INFERRED` — reasoned from specification only;
- `NOT_EXECUTABLE_IN_CURRENT_ENVIRONMENT`;
- `BLOCKED`.

Never upgrade `INFERRED` or `VISUALLY_INSPECTED` to `PROVEN` without evidence.

## v2.6.4.3 evidence-backed statuses
Use `GATE_DEFINED | NOT_EXECUTED | PASS | FAIL | BLOCKED | N_A`. `PASS` is valid only with actual execution evidence (`evidence_id`). If any required renderer/parity/topology/directional/brand machine gate is unavailable or not executed, final production release is `BLOCKED`, while knowledge/governance readiness may be reported separately.
