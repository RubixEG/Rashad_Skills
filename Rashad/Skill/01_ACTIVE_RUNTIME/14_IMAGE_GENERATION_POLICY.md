MODULE:
## v2.3 mandatory image/production gate
Before any image-generation call related to an artifact, load `29_PRODUCTION_EXECUTION_FIREWALL.md` **and** `03_ARTIFACT_ENGINE/28_IMAGE_IDEATION_INTERFACE.md`.

There are only two permitted modes:
- `INTERNAL_VISUAL_CONCEPT` — a non-client-facing, non-authoritative composition reference with no official text, numbers, dates, logos, client facts, or final analytical labels; never embedded as production.
- `PRODUCTION_VISUAL_INGREDIENT` — an isolated text-free/logo-free/number-free/fact-free hero, illustration, texture, background, or icon concept.

**Never generate a full client-facing production slide/page/deck preview.** If a requested call would bake production titles, body copy, labels, page numbers, dates, logos, tables, timelines, Arabic numerals, BOQ/evaluation/risk data, or authoritative analytical structures into pixels, do not call the image model.

IMAGE_GENERATION_POLICY

STATUS:
AUTHORITATIVE_POLICY — GOLDEN_VISUAL_MASTER_OR_ISOLATED_ASSET_GATE

LOAD WHEN:
Any request to generate, reuse, or brief imagery for covers, section openers, or decorative support; deciding native vs raster-augmented pages.

DEPENDS ON:
10_ARTIFACT_ENGINE
12_STORYTELLING_AND_VISUAL_INTELLIGENCE
13_RUBIX_DECK_AND_BRAND
15_IMAGE_BATCH_AND_PHASE_POLICY
04_LANGUAGE_RTL_LTR_NUMERALS
BRAND/DECK_AUTHORITY

DO NOT APPLY TO:
Using image models for authoritative analytical content; inventing logos/seals/screenshots; letting an image model choose language or alter facts; treating generated-image text as authoritative.

SUPERSEDES:
Full-page final slides as single generated images; accepting generated Arabic/English text as source of truth; Concept Mode as production delivery.

---

# Image Generation Policy

## Execution gate

Image generation policy is **authoritative knowledge** and always active.  
**Image generation is permitted only through the v2.6.4.3 isolated-asset gate** (`44_IMAGE_GENERATION_ISOLATION_AND_ASSET_QA_CONTRACT.md` / `03_ARTIFACT_ENGINE/72_IMAGE_GENERATION_ISOLATION_GATE.md`). Image-tool availability alone is not sufficient. When no image tool is available—or when the environment cannot safely isolate a high-risk production asset—Rashad produces an image brief / visual specification or uses `REFERENCE_ONLY`.

```text
IMAGE GENERATION = EXECUTE_ONLY_THROUGH_ISOLATED_ASSET_GATE (else brief/reference-only/block)
ANALYTICAL TRUTH = NATIVE/HYBRID, ARTIFACT-ENGINE-LED (never image-model text)
```

Historical application-runtime image blocks (Phase 5B / Luna / certification) are recorded only in `10_PROVENANCE/ENGINEERING_HISTORY.md` and do not govern chatbot behavior.

Do not imply the runtime can call image models or inject production assets today.

## Source paths

- `03_ARTIFACT_ENGINE/14_IMAGE_GENERATION_DECISION_ENGINE.md`
- `03_ARTIFACT_ENGINE/07_IMAGE_ICON.md`
- `03_ARTIFACT_ENGINE/15_VISUAL_ASSET_BRIEF_SCHEMA.md`
- `08_BRAND_CURRENT/LOGO_ROUTING_AUTHORITY.md`
- Master Context Engineering Prompt §§12–15, §32

## v2.6.4.3 isolation rule

A production-asset prompt must describe the **visual asset itself**, not a slide/deck/report/RFP page. Avoid passing final page title/body, official figures, logos, page numbers, tables/cards, final analytical structure, full conversation, or full RFP pack. Explicitly prohibit presentation/document chrome. If the result contains forbidden baked content, reject the entire asset.

## Allowed uses (when the isolated-asset gate permits generation)

Use image generation primarily for:

- Cover hero imagery (**must be strictly text-free**)
- Conceptual visuals
- Atmospheric backgrounds
- Sector imagery
- Decorative illustration
- Icon *concepts* to be vectorized into the Rubix icon family

## Forbidden uses

Do **not** rely on image generation for authoritative analytical content:

