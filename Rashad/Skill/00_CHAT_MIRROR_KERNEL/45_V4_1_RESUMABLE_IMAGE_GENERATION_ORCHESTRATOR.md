> **V6.2 SUPERSESSION BANNER — Specialist image-substep detail only; global HIGHEST authority claim is superseded by v6.2.**

# V4.1 Resumable Image Generation Orchestrator

STATUS: SPECIALIST LEGACY IMAGE-SUBSTEP DETAIL — NOT GLOBAL ROUTING AUTHORITY

## Problem addressed
Some image-generation runtimes terminate the conversational turn immediately after returning the image. That is a transport/tool boundary, not a Rashad product boundary.

## Required state before image call
- product_id
- engagement_id
- page_id / asset_id
- product_status = IN_PROGRESS
- content_pack_hash
- approved_visual_concept_id
- reference_anchor_ids
- asset_purpose
- asset_acceptance_tests
- generated_asset_slot
- next_step
- remaining_pages / remaining_outputs
- blockers

## Resume behavior
When the tool returns:
1. bind returned image to `generated_asset_slot`;
2. keep product `IN_PROGRESS`;
3. run asset QA when execution resumes;
4. continue from `next_step`;
5. never regenerate accepted image merely because the tool created a turn boundary;
6. never terminate an RFP Summary / Proposal after image generation unless the user requested only an image.

## Completion truth
`IMAGE_GENERATED` is a sub-state, not `PRODUCT_COMPLETE`.
