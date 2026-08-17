# 27 — Visual Blueprint Schema

STATUS: HARD SCHEMA — v2.5
PURPOSE: Translate Artifact Intent into a deterministic production specification. Canonical vocabulary: `40_CANONICAL_ARTIFACT_VOCABULARY_AND_MAPPING.md`.

```text
VISUAL_BLUEPRINT
blueprint_id:
artifact_id:
page_id:
version:
source_artifact_intent_hash:

PAGE_LOGIC
executive_question:
thesis:
implication:
dominant_relationship:
secondary_relationship:
artifact_family:
archetype_id:
density_class: LOW | MEDIUM | HIGH
editability_class: FULLY_NATIVE | VECTOR_HYBRID | RASTER_AUGMENTED

SEMANTICS
semantic_nodes:
semantic_edges:
groupings:
exceptions:
uncertainties:
required_evidence_refs:

COGNITIVE_PATH
entry_point:
primary_scan_path:
secondary_scan_path:
decision_anchor:
focal_point:

GEOMETRY
canvas_ratio: 16:9 unless higher authority overrides
safe_zones:
major_regions:
anchor_points:
node_placement_logic:
edge_routing_logic:
whitespace_budget:
continuation_strategy:
minimum_text_legibility:

RTL_AND_LANGUAGE
page_direction: RTL | LTR
directional_islands: []  # optional zone-level LTR/RTL/PRESERVE islands; page-level MIXED is invalid
physical_sequence_rule:
ltr_isolates:
numeral_policy:
table_column_order:
connector_direction:

BRAND
brand_applied_after_artifact_lock: TRUE
rubix_logo_asset_id:
client_logo_requirement:
primary_brand_anchor:
semantic_accent:
background_luminance_class: LIGHT_ONLY
forbidden_colors_or_treatments:

VISUAL_ASSETS
image_mode: NONE | INTERNAL_VISUAL_CONCEPT | PRODUCTION_VISUAL_INGREDIENT
image_brief_id:
image_zone:
image_crop_behavior:
strict_no_text_logo_number_fact: TRUE

PRODUCTION
composer_capabilities_required:
native_text_required: TRUE
exact_asset_injection_required: TRUE
native_connectors_required:
native_tables_required:
editable_output_required:

QA_ASSERTIONS
no_semantic_node_loss: TRUE
no_semantic_edge_loss: TRUE
no_generic_card_fallback: TRUE
no_black_or_near_black: TRUE
no_generated_logo: TRUE
no_generated_client_facing_text: TRUE
no_western_numeral_leakage_in_arabic_prose: TRUE
physical_rtl_verified:
collision_scan_required: TRUE

GOVERNANCE
artifact_council_session_id:
artifact_intent_approval_id:
visual_blueprint_approval_id:
lock_hash:
```

## Rule
The blueprint describes **meaning and geometry**, not only styling. Production may vary pixel-perfect layout as needed for safety, but may not alter semantics, relationship, focal point, reading path, or artifact family without returning to Artifact Council.
