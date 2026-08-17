MODULE:
APPENDIX_AND_EVIDENCE

STATUS:
AUTHORITATIVE (process + honesty rules); library indexes are REUSABLE_RUBIX_EVIDENCE only

LOAD WHEN:
RFP requires team/docs/cases; Summary evidence-readiness; Team & Evidence Readiness; SEC-08 / SEC-12 / SEC-15; Compliance Matrix evidence mapping; appendix composition.

DEPENDS ON:
03_ENGAGEMENT_RESET_AND_SOURCE_GROUNDING
06_RFP_SUMMARY
09_COUNCILS_AND_ROLES
16_QA_AND_RELEASE_GATES
EVIDENCE/EVIDENCE_INDEX
EVIDENCE/TEAM_INDEX
EVIDENCE/CASE_STUDY_INDEX
EVIDENCE/CERTIFICATION_INDEX
CURRENT_RFP_SOURCES

DO NOT APPLY TO:

SUPERSEDES:
“Library presence = RFP compliance”; automatic inclusion of all CVs/cases; treating certificate scan presence as current validity.

CLASSIFICATION:
**Reusable Rubix evidence library process.** Distinct from **current RFP truth**. Matching an RFP requirement requires a fresh A1 matrix against the active pack.

---

# Appendix and Evidence

## Honesty rule (non-negotiable)

```text
Requirement → search evidence → match candidate → verify strength → identify gap → route into proposal
Never fabricate supporting evidence.
Show MISSING. Do not invent.
```

Evidence honesty statuses (use explicitly):

| Status | Meaning |
|---|---|
| VERIFIED_SOURCE_PAGE | Source page located; content usable pending bid-date validity/fit checks |
| SOURCE_PAGE_AVAILABLE | Page exists; further review required |
| SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED | Case/client identity incomplete or needs confirmation |
| ROLE_CONFLICT | Same person, conflicting role labels across sources |
| DUPLICATE_LANGUAGE_VERSION | Same person, AR/EN versions — deduplicate |
| VALIDITY_REVIEW_REQUIRED | Document present; expiry/authenticity not certified for this bid date |
| MISSING | Required evidence not found |
| NOT_INCLUDED_IN_10_DOCUMENT_DECK_LIST_REVIEW_REQUIRED | Extra asset outside the standard 10-document list |
| REFERENCE_ONLY | Structural/style reference; not factual proof |
| TEMPLATED_NOT_EVIDENCE | Generated/templated text — forbidden as proof |

## Current RFP truth vs reusable Rubix evidence

| | Current RFP truth | Reusable Rubix evidence |
|---|---|---|
| Source | Active engagement RFP pack / addenda / Q&A | `EXTERNAL_ENGAGEMENT_DEPENDENCY::APPENDIX_LIBRARY_INDEX.md` + primary PDFs/PPTX |
| Answers | What this client requires now | What Rubix can show from its library |
| May claim in proposal | Only after A1 match + A2 selection + A3 release | Candidate assets only until matched |
| Contamination rule | Prior engagements never supply facts | Library assets never imply another client’s outcomes |

## Primary library sources

From `EXTERNAL_ENGAGEMENT_DEPENDENCY::APPENDIX_LIBRARY_INDEX.md` (classification: reusable Rubix evidence; **not** current RFP authority):

| Source | Role |
|---|---|
| `EXTERNAL_APPENDIX_PACKAGE/CV_SOURCE` | Expanded CV library |
| `EXTERNAL_APPENDIX_PACKAGE/APPENDIX_SOURCE` | Cases, company profile, company documents, selected CVs |
| `Case Stuides.pptx` | Case-study visual source |

Workspace index path:

`EXTERNAL_ENGAGEMENT_DEPENDENCY::APPENDIX_LIBRARY_INDEX.md`

## Gates A0–A3

### A0 — Library preflight

Confirm sources, hashes, index, readability, duplicates, conflicts, and validity-review needs.

### A1 — RFP requirement matching

Approve team, document, and case-study matrices. **Every gap must be disclosed in the Summary / readiness register.** Current RFP requirements drive the matrix; the library does not.

### A2 — Selection and appendix plan

Approve selected CVs, cases, company pages, official documents, ordering, page budget, confidentiality, and current-deck render contracts.

### A3 — Final appendix release

