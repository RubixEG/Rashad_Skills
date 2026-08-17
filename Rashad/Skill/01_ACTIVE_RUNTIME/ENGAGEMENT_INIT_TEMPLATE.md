MODULE: ENGAGEMENT_INIT_TEMPLATE
STATUS: AUTHORITATIVE_TEMPLATE
LOAD WHEN: Start of every new engagement; before any client-facing output.
DEPENDS ON: PROJECT_INSTRUCTIONS; 03_ENGAGEMENT_RESET_AND_SOURCE_GROUNDING; 05_RFP_INGESTION; current RFP pack.
DO NOT APPLY TO: Resuming an already-initialized engagement (use ENGAGEMENT_STATE instead); promoting historical RFPs into permanent Sources.
SUPERSEDES: Implicit reuse of prior chat client/logo/facts; starting Summary generation without inventory + gate pass.

---

# Engagement Init Template

Copy into a new engagement chat and fill every field. Mark UNKNOWN rather than inventing.

## Identity block

```text
CURRENT_ENGAGEMENT_ID:
CURRENT_CLIENT:
CURRENT_CLIENT_LOGO_SOURCE:   # VERIFIED path or BLOCK
CURRENT_PROJECT:
CURRENT_SECTOR:
CURRENT_RFP_SOURCES:          # chat/engagement uploads only — not Project Sources
CURRENT_RFP_LANGUAGE:         # ar | en | mixed (state primary)
SOURCE_NUMERAL_STYLE:         # observation only, as evidenced in RFP
ARABIC_OUTPUT_NUMERAL_POLICY: ARABIC_INDIC_IN_ARABIC_PROSE  # current explicit user authority
CURRENT_VISUAL_THEME:         # current Rubix deck authority; not prior client theme
CURRENT_PRODUCT:              # e.g. RFP_UNDERSTANDING_SUMMARY | SECTION | …
CURRENT_SECTION:
CURRENT_EVIDENCE_LIBRARY:     # Appendix library status: PRESENT | APPENDIX_LIBRARY_MISSING
SOURCE_PACK_MODE:             # SCOPE_ONLY | PARTIAL_RFP_PACK | FULL_RFP_PACK
```

## Mandatory preflight gates (blocking)

Run before any client-facing page:

| Gate | Result (PASS / FAIL / N_A) | Evidence |
|---|---|---|
| CLIENT_IDENTITY_GATE |  |  |
| CLIENT_LOGO_GATE |  |  |
| SECTOR_CONTAMINATION_GATE |  |  |
| CROSS_ENGAGEMENT_MEMORY_GATE |  |  |
| SOURCE_FACT_GATE |  |  |
| LANGUAGE_GATE |  |  |
| RTL_LTR_GATE |  |  |
| NUMERAL_STYLE_GATE |  |  |

Any **FAIL** on a blocking gate = **DO NOT RELEASE**.

## Source inventory (required)

1. List all uploaded RFP files (name, type, role).
2. Classify: PRIMARY_RFP | ANNEX | BOQ | CLARIFICATION | REFERENCE_ONLY | DUPLICATE | CONFLICT | MISSING.
3. Create Source Manifest.
4. **Wait for approval** before RFP Understanding Summary content (unless user explicitly overrides wait).

## Historical contribution rules

Historical engagements **may** contribute: visual grammar, artifact patterns, methodology, storytelling, spacing/quality/workflow/failure lessons.

Historical engagements **must never** auto-contribute: client identity, logo, project title, sector, imagery, facts, dates, quantities, evaluation weights, prices, commitments, copied wording.

## After init

1. Write `01_ACTIVE_RUNTIME/ENGAGEMENT_STATE_TEMPLATE.md` from `ENGAGEMENT_STATE_TEMPLATE.md`.
2. Load context per `20_CONTEXT_LOADING_PROTOCOL.md`.
3. Proceed to Adaptive RFP Understanding Summary **content** (artifact render still blocked in Phase5A official state unless separately authorized later).
