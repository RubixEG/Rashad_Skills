# 72 — Rubix Artifact Family Catalog

**Status:** CURRENT — the single artifact vocabulary. Closes audit finding ART-05 (five uncoordinated vocabularies; the harness branching on a sixth).
**Owner:** Artifact Intelligence Architect (C5 #40)
**Relationship to module 71:** module 71 is the *generative* authority — it composes artifacts from primitives. This catalog is the *recognition and benchmark* authority: named compositions that recur, with acceptance criteria.

---

## 72.0 How to use this catalog — and how not to

**This is not a menu.** The engine does not look a page up here. The order of operations is
always: relationships → graph signature → synthesis → competition → winner. Only *after* a
winner is chosen does the catalog matter, and it matters for three things:

1. **Recognition** — if the winning expression matches a catalogued family, inherit its
   geometry rules and acceptance criteria rather than re-deriving them.
2. **Benchmark** — the `benchmark_fit` dimension (5 of 100) scores against same-intent
   reference pages retrieved by graph signature.
3. **Anti-pattern defence** — each family records how it degrades, so QA knows what a
   *failed* instance of it looks like.

**A page whose winning expression matches nothing here is not a problem.** It is the engine
inventing, which is the intended behaviour. Add it to the catalog afterwards if it recurs.

Every family is written as a composition expression over the 16 primitives in `71` §71.5.

---

## AF-01 · Operating Spine
`SPINE(3..9) ⊕ BAND_UNDER(CONTROLS) ⊕ GAUGE×n@nodes ⊕ RAIL_LATERAL`

| | |
|---|---|
| **Topology** | linear chain, one dominant axis, optional governance band crossing beneath |
| **Carries** | `FLOWS_TO`, `DEPENDS_ON`, `APPROVES`, `CONTROLS` (via band), `MEASURES` (via gauges) |
| **Use when** | an ordered operating process must read as one continuous capability, not as stages |
| **Do not use when** | the sequence has no real ordering — a spine asserts order that must exist in evidence |
| **Node range** | 3–9. Above 9, compress to phases or move to `AF-06` |
| **RTL** | item 1 sits at the **physical right**; arrows point leftward; connector geometry is computed **after** direction resolution |
| **Acceptance** | every adjacent pair has a rendered, endpoint-attached connector; the band visibly crosses ≥80% of the spine width; gauges are anchored to their owner node |
| **Degrades into** | a row of equal cards with decorative chevrons between them. That is the failure mode observed in the delivered deck: 7 stages, arrows drawn as glyphs, **0 semantic edges** |

---

## AF-02 · Operating Spine + Enabling Layers + Feedback Loop
`SPINE ⊕ STACK_UNDER ⊕ LOOP(tail→head) ⊕ RAIL`

| | |
|---|---|
| **Topology** | a chain resting on enabling planes, closing back on itself |
| **Carries** | `FLOWS_TO`, `ENABLES`, `FEEDS_BACK`, `OWNS` |
| **Use when** | there is an operating sequence **and** cross-cutting enablers (platform, data, AI) **and** the cycle genuinely closes |
| **Critical rule** | if `FEEDS_BACK` exists in the graph, a `LOOP` or `RING` carrier is **mandatory** (AI2-L04). Feedback that is implied rather than drawn fails the page |
| **Node range** | spine 3–7, layers 2–4 |
| **Acceptance** | the return path is a rendered edge with an arrowhead, not a caption saying "continuous improvement" |
| **Note** | this is the family the REDF-style scope example converges toward. It did not need to pre-exist — the engine composed it from `ENABLES` + `FLOWS_TO` + `FEEDS_BACK` + cross-cutting nodes |

---

## AF-03 · Core Capability Hub
`HUB(core) ⊕ SATELLITES(3..8) ⊕ RAIL_EVALUATOR ⊕ BAND_IMPLICATION`

| | |
|---|---|
| **Topology** | one central proposition, satellites bound to it by real edges |
| **Carries** | `ENABLES`, `MEASURES` (via attached gauges) |
| **Use when** | the thesis is a single institutional capability and everything else exists to serve it |
| **Do not use when** | the satellites do not actually connect to the core — that is a set, not a hub, and belongs in `AF-08` |
| **Acceptance** | core occupies ≥18% of live area; every satellite has a rendered edge to the core; the core carries a claim, not a label |
| **Reference behaviour** | the strongest observed page in the generated-image corpus is this family: central node, 6 satellites, evaluator rail on the right, implication band at the bottom, source line at the foot |
| **Degrades into** | a circle in the middle with six unconnected boxes around it |

---

## AF-04 · Governance Ring
`RING(CONTROLS) ⊕ INNER(operating form) ⊕ GAUGE ⊕ RAIL`

| | |
|---|---|
| **Topology** | a control boundary enclosing the thing it controls |
| **Carries** | `CONTROLS`, `OWNS`, `APPROVES`, `FEEDS_BACK` |
| **Use when** | governance must read as **enclosing**, not as one more peer box in a row |
| **Critical rule** | AI2-L05 — a cross-cutting node rendered as a peer box is an illegal composition. Governance, platform and data layers are planes, not items |
| **Acceptance** | the ring geometrically encloses ≥70% of the inner form's bounding box |

---

## AF-05 · Evaluation Architecture *(composite)*
`FIELD(criteria) ⊕ GAUGE(threshold) ⊕ RAIL(win messages) ⊕ BAND(bid implication)`

| | |
|---|---|
| **Topology** | position encodes weight × difficulty; a scalar instrument marks the pass threshold |
| **Carries** | `THRESHOLD_FOR`, `PRIORITIZES`, `MEASURES`, `EVIDENCES` |
| **Area budget** | dominant 50–55% · gauge 8–12% · rail 20–25% · band 10–15% |
| **Acceptance** | the threshold is drawn as a **cut line on the instrument**, not stated in prose; every criterion's position is derived from its published weight; the rail states how we win each criterion |
| **Why composite** | this is the page where one artifact cannot carry the argument. Criteria, threshold and win logic are three different questions the evaluator asks in sequence |

---

## AF-06 · Deliverable Chain
`LADDER(stage↔deliverable) ⊕ MATRIX(acceptance criteria) ⊕ BAND(value)`

| | |
|---|---|
| **Carries** | `FLOWS_TO`, `MAPS_TO`, `APPROVES` |
| **Use when** | outputs must read as an operational chain rather than a list of documents |
| **Acceptance** | every deliverable binds to exactly one stage and one acceptance criterion; no orphan rows |
| **Degrades into** | a plain table. A table is legitimate for dense evidence but it is not a chain — it carries `MAPS_TO` and loses the flow |

---

## AF-07 · Risk & Clarification Register *(dense evidence)*
`MATRIX(dense) ⊕ FIELD(exposure) ⊕ RAIL(mitigation owner)`

| | |
|---|---|
| **Carries** | `RISKS`, `PRIORITIZES`, `OWNS`, `BLOCKS` |
| **Complexity band** | AC-4 / AC-5 — density here is a **virtue**, not a defect |
| **Critical rule** | AI2-C01 — QA may not require fewer rows. It may only require that rows remain legible at the declared band's minimum font size |
| **Acceptance** | every risk has an owner, a trigger and a mitigation; probability/impact positions are derived, not decorative |
| **Degrades into** | six "risk cards" with traffic-light icons — the single most common substitution of decoration for analysis |

---

## AF-08 · Structured Set *(the honest one)*
`MATRIX or STACK ⊕ RAIL`

| | |
|---|---|
| **Carries** | nothing directional. This family is for genuinely unordered, unconnected items |
| **Use when** | the evidence really does contain a set with no relationships — a list of standards, a glossary, an inventory |
| **Critical rule** | using `AF-08` when relationships **do** exist is the core defect this whole module exists to prevent. If the graph has edges, `AF-08` is illegal |
| **Machine consequence** | a page whose graph has 0 edges can score at most ≈53/100 (measured). If a page must be a set, accept the ceiling and keep it short — do not dress it as an artifact |

---

## AF-09 · Team & Capability Depth
`TREE(structure) ⊕ MATRIX(capability × person) ⊕ GAUGE(availability) ⊕ RAIL(key personnel)`

| **Carries** | `OWNS`, `MAPS_TO`, `MEASURES` |
| **Acceptance** | every named person maps to a verified CV record (Council role #35); availability is evidenced, not asserted |

---

## AF-10 · Timeline with Decision Gates
`SPINE(time) ⊕ LANE(workstream) ⊕ GATE_MARKERS(APPROVES) ⊕ BAND(dependencies)`

| **Carries** | `FLOWS_TO`, `DEPENDS_ON`, `APPROVES`, `BLOCKS` |
| **RTL** | the time axis runs **right → left**. This is the highest-risk RTL surface in the whole system: a mirrored timeline reverses the project |
| **Acceptance** | gates sit **on** the spine, not beside it; every cross-lane dependency is a rendered edge |

---

## 72.1 Composite area budgets

| Region | Share of live area | Notes |
|---|---|---|
| Dominant artifact | 50–60% | if it measures below 35% it is not dominant; `G32` checks the declared budget against the rendered geometry |
| Supporting evidence | 20–30% | |
| Decision / implication rail | 15–25% | every consulting exhibit owes the evaluator this |
| Source / caveat layer | 3–6% | |
| **Whitespace floor** | ≥ 5% | AI2-L06 |

---

## 72.2 Universal acceptance criteria

Applied to every family, machine-checked:

| Criterion | Gate |
|---|---|
| Every relationship in the graph has a rendered carrier | `G32` relationship truth |
| Directed relations carry rendered arrowheads | `G16`, `G32` topology clarity |
| Every node label sits with its node | `G17` |
| Every badge/KPI/icon stays inside its owner's permitted area | `G11` |
| Structure density ≥ 0.055 for artifact-led pages | `C9_PIXEL` |
| Composition is not a template twin of a nearby page | `G33` |
| Declared area budgets match rendered geometry | `G32` |
| Current independent Artifact Truth ≥90 for analytical/critical release; any legacy Artifact Strength ≥85 value is diagnostic only | `G32` |

---

## 72.3 The universal anti-pattern

> **N ideas → N equal surfaces.**

Cards are a legitimate *supporting* primitive and Rubix's strongest historical pages use panels
heavily. What is prohibited is card-**only** thinking: reaching for a grid because there are six
items, when the six items stand in relationships that a grid destroys.

Mechanically: `CARD` has an empty carrier set. A card-only composition is illegal for any graph
with at least one edge. If a page genuinely has no edges, it is `AF-08`, it will score ~53, and
that is the correct and honest outcome — not something to be dressed up.
