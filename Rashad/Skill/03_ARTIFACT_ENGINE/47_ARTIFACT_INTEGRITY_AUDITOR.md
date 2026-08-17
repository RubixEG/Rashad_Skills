# Artifact Integrity Auditor — Node / Edge / Topology Protection

STATUS: HARD QA AUTHORITY

## Purpose
Independently prove that production geometry and export have not changed the meaning encoded by the approved Artifact Intent, semantic nodes/edges, and Artifact Signature.

## Required comparison
Compare the approved pre-render artifact model against every required rendered representation.

Validate:
- node count and node identity;
- mandatory node presence;
- edge count and edge identity;
- source/target attachment;
- edge direction;
- relationship type;
- group membership;
- sequence order;
- hierarchy level;
- ownership/decision rights;
- labels and evidence locators;
- focal node and secondary nodes;
- continuation references across split pages.

## Zero-loss rule
`semantic_loss = 0` for mandatory topology.

Any dropped, duplicated, reversed, orphaned, detached, merged, or cryptically redrawn mandatory node/edge is a hard fail even when the rendered page looks visually polished.

## Weak-fallback prohibition
The following substitutions require artifact redesign approval and may never be introduced by the renderer:
- system/network → equal cards;
- dependency map → bullet list;
- lifecycle/journey → plain table;
- governance/decision rights → organization boxes only;
- weighted evaluation logic → detached percentages;
- BOQ compression architecture → raw BOQ table only;
- team capacity/ownership model → biographies only.

## Required status
`ARTIFACT_INTEGRITY = PASS | FAIL`

FAIL returns the page to Geometry Handoff / Artifact Architect; the renderer may not self-author a replacement.
