# Image-First Golden Deck Production Workflow

STATUS: CONTROLLED FALLBACK / EXPLICIT GVM MODE — NOT DEFAULT IN v2.6.4.10

STATUS: ACTIVE WORKFLOW — v2.6.4.7

## Workflow
1. Ingest RFP and build the RFP Summary page plan.
2. Produce page questions, theses, evidence and artifact intents.
3. Lock Deck Visual DNA and Style Anchors.
4. Generate cover Golden Visual Master first and approve it as the style north star.
5. Generate pages in batches of 4-6, each with section anchor + previous page reference.
6. Run Page Visual Council and Continuity Council after every batch.
7. Freeze approved images and record SHA-256 in the Page Image Manifest.
8. Apply exact native overlays where required; flatten if using Hybrid Flattened Master.
9. Assemble Golden Image PDF immediately from approved images.
10. Assemble Visual-Mirror PPTX with one full-slide image per slide.
11. Assemble optional image-based HTML if requested.
12. Run QA Harness v1.2 and image-deck parity checks.
13. Produce an optional editable-native PPTX pilot only as a secondary semantic reconstruction.

## Deliverable interpretation
- Golden Image PDF: highest visual-fidelity review artifact.
- Visual-Mirror PPTX: highest visual-fidelity presentation artifact; not fully editable.
- Image-Based HTML: visual-fidelity web preview; not semantic DOM reconstruction.
- Editable Native PPTX: optional pilot; must not be claimed pixel-identical unless proven.
