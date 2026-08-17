# V7 — RFP Summary Canonical Decision Architecture

**STATUS: CURRENT V7 PRODUCT AUTHORITY**  
**INHERITS:** `01_ACTIVE_RUNTIME/22_RFP_SUMMARY_FINAL_PRODUCT_CONTRACT.md` and `01_ACTIVE_RUNTIME/40_RFP_SUMMARY_24_ROLE_DEPTH_CONTRACTS.md`.  
**DOES NOT REDESIGN THE APPROVED PRODUCT.** It locks order, naming, language, decision purpose, and management/evaluator questions.

## 1. Product purpose
`RFP Summary` remains the internal pursuit/decision brief. Its job is not to summarize documents; it must let GM/CEO/Partners understand the opportunity, decide whether to bid, identify what is required to win, and know what must be resolved before commitment.

## 2. Canonical role count and order
- Exactly **24 logical roles** in the canonical storyline.
- Logical role count is stable; physical page count is dynamic.
- Do not add, remove, rename, or reorder a visible role because a model prefers a different consulting label. **Do not invent or cosmetically rename canonical RFP Summary sections.**
- A role may expand to multiple pages when evidence or relationships require it.
- Any omission follows the existing product contract; mandatory management roles remain present.
- Canonical machine IDs, visible labels and legacy aliases are owned by `rfp_summary_role_registry_v7.json`.

## 3. Six navigation chapters — not extra roles
1. فهم الفرصة وقرار الإدارة المبكر / Opportunity Understanding & Early Management Decision — roles 01–05
2. ما الذي يطلبه العميل فعلًا؟ / What the Client Actually Requires — roles 06–10
3. حجم الالتزام والتنفيذ / Commitment & Delivery Scale — roles 11–13
4. كيف نفوز؟ / How We Win — roles 14–16
5. استراتيجية التقديم والتنفيذ / Proposal & Delivery Strategy — roles 17–19
6. المخاطر والقرار / Risks & Decision — roles 20–24

These are TOC/navigation groupings only. They do not create six mandatory divider slides.

## 4. Role decision contract
Before producing any analytical role, compile:
`Management Question → Evaluator/Assurance Question → Decision Supported → Evidence → Thesis → Counter-evidence → Semantic Relationships → Artifact Intent → Management Implication`.

Existing depth contracts remain mandatory. V7.0.2 keeps `Required Analysis` and `Evidence` explicit for all 24 roles in both the role-depth authority and canonical registry. V7 adds the management/evaluator questions and decision relevance; it does not weaken mandatory content.

## 5. Naming authority
Visible titles use the canonical role registry as a safe default and may adapt to the RFP topic when the management question becomes clearer. Generate from `Canonical Role + RFP Topic + Management Question + Primary Executive Audience`, then pass the Executive Naming Council. Internal engine names such as `BOQ_INTELLIGENCE`, `WIN_STRATEGY`, `Artifact Intelligence`, `Council`, or English role IDs never leak into an Arabic product. Execute `75_V7_0_2_OWNER_ARABIC_EXECUTIVE_TERMINOLOGY_AND_NAMING_LAW.md` for the owner language lock.

## 6. Management decision role
The final decision must synthesize at minimum when evidenced/material:
- opportunity attractiveness;
- strategic fit;
- win potential / evaluation position;
- delivery confidence;
- team readiness;
- qualification/evidence readiness;
- commercial/pricing confidence;
- schedule pressure;
- critical dependencies and information gaps;
- top material risks;
- required executive actions and conditions.

The decision is evidence-backed and must validate against `schemas/rfp_bid_decision_evidence_v7.schema.json`: `GO | GO_WITH_CONDITIONS | HOLD | NO_GO_RECOMMENDATION | INSUFFICIENT_INFORMATION`. A model preference or automatic weighted formula is never a sufficient reason.

## 7. RFP authorship / procurement maturity
Role 23 is intentionally retained. It must help management understand whether the package appears to be:
- a limited/single internal-author effort;
- an internal multi-function effort;
- specialist external advisory-led;
- hybrid internal/external or compiled/legacy;
- insufficient evidence to infer.

This is an evidence-based fingerprint with confidence and counter-evidence. Never name a consulting company/person as author unless the source explicitly proves it. The purpose is to infer likely ambiguity, decision authority, clarification need, evaluation sophistication and commercial protection — not to criticize the client.

## 8. Failure conditions
Hard fail when the Summary becomes a document checklist, uses invented section names, mixes Arabic/English decoratively, hides material gaps, repeats source text without interpretation, or produces a GO/NO-GO recommendation without evidence and conditions.

## 9. Current workflow
Execute `05_WORKFLOW_ENGINE/23_V7_RFP_SUMMARY_DECISION_WORKFLOW.md`. Legacy `17_A_TO_Z_RFP_SUMMARY_PRODUCTION_FLOW.md` is lineage only and cannot own current concept counts or release routing.


## 10. Machine execution evidence — no silent step skipping
Every RFP Summary run must persist and validate a machine execution state against `schemas/rfp_summary_execution_state_v7.schema.json`. Ingestion must persist `schemas/rfp_ingestion_state_v7.schema.json`. The canonical executable validator is `Rashad/Brain/runtime/rfp_summary_runtime.py`.

Each of the 15 workflow steps produces `PASS`, `BLOCKED`, or `NOT_EXECUTED` evidence. A downstream step may not be treated as executed when an upstream required step is not `PASS`. Missing provider, render, independent judge, detector, parity, or release evidence is `NOT_EXECUTED`/`BLOCKED`, never inferred from prose quality.

The machine state must include the persisted pack mode, all mandatory ingestion registers, derived `ClarificationWindowState`, 24-role depth plan, role outputs, cognitive packets, Council sessions, Page Content Packs, semantic graphs, five-hypothesis visual-search evidence for critical pages, actual render hashes, independent judgments, QA/stress evidence, schema-valid Role-24 decision object, and final release evidence.
