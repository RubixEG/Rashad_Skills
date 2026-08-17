
# Layout-Aware Connector & Label Engine

## Required edge fields
`edge_id | source_node_id | target_node_id | relationship_type | source_anchor | target_anchor | directionality | arrowhead_owner | route_policy | label_id`.

## Runtime sequence
`fonts ready → nodes measured → page direction resolved → anchors chosen → route generated → arrowheads placed → labels placed → collision test → endpoint assertion`.

## RTL
Semantic order stays stable. Physical positions may mirror. Connector endpoints and arrowheads are always recomputed **after** RTL resolution.

## Blockers
- detached label;
- connector enters wrong node;
- arrowhead on wrong end;
- line crosses a critical label without routing reason;
- clipped connector;
- edge exists in spec but not DOM;
- DOM edge exists but not spec.
