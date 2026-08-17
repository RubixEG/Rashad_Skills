# AR-GRP-001 — Arabic Grouped Ordering Authority

## Relationship to AR-SEQ-001
AR-SEQ-001 governs numbered and ordered flows. AR-GRP-001 extends the same authority to **lettered, categorized, and grouped Arabic blocks**, even when they are not a chronological process.

## Absolute rule
On Arabic pages, the first logical group must occupy the far-right approved slot, and subsequent groups proceed right-to-left.

Examples:
- `أ` at the far right, then `ب`, then `ج` to the left;
- `الفئة الأولى` at the far right, followed by the second and third categories;
- grouped panels in the same logical reading order as their Arabic labels.

## Explicit slot mapping
Do not rely only on DOM order, `direction:rtl`, `row-reverse`, or browser grid behavior. Each group must receive an explicit visual slot map.

Example for three physical LTR-safe columns:
- `أ → grid-column: 3`;
- `ب → grid-column: 2`;
- `ج → grid-column: 1`.

## Wrapped groups
When groups wrap to a new row, each row restarts from the right. Snake order is forbidden unless the information relationship explicitly requires it and the council approves it.

## Hard fails
- `أ` visually placed on the left;
- `أ، ب، ج` progressing left-to-right;
- the second row restarting from the left;
- arrows or visual emphasis contradicting group order;
- HTML order correct but PDF/PPTX order reversed.
