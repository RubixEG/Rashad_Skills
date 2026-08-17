# 27 — Artifact Intent Ledger Schema

STATUS: **OPERATIONAL SCHEMA — v2.5**
CANONICAL VOCABULARY: `03_ARTIFACT_ENGINE/40_CANONICAL_ARTIFACT_VOCABULARY_AND_MAPPING.md`

| Field | Required | Meaning |
|---|---|---|
| artifact_id | yes | Stable engagement-local artifact ID |
| page_or_object_id | yes | Parent page/product node |
| version | yes | Version under review |
| executive_question | yes | Material evaluator/management question |
| thesis | yes | One-sentence takeaway |
| implication | yes | Why it matters |
| evidence_refs | yes | Current engagement evidence IDs |
| dominant_relationship | yes | REL-* classifier ID |
| secondary_relationship | no | At most one |
| artifact_family | yes | Selected family |
| archetype_id | conditional | VAI-* or COMPOSITE_BESPOKE |
| selector_decision_id | yes | Deterministic selector output |
| semantic_nodes | yes | Preserved entities |
| semantic_edges | yes | Preserved relationships |
| reading_path | yes | Physical reader path |
| focal_point | yes | Primary emphasis |
| image_mode | yes | NONE / INTERNAL_VISUAL_CONCEPT / PRODUCTION_VISUAL_INGREDIENT |
| editability_class | yes | FULLY_NATIVE / VECTOR_HYBRID / RASTER_AUGMENTED |
| reference_pattern_ids | no | Reference-only abstract patterns; never authority |
| engagement_local_prior_ref | no | Approved prior artifact from the current engagement only |
| strength_target | yes | Required artifact quality/strength floor |
| safety_constraints | yes | Geometry/content safety constraints |
| fallback_family | conditional | Equivalent-strength fallback only |
| forbidden_fallbacks | yes | Explicit forbidden downgrade families |
| rtl_sequence_contract | conditional | Required for ordered RTL content |
| status | yes | Canonical node state vocabulary |
| council_session_id | yes for approval | Artifact Council session |
| approval_id | yes for lock | Approval Ledger ID |
| lock_hash | yes for lock | Hash of approved intent |

Modification after lock marks the Artifact Intent `STALE` and propagates staleness to Blueprint + Geometry Handoff.
