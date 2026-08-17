# v2.6.4.7 Root Cause & Strategy Decision

## Root cause
Recent output quality degraded because the system over-corrected toward image isolation and then asked a limited native renderer to rebuild complex consulting artifacts. The renderer selected generic safe primitives — cards, boxes and tables — which protected layout but weakened artifact richness and visual maturity.

## Strategic correction
Restore page-by-page image generation as Golden Visual Master production, but under governance:
- Page Spec and Artifact Intent first;
- Deck Visual DNA and style anchors;
- controlled 4-6 page batches;
- previous-page continuity reference;
- image SHA freeze;
- exact overlays where needed;
- image-based PDF/PPTX/HTML projection;
- QA Harness v1.2 and continuity QA.

## Better than both extremes
- Better than uncontrolled full-slide AI: because facts/logos/continuity/QA are governed.
- Better than pure native HTML/PPTX: because artifact richness is preserved and renderer card downgrade is avoided.
