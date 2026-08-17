# Golden Visual Master Semantic Topology Sidecar Contract

STATUS: HARD GVM TOPOLOGY AUTHORITY — v2.6.4.6

## Problem resolved
A Golden Visual Master may visually contain an architecture/network/journey whose nodes and connectors are baked into the master raster. DOM-only topology counting cannot legitimately see those internal visual nodes.

## Required solution
Compile a governed semantic sidecar from the approved Canonical Page Spec containing:
- page ID;
- artifact family;
- stable node IDs;
- stable edge IDs;
- source/target for each edge;
- sidecar SHA-256.

G11 may use `SIDECAR` mode for GVM pages. It verifies node/edge identity, count, edge referential integrity and sidecar hash lineage.

## Truthfulness boundary
A sidecar PASS proves **approved semantic topology lineage**, not pixel-level computer-vision recognition of every internal node in the image. Visual/artifact councils still judge whether the master visibly embodies that topology.

Never create hidden fake DOM nodes/edges solely to make G11 pass.
