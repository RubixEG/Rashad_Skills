# Governed Master & Logo Transform Integrity

STATUS: HARD PRODUCTION QA CONTRACT — v2.6.4.6

For the Golden Visual Master and governed Rubix/client marks, executable QA must reject:
- CSS/format mirroring or rotation not explicitly approved;
- filters/recolor effects;
- clipping/clip-path that removes governed pixels;
- `object-fit: cover` crop when aspect ratios differ;
- non-uniform stretch / aspect-ratio drift beyond tolerance;
- master replacement with a same-looking but different-hash image.

Golden Master G13 proves source hash/canvas placement; G14 proves transform integrity. Both are required for GVM pages.
