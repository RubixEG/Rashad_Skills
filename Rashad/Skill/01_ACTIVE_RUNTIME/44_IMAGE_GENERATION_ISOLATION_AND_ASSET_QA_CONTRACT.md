# Image Generation Isolation & Asset QA Contract

STATUS: HARD ACTIVE RUNTIME CONTRACT — v2.6.4.3

## Purpose
Ensure generated imagery cannot silently become a malformed proposal page or introduce fabricated brand/text/data.

## Required sequence
`Page Contract → Visual Need Detection → Isolated Asset Brief → Image Generation → Generated Asset Admission QA → Approved Asset → Deterministic Composer`

Never use:
`Full page brief → image model → accept generated slide`.

## Isolated brief minimum
- asset ID / page ID;
- asset role;
- visual subject;
- sector/business tone at high level;
- composition/focal zone/negative-space zone;
- style family;
- resolution/aspect ratio;
- explicit forbidden semantic classes;
- no-text/no-logo/no-number/no-document-chrome flags;
- fallback strategy.

## Context minimization
Do not pass raw transcript, full RFP pack, final page title/body, exact official figures, logo files, page number, full slide skeleton, or unrelated neighboring pages into a generation request unless the environment can guarantee those inputs cannot be reproduced and their inclusion is essential. Prefer abstracted evidence boundaries.

## Admission status
`DRAFT → ASSET_QA → APPROVED | REJECTED`

An approved generated asset remains an ingredient only; it never becomes source of truth.

## v2.6.4.4 supersession — Golden Visual Master mode
The strict isolated-ingredient path remains valid for ingredient generation. It no longer prohibits complete page-level visual generation. A separate `GOLDEN_VISUAL_MASTER` mode is governed by `46_GOLDEN_VISUAL_MASTER_PAGE_GENERATION_CONTRACT.md`: full-page composition is allowed, contextual flags/screens/devices are allowed, and exact production copy/logos remain native overlays. Do not reject a master merely because it visually resembles a slide.

## v2.6.4.7 Golden Master exception
`PRODUCTION_VISUAL_ASSET_ISOLATED` is not the only valid image mode. `GOLDEN_VISUAL_MASTER_PAGE` is a governed full-page mode used for visual-fidelity decks. It requires Page Spec, Deck Visual DNA, page manifest, SHA freeze and council admission. It may include complete page composition, but official text/logos/numbers must be verified or overlaid natively before final flattening.
