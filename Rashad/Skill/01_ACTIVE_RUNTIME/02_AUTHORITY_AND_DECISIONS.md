MODULE: 02_AUTHORITY_AND_DECISIONS
STATUS: AUTHORITATIVE
LOAD WHEN: Any conflict, version dispute, “which file wins,” regression argument, or before treating a historical skill/output as current.
DEPENDS ON: 00_START_HERE; 01_RASHAD_CORE
DO NOT APPLY TO: Choosing authority by filename version number alone or by file mtime alone; reopening RESOLVED CONF-001..007 as open authority fights; treating implementation gaps as unresolved authority conflicts.
SUPERSEDES: GM v2.1 conflicting Summary rules; VIS-KB-001 production; global Golden MWAN; Jul-29 deck as decision authority; M2D-as-present-code claims; v7.0 / Connect v6.4 packages as active OS.

# Authority and Decisions

## Authority hierarchy (latest accepted)

Unless later explicit user decision overrides:

1. Latest explicit final **user** decisions (chronological conversation / approvals)
2. **Final Canonical Proposal Skeleton Owner Lock for proposal architecture only** — `PSK-OWNER-LOCK-2026-08-12`; section IDs/order/hierarchy cannot be auto-overridden
3. **Current engagement RFP evidence and mandatory submission requirements** — including appendices, official clarifications/addenda, evaluation, legal, cyber, procurement, data, security, commercial, forms, and compliance requirements
4. Latest accepted Rashad operating rules and hard fail-closed / integrity rules
5. Final product-specific contracts
6. Exact Rashad prompt corpus (immutable analytical authority; never a source of engagement facts)
7. Canonical proposal skeleton detailed language files — governed by the Owner Lock; never a fallback-only house template
8. Current Rubix brand / visual identity decisions
9. Appendix / evidence library for evidence availability only
10. Brand reference documentation
11. Historical proposal examples — **REFERENCE / METHOD INTELLIGENCE ONLY**
12. Old versions / rejected experiments / superseded outputs

**Never** pick authority only because a path contains a higher version string or a newer filesystem date. Use the decision trail.

## Active authority classes

| Class | Meaning |
|---|---|
| CANONICAL_AUTHORITY | Immutable or primary OS source (e.g. prompts master) |
| CURRENT_AUTHORITY | Active product/contract rules |
| CURRENT_ARTIFACT_AUTHORITY | Artifact vocabulary/method (always active; production execution requires external deterministic composer + firewall PASS) |
| CURRENT_DIRECTION | Approved direction; pilot may be experimental |
| SUPERSEDED_IN_PART | Keep non-conflicting ops detail; ignore conflicting rules |
| STALE_IMPLEMENTATION | Exists as code/assets but must adapt to authority |
| DEPRECATED | Must not control production |
| EXPERIMENTAL_REFERENCE | Study only; not production compiler |
| ENGAGEMENT_OUTPUT_NOT_AUTHORITY | Client-specific deliverable; not global rule |

## Cutover locks (Milestone-1 — APPROVED 2026-08-09)

| Lock | State |
|---|---|
| `blocking_authority_conflicts` | **0** |
| GM v2.1 visible Source Coverage | SUPERSEDED |
| GM v2.1 fixed Summary architecture | SUPERSEDED |
| VIS-KB-001 production | DEPRECATED |
| Global Golden MWAN | REMOVED |
| Jul-29 `rubix-deck.zip` | STALE_IMPLEMENTATION |
| M2D local code | NOT_PRESENT — historical claim only |
| Native twin 6-slide pilot | EXPERIMENTAL_REFERENCE |

Known **implementation gaps** remain allowed. Gaps ≠ open authority conflicts.

## Resolved conflicts (do not reopen)

### CONF-001 — Visible Source Coverage
**Final (v2 product split):** `CLIENT_FACING_RFP_UNDERSTANDING` hides Source Coverage/Confidence mechanics by default. `INTERNAL_PURSUIT_BRIEF` may visibly show **Source Coverage, Gaps & Conflicts** when it materially affects estimation, pricing, qualification, schedule, or bid decision. Source Manifest, Evidence Ledger, Claim/Contradiction registers, and detailed confidence mechanics remain internal.

