# V7 — Total Quality Operating Model

**STATUS: CURRENT V7 QA AUTHORITY**

V7 unifies existing geometry, typography, RTL, brand, evidence, artifact, deck and release authorities through a machine-readable failure taxonomy rather than adding another prose-only checklist.

## QA layers
1. Text geometry
2. Component geometry and intentional hierarchy
3. Connector/edge truth
4. Artifact-family-specific QA
5. Arabic/RTL/BiDi/language
6. Typography/font readiness
7. Image and hero assets
8. Brand/co-brand
9. Data/evidence truth
10. Consulting/executive quality
11. Anti-card / anti-template quality
12. Cross-deck narrative/rhythm/diversity
13. Stress/chaos/metamorphic mutation
14. Multi-resolution/export parity
15. Non-destructive repair and QA-integrity

`73_V7_VISUAL_AND_EXECUTIVE_FAILURE_TAXONOMY.json` currently enumerates **233** known failure cases. `74_V7_ARTIFACT_FAMILY_QA_MATRIX.json` applies additional family-specific invariants. `75_V7_STRESS_CHAOS_AND_METAMORPHIC_MATRIX.json` attacks unknown edge cases.

## Consistency rule
"Everything equal" is not a quality rule. **Same semantic level → consistent geometry. Different strategic/decision/evidence importance → intentional hierarchy is allowed and often required.** QA blocks accidental inconsistency, not meaningful hierarchy.

## Runtime truthfulness
Each failure case is a specification until a detector is implemented and executed in the runtime. Static existence of this registry never equals PASS. Required detector returns must include measured objects, thresholds, evidence/master hashes and status; zero measured objects cannot PASS.

## Permanent learning loop
Every newly observed visual/content/release defect receives a stable failure ID and a **permanent regression fixture** (or child fixture) and is added to regression QA. Unknown failures are not a reason to claim completeness; they are actively searched through mutation and Red Team.

## v7.0.1 detector-spec closure
All 233 failure cases now carry implementation-grade detector contracts and are governed by `79_V7_0_1_QA_DETECTOR_IMPLEMENTATION_CONTRACT.md`. This closes specification ambiguity without falsely claiming runtime implementation.
