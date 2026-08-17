# 50 - V3 Predictive Stress / Load / Integration Test Plan

## Stress tests
- long Arabic title;
- dense evidence page;
- mixed Arabic + API / ISO / URL text;
- 15+ semantic nodes;
- 20+ connectors;
- multiple source notes;
- two-logo co-brand;
- right-to-left timeline;
- risk matrix with labels;
- evaluation weights.

## Load tests
- 30-page deck rhythm;
- no more than two consecutive same-grammar pages unless justified;
- repeated palette check;
- style-anchor drift check;
- font and asset loading across all pages.

## Integration tests
- Page Content Pack to HTML/SVG master;
- HTML/SVG master to PDF;
- PDF raster inspection;
- PPTX visual mirror from same raster;
- PDF/PPTX parity;
- contact sheet review;
- no internal metadata leakage;
- QA evidence per page.

## Predictive tests
Before rendering, the council predicts probable failure modes. Any high-risk unmitigated failure blocks generation.

## V3 SVG Arabic Text Safety Patch

During the six-page acceptance pilot, the Council detected that Arabic text rendered directly inside SVG text elements may lose shaping or become visually garbled in some PDF/browser pipelines. Version 3 therefore adds this hard rule:

- SVG is responsible for shapes, routes, connectors, charts and relationship geometry.
- Arabic natural-language text is rendered as native HTML text overlays, not SVG text, unless the active renderer has proven Arabic SVG shaping support.
- SVG labels may use numeric geometry IDs only when hidden from client-facing output.
- Every Arabic label in a diagram must have a stable HTML label box linked to its semantic node or edge.

Failure to follow this rule is a glyph/BiDi production blocker.

