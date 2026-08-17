# Image Generation Decision Engine

## Inputs
- page thesis;
- evaluator question;
- information relationship;
- service-line owner;
- artifact archetype;
- density target;
- section narrative role;
- available approved assets.

## Decision outcomes
- `NO_ASSET_NATIVE_ARTIFACT`
- `REUSE_APPROVED_ASSET`
- `GENERATE_PRODUCTION_HERO_ISOLATED`
- `GENERATE_PRODUCTION_ILLUSTRATION_ISOLATED`
- `GENERATE_ICON_CONCEPT_AND_VECTORIZE`
- `GENERATE_CONCEPT_PAGE_THEN_REBUILD`
- `REFERENCE_ONLY`

## Scoring criteria
Score each candidate 0–5:
- thesis relevance;
- comprehension benefit;
- emotional/sector relevance;
- brand compatibility;
- editability requirement;
- risk of hallucination;
- provenance clarity;
- renderer compatibility.

Generation requires a positive net contribution. Decorative novelty alone is insufficient.

## Hard constraints
- no logos or brand wordmarks in generated pixels;
- no proposal text or numeric labels in generated pixels;
- no generated official seals or certificates;
- no fake screenshots;
- no precision diagrams as raster artwork;
- no unapproved portraits or identifiable staff likenesses;
- no client-specific confidential elements.

## Recommended modes by page
- Cover: hero/abstract production asset or current Rubix device.
- Section opener: hero, sector, or conceptual illustration.
- Executive synthesis: usually native editorial layout, optional subtle motif.
- Diagnostic: native diagram, optional supporting illustration.
- Methodology: native lifecycle; icons may support stages.
- Governance: native model; icons may support roles/controls.
- Team: approved line icons, not generated people portraits by default.
- Experience/case study: approved photography or evidence, never fabricated proof.
- Appendix/compliance/commercial: native only unless a small supporting motif adds clarity.


## External reference pattern gate
Before image generation, retrieve only approved references/patterns/components from the Proposal Visual Intelligence Knowledge Base. Unreviewed corpus pages may inform council analysis but cannot enter the production brief automatically. The brief must state the asset's role, content relationship, section relationship, neighboring-page role, provenance, and fallback.

## v2.3 authority upgrade
For all new image-generation decisions, `28_IMAGE_IDEATION_INTERFACE.md` is the controlling interface. It distinguishes internal visual concept ideation from production visual ingredients and forbids final-slide generation. If this file conflicts with the v2.3 interface, the v2.3 interface wins without weakening the Production Firewall.


## v2.6.4.3 controlling gate
All production generation outcomes above are subordinate to `72_IMAGE_GENERATION_ISOLATION_GATE.md` and `73_GENERATED_ASSET_ADMISSION_QA.md`. A generated page/slide/infographic or any asset containing baked text/logo/numerals/document chrome is not a recoverable production asset; it is rejected or reference-only. Generic image capability does not authorize final page production.
