
# Non-Destructive Stress Repair Engine

## Before repair
Freeze `content_signature`, `topology_signature`, `brand_signature`, `direction_signature`.

## Stress cases
- long Arabic titles and labels;
- dense BOQ/evaluation tables;
- mixed Arabic/English IDs;
- narrow labels around networks;
- 20+ nodes / 20+ edges;
- large team matrices;
- small client logo artwork inside padded transparent canvas;
- PPTX/PDF raster differences;
- 30+ page deck continuity.

## Repair invariant
Safety changes geometry, never meaning.
If a fix would delete or simplify semantics, split/redesign upstream instead.
