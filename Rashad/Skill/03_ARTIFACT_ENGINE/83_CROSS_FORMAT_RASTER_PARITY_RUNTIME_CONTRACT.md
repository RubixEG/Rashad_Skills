# Cross-Format Raster Parity Runtime Contract

STATUS: HARD FINAL-FORMAT QA CONTRACT — v2.6.4.6

## Purpose
HTML success does not prove PDF/PPTX success. Final formats must be rasterized and compared against the approved final-page reference.

## Evidence
For every required format capture:
- candidate file hash;
- page count;
- normalized raster dimensions;
- per-page mean absolute pixel difference;
- per-page material pixel-difference ratio under configured threshold;
- pass/fail evidence ID.

Thresholds are implementation parameters and must be calibrated against approved clean fixtures. Numeric similarity never overrides hard semantic/brand blockers.

## Runtime unavailable
If PDF or PPTX cannot be rasterized in the current environment, parity is `NOT_EXECUTED/BLOCKED`; final release cannot occur.
