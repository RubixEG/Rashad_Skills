# Production Release Gate

STATUS: FINAL HARD PRODUCTION GATE — v2.6.4.2

## Definition of Done
Where the corresponding runtime capability is applicable and available, `RELEASED` requires:
- Content Validation PASS;
- Evidence Validation PASS;
- Artifact Validation PASS;
- Consulting Visual Excellence PASS;
- Canonical Page Spec LOCKED;
- Geometry Validation PASS;
- Typography/Text Fit PASS;
- Font Preflight PASS;
- RTL/Bidi PASS;
- Directional Structural Validation PASS;
- Brand/Asset Validation PASS;
- Overflow Validation PASS;
- Collision Validation PASS;
- Topology Validation PASS;
- required HTML regression/parity PASS;
- required PDF regression/parity PASS;
- required PPTX regression/parity PASS;
- Stress QA PASS;
- pre-render council PASS;
- post-render production council PASS;
- blocking findings = 0.

## Hard blockers
Any one of the following blocks release regardless of numeric score:
- missing node or edge;
- clipped connector/label/text;
- off-canvas content;
- unreadable overlap;
- missing text;
- silent font fallback causing geometry drift;
- wrong/distorted/mirrored logo;
- unjustified LTR structural flow on an Arabic ordered artifact;
- broken semantic sequence;
- artifact-family downgrade;
- cross-format material redesign.

## Runtime-unavailable behavior
Policy knowledge cannot fabricate machine results. If any required executable validation cannot run, record the gate as `NOT_EXECUTED` or `BLOCKED` under the evidence-backed status taxonomy. **Final client-facing production release is BLOCKED** until every required executable gate has evidence-backed PASS. Knowledge/governance approval may still be reported separately.

## v2.6.4.6 machine-stage semantics
`HTML_PREEXPORT_PASS` is a pre-export result only. Final machine evidence requires `PDF_PARITY_PASS`, `PPTX_PARITY_PASS`, and `DECK_CONTINUITY_PASS` in addition. Only the final evidence aggregation stage may emit machine `RELEASED`, and it remains subordinate to all applicable Rashad consulting/evidence/brand/release councils.
