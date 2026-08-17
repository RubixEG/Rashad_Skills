# Production Renderer Release Council

STATUS: ACTIVE POST-RENDER COUNCIL — v2.6.4.2

## Purpose
Convert the existing post-render quality council into a production compiler/release checkpoint with explicit direction, topology, regression, and truthfulness responsibilities.

## Required roles
- Rendering Fidelity Director
- Stress QA Director
- Artifact Integrity Auditor
- Directional Layout QA Lead
- Arabic RTL/Bidi reviewer for Arabic/mixed pages
- Typography/Prepress Lead
- Brand Governor / Co-Brand Logo Director where branded
- Format Adapter QA
- QA/Regression Lead
- Release Chair

## Mandatory evidence
For each required output format:
- source Page Spec hash;
- final render reference;
- geometry status;
- text-fit/font status;
- directional structure status;
- node/edge reconciliation;
- brand/asset status;
- overflow/collision status;
- parity status/score where executed;
- Stress QA findings;
- truth label for each check (`PROVEN`, `VISUALLY_INSPECTED`, etc.).

## Decision
`RELEASE | FIX | RE_RENDER | REGENERATE | REDESIGN | BLOCK`

## Non-compensation
High consulting quality cannot compensate for renderer corruption. High renderer fidelity cannot compensate for weak consulting quality. Numeric parity cannot waive a hard blocker.

## v2.6.4.7 image-based release path
For Golden Visual Master decks, evaluate the frozen image master, overlays, output raster parity and deck continuity. Do not require native DOM/PPTX object reconstruction to release the visual-fidelity PDF/PPTX. Editable-native release is a separate decision.
