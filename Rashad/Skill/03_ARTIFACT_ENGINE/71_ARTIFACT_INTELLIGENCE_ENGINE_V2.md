> **V6.2.2 SUPERSESSION BANNER — Artifact Intelligence v2 is preserved as specialist lineage only. Current structural truth is Artifact Intelligence V3; the 3–5 synthesis count below is non-governing.**
# 71 — Artifact Intelligence Engine v2 (Synthesis Authority)

**Status:** LEGACY V2 SPECIALIST LINEAGE — current structural-truth authority is Artifact Intelligence V3
**Owner:** Artifact Intelligence Architect (blocking role)
**Executable companion:** `qa-harness-v2.6/detectors/artifact_synthesis.py`
**Applies to:** every analytical, artifact-led or hybrid page. Not covers, not pure dividers.

---

## 71.0 The problem this module exists to fix

v5.1 reasons like this:

```
page role  ->  artifact family  ->  template  ->  layout
```

That is an **Artifact Selector**. It is why the delivered MWAN deck measures as it does:

| Measured on the 19 delivered MWAN slides | Value |
|---|---|
| Slides carrying any semantic node instrumentation | **0 / 19** |
| Slides carrying any connector or SVG topology | **3 / 19** |
| Machine Artifact Strength score (floor is 85) | **18 – 42 / 100** |
| Deck distinct-composition ratio (floor is 0.70) | **0.684** |
| Template-twin page pairs inside a 4-page window | **5** |

The information was correct. The render was mostly clean. The **form** was a box grid.
Polishing the renderer cannot fix this, because the defect is upstream of rendering.

v2 reasons like this instead:

```
evidence -> semantic nodes -> typed relationships -> graph signature
        -> VISUAL PROBLEM STATEMENT
        -> LEGACY V2: 3-5 synthesised compositions; CURRENT v6.2.2 critical-page law: exactly 5 materially distinct hypotheses
        -> legality filter -> council scoring -> winner
        -> composite plan with area budgets -> production
```

The artifact is **composed from primitives**, and a composition is legal only when
every relationship in the graph has a visual carrier.

---

## 71.1 Governing doctrine

**AI2-D01 — Form follows relationship, not section name.**
The question is never "which artifact family is this page?". It is
"**what relationship architecture best explains this page?**".

**AI2-D02 — A card carries no relationship.**
`CARD` is a surface. It is a supporting primitive. It has an empty carrier set.
Therefore **a card-only composition is structurally illegal for any graph with
at least one edge**. This is not a style preference; it is a constructive
constraint that the engine enforces mechanically. Cards remain fully allowed as
*supporting* primitives inside a legal composition — MWAN's strongest pages use
panels heavily.

**AI2-D03 — Complexity is permitted; clutter is not.**
QA must never say "you have too many nodes, reduce them". It must ask: are the
relationships readable, is the hierarchy clear, are connectors unambiguous, are
labels legible. If yes, complexity is approved. See §71.7.

**AI2-D04 — Beauty never overrides relationship truth.**
A composition that scores highly on visual synthesis but cannot draw a
relationship that exists in the evidence is ILLEGAL, not merely weaker. The
reference implementation rejects `SPINE ⊕ BAND ⊕ GAUGE ⊕ RAIL` at score 94.5
when the graph contains `FEEDS_BACK` and the composition has no `LOOP`/`RING`
carrier. That is the doctrine working.

**AI2-D05 — One artifact per page is a default, not a rule.**
Consulting-grade pages are composite: dominant + supporting + implication rail +
source layer, with declared area budgets. See §71.6.

**AI2-D06 — The engine may invent.**
If no catalogued family fits, the engine composes a new one and names it by its
expression (e.g. `HUB ⊕ BAND ⊕ GAUGE ⊕ LOOP ⊕ SPINE`). Absence from the catalog
is never a reason to fall back to a grid.

---

## 71.2 Stage 1 — Semantic nodes

Every node extracted from evidence is typed. Type drives what visual roles it may take.

| Node type | Meaning | Typical visual role |
|---|---|---|
| `ACTOR` | who performs or decides | lane owner, swimlane header |
| `CAPABILITY` | what the organisation can do | stack layer, hub satellite |
| `PROCESS` | a transformation over time | spine segment, funnel stage |
| `ASSET` | platform, system, dataset | cross-cutting plane, hub core |
| `OUTCOME` | a result the client receives | spine terminus, ring output |
| `CONSTRAINT` | rule, regulation, threshold | enclosing band or ring |
| `MEASURE` | KPI, metric, index | gauge attached to its owner |
| `DECISION` | gate, choice, approval | node on a spine, threshold marker |
| `RISK` | exposure | field position, overlay marker |
| `EVIDENCE` | a source document or datum | rail item, footnote anchor |

