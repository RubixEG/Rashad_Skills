# Connector Semantics & Endpoint Contract

STATUS: HARD TOPOLOGY/GEOMETRY CONTRACT — v2.6.4.3

Every semantic edge records:
- `edge_id`;
- `source_node_id`;
- `target_node_id`;
- `relationship_type`;
- `directionality = DIRECTED | BIDIRECTIONAL | UNDIRECTED`;
- `source_anchor = START | END | TOP | BOTTOM | CENTER | NAMED_PORT`;
- `target_anchor`;
- `arrowhead_owner = SOURCE | TARGET | BOTH | NONE`;
- `route_policy = DIRECT | ORTHOGONAL | CURVED | BRANCHED`;
- `branch_group_id` if applicable;
- `cycle_id` if applicable;
- `label_id` if applicable;
- post-direction endpoint assertions.

## Coordinate system
Canonical canvas uses a fixed top-left physical origin for final numeric coordinates, while semantic placement uses logical START/END tokens before direction resolution. Units are canonical scene-graph units mapped deterministically to target formats.

## Required build order
`semantic nodes/edges → resolve page/zones → resolve physical node geometry → resolve anchors → calculate routes/endpoints → render connectors → assert endpoints/arrowheads`.

## Fail conditions
Wrong endpoint, wrong arrowhead owner, clipped route, detached label, wrong branch/cycle semantics, or direction reversal is topology FAIL.

