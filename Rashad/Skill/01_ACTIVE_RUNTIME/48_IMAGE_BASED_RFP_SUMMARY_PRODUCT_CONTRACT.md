STATUS: FALLBACK / EXPLICIT GVM MODE — SUPERSEDED AS DEFAULT BY v2.6.4.10

# Image-Based RFP Summary Product Contract

STATUS: ACTIVE PRODUCT CONTRACT — v2.6.4.7

## Product intent
Create RFP Summary / competitive-understanding decks with the visual quality of MWAN-style full-page generated slide images while preserving evidence discipline, Arabic RTL, brand governance, and output parity.

## Required outputs
At minimum:
- Golden Image PDF — one approved full-page image per page;
- Visual-Mirror PPTX — each slide contains the exact approved full-page image;
- Image-Based HTML where requested — pages are rendered as approved images, not rebuilt into weak responsive cards;
- QA report and image manifest;
- optional editable-native PPTX pilot clearly marked as non-pixel-identical.

## Required page assets
For every page:
- `page_id`;
- `golden_visual_master_path`;
- `golden_visual_master_sha256`;
- `source_page_spec_id`;
- `style_anchor_ids`;
- `section_anchor_id` where applicable;
- `previous_page_reference_id` except cover/first page;
- overlay strategy: `FULL_RASTER | HYBRID_FLATTENED | NATIVE_RECONSTRUCTION_PILOT`;
- text/brand/content QA status;
- continuity status;
- release decision.

## Official text/logo handling
Recommended default for production accuracy: `HYBRID_FLATTENED`.
- The AI-generated visual carries the page's visual richness.
- Exact official text, numbers, client/Rubix logos and page chrome are applied as native overlays.
- The final flattened page image becomes the master inserted into PDF/PPTX/HTML.

Full raster masters with baked text/logos may be used only when council QA confirms readability, correctness, no fake logo issue, no BiDi corruption, and owner/project approval for raster text.

## No-card downgrade rule
Native HTML/PPTX builders must not replace an approved Golden Visual Master with generic cards. If native reconstruction is required, it is a separate pilot and must be compared against the master.
