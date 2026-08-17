# 29 — Production Execution Firewall

STATUS: **HARD AUTHORITY — BLOCKING — v2.2**

## Purpose
Convert Rashad's visual/brand/RTL rules from advisory knowledge into **pre-execution gates**. No image, slide, PDF, PPTX, HTML, or other client-facing render action may run before this firewall passes.

## Rule 1 — Golden Visual Master full-page generation is permitted under v2.6.4.4
Image generation has three governed roles:
1. `GOLDEN_VISUAL_MASTER` — a complete one-page visual composition used as an approved fixed underlay; exact production text/numbers/logos are added natively after generation.
2. `PRODUCTION_VISUAL_INGREDIENT` — isolated hero/photo/illustration/texture/icon ingredient.
3. `INTERNAL_VISUAL_CONCEPT` — non-client-facing exploration only.

`GOLDEN_VISUAL_MASTER` may include contextual people, Saudi flags, architecture, devices, screens and dashboard-like cues when relevant. It must not be treated as the source of exact proposal copy, official tender values, or exact Rubix/client brand identity.

A generated full page is production-eligible only after Golden Visual Master Council approval, continuity lock, master hash freeze, and exact native overlay. The composer must not redraw or simplify the approved master.

## Rule 2 — Exact Rubix logo asset lock
Before rendering any page carrying Rubix identity, resolve an **exact embedded current asset** from `08_BRAND_CURRENT/LOGO_ROUTING_AUTHORITY.md`. For consulting proposals the default is:

`08_BRAND_CURRENT/assets/rubix-consulting-current-light.png`

Never ask an image model to draw, reconstruct, restyle, infer, approximate, or embed a Rubix logo. Never substitute typography that spells RUBIX as a logo. Never use a logo from a screenshot, old proposal, generated image, memory, or web search.

If the exact asset cannot be loaded into the production composer, stop with:

`BLOCKED — VERIFIED RUBIX LOGO ASSET NOT INJECTABLE`

## Rule 3 — Client logo lock
Client logo must come from a validated engagement-specific asset. Do not generate it. Record `client_logo_requirement = REQUIRED | OPTIONAL | NOT_REQUESTED`.
- `REQUIRED` + unavailable/uninjectable → BLOCK.
- `OPTIONAL` omission requires an `APPROVAL_LEDGER` record identifying the authorized approver and reason.
- `NOT_REQUESTED` may omit without a visual substitute.
Never infer permission to omit from tool limitations.

## Rule 4 — Arabic production text is native/deterministic
For an Arabic client-facing deliverable:
- all Arabic titles, labels, paragraphs, captions, table text, dates, and numeric values are native text/vector objects;
- ordered flows start physically on the right and progress left;
- Latin acronyms such as `AI`, `POC`, `SLA`, `UAT`, `UI/UX` remain internally LTR and bidi-isolated;
- generated pixels never determine spelling, alignment, direction, or sequence.

If Arabic production text is baked into a generated image, the page fails.

## Rule 5 — Arabic numeral hard lock
**Current user authority:** in Arabic client-facing natural-language content, use Arabic-Indic numerals `٠١٢٣٤٥٦٧٨٩`. Western digit leakage is a blocking error.

Examples:
- `٢٤ موردًا` not `24 موردًا`
- `٣٠ نموذجًا أوليًا` not `30 نموذجًا أوليًا`
- `٢٠ خدمة` not `20 خدمة`
- `١٢ شهرًا` not `12 شهرًا`

Exceptions are limited to machine/technical identifiers whose exact raw form must remain unchanged for correctness, such as URLs, email addresses, source code, hashes, API keys, exact product/version strings, and official reference identifiers when changing their digits would alter the identifier. These exceptions must be visually isolated from Arabic prose.

## Rule 6 — Theme and background lock
Every client-facing page must pass the Theme & Color Governor. Black and near-black full-slide backgrounds are forbidden. For deterministic QA, **near-black** means WCAG relative luminance `Y ≤ 0.04` for the dominant background color or an equivalent rendered sample. Do not use dark legacy masters as fallback. Rashad remains light-first even when a dark color is a valid accent.

## Rule 7 — Deterministic composer requirement
Client-facing production path:

`Content Contract → Artifact Contract → Visual Geometry Spec → Native/Deterministic Composer → Exact Asset Injection → RTL/Numeral/Logo QA → Release`

Image generation may supply either isolated ingredients or the complete approved `GOLDEN_VISUAL_MASTER` underlay. The deterministic composer still owns exact native text, exact logos, placement/provenance and final QA; it must not reconstruct the master into weaker primitives.

If the runtime lacks a deterministic production method capable of separate native text and exact asset injection, return the content/artifact/geometry specification and state:

`BLOCKED — DETERMINISTIC RASHAD PRODUCTION COMPOSER NOT AVAILABLE`

Do **not** fall back to a generic image, generic deck, generic HTML report, or approximate logo and call it Rashad.

## Mandatory pre-render checklist
All must be PASS before the first client-facing render action:

