# Canonical Page Specification

STATUS: HARD PRE-RENDER CONTRACT — v2.6.4.2

## Purpose
Freeze the approved analytical and visual intent before deterministic rendering.

## Minimum required fields
Every production page specification records at least:

### Identity and routing
- `page_id`
- `product_id`
- `role_id`
- `role_depth_level`
- `section_id`
- `language`

### Direction
- `page_direction`
- `flow_direction`
- `reading_order`
- `directional_zones`
- component-level `component_direction`
- component-level `mirror_policy`

### Intelligence
- `management_or_evaluator_question`
- `page_thesis`
- `evidence_refs`
- `fact_inference_status`
- `information_relationship`

### Artifact
- `artifact_intent_id`
- `artifact_family`
- `artifact_archetype`
- `semantic_nodes`
- `semantic_edges`
- `node_ids`
- `edge_ids`
- `grouping_logic`
- `sequence_logic`
- `causality_logic`
- `ownership_logic`
- `dependency_logic`

### Visual target
- `visual_depth_level`
- `benchmark_family`
- `visual_quality_target`
- `regions`
- `canvas`
- `safe_margins`
- `geometry`
- `typography`

### Assets/output
- `brand_assets`
- `images`
- `charts`
- `tables`
- `source_labels`
- `footers`
- `page_number`
- `release_requirements`

## Lock rule
After `PAGE_SPEC_LOCKED = true`, a downstream adapter may not reinterpret the analytical model. Any change to question, thesis, evidence, artifact family, semantic node/edge set, or direction policy invalidates the lock and returns the page upstream.

## Version/hash rule
The page spec must be versioned and hash-linked to the approved Artifact Intent / Blueprint / Geometry Handoff lineage so stale downstream renders can be detected.

## v2.6.4.9 stage clarification
The semantic fields of the Page Spec lock before composition. **Exact physical geometry does not lock until after Visual Concept Council approval and at least one browser-rendered HTML/SVG/CSS candidate has been visually approved.** Before that point, geometry is expressed only as relative zones/proportions/visual mass. This prevents deterministic geometry from freezing a weak composition prematurely.
