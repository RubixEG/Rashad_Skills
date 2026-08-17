# Artifact Engine Authority Index & Legacy Prefix Collision Resolution

## Problem
Historical additive releases created duplicate numeric prefixes for `81`, `82`, and `83`. Numeric prefixes are ordering aids, not unique authority IDs.

## Resolution
From v2.6.4.9 onward:
- authority routing MUST use the **full filename**, never a numeric prefix alone;
- `81_GOLDEN_VISUAL_MASTER_FULL_PAGE_GENERATION_AUTHORITY.md` and `81_GVM_SEMANTIC_TOPOLOGY_SIDECAR_CONTRACT.md` are distinct authorities;
- `82_GOVERNED_MASTER_AND_LOGO_TRANSFORM_INTEGRITY.md` and `82_MWAN_COVER_AND_VISUAL_DNA_REFERENCE_LOCK.md` are distinct authorities;
- `83_CROSS_FORMAT_RASTER_PARITY_RUNTIME_CONTRACT.md` and `83_DECK_STYLE_ANCHOR_AND_CONTINUITY_BATCH_PROTOCOL.md` are distinct authorities.

The current default visual-production chain is:
`91 → 92 → 93 → 94 → 96 → 97 → QA / release`, with exact full filenames used in routing.

## v2.6.4.10 canonical A-to-Z chain
Current visual/content chain uses full filenames: `107_VISUAL_REASONING_FUNCTIONAL_EMULATION_PROTOCOL.md → 109_CONTENT_ARTIFACT_CO_DESIGN_ENGINE.md → 114_VISUAL_CONCEPT_BENCHMARK_AND_SELECTION_SCORE.md → 111_HTML_SVG_SEMANTIC_COMPOSER_V2.md → 112_LAYOUT_AWARE_CONNECTOR_AND_LABEL_ENGINE.md → 115_NON_DESTRUCTIVE_STRESS_REPAIR_ENGINE.md → 120_FINAL_CONSULTING_PAGE_RELEASE_SCORECARD.md`.
