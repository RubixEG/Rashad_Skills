MODULE:
SECTION_DEPENDENCIES

STATUS:
AUTHORITATIVE — CURRENT

LOAD WHEN:
User asks what section to draft next, whether a section is ready, how reader order differs from production order, or how a change propagates.

DEPENDS ON:
- `07_PROPOSAL_WORKFLOW`
- `08_FINAL_PROPOSAL_SKELETON`
- `27_FINAL_SKELETON_IMMUTABILITY`
- current RFP sources
- current Section Contracts

# Section Dependencies

## 1. Core distinction
Separate:
1. **Reader order** — what the evaluator must receive/read.
2. **Production order** — what the team must create first.
3. **Finalization order** — what can be locked only after dependencies stabilize.

Reader order is fixed by the owner-locked Final Canonical Proposal Skeleton.

RFP requirements may add mandatory forms, attachments, navigation, or pages inside the locked IDs, but they do not rename or reorder Sections 0–8. If a legally mandatory reader structure cannot coexist with the lock, set `STRUCTURE_CONFLICT_BLOCK` and require explicit owner resolution.

## 2. Production control flow

Regardless of reader order, the normal dependency logic is:

```text
RFP ingestion + engagement reset
→ evidence / requirement / evaluation extraction
→ INTERNAL_PURSUIT_BRIEF RFP Summary
→ council review + approval
→ Compliance Register v0
→ Bid Strategy / evaluator question map / win themes
→ Section Contracts
→ dependency-ready substantive solution/delivery sections
→ team/evidence/commercial stabilization
→ final Executive Summary late
→ CEO Letter after final Executive Summary
→ final Compliance Matrix / references
→ Cover / TOC / Close / Pagination
→ QA / release
```

If the RFP mandates supplemental forms or navigation, map these production objects to the fixed canonical IDs without changing their analytical dependency. An irreconcilable reader-structure requirement triggers `STRUCTURE_CONFLICT_BLOCK`.

## 3. Canonical state + derived readiness

Persist node state using **only**:
`NOT_STARTED | DRAFT | REVIEW_REQUIRED | APPROVED | LOCKED | STALE | BLOCKED | REJECTED | SUPERSEDED`.

Readiness is a separate derived attribute:
- `READINESS=READY` when all blocking dependencies/evidence/approvals required to start the next stage are satisfied.
- `READINESS=NOT_READY` otherwise.

Use `07_GOVERNANCE_AND_QA/19_UNIFIED_STATE_MACHINE.md`. Do not persist `READY_TO_DRAFT`, `IN_DRAFT`, `IN_REVIEW`, `CHANGES_REQUIRED`, `CONTENT_DRAFT`, `VISUAL_DRAFT`, or `FINAL`.

## 4. Dependency examples

- Methodology depends on client need/scope/evidence.
- Timeline depends on phases, activities, deliverables, gates, client dependencies and team capacity.
- Governance depends on workstreams, decision needs, risks, ownership and delivery cadence.
- Team depends on workstreams, workload, mandatory RFP roles and mobilization assumptions.
- Commercial logic depends on scope/WBS, timeline, team, third-party/tools/support obligations, assumptions and risk allocation.
- Risk register depends on the proposed solution, commercial model, delivery plan, launch/operations obligations and open dependencies.
- Executive Summary depends on approved downstream logic; it cannot be authored as an isolated first draft.
- CEO Letter depends on the final Executive Summary, final win themes and final commitments.
- Compliance Matrix and TOC/page references depend on final assembly/pagination.

## 5. Change propagation

A material change marks every dependent node `STALE`.
Examples:
- duration changes → roadmap, resource loading, support, commercial, risk, executive summary;
- deliverable definition changes → methodology, timeline, team, BOQ, acceptance, risk, commercial;
- mandatory RFP forms/submission requirements → canonical section/page mapping, compliance matrix, supplemental artifacts, TOC and final assembly;
- client clarification changes scope/volume → assumptions, solution, effort, price, team, schedule and relevant summaries.

No stale node can be released.

## 6. Tool boundary
Rendering/slide/export steps execute only when an external deterministic composer capable of native text and exact asset injection is actually available and the Production Firewall passes. Otherwise produce approved content/artifact specifications and explicitly record production rendering as blocked.
