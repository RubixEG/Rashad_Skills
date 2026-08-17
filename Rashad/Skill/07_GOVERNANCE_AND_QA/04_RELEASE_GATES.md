# Release Gates

## Gate 1 — Source integrity
No drafting until all source files are indexed, readable, and classified. Missing annexes and contradictions are logged.

## Gate 2 — RFP understanding (`RFP-SUM-001`)
The summary must cover overview, scope, BOQ, team, evaluation, documents, contractual controls, cybersecurity, ambiguities, and official section mapping when present.

## Gate 3 — Bid strategy (`SEC-DEP-001` prerequisite)
Approve evaluator questions, issue tree, win themes, differentiation, proof plan, and commitment boundaries.

## Gate 4 — Section dependency and contract
Each section has an owner, evaluator purpose, requirements, claims, evidence, dependencies, forbidden duplication, and intended artifacts. Its status must be allowed by `SEC-DEP-001`.

## Gate 5 — Content and evidence
All claims are factual, inferred, assumed, or proposed—and clearly labeled internally. Unsupported claims are removed or qualified.

## Gate 6 — Artifact and visual-knowledge fitness
The visual relationship must match the information relationship. Generic cards cannot replace sequence, hierarchy, system, dependency, risk, or decision logic. Historical visual knowledge may influence production only as council-approved **abstract pattern intelligence** from an External Proposal Reference Session; exact old layouts/assets are never automatically reused.

## Gate 7 — Government readiness
Compliance, Arabic quality, legal/contractual obligations, cyber/data controls, acceptance, knowledge transfer, and client dependencies are explicit.

## Gate 8 — Renderer quality
No overflow, crop, hidden text, wrong numeral, wrong direction, wrong logo, font fallback, or uneditable flattening.

Every Arabic ordered page must pass AR-SEQ-001: the **first sequence item** begins top-right/rightmost, wrapped rows restart on the right, vertical paths move top-to-bottom, diagonal paths move top-right to bottom-left, and every produced representation preserves the same physical coordinates/reading order. Arabic client-facing semantic numerals use Arabic-Indic digits under `ARABIC_OUTPUT_NUMERAL_POLICY`; immutable technical/reference identifiers retain exact raw form. A violation is a hard fail with no silent waiver.

## Gate 9 — Red team
An independent simulated evaluator attempts to reject, downgrade, or challenge the proposal.

## Gate 10 — Final release
Critical pages score 92+, other pages 86+, overall 90+, awardability score reaches the approved threshold, and there are no hard fails.

## v7.6 Gate — Artifact Strength Non-Regression
After technical safety validation and before approval, every page and the section as a whole must pass ART-NR-001. A safe but generic or weaker artifact is a release failure.

## v7.7 Gate 0 — Test readiness
Before Gate 1 and before any render, TEST-GATE-001 must report PASS. Artifact Intent Contracts, benchmark coverage, cross-page diversity, visual-asset decisions, and renderer validation capability must be confirmed.

## v7.7 Gate — Artifact fallback lock
Any renderer change to an approved artifact family must be logged, re-scored, and council-approved under ART-LOCK-001. Silent downgrade is a hard fail.

## v7.8 Gate — Artifact-Preserving Layout Integrity
After Artifact Strength approval and before final release:
- the Artifact Signature is frozen and must match after repair;
- title, artifact body, and footer zones are measured and separated;
- glyph-level fit/collision validation passes;
- HTML, Chromium PDF, and PowerPoint-exported PDF each report zero unresolved issues;
- strength after repair is not lower than before;
- no generic-card fallback, visual-asset removal, topology loss, global scaling, clipping, or hidden overflow occurred;
- both the Artifact Architect and Proposal Artifact Integrity & Prepress Director approve.
## v2.6.4.1 Gate — Consulting Visual Excellence
Before Renderer Quality, each analytical page must pass `36_CONSULTING_VISUAL_EXCELLENCE_AND_MINISTRY_GATE.md`. Technical safety cannot compensate for weak consulting visual quality.

## v2.6.4.1 Gate — Rendering Stress QA & Parity
After render/export and before Red Team, each required representation must pass `35_RENDERING_STRESS_QA_AND_PARITY_GATE.md`. A file opening successfully is not proof of visual parity. Any unresolved overflow, overlap, clipping, topology loss, RTL/LTR error, brand corruption, crop drift, font drift or material cross-format mismatch blocks release.
