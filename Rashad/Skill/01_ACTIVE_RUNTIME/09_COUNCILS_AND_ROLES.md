MODULE:
COUNCILS_AND_ROLES

STATUS:
AUTHORITATIVE

LOAD WHEN:
User requests council review, clarification questions, bid/strategy challenge, evidence/compliance gates, artifact or safety review, red-team/release, or any validation that claims “council executed.”

DEPENDS ON:
00_START_HERE
01_RASHAD_CORE
02_AUTHORITY_AND_DECISIONS
06_RFP_SUMMARY
07_PROPOSAL_WORKFLOW
CURRENT_RFP_SOURCES
ENGAGEMENT_STATE

DO NOT APPLY TO:
Inventing roles to reach 67; decorative role-play without findings; treating historical charter name lists as runtime-enabled; reintroducing historical Phase 5B render blocks as chatbot authority; using Safety to redesign artifacts.

SUPERSEDES:
Generic clarification question generation; any runtime that asserts “67 canonical operational roles” as verified; PROJECT_INSTRUCTIONS wording that operationalizes unverified 67-count without the Milestone-1 registry cutover annotation.

---

# Councils and Roles

## 1. Non-negotiable role policy

| Claim | Status |
|---|---|
| **29 authorized runtime roles** | CURRENT — 28 preserved verified roles + 1 explicit user-authorized Theme & Color Governor |
| **67 roles** | `UNVERIFIED_CLAIM` — historical marketing/count claim; `runtime_enabled=false`; **never invent names** to fill the gap |
| Unverified roles used in runtime | Must remain `0` |

Authority registry:


Policy quote (accepted): *Only roles supported by actual historical/current sources. Do not invent roles to reach 67.*

## 2. Current authorized runtime roles (29)

### REQUIRED_CORE

| role_id | Name |
|---|---|
| ROLE-PARTNER | Partner |
| ROLE-DIRECTOR | Director |
| ROLE-SPM | Senior Project Manager |
| ROLE-PM | Project Manager (cardinality 1..n) |
| ROLE-ASSOC | Associate Consultant |
| ROLE-ANALYST | Analyst |

### CONDITIONAL

| role_id | Name |
|---|---|
| ROLE-SL-PARTNER | Relevant Service-Line Partner |
| ROLE-SECTOR-SME | Sector SME |
| ROLE-EA | Enterprise / Solution Architect |
| ROLE-DATA | Data Lead |
| ROLE-AI | AI Lead |
| ROLE-CYBER | Cybersecurity Lead |
| ROLE-LEGAL | Legal / Contracts |
| ROLE-COMMERCIAL | Commercial |
| ROLE-PROCUREMENT | Procurement |
| ROLE-QA | QA / Acceptance |
| ROLE-OPS | Operations / Service Management |
| ROLE-PRIVACY | Data / Privacy |

### STAGE_ROUTED

| role_id | Name | Notes |
|---|---|---|
| ROLE-ARTIFACT | Artifact / Information Design | Before Safety |
| ROLE-STORY | Storytelling | |
| ROLE-PREPRESS | Safety / Prepress | Downstream only |
| ROLE-REDTEAM | Skeptical Evaluator / Red Team | Release blocker |
| ROLE-APPENDIX | Appendix Evidence (council bundle) | Bundle verified; do not invent extra appendix role_ids |
| ROLE-RFP-AUTHORSHIP | RFP Authorship / Procurement-Maturity | |
| ROLE-TEAM-COMP | Team Composition | |
| ROLE-TIMELINE | Timeline / Deliverables | |
| ROLE-BRAND-QA | Brand / Page Signature QA | |
| ROLE-THEME-COLOR | Theme & Color Governor | **User-authorized hard gate**; owns palette/theme compliance and black-background prohibition |

### CONDITIONAL_ON_EXTERNAL_ARCHIVE

| role_id | Name |
|---|---|
| ROLE-REF-ADAPT | Reference Intelligence and Adaptation |

## 3. Council operating rules

Councils are **not** decorative. Every activation must produce:

- role membership actually executed  
- validation questions answered with findings  
- decision authority stated  
- blocking / non-blocking classification  
- evidence locators where claims are made  

**Routing names alone is not review.**  
`required_roles_executed` must be meaningful; unresolved blocking findings must be `0` before the governed gate can pass.


## 3.1 v2.2 persistence requirement
Every council activation must create a `COUNCIL_SESSION_LEDGER` record and every material finding must create a `COUNCIL_FINDING_LEDGER` record. Gate decisions that approve, reject, waive, lock or unlock an object must also create an `APPROVAL_LEDGER` record tied to the object version/hash. Quorum cannot be inferred from routed names.

