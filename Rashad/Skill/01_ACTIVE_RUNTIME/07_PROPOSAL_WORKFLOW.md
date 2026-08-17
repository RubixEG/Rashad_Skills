MODULE:
PROPOSAL_WORKFLOW

STATUS:
AUTHORITATIVE

LOAD WHEN:
User requests proposal generation, section drafting, Bid Strategy, next-section recommendation, or end-to-end engagement progression after RFP Summary.

DEPENDS ON:
00_START_HERE
01_RASHAD_CORE
02_AUTHORITY_AND_DECISIONS
03_ENGAGEMENT_RESET_AND_SOURCE_GROUNDING
04_LANGUAGE_RTL_LTR_NUMERALS
05_RFP_INGESTION
06_RFP_SUMMARY
08_FINAL_PROPOSAL_SKELETON
09_COUNCILS_AND_ROLES
SECTION_DEPENDENCIES
CURRENT_RFP_SOURCES
ENGAGEMENT_STATE

DO NOT APPLY TO:
Reintroducing historical application-runtime blocks (Phase 5B / Luna / API / Streamlit) as chatbot authority; inventing section names; treating reader order as production order.

SUPERSEDES:
Any workflow that drafts Executive Summary or CEO Letter before their material input dependencies stabilize; any workflow that drafts Section 3 before approved RFP Understanding Summary and Bid Strategy Gate; historical “generate deck first” paths; GM v2.1 rules that conflict with adaptive Summary authority after Milestone-1 cutover.

---

# Proposal Workflow

## 1. Purpose

This module is the **production operating procedure** for Rashad proposals. It defines how an engagement moves from RFP intake to section-by-section generation, approvals, late executive pages, compilation in reader order, and release gates.

It does **not** redefine the reader-facing skeleton. Reader order lives in `08_FINAL_PROPOSAL_SKELETON.md`. Dependency and readiness rules live in `SECTION_DEPENDENCIES.md` (`SEC-DEP-001`).

## 2. Hard distinction — reader order vs production order

| Axis | Authority | Rule |
|---|---|---|
| **Reader order** | Final Canonical Proposal Skeleton Owner Lock | Sections 0–8 and front/back matter remain fixed; RFP mandatory forms are mapped/supplemental. |
| **Production orchestration** | Dependency Ledger + Product Completion Contract | What the team builds: Summary → controls → Bid Strategy → **eligible proposal workstreams in parallel** → dependency-bound late syntheses (Executive Summary / CEO Letter) → shell/pagination → QA/release. Reader order never creates a dependency by itself. |
| **Finalization order** | `SEC-DEP-001` | Same dependency spine as production for approvals; early Strategy Skeleton is not final Section 2 |

Never rename/reorder the owner-locked canonical skeleton. Map RFP-mandated headings/forms into canonical section IDs or supplemental artifacts. If that is impossible, raise `STRUCTURE_CONFLICT_BLOCK`.

## 3. Current posture (accepted authority)

- Adaptive RFP Summary content path is the current Summary product contract.
- **Artifact Engine knowledge/contracts are authoritative and always active.**
- **Execution follows deterministic-composer availability, not generic tool availability:** image generation may supply isolated ingredients; client-facing page rendering requires native text + exact asset injection + firewall PASS. Otherwise produce content + contracts + council findings + full production brief.

Never refuse render/visual work on the basis of historical application-runtime milestones (Phase 5B / Luna / API / Streamlit) — those are recorded only in `10_PROVENANCE/ENGINEERING_HISTORY.md`.

## 4. End-to-end production chain

```text
ENGAGEMENT_RESET
→ RFP ingestion / source register / pack mode
→ evidence extraction + reconciliation (+ Appendix Library inspect)
→ INTERNAL_PURSUIT_BRIEF / Adaptive RFP Understanding Summary
→ council review + user approval of Summary
→ Compliance Register v0 + Bid Strategy Gate + Section Contracts
→ ACTIVATE CONTROLLED PARALLEL BID WORKSTREAMS
   A Solution/Methodology
   B Compliance/Requirements
   C Team/CVs/Evidence
   D Commercial/Pricing inputs
   E Legal/Cyber/Data/Technical assurance as applicable
   F Editorial/Arabic/Translation
   G Artifact/Brand/Production planning
→ Draft each substantive section when its own dependency ledger says READINESS=READY
→ Integrate Delivery/Governance once methodology/workstreams are stable enough
→ Stabilize Team/Evidence/Commercial commitments
→ Executive Summary late
→ CEO Letter after Executive Summary
→ Final Compliance Matrix after references stabilize
→ Compile in the owner-locked Final Canonical Proposal Skeleton reader order
→ QA / Red Team / Release
```

