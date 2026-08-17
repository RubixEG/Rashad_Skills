# Deterministic Renderer Contract

## Renderer responsibilities
- exact page dimensions and safe zones;
- current logos from asset IDs;
- approved fonts and actual font embedding;
- RTL text and bidi-safe numerals;
- AR-SEQ-001 explicit sequence contracts, visual-slot maps, and connector directions;
- component measurement before render;
- editable shapes, text, tables, charts, icons, and diagrams;
- HTML/PDF/PPTX parity;
- source notes and navigation;
- page image review after PDF creation;
- PPTX object-coordinate validation for ordered artifacts.

## Preflight
The build fails if:
- approved fonts are unavailable;
- logo pixels touch source boundaries;
- content exceeds page bounds;
- a page uses an unsupported fallback component;
- an Arabic ordered artifact starts from the left or bottom;
- a sequence proceeds bottom-to-top or reverses on a later row;
- sequence labels/connectors are baked into generated imagery;
- the PDF and HTML differ materially;
- a critical PowerPoint page falls below 95% parity;
- overall parity falls below 92%.

## v2.3 upstream contract
The deterministic production runtime consumes an approved `Visual Blueprint` and `Geometry Handoff Contract` from `27_VISUAL_BLUEPRINT_SCHEMA.md` and `32_GEOMETRY_HANDOFF_CONTRACT.md`. Renderer availability remains external to the portable skill. No renderer may reinterpret the Artifact Intent, substitute a generic layout family, or convert authoritative content into generated pixels.

## v2.6.4.9 renderer priority
The primary visual-production adapter is now a fixed-canvas **HTML/SVG/CSS composer**. The renderer consumes an approved visual concept and relative composition blueprint, renders to browser pixels, and only then freezes final geometry. SVG is the preferred mechanism for relationship geometry. PDF and PPTX are projections from the approved HTML master unless explicit GVM mode is selected.
