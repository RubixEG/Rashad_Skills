# 25 — Information Relationship Classifier

STATUS: ACTIVE AUTHORITY — v2.5
PURPOSE: Make artifact selection deterministic by classifying the information shape before visual design.

## Primary relationship classes

| ID | Relationship | Diagnostic question | Typical artifact direction |
|---|---|---|---|
| REL-HIER | Hierarchy | What sits above/below or contains what? | layered model, tree, capability stack |
| REL-SEQ | Sequence | What happens in what order? | lifecycle, journey, stage-gates |
| REL-TIME | Time | What happens when, for how long, and with what milestones? | roadmap, Gantt, timeline |
| REL-SYS | System / Network | What components interact and exchange value/data/control? | ecosystem, architecture, system map |
| REL-COMP | Comparison | What differs across options/entities/states? | matrix, benchmark, before/after |
| REL-OWN | Ownership | Who owns/approves/contributes to what? | RACI, role-output map, governance |
| REL-CAUSE | Cause / Effect | What drives what? | issue tree, driver tree, causal chain |
| REL-RISK | Risk / Control | What can fail, why, and how is it controlled? | risk register, bow-tie, control map |
| REL-DEC | Decision | How do choices narrow to a recommendation? | choice cascade, funnel, decision gate |
| REL-EVID | Evidence | What proof supports which claim/criterion? | evidence chain, case map, proof matrix |
| REL-DEP | Dependency | What relies on what and where is the critical path? | dependency map, interlock, critical path |
| REL-MAT | Maturity / Transition | Where are we now and what is the target state? | maturity ladder, heatmap, transition roadmap |
| REL-VAL | Value | What creates value and how does it accumulate? | value tree, benefits bridge |
| REL-QUANT | Quantitative | What does the data distribution/trend/bridge show? | chart, waterfall, scorecard |
| REL-NAV | Navigation | How should the reader navigate a long argument? | journey TOC, section map |
| REL-PULSE | Executive synthesis | What must management grasp immediately? | executive pulse / synthesis canvas |

## Classifier sequence
1. Extract entities/nodes.
2. Extract verbs/relations between them.
3. Determine whether order, dependency, ownership, comparison, time, or causality is material.
4. Identify dominant relationship.
5. Identify at most one secondary relationship.
6. Reject decorative families that do not encode the relationship.
7. Pass result to `39_DETERMINISTIC_ARCHETYPE_SELECTOR.md`; do not select from expert memory alone.

## Confidence
Use:
- `HIGH` — relationship is explicit in evidence or logically necessary.
- `MEDIUM` — relationship is strongly inferred but not explicitly stated.
- `LOW` — multiple plausible interpretations; return to consulting reasoning before design.

Do not use visual design to hide low relationship confidence.