**Rule AI2-N01.** A node with no type is not admissible. Untyped nodes are the
first step back toward boxes.

---

## 71.3 Stage 2 — Typed relationships and their carriers

The relationship vocabulary is **closed**. Each relation declares which
primitives can legitimately express it. A primitive not listed may not be used
to claim that relation.

| Relation | Directed | Legitimate carriers |
|---|---|---|
| `ENABLES` | yes | STACK, HUB, SPINE, TREE |
| `DEPENDS_ON` | yes | SPINE, TREE, LADDER, MATRIX |
| `FLOWS_TO` | yes | SPINE, FUNNEL, LANE, RING |
| `CONTROLS` | yes | RING, BAND, LANE, TREE |
| `MEASURES` | yes | GAUGE, RAIL, MATRIX, FIELD |
| `EVIDENCES` | yes | RAIL, BAND, MATRIX |
| `RISKS` | yes | FIELD, MATRIX, RAIL, BAND |
| `PRIORITIZES` | yes | FIELD, FUNNEL, LADDER, MATRIX |
| `OWNS` | yes | LANE, TREE, STACK |
| `APPROVES` | yes | SPINE, LANE, LADDER |
| `FEEDS_BACK` | yes | RING, SPINE, LOOP |
| `THRESHOLD_FOR` | yes | GAUGE, FIELD, MATRIX |
| `MAPS_TO` | no | MATRIX, LADDER, LANE |
| `BLOCKS` | yes | SPINE, LANE, FIELD |

**Rule AI2-R01.** Relationships are extracted from evidence, never asserted to
justify a chosen picture. A relationship without an evidence reference is
inadmissible and blocks the page at `G31_EVIDENCE_TRACE`.

---

## 71.4 Stage 3 — Graph signature and the Visual Problem Statement

Before any drawing, the engine computes invariants:

- `topology_class` ∈ {SET, CHAIN, TREE, DAG, STAR, CYCLIC}
- `dominant_relation`, `relation_counts`
- `depth`, `max_degree`, `roots`, `leaves`, `hub_nodes`
- `cross_cutting` — nodes touching ≥60% of the graph
- `has_time_axis`, `has_decision`, `has_measurement`, `has_governance`, `has_feedback`

From these it emits a **Visual Problem Statement** — the brief the competing
concepts must solve. Worked example (REDF-style scope, 7 nodes / 10 relations):

> The evaluator must be able to see: 7 semantic nodes and 10 typed relationships
> forming a STAR whose dominant relation is ENABLES; 2 cross-cutting nodes
> touching most of the graph (Innovation Factory, Digital Platform) — these must
> read as a plane or band, **not as a peer box**; a governance relation that must
> visibly enclose or cross the operating form; a feedback relation that must be
> shown **closing**, not implied; measurement attached to specific nodes, not
> floated as a separate list; a 5-step ordered progression that must survive RTL
> as physical geometry. A composition that renders these as equal parallel
> surfaces has failed the page regardless of visual polish.

**Rule AI2-G01.** The Visual Problem Statement is persisted with the page and is
part of the release evidence. A page whose statement was never computed cannot
pass `AI2_SYNTHESIS`.

---

## 71.5 Stage 4 — Composition primitives and synthesis

### The primitive vocabulary

| Primitive | Role | Axis | Node capacity | Default area | Expresses |
|---|---|---|---|---|---|
| `SPINE` | dominant | linear | 3–9 | 0.42 | ENABLES, DEPENDS_ON, FLOWS_TO, APPROVES, FEEDS_BACK, BLOCKS |
| `RING` | dominant | cyclic | 3–8 | 0.40 | FLOWS_TO, CONTROLS, FEEDS_BACK |
| `STACK` | dominant | vertical | 2–6 | 0.45 | ENABLES, OWNS |
| `HUB` | dominant | radial | 3–8 | 0.44 | ENABLES |
| `LANE` | dominant | parallel | 2–6 | 0.46 | FLOWS_TO, CONTROLS, OWNS, APPROVES, MAPS_TO, BLOCKS |
| `MATRIX` | dominant | bi-axial | 4–40 | 0.44 | DEPENDS_ON, MEASURES, EVIDENCES, RISKS, PRIORITIZES, THRESHOLD_FOR, MAPS_TO |
| `TREE` | dominant | hierarchy | 4–15 | 0.42 | ENABLES, DEPENDS_ON, CONTROLS, OWNS |
| `FUNNEL` | dominant | narrowing | 3–6 | 0.38 | FLOWS_TO, PRIORITIZES |
| `FIELD` | dominant | positional | 3–25 | 0.40 | MEASURES, RISKS, PRIORITIZES, THRESHOLD_FOR, BLOCKS |
| `LADDER` | dominant | paired | 3–10 | 0.40 | DEPENDS_ON, PRIORITIZES, APPROVES, MAPS_TO |
| `BAND` | supporting | transverse | 2–6 | 0.12 | CONTROLS, EVIDENCES, RISKS |
| `RAIL` | supporting | lateral | 2–6 | 0.20 | MEASURES, EVIDENCES, RISKS |
| `GAUGE` | supporting | scalar | 1–4 | 0.10 | MEASURES, THRESHOLD_FOR |
| `LOOP` | modifier | return | 1–2 | 0.04 | FEEDS_BACK |
| `ANCHOR` | modifier | focal | 1 | 0.08 | — |
| **`CARD`** | **primitive** | **none** | 1–12 | 0.06 | **— (nothing)** |

