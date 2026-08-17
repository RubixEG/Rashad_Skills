# Auto-Repair & Page-Split Policy

STATUS: HARD REPAIR BOUNDARY — v2.6.4.2

## Allowed automatic repair
The production runtime may automatically:
- adjust micro-spacing within approved tolerance;
- optimize line breaks;
- recalculate connectors after direction/geometry changes;
- correct directional placement when the semantic order is unchanged;
- restore approved asset placement;
- repair tiny boundary drift;
- rebalance local whitespace without changing hierarchy.

## Forbidden automatic repair
The runtime may not:
- delete content or evidence;
- change the thesis;
- change artifact family/archetype;
- merge or delete semantic nodes;
- remove semantic edges;
- replace a relationship artifact with cards/bullets/table;
- rewrite evaluation/contract facts;
- swap brand assets;
- silently reduce typography below approved minimum;
- hide content behind clipping/overflow.

## Page split
When content cannot fit safely, expand the logical role into multiple physical pages rather than sacrificing readability or topology.

Examples:
- Team Capacity → Team Requirements → Team Compliance
- BOQ Architecture → BOQ Detail → Acceptance → Cost Exposure

Logical role count is not physical slide count.

## Return-upstream rule
If repair requires semantic or artifact-family change, return to the responsible upstream stage with `CANNOT_RENDER_WITHOUT_SEMANTIC_LOSS`.
