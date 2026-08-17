# LAY-PRES-001 — Artifact-Preserving Layout Assurance Authority

## Status
Priority-0 production authority. It applies after artifact intent is approved and before any HTML, PDF, or PowerPoint release.

## Purpose
Prevent overflow, clipping, text collision, text appearing above or behind cards, numeric escape, and PDF/PPTX reflow **without weakening, skipping, simplifying, or replacing the approved artifact**.

The rule exists because technical safety and artifact strength are separate concerns. A page is not acceptable when it is visually powerful but broken, and it is also not acceptable when it is technically safe only because the renderer replaced a lifecycle, architecture, dependency map, evaluation funnel, or evidence system with generic cards.

## Absolute principle

```text
Approved Artifact Intent
+ Artifact Signature Lock
+ Layout Repair
+ Safety PASS
+ Strength PASS
= Approved Page
```

A layout defect authorizes a geometry repair. It does **not** authorize a semantic redesign.

## Independent production role
Every client-facing deck must assign a **Proposal Artifact Integrity & Prepress Director**. This role is independent from:
- the proposal strategist;
- the content author;
- the artifact architect;
- the visual-asset generator;
- the renderer engineer.

The director owns layout integrity and cross-format preflight, but may not silently change:
- evaluator question;
- page thesis;
- information relationship;
- artifact family;
- semantic topology;
- sequence direction;
- evidence mapping;
- primary focal point;
- visual-asset role;
- approved benchmark floor.

## Artifact Signature Lock
Before layout begins, record an immutable signature:

```json
{
  "artifact_id": "",
  "page_id": "",
  "evaluator_question_id": "",
  "page_thesis": "",
  "information_relationship": "",
  "artifact_family": "",
  "semantic_nodes": [],
  "semantic_edges": [],
  "ordered_sequence": [],
  "focal_point": "",
  "evidence_ids": [],
  "visual_asset_ids": [],
  "golden_benchmark_ids": [],
  "minimum_strength_score": 0
}
```

After every repair, compare the page with the signature. Release requires:
- no missing semantic node;
- no changed edge or sequence;
- no replaced artifact family;
- no removed evidence;
- no lost visual asset required by the brief;
- no lower strength score;
- no new generic-card fallback.

## Page Zone Contract
Every page must calculate and reserve four measured zones after approved fonts are loaded:
1. **Header/identity zone** — logos, section marker, page furniture.
2. **Title zone** — title and subtitle only.
3. **Artifact body zone** — cards, diagrams, charts, illustrations, tables, callouts.
4. **Footer/source zone** — source, confidentiality, page number, footer line.

The body zone starts at:

```text
body_zone_top = measured_title_block_bottom + approved_vertical_clearance_token
```

Hard requirements:
- no body component may begin above `body_zone_top`;
- no free-floating text may sit between the title zone and a card unless it is declared in the page contract;
- no title/subtitle may extend into the artifact body;
- no card, bar, connector, annotation, or image may enter the footer zone;
- every text node must belong to a named component or declared annotation zone;
- `z-index`, clipping, negative margins, transforms, or `overflow:hidden` may not conceal a violation.

## Text and Glyph Geometry Validation
Do not rely only on `scrollHeight` or element boxes. After `document.fonts.ready`, validate actual rendered text using `Range.getClientRects()` or equivalent glyph/line geometry.

Reject when any rendered text rectangle:
- crosses its component content box after padding;
- intersects text from another component;
- intersects an icon, badge, number, bar, connector label, or footer not declared as an overlay;
- sits behind or above an adjacent card;
- leaves the page safe zone;
- is clipped, ellipsized, hidden, or covered.

Parent-child containment is allowed. Independent component intersection is not.

## Numeric and Mixed-Script Validation
Percentages, Arabic-Indic numbers, English codes, and mixed Arabic/English strings must be tested as rendered glyphs, not only as text values. The whole token—including percent sign, separator, and unit—must remain inside its intended box with safe padding.

## Repair Ladder — preserve the artifact
When a defect is found, repair in this order:

### Tier 1 — Geometry repair
- increase or rebalance internal padding;
- adjust grid tracks and component widths;
- increase component height within the body zone;
- align baselines and connector anchors;
- move annotations to declared callout zones;
- change line breaks intentionally;
- rebalance whitespace around the same focal point.

### Tier 2 — Typography repair within approved tokens
- use the next approved type-size token for supporting copy only;
- adjust line-height or paragraph spacing within the brand system;
- never apply global page scaling;
- never shrink titles, key numbers, or decision statements below approved minimums.

### Tier 3 — Editorial compression
- remove duplication and filler only;
- preserve every requirement, claim, evidence item, qualifier, number, and decision implication;
- record before/after copy and confirm semantic equivalence;
- do not summarize away evaluation-critical detail.

### Tier 4 — Artifact-preserving continuation
If the page still cannot fit, split it into a coordinated two-page sequence while preserving the artifact family:
- page A presents the full system/architecture/logic;
- page B continues detail, evidence, or controls;
- both pages retain the same visual grammar and explicit continuation marker;
- page references, dependencies, and Compliance Matrix update automatically.

### Tier 5 — Escalation
Return the page to the Artifact Architect with a defect report. The renderer is not allowed to substitute generic cards, remove the visual asset, flatten the relationship, or skip the artifact.

## Forbidden repairs
- converting a lifecycle into equal cards;
- converting dependencies into a list;
- converting architecture into a logo cloud;
- converting escalation into unsupported bars;
- removing images, icons, evidence, or connectors merely to create space;
- deleting content without claim/evidence review;
- global font shrinking;
- whole-page scaling;
- clipping or hiding overflow;
- rasterizing the page;
- changing RTL sequence geometry;
- releasing HTML while PDF or PPTX fails.

## Strength preservation gate
After repair:
- page strength score must be equal to or higher than the approved pre-layout score;
- artifact-family and topology hashes must match;
- card-led share must not increase unless cards were the approved relationship;
- the page must remain at or above the golden benchmark floor;
- the visual-asset decision must remain fulfilled.

## Evidence bundle required for release
Each repaired page produces:
- pre-repair screenshot;
- post-repair HTML screenshot;
- PDF raster screenshot;
- PowerPoint-exported PDF screenshot;
- bounds/collision report;
- artifact-signature diff;
- content-diff report;
- strength score before/after;
- AR-SEQ/AR-GRP validation when applicable;
- director approval record.

A page with an empty report but visible failure, or a report containing unresolved issues, cannot be released.