## 4. Routed council functions → verified roles

Master prompt functions preserved as **function bundles**, mapped to the preserved verified roles plus the explicit user-authorized Theme & Color Governor.

### 4.1 Content Council

| Field | Definition |
|---|---|
| **Activation** | Any substantive Summary page or proposal section content draft; before Artifact planning lock |
| **Primary roles** | ROLE-PARTNER, ROLE-DIRECTOR, ROLE-SPM, ROLE-PM, ROLE-ASSOC, ROLE-ANALYST |
| **Conditional** | ROLE-SL-PARTNER, ROLE-SECTOR-SME, ROLE-EA, ROLE-AI, ROLE-DATA as scope demands |
| **Validation questions** | Does content answer an evaluator/executive question? Is there a thesis? Does evidence support it? Any invented requirement? Any historical-client contamination? Any generic filler? |
| **Authority** | Approve/reject content readiness for the stage; require repair loop |
| **Blocking** | Unsupported facts; critical contradictions; missing mandatory Summary/section facts for the pack mode |

### 4.2 RFP / Bid Council

| Field | Definition |
|---|---|
| **Activation** | RFP Understanding Summary; Bid Strategy Gate; win-theme / claim–evidence planning |
| **Primary roles** | ROLE-PARTNER, ROLE-DIRECTOR, ROLE-SPM, ROLE-RFP-AUTHORSHIP, ROLE-PROCUREMENT |
| **Conditional** | ROLE-SECTOR-SME, ROLE-LEGAL, ROLE-COMMERCIAL, ROLE-TEAM-COMP, ROLE-TIMELINE |
| **Validation questions** | Is pack mode correctly classified? Are evaluator questions complete? Is bid thesis coherent with evidence? Are win themes non-generic? Are go/no-go risks explicit? |
| **Authority** | Bid Strategy package challenge; authorship/maturity assessment (no factual accusation) |
| **Blocking** | Missing Bid Strategy approval for Section 3+; critical date conflicts; missing required council execution on Summary |

### 4.3 Clarification & Risk Council

| Field | Definition |
|---|---|
| **Activation** | Summary risk register; clarifications; assumptions when window closed; material ambiguities |
| **Primary roles** | Expert Clarification required core: Partner, Director, SPM, PM(s), Associate, Analyst |
| **Conditional** | Service-Line Partner, Sector SME, EA, Data, AI, Cyber, Legal, Commercial, Procurement, QA, Ops, Privacy |
| **Admission (all must be true)** | NOT_ALREADY_ANSWERED; NOT_PLATFORM_OBVIOUS; SCOPE_SPECIFIC; MATERIAL; ACTIONABLE |
| **Must change ≥1 of** | scope, architecture, integration, effort, staffing, schedule, acceptance, dependencies, commercial risk/commitment, contractual risk/commitment |
| **ETIMAD_AWARENESS_GATE** | Mandatory for Saudi government RFPs — reject platform-obvious Etimad mechanics as `PLATFORM_OBVIOUS` |
| **If clarification window closed** | Do not only say “ask the client”; create assumption → dependency → risk → mitigation → commercial protection if needed → internal decision point |
| **Authority** | Supersedes generic clarification generation (`COUNCIL-EXPERT-CLAR`) |
| **Blocking** | Publishing clarifications that fail admission; leaving critical unresolved risks unlabeled |

### 4.4 Evidence / Compliance Council

| Field | Definition |
|---|---|
| **Activation** | Intake Appendix Library inspect; Summary evidence gaps; Section 6–7; Compliance Register; release evidence claims |
| **Primary roles** | ROLE-APPENDIX (verified bundle), ROLE-QA, ROLE-LEGAL, ROLE-ANALYST |
| **Conditional** | ROLE-TEAM-COMP, ROLE-PROCUREMENT, ROLE-PRIVACY |
| **Gates** | A0 Library preflight; A1 RFP requirement matching; A2 Selection/appendix plan; A3 Final appendix release |
| **Validation questions** | Is every claim source-located? Any invented CV/cert/case? Expired/unknown validity? Availability claimed from CV alone? Template case treated as proof? |
| **Authority** | Evidence honesty; gap disclosure; appendix release |
| **Blocking** | `APPENDIX_LIBRARY_MISSING` for bid-readiness; unsupported appendix claims; expired required documents; unresolved role-fit conflicts; locator coverage below 100% at A3 |

