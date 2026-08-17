# Visual Containment and Arabic Group-Order Hard Gate

## Test A — Independent-zone collision
Create a card containing marker, icon, title, body, and unit label. Assert every independent bounding box is separated after fonts load.

Reject when:
- title intersects body;
- body intersects unit label;
- icon or marker intersects title;
- a note intersects list content.

## Test B — Numeric containment
Render `٥٠٪`, `٣٠٪`, and `١٠٪` in wide and narrow metric blocks.

Assert:
- complete token is inside the parent safe padding;
- percent sign follows the value visually;
- no clipping in HTML, PDFium, Poppler, or PowerPoint export;
- label occupies a separate zone.

## Test C — Arabic grouped order
Render three lettered panels in an LTR-safe physical grid.

Expected physical positions:
- `أ` rightmost;
- `ب` middle;
- `ج` leftmost.

Reject browser-direction-only implementations.

## Test D — Cross-format parity
The same collision, containment, and group-order tests must pass in:
1. HTML DOM;
2. PDF raster;
3. editable PowerPoint object coordinates;
4. PowerPoint-exported PDF.

## Required rejection status
`REJECTED — VISUAL CONTAINMENT OR ARABIC GROUP-ORDER VIOLATION — REBUILD REQUIRED`
