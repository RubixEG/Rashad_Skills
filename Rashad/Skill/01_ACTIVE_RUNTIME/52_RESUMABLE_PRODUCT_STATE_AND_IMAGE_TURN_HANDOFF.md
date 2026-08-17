# Resumable Product State & Image Turn Handoff

STATUS: HARD ACTIVE RUNTIME CONTRACT — v4.1

State vocabulary:
`IN_PROGRESS → WAITING_IMAGE_TOOL → IMAGE_RETURNED → ASSET_QA → PAGE_COMPOSITION → PAGE_QA → EXPORT_QA → RELEASED`

Forbidden transition:
`WAITING_IMAGE_TOOL / IMAGE_RETURNED → RELEASED`

Minimum persisted handoff object:
- current_product
- current_engagement
- current_page
- requested_asset
- source/content hashes
- approved visual concept
- asset path/id when returned
- QA status
- next executable action
- remaining deliverables

If the conversational runtime ends the turn after image output, the next turn loads this object before any other product routing.
