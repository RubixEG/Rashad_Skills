# ART-NR-001 Non-Regression Test Suite

## Test 1 — Safety fix preserves artifact family
Given a lifecycle page with overflow, the repaired page must remain a lifecycle or equivalent sequence artifact.
Fail if it becomes an equal-card grid without council approval.

## Test 2 — Golden benchmark score
Every critical page must record a prior approved benchmark and achieve the required score.
Fail if score < threshold or if a core dimension drops by more than 3 points.

## Test 3 — Card share
For a pack of 10+ pages, calculate the share of card-led pages.
Fail when card-led pages exceed 30% without documented content justification and council approval.

## Test 4 — Repetition
Fail when more than 2 consecutive pages use the same composition family.

## Test 5 — Relationship fidelity
Fail when:
- sequence becomes taxonomy cards;
- dependency becomes isolated boxes;
- governance becomes a list;
- escalation becomes equal cards;
- system/network becomes a table without a rationale.

## Test 6 — Unsupported quantitative encoding
Fail when bar length, color intensity, heat, maturity, or severity implies a quantitative comparison not supported by a source or approved scoring model.

## Test 7 — Narrative rhythm
For long packs, verify variation among:
- synthesis;
- diagnostic;
- relationship-led artifact;
- evidence or proof;
- decision/control page;
- narrative reset or section visual when valuable.

## Test 8 — Visual asset decision
Verify that the Visual Asset Decision Engine was called for every page.
The result may be "no asset required," but omission of the decision is a failure.

## Test 9 — Cross-format strength
HTML, PDF, and PPTX must preserve not only geometry but also the selected artifact family, focal point, hierarchy, and benchmark score.