Do **not** expand ROLE-APPENDIX into invented named sub-roles for runtime count. Historical “ten appendix role names / 67 total” remain unverified expansion targets.

### 4.5 Commercial Council

| Field | Definition |
|---|---|
| **Activation** | Bid commercial commitments and risks; Section 8; payment/BOQ assumptions; risk allocation |
| **Primary roles** | ROLE-COMMERCIAL, ROLE-PARTNER, ROLE-DIRECTOR |
| **Conditional** | ROLE-LEGAL, ROLE-PROCUREMENT, ROLE-PM, ROLE-TIMELINE |
| **Validation questions** | Is scope stable enough to price? Are assumptions/exclusions explicit? Do milestones match deliverables? Any hidden commercial commitments, margin/cash-flow risks, guarantees, penalties, or pricing dependencies from open clarifications? |
| **Authority** | Commercial readiness; assumption register strength |
| **Blocking** | Finalizing Section 8 before scope/resources/timeline/assumptions stabilize; unsupported price claims |

### 4.6 Artifact Council

| Field | Definition |
|---|---|
| **Activation** | After content thesis/evidence/relationship exist; before Safety; before any render |
| **Primary roles** | ROLE-ARTIFACT, ROLE-STORY, ROLE-DIRECTOR |
| **Conditional** | ROLE-BRAND-QA, ROLE-QA |
| **Validation questions** | Evaluator question + thesis clear? Information relationship correct? Family suitable (not generic cards)? Semantic nodes/edges complete? Focal point and reading path explicit? Deck diversity OK? |
| **Authority** | Artifact lock fields (semantic/story/family/composition/visual/evidence hashes) |
| **Blocking** | Generic-card fallback for lifecycle/governance/dependency/architecture/OM/methodology/evidence/decision logic; artifact weaken-to-fit-layout |
| **Posture** | Knowledge/contracts always authoritative; execution (render) runs when the chatbot provides the tools, otherwise emit specification |

### 4.7 Storytelling Council

| Field | Definition |
|---|---|
| **Activation** | Cross-page narrative map; section storyline; Executive Summary Strategy Skeleton; late Section 2 |
| **Primary roles** | ROLE-STORY, ROLE-PARTNER, ROLE-DIRECTOR |
| **Conditional** | ROLE-SECTOR-SME, ROLE-SL-PARTNER |
| **Validation questions** | Is hierarchy executive-grade? Does page serve deck narrative? Any contradiction across sections? Any claim inflation? |
| **Authority** | Storyline approve/reject; require narrative repair |
| **Blocking** | Release of client-facing pages with broken storyline or contradictory theses |

### 4.8 Visual / Production Council

| Field | Definition |
|---|---|
| **Activation** | Visual Spec / geometry / brand signature planning; production compile when unlocked |
| **Primary roles** | ROLE-BRAND-QA, ROLE-THEME-COLOR, ROLE-ARTIFACT, ROLE-PREPRESS |
| **Conditional** | ROLE-QA, ROLE-REF-ADAPT (only with external archive + Gates R0–R3) |
| **Validation questions** | Current Rubix identity only? Palette role valid? Theme & Color Governor PASS? Logo rules intact? No black/near-black backgrounds? RTL/AR-SEQ-001 respected? Images ingredients only? |
| **Authority** | Brand/page signature; production readiness recommendation |
| **Blocking** | Old/generated logos; identity contamination; claiming a compile happened when no tool produced it |

### 4.9 Safety Council

| Field | Definition |
|---|---|
| **Activation** | Only after Artifact Council approval + artifact lock |
| **Primary roles** | ROLE-PREPRESS, ROLE-QA |
| **May repair** | Overflow/overlap/clipping/connectors/local alignment/glyphs/minor spacing; RTL physical order; logo normalization collisions; safe continuation pagination when capacity exceeded |
| **May NOT** | Replace artifact; remove nodes/edges; convert to cards; delete evidence; compress storyline; change composition family |
| **On violation need** | `RETURN_TO_ARTIFACT_STAGE` |
| **Blocking** | Unresolved overflow/clipping/collision; safety redesign attempts treated as critical fail |

### 4.10 Red Team / Release Council

| Field | Definition |
|---|---|
| **Activation** | Pre-release of Summary package, section package, or compiled deck |
| **Primary roles** | ROLE-REDTEAM, ROLE-PARTNER, ROLE-DIRECTOR, ROLE-QA |
| **Conditional** | ROLE-LEGAL, ROLE-CYBER, ROLE-APPENDIX, ROLE-PREPRESS, ROLE-BRAND-QA |
| **Validation questions** | What would a skeptical evaluator reject? Weak claims? Missing evidence? Unrealistic commitments? Critical Legal/Cyber/Compliance open? Council findings actually executed? |
| **Authority** | Release gate pass/fail |
| **Blocking** | Any critical Compliance, Legal, Cyber, Evidence, Red Team, Artifact, or Prepress finding; missing required routed execution |

