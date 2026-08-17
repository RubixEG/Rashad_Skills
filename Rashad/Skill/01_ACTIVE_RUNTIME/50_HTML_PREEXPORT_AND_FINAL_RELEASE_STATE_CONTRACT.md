# 50 — HTML Pre-Export vs Final Release State Contract

STATUS: HARD RELEASE-SEMANTICS CONTRACT — v2.6.4.6

## Stage verdicts
- `HTML_PREEXPORT_PASS` — executable browser/page QA passed all applicable required HTML gates.
- `PDF_PARITY_PASS` — final PDF raster materially matches the approved reference under configured thresholds.
- `PPTX_PARITY_PASS` — final PPTX raster materially matches the approved reference under configured thresholds.
- `DECK_CONTINUITY_PASS` — deck-level anchor/master/adjacency continuity executable QA passed.
- `RELEASED` — only after all four required evidence classes plus the applicable Rashad councils/release authorities pass.

HTML QA can never emit or imply final `RELEASED` by itself.

## Runtime failure
If browser/rasterizer/LibreOffice/PDF tooling or another required runtime is unavailable, record structured `NOT_EXECUTED/BLOCKED` evidence. Do not fabricate an execution PASS.

## Multi-page deck aggregation
Per-page HTML reports must be aggregated across the full deck. `HTML_PREEXPORT_PASS` for a deck is valid only when every required page report is `HTML_PREEXPORT_PASS`; one passed page cannot stand in for the deck.
