MODULE:
IMAGE_BATCH_AND_PHASE_POLICY

STATUS:
AUTHORITATIVE_POLICY — EXECUTION_CONDITIONAL_ON_CHATBOT_TOOLS

LOAD WHEN:
Planning or executing multi-image production for a deliverable; enforcing phase consistency; running image-phase QA.

DEPENDS ON:
14_IMAGE_GENERATION_POLICY
13_RUBIX_DECK_AND_BRAND
BRAND/DESIGN_TOKENS
VISUAL_PHASE_LOCK_TEMPLATE
10_ARTIFACT_ENGINE
04_LANGUAGE_RTL_LTR_NUMERALS

DO NOT APPLY TO:
Blind full-deck image dumps; continuing after failed batch QA; treating Concept Mode dumps as final pages; reintroducing historical Phase 5B image blocks as chatbot authority.

SUPERSEDES:
All-20-at-once generation as default; Phase 2 aesthetic drift; skipping LANGUAGE/RTL/LOGO QA between phases.

---

# Image Batch and Phase Policy

## Execution gate

Batching rules are **authoritative** and always apply to image production.  
**Execute image batches when the current chatbot has an image-generation tool:**

```text
IMAGE GENERATION = EXECUTE_WHEN_CHATBOT_TOOL_AVAILABLE
BATCH DISCIPLINE = MANDATORY (max 20 per major phase; 3–5 per operational batch; QA between)
```

When the isolated-asset gate cannot authorize generation (including no image tool or non-isolatable context), produce batch-organized image briefs instead. Historical application-runtime image blocks (Phase 5B / Luna / certification) are recorded only in `10_PROVENANCE/ENGINEERING_HISTORY.md` and do not govern chatbot behavior.

## Source paths

- Master Context Engineering Prompt §§16–18
- `14_IMAGE_GENERATION_POLICY.md` (this package)
- `VISUAL_PHASE_LOCK_TEMPLATE.md` (this package)
- `BRAND/DESIGN_TOKENS.md`
- `10_PROVENANCE/ENGINEERING_HISTORY.md`

## Major phase size = 20 images maximum

| Total images needed | Major phases |
|---|---|
| 1–20 | One phase |
| 21–40 | Exactly two phases: 1–20, 21–40 |
| 41–60 | Three phases: 1–20, 21–40, 41–60 |
| 61+ | Continue; **maximum 20 images per major phase** |

Never create a major phase larger than 20.

## Operational batches inside a major phase = 3–5 images

Do **not** request all 20 simultaneously when smaller batches are more stable.

Recommended pattern for Phase 1 (slides/images 1–20):

| Batch | Range |
|---|---|
| A | 1–5 |
| B | 6–10 |
| C | 11–15 |
| D | 16–20 |

Use 3–5 images per generation batch (example above uses 5). Prefer 3 when failure rate is high.

## Validate before continuing

After **each** operational batch:

1. Inspect outputs against brief and provenance rules
2. Run applicable QA gates (below)
3. Repair or discard failures
4. Only then start the next batch

```text
Do not continue blindly after a failed batch.
```

## Phase consistency lock

Between major phases, preserve exactly the same:

- Rubix visual language
- Current client identity
- RFP language
- Numeral style
- Typography rules
- Color tokens
- Background policy
- Logo placement
- Artifact grammar
- Section markers
- Spacing rhythm
- Icon grammar
- Image aesthetic
- Light-background policy (Aug 8)

Do not allow Phase 2 to become visually different from Phase 1.

**Required artifact before Phase 2+:** fill `VISUAL_PHASE_LOCK_TEMPLATE.md` (or engagement copy `01_ACTIVE_RUNTIME/VISUAL_PHASE_LOCK_TEMPLATE.md`) with locked constants. Exact unverified token values → `UNKNOWN` / `ASSET_INSPECTION_REQUIRED` (never invent).

## Image phase QA (blocking)

Before moving to another major image phase, run:

| Gate | Intent |
|---|---|
| `LANGUAGE_QA` | Correct engagement language; no contamination |
| `RTL_QA` | Direction, ordered sequences, BiDi isolation |
| `NUMERAL_QA` | Arabic client-facing natural-language content uses Arabic-Indic numerals; immutable technical/reference identifiers retain exact raw form; no image-decided formatting |
| `LOGO_QA` | Verified assets only; clear space; no mirror misuse |
| `CLIENT_IDENTITY_QA` | Current client only |
| `SECTOR_CONTAMINATION_QA` | No prior-engagement sector bleed |
| `VISUAL_CONSISTENCY_QA` | Matches Visual Phase Lock |
| `ARTIFACT_FIDELITY_QA` | Analytical meaning still native/hybrid; no card collapse |

If blocking failures exist, **repair the current phase before continuing**.

## Interaction with Artifact Engine

Image batches support covers / openers / secondary illustration. They do **not** replace Artifact Engine analytical pages. Artifact Council remains before Safety; generic-card fallback remains forbidden.

## Operator checklist (when the isolated-asset gate permits generation)

1. Confirm the chatbot actually has an image-generation tool (do not assume)
2. Confirm content + artifact intents are stable
3. Split work into ≤20 major phases
4. Split each phase into 3–5 image batches
5. Write Visual Phase Lock before Phase 2
6. QA after every batch and every phase
7. Stop on blockers; no silent continue
