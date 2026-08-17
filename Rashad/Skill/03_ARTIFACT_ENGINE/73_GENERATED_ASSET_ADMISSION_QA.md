# Generated Asset Admission QA

STATUS: HARD POST-GENERATION GATE — v2.6.4.3

Before a generated image enters any client-facing composition, verify:

1. `text_or_pseudo_text = 0`;
2. `letters_or_numerals = 0` when forbidden by brief;
3. `logo_or_logo_like_mark = 0`;
4. `seal_signature_watermark = 0`;
5. `slide_document_chrome = 0`;
6. `cards_tables_dashboard_ui = 0` unless explicitly reference-only;
7. `final_analytical_topology = 0`;
8. focal area and negative-space zones match brief;
9. crop/resolution/visual quality are suitable;
10. asset contains no fabricated evidence or client-specific confidential content.

## Decision
- `APPROVED_AS_VISUAL_INGREDIENT`
- `REJECTED_CONTAMINATED`
- `REJECTED_WRONG_COMPOSITION`
- `REFERENCE_ONLY`

No generated asset is promoted directly to `PRODUCTION_PAGE`.

## v2.6.4.4 admission split
Do not apply the old `slide_document_chrome=0` rule to an approved `GOLDEN_VISUAL_MASTER`. For that mode, evaluate visual quality, topology, continuity and overlay safety instead. Exact generated Rubix/client identity or authoritative proposal copy still fails admission.

## v2.6.4.7 full-page admission
For `GOLDEN_VISUAL_MASTER_PAGE`, evaluate the complete page as a visual master. Text/logos/numbers are not automatically forbidden, but they must be correct, readable, brand-approved or superseded by native overlay/flattening. Hallucinated logos, fake facts and garbled Arabic remain hard failures.
