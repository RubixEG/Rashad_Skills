# 34 — Rashad Product Router & Registry

STATUS: **HARD ROUTING AUTHORITY — v2.5**
PURPOSE: Prevent domain product names from collapsing into generic chat meanings.

## Domain-name precedence
When Rashad is active, a defined Rashad product name overrides the generic conversational meaning unless the user explicitly requests another delivery mode.

| User intent / phrase | Product ID | Default delivery |
|---|---|---|
| RFP Summary / Create the RFP Summary | `INTERNAL_PURSUIT_BRIEF` | `ARTIFACT` |
| Client RFP Understanding | `CLIENT_FACING_RFP_UNDERSTANDING` | `ARTIFACT` |
| Proposal / Technical Proposal | `FULL_TECHNICAL_PROPOSAL` | `ARTIFACT` |
| Proposal Section / Section N | `PROPOSAL_SECTION` | `ARTIFACT_SPEC` progressing to artifact when requested/required by workflow |
| Analyze RFP / RFP analysis | `RFP_ANALYSIS` | `CONTENT` |
| Content only / no artifact | `CONTENT_ONLY` | `CONTENT` |
| Artifact spec / blueprint only | `ARTIFACT_SPEC` | `ARTIFACT_SPEC` |

## Hard default for RFP Summary
`RFP Summary` is a named Rashad OS product, not a generic text-summarization verb.

Route:
```text
PRODUCT_ID = INTERNAL_PURSUIT_BRIEF
DELIVERY_MODE = ARTIFACT
CONTENT_ONLY = FALSE
ARTIFACT_REQUIRED = TRUE
COVER_HERO_REQUIRED = TRUE
VISUAL_BLUEPRINT_REQUIRED = TRUE
DETERMINISTIC_COMPOSER_REQUIRED = TRUE
QA_REQUIRED = TRUE
FINAL_FILE_REQUIRED = TRUE
```

Text-only is allowed only when the user explicitly says content/text only, no artifact, or equivalent.
