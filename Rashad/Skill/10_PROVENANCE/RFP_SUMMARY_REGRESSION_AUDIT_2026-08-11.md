# RFP Summary Regression Audit — Innovation & Digital Culture Example

## Finding 1 — Missing authorship inference
The prior Summary included procurement maturity scores but did not answer the requested decision question: **does the RFP appear to have been authored/assembled by a single client owner, a multi-function client team, an external advisory firm, or a hybrid compiled process — and why?**

V2.4 fixes this by requiring `32_RFP_AUTHORSHIP_AND_PROCUREMENT_MATURITY.md` and the authorship assessment schema.

## Finding 2 — English structural labels leaked into Arabic output
The prior Summary visibly used labels such as `Competition Narrative`, `Table of Contents`, `Opportunity Snapshot`, `Key Dates`, `Strategic Reading`, and other English structural terms in an Arabic document. This happened because internal canonical role names were emitted directly as visible headings.

V2.4 separates `internal_role_id` from `visible_label` and makes English structural leakage a blocking QA failure for Arabic engagements.

## Current REDF authorship fingerprint — provisional council reading
Based on the RFP evidence already modeled in the engagement, the strongest hypothesis is **HYBRID_COMPILED_PACKAGE / INTERNAL_MULTI_FUNCTION assembly**, not a single individual author and not enough evidence to assert that one external consulting company authored the complete package.

### Evidence supporting the hypothesis
- very detailed business/innovation and technical requirements;
- specialist annexes for cyber, software, team, quality, evaluation and contract;
- strong acceptance and staffing detail;
- material mismatch between a broad multi-domain scope and only five BOQ lines;
- unresolved support-duration vs contract-duration relationship;
- missing integration/data volumes despite high technical specificity;
- different levels of granularity across business, technical and commercial components.

### Counter-evidence / limits
- structured innovation language can also be produced by an advisory firm;
- no explicit source evidence identifies a named external author;
- some inconsistencies can arise from procurement packaging rather than multiple authors.

### Provisional classification
`HYBRID_COMPILED_PACKAGE`  
**Authorship confidence:** 81/100  
**Implication:** expect boundary ambiguities at handoffs between business scope, technical annexes and commercial packaging; use clarifications and pricing assumptions to protect these seams.

This provisional reading must be regenerated from the active RFP evidence registers on each engagement; it is not a reusable fact.
