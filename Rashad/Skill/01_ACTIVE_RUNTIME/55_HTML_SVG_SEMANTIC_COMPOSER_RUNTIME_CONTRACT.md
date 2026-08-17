
# HTML/SVG Semantic Composer Runtime Contract

STATUS: DEFAULT PRODUCTION COMPOSER AUTHORITY — v2.6.4.10

## Master
**VERSION 4 SUPERSESSION:** HTML/SVG is a semantic reconstruction technology, not the universal design source of truth. The approved Golden Visual Master/whole-page visual board is the visual-design truth; HTML/SVG becomes production master only after it passes reconstruction fidelity.

## Responsibilities
- HTML: native Arabic/English text, semantic regions, tables, labels, evidence blocks.
- CSS Grid/Flex: macro composition and spacing.
- SVG: flows, architecture, connectors, matrices, timelines, networks, curves, braces and custom relationship geometry.
- JavaScript may measure fixed-layout element bounds after fonts load to place connectors deterministically.

## Mandatory render order
1. load exact fonts/assets;
2. render semantic text/regions;
3. await `document.fonts.ready`;
4. measure node bounding boxes;
5. resolve RTL/LTR physical positions;
6. compute SVG anchors/routes/arrowheads;
7. place labels/annotations;
8. rerun collision checks;
9. rasterize only after stable layout.

## Prohibitions
- responsive production reflow;
- CSS `row-reverse` as a substitute for semantic RTL resolution;
- div-only approximations of relationship-rich artifacts;
- detached SVG labels;
- arbitrary shrink-to-fit;
- decorative dashboard styling unrelated to the argument.
