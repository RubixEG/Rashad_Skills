# Optical Logo Measurement Algorithm

STATUS: HARD CO-BRAND GEOMETRY SPECIFICATION — v2.6.4.3

## Purpose
Turn "same visible/optical height" into a repeatable measurement rather than subjective eyeballing.

## Visible bounds
For transparent PNG/SVG-derived raster:
1. read alpha channel;
2. define visible pixel mask as `alpha >= 0.05` by default;
3. compute the smallest bounding box containing the mask;
4. ignore fully transparent padding;
5. shadows/glows with alpha below threshold do not expand the visible box;
6. if the source has no alpha or contains an opaque background, brand preflight must classify it explicitly rather than pretending it is transparent.

## Optical height
`visible_height = bottom_visible - top_visible + 1`.
Scale each co-brand asset preserving aspect ratio so the visible-height ratio is target `0.98–1.02`, subject to each mark's minimum-size/clear-space rule.

## Optical center
Use the center of the alpha-weighted visible mask for vertical optical alignment; if unavailable, use visible bounding-box center and flag `OPTICAL_CENTER_APPROXIMATED`.

## Tolerances
- aspect-ratio drift: 0%;
- crop: 0; mirror: false; recolor: false; stretch: 0;
- visible-height ratio target: 0.98–1.02;
- geometry measurement tolerance: ±1 canonical pixel after raster normalization, or equivalent target-format unit.

## Evidence
Record input hash, alpha threshold, visible bounds, scale factor, resulting visible height, center, and final geometry in brand QA evidence.

