# V7 — Consulting Cognitive Packet Contract

**STATUS: BLOCKING BEFORE ANALYTICAL ARTIFACT SYNTHESIS**

The renderer and Artifact Engine may not receive a critical analytical page until the cognitive packet is complete and evidence-backed. Required schema: `schemas/consulting_cognitive_packet_v7.schema.json`.

The packet exists to force the model to answer: What decision is being supported? What must management/evaluator believe? What evidence supports and contradicts the thesis? What could make the conclusion wrong? What relationships must the exhibit make visible?

A packet with generic placeholders, repeated questions across unrelated pages, unsupported evidence, or no counterargument is `BLOCKED_CONTENT_INTELLIGENCE`.

## v7.0.1 schema hardening
`schemas/consulting_cognitive_packet_v7.schema.json` now constrains `role_id` to the 24 canonical RFP role IDs, relationship types to the current semantic graph vocabulary, and Council routes to registered lens IDs plus mapped authorized `ROLE-*` identities. Evidence-for items require source reference + locator + confidence; evidence-against requires source reference + locator. Arbitrary `FAKE_ROLE`, relationship or Council label is schema-invalid.