- Exact Arabic (or English) paragraphs
- Tables / BOQ
- Timelines / process maps / architecture diagrams
- Team matrices / evaluation logic / compliance matrices
- Exact numbers / contractual facts
- Client or Rubix logos
- Official seals, certificates, signatures
- Fake screenshots / fabricated UI
- Unapproved portraits / identifiable staff likenesses
- Third-party marks and watermarks
- Client-specific confidential elements

## Hard principle

```text
GENERATED IMAGE TEXT IS NEVER AUTHORITATIVE.
```

Image models may hallucinate English labels, reverse Arabic, corrupt shaping, reorder numbers, invent logos, alter quantities, and mix RTL/LTR incorrectly. Numeral formatting must not be decided by generated pixels.

## Correct production path (analytical pages)

```text
CONTENT
→ STRUCTURED ARTIFACT
→ DETERMINISTIC GEOMETRY
→ NATIVE TEXT
→ QA
```

Not:

```text
CONTENT → IMAGE MODEL → ACCEPT IMAGE TEXT
```

## Cover rule

1. Generate strictly text-free isolated hero visual (when the isolated-asset gate permits generation)
2. Overlay exact project title, client name, section markers, Rubix identity as **native text/assets**
3. Never ask the model to invent a client logo

## Analytical slides

Analytical slides are Artifact Engine outputs. Imagery may provide secondary illustration, texture, or small conceptual support. Core remains:

| Page type | Core |
|---|---|
| Scope architecture | native/vector artifact |
| Evaluation logic | native artifact |
| Team matrix | native table/matrix |
| Governance | native governance model |
| Roadmap | native timeline |
| Risk register | native risk artifact |
| Compliance | native table |

Modes: `FULLY_NATIVE` | `VECTOR_HYBRID` | `RASTER_AUGMENTED` (canonical v2.5 editability vocabulary; image mode is a separate axis).

## Decision outcomes

- `NO_ASSET_NATIVE_ARTIFACT`
- `REUSE_APPROVED_ASSET`
- `GENERATE_PRODUCTION_HERO`
- `GENERATE_PRODUCTION_ILLUSTRATION`
- `GENERATE_ICON_CONCEPT_AND_VECTORIZE`
- `GENERATE_INTERNAL_VISUAL_CONCEPT_THEN_BLUEPRINT`
- `REFERENCE_ONLY`

Generation requires positive net contribution vs hallucination risk. Decorative novelty alone is insufficient.

## Whole-page composition ideation

Permitted only as `INTERNAL_VISUAL_CONCEPT`: a non-client-facing, unlabeled, non-authoritative spatial composition reference. It must comply with `03_ARTIFACT_ENGINE/28_IMAGE_IDEATION_INTERFACE.md`, contain no production text/logos/numbers/dates/client facts, and be translated into a native Visual Blueprint before production. It is never embedded as the final proposal page.

## Provenance classes

- `OWNED_APPROVED`
- `GENERATED_APPROVED`
- `LICENSED_RESTRICTED`
- `OFFICIAL_PUBLIC`
- `REFERENCE_ONLY`
- `PROHIBITED`

Selection priority: exact current brand assets → owned/approved → generated-approved → new briefed generation → native vector/shape fallback.

## Arabic text / RTL rules for imagery

- Do not bake Arabic body copy into pixels
- Do not bake logos into pixels
- Direction, numerals, and labels belong to native renderer / text layer
- If Arabic must appear near imagery, it is native overlay under RTL rules (`04_LANGUAGE_RTL_LTR_NUMERALS`)

## Logo rules (image context)

- Never generate logos
- Never reuse historical client logos
- Never mirror co-brand signature solely for RTL
- Inject verified assets only after logo QA

## Batching

When the isolated-asset gate permits generation, follow `15_IMAGE_BATCH_AND_PHASE_POLICY.md` and run `03_ARTIFACT_ENGINE/73_GENERATED_ASSET_ADMISSION_QA.md` before any asset enters composition.


## v2.6.4.4 primary page-generation mode
For page-level visual production, `GOLDEN_VISUAL_MASTER` is permitted and preferred when it preserves consulting-grade artifact strength better than native reconstruction. It is generated one page at a time under persistent visual anchors and then receives native exact text/logo overlays.

Contextual Saudi flags, people, devices, screens, dashboards and environmental signage are allowed when relevant. They are never treated as exact source evidence or brand identity.
