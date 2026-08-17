# 32 — Capability Preflight Ledger Schema

STATUS: OPERATIONAL SCHEMA — v2.5

Persist:
`capability_preflight_id | product_id | image_generation | deterministic_composer | native_text | exact_asset_injection | vector_shapes | tables | connectors | rtl_control | file_output | pdf_export | pptx_export | visual_inspection | required_vs_available | result | blocking_reason | checked_utc`

`result=PASS` only when every capability required by the current Product Delivery Contract and approved Geometry Handoffs is available. Generic rendering/image tools do not imply `deterministic_composer=TRUE`.
