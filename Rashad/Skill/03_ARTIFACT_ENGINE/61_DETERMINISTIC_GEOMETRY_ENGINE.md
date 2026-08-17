# Deterministic Geometry Engine Contract

STATUS: HARD RENDER GEOMETRY AUTHORITY — v2.6.4.2

## Fixed canvas
Final production uses an exact 16:9 coordinate system. Presentation geometry must resolve to explicit values before release rendering.

## Boundary checks
For every object, the runtime must verify mathematically that the object remains inside its approved safe bounds and page canvas.

Conceptual conditions:
- `x >= safe_left`
- `y >= safe_top`
- `x + width <= canvas_width - safe_right`
- `y + height <= canvas_height - safe_bottom`

## Collision checks
Every pair of potentially intersecting objects must be classified as:
- `INTENTIONAL_OVERLAP`
- `ACCIDENTAL_COLLISION`

Unapproved collision is a hard failure.

## Required checks
- page boundaries;
- safe margins;
- region containment;
- spacing and padding;
- overlap/collision;
- clipping;
- z-order;
- footer/trim safety;
- artifact canvas bounds;
- connector routing space;
- minimum readable geometry.

## Prohibited release behavior
- uncontrolled responsive reflow;
- automatic grid rearrangement;
- hidden overflow;
- browser/office shrink-to-fit;
- global page scaling used to mask a fit failure.

## Repair authority
Geometry repair may change micro-placement only within approved tolerances and may not change semantic topology or visual hierarchy. If repair would require semantic change, return upstream.