### 4.1 Bid Strategy Gate contents (mandatory before Section 3)

```text
Evaluator Question Map
→ Issue Tree
→ Bid Thesis
→ Win Themes
→ Claim–Evidence Plan
→ Assumptions and Clarifications Register
→ Executive Summary Strategy Skeleton (internal, incomplete)
```

Missing Bid Strategy approval blocks every substantive proposal section.

### 4.2 Section cycle (interactive, every section)

For every node with `READINESS=READY` and a canonical state that permits work:

1. Determine section objective (evaluator question).
2. Load relevant RFP evidence only.
3. Load exact Rashad R-codes / scopes for the section.
4. Invoke relevant routed councils (findings required; names alone are not review).
5. Create **content first**.
6. Identify artifact intent / information relationship.
7. Design artifact (knowledge/contract level).
8. Create visual plan.
9. Render only when an external deterministic composer is available, the user requested production, and the Production Firewall passes; otherwise deliver the production brief.
10. Run QA appropriate to current posture.
11. Update `ENGAGEMENT_STATE`.
12. Recommend the next section (never only “What next?”).

Never jump to images when content is unstable unless the user explicitly asks.

## 5. P0 Proposal Control Layer (internal; not reader sections)

These objects precede Section 3 drafting:

1. Compliance Register v0  
2. Evaluator Question Map  
3. Issue Tree  
4. Bid Thesis  
5. Win Themes  
6. Claim–Evidence Plan  
7. Assumptions and Clarifications Register  
8. Executive Summary Strategy Skeleton  
9. Section Contracts  

### Distinctions that must not collapse

- **Strategy Skeleton ≠ Section 2.** Skeleton guides; Section 2 is finalized late.
- **Compliance Register v0 ≠ Section 0.** Register starts early; Section 0 finalizes after page/appendix references stabilize.
- **RFP Understanding Summary ≠ Executive Summary.** Summary is the internal consulting brief first.

## 6. Dependency-driven parallel production

After Bid Strategy approval, **reader order must not serialize the team**. Activate workstreams in parallel and let the Dependency Ledger determine readiness.

| Workstream | Starts | Blocking dependencies for lock |
|---|---|---|
| Solution / Client Environment | After Summary + Bid Strategy + relevant Section Contract | Current RFP evidence and client need/scope stable |
| Methodology | May start in parallel with Solution once problem/scope/workstreams are stable | Scope/workstreams, evaluator logic, solution thesis |
| Delivery & Governance | Design may start while Methodology is under review | Methodology/workstream architecture stable enough; timeline/dependency inputs |
| Capabilities / Experience | Evidence collection starts day one; narrative can draft after win themes | Verified case/CV/company evidence matched to criteria |
| Appendix / Evidence | Starts day one | A0–A3 evidence gates for final lock |
| Commercial | Estimation model starts early; final commercial narrative waits | Scope/WBS, volumes, team, schedule, assumptions, third-party/support exposure |
| Legal/Cyber/Data/Technical assurance | Starts as soon as applicable requirements are discovered | Critical findings closed before release |
| Editorial / Arabic / Translation | Style prep can start early; final edit after content lock | Content semantics locked for final pass |
| Artifact / Brand / Production | Artifact intent follows approved content blocks; production follows firewall | Artifact lock + exact assets + external composer + QA |

**Late-only objects:** Executive Summary, CEO Letter, final Compliance Matrix, final TOC/pagination.

No active rule may require “Section 4 waits for full Section 3 approval” merely because of reader numbering. It may wait only for a **material dependency** recorded in the Dependency Ledger.

## 7. Next-section recommendation contract

After any major deliverable, return:

```text
COMPLETED:
[section]

BLOCKING GAPS:
[only if present]

RECOMMENDED NEXT SECTION:
[next section]

WHY:
[brief reason]
```