- `artifact_intent_locked = true`
- `visual_generation_mode = GOLDEN_VISUAL_MASTER | PRODUCTION_VISUAL_INGREDIENT | INTERNAL_VISUAL_CONCEPT`
- `verified_rubix_logo_resolved = true` when Rubix identity is visible
- `client_logo_validated = true` when required
- `production_text_native = true`
- `rtl_geometry_deterministic = true` for Arabic
- `arabic_indic_numerals_locked = true` for Arabic natural-language content
- `western_numeral_leakage = 0`
- `black_or_near_black_background = 0`
- `theme_color_governor = PASS`
- `renderer_capability_not_faked = true`

Any failure blocks rendering.

## Post-render release checks
A render is not final until:
- selected Rubix source asset provenance hash matches `LOGO_ROUTING_AUTHORITY`; rendered placement preserves source aspect ratio within ±0.5%, has no crop, mirror or recolor, and uses only scaling/positioning/transparency permitted by the composer;
- no generated/reconstructed logo exists anywhere;
- Arabic reading order is physically RTL;
- Western numeral leakage in Arabic natural-language text = 0;
- no generated Rubix/client identity or authoritative proposal copy is relied on as production truth;
- no black/near-black slide background;
- no clipping, overflow, overlap, or footer collision;
- visual meaning matches the approved Artifact Contract.


## v2.2 logo geometry gate
Pixel-for-pixel equality after raster resizing is **not** the release test because resampling/anti-aliasing changes rendered pixels. Validate instead:
1. source asset SHA-256 provenance before placement;
2. correct logical asset ID;
3. aspect-ratio drift ≤ 0.5%;
4. crop = 0; mirror = false; recolor = false;
5. clear space on all four sides ≥ 0.25 × the visible logo height (Rashad production minimum where the source guideline does not specify a stricter value);
6. visible full-wordmark height ≥ 0.28 in on a 16:9 slide or an equivalent legibility floor in another format;
7. no overlap with trim/safe-area/footer.

## v2.2 execution honesty
This firewall is a policy/gate authority. Passing its documented checks does **not** prove that a renderer, PDF/PPTX parity engine, browser, or test runner exists. Record separately:
- `production_policy_check = PASS | FAIL`
- `production_runtime_available = TRUE | FALSE`
- `render_regression_executed = TRUE | FALSE`
Never convert a written test specification into an execution claim.

## v2.3 internal visual ideation distinction
This firewall does not prohibit **non-client-facing** `INTERNAL_VISUAL_CONCEPT` generation when all conditions in `03_ARTIFACT_ENGINE/28_IMAGE_IDEATION_INTERFACE.md` are met. Such a concept is an ideation reference only: no official text, numbers, dates, logos, client facts, BOQ/evaluation/risk data, or final analytical labels; it must never be embedded as the production page. The useful composition ideas must be translated into a native `VISUAL_BLUEPRINT` before production.

Before client-facing production, additionally require:
- `visual_blueprint_locked = true`
- `geometry_handoff_ready = true`
- `internal_visual_concept_embedded_as_final = false`

These are additive controls and do not weaken any V2.2 rule.

## v2.5 product/orchestration lock
Passing this firewall does not complete an artifact product. The Product Completion Contract and Release Completion Gate are separate mandatory authorities.

- `cover_hero_generated = true` is never a completion condition.
- after any image-generation substep, control returns to the Artifact Production Orchestrator;
- `deterministic_composer_required = true` for artifact products;
- generic renderer/image/document availability alone never satisfies capability preflight;
- Arabic RFP Summary cover composition follows `39_ARABIC_COVER_COMPOSITION_AUTHORITY.md` unless explicitly overridden by the current user.
## v2.6.4.2 canonical render compiler preflight
Before a final client-facing format render, additionally require:
- `canonical_page_spec_locked = true`;
- `canonical_scene_graph_resolved = true`;
- `direction_policy_resolved = true`;
- `directional_zones_resolved = true` for mixed-direction pages;
- `connector_geometry_rebuilt_after_direction = true` for direction-sensitive artifacts;
- `text_fit_preflight = PASS`;
- `font_preflight = PASS`;
- `asset_hash_preflight = PASS` for governed assets;
- `renderer_adapter_uses_shared_scene_graph = true`.

Do not claim any of these runtime checks passed unless they were actually executed in the active environment.


## v2.6.4.3 image-isolation and evidence-backed release extension
Before any production-asset image call additionally require:
- `isolated_visual_asset_brief_locked = true`;
- `context_isolation_status = ISOLATED` or an explicitly approved low-risk equivalent;
- `forbidden_document_chrome = true`;
- `forbidden_text_logo_number_data = true`;
- `image_generator_not_authority_for_page_layout = true`.

After generation require `03_ARTIFACT_ENGINE/73_GENERATED_ASSET_ADMISSION_QA.md`. A generated slide/page, pseudo-text, numeral, logo-like mark, document chrome, cards/tables/dashboard, or final analytical topology rejects the asset.

Machine-verifiable gates use `GATE_DEFINED | NOT_EXECUTED | PASS | FAIL | BLOCKED | N_A`. Runtime PASS requires `evidence_id`. If a required executable production gate is unavailable or unexecuted, final client-facing production release is BLOCKED.

## v2.6.4.4 supersession of strict page-isolation rule
The v2.6.4.3 rule that rejected any slide-like generated composition is superseded for `GOLDEN_VISUAL_MASTER` mode. Full-page visual composition is now explicitly allowed. Exact logos, official copy/numbers and factual labels remain native-overlay authorities. Contextual flags/screens/devices/dashboard-like scene elements are allowed.
