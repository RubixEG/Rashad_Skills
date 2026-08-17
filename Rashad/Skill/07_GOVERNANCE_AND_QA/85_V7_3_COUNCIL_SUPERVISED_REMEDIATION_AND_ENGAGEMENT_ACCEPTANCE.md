# V7.3 Council-Supervised Remediation & Engagement Acceptance

**STATUS: CURRENT P0 QA / REMEDIATION AUTHORITY**

Every production defect and every remediation work package is governed by four independent layers:

`Implementer → Specialist Council → Adversarial Council → Engagement-File Acceptance`.

A work package cannot close from code presence, a fixture PASS, or the implementer's own score.

## Acceptance hierarchy
1. unit/contract evidence proves the component exists;
2. Specialist Council proves the intended capability is reachable;
3. Red Team proves known bypasses fail closed;
4. the actual engagement artifact is inspected in its delivered format and hash-bound.

`FINAL_VERIFY` fixture suites are system certification evidence only. They cannot substitute for engagement acceptance.

## Format-neutral product QA
PPTX and PDF are first-class delivered formats. Card-grid, monotony, typography, visible-language, mass and product-quality checks must operate through a format-neutral page model. Unknown deliverable formats fail rather than bypass inspection.

Instrumented HTML master QA and delivered-file QA are both required: HTML owns semantic gates; PDF/PPTX inspection owns what the client actually receives.

## Council monitoring
The remediation matrix assigns each audit finding to an owner council and a closure test. P0/P1 findings cannot be marked CLOSED unless machine evidence exists. Any regression reopens the finding automatically.

## Arabic output
Arabic visible-language purity, numeral policy, BiDi, co-brand geometry and PDF logical-text-layer integrity are release conditions. Internal runtime vocabulary may not render as client content.

## Stress
Metamorphic stress must render and regate mutated artifacts. A byte change alone is never a stress PASS. Repair-destructive mutation M19 must be `EXPECTED_BLOCK` / `REPAIR_SAFETY_FAIL`.
