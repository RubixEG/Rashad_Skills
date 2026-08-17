from __future__ import annotations
QUALITY_FLOORS={
 "dominant_mass_min":0.32,"dominant_mass_max":0.68,"min_pairwise_structural_divergence_critical":0.12,
 "target_pairwise_structural_divergence":0.18,"min_exhibit_hypotheses":5,"min_actual_render_candidates_critical":3,
 "diagram_ratio_hard_block":0.55,"artifact_truth_min":90,"ceqs_min":90,"safe_area_min_visible_px2":16,"min_type_hierarchy_levels":3
}
def get(k,default=None): return QUALITY_FLOORS.get(k,default)
