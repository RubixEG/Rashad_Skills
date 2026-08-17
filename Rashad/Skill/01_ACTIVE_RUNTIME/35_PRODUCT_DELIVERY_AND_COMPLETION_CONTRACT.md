# 35 — Product Delivery & Completion Contract

STATUS: **HARD COMPLETION AUTHORITY — v2.5**
PURPOSE: Define DONE by product release, not by content existence.

## Artifact-product completion
For `INTERNAL_PURSUIT_BRIEF` and any product routed with `DELIVERY_MODE=ARTIFACT`, mandatory stages are:
1. source/RFP processing complete;
2. content model complete;
3. page roles/questions/theses/evidence complete;
4. relationship classification complete;
5. deterministic archetype selection complete;
6. Artifact Intent approved for every analytical page;
7. Visual Blueprint approved;
8. required assets generated/resolved;
9. Geometry Handoff locked and ledgered;
10. Capability Preflight PASS;
11. deterministic composition complete;
12. exact brand assets + native language/RTL/numeral layer applied;
13. semantic/topology/visual/geometry/RTL/numeral/brand QA PASS;
14. final artifact file/object created;
15. release gate PASS and artifact delivered.

`CONTENT_OUTPUT_DOES_NOT_SATISFY_PRODUCT_COMPLETION = TRUE`

## No-stop-after-image gate
A generated image is always an asset node, never a product completion event. After image generation:
- persist asset provenance;
- set asset status to `APPROVED` or `REVIEW_REQUIRED`;
- return control to the Artifact Production Orchestrator;
- continue to Geometry/Composition/QA.

If composition cannot continue, product state becomes `BLOCKED`, not `LOCKED`/complete.

## Honest blocked outcome
When a mandatory capability is unavailable, report:
`ARTIFACT_PRODUCTION_BLOCKED` + blocking capability + completed stages + incomplete stages. Do not call the product complete.
