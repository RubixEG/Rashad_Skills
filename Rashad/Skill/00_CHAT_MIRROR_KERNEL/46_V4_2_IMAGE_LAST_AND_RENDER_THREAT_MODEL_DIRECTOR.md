> **V6.2 SUPERSESSION BANNER — Specialist image-last/render-threat detail only; global HIGHEST authority claim is superseded by v6.2.**

# V4.2 Image-Last & Exhaustive Render Threat Model Director

STATUS: SPECIALIST LEGACY IMAGE-LAST / RENDER-THREAT DETAIL — NOT GLOBAL ROUTING AUTHORITY

## Image-last turn invariant
Image generation MUST be the last executable tool action in a conversational turn.
Before the image call, persist: product ID, page ID, Content Pack hash, approved visual concept, reference anchors, exact image brief, page family, expected topology, expected owner/anchor objects, QA spec, output asset slot, and `NEXT_STEP=ASSET_QA`.
The product remains `IN_PROGRESS`. The next turn resumes from saved state and must not redo accepted upstream decisions.

## Render threat model invariant
Do not maintain QA as a list of previously observed bugs. Treat every rendered object as a governed object with:
- geometry and bounds;
- typography / line fragments;
- parent, region, owner and anchor;
- padding / margin / spacing / alignment;
- layer / z-index / opacity / occlusion;
- transform / scale / rotation / clipping;
- direction / BiDi run behavior;
- semantic node / edge / label relationships;
- asset hash / aspect / crop behavior;
- stress mutation response;
- export projection behavior.

## No-vacuous-pass
A required gate that has zero instrumented/testable objects is a hard failure, not PASS.

## Pixel truth
DOM success is necessary but insufficient. Final page approval requires actual raster inspection and high-resolution master parity.

## Repair invariant
Safety repair may move/resize/reflow/split; it may not remove evidence, nodes, edges, labels, title meaning, source traceability, brand signature, direction semantics or consulting artifact strength.
