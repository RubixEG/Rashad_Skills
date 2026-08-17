# ART-LOCK-001 — Artifact Intent and Fallback Lock

## Authority
Priority 0. Applies before generation and during every safety repair for RFP summaries, proposal sections, HTML, PDF, and editable PowerPoint.

## Purpose
Prevent the renderer from responding to overflow, density, RTL, or collision risk by silently replacing a strong relationship-led artifact with generic cards, equal boxes, or a weak list.

## Mandatory pre-generation object
Every analytical page must have an approved **Artifact Intent Contract** before production. The canonical schema is defined by `40_CANONICAL_ARTIFACT_VOCABULARY_AND_MAPPING.md` and persisted through `07_GOVERNANCE_AND_QA/27_ARTIFACT_INTENT_LEDGER_SCHEMA.md`.

This file no longer defines a parallel field vocabulary. Historical fields such as `benchmark_refs` and `golden_prior_ref` map to `reference_pattern_ids` and `engagement_local_prior_ref` respectively. Global golden-deck authority remains prohibited.

## Freeze rule
Once approved, the renderer may change spacing, geometry, line breaks, supporting copy, or split the page. It may not change the dominant information relationship or artifact family without:
1. logging the reason;
2. selecting an equivalent or stronger family;
3. rerunning the Artifact Strength Score;
4. passing council review.

## Forbidden silent fallbacks
The following are prohibited unless the Artifact Intent Contract explicitly declares them correct:
- equal-card grid;
- three-column text boxes;
- generic icon cards;
- unscored bar chart;
- detached KPI boxes;
- decorative image replacing a precise relationship;
- list replacing a lifecycle, dependency, governance, escalation, or architecture model.

## Repair hierarchy
1. preserve thesis;
2. preserve relationship;
3. preserve artifact family;
4. recompose geometry;
5. increase or rebalance whitespace;
6. compress supporting copy only;
7. split into a controlled continuation page;
8. move to an equivalent power artifact;
9. reject and request editorial intervention.

Generic cards are not an automatic repair option.

## Hard fail
`REJECTED — ART-LOCK-001 UNAPPROVED ARTIFACT DOWNGRADE — REBUILD REQUIRED`
