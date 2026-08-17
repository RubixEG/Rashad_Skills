MODULE: 03_ENGAGEMENT_RESET_AND_SOURCE_GROUNDING
STATUS: AUTHORITATIVE
LOAD WHEN: Start of every new engagement; whenever switching clients/RFPs; before any client-facing claim; whenever contamination risk appears; whenever classifying facts vs inferences.
DEPENDS ON: 00_START_HERE; 02_AUTHORITY_AND_DECISIONS
DO NOT APPLY TO: Carrying prior engagement facts “for convenience”; using historical proposals as factual authority; treating Human Approved Baseline / dimension_scores as generation context; letting model/engagement booleans decide clarification window.
SUPERSEDES: Cross-engagement memory reuse of client facts; VIS-KB-001 as production memory; global Golden MWAN as default baseline; model-decided `clarification_period_open`; presenting inferences as RFP requirements.

# Engagement Reset and Source Grounding

## Why this module exists

Rashad previously suffered **cross-engagement contamination** (wrong client name/logo/sector/facts leaking into a new bid). That is a hard integrity failure. This module is absolute.

## ENGAGEMENT_RESET — mandatory start state

At the beginning of **every** new engagement initialize:

```text
CURRENT_ENGAGEMENT_ID
CURRENT_CLIENT
CURRENT_CLIENT_LOGO_SOURCE
CURRENT_PROJECT
CURRENT_SECTOR
CURRENT_RFP_SOURCES
CURRENT_RFP_LANGUAGE
SOURCE_NUMERAL_STYLE
CURRENT_VISUAL_THEME
CURRENT_PRODUCT
CURRENT_SECTION
CURRENT_EVIDENCE_LIBRARY
```

Clear prior engagement values. Do not soft-merge.

## Never carry (HARD FAIL if previous client appears)

Do **not** carry into a new engagement:

- client name / logo
- project title
- sector imagery
- dates / numbers / facts
- BOQ
- team facts
- maturity assessment
- bid decision
- evaluation weights
- commercial terms
- risks / deliverables / scope (unless independently supported by **current** RFP)

`previous_client_in_new_engagement` = **HARD FAIL**.  
Target: `cross_engagement_contamination = 0`.

## What history may contribute (style only)

Historical engagements / proposals may provide **only**:

- visual grammar
- artifact patterns
- reasoning methodology
- consulting structure
- storytelling patterns
- spacing / quality precedent
- workflow and failure lessons

via **ExternalProposalReferenceSession** / abstract `ReferencePatternRegistry` — never as automatic fact injection. VIS-KB-001 is **DEPRECATED** as production authority.

## Pre-release gates (blocking)

Before anything client-facing:

1. `CLIENT_IDENTITY_GATE`
2. `CLIENT_LOGO_GATE`
3. `SECTOR_CONTAMINATION_GATE`
4. `CROSS_ENGAGEMENT_MEMORY_GATE`
5. `SOURCE_FACT_GATE`
6. `LANGUAGE_GATE`
7. `RTL_LTR_GATE`
8. `NUMERAL_STYLE_GATE`

Any blocking failure ⇒ **DO NOT RELEASE**.

## Source classification (every material statement)

Assign one status to every important statement:

| Status | Meaning |
|---|---|
| `SOURCE_FACT` | Explicitly supported by current pack excerpt + locator |
| `DERIVED_CALCULATION` | Deterministic calc from sourced inputs (show inputs) |
| `CONSULTING_INFERENCE` | Expert reading of sourced facts — labeled as interpretation |
| `RUBIX_RECOMMENDATION` | Council/Rubix advice — not an RFP requirement |
| `ASSUMPTION` | Explicit default when window closed / gap material |
| `UNRESOLVED_CONFLICT` | Sources disagree — show both |
| `MISSING_SOURCE` | Referenced but absent |

Evidence-label vocabulary also used in ingestion/QA:

`VERIFIED` | `STATED_FACT` | `EVIDENCE_BASED_INFERENCE` | `ASSUMPTION` | `ATTRIBUTION_NOT_VERIFIED` | `SOURCE_AVAILABLE` | `CURRENT_VALIDITY_NOT_VERIFIED` | `NO_EVIDENCE` | `MISSING` | `CONFLICT` | `BLOCKED` | `REFERENCE_ONLY` | `NOT_EVIDENCE`

Content fact kinds in Summary contracts:

`RFP_REQUIREMENT` | `RASHAD_INTERPRETATION` | `COUNCIL_RECOMMENDATION`

### Forbidden conversions

- `MISSING` → `FACT`
- `COUNCIL_RECOMMENDATION` → `RFP_REQUIREMENT`
- `INTERPRETATION` → `SOURCE_CLAIM`
- Invented dates, quantities, weights, team requirements, duration, SLAs, technologies, certifications, commercial terms, evaluation rules

Every extracted item needs: source file, page/line or excerpt pointer, classification, owner, status, downstream refs.

## Derived clarification window (not a boolean guess)

`clarification_period_open` / engagement booleans are **non-authoritative**. Derive `ClarificationWindowState`:

**Precedence:**

1. Latest verified tender addendum / deadline extension → status `EXTENDED` or `CLOSED`
2. Verified clarification deadline from procurement pack → `OPEN` or `CLOSED`
3. Verified tender metadata fallback → `OPEN` or `CLOSED` (medium confidence)
4. Else `UNKNOWN` (do not trust booleans)

Fields to preserve:

- `status`
- `deadline_source_value`
- `deadline_source_calendar`
- `deadline_source_refs`
- `deadline_normalized_gregorian`
- `addendum_source_refs`
- `evaluated_at`
- `derivation_method`
- `confidence`
- `conflict`
- `conflict_notes`
- `closed_routing`

`deadline_normalized_gregorian` = optional `DERIVED_CALCULATION` used for countdown logic only. It must never silently replace the source date in client-facing outputs.

Model cannot win: overwrite model-emitted open/closed with derived state; strip `clarification_period_decided_by_model`.

### When status = CLOSED

Do **not** merely tell the user “ask the client.” Route:

```text
CHECK_ETIMAD_QA → CHECK_ADDENDA → BID_ASSUMPTION → DEPENDENCY
→ COMMERCIAL_PROTECTION → CONTRACT_RECONCILIATION
```

Create explicit assumption, dependency, risk, mitigation, commercial protection, and internal decision point as appropriate.

### When status = OPEN

Admit only Expert Clarification questions that pass admission (see `06_RFP_SUMMARY.md`).

### When status = UNKNOWN

Do not invent a window. Prefer assumption / dependency / risk labeling; seek verified deadline evidence.

## Benchmark / baseline isolation

Human Approved Baseline, `dimension_scores`, `overall_score`, `expected_verdict`, quality targets must **never** enter Stage A / Stage B / Council / Repair generation context. They belong only to independent parity evaluation **after** the Final Candidate. Generation pack ≠ evaluation context.

## Context assembly order (selective)

1. System authority (this pack + immutable masters)
2. Current engagement state (post-reset)
3. RFP evidence
4. Appendix evidence matches/gaps
5. Retrieved exact Rashad blocks (by need)
6. Page / artifact contracts
7. Council routing
8. QA rules

Never send the complete ChatGPT transcript on every request.

## Logo signature

Client-facing logo signature: **Rubix | Client**. Logo signature is **not mirrored** under RTL.

## Sources and authority

- User master prompt §§6, 21, 25 (2026-08-10)
- CONF-003, CONF-004, CONF-007
