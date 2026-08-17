# 106 - V3 Stress, Safety and Artifact Preservation

Safety checks must never destroy the consulting argument.

Before repair, record:
- content signature;
- topology signature;
- brand signature;
- direction signature.

After repair, compare them. Block if repair:
- removes evidence;
- hides labels;
- drops nodes or edges;
- reverses relationships;
- converts system artifact to cards;
- leaks debug/internal metadata;
- causes broken glyphs;
- loses source traceability.

## V3 SVG Arabic Text Safety Patch

During the six-page acceptance pilot, the Council detected that Arabic text rendered directly inside SVG text elements may lose shaping or become visually garbled in some PDF/browser pipelines. Version 3 therefore adds this hard rule:

- SVG is responsible for shapes, routes, connectors, charts and relationship geometry.
- Arabic natural-language text is rendered as native HTML text overlays, not SVG text, unless the active renderer has proven Arabic SVG shaping support.
- SVG labels may use numeric geometry IDs only when hidden from client-facing output.
- Every Arabic label in a diagram must have a stable HTML label box linked to its semantic node or edge.

Failure to follow this rule is a glyph/BiDi production blocker.

