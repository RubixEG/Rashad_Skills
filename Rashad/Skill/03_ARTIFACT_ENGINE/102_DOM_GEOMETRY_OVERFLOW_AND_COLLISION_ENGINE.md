# DOM Geometry, Overflow & Collision Engine

## Required checks
- exact 16:9 canvas and expected pixel dimensions;
- safe-area containment;
- Range-based text bounds vs padding box;
- scrollWidth/scrollHeight overflow;
- overflow hidden/clip masking;
- transformed physical bounds;
- unrelated element intersection area;
- footer/header encroachment;
- off-canvas objects;
- page/document unexpected scroll.

Intentional overlaps are allowed only when explicitly instrumented and non-destructive.

Any clipped visible text, hidden content, or accidental collision is HARD FAIL.
