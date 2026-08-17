# SEC-DEP-001 — Section Dependency & Production Priority Authority

## Status
Priority-1 workflow invariant and release blocker.

## Purpose
Keep the owner-locked evaluator reading order separate from proposal production/finalization order while satisfying mandatory RFP forms and submission requirements without mutating the skeleton.

## Reader structure
Resolve first through `01_ACTIVE_RUNTIME/27_FINAL_SKELETON_IMMUTABILITY.md`:
- Reader order → Final Canonical Proposal Skeleton Owner Lock.
- RFP mandatory forms/headings/envelopes → map or attach without mutating Sections 0–8.
- Irreconcilable structure conflict → `STRUCTURE_CONFLICT_BLOCK`.

No workflow rule may rename, reorder, merge, split, delete, or replace the canonical section architecture.

## Pre-section control chain

```text
Approved INTERNAL_PURSUIT_BRIEF
→ Compliance Register v0
→ Evaluator Question Map
→ Issue Tree / Bid Thesis
→ Win Themes
→ Claim–Evidence Plan
→ Assumptions & Clarifications
→ Section Contracts
→ first dependency-ready substantive section
```

## Production principle
Do not start with the final Executive Summary merely because it appears early to evaluators.

Typical build sequence:
1. RFP/evidence and pursuit intelligence.
2. Bid/compliance control layer.
3. Client/scope/problem understanding.
4. Solution/methodology/workstreams/deliverables.
5. Delivery/governance/quality/risk.
6. Team/evidence/capabilities.
7. Commercial architecture.
8. Executive Summary late.
9. CEO Letter after Executive Summary.
10. Final compliance/page references/TOC.
11. Cover/close/final assembly.

The numbered section architecture is fixed by the Final Canonical Proposal Skeleton; only page expansion inside those IDs is dynamic.

## Staleness
A material upstream change marks dependent sections/pages `STALE` and blocks release until re-reviewed.

## Approval
Use the unified state machine and council operating RACI. Silence or “Next” is not approval; approval must identify the approved version/object.