### Synthesis procedure

1. Seed candidate dominants from `topology_class` fit **and** from the carriers
   of the dominant relation.
2. For every relation the dominant cannot carry, attach the cheapest legitimate
   carrier, preferring supporting/modifier over a second dominant.
3. Attach a `RAIL` unless a lateral channel already exists — every consulting
   exhibit owes the evaluator an implication channel.
4. Enforce **structural diversity**: two candidates that share a dominant and an
   axis signature are the same idea in different clothes; keep one.
5. LEGACY V2 lineage: emit 3–5 candidates. CURRENT v6.2.2 critical-page law: exactly 5 materially distinct hypotheses.

**Rule AI2-S01.** Fewer than 3 candidates means no competition occurred → gate FAIL.
**Rule AI2-S02.** Diversity index < 0.45 means the candidates differ in styling,
not topology → gate FAIL.

---

## 71.6 Stage 5 — Legality filter

| Rule | Test | Verdict |
|---|---|---|
| `AI2-L01` relationship coverage | every relation in the graph has a carrier | ILLEGAL if not |
| `AI2-L02` card-only prohibition | composition ⊄ {CARD} when edges > 0 | ILLEGAL if violated |
| `AI2-L03` capacity fit | node count within dominant's capacity | WARN |
| `AI2-L04` feedback must be drawn | FEEDS_BACK present ⇒ LOOP or RING present | ILLEGAL if not |
| `AI2-L05` cross-cutting node is a plane | cross-cutting nodes ⇒ BAND/RING/STACK/LANE present | ILLEGAL if not |
| `AI2-L06` whitespace floor | total area budget ≤ 0.95 of live area | WARN |
| `AI2-L07` complexity budget | primitive count ≤ band budget | WARN |

Illegal candidates are eliminated **before** scoring. A high score cannot rescue
an illegal composition.

---

## 71.7 Stage 6 — Complexity budget

Complexity band is set by the **harder** of node count and relationship count.
A 7-node graph carrying 10 typed relationships is not a simple page.

| Band | Name | Nodes | Relations | Max primitives | Min font px |
|---|---|---|---|---|---|
| `AC-1` | Executive | 1–4 | 0–3 | 2 | 18 |
| `AC-2` | Analytical | 4–8 | 3–10 | 3 | 16 |
| `AC-3` | Multi-layer | 6–14 | 6–20 | 4 | 15 |
| `AC-4` | Dense system | 10–22 | 12–40 | 5 | 14 |
| `AC-5` | Decision cockpit | 14–40 | 16–80 | 6 | 14 |

**Rule AI2-C01.** QA may not reduce node count to achieve a pass. It may only
require that readability, hierarchy, connector clarity and label legibility hold
at the declared band. Reducing analytical content to satisfy geometry is a
semantic-loss repair and is forbidden (see `Repair Safety`).

---

## 71.8 Stage 7 — Artifact Council scoring

| Dimension | Weight | Machine proxy (lower bound) |
|---|---|---|
| Relationship truth | 20 | fraction of graph relations with a real, endpoint-attached carrier |
| Analytical depth | 15 | relation/node ratio, normalised at 1.4 |
| Visual synthesis | 15 | dominant-form area share vs 0.45 |
| Information density | 10 | node count inside the dominant's capacity band |
| Hierarchy | 10 | ≥2 distinct primitive roles present |
| Topology clarity | 10 | directed relations carry rendered arrowheads |
| Decision usefulness | 10 | an implication rail or threshold gauge exists |
| Non-template originality | 5 | composition-fingerprint distance to nearest deck page |
| Reference benchmark fit | 5 | similarity to retrieved same-intent reference pages |

Weights sum to **100** (verified).

- LEGACY V2 diagnostic floor: **≥85**. CURRENT release authority: independent Artifact Truth **≥90**.
- Partner-ready target: **≥ 90**

