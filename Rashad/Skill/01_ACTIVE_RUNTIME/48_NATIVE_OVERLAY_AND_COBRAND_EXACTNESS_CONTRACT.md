# 48 — Native Overlay & Co-Brand Exactness Contract

STATUS: HARD FINAL-COMPOSITION AUTHORITY — v2.6.4.4

## Purpose
Keep the Golden Visual Master visually intact while ensuring exact copy, RTL, numerals and brand identity.

## Native overlay owns
- final Arabic/English heading and body copy;
- official dates, values, weights, quantities and IDs;
- source/evidence labels;
- page number/footer identifiers;
- exact Rubix logo;
- exact client logo/seal when required;
- any factual chart/table labels that cannot safely be baked into generated pixels.

## Co-brand geometry
`Rubix | Client` remains a single physical left-side signature unless current authority explicitly overrides it.
- same visual line / optical center;
- visible/optical height ratio target 0.98–1.02;
- adequate production ink height; do not make the client mark visually weak merely to fit a raw PNG box;
- exact source hash;
- transparent background;
- no crop/stretch/recolor/mirror;
- separator vertically centered to the optical marks.

## Master/overlay interaction
The master must reserve overlay-safe zones or contain low-detail regions behind important copy. If native overlay would cover a critical visual relationship, regenerate the master rather than shrinking the text or destroying hierarchy.

## Projection rule
PDF/PPTX/HTML may use the approved master as a fixed underlay. Do not rebuild the artifact in each format. Editable overlay objects may remain native on top.
