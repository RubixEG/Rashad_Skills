# 39 — Deterministic Artifact Archetype Selector

STATUS: **HARD SELECTION AUTHORITY — v2.5**
PURPOSE: Convert classified information relationships into an archetype choice with explicit scoring, composite handling and tie-break rules.

## Inputs
- dominant `REL-*` relationship;
- optional secondary `REL-*` relationship;
- page role / executive question;
- semantic nodes and edges;
- time/dependency/ownership/decision materiality flags;
- density and precision requirements;
- evidence lookup requirement;
- engagement language / RTL constraints.

## Candidate routing table
| Relationship | Primary candidate archetypes |
|---|---|
| REL-HIER | VAI-13, VAI-23, VAI-25 |
| REL-SEQ | VAI-04, VAI-07, VAI-14, VAI-20 |
| REL-TIME | VAI-05, VAI-12, VAI-20 |
| REL-SYS | VAI-13, VAI-18, VAI-23 |
| REL-COMP | VAI-06, VAI-08, VAI-14, VAI-15, VAI-24 |
| REL-OWN | VAI-08, VAI-19, VAI-22 |
| REL-CAUSE | **VAI-27 CAUSE-TO-INTERVENTION TREE**, VAI-14 when cause is embedded in transformation |
| REL-RISK | VAI-10, VAI-28 when control topology is dominant |
| REL-DEC | VAI-06, VAI-09, VAI-10, VAI-29 |
| REL-EVID | VAI-09, VAI-15, VAI-21 |
| REL-DEP | VAI-12, VAI-18, VAI-20 |
| REL-MAT | VAI-11, VAI-14, VAI-24 |
| REL-VAL | **VAI-30 VALUE-CREATION TREE / BENEFITS BRIDGE**, VAI-18 when value exchanges form a network |
| REL-QUANT | **VAI-31 QUANTITATIVE EVIDENCE VIEW**, VAI-02 only when executive synthesis is the actual question |
| REL-NAV | VAI-03 |
| REL-PULSE | VAI-02, VAI-05 |

## Scoring
Score every routed candidate 0–100:
- `relationship_fidelity` 0–35
- `question_fit` 0–20
- `node_edge_preservation` 0–15
- `decision_usefulness` 0–10
- `precision_fit` 0–10
- `narrative_rhythm_fit` 0–5
- `rtl_geometry_fit` 0–5

Hard deductions:
- loses a material semantic edge: candidate rejected;
- requires invented data: candidate rejected;
- generic equal-card fallback for a non-peer relationship: candidate rejected;
- conflicts with a mandatory page/product contract: candidate rejected.

## Composite relationships
1. Score candidates for the dominant relationship.
2. Add `secondary_fit` by evaluating whether the same candidate encodes the secondary relationship without losing the dominant one.
3. If no single archetype scores ≥80 and both relationships are material, select `COMPOSITE_BESPOKE` and construct a new artifact using the two relationship grammars. Register the bespoke logic; do not force a catalog match.
4. Maximum two material relationship classes per artifact. More than two means the page must split or return to consulting reasoning.

## Tie-break rules
If top scores differ by <5 points:
1. choose greater relationship fidelity;
2. then greater node/edge preservation;
3. then lower cognitive complexity;
4. then stronger narrative-rhythm diversity vs previous two pages;
5. if still tied, Artifact Council must decide and log rationale.

## Confidence / action
- `SELECTOR_CONFIDENCE >= 85`: auto-propose archetype to Artifact Council.
- `70–84`: Council review required.
- `<70`: no selection; return to relationship/thesis reasoning.

## Output
`selector_decision_id`, candidates/scores, selected archetype or `COMPOSITE_BESPOKE`, rationale, confidence, rejected candidates/reasons, tie-break path.
