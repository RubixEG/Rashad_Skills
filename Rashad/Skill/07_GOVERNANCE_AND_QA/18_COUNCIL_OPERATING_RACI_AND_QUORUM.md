# Council Operating RACI, Quorum and Decision Control

STATUS: CURRENT HARD GOVERNANCE

A council is an executed review function, not a role-name list. Every required role must produce a finding, decision, approval or explicit `NO_FINDING` record.

## Core council for OS/skill changes
| Role | Owns | Approval / blocking rights |
|---|---|---|
| AI Skill Architect / Context Engineer | authority map, context loading, supersession, contamination prevention | blocks authority conflicts / context pollution |
| Consulting Partner | strategic posture, commitments, bid risk, client promise | approves major commercial/strategic commitments |
| Proposal Director | evaluator journey, proposal thesis, win strategy, section coherence | owns proposal/summary content baseline |
| Senior Project Manager | delivery feasibility, WBS, dependencies, resources, acceptance, bid plan | blocks infeasible delivery assumptions |
| Operations & Launch Lead | go-live, transition, handover, hypercare, support/BAU | blocks unsupported launch/operations commitments |
| Governance & Decision-Control SME | decision records, state machine, RACI, due gates, escalation | blocks undocumented approvals/state conflicts |
| Artifact / Brand / RTL Production SME | artifact intent, palette, logo, RTL, geometry, cover production | blocks visual/brand/RTL failures |
| Theme & Color Governor | palette semantics, color balance, light-canvas enforcement, secondary-accent discipline | blocks off-palette color, black/near-black slides, rainbow misuse, brand-anchor drift |
| QA & Release SME | package integrity, contradictions, stale nodes, release evidence | final release blocker |

## Dynamic specialists
Finance/Commercial, Legal, Cyber, Data/AI, Architecture, Change, Experience/Service Design, sector SMEs and relevant PMs join only when the active RFP creates a material decision in their domain.

## Quorum
- **Skill/architecture release:** Skill Architect + Proposal Director + QA are mandatory; Partner required for material policy/commitment changes; Artifact SME and Theme & Color Governor required for visual/brand changes.
- **RFP Summary approval:** Proposal Director + Senior PM + QA mandatory; Partner for material bid/commercial exposure; Operations when launch/support is in scope; Artifact SME + Theme & Color Governor before visual release.
- **Proposal section approval:** section owner + Proposal Director + applicable SME + QA.
- **Final submission release:** Partner/authorized approver + Proposal Director + QA + Production SME; no critical applicable role may remain `BLOCKED` or `REVIEW_REQUIRED`.

## Operational record required for every material finding
`finding_id | role | affected node | severity | evidence | decision | owner | due_gate | status | closure_evidence | approver`.

## SLA principle
Do not invent generic clock-hour SLAs. Due dates are derived from the Bid Calendar and the submission deadline. Critical findings inherit the nearest freeze/gate and must close before it.

## Escalation
A missed critical gate escalates one level: workstream owner → Proposal Director → Partner/authorized bid owner. Release cannot bypass an unresolved critical finding by cosmetic approval.
