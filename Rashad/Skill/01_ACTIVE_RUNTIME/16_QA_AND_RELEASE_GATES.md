MODULE:
QA_AND_RELEASE_GATES

STATUS:
AUTHORITATIVE

LOAD WHEN:
Any client-facing draft, visual, PDF/PPTX candidate, appendix package, or release decision is under review; after content or artifact planning; before release lock.

DEPENDS ON:
00_START_HERE
03_ENGAGEMENT_RESET_AND_SOURCE_GROUNDING
04_LANGUAGE_RTL_LTR_NUMERALS
09_COUNCILS_AND_ROLES
10_ARTIFACT_ENGINE
13_RUBIX_DECK_AND_BRAND
17_APPENDIX_AND_EVIDENCE
19_FAILURE_PATTERNS
20_CONTEXT_LOADING_PROTOCOL
CURRENT_RFP_SOURCES (engagement-local)

DO NOT APPLY TO:
Internal working notes requested by the user; non-client diagnostics where metadata visibility is explicitly allowed; historical corpus browsing that is Style/Golden reference only.

SUPERSEDES:
Informal “looks good” release; Safety-only pass without strength; Global Golden MWAN as release authority; generator self-approval as proof.

CLASSIFICATION:
Reusable Rashad operating rules. Not current RFP factual truth.

---

# QA and Release Gates

## Authority split

| Layer | What is true | May block release |
|---|---|---|
| **Current RFP truth** | Facts, deadlines, roles, evaluation, BOQ, clarifications from the active engagement pack | Unsupported client facts, invented weights/dates/terms, unresolved material conflicts |
| **Reusable Rubix evidence** | CV/case/cert library indexes, brand/deck rules, QA contracts | Validity gaps, role conflicts, fabrication, expired required docs, wrong brand |
| **Benchmark / Golden references** | Structure and strength comparison only | Never become current-client facts; never enter generation context as score targets |

## Canonical QA stack (must all run)

Order is fixed. Later gates may fail a pack; they may not rewrite earlier meaning.

1. **Content QA**
2. **Source QA**
3. **Artifact QA** (semantic non-regression)
4. **Geometry QA**
5. **Language / RTL / numerals QA**
6. **Brand QA**
7. **Appendix evidence gates A0–A3** (when evidence is in scope)
8. **Safety / prepress** (layout only; cannot change artifact family)
9. **Red Team / Release**
10. **Parity** (HTML ↔ PDF ↔ PPTX / Golden visual) when a visual release candidate exists

## Content QA

Before release verify:

- page answers an executive/evaluator question
- thesis exists and is distinct from adjacent pages
- evidence supports thesis
- no generic filler or unnecessary repetition
- no invented requirement
- no historical-client contamination
- language follows RFP
- slide justifies its existence
- internal source-coverage remains internal (not a client-facing Summary page unless user explicitly requests it)

Hard counters:

```text
unsupported_client_fact = 0
invented_evaluation_weight = 0
invented_team_requirement = 0
invented_date = 0
invented_quantity = 0
invented_commercial_term = 0
cross_engagement_contamination = 0
generic_clarifications = 0
etimad_naive_questions = 0
```

## Source QA

- Every material claim maps to a source locator or is labeled `MISSING` / `ASSUMPTION` / `CONFLICT`.
- Current RFP pack is the only factual authority for the engagement.
- Reusable Rubix appendix assets are candidates, not automatic proof of RFP fit.
- Presence of a certificate/CV/case page is not proof of current validity or role fit.

## Artifact QA (semantic non-regression)

```text
semantic_node_loss = 0
semantic_edge_loss = 0
artifact_family_changed = false
generic_card_fallback = false   # unless explicitly justified and approved
reading_path_clear = true
focal_point_clear = true
artifact_supports_thesis = true
strength_after_gte_strength_target = true
```

Baseline for strength is the **current engagement approved page contract / Current Engagement Baseline**, not a global Golden MWAN gate.

Global Golden MWAN authority is **REMOVED**. MWAN materials may be used only as a temporary engagement baseline when explicitly supplied for that engagement.

## Geometry QA

```text
overflow = 0
clipping = 0
unintended_overlap = 0
text_connector_collision = 0
protected_zone_violation = 0
logo_collision = 0
unsafe_font_shrink = 0
```

Release levels (canonical contracts):

1. L1 object geometry  
2. L2 glyph/text geometry  
3. L3 raster visual QA  
4. L4 PPTX/PDF parity  
5. L5 semantic topology preservation  

## Language / RTL / numerals QA

```text
wrong_language_heading = 0
english_heading_leakage = 0
english_subtitle_leakage = 0
avoidable_english_label_leakage = 0
unnecessary_english = 0
rtl_error = 0
ltr_token_error = 0
reversed_acronym = 0
numeral_style_error = 0
punctuation_direction_error = 0
```

Image models must never decide final language, numeral system, or RTL geometry. Deterministic Rashad gates own those decisions. For Arabic engagements, `33_ARABIC_VISIBLE_LANGUAGE_PURITY_GATE.md` is a blocking sub-gate.

