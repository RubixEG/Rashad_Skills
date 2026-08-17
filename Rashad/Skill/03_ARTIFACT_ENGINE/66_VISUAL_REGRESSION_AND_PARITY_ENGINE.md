# Visual Regression & Cross-Format Parity Engine

STATUS: HARD POST-RENDER QA CONTRACT — v2.6.4.2

## Comparison set
Where required by the product/runtime, compare normalized renders of:
- Approved Reference / approved scene graph;
- HTML render;
- PDF render;
- PPTX render.

Do not assume success in one format proves another format.

## Comparison dimensions
### Geometry — 30
positions, bounding boxes, proportions, region placement.

### Artifact topology — 25
nodes, edges, grouping, sequence, connector attachment, directionality.

### Typography — 15
strings, missing text, line count, clipping, font behavior, hierarchy.

### RTL / Direction — 10
zones, logical start/end, physical sequence, arrows, timeline origin, LTR islands.

### Brand — 10
approved assets, aspect ratio, placement, co-brand order.

### Images — 5
crop, focal area, resolution, distortion.

### Color / appearance — 5
material palette/contrast drift that changes approved visual hierarchy.

## Thresholds
- normal pages: parity >= 95;
- critical pages: parity >= 97.

## Hard blockers override score
- missing node/edge;
- overflow;
- clipping;
- readability-affecting overlap;
- missing text;
- wrong/distorted logo;
- RTL structural reversal;
- broken sequence;
- brand corruption;
- artifact-family downgrade.

## Pixel-only caution
Raw pixel difference alone is insufficient because rasterizers may vary in antialiasing. Structural, geometric, semantic, and textual checks are mandatory.
