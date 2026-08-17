# Production Render Compiler Workflow

STATUS: ACTIVE ADDITIVE WORKFLOW — v2.6.4.2

## Entry condition
The page has passed the existing Artifact/Visual Excellence stage under v2.6.4.1.

## Workflow
1. Freeze approved Question, Thesis, Evidence, Relationship, Artifact Intent, Archetype and semantic topology.
2. Compile `Canonical Page Specification`.
3. Compile canonical scene graph with stable object/node/edge IDs.
4. Resolve page and zone direction policies.
5. Resolve logical START/END to physical geometry.
6. Recalculate connector endpoints after direction resolution.
7. Run deterministic geometry and collision preflight.
8. Run text-fit and font preflight.
9. Run brand/asset hash preflight.
10. Render one format adapter from the same scene graph.
11. Rasterize/inspect the final rendered output.
12. Run independent Stress QA and Artifact Integrity checks.
13. Compare required formats using Visual Regression / Parity.
14. Apply micro-repair only within approved limits; otherwise return upstream.
15. Record the Machine Render QA report.
16. Run Post-Render Production Council.
17. Release only through `70_PRODUCTION_RELEASE_GATE.md`.

## Critical RTL order
For Arabic sequential artifacts:
`Semantic Graph → Direction Resolution → Physical Node Geometry → Connector Rebuild → Render → Structural RTL QA`.

Do not render an LTR structure and mirror the finished page.

## No redesign rule
Format adapters project the same scene graph. They do not independently design HTML/PDF/PPTX.
## Repair / CI extension
Use `03_ARTIFACT_ENGINE/71_AUTO_REPAIR_AND_PAGE_SPLIT_POLICY.md` for repair limits and `07_GOVERNANCE_AND_QA/40_COUNCIL_TO_CI_GATE_MAPPING.md` to translate machine-verifiable council rules into implementation gates.