## Brand QA

```text
wrong_logo = 0
historical_client_logo = 0
logo_distortion = 0
wrong_background_policy = 0
wrong_font = 0
wrong_master_or_theme = 0
unapproved_black_background = 0
near_black_forbidden = true
```

Never generate logos. Use verified assets only.

## Derived clarification window gate

Clarification open/closed status is **derived**, never decided by the model or by engagement/pack boolean flags.

Precedence:

1. Latest verified tender addendum / deadline extension  
2. Verified clarification deadline from procurement pack  
3. Verified tender metadata  
4. `UNKNOWN`

When status = `CLOSED` / not reliably open:

- do not tell the user only to “ask the client”
- route: check Etimad Q&A/addenda → explicit assumption → dependency → risk → mitigation → commercial protection → internal decision point

Hard telemetry:

```text
clarification_window_conflict = 0
model_cannot_override_clarification_window = true
```

## Benchmark isolation gate

`GENERATION_CONTEXT` must never contain evaluation-only benchmark fields (dimension scores, expected verdicts, human evaluator scores, quality targets, parity baselines used as generation targets).

```text
benchmark_context_leakage = 0
```

`EVALUATION_CONTEXT` may include human-approved baselines **after** generation, for independent parity review only. Generator self-score is never proof.

## Dual release principle (Safety ≠ Strength)

A page that is safer but weaker fails.

| Gate | Pass condition |
|---|---|
| Safety Gate | geometry, RTL, numerals, logos, fonts, parity clean |
| Strength Gate | correct relationship→artifact mapping; no generic-card collapse; evaluator-useful focal thesis preserved |

Both must pass for visual release.

## Final client-facing release blockers

A client-facing artifact is not releaseable until:

```text
semantic_parity = 100%
node_loss = 0
edge_loss = 0
overflow = 0
clipping = 0
unintended_overlap = 0
rtl_error = 0
language_error = 0
numeral_error = 0
logo_error = 0
cross_engagement_contamination = 0
unsupported_client_fact = 0
internal_metadata_visible = 0
unresolved_blocking_findings = 0
```

If Golden Visual comparison is required:

```text
visual_parity_target >= 95%
```

Never trade semantic accuracy for visual parity.

## PDF / PPTX release notes

- HTML approval alone does not release PDF.
- No full-slide screenshot substitution for PPTX.
- Spec-First Native Twin: Golden visual and Native PPTX are siblings under one visual spec; parity QA follows.
- Critical page parity target ≥ 95%; overall ≥ 92% when that contract applies.

## Internal metadata (never on client slides)

Do not expose council names, R-codes, source-confidence labels, QA counters, prompt IDs, engagement-state fields, or debugging labels unless the user explicitly requests an internal working deck.

## Appendix release counters (when appendix in scope)

```text
required_roles_executed = 100%
unresolved_blocking_findings = 0
unsupported_appendix_claims = 0
expired_required_documents = 0
unresolved_role_fit_conflicts = 0
source_locator_coverage = 100%
```

## Canonical state vs release

| Canonical node state | Releaseable? |
|---|---|
| NOT_STARTED / DRAFT / REVIEW_REQUIRED / STALE / BLOCKED / REJECTED / SUPERSEDED | No |
| APPROVED | No — approved for its current production stage only |
| LOCKED | Only when `PRODUCTION_STAGE=RELEASE` and `RELEASE_GATE=PASS` |

## Source paths

| Path | Role |
|---|---|
| `_forensic_work\master_prompt_extract.txt` (§37–§44, §50, §58–§59) | Master QA / release / loading rules |
| `09_APPENDIX_EVIDENCE/08_APPENDIX_EVIDENCE_COUNCIL_AND_GATES.md` | A0–A3 appendix gates |
| `07_GOVERNANCE_AND_QA/48_FINAL_RELEASE_EVIDENCE_AGGREGATION_GATE.md` | PDF release authority |
| `13_ARTIFACT_QUALITY_FLOOR_AND_GOLDEN_BENCHMARK_GATE.md` | Safety vs strength dual gate |
| `07_GOVERNANCE_AND_QA/57_FINAL_A_TO_Z_RELEASE_COUNCIL.md` | Historical gate checklist (reference) |
| `10_PROVENANCE/ENGINEERING_HISTORY.md` | Derived clarification window + benchmark isolation |
| `PROJECT_INSTRUCTIONS.md` | Project behavior constraints |

## v2.1 Production Firewall QA — blocking
Before render and again before release:

```text
production_firewall = PASS
full_slide_image_generation = 0
generated_production_text_pixels = 0
generated_logo_pixels = 0
verified_rubix_logo_source_provenance = PASS
rubix_logo_aspect_ratio_drift_le_0_5_percent = PASS
rubix_logo_crop_mirror_recolor = 0
rubix_logo_clear_space_and_min_size = PASS
western_numeral_leakage_in_arabic_prose = 0
rtl_physical_order_error = 0
black_or_near_black_background = 0
renderer_capability_faked = 0
```

Any non-zero failure blocks client-facing output. A visually attractive output does not override these gates.
