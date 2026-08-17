# Connector Endpoint, Arrowhead & Label Engine

Every semantic relationship must survive rendering.

For each edge:
- source and target nodes exist;
- rendered connector exists exactly once unless the topology requires branching;
- first endpoint attaches to source bounds/port within tolerance;
- final endpoint attaches to target bounds/port within tolerance;
- directed edges have arrowhead on the correct owner/end;
- RTL direction resolution occurs before endpoint calculation;
- connector is not clipped or hidden;
- edge label, when present, is linked by `data-label-for` and remains near the edge;
- label does not collide with unrelated nodes or text.

Missing, detached, reversed, duplicated, or orphan connectors are HARD FAIL.
