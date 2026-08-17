# Full Council Audit — v2.6.4.9

## Council
- AI Skill Architect / Context Engineer
- Consulting Partner
- Proposal Director
- Senior Project Manager
- Operations / Launch Lead
- Governance & Decision-Control SME
- Artifact / Information Design SME
- HTML/SVG/CSS Composition Lead
- Brand / RTL SME
- QA / Release SME

## Evidence reviewed
- v2.6.4.8 Skill package;
- latest v2.6.4.8 REDF RFP Summary contact sheet;
- MWAN / image-generation visual references;
- current Rubix Artifact Palette and brand authorities;
- GVM, Page Spec, Scene Graph, renderer and card-control authorities.

## Root-cause findings
1. **Premature determinism.** Existing Page Spec / Scene Graph logic can freeze geometry before holistic composition search. This strongly favors safe, simple layouts.
2. **Renderer vs art-direction role confusion.** Renderer contracts are strong at fidelity and safety but not responsible for visual invention; the architecture did not give visual invention enough space before render.
3. **Raster-GVM overcorrection.** v2.6.4.7/8 correctly recovered image-first quality but made raster preservation too central. The owner now prefers professional HTML/CSS as the production master.
4. **Card policy needed nuance.** “No cards” is the wrong target; MWAN itself uses bounded panels. The failure is card-only page architecture without a higher-order artifact.
5. **Content compression contributed to weak pages.** Recent outputs were cleaner but visually/analytically thinner than the stronger MWAN references. Consulting quality needs disciplined density, not emptiness.
6. **Reference conditioning needed to drive composition, not just style.** MWAN must inform hierarchy, density, evidence placement and page rhythm.
7. **Palette governance existed but was not tightly integrated with the composer.** The HTML/SVG master now activates a limited page-specific color budget.
8. **No browser visual self-critique loop was authoritative enough.** Mechanical QA alone cannot identify a generic but technically safe page.

## Architectural decisions
- Default final visual master becomes **HTML_SVG_MASTER**.
- Image generation becomes optional **Visual Ideation / Reference** and explicit GVM fallback.
- Physical geometry freezes **after** concept selection and browser critique.
- SVG becomes first-class for analytical geometry.
- CVFS ≥90/100 is mandatory for critical pages.
- Content Density & Artifact Richness becomes a release concern.
- Cover-left editorial hero rule remains hard default.

9. **Legacy route ambiguity cleaned up.** Active GVM files are explicitly labeled fallback/reference rather than default, and duplicate numeric authority prefixes are resolved by full-filename routing.

## Verdict
**GO — MAJOR NON-BREAKING VISUAL ARCHITECTURE UPGRADE.**

The council expects this architecture to materially close the gap between Rashad's deterministic outputs and the stronger holistic page quality historically seen from direct image generation, while retaining exact content/brand/RTL control.
