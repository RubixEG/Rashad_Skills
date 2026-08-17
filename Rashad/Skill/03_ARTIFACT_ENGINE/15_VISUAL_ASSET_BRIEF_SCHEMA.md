# Visual Asset Brief Schema

Every generated or selected asset must be requested through a brief with these fields:

```json
{
  "asset_id": "VAS-SEC04-P08-01",
  "page_id": "SEC04-P08",
  "page_thesis": "",
  "artifact_archetype": "",
  "visual_asset_required": true,
  "asset_type": "HERO_PHOTO | EDITORIAL_ILLUSTRATION | ABSTRACT_BACKGROUND | ICON | MOTIF",
  "asset_role": "PRIMARY_HERO | SUPPORTING_EDITORIAL | CONCEPTUAL_EXPLANATORY | BACKGROUND_ATMOSPHERE | NAVIGATION_ICON | ACCENT_MOTIF",
  "generation_mode": "GOLDEN_VISUAL_MASTER | PRODUCTION_VISUAL_ASSET_ISOLATED | REFERENCE_ONLY_VISUAL_CONCEPT | INSPIRATION",
  "subject": "",
  "business_context": "",
  "sector_context": "",
  "composition": {
    "orientation": "16:9 landscape",
    "subject_zone": "left | center | right",
    "negative_space_zone": "",
    "crop_strategy": ""
  },
  "style_family": "Rubix editorial / Rubix line icon / Rubix abstract geometry",
  "no_text_in_asset": true,
  "no_letters_or_numerals_in_asset": true,
  "no_logos_in_asset": true,
  "no_document_chrome_in_asset": true,
  "no_cards_tables_dashboards_in_asset": true,
  "no_final_analytical_topology_in_asset": true,
  "semantic_firewall_not_a_slide_or_document": true,
  "editable_overlay_required": true,
  "output_format": "PNG | WEBP | SVG",
  "minimum_resolution": "",
  "negative_constraints": [],
  "provenance_class": "GENERATED_APPROVED",
  "fallback_visual_strategy": "",
  "approval_status": "DRAFT | APPROVED | REJECTED"
}
```

The asset brief is versioned and linked to the page contract. A material page change marks its asset brief stale when the asset subject or composition may no longer support the page thesis.


## v2.6.4.3 context-isolation fields
A production brief also records:
- `context_isolation_status = ISOLATED | NOT_GUARANTEED | BLOCKED`;
- `forbidden_prompt_context[]` (final title/body, official values, logos, page number, full RFP/transcript, slide chrome);
- `asset_admission_gate = 03_ARTIFACT_ENGINE/73_GENERATED_ASSET_ADMISSION_QA.md`.

`approval_status=APPROVED` means approved as a **visual ingredient**, never as a final production page.


## v2.6.4.4 Golden Visual Master fields
When `generation_mode=GOLDEN_VISUAL_MASTER`, also include `deck_visual_dna_id`, `style_anchor_ids[]`, `section_anchor_id`, `previous_page_master_id`, `page_family`, `artifact_family`, `native_overlay_zones[]`, `contextual_scene_elements_allowed[]`, and `master_continuity_target`. The no-document-chrome/no-cards flags from isolated-asset mode do not apply globally; use relationship-led artifact and overlay-safety constraints instead.
