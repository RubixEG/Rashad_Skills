# 32 — Geometry Handoff Contract

STATUS: **HARD PRODUCTION INTERFACE — v2.5**
PURPOSE: Convert an approved Visual Blueprint into a versioned composer-ready specification with full approval/staleness traceability.

## Required contract
```text
GEOMETRY_HANDOFF
contract_id:
artifact_id:
visual_blueprint_id:
version:
status: NOT_STARTED | DRAFT | REVIEW_REQUIRED | APPROVED | LOCKED | STALE | BLOCKED | REJECTED | SUPERSEDED
source_visual_blueprint_hash:
council_session_id:
approval_id:
lock_hash:
created_utc:
updated_utc:

CANVAS
canvas_width:
canvas_height:
safe_margin_top:
safe_margin_right:
safe_margin_bottom:
safe_margin_left:

REGIONS:
  - region_id
  - purpose
  - x/y/w/h OR relational anchors
  - min/max capacity

NODES:
  - node_id
  - region_id
  - priority
  - content_type
  - alignment
  - min_font_size
  - native_required

EDGES:
  - edge_id
  - source_node
  - target_node
  - semantic_type
  - routing_priority
  - direction

ASSETS:
  - asset_id
  - provenance_hash
  - logical_asset_id
  - crop_mode
  - contain/cover rule
  - clear_space

RTL:
  - physical_start_edge
  - sequence_order
  - bidi_isolates
  - table_column_order

OVERFLOW:
  - reflow_order
  - continuation_page_same_family
  - REQUIRES_ARTIFACT_REPLAN trigger

QA:
  - collision zones
  - clipping checks
  - semantic node count
  - semantic edge count
  - logo/brand checks
```

## Lifecycle
- Geometry Handoff must be persisted in the Geometry Handoff Ledger before production.
- Approval is specific to `source_visual_blueprint_hash + version + lock_hash`.
- Any upstream Artifact Intent or Visual Blueprint hash change marks dependent Geometry Handoff `STALE` automatically.
- `STALE`, `DRAFT`, `REVIEW_REQUIRED`, or unapproved contracts cannot enter production.

## Composer boundary
The external deterministic composer may choose exact pixel coordinates within approved geometry logic, but may not delete nodes/edges, change the artifact family, reverse RTL sequence, substitute approximate logos, convert native text/data into generated imagery, introduce black/near-black backgrounds, or change the page thesis.

If required composer capabilities are unavailable, mark the product/geometry node `BLOCKED`, persist the Geometry Handoff, and route through the Product Completion Contract. Do not claim the artifact product is complete.
