# Stress Mutation & Deterministic Render Engine

A page that passes only under ideal text and timing is not production-ready.

Required stress suite:
1. `FONT_SCALE_108` — increase governed text by 8% and re-check bounds/collisions.
2. `LINE_HEIGHT_108` — increase line-height by 8% on body/labels.
3. `ARABIC_EXPANSION` — page-family fixture with long Arabic strings at expected percentile.
4. `MIXED_BIDI` — Arabic + API/ISO/URL/parentheses/slash cases.
5. `RENDER_REPEAT` — render the same page at least 3 times after fonts-ready; geometry/pixel fingerprint must remain stable within tolerance.
6. `PAGE_LOAD` — execute all pages in the pilot/deck and ensure no resource/font timeout silently changes layout.

Stress failure predicts a future overflow and blocks full-deck cutover until repaired.