Evaluate: section dependencies, unresolved evidence, proposal risk, user approvals, completed sections, commercial dependencies, team dependencies.

Examples:

- After RFP Summary → Compliance Register / Bid Strategy path (convert obligations into controlled response map).
- After Summary with incomplete mandatory team evidence → Team & Evidence Readiness before commitments.

## 8. Council routing in the workflow

Route functions to **verified runtime-enabled roles only** (28). See `09_COUNCILS_AND_ROLES.md`.

| Workflow stage | Routed council function |
|---|---|
| Summary / bid readiness | Content; RFP/Bid; Clarification & Risk; Evidence/Compliance |
| Bid Strategy | RFP/Bid; Clarification & Risk; Commercial (conditional); Team Composition; Timeline |
| Sections 3–6 | Content; Storytelling; Artifact (plan); sector/tech conditionals |
| Section 7 | Evidence/Compliance (Appendix bundle); Brand QA |
| Section 8 | Commercial; Legal; Procurement |
| Pre-release | Artifact; Safety; Brand QA; Red Team / Release |

Critical Compliance, Legal, Cyber, Evidence, Red Team, Artifact, or Prepress findings **block release**.

## 9. Artifact posture inside this workflow

Preserve Artifact Engine as highest-priority production intelligence **after content correctness**:

```text
Evaluator/Executive Question → Thesis → Evidence → Information Relationship
→ Artifact Intent Contract → Family → Semantic Nodes/Edges
→ Artifact Council → Visual Spec → Geometry Lock → Render → Safety → Parity → Release
```

Execution rule:

- Execute client-facing rendering only when capability preflight proves an approved deterministic composer; generic rendering/image/document tool availability is insufficient.
- When the deterministic composer is unavailable or blocked, keep contracts, node/edge intent, and council findings in engagement state and deliver the production brief.
- Do **not** claim to have compiled a file (PPTX/PDF/HTML) that was not actually produced.

Safety remains downstream of Artifact Council. Safety may not replace artifacts with generic cards.

## 10. Anti-contamination and honesty rules

- Initialize every engagement from current RFP evidence only.
- Historical proposals are reference-only under External Proposal Reference Method; never current facts.
- Never invent requirements, CVs, certificates, prices, outcomes, or compliance.
- Label analytical claims as `Stated Fact | Logical Inference | Assumption` in working notes.
- Appendix Library gaps must be disclosed; never invent appendix pages.
- If Appendix Library missing: `APPENDIX_LIBRARY_MISSING` blocks bid-readiness approval.

## 11. Hard fails

- Drafting Section 3 before Bid Strategy approval.
- Starting any node while `READINESS=NOT_READY` or a blocking dependency/council finding is open.
- Finalizing Section 2 before Sections 3–8 stabilize.
- Writing CEO Letter before Section 2.
- Finalizing Section 0 before page references stabilize.
- Keeping dependent `APPROVED`/`LOCKED` nodes unchanged after material upstream change (must mark `STALE`).
- Executing unverified “67 roles” or inventing role names.
- Claiming a render/compile happened when no tool actually produced it.

## 12. Source paths

| Source | Path | Controls |
|---|---|---|
| Reader skeleton | `FINAL_CANONICAL_PROPOSAL_SKELETON_EN.md` / `FINAL_CANONICAL_PROPOSAL_SKELETON_AR.md` | Owner-locked reader-facing order/names |
| Detailed CRAFT library | `rubix-proposal-master-skeleton-v2.md` | Slide/detail prompt patterns only; no section-architecture authority |
| SEC-DEP-001 | `05_WORKFLOW_ENGINE/06_SEC_DEP_001_SECTION_DEPENDENCY_AUTHORITY.md` | Readiness/production/finalization |
| E2E workflow | `05_WORKFLOW_ENGINE/01_END_TO_END_WORKFLOW.md` | Step sequence |
| SKILL invariant | `SKILL.md` | SEC-DEP-001 / RFP-SUM-001 boundaries |
| Project instructions | `PROJECT_INSTRUCTIONS.md` | Operating procedure (annotate GM conflicts) |
| Artifact-first policy | `03_ARTIFACT_ENGINE/20_ARTIFACT_STRENGTH_NON_REGRESSION_AUTHORITY.md` | Artifact before Safety |
