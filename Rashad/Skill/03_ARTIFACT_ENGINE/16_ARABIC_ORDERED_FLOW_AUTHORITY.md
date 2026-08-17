# AR-SEQ-001 — Arabic Ordered Flow Authority
> **v2.2 USER AUTHORITY — BLOCKING:** For Arabic client-facing natural-language content, use Arabic-Indic numerals `٠١٢٣٤٥٦٧٨٩`. Any older instruction in this file to follow Western RFP digits for Arabic prose is superseded. Preserve raw Western digits only in exact technical/machine/reference identifiers that cannot safely change. `01_ACTIVE_RUNTIME/29_PRODUCTION_EXECUTION_FIREWALL.md` governs release.


## Numeral authority override — current rule
Current user override supersedes historic source-following numeral heuristics for Arabic natural-language output. Arabic-Indic numerals are mandatory in Arabic prose; exact technical/machine/reference identifiers remain raw when necessary for correctness. Generated imagery never decides numeral style.


## Status
**Priority 0 / hard layout invariant / production release blocker.**

This file is the definitive authority for every Arabic numbered or otherwise ordered artifact. It overrides benchmark-page imitation, artifact-template defaults, CSS convenience, visual-generation concepts, and renderer heuristics.

## Core rule
For an Arabic or RTL client-facing page, the first logical item must begin visually from the **top-right or rightmost approved starting anchor**.

The sequence may progress only through an approved path:

1. **Horizontal:** right → left.
2. **Vertical:** top → bottom.
3. **Wrapped grid:** right → left within each row, then top → bottom across rows.
4. **Diagonal / staircase:** top-right → bottom-left.
5. **Radial / circular:** item `١` begins in the upper-right quadrant and the declared connector path remains unambiguous.

It must never:
- start from the left;
- start from the bottom;
- progress bottom → top;
- place item `١` visually after item `٢`;
- reverse a later row;
- use Western digits in Arabic semantic sequence labels;
- use numbers baked into an AI-generated image;
- depend on CSS `direction`, `row-reverse`, flex `order`, DOM order, or CSS counters as the only ordering mechanism.

## Scope
Treat a page as ordered whenever it contains:
- phases, stages, steps, activities, workstreams, gates, milestones, or waves;
- sequential outputs or deliverables;
- numbered cards or panels `١..ن`;
- maturity or readiness progression;
- evaluation or decision gates;
- timelines and roadmaps;
- numbered team roles when the numbers communicate an intended order;
- any labels `١..ن` unless the page contract explicitly declares them `identifier_only`.

If numbers are identifiers only and have no reading sequence, the page contract must state that explicitly. Ambiguity defaults to **ordered**.

## Approved physical patterns

### Horizontal
Visual result:

```text
Left edge                               Right edge
٤            ٣            ٢            ١
             ← progression direction ←
```

Coordinate invariant:

```text
X(١) > X(٢) > X(٣) > ... > X(ن)
```

### Vertical
Visual result:

```text
١
↓
٢
↓
٣
↓
٤
```

Coordinate invariant:

```text
Y(١) < Y(٢) < Y(٣) < ... < Y(ن)
```

### Wrapped grid
For seven items in four physical columns:

```text
Top row:       ٤    ٣    ٢    ١
Second row:    ٧    ٦    ٥
```

Rules:
- the first row begins with `١` at the right;
- the next logical item after the row break begins at the right of the next row;
- rows progress downward;
- snake order is forbidden unless the relationship explicitly requires it and the user approves it.

### Diagonal or staircase

```text
                    ١  top-right
                 ↙
              ٢
           ↙
        ٣
     ↙
٤  bottom-left
```

Coordinate invariant:

```text
X(١) > X(٢) > X(٣) > ...
Y(١) < Y(٢) < Y(٣) < ...
```

### Radial or circular
- `١` begins in the upper-right quadrant, approximately the 1–2 o'clock zone;
- arrows/connectors declare the path explicitly;
- the path must not visually imply a bottom-origin start;
- use a linear alternative when the radial path is ambiguous.

