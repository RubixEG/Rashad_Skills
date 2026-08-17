> **V6.2.2 SUPERSESSION BANNER — Legacy V3 composer detail only. Universal HTML/SVG-first production is superseded by current per-page fidelity-based native/hybrid selection; this file cannot own release or production routing.**

# V3 HTML/SVG Composer Runtime Contract

LEGACY V3 default (non-governing):
`HTML + CSS + SVG → PDF/PPTX visual mirror`.

HTML owns:
- exact Arabic/English text;
- section labels;
- metadata;
- source notes;
- tables;
- legends.

SVG owns:
- system maps;
- connectors;
- timelines;
- matrices;
- operating models;
- dependency networks;
- risk/evaluation architectures.

Forbidden production route:
- PIL rounded-card page composer;
- card-only HTML grid;
- a pile of equal rectangles as the default response to complexity.

Allowed PIL/raster uses:
- contact sheet;
- thumbnail;
- final full-slide raster export after approved HTML/SVG rendering;
- emergency fallback explicitly labelled and Council-approved.

## V3 SVG Arabic Text Safety Patch

During the six-page acceptance pilot, the Council detected that Arabic text rendered directly inside SVG text elements may lose shaping or become visually garbled in some PDF/browser pipelines. Version 3 therefore adds this hard rule:

- SVG is responsible for shapes, routes, connectors, charts and relationship geometry.
- Arabic natural-language text is rendered as native HTML text overlays, not SVG text, unless the active renderer has proven Arabic SVG shaping support.
- SVG labels may use numeric geometry IDs only when hidden from client-facing output.
- Every Arabic label in a diagram must have a stable HTML label box linked to its semantic node or edge.

Failure to follow this rule is a glyph/BiDi production blocker.

