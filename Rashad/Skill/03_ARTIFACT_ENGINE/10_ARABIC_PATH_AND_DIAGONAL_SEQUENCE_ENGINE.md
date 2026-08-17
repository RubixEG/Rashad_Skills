# Arabic Path and Diagonal Sequence Engine
> **v2.2 USER AUTHORITY — BLOCKING:** For Arabic client-facing natural-language content, use Arabic-Indic numerals `٠١٢٣٤٥٦٧٨٩`. Any older instruction in this file to follow Western RFP digits for Arabic prose is superseded. Preserve raw Western digits only in exact technical/machine/reference identifiers that cannot safely change. `01_ACTIVE_RUNTIME/29_PRODUCTION_EXECUTION_FIREWALL.md` governs release.


## Numeral authority override — current rule
Current user override supersedes historic source-following numeral heuristics for Arabic natural-language output. Arabic-Indic numerals are mandatory in Arabic prose; exact technical/machine/reference identifiers remain raw when necessary for correctness. Generated imagery never decides numeral style.


> `AR-SEQ-001` in `16_ARABIC_ORDERED_FLOW_AUTHORITY.md` is the definitive Priority-0 authority. This file supplies implementation detail and cannot weaken that rule.

## Core rule
Arabic sequence reading begins at the **top-right/rightmost approved starting anchor**. It never begins from the left or bottom.

The permitted progression patterns are:

1. horizontal: top-right → left;
2. wrapped grid: each row starts on the right, rows continue top → bottom;
3. diagonal: top-right → bottom-left;
4. vertical: top → bottom, aligned to the approved right-side axis;
5. radial: item `١` begins in the upper-right quadrant and follows an explicit connector path.

The following is forbidden for chronological or logical sequences:
- bottom-right → top-left;
- bottom-left → top-right;
- item `١` at the bottom;
- first row RTL but second row reversed;
- numbers created using CSS counters;
- rotated Arabic text;
- relying only on CSS direction, `row-reverse`, flex order, or DOM order;
- numbers or arrows baked into generated imagery.

## Explicit coordinate algorithm
For a horizontal RTL sequence:

```text
x(i) = right_anchor - i × (item_width + gap)
y(i) = top_anchor
```

For a wrapped RTL grid:

```text
row(i) = floor(i / columns)
column(i) = i mod columns
x(i) = right_anchor - column(i) × (item_width + gap)
y(i) = top_anchor + row(i) × (item_height + row_gap)
```

For a diagonal RTL sequence:

```text
x(i) = right_anchor - i × horizontal_step
y(i) = top_anchor + i × vertical_step
```

`i = 0` represents item `١`.

## Data order rule
The logical array remains `[١, ٢, ٣, ...]`. The renderer calculates physical positions. Do not reverse the data array and then reverse CSS direction again.

## Variable-height artifact rule
Variable-height bars may represent quantities, percentages, or severity. They may not also function as a chronological numbered sequence.

When a page communicates process order:
- use equal-height stage containers;
- show progression using arrows, connectors, or a path;
- keep all Arabic labels horizontal.

When a page communicates quantitative increase:
- use bars without stage numbering;
- label values explicitly;
- do not imply chronological order through bar height.

## Numeral rule
Generate sequence labels at the data layer using Arabic-Indic digits for Arabic client-facing natural-language content:

```text
١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩ ١٠
```

Do not depend on font substitution, CSS `counter()`, or pseudo-elements.

## Mandatory explicit slot map
Every ordered component must receive an `explicit_visual_slot_map` before layout. DOM order alone is not a visual-order contract.

## Validation authority
Run blueprint, HTML DOM, PDF raster, and PowerPoint object-coordinate checks defined by `AR-SEQ-001`. Any mismatch is a hard fail.
