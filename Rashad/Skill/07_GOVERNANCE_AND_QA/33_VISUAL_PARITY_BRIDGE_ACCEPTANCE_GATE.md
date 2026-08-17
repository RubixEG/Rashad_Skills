# Visual Parity Bridge Acceptance Gate

STATUS: BLOCKING RELEASE GATE

## Required comparisons
For every page produced from a Golden Section Board compare:
- approved board/page target vs native HTML render;
- HTML render vs PDF render;
- HTML/PDF vs PPTX render when PPTX is produced.

## Blocking checks
- same artifact family/topology;
- same primary focal quadrant and comparable footprint;
- same major region ordering;
- same semantic nodes/edges;
- same ordered-flow direction;
- same co-brand location/order;
- comparable whitespace/density;
- same intended section rhythm;
- same approved image crop role;
- no new generic-card/table downgrade.

## Quantitative target
Use the Visual Fidelity Score defined in `03_ARTIFACT_ENGINE/45_VISUAL_FIDELITY_CONTRACT.md`.

Release requires:
- Visual Fidelity Score >= 90/100;
- Artifact Topology = PASS;
- no critical semantic/RTL/logo failure;
- no page that is visibly weaker because the renderer chose an easier layout.

## Repair order
1. preserve content/evidence;
2. preserve artifact topology;
3. repair geometry;
4. repair typography/line breaks;
5. repair micro-spacing;
6. re-render and compare again.

Never repair parity by deleting content or simplifying the artifact family unless the upstream Artifact Council explicitly redesigns and re-approves the page.