### CONF-002 — Adaptive Summary
**Final:** Adaptive Summary wins. No mandatory fixed 15/20-page architecture. Pack modes: `SCOPE_ONLY` | `PARTIAL_RFP_PACK` | `FULL_RFP_PACK`. A page does not exist merely because a document category exists.

### CONF-003 — Visual KB
**Final:** ExternalProposalReferenceSession wins. No permanent cross-engagement visual corpus. VIS-KB-001 deprecated as production authority.

### CONF-004 — Golden MWAN
**Final:** Semantic Non-Regression wins. MWAN may be a **temporary engagement-specific baseline only when explicitly supplied** — never global gate.

### CONF-005 — Renderer runtime
**Final:** Aug-8 decisions are authority. Jul-29 deck is stale. Do **not** weaken decisions to fit old deck limits; create deck-adapter gaps instead.

### CONF-006 — M2D presence
**Final:** Do not claim M2D exists locally; do not blindly recreate it. Map F1–F13 to current needs; reimplement missing keepers only. F3 permanent KB / F13 Golden MWAN are superseded paths.

### CONF-007 — Clarification quality
**Final:** Expert Clarification Council + admission test + `ETIMAD_AWARENESS_GATE` supersede generic/completeness-checklist questions.

## Deprecated rules (must not remain active instructions)

| ID | Old rule | Replacement |
|---|---|---|
| DEP-001 | Global Golden MWAN | Semantic Non-Regression + engagement baseline |
| DEP-002 | VIS-KB-001 production corpus | External reference session + abstract patterns |
| DEP-003 | Image → guess geometry → PPTX | Spec-first native twin from shared visual_spec |
| DEP-004 | Generic-card fallback | Fail closed / RETURN_TO_ARTIFACT_STAGE |
| DEP-005 | Default Office / Arial-Calibri-Aptos brand | Current Rubix identity |
| DEP-006 | Raster screenshot PPTX as editable | Native elements; raster for photo/hero only |
| DEP-007 | Safety redesigns artifacts | Constrained repair ladder only |
| DEP-008 | Visible Source Coverage | Internal pursuit: allowed when decision-material; client-facing: internal QA by default |
| DEP-009 | Naive Etimad / generic clarifications | Expert Clarification + ETIMAD gate |
| DEP-010 | Fixed Summary page architecture | Adaptive pack modes |
| DEP-011 | Old deck/logo as identity | Aug-8 brand; Jul-29 STALE |
| DEP-012 | Enable all 67 claimed roles | Verified roles only |
| DEP-013 | 93 catalog rows = 93 renderers | Classify vocabulary first |
| DEP-014 | Scale 6-slide pilot as production | EXPERIMENTAL_REFERENCE |
| DEP-015 | Blindly recreate M2D | Historical claims; map gaps |
| DEP-016 | Alter Aug-8 decisions for old deck | Adapter under CONF-005 |

## Decision lifecycle labels

Use these in ledgers when reconstructing history:

`PROPOSED → TESTED → ACCEPTED → CURRENT`  
or `PROPOSED → TESTED → REJECTED`  
or `CURRENT → SUPERSEDED`

Rejected approaches belong in failure/decision libraries — **not** in active instructions.

## Artifact Engine execution gate (latest)

Artifact Engine remains **authoritative knowledge**, and it is always active for reasoning, planning, intent, selection, geometry, and QA. Client-facing production is unlocked only when `36_CAPABILITY_PREFLIGHT_AND_TOOL_ROUTING.md` confirms a **deterministic composer** that can satisfy the approved Visual Blueprint / Geometry Handoff, inject exact assets, preserve native text/RTL/numerals, and support required QA. The mere presence of generic chatbot rendering/image/document tools is insufficient. The former Phase 5A/5B / Luna / Smoke / API gates are `HISTORICAL_ENGINEERING_STATE` and live in `10_PROVENANCE/ENGINEERING_HISTORY.md`; they do not govern chatbot sessions.

## Sources and authority

- User master prompt §§4–5, 48–51 (2026-08-10)
- User approvals: Stage-0; M1 Authority Cutover; Phase 4; Phase 5A engineering posture
