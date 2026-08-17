# Image Generation Isolation Gate

STATUS: HARD PRE-GENERATION GATE — v2.6.4.3

## Core rule
**Default image generation is isolated visual-asset mode. Approved Golden Visual Master mode is the controlled exception for a full-page visual underlay, not a final authoritative page.**

## Semantic firewall
The image call should not know or reproduce the final document chrome. Prefer prompts that describe the visual object rather than the document containing it.

FORBIDDEN INPUT/OUTPUT CLASSES FOR PRODUCTION-ASSET MODE:
- final page/slide copy;
- official numbers/dates/IDs that may be baked into pixels;
- Rubix/client logos or seals;
- page/slide number;
- tables, cards, dashboard layouts, footer/header chrome;
- final analytical diagrams/topology;
- full raw RFP or conversation context.

## Negative semantic firewall
For production asset mode the brief explicitly says the asset is NOT a presentation, slide, infographic, dashboard, report page, proposal page, UI, poster, or document.

## Modes
- `PRODUCTION_VISUAL_ASSET_ISOLATED` — eligible for admission QA.
- `REFERENCE_ONLY_VISUAL_CONCEPT` — may contain composition ideas but is never production-admissible without rebuilding.
- `BLOCKED_CONTEXT_NOT_ISOLATABLE` — use when the environment cannot prevent full-context contamination and the requested asset has high risk of reproducing forbidden page/brand content.

## Failure
Any production-asset generation that returns a slide-like composition, baked text/numerals/logo, or final analytical structure is `REJECTED — IMG-ISO-001`.

## v2.6.4.4 mode split
This gate now applies to `PRODUCTION_VISUAL_ASSET_ISOLATED`. It does **not** reject `GOLDEN_VISUAL_MASTER` page generation. Full-page visual masters use `77_GOLDEN_VISUAL_MASTER_GENERATION_ENGINE.md` and may contain contextual people/flags/screens/dashboard-like cues. Exact brand identity and authoritative visible copy remain native overlay responsibilities.

## v2.6.4.6 GVM mode exception
`GOLDEN_VISUAL_MASTER_PAGE` is an approved production-underlay mode and may be full-page. It may contain analytical visual structure. The prohibition remains on treating generated pixels as authority for exact production text, official values, Rubix/client logos, evidence, or final page chrome. GVM output must be frozen and governed under `77`, `80`, `81`, G13/G14 and deck continuity.

## v2.6.4.7 Golden Visual Master mode
This gate does not prohibit governed full-page image generation. `GOLDEN_VISUAL_MASTER_PAGE` is valid when called by the image-based Golden Deck workflow. The gate blocks uncontrolled slide generation; it does not block an approved master page with Page Spec, style anchors and QA admission.