## Sequence contract
Every ordered page must include:

```json
{
  "ordered_sequence_present": true,
  "sequence_semantics": "chronological | logical | ranked | phased | identifier_only",
  "sequence_layout_mode": "horizontal | vertical | wrapped_grid | diagonal | staircase | radial",
  "flow_start_anchor": "top_right",
  "flow_direction": "right_to_left | top_to_bottom | top_right_to_bottom_left | declared_radial",
  "number_system": "arabic_indic",
  "sequence_labels": ["١", "٢", "٣", "٤"],
  "explicit_visual_slot_map": [
    {"logical_index": 1, "row": 1, "column_from_right": 1},
    {"logical_index": 2, "row": 1, "column_from_right": 2}
  ],
  "connector_direction_matches_sequence": true,
  "validation_status": "pending"
}
```

## Renderer implementation rule
The logical data array remains in semantic order:

```js
const items = [item1, item2, item3, item4];
```

The renderer assigns explicit physical slots. For a fixed LTR-safe CSS grid:

```js
function getArabicGridPosition(index, columns) {
  const row = Math.floor(index / columns) + 1;
  const indexInsideRow = index % columns;
  const column = columns - indexInsideRow;
  return { gridRow: row, gridColumn: column };
}
```

Do not reverse the data array and then reverse CSS again. Do not trust CSS direction to produce the intended physical order.

## Arabic numeral rule
Sequence labels must be created at the data layer using Arabic-Indic digits for Arabic client-facing natural-language content:

```text
٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩
```

Do not use Western digits for Arabic semantic sequence labels. Approved technical identifiers, URLs, product names, email addresses, and immutable reference codes retain their exact source form when altering digits would make them incorrect.

## Image-generation rule
AI-generated production assets may not contain sequence numbers, arrows, stage labels, or ordering text. Generate only the visual ingredient; the deterministic renderer adds all sequence labels and connectors.

## Validation layers
A sequence page cannot be approved until it passes all four layers.

### 1. Blueprint validation
- sequence contract exists;
- start anchor is valid;
- slot map is complete and unique;
- connectors follow the declared path.

### 2. HTML DOM validation
For horizontal order:

```js
function validateHorizontalRTLSequence(elements) {
  const boxes = elements.map(el => el.getBoundingClientRect());
  for (let i = 0; i < boxes.length - 1; i++) {
    if (boxes[i].left <= boxes[i + 1].left) {
      throw new Error(`AR-SEQ-001: item ${i + 1} must be right of item ${i + 2}`);
    }
  }
}
```

For vertical order:

```js
if (!(Y1 < Y2 && Y2 < Y3)) reject();
```

For diagonal order:

```js
if (!(X1 > X2 && X2 > X3 && Y1 < Y2 && Y2 < Y3)) reject();
```

### 3. PDF validation
- rasterize the production PDF;
- verify number and card centers follow the same coordinate invariant;
- compare HTML golden screenshot with the PDF raster;
- reject if PDF conversion changes the order.

### 4. PowerPoint validation
- inspect editable object coordinates;
- confirm the logical item `١` occupies the approved starting slot;
- confirm connectors and labels preserve the same path;
- reject any independently rewritten or reversed layout.

## Hard-fail conditions
Any one of the following rejects the page:
- item `١` appears on the left in a horizontal sequence;
- item `١` begins at the bottom;
- sequence moves bottom-to-top;
- a wrapped row restarts from the left;
- a later row is reversed;
- arrows oppose the number order;
- sequence labels use Western digits inside Arabic natural-language content;
- sequence labels are embedded in a generated image;
- HTML passes but PDF or PPTX reverses the order;
- no explicit sequence contract exists for a numbered artifact;
- an artifact uses variable-height bars to imply chronological order.

## Recovery order
When the gate fails:
1. rebuild the explicit visual-slot map;
2. correct connector direction;
3. choose a simpler approved layout mode;
4. split the page if density makes the path ambiguous;
5. re-render and rerun all four validation layers.

Never waive the rule silently. A waiver requires explicit user authorization and a documented reason.
