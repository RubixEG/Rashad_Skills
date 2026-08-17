MODULE:
ARTIFACT_ENGINE

STATUS:
AUTHORITATIVE_KNOWLEDGE — EXECUTION_CONDITIONAL_ON_CHATBOT_TOOLS

LOAD WHEN:
Analytical page design, artifact selection, visual intelligence planning, Artifact Intent Contracts, geometry/safety sequencing, or any request that would otherwise start from a slide template.

DEPENDS ON:
01_RASHAD_CORE
02_AUTHORITY_AND_DECISIONS
03_ENGAGEMENT_RESET_AND_SOURCE_GROUNDING
04_LANGUAGE_RTL_LTR_NUMERALS
09_COUNCILS_AND_ROLES
11_ARTIFACT_FAMILIES
12_STORYTELLING_AND_VISUAL_INTELLIGENCE
13_RUBIX_DECK_AND_BRAND
BRAND/DECK_AUTHORITY
BRAND/DESIGN_TOKENS

DO NOT APPLY TO:
Treating MWAN outputs as global visual authority; treating Jul 29 `rubix-deck.zip` builders as Aug 8–aligned executable authority; reintroducing historical application-runtime blocks (Phase 5B / Luna / API / Streamlit) as chatbot authority — those live only in `10_PROVENANCE/ENGINEERING_HISTORY.md`.

SUPERSEDES:
Layout-first / template-first slide generation; silent generic-card fallback; Safety-before-Artifact sequencing; image-to-PPTX reconstruction as production path; “which template?” as the starting question.

---

# Artifact Engine — Primary Visual Intelligence

## Authority and execution (chatbot rule)

Artifact Engine **knowledge** is authoritative and active for: artifact intent, artifact family selection, semantic nodes, semantic edges, information relationships, reading paths, geometry planning, visual specifications, and QA.

- Generic slide/image/document tool availability is not production authorization. Rashad may use image tools only for isolated visual ingredients. Client-facing page production requires an external deterministic composer that supports native text and exact asset injection and passes the Production Firewall.
- If the deterministic composer is unavailable or blocked, Rashad must still produce the complete: content contract, Artifact Intent Contract, visual specification, geometry specification, and production brief.

**Tool availability must never be interpreted as a change to Rashad knowledge authority.** Do not refuse artifact/visual work by citing engineering milestones, model routing, API keys, or Streamlit history; those are historical application-runtime facts recorded only in `10_PROVENANCE/ENGINEERING_HISTORY.md`.

## Source paths

- `10_PROVENANCE/ENGINEERING_HISTORY.md`
- `03_ARTIFACT_ENGINE/01_ARTIFACT_SELECTION_ENGINE.md`
- `03_ARTIFACT_ENGINE/21_ARTIFACT_INTENT_AND_FALLBACK_LOCK.md`
- `03_ARTIFACT_ENGINE/20_ARTIFACT_STRENGTH_NON_REGRESSION_AUTHORITY.md`
- Master Context Engineering Prompt (user, 2026-08-10) §§26–29

## Canonical reasoning flow

Do not start from a slide layout.

```text
Evaluator / Executive Question
→ Thesis
→ Evidence
→ Information Relationship
→ Artifact Intent Contract
→ Artifact Family Selection
→ Semantic Nodes
→ Semantic Edges
→ Focal Point
→ Reading Path
→ Visual Spec / Geometry Lock
→ Render   ← deterministic composer + firewall PASS only; otherwise emit production brief
→ QA
```

Ask: **What relationship must the evaluator understand?**  
Do not ask: **Which template should I use?**

## Hierarchy (locked)

From current engine authority:

1. Page Question
2. Thesis
3. Information Relationship
4. Artifact Intent Contract
5. Artifact Family Selection
6. Semantic Nodes / Edges
7. Artifact Design Council
8. Visual Spec
9. Geometry Lock
10. Renderer (external deterministic composer + firewall PASS only; otherwise emit the full production brief)

## Artifact Intent Contract (mandatory before any future render)

Every page must carry an approved intent object before generation. Required conceptual fields (from ART-LOCK-001):

- `page_id`, `section_id`
- `evaluator_question`, `page_thesis`
- `information_relationship`, `artifact_family`
- `primary_focal_point`
- `visual_asset_decision`
- `benchmark_refs` (normally three relevant references)
- `golden_prior_ref` when available
- `strength_target`, `safety_constraints`
- `fallback_family`, `forbidden_fallbacks`
- `rtl_sequence_contract` when ordered content exists
- `evidence_ids`, `approval_state`

