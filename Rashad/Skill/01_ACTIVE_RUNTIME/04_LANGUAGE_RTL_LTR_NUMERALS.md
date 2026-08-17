MODULE: 04_LANGUAGE_RTL_LTR_NUMERALS
STATUS: **AUTHORITATIVE — v2.1**
LOAD WHEN: Before any client-facing text, table, artifact, timeline, overlay, or render.
DEPENDS ON: 00_START_HERE; 03_ENGAGEMENT_RESET_AND_SOURCE_GROUNDING; 29_PRODUCTION_EXECUTION_FIREWALL; 33_ARABIC_VISIBLE_LANGUAGE_PURITY_GATE

# Language, RTL/LTR, Numerals, and Dates

## 1. Client-facing language
The authoritative RFP language is the default client-facing language unless the user explicitly overrides it.

For Arabic RFPs, client-facing content is Arabic: titles, subtitles, narrative, labels, tables, processes, timelines, roles, methodology, governance, risks, recommendations, decisions, captions, and footers. English is used only for legitimate technical/product names, standards, acronyms, and exact source-defined terms.

Do not introduce English consulting headings merely for style. Internal English role IDs are invisible implementation identifiers only; `33_ARABIC_VISIBLE_LANGUAGE_PURITY_GATE.md` owns visible-label localization and blocks leakage.

## 2. Physical RTL
For Arabic engagements:
- titles/paragraphs/bullets align physically right;
- ordered sequences begin on the right;
- timelines normally begin on the right and progress left;
- semantic table columns are ordered for Arabic reading;
- `item_01` is physically the rightmost item;
- arrows and connectors follow the intended RTL reading path.

Latin technical tokens remain internally LTR and bidi-isolated. Never reverse `AI`, `POC`, `SLA`, `UAT`, `UI/UX`, product names, URLs, or code.

The Rubix/client logo signature is not mirrored merely because the page is RTL.

## 3. Arabic numeral hard lock — current user override
For **Arabic client-facing natural-language content**, use Arabic-Indic numerals:

`٠١٢٣٤٥٦٧٨٩`

This rule intentionally overrides older source-following numeral heuristics for Arabic client-facing prose.

Examples:
- `٢٤ موردًا`
- `٣٠ نموذجًا أوليًا`
- `٢٠ خدمة`
- `١٢ شهرًا`
- `٧٠٪`

Western-digit leakage into Arabic natural-language content is a **blocking QA failure**.

### Narrow exceptions
Preserve raw Western/Latin digits only when they are part of an exact machine/technical identifier that must not change: URL, email, source code, hash, API key, exact product/version string, or official reference identifier whose alteration would make it incorrect. Visually isolate these tokens from Arabic prose.

Generated pixels never decide numeral formatting.

## 4. Dates
Follow the authoritative RFP's calendar/date convention unless the user requests conversion. Any conversion is a `DERIVED_CALCULATION`, not a source fact.

When a date is rendered inside Arabic natural-language client-facing content, its visible digits use Arabic-Indic numerals unless it is an exact official reference token that must remain raw.

Never silently replace Hijri with Gregorian or vice versa. Show conflicts rather than normalizing them silently.

## 5. Image-generation boundary
Generated imagery is text-free for production purposes. No Arabic/English production text, numbers, logos, dates, page numbers, tables, or ordered labels may be baked into generated pixels.

Correct path:
`Content → Artifact → Geometry → Native Text/Vector → Exact Assets → QA`

## Blocking gates
`LANGUAGE_GATE` | `RTL_LTR_GATE` | `ARABIC_NUMERAL_GATE` | `LOGO_SIGNATURE_GATE` | `29_PRODUCTION_EXECUTION_FIREWALL`

Release targets for Arabic client-facing pages:
- `rtl_error = 0`
- `western_numeral_leakage = 0`
- `generated_text_pixels = 0`
- `reversed_ltr_token = 0`


## v2.2 authority clarification
The current explicit user instruction supersedes the older source-following numeral heuristic: Arabic client-facing natural-language content uses Arabic-Indic numerals. Preserve Western digits only in immutable identifiers where conversion changes the identifier.
