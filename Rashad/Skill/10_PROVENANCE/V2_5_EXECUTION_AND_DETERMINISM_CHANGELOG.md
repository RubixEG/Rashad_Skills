# V2.5 Execution & Determinism Changelog

## Why this release exists
Council review of V2.3/V2.4 identified a remaining authority-order conflict, nondeterministic archetype selection, duplicate artifact vocabularies, unledgered Geometry Handoff state, residual generic-renderer / text-free / logo-metric language, and a product-orchestration gap that allowed RFP Summary requests to stop at content or cover-image generation.

## Corrected
- current mandatory RFP structure now outranks house skeleton;
- deterministic relationship→archetype selector with scores/ties/composite resolution;
- canonical artifact intent/editability vocabulary;
- first-class Geometry Handoff ledger + stale propagation;
- provenance/geometry-based logo QA; strict text-free hero wording;
- Product Router and Registry;
- Product Delivery & Completion Contract;
- Capability Preflight and Tool Routing;
- Artifact Production Orchestrator;
- Release Completion Gate;
- Arabic cover image-left/native-text-right authority;
- no-stop-after-image gate;
- reader-order workflow regression test corrected.

## Non-goal
V2.5 does not bundle a PPTX/PDF composer. It makes the dependency explicit and prevents false completion/fallback when the runtime lacks one.
