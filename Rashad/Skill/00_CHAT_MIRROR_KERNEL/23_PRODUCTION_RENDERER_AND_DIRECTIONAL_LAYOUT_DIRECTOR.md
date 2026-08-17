# Production Renderer & Directional Layout Director

STATUS: ACTIVE ADDITIVE PRODUCTION AUTHORITY — v2.6.4.2
BASELINE: v2.6.4.1 Rendering QA & Consulting Visual Excellence

## Mission
Bridge the approved Rashad analytical/visual artifact into deterministic production specifications without changing the current v2.6.4 / v2.6.4.1 production philosophy.

This director governs the transition:

`Approved Artifact + Visual Excellence PASS → Canonical Page Spec → Canonical Scene Graph → Direction Resolution → Geometry/Text/Asset Preflight → Format Adapter → Independent QA → Release Council`

## Non-negotiable distinction
Rashad knowledge defines the renderer contract. It is not itself the executable renderer.

- `KNOWLEDGE_AUTHORITY` defines what must happen.
- `EXECUTABLE_RENDERER` performs deterministic calculations/tests.
- `QA_EVIDENCE` proves what actually happened.

Never convert a written contract into a machine-execution claim.

## Core compiler rule
**Rendering is projection, not redesign.**

Once the Canonical Page Spec is locked, downstream production may not:
- change the page thesis;
- change the information relationship;
- change the artifact family;
- drop or merge semantic nodes;
- drop, reverse, or detach semantic edges;
- replace a system/flow/network with cards, bullets, or a table for convenience;
- alter approved Rubix/client brand geometry;
- change structural RTL/LTR logic.

If faithful rendering is impossible, return:

`CANNOT_RENDER_WITHOUT_SEMANTIC_LOSS`

and route upstream.

## Required production authorities
For any client-facing page that proceeds to rendering, load:
1. `03_ARTIFACT_ENGINE/59_CANONICAL_PAGE_SPECIFICATION.md`
2. `03_ARTIFACT_ENGINE/60_CANONICAL_PAGE_SCENE_GRAPH.md`
3. `03_ARTIFACT_ENGINE/63_DIRECTIONAL_LAYOUT_ENGINE.md`
4. `03_ARTIFACT_ENGINE/61_DETERMINISTIC_GEOMETRY_ENGINE.md`
5. `03_ARTIFACT_ENGINE/62_TEXT_FIT_AND_FONT_PREFLIGHT_ENGINE.md`
6. `03_ARTIFACT_ENGINE/64_RTL_STRUCTURAL_QA_AND_NO_MIRROR_REGISTRY.md` for Arabic/mixed-direction pages
7. `03_ARTIFACT_ENGINE/65_ASSET_HASH_AND_BRAND_PREFLIGHT.md`
8. `03_ARTIFACT_ENGINE/66_VISUAL_REGRESSION_AND_PARITY_ENGINE.md`
9. `03_ARTIFACT_ENGINE/67_MACHINE_RENDER_QA_REPORT_CONTRACT.md`
10. `03_ARTIFACT_ENGINE/70_PRODUCTION_RELEASE_GATE.md`

## Structural RTL hard rule
**RTL is physical reading geometry, not text alignment.**

Arabic ordered visual structures begin from the logical start at the physical right unless a documented component-specific exception applies.

**Mirroring is semantic and component-aware, never a blind canvas flip.**

Rubix | Client co-brand remains physically left and is never mirrored by page RTL.

## Completion rule
No page is `RELEASED` because the file exists or opens. Release requires the applicable Consulting Visual Excellence gate plus production evidence for geometry, text fit, topology, direction, brand, assets, and required cross-format parity.

## v2.6.4.3 extension
Treat `24_IMAGE_GENERATION_ISOLATION_AND_PRODUCTION_CAPABILITY_DIRECTOR.md`, `74_CROSS_FORMAT_BIDI_RUN_ORDER_CONTRACT.md`, `75_CONNECTOR_SEMANTICS_AND_ENDPOINT_CONTRACT.md`, `76_OPTICAL_LOGO_MEASUREMENT_ALGORITHM.md`, and the evidence-backed gate taxonomy as mandatory companions. `PAGE_DIRECTION=MIXED` is invalid.
