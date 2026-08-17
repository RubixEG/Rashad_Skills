# 28 — Image Ideation Interface

STATUS: HARD POLICY — v2.3
PURPOSE: Use image generation for visual creativity without surrendering production control.

## Image generation is a subordinate service
Image generation may propose visual mood, metaphor, composition inspiration, sector imagery, texture, or isolated illustrations. It is **not** the artifact composer and is never an authority on facts, text, logos, numbers, geometry, RTL, tables, timelines, BOQ, evidence, or semantic edges.

## Mode 1 — INTERNAL_VISUAL_CONCEPT
Allowed only after:
- page question/thesis/evidence are fixed;
- dominant information relationship is fixed;
- semantic nodes/edges are already defined;
- Artifact Council authorizes ideation.

Prompt constraints:
- no Rubix logo;
- no client logo;
- no readable text;
- no numbers or dates;
- no named client facts;
- no official seals/signatures;
- no exact tables, charts, BOQ, risk rows, or evaluation values;
- unlabeled shapes/paths may explore composition only.

Output constraints:
- label `INTERNAL_VISUAL_CONCEPT — NOT FOR CLIENT USE`;
- never embed directly in final PPTX/PDF;
- extract only: hierarchy, balance, negative space, spatial metaphor, framing, shape language, rhythm;
- create a native Visual Blueprint from the useful ideas;
- discard the concept after blueprint lock unless retained outside the portable skill as reference evidence.

## Mode 2 — PRODUCTION_VISUAL_INGREDIENT
Allowed for:
- cover hero;
- section hero;
- conceptual sector illustration;
- texture/background;
- isolated icon concept.

Must be strictly:
`TEXT_FREE + LOGO_FREE + NUMBER_FREE + FACT_FREE`.

## Forbidden modes
- generated complete slide/page;
- generated branded deck preview treated as production;
- generated Arabic text inside artwork;
- generated tables, Gantt, risk register, compliance matrix, architecture labels, scorecards, BOQ, or official timelines;
- generated logo approximation;
- screenshot-to-slide production reconstruction.

## Handoff rule
Image generation may influence `Visual Blueprint`, but the deterministic composer owns:
- all words;
- all numbers;
- all tables;
- all connectors/edges with meaning;
- all official diagrams;
- all logos;
- all dates/references;
- RTL sequence;
- final layout geometry.

## Controlled ideation cycle
Do not call image generation by default. Use it only when the Artifact Director judges that spatial ideation can materially improve the blueprint.

When used:
1. Generate at most **3 materially different** internal concepts for one artifact decision.
2. Reject any concept containing pseudo-text, watermark-like marks, logo-like brand reconstruction, readable numbers, or client-specific factual content.
3. Score concepts on: relationship fit, hierarchy, focal-point clarity, whitespace, RTL rebuild feasibility, native editability feasibility, and narrative distinctiveness.
4. Select **composition intelligence**, not the pixels.
5. Translate the selected intelligence into the Visual Blueprint.
6. The selected concept has no release status and cannot be promoted to production.

If native geometry can be designed confidently without ideation, skip image generation.



## v2.6.4.3 image-isolation override
All `PRODUCTION_VISUAL_INGREDIENT` calls must pass `72_IMAGE_GENERATION_ISOLATION_GATE.md` and `73_GENERATED_ASSET_ADMISSION_QA.md`. The prompt must describe the visual object rather than the slide/deck/report containing it, and should not include final production copy, official values, logos, page number, tables/cards, final analytical topology, or raw full-RFP/full-conversation context. If context isolation cannot be guaranteed for a high-risk asset, use `REFERENCE_ONLY` / `BLOCKED_CONTEXT_NOT_ISOLATABLE`.

`INTERNAL_VISUAL_CONCEPT` may explore composition only as reference and must be explicitly framed as NOT a production page. Any slide-like output remains reference-only and cannot be admitted as a production visual ingredient.
