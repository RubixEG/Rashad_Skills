# 36 — Capability Preflight & Tool Routing

STATUS: **HARD EXECUTION AUTHORITY — v2.5**
PURPOSE: Decide whether the current runtime can execute the approved artifact product without generic fallback.

## Required preflight
Before the first production action, compare the Delivery Contract + all locked Geometry Handoffs against runtime capabilities:
- image generation when an asset plan requires it;
- deterministic composer;
- native/editable text;
- exact asset injection;
- native/vector shapes/connectors/tables as required;
- physical RTL control;
- file output;
- requested export (PPTX/PDF when required);
- visual inspection/QA capability.

## Deterministic composer definition
A capability may be marked `deterministic_composer=TRUE` only if it can consume the approved Blueprint/Geometry semantics and construct native page elements while preserving exact text/assets/RTL/numerals. Generic HTML, generic document generation, screenshot assembly, or image generation alone does not qualify.

## Outcomes
- `PASS`: execute orchestrator.
- `BLOCKED`: persist specs/ledgers and stop production truthfully.
- `PARTIAL`: allowed only for a product whose Delivery Contract explicitly permits `ARTIFACT_SPEC`; never satisfies a required artifact product.

## Tool routing
Image generation is routed only to approved hero/illustration/concept asset substeps. It is never routed as a replacement composer.

## v2.6.4.3 production capability invariant
`deterministic_composer=TRUE` requires native text, exact asset injection, canonical scene-graph projection, fixed geometry, directional RTL/LTR, connector rebuilding, raster inspection, topology/parity evidence, and fail-closed release behavior. Generic image/slide/document/HTML/PDF/PPTX tool availability is insufficient. Image generation is separately governed as isolated asset creation only.
