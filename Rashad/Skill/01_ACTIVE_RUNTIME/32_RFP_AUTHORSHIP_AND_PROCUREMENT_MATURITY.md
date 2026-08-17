MODULE: 32_RFP_AUTHORSHIP_AND_PROCUREMENT_MATURITY
STATUS: AUTHORITATIVE — v2.4
LOAD WHEN: INTERNAL_PURSUIT_BRIEF; bid intelligence; RFP maturity analysis.

# RFP Authorship Fingerprint & Procurement Maturity

## Purpose

The internal RFP Summary must assess **how the procurement package appears to have been assembled** because authoring style affects ambiguity, clarification strategy, estimation confidence, and where hidden dependencies are likely to exist.

This is an **evidence-based inference**, never a factual accusation and never a claim about a named person/company unless the RFP itself states the author.

## Required classification

Choose one only when evidence is sufficient:

- `SINGLE_CLIENT_OWNER`
- `INTERNAL_MULTI_FUNCTION_TEAM`
- `EXTERNAL_ADVISORY_LED`
- `HYBRID_COMPILED_PACKAGE`
- `INSUFFICIENT_EVIDENCE`

Never output “a consulting company wrote this” as fact unless explicitly evidenced.

## Evidence dimensions — score 0–5 each

1. **Cross-document terminology consistency**
2. **Writing/style consistency across annexes**
3. **Scope decomposition coherence**
4. **Scope-to-BOQ alignment**
5. **Evaluation-to-scope alignment**
6. **Team-to-scope alignment**
7. **Acceptance/payment alignment**
8. **Technical/commercial depth consistency**
9. **Annex modularity / template fingerprints**
10. **Contradictions, duplicated language or handoff seams**

For each dimension capture:
`score | evidence_for | evidence_against | source_refs | implication`.

## Authoring-model inference

Use the pattern, not one clue:

### Signals supporting `SINGLE_CLIENT_OWNER`
- unusually consistent terminology/style;
- limited specialist depth;
- high cross-document coherence;
- few annex seams.

### Signals supporting `INTERNAL_MULTI_FUNCTION_TEAM`
- specialist depth varies by domain;
- procurement/legal/technical/operations sections show distinct styles;
- overall client vocabulary remains consistent;
- some cross-functional misalignment appears at boundaries.

### Signals supporting `EXTERNAL_ADVISORY_LED`
- strong framework consistency across business sections;
- deliberate narrative/decomposition across scope/evaluation/deliverables;
- consistent maturity language and structured methodologies;
- fewer unexplained seams, unless multiple advisory workstreams were involved.

### Signals supporting `HYBRID_COMPILED_PACKAGE`
- highly detailed specialist annexes combined with uneven commercial packaging;
- different terminology/granularity by document;
- contradictions at scope/BOQ/duration/acceptance boundaries;
- evidence of modular templates or legacy technical requirements;
- some sections feel advisory-designed while others feel internal/procurement-generated.

## Required visible output in INTERNAL_PURSUIT_BRIEF

Legacy internal descriptor: `بصمة إعداد الكراسة ونضج الحزمة` — **INTERNAL/HISTORICAL ONLY; never use as the current visible title.**

### `ماذا تكشف طريقة إعداد المنافسة عن عملية الشراء؟`

Show:
1. **نموذج الإعداد المرجح**
2. **درجة الثقة: 0–100**
3. **الأدلة المؤيدة**
4. **الأدلة المضادة / ما يمنع الجزم**
5. **بطاقة نضج** across the 10 dimensions
6. **دلالة على بناء العرض والتسعير والاستفسارات**

Do not use insulting labels such as “bad RFP”, “client mistake”, or “amateur author”.

## Confidence

Confidence measures confidence in the **inference**, not procurement quality.

- 85–100: strong, repeated cross-document fingerprints
- 70–84: probable, with meaningful counter-evidence
- 50–69: tentative
- <50: output `INSUFFICIENT_EVIDENCE`

## Separation from maturity score

`AUTHORSHIP_CONFIDENCE` ≠ `PROCUREMENT_MATURITY_SCORE`.

A package can be professionally authored yet commercially misaligned, or internally authored yet highly mature.


## v7.0 extension
Apply `73_V7_RFP_AUTHORSHIP_FINGERPRINT_EXTENSION.md` to distinguish likely limited/single internal authoring, multi-function internal preparation, specialist external advisory-led preparation, hybrid/compiled preparation, or insufficient evidence. Legacy classification IDs remain accepted as aliases.
