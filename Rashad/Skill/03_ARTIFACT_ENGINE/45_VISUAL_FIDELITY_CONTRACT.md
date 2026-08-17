# Visual Fidelity Contract — HTML / PDF / PPTX Projection

STATUS: HARD PRODUCTION PARITY AUTHORITY

## Principle
HTML, PDF, and editable PPTX are projections of one approved visual model. They are not separate opportunities to redesign the page.

## Fixed-canvas rule
For presentation artifacts, resolve one fixed 16:9 canvas before composition. Responsive web reflow is prohibited inside slide/page canvases.

Required behavior:
- fixed page width and height;
- zero print margins unless an approved format requires otherwise;
- deterministic region coordinates from Geometry Handoff;
- no responsive wrapping that changes composition family;
- no browser shrink-to-fit;
- no automatic flex/grid wrapping across print boundaries;
- identical asset crop boxes across HTML and PDF;
- page break controlled explicitly;
- screen and print representations use the same composition DOM/geometry wherever the runtime allows.

## Font and RTL stability
- Use approved/native fonts available to the runtime.
- Verify font fallback before release.
- Arabic text remains native and physically RTL.
- Latin identifiers remain internally LTR without reversing surrounding geometry.
- A font substitution that changes line count or breaks the visual target is a parity failure.

## Projection preservation
Each representation must preserve:
1. artifact topology;
2. semantic nodes/edges;
3. primary focal point;
4. composition family;
5. region ordering;
6. relative visual weight;
7. whitespace strategy;
8. image crop/position;
9. section rhythm;
10. co-brand placement.

## Visual Fidelity Score
Assess the rendered page/section against the approved Page Visual Target / Golden Section Board:
- Artifact topology: 30 points
- Focal placement and scale: 20
- Hierarchy and region ordering: 15
- Whitespace / density: 10
- Section rhythm / variation: 10
- Accent / contrast distribution: 5
- Asset crop / visual-zone fidelity: 5
- Brand/co-brand geometry: 5

Release target: `>= 90/100` and Artifact Topology = PASS.

A score does not excuse semantic loss. Any lost node/edge, wrong ordered-flow direction, wrong logo order, or replacement of the approved artifact family is an automatic FAIL.

## HTML → PDF rule
When PDF is produced from HTML, render PDF from the same approved fixed-canvas HTML rather than rebuilding the layout in a separate document model. Compare the final PDF render to the HTML render page-by-page.

## PPTX rule
Editable PowerPoint may use a different native object model, but it must remain a projection of the same approved geometry and visual target. Any unavoidable deviation must be surfaced and approved, not silently accepted.

## v2.6.4.4 master-underlay projection
When a Golden Visual Master is approved, HTML/PDF/PPTX fidelity is measured primarily against preservation of that exact underlay plus native-overlay geometry. Rebuilding the master artifact independently in each format is prohibited.
