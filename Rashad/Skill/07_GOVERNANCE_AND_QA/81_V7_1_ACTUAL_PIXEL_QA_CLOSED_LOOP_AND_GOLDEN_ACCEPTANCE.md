# V7.1 — Actual Pixel QA Closed Loop & Golden Acceptance Gate

**STATUS: CURRENT USER-VISIBLE QUALITY FOUNDATION UNDER V7.2 — V7.2 BRAIN-COHERENCE PROOF IS ADDITIONALLY REQUIRED**

## Core law
QA of the framework is not QA of the product. A user-visible Artifact Draft must be reviewed from its actual rendered pixels and tied to the exact render/file hash.

## Mandatory page-level independent review
Every user-visible page must receive independent scores for:
- message clarity;
- 5-second comprehension;
- visual-form fitness;
- simplicity;
- executive hierarchy;
- evidence legibility;
- artifact usefulness;
- specificity to this page/client problem;
- Arabic/RTL/typography quality when applicable;
- brand fidelity;
- production quality.

Minimum: every dimension ≥80 and mean ≥85, with no hard blocker.

Required challenges:
- `GENERIC_LAYOUT_SWAP_TEST` — would the page still work by swapping labels for another RFP? If yes, fail.
- `ARTIFACT_SKEPTIC_PIXEL_TEST` — does the visual do analytical work or merely decorate/box text? Decoration-only fails.
- `FIVE_SECOND_PIXEL_TEST` — can an executive identify the answer and focal point in ~5 seconds? If no, fail.

## Repair loop
`Render → Pixel QA → Repair Brief → Re-render → Pixel QA` repeats until PASS or a bounded maximum repair count is reached. QA findings are actionable production instructions, not a report-only endpoint.

Any failed quality round requires persisted repair history. A failed round followed by no repair is `BLOCK_DELIVERY`.

## Deck-level review
For multi-page products, render every page, create a montage/contact sheet, then independently review:
- narrative rhythm;
- visual variety;
- calm versus dense-page rhythm;
- executive coherence;
- cross-page specificity;
- diagram overuse;
- repeated structural fingerprints;
- brand consistency;
- RTL consistency;
- overall Partner-grade quality.

A deck may fail even if every individual page passes.

## Deterministic product inspection
The delivery gate must inspect the actual PPTX/package structure and reject obvious production collapse, including:
- claimed `IMAGE_LED` page without an image;
- claimed `CHART_LED` page without a chart or equivalent governed chart proof;
- claimed `TABLE_LED` page without a native table or explicit structured-grid proof;
- `NUMBER_LED` without hero-metric proof;
- structural monotony across most slides;
- excessive shape-only analytical pages;
- repeated production fingerprint disguised by different labels.

## Golden real-RFP acceptance
At least one real RFP is maintained as a golden end-to-end regression scenario. A release cannot call Artifact/QA integration closed merely because synthetic unit tests pass. The golden scenario must prove:
`RFP → cognition → strategy search → production render → actual pixel QA → repair → deck QA → delivery gate`.

The golden fixture is evidence of execution quality, not a template to copy.