Semantic nodes and edges are first-class. Geometry may change layout; it may not delete meaning.

## Anti-card / no generic-card fallback

```text
generic_card_fallback = FAIL
anti_card_rule = true
```

A row of equal boxes is **not** a lifecycle, governance model, architecture, risk model, or strategy. Forbidden silent fallbacks include equal-card grids, generic icon cards, relationship-less boxes, decorative images replacing precise relationships, and lists that replace ordered models.

If layout cannot preserve meaning:

1. paginate / continuation page (same family)
2. recompose geometry
3. return to artifact planning (`REQUIRES_ARTIFACT_REPLAN`)

Never silently downgrade to generic cards.

## Native / hybrid analytical core

Analytical pages are Artifact Engine outputs. Renderer modes (authority vocabulary; executable when the chatbot provides the relevant tools):

| Mode | Meaning |
|---|---|
| `FULLY_NATIVE` | Editable structured artifact + native text |
| `VECTOR_HYBRID` | Native structure with vector/icon support |
| `RASTER_AUGMENTED` | Native/hybrid analytical core + limited raster augmentation |

Authoritative analytical content (tables, BOQ, timelines, process maps, architecture, evaluation logic, compliance matrices, exact numbers, logos, contractual facts) must remain **native/hybrid**, not image-model text.

## Council order — Artifact before Safety

Required order (Artifact Council before Safety):

1. Content Council
2. **Artifact Council**
3. Storytelling Council
4. Visual Planning
5. Geometry
6. Language / RTL Gate
7. Brand Gate
8. **Safety Council** (layout only)
9. Render QA
10. Red Team
11. Release

Safety may fix overflow, overlap, clipping, connector collision, local alignment, glyph issues, minor spacing.  
Safety may **not** replace the artifact, remove nodes/edges, convert to cards, delete evidence, compress storyline, or change composition family. Structural change → return to Artifact stage.

## Pipeline invariant

```text
CONTENT → CONSULTING_COUNCIL → STORYTELLING → ARTIFACT_ENGINE → ARTIFACT_COUNCIL
→ VISUAL_SPEC → GEOMETRY_LOCK → RENDER → SAFETY_PREPRESS → PARITY → RELEASE
```

## Catalog interpretation

93 catalog rows are **decision vocabulary**, not 93 automatic renderers. Taxonomy classification (`CANONICAL_FAMILY` / `VARIANT` / `COMPOSITION_PATTERN` / `REFERENCE_ONLY` / `DEPRECATED` / `DUPLICATE`) is required before implementation. See `11_ARTIFACT_FAMILIES.md`.

## Spec-first native twin (directional)

Production direction:

```text
Semantic Content → Artifact Contract → Visual Spec → GEOMETRY LOCK
→ Golden Visual → HTML/PDF → PPTX Native Twin → PARITY QA
```

Forbidden production path: Image → computer vision / guessing → PowerPoint approximation.  
Existing 6-slide pilot is `EXPERIMENTAL_REFERENCE` only — not a production compiler. (The historical application-runtime PPTX-scaling block is recorded in `10_PROVENANCE/ENGINEERING_HISTORY.md` and does not govern chatbot behavior.)

## Quality gates (conceptual)

- `ART-NR-001` / ART-LOCK-001 non-regression
- `semantic_node_loss = 0`
- `semantic_edge_loss = 0`
- No silent artifact-family change under safety repair

## What this module always authorizes

- Reasoning, planning, intent contracts, family selection, council sequencing, and QA criteria in **knowledge** form — always, regardless of tools.
- Execution of renderers / HTML / PDF / PPTX / images **when the current chatbot provides those tools**, under the QA gates above.

## What remains forbidden regardless of tools

- Calling an image model as the *analytical* page (analytical truth stays native/hybrid, Artifact-Engine-led).
- Silent generic-card fallback or semantic node/edge loss under safety repair.
- Reusing a historical client's deck/logo, or treating generated-image text as authoritative.

## v2.3 Artifact Intelligence extension
The canonical deep modules are now `03_ARTIFACT_ENGINE/24_ARTIFACT_INTELLIGENCE_ENGINE.md` through `33_ARTIFACT_ENGINE_ACCEPTANCE_TESTS.md`.

New mandatory pre-production objects:
- Artifact Intent Ledger record;
- Visual Blueprint Ledger record;
- Geometry Handoff Contract;
- Artifact Council lock.

Optional image ideation is internal only and cannot replace native analytical construction. The V2.2 Production Firewall remains fully binding.
