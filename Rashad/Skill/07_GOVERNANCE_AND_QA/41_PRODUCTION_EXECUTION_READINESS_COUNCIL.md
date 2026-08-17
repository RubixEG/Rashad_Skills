# Production Execution Readiness Council

STATUS: INTEGRATION / RELEASE-GOVERNANCE COUNCIL — v2.6.4.3

## Seats
Consulting Partner; Rashad Product Architect; Proposal Director; Artifact Intelligence Director; Visual Benchmark Director; Rendering Architecture Lead; Image Generation Isolation Lead; RTL/BiDi & Directional Layout Lead; Typography/Prepress Lead; Topology/Connector Lead; Brand Governor; QA/Regression Lead; Evidence/Truthfulness Auditor; Non-Regression Auditor.

## Mandatory questions
1. Can a generic image/slide/document tool still be mistaken for production capability?
2. Can an image model receive enough context to infer/recreate a final slide when only an asset is requested?
3. Can a generated logo/text/slide-like image enter production?
4. Is page-level MIXED direction eliminated?
5. Are BiDi neutral punctuation and LTR islands specified across formats?
6. Are connector source/target/arrowhead/anchors deterministic after direction resolution?
7. Is co-brand override precedence singular and unambiguous?
8. Is optical logo matching measurable?
9. Are external appendix/source dependencies explicitly labeled rather than appearing as missing bundled files?
10. Can policy documentation ever produce a machine PASS without evidence?
11. Does missing required runtime evidence block final production release?

## Verdict vocabulary
- `GO — KNOWLEDGE/GOVERNANCE RELEASE`
- `GO WITH CONDITIONS`
- `NO-GO`

Executable production readiness is reported separately and may remain `NOT_BUNDLED / BLOCKED` even when the knowledge/governance release is GO.

## v2.6.4.7 added council check
Can the current task achieve the approved concept through the default HTML/SVG/CSS master route? If yes, use that route. If not, and visual fidelity would otherwise be materially lost, the council may authorize GVM fallback. In either case, generic native-card reconstruction is not an acceptable downgrade.