**Rule AI2-B01 — the machine ceiling.** `G32_ARTIFACT_STRENGTH` computes a score
from measurable page properties. **The council may score lower than the machine
ceiling but never higher.** A page measuring 41 cannot be argued to 88.

---

## 71.9 Stage 8 — Composite artifact planning

A consulting page is a composition with declared area budgets, not one picture
plus text.

```
Dominant artifact        50–60% of live area
Supporting evidence      20–30%
Decision / implication   15–25%
Source / caveat layer     3–6%
```

Worked example — Evaluation page:

```
Dominant     : FIELD (weighted criteria, position encodes weight × difficulty)
Supporting   : GAUGE (70% technical threshold, with the cut line drawn)
Rail (right) : RAIL  (how we win — three win messages)
Band (bottom): BAND  (bid implication, one sentence)
Source layer : source line + evidence IDs
```

**Rule AI2-P01.** Every composite region declares its area budget in the Page
Spec, and `G32` verifies the dominant actually occupies its declared share. A
"dominant" artifact rendered at 18% of the page is not dominant.

---

## 71.10 Stage 9 — Reference retrieval by analytical intent

Retrieval is by **graph signature similarity**, not by sector, client or section name.

Query key: `(topology_class, dominant_relation, has_governance, has_feedback,
has_measurement, complexity_band)`.

For each retrieved reference page, extract only:

```
page role · information relationship · artifact family · semantic topology
composition grammar · focal point · image role · anti-patterns
```

Never extract:

```
client identity · old logos · engagement facts · exact copy · exact layout
retired palettes · retired page furniture
```

**Rule AI2-X01.** Every retrieved reference is tagged `REFERENCE_ONLY`. Any fact
originating from a reference page is inadmissible as engagement evidence.

---

## 71.11 Stage 10 — Anti-template repetition (deck level)

Individual-page QA is structurally blind to deck monotony. Each page is reduced
to a composition fingerprint over grid signature, 4×4 mass profile, focal
signature, rhythm (area Gini + modal size count) and topology signature.

- Template twins: fingerprint distance < **0.085** within a 4-page window → FAIL
- Consecutive template run > 1 → FAIL
- Deck distinct-composition ratio < **0.70** → FAIL

Measured on the delivered MWAN deck: ratio **0.684**, 5 twin pairs → FAIL.

---

## 71.12 Stage 11 — Image generation as an ideation engine

Image generation is strong at global composition, spatial synthesis and visual
imagination; weak at exact Arabic copy, official values, logos, dates and
precise tables. Therefore:

**Rule AI2-I01.** Image generation is used to produce **3 structurally different
ways to represent the relationship**, not to produce a final slide.
**Rule AI2-I02.** Only composition, topology, spatial relationship, visual
metaphor and information hierarchy are harvested. Text inside generated images
is never used.
**Rule AI2-I03.** The winning topology is reconstructed natively (or via the
governed hybrid route) with exact copy and exact assets.
**Rule AI2-I04.** Image generation remains the **last tool action of the turn**,
after the content pack, graph, concepts, page spec, QA expectations and resume
state have been persisted.

---

## 71.13 Gate: `AI2_SYNTHESIS`

PASS requires **all** of:

1. Graph exists, every node typed, every relation evidence-referenced
2. Visual Problem Statement computed and persisted
3. ≥3 candidate compositions synthesised
4. Diversity index ≥ 0.45
5. ≥1 LEGAL candidate
6. LEGACY V2 metric only: former Artifact Strength ≥85/≥90. CURRENT release authority is independent Artifact Truth ≥90.
7. Composite area budgets declared and honoured

A page that fails `AI2_SYNTHESIS` may not proceed to Visual Imagination or
Production. This gate sits **upstream** of every render QA gate.

---

## 71.14 Reference results (reproducible)

Run `python detectors/artifact_synthesis.py <graph.json>`.

| Case | Graph | Band | Legal candidates | Winner | Score | Gate |
|---|---|---|---|---|---|---|
| Methodology page **as delivered today** | 7 nodes, **0 relations** | AC-2 | 5 | `MATRIX ⊕ RAIL` | **53.2** | **FAIL** |
| Same content, relationships modelled | 11 nodes, 14 relations | AC-4 | 4 | `TREE ⊕ SPINE ⊕ GAUGE ⊕ LANE ⊕ LOOP ⊕ FIELD` | **93.1** | PASS |
| REDF-style scope | 7 nodes, 10 relations | AC-3 | 3 | `HUB ⊕ GAUGE ⊕ BAND ⊕ SPINE ⊕ LOOP` | **95.2** | PASS |

The first two rows are the whole argument. **Identical content.** The only
difference is whether the relationships were modelled. Score moves 53 → 93.

The bottleneck was never the renderer.
