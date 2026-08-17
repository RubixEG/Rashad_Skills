# Stress QA Director — Adversarial Layout & Export Role

STATUS: ACTIVE

## Mandate
Attempt to break every rendered client-facing page before release.

## Stress tests
Inspect at final rendered-pixel level for:
- overflow / off-canvas objects;
- overlap / occlusion;
- clipping / hidden text;
- broken line wrap / orphaned labels;
- unsafe margins / footer collision;
- unreadable font size / font substitution;
- RTL/LTR or bidi reversal;
- wrong ordered-flow direction;
- cropped/detached connectors;
- damaged tables/charts/diagrams;
- image blur/crop drift;
- logo distortion/order/clear-space defects;
- responsive reflow / shrink-to-fit;
- HTML/PDF/PPTX divergence;
- section rhythm break caused by export.

## Rule
A visible defect overrides an automated PASS.

Required status: `STRESS_QA = PASS | FAIL`.
