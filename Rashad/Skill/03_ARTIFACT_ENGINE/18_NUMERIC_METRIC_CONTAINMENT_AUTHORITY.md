# KPI-FIT-002 — Numeric and Percentage Containment Authority
> **v2.2 USER AUTHORITY — BLOCKING:** For Arabic client-facing natural-language content, use Arabic-Indic numerals `٠١٢٣٤٥٦٧٨٩`. Any older instruction in this file to follow Western RFP digits for Arabic prose is superseded. Preserve raw Western digits only in exact technical/machine/reference identifiers that cannot safely change. `01_ACTIVE_RUNTIME/29_PRODUCTION_EXECUTION_FIREWALL.md` governs release.


## Numeral authority override — current rule
Current user override supersedes historic source-following numeral heuristics for Arabic natural-language output. Arabic-Indic numerals are mandatory in Arabic prose; exact technical/machine/reference identifiers remain raw when necessary for correctness. Generated imagery never decides numeral style.


## Priority
Priority 0 for every KPI, percentage, score, duration, quantity, weight, threshold, and page metric.

## Absolute rule
The complete numeric expression must remain inside its assigned container with safe padding on all sides.

This includes:
- Arabic-Indic digits;
- Arabic percent sign `٪`;
- decimal separators;
- units and abbreviations;
- plus/minus and comparison signs when required.

## Bidi-safe rendering
Numeric expressions in Arabic pages must be rendered as an isolated metric token. The renderer must not depend on surrounding RTL text to position the percent sign.

Approved implementation options:
- a dedicated `dir="ltr"` isolated metric element containing Arabic-Indic digits and `٪`;
- separate numeric and unit spans inside a deterministic flex/grid slot;
- native vector text boxes with explicit coordinates in PowerPoint.

## Container rules
- minimum internal padding must be measurable;
- values may not touch the edge;
- no glyph may exceed the card or bar bounds;
- narrow metric blocks must receive a smaller approved metric size or a wider layout allocation;
- long labels must wrap independently below the metric.

## Resolution sequence
1. widen/rebalance the metric layout;
2. use a dedicated metric token and separate label zone;
3. reduce the metric size within approved bounds;
4. change the artifact composition;
5. split the page.

## Hard fails
- percent sign outside the box;
- number clipped or touching the edge;
- value overlapping its label;
- Western numeral leakage inside Arabic natural-language metrics, except immutable technical/reference identifiers;
- HTML fits but PDF/PPTX does not.