Source fidelity, no fabrication, current brand, native/editable CV and case pages, unmodified official documents, Arabic RTL, privacy, validity, traceability, prepress.

A gate passes only when:

```text
required_roles_executed = 100%
unresolved_blocking_findings = 0
unsupported_appendix_claims = 0
expired_required_documents = 0
unresolved_role_fit_conflicts = 0
source_locator_coverage = 100%
```

## Critical conflicts (must remain visible)

1. **CV role conflicts** between `EXTERNAL_APPENDIX_PACKAGE/CV_SOURCE` and `EXTERNAL_APPENDIX_PACKAGE/APPENDIX_SOURCE` for some people (see `EVIDENCE/TEAM_INDEX.md`).
2. **Arwa Ajarem** appears in Arabic and English — deduplicate.
4. Certificate asset folder has **11** assets while the rendered appendix document lists **10** documents — resolve via review, do not silently drop or invent.
5. **Validity and expiry must be rechecked at each bid date**; presence ≠ current validity.

## Case-study status discipline

- Verified source pages (IDs 01–03 in index) remain `VERIFIED_SOURCE_PAGE`.
- Many dual cases (04A–11B) remain `SOURCE_PAGE_AVAILABLE_CLIENT_REVIEW_REQUIRED` with `NOT_EXTRACTED` client fields — do not invent client names.
- Do not promote a case to VERIFIED without a located source page and client review when required.

## Company documents / certifications

Standard ordered list (pages 46–55 in `EXTERNAL_APPENDIX_PACKAGE/APPENDIX_SOURCE`) plus media license extra asset — all default to `VALIDITY_REVIEW_REQUIRED` until bid-date review. See `EVIDENCE/CERTIFICATION_INDEX.md`.

## Company profile (reusable narrative pages)

Pages 14–44 in `EXTERNAL_APPENDIX_PACKAGE/APPENDIX_SOURCE` cover identity, consulting services, solutions, platforms, communications, and engagement models. These are Rubix self-description assets — still not current RFP truth.

## Selective loading

Never load the full CV library, all cases, or all certificates into context for a Summary or single section.

Load:

- the requirement matrix slice
- matched candidates only (capped)
- conflict/gap notes
- validity flags for selected docs

See `20_CONTEXT_LOADING_PROTOCOL.md`.

## Appendix councils (roles)

Use as reasoning roles; do not decorate client slides with council names:

1. Appendix Intelligence Director  
2. CV and Team Evidence Curator  
3. Corporate Documents and Eligibility Curator  
4. Case Study and Experience Evidence Curator  
5. Credential Validity and Authenticity Reviewer  
6. Appendix Gap and Substitution Manager  
7. Appendix Traceability and Citation Manager  
8. Appendix Privacy and Redaction Reviewer  
9. Appendix Composition and Deck Integration Architect  
10. Appendix Release and Prepress Reviewer  

## Indexes in this package

| File | Contents |
|---|---|
| `EVIDENCE/EVIDENCE_INDEX.md` | Master map + honesty protocol |
| `EVIDENCE/TEAM_INDEX.md` | CV inventory + conflicts |
| `EVIDENCE/CASE_STUDY_INDEX.md` | Case inventory + statuses |
| `EVIDENCE/CERTIFICATION_INDEX.md` | Company documents + validity flags |

## Source paths

| Path | Role |
|---|---|
| `EXTERNAL_ENGAGEMENT_DEPENDENCY::APPENDIX_LIBRARY_INDEX.md` | Canonical library inventory |
| `09_APPENDIX_EVIDENCE/08_APPENDIX_EVIDENCE_COUNCIL_AND_GATES.md` | Councils + A0–A3 |
| `09_APPENDIX_EVIDENCE/09_RFP_SUMMARY_APPENDIX_GAP_RULE.md` | Summary gap disclosure rule |
| `09_APPENDIX_EVIDENCE/13_READY_PROMPT_GENERATE_APPENDICES.md` | Appendix generation ready prompt |
| `_forensic_work\master_prompt_extract.txt` (§46) | Evidence engine mandate |
| `EXTERNAL_ENGAGEMENT_DEPENDENCY::SOURCE_INVENTORY_AND_FILE_GUIDE.md` | Source authority rules |
| `01_ACTIVE_RUNTIME/SECTION_DEPENDENCIES.md` | SEC-08 / SEC-12 / SEC-15 dependencies |
