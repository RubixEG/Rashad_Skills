# Test 13 — Artifact-Preserving Layout Stress Test

## Objective
Prove that pages remain free of overflow and collision across HTML, PDF, and PowerPoint while retaining the approved artifact family, topology, focal point, evidence, and strength score.

## Required fixtures
Test at least one page from each family:
- cover/section opener;
- lifecycle or ordered sequence;
- output/dependency architecture;
- evaluation or weighted scoring;
- team responsibility matrix;
- evidence/submission package;
- cybersecurity/control lifecycle;
- contractual escalation;
- risk/clarification map;
- table or compliance page.

## Stress variants
For each fixture, render:
1. baseline approved Arabic copy;
2. title expanded by 25%;
3. body copy expanded by 20%;
4. mixed Arabic/English technical terms;
5. long government entity and competition names;
6. Arabic-Indic percentages and multi-digit values;
7. approved font metrics plus 8% width/height stress;
8. one additional evidence note;
9. PDF and PowerPoint export.

## Automated checks
- actual glyph rectangles inside component content boxes;
- no independent text-text or text-component intersections;
- title zone separated from body zone;
- body separated from footer;
- no `overflow:hidden`, clipping, ellipsis, negative-offset concealment, or whole-page scaling;
- numbers and percent signs contained;
- AR-SEQ-001 and AR-GRP-001 coordinates correct;
- PDFium and Poppler parity;
- PowerPoint-exported PDF parity;
- unresolved issue count equals zero.

## Artifact-preservation checks
- artifact family unchanged;
- semantic node count unchanged;
- semantic edge count unchanged;
- ordered sequence unchanged;
- evidence IDs unchanged;
- required visual asset retained;
- focal point retained;
- strength score after repair is not lower than before;
- generic-card share does not increase.

## Expected repair behavior
The test must demonstrate at least:
- one geometry-only repair;
- one editorial compression with semantic-diff approval;
- one two-page artifact-preserving continuation;
- one blocked repair that correctly escalates rather than downgrades.

## Pass condition
All formats pass, unresolved issue count is zero, and the Artifact Signature matches. Any safe-but-weaker result fails.
