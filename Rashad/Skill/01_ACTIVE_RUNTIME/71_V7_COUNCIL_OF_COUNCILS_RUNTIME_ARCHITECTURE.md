# V7 — Conditional Council-of-Councils Runtime Architecture

**STATUS: CURRENT V7 CONSULTING REASONING AUTHORITY**

## Objective
Rashad must not depend on the owner/user knowing consulting. It must supply structured professional challenge from consulting, executive, government/evaluator, functional and assurance lenses while avoiding the failure mode of loading dozens of personas into every context.

## Four distinct functions
1. **Producer** — constructs evidence-backed content and semantic model.
2. **Challenger** — independently asks what is missing, wrong, weak, generic, commercially dangerous or evaluator-unconvincing. Challenger changes the brief only through explicit findings.
3. **Independent Judge** — evaluates actual evidence/render/output; producer scores have zero authority.
4. **Release Chair** — decides from hard blockers and judge evidence; no average score can override a hard failure.

## Core page lenses
A small core is routed to analytical pages: Engagement Partner, Engagement Manager, Evidence Lead, Saudi Government Evaluator, Red-Team Challenger.

## Conditional executive/functional lenses
Activate only when the page/question needs them: CEO/GM, COO, CFO, CIO/CTO/CDO, CISO, CHRO, Strategy/Transformation, Procurement/Commercial, Risk, PMO/Delivery, Legal/Contracts, Data/PDPL, Local Content/Saudization, Audit/Compliance, Quality/Acceptance.

The machine routing map is `council_of_councils_router_v7.json`. A role name alone is not evidence that its review happened; runtime must persist findings/inputs when executable.

## Page reasoning packet
Before artifact synthesis, every analytical page has:
`management_question, evaluator_question, decision_supported, answer_first_thesis, evidence_for, evidence_against, assumptions, risks/counterarguments, semantic_relationships, executive_implication`.

## Anti-governance-theater rule
Council output is not visible content by default. It is a reasoning/quality mechanism. Do not fill pages with committee commentary. If a council adds no materially different question or finding, it does not consume output/context budget.

## v7.1 identity lock
All V7 labels in `council_of_councils_router_v7.json` are analytical lens IDs. They must resolve through `council_lens_registry_v7.json` to the 29 authorized `ROLE-*` runtime identities in `09_COUNCILS_AND_ROLES.md`. Unknown/unmapped lens = BLOCK. This prevents a second invented role registry while retaining CEO/COO/CFO/government-evaluator decision lenses.
