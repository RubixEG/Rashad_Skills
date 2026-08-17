# Image Generation Isolation & Production Capability Director

STATUS: ALWAYS-ON FOR IMAGE / VISUAL / RENDER TASKS — v2.6.4.3

## Mission
Prevent context-contaminated image generation and prevent generic tool availability from being misclassified as Rashad production capability.

## Non-negotiable distinction
- **Image generator:** may create an isolated visual ingredient.
- **Rashad production composer:** deterministically projects an approved Canonical Page Scene Graph using native text, exact governed assets, directional geometry and machine-verifiable QA.

These are not interchangeable.

## Isolation rule
Before any image call, compile an `ISOLATED_VISUAL_ASSET_BRIEF` containing only what the asset needs. Do not expose final slide/page structure, final visible text, official numbers/dates, logos, seals, page number, tables, cards, footer chrome, or full document context. Avoid prompt terms that bias the model toward page composition such as `slide`, `deck`, `proposal page`, `RFP summary`, `dashboard`, or `infographic` unless the generation is explicitly reference-only and never eligible for production admission.

The preferred framing is the visual object itself: e.g. `wide editorial institutional visual`, not `cover slide`.

## Generated asset rejection
Reject the complete generated asset if it contains any forbidden baked element:
- readable or pseudo text/letters/numerals;
- Rubix/client/third-party logos or logo-like marks;
- seals/signatures/watermarks;
- slide frames, title zones, footer bars, page numbers;
- cards/tables/charts/dashboard chrome unless explicitly requested as reference-only;
- fabricated UI/evidence;
- final analytical topology.

Do not "fix" a contaminated asset by pretending the baked content is authoritative.

## Capability rule
Generic image, slide, document, HTML, PDF, or presentation tooling is insufficient for client-facing Rashad Production Rendering. Production may execute only when capability preflight proves:
1. canonical Page Spec / Scene Graph consumption;
2. deterministic fixed geometry;
3. native Arabic/English text and font preflight;
4. exact asset/hash injection;
5. structural RTL/LTR direction resolution;
6. connector rebuilding after direction resolution;
7. output rasterization/inspection;
8. topology and parity evidence;
9. fail-closed release gating.

## Truthfulness
If those capabilities are absent, Rashad may still produce content, Artifact Intent, Visual Blueprint, Geometry Handoff, isolated visual assets, and production specifications. It must label executable production validation `NOT_EXECUTED`/`BLOCKED`, never PASS.

## v2.6.4.6 Golden Visual Master supersession clarification
The earlier isolation rule is superseded for approved `GOLDEN_VISUAL_MASTER_PAGE` mode. Rashad may generate a full-page consulting visual underlay containing the artifact composition, architecture, journeys, systems, contextual people/flags/devices/screens and other non-authoritative visual elements. It is still **not the final production page**: exact Rubix/client logos, official visible copy, dates, numbers, source labels and page chrome remain governed native overlays. The master must be frozen by ID/SHA and pass G13/G14 plus continuity QA.

## v2.6.4.7 precedence note
The earlier isolation gate still blocks uncontrolled or contaminated image assets. However, declared `GOLDEN_VISUAL_MASTER_PAGE` generation is allowed under `28_IMAGE_BASED_GOLDEN_DECK_PRODUCTION_DIRECTOR.md` and `81_GOLDEN_VISUAL_MASTER_FULL_PAGE_GENERATION_AUTHORITY.md`. Do not reject a full-page master merely because it is full-page; reject it only when it violates fact/brand/readability/continuity/admission rules.

## v2.6.4.9 superseding clarification — visual ideation vs production master
The isolation rules remain valid for generated assets. For **Consulting Visual Ideation Mode**, however, the image model may receive the approved page thesis, topology and reference anchors so it can propose a holistic page composition. That output is a **reference concept**, not authoritative text/data/brand. The default final production master is then rebuilt in governed HTML/SVG/CSS. This clarification supersedes any reading that would prevent reference-conditioned page-level visual ideation.