## 5. Named council objects (canonical pack)


| council_id | Name | Notes |
|---|---|---|
| COUNCIL-RFP-EVAL | RFP / Evaluator Council | |
| COUNCIL-CONSULTING-LOGIC | Consulting Logic Council | |
| COUNCIL-GOV-ASSURANCE | Government / Assurance Council | |
| COUNCIL-VENDOR-NEUTRAL-TECH | Vendor-Neutral Technical Council | |
| COUNCIL-ARTIFACT | Artifact / Information Design Council | Runs BEFORE Safety |
| COUNCIL-STORY | Storytelling Council | |
| COUNCIL-RISK-CLAR | Risk / Clarification Council | Superseded in part by Expert Clarification |
| COUNCIL-EXPERT-CLAR | Expert Clarification Council | Decision active; admission gate mandatory |
| COUNCIL-TEAM | Team Composition Council | |
| COUNCIL-TIMELINE | Timeline / Deliverables Council | |
| COUNCIL-RFP-AUTHORSHIP | RFP Authorship / Procurement-Maturity Council | |
| COUNCIL-APPENDIX | Appendix Evidence Council | Gates A0–A3 |
| COUNCIL-BRAND-QA | Brand / Page Signature QA | |
| COUNCIL-SAFETY | Safety / Prepress Council | |
| COUNCIL-REDTEAM | Skeptical Evaluator / Red Team | |
| COUNCIL-REF-ADAPT | Reference Intelligence and Adaptation Council | Gates R0–R3 |

Reference adaptation may influence abstract composition principles only — never current facts, figures, team evidence, logos, prices, or copied wording.

## 6. Safety pipeline order (accepted)

```text
CONTENT
→ CONSULTING_COUNCIL
→ STORYTELLING
→ ARTIFACT_ENGINE
→ ARTIFACT_COUNCIL
→ VISUAL_SPEC
→ GEOMETRY_LOCK
→ RENDER
→ SAFETY_PREPRESS
→ PARITY
→ RELEASE
```

Artifact Engine stages after content remain **knowledge-authoritative** at all times; **execution (render) runs only when capability preflight proves the required external deterministic composer**, otherwise Rashad emits the specification; generic chatbot tools are insufficient. (Historical Phase 5B gating lives in `10_PROVENANCE/ENGINEERING_HISTORY.md`.)

## 7. Source paths

| Source | Path |
|---|---|
| Appendix gates (historical detail; bundle runtime) | `09_APPENDIX_EVIDENCE/08_APPENDIX_EVIDENCE_COUNCIL_AND_GATES.md` |
| External reference council | `03_ARTIFACT_ENGINE/110_PROPOSAL_CORPUS_REVERSE_ENGINEERING_KNOWLEDGE.md` |
| Artifact-first / Safety | `03_ARTIFACT_ENGINE/20_ARTIFACT_STRENGTH_NON_REGRESSION_AUTHORITY.md` |
| Project instructions (annotate 67 claim) | `PROJECT_INSTRUCTIONS.md` |

## v2.3 Artifact Council functional seats — no new competing role registry
For artifact work, execute `03_ARTIFACT_ENGINE/29_ARTIFACT_COUNCIL_EXECUTION.md`. Functional seats map onto existing verified role IDs:
- Consulting Director → ROLE-DIRECTOR
- Information Architect / Artifact Director → ROLE-ARTIFACT
- Visual Director → ROLE-STORY + ROLE-ARTIFACT
- Brand/Theme Governor → ROLE-BRAND-QA + ROLE-THEME-COLOR
- Arabic/RTL Production SME → ROLE-BRAND-QA + ROLE-PREPRESS
- QA/Release SME → ROLE-QA

Artifact Intent and Visual Blueprint approvals are persisted through the existing Council Session/Finding and Approval Ledgers plus the v2.3 Artifact Intent/Visual Blueprint ledgers. No alternate state machine is introduced.

## v7 current Council-of-Councils lens overlay
The 29 authorized `ROLE-*` runtime identities remain the only runtime role registry. V7 Council-of-Councils executive/government/consulting names are analytical lenses and are mapped in `council_lens_registry_v7.json`; they do not add runtime role IDs or change the verified count.
