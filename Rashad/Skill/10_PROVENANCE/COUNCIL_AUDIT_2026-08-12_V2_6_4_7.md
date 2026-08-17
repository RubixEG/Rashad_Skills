# Council Audit — v2.6.4.7 Image-Based Golden Deck & MWAN Quality Restore

## Council
Consulting Partner; Proposal Director; Artifact Intelligence Director; Golden Visual Master Director; Image Generation Director; Brand/Co-Brand Director; Arabic RTL/BiDi Director; QA Harness Lead; Prepress/Export Lead; Non-Regression Auditor.

## Verdict
**GO — restore image-based Golden Visual Master production as the primary visual-fidelity route.**

## Decisions
- MWAN-style full-page slide images are a valid quality benchmark.
- Full-page Golden Visual Master generation is allowed and preferred for visually rich RFP summaries.
- Exact visual delivery uses image-based PDF and visual-mirror PPTX.
- Native editable PPTX is optional and cannot claim pixel parity unless separately proven.
- The cover follows the MWAN reference grammar by default.
- Saudi flags, people, devices and dashboard-like screens are contextually allowed; fake logos/facts and unreadable text are not.
- Cards are allowed only as supporting objects; generic card-grid fallback is a downgrade.
- More than 20 pages must be handled via style anchors, section anchors, batch generation, previous-page reference and continuity ledger.

## Risks
- Raster text is less editable and must be QA-reviewed visually/OCR-assisted where possible.
- Full image pages increase file size.
- Image generators may still hallucinate text/logos if asked to bake them; use Hybrid Flattened Master for critical official text/brand.

## Best approach
Use **Hybrid Flattened Golden Master** as the production default:
1. Generate visually rich page/artifact underlay.
2. Add exact text/logos/page chrome natively.
3. Flatten into one approved page image.
4. Insert that same image into PDF/PPTX/HTML.

This restores image quality while protecting factual and brand accuracy.
