# MWAN Reference & Last-Version Audit — v2.6.4.7

## Inputs reviewed
- `MWAN.pptx` — 20-slide deck where each slide is effectively a full-page raster image at 1672×941 inside a 16:9 PowerPoint canvas.
- `last version(4).zip` — contains 46 generated PNGs plus a six-slide parity pilot and report.

## Findings
1. MWAN delivery quality came from using approved full-slide images, not from reconstructing every artifact as editable PowerPoint objects.
2. The six-slide pilot report states that image-based PDF and visual-mirror PPTX preserve approved images as full-page visuals and are the correct route for exact visual delivery.
3. Editable-native PPTX was correctly treated as a separate pilot, not pixel-identical.
4. The cover grammar is a valuable reference: left institutional/sector visual, right clean Arabic title zone, co-brand top-left, magenta accent, light background.
5. The previous over-tight image isolation caused underuse of the image engine and pushed the renderer toward generic cards.
6. The corrected approach is not uncontrolled slide-image generation; it is Golden Visual Master generation governed by Page Spec, Deck Visual DNA, style anchors, SHA freeze and QA.

## Council decision
Adopt image-based Golden Deck delivery as the primary visual-fidelity route for RFP Summary and internal competitive understanding decks. Keep editable-native reconstruction optional and secondary.
