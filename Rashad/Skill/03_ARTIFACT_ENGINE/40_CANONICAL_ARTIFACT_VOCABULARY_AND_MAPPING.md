# 40 — Canonical Artifact Vocabulary & Mapping Authority

STATUS: **HARD AUTHORITY — v2.5**
PURPOSE: Remove duplicate Artifact Intent / production vocabularies and make every downstream object interoperable.

## Canonical production editability class
Only these values are active:
- `FULLY_NATIVE` — native text/shapes/tables/connectors; no raster dependency for analytical meaning.
- `VECTOR_HYBRID` — native analytical structure with approved vector/icon assets.
- `RASTER_AUGMENTED` — native/vector analytical core plus approved raster hero/illustration/texture ingredient.

Historical aliases are **input-only migration aliases**, never persisted:
- `NATIVE` → `FULLY_NATIVE`
- `HYBRID` → `VECTOR_HYBRID`
- `VISUAL_INGREDIENT_ONLY` → **INVALID as a production editability class**. If a raster ingredient exists, use `RASTER_AUGMENTED` while preserving a native analytical core. If no native analytical core exists, production is blocked.

## Canonical image mode
`NONE | INTERNAL_VISUAL_CONCEPT | PRODUCTION_VISUAL_INGREDIENT`

Image mode and editability class are different axes. Never overload one to mean the other.

## Canonical Artifact Intent Contract fields
Every Artifact Intent persists the following fields:
- `artifact_id`, `page_or_object_id`, `version`
- `executive_question`, `thesis`, `implication`
- `evidence_refs`
- `dominant_relationship`, `secondary_relationship`
- `artifact_family`, `archetype_id`
- `semantic_nodes`, `semantic_edges`
- `reading_path`, `focal_point`
- `image_mode`, `editability_class`
- `reference_pattern_ids` — optional reference-only abstract patterns
- `engagement_local_prior_ref` — optional strongest **current-engagement** approved prior artifact for the same role; never a global golden deck
- `strength_target`
- `safety_constraints`
- `fallback_family`
- `forbidden_fallbacks`
- `rtl_sequence_contract` when ordered content exists
- `status`, `council_session_id`, `approval_id`, `lock_hash`

## Fallback vocabulary
Fallback is never a generic-card escape hatch.
- `fallback_family` must preserve the dominant relationship and all material nodes/edges.
- `forbidden_fallbacks` must include any layout that loses hierarchy/sequence/dependency/ownership/causality encoded by the intent.
- If no equivalent-strength fallback exists: `RETURN_TO_ARTIFACT_STAGE`.

## Migration rule
Any active file using a historical alias must map through this authority before persistence. New ledgers, blueprints, geometry contracts and tests use canonical values only.
