# RTL Structural QA & No-Mirror Exception Registry

STATUS: HARD QA AUTHORITY — v2.6.4.2

## Default no-mirror / preserve registry
- `Rubix | Client` co-brand cluster → `NEVER_MIRROR`; remains physically left; Rubix far-left/first.
- Rubix logos → `NEVER_MIRROR`.
- Client/official logos → `NEVER_MIRROR`.
- photographs → `NEVER_MIRROR`.
- screenshots → `NEVER_MIRROR`.
- maps → `PRESERVE` unless map-specific semantics explicitly require another treatment.
- URLs → `LTR`.
- API identifiers → `LTR`.
- technical IDs → `LTR`.
- ISO identifiers → `LTR`.
- Latin acronyms → `LTR` with bidi isolation.
- mathematical expressions → `PRESERVE`.
- charts → chart-specific `PRESERVE` unless the chart's meaning explicitly requires directional transformation.
- financial conventions → preserve unless explicitly redesigned under a chart-specific authority.

## Structural tests
The runtime/QA suite must define tests equivalent to:
- `test_arabic_timeline_origin_is_right`
- `test_arabic_process_progresses_right_to_left`
- `test_rtl_sequence_visual_order`
- `test_rtl_progression_arrow_direction`
- `test_rtl_numbered_stage_position`
- `test_mixed_ltr_token_preservation`
- `test_api_token_preserves_ltr_inside_rtl_page`
- `test_latin_acronym_bidi_isolation`
- `test_cobrand_does_not_mirror_with_page_rtl`
- `test_logo_asset_never_mirrors`
- `test_connector_endpoints_after_direction_resolution`

## Example invariant
For a horizontal RTL sequence, after geometry resolution:
`x(item_1) > x(item_2) > x(item_3)`
unless the component explicitly declares a different valid structure.

## Prohibition
Do not use a blind whole-canvas flip as the implementation of RTL.

## v2.6.4.3 cross-format extension
Text alignment alone cannot prove RTL/BiDi correctness. Validate mixed-run visual order according to `74_CROSS_FORMAT_BIDI_RUN_ORDER_CONTRACT.md`. Validate edges only after direction resolution according to `75_CONNECTOR_SEMANTICS_AND_ENDPOINT_CONTRACT.md`.
