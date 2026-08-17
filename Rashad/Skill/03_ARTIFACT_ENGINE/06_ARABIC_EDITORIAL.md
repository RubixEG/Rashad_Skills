# Arabic Editorial and RTL Standard
> **v2.2 USER AUTHORITY — BLOCKING:** For Arabic client-facing natural-language content, use Arabic-Indic numerals `٠١٢٣٤٥٦٧٨٩`. Any older instruction in this file to follow Western RFP digits for Arabic prose is superseded. Preserve raw Western digits only in exact technical/machine/reference identifiers that cannot safely change. `01_ACTIVE_RUNTIME/29_PRODUCTION_EXECUTION_FIREWALL.md` governs release.


## Numeral authority override — current rule
Current user override supersedes historic source-following numeral heuristics for Arabic natural-language output. Arabic-Indic numerals are mandatory in Arabic prose; exact technical/machine/reference identifiers remain raw when necessary for correctness. Generated imagery never decides numeral style.


## Arabic quality
- write native institutional Arabic, not literal English translation;
- prefer concise conclusions over noun-heavy fragments;
- preserve official RFP terminology;
- distinguish fact, inference, assumption, and proposal;
- use consistent names for entities, outputs, roles, and systems.

## RTL geometry
- visible sequence begins on the right;
- arrows follow right-to-left progression;
- multirow numbering continues logically from the right;
- table column order is designed for Arabic reading;
- numeric runs are bidi-isolated so digits do not reverse.

## Numerals
Client-facing Arabic natural-language output uses Arabic-Indic numerals `٠١٢٣٤٥٦٧٨٩`. Western digits are permitted only in exact technical/machine/reference identifiers that cannot safely change.
Machine identifiers, email addresses, URLs, code, and technical keys retain valid raw forms.
