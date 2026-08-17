# V7 — Monolingual Visible Output & Canonical Naming Authority

**STATUS: BLOCKING V7 LANGUAGE/NAMING AUTHORITY**

## Root law
One engagement output has one visible primary language unless the owner explicitly requests a bilingual deliverable.

- Arabic RFP / Arabic selected output → visible product is Arabic.
- English RFP / English selected output → visible product is English.
- A bilingual source does **not** automatically create bilingual headings; choose the primary contractual/owner-selected output language.
- When both language versions are required, prefer separate Arabic and English outputs rather than mixed decorative headings.

## Allowed foreign-language islands
A foreign-language token is allowed only when precision requires it: official company/product/proper name, acronym, standard, immutable identifier, URL/email/code/version, or exact source term that should not be translated. Use bidi isolation where required.

**Decorative bilingualism is forbidden.**

## Forbidden behavior
- `القراءة الاستراتيجية — Strategic Reading` in an Arabic Summary.
- English subtitles/callouts/table headers because they look consulting-grade.
- Arabic translations inserted into an English product unless needed to quote/source a term.
- Internal role IDs visible to management.

## Canonical names
`01_ACTIVE_RUNTIME/rfp_summary_role_registry_v7.json` owns the 24 visible names in Arabic and English. No model-created synonym replaces them without an owner decision. Source-specific labels may appear inside content when they are factual source terminology; they do not rename the canonical role.

## QA targets
Arabic product: `avoidable_english_heading=0`, `avoidable_english_label=0`, `western_numeral_leakage=0` under current numeral authority.
English product: `unrequested_arabic_heading=0`, `unrequested_arabic_label=0`.
