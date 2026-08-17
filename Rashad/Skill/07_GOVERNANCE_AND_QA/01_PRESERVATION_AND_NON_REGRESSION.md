# Preservation and Non-Regression Charter

## Purpose
Prevent the system from improving one dimension while breaking another.

## Preserved authorities from v6.5
The following are immutable unless the user provides a new approved authority:

- exact deck section names and order;
- Compliance Matrix placement;
- generation order versus reading order;
- current Rubix logo and device policy;
- RFP Summary completeness standard;
- Arabic RTL and Arabic-Indic numeral rules;
- AR-SEQ-001: no ordered sequence starts from the left or bottom, and no sequence progresses bottom-to-top;
- no old logos or legacy geometry;
- no full-slide image generation for production;
- renderer-first editable output;
- section distinctness and claim ownership;
- dependency and stale-content propagation;
- page overflow and safe-zone controls;
- approved artifact parity into PowerPoint.

## Change protocol
Any update must include:

1. proposed change;
2. reason;
3. affected authorities;
4. regression risk;
5. files changed;
6. tests added or updated;
7. rollback path;
8. council approval.

## No side-by-side authority conflict
Do not inject v7.3 beside older active prompts. v7.3 becomes the single runtime authority while prior versions remain regression references only.

## v7.6 preserved quality floor
The strongest approved artifact level is itself a preserved authority. Future correctness fixes may not reduce analytical strength, evaluator utility, visual ambition, artifact diversity, or narrative rhythm without explicit council and user approval.
