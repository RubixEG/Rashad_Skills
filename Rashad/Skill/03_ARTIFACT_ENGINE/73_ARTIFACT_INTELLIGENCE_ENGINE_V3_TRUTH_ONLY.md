# 73 — Artifact Intelligence Engine V3 — Truth-Only

**Status:** CURRENT STRUCTURAL-TRUTH AUTHORITY — v6.2.2 floor aligned

**Purpose:** remove the last source of score inflation from v5.2 by separating semantic/artifact truth from visual/benchmark quality.

## Input
A schema-valid, referentially-valid Relationship Graph. Every node and edge must be evidence-linked.

## Artifact Truth Score /100
- Relationship coverage & carrier truth — 30
- Evidence traceability — 15
- Topology fidelity — 15
- Semantic hierarchy / cross-cutting treatment — 10
- Complexity discipline — 10
- Feedback/governance/decision explicitness — 10
- Node/edge completeness — 10

There is **no benchmark-fit or novelty default** in Artifact Truth. Unknown values score neither positively nor negatively because they belong to Exhibit Quality, not Artifact Truth.

## Complexity is a hard legality gate
The winner may not exceed the declared AC-1…AC-5 primitive budget. If all candidates exceed it, synthesis returns `NO_LEGAL_COMPOSITION_WITHIN_COMPLEXITY_BUDGET` and must re-synthesise or split the page. It may not pass with a warning.

## Thresholds
- analytical client-facing page: ≥90
- critical / partner target: ≥90
- any lower legacy 85 score is diagnostic only and has zero release authority
- any missing relationship carrier, dangling edge, duplicate semantic ID or evidence-free relation: hard FAIL
