# 41 — Production Renderer Knowledge Contract

STATUS: HARD OPERATING CONTRACT — v2.6.4.2

## Purpose
Define the deterministic production renderer expected by Rashad without falsely claiming that the portable Markdown skill contains executable renderer code.

## Architecture boundary
Rashad has two coordinated layers:

### A. Rashad Skill / Knowledge
Owns:
- RFP and proposal intelligence;
- evidence and compliance reasoning;
- artifact intent and topology;
- visual-excellence decisions;
- page specification contracts;
- renderer requirements;
- QA and release governance.

### B. Production Renderer Runtime
Must implement:
- fixed canvas layout;
- direction resolution;
- deterministic geometry;
- text fit and font preflight;
- topology preservation;
- brand/asset preflight;
- HTML/PDF/PPTX adapters from one canonical scene graph;
- rasterized post-render inspection;
- visual/geometry/topology/directional parity;
- independent release QA.

## Compiler behavior
The runtime receives a locked Canonical Page Spec and must behave as a compiler, not a designer:

`Validate → Resolve Direction → Resolve Geometry → Compose → Render → Raster Inspect → Parity Check → Release/Block`

## Fixed-canvas requirement
Final presentation production resolves to explicit coordinates on an exact 16:9 canvas, normally equivalent to 1920×1080. Uncontrolled responsive reflow, auto-grid rearrangement, shrink-to-fit, and browser-dependent placement are prohibited in release geometry.

## Fail-closed outcomes
If the runtime cannot preserve topology or required directionality:
- do not simplify;
- do not hide content;
- do not silently shrink text;
- do not substitute another artifact family;
- return upstream with the exact blocking condition.

## Execution honesty
When an executable renderer or comparison engine is unavailable, record the relevant checks as `NOT_EXECUTABLE_IN_CURRENT_ENVIRONMENT` or `BLOCKED`; never claim machine PASS from policy knowledge alone.

## v2.6.4.10 timing clarification
Semantic Page Spec may exist before visual search, but final physical geometry and connector endpoints are frozen only after concept selection and initial HTML/SVG render critique.
