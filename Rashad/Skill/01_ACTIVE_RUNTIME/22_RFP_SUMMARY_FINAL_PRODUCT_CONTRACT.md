# RFP Summary vNext — Canonical Product Contract

STATUS: CURRENT AUTHORITATIVE — USER-APPROVED 2026-08-11
SUPERSEDES: fixed-count Summary architectures; generic RFP checklist summaries; the rule that Source Coverage can never be visible in an internal pursuit brief.

## 1. Two separate products

Rashad must never blur these two products.

### A. `INTERNAL_PURSUIT_BRIEF` — default when the user asks for “RFP Summary”
A senior bid, commercial, delivery, launch, and decision brief used by Rubix internally before proposal production. **Default delivery mode is ARTIFACT, not text.** Content-only delivery is an explicit user exception governed by `34_PRODUCT_ROUTER_AND_REGISTRY.md`.

It may contain: evidence gaps, cross-document conflicts, bid strategy, commercial commitments and risks, proposal-preparation planning, delivery planning, risks, clarifications, assumptions, procurement maturity, and bid decision.

### B. `CLIENT_FACING_RFP_UNDERSTANDING` — only when explicitly requested
A sanitized client-facing statement of understanding. It must not expose internal win strategy, margin/commercial commitments and risks, procurement-maturity criticism, internal bid decision, source-control mechanics, red-team findings, or internal council debate.

## 2. Dynamic, not fixed

The architecture below defines **logical page roles**, not a fixed slide count. One logical role may expand into multiple continuation pages. A role may be omitted only when it is genuinely unsupported/non-material, except Cover, Competition Narrative, TOC, and final decision/action framing which remain required for the internal product.

Do not compress 20 deliverables, 20 roles, 40 risks, or 50 questions into one page. Expand while preserving information hierarchy.

For Arabic engagements, canonical role names above are **internal IDs only**. Visible titles/subtitles/labels must use the Arabic mapping in `33_ARABIC_VISIBLE_LANGUAGE_PURITY_GATE.md`. English structural labels in an Arabic Summary are a blocking release defect.

## 3. Canonical INTERNAL_PURSUIT_BRIEF storyline

The following is the Arabic visible storyline for an Arabic engagement. The code token in parentheses is an **internal role ID only** and must never replace the Arabic visible title.

1. **الغلاف** (`COVER`)
2. **ماذا تشتري الجهة فعليًا؟** (`COMPETITION_NARRATIVE`)
3. **خريطة الملخص التنفيذي** (`TABLE_OF_CONTENTS`)
4. **صورة الفرصة في دقيقة واحدة** (`OPPORTUNITY_SNAPSHOT`)
5. **الجدول الزمني وضغط التقديم** (`KEY_DATES`)
6. **اكتمال مستندات المنافسة وما يحتاج إلى حسم** (`SOURCE_COVERAGE`)
7. **أهداف المشروع والنتائج التي تتوقعها الجهة** (`CLIENT_NEED`)
8. **القراءة الاستراتيجية للفرصة** (`STRATEGIC_READING`)
9. **نطاق المشروع ومجالات العمل** (`SCOPE_ARCHITECTURE`)
10. **كيف سينتقل المشروع من التأسيس إلى التشغيل؟** (`DELIVERY_JOURNEY`)
11. **المخرجات والكميات: ما الذي سنلتزم بتسليمه فعليًا؟** (`BOQ_INTELLIGENCE`)
12. **متطلبات الحل التقني والبيانات والتكامل** (`TECHNICAL_REQUIREMENTS`)
13. **القدرات المطلوبة لتنفيذ المشروع** (`TEAM_CAPACITY`)
14. **كيف سيُقيَّم العرض وما الذي يصنع التفوق؟** (`EVALUATION_WIN`)
15. **جاهزية التأهيل والأدلة الداعمة** (`QUALIFICATION_READINESS`)
16. **الالتزامات والمخاطر التجارية والمالية** (`COMMERCIAL_EXPOSURE`)
17. **استراتيجية الاستجابة للمنافسة** (`PROPOSAL_STRATEGY`)
18. **خطة إعداد العرض حتى التقديم** (`PROPOSAL_GANTT`)
19. **تصور تنفيذ المشروع بعد الترسية** (`CONTRACT_GANTT`)
20. **ما الذي قد يهدد الفوز أو التنفيذ؟** (`RISKS`)
21. **الاستفسارات التي يجب حسمها قبل التقديم** (`CLARIFICATIONS`)
22. **الافتراضات والفجوات المؤثرة على القرار** (`ASSUMPTIONS_GAPS`)
23. **ماذا تكشف طريقة إعداد المنافسة عن عملية الشراء؟** (`AUTHORSHIP_MATURITY`)
24. **قرار الدخول وشروط النجاح** (`BID_DECISION`)

For non-Arabic engagements, visible labels localize to the engagement language. Internal role IDs remain invisible in final output.

### Internal contract-label law
All subsequent `##` role-contract headings in this authority are **INTERNAL DESCRIPTIVE LABELS ONLY**. They are never approved visible titles. Final visible titles must come from `rfp_summary_role_registry_v7.json` + the v7.0.2 Executive Naming authority and may be topic-adaptive. If an internal English/legacy label differs from the current visible mapping, the visible mapping wins.

### Arabic executive naming rule — v7.0.2
For Arabic executive output, role names are safe defaults, not mechanical labels. Generate the final visible title from `Canonical Role + RFP Topic + Management Question + Primary Executive Audience`, then apply the Executive Naming Council. The Arabic prohibited exposure jargon must never appear in visible titles, subsection headings, callouts, management questions, decision labels, or artifact labels unless an engagement-specific owner exception is explicitly recorded. Role 16 defaults to **الالتزامات والمخاطر التجارية والمالية**. Profitability/cash-flow wording requires evidence support.


## 4. Page contract

Every analytical page must follow:

`Management/Evaluator Question → Thesis → Evidence → Consulting Interpretation → Information Relationship → Artifact Intent → Implication → Decision/Action`

A page that only repeats the RFP fails.

## 5. COVER — internal role contract

The first page **always uses a newly generated hero image tailored to the current competition**, unless the user explicitly overrides this rule. The hero is an asset sub-step and can never satisfy product completion.

Production method:

`RFP scope → Artifact Intent → hero brief → generated strictly text-free hero asset → Geometry Handoff → deterministic crop/mask/composition → native editable title/logos/date/reference → QA → release`

For Arabic Summaries, apply `39_ARABIC_COVER_COMPOSITION_AUTHORITY.md`: image left; native identity/text zone right, unless the user explicitly overrides.

Hard prohibitions:
- no generated Rubix logo;
- no generated client logo;
- no baked-in Arabic/English title inside the generated image;
- no baked-in numbers/dates/references;
- no full-slide screenshot masquerading as an editable cover;
- no black or near-black canvas.

If image generation is unavailable and the user has not explicitly waived the rule: `BLOCKED — COVER HERO IMAGE REQUIRED`.

## 6. OPPORTUNITY_SNAPSHOT — internal role contract

Use only decision-relevant facts: client, competition, duration, submission deadline, language, major scope/workstreams, key deliverable/team/evaluation facts. Currency is not a decorative standalone metadata tile; show financial values only where materially supported.

## 7. SOURCE_COVERAGE — internal role contract

Show `Received → Covered → Missing → Conflicting → Bid/Delivery Impact`.

Do not expose raw file inventories or internal evidence IDs. This role is visible in `INTERNAL_PURSUIT_BRIEF` because it directly affects estimation and bid decisions. It is hidden in the client-facing product.

## 8. CLIENT_NEED / STRATEGIC_READING — internal distinction contract

- **Client Need, Objectives & Success Outcomes** = what the client is trying to achieve.
- **Strategic Reading** = what Rubix concludes this means for the engagement, complexity, success conditions, evaluator expectations, and solution posture.

Do not duplicate the same content across both.

## 9. SCOPE_ARCHITECTURE — internal role contract

Convert scope paragraphs into a coherent workstream/capability system. For each material workstream show purpose, activities, outputs, dependencies, client counterpart, and required disciplines where supportable.

## 10. DELIVERY_JOURNEY — internal role contract

Show phases, parallel tracks, dependencies, client inputs, approvals, gates, and critical path. Do not force a generic Mobilize/Discover/Design/Build sequence when the RFP specifies another model.

## 11. BOQ_INTELLIGENCE — internal role contract

Every material BOQ/deliverable item must be explained, not repeated. Capture:
- exact RFP wording;
- plain-language meaning;
- expected components;
- effort/cost drivers;
- acceptance evidence;
- delivery phase;
- dependencies;
- owner/discipline;
- pricing sensitivity: Low / Medium / High;
- clarification required;
- confidence / source status.

Separate `RFP REQUIREMENT` from `RASHAD INTERPRETATION`, `PROPOSED ACCEPTANCE INTERPRETATION`, and `MISSING INFORMATION`.

## 12. TECHNICAL_REQUIREMENTS — internal role contract

Only when applicable. Cover architecture, platforms, integrations, APIs, data, migration, hosting/cloud, cybersecurity, privacy, environments, licences, NFRs, support and technical acceptance — always tied to solution/effort/price/launch implications.

## 13. TEAM_CAPACITY — internal role contract

First show actual RFP roles and quantities, including minimum experience years. If experience is not specified, state `RFP minimum experience: Not specified`.

Then, when necessary, show `COUNCIL RECOMMENDATION — NOT AN RFP REQUIREMENT` with recommended roles, quantity, experience, rationale, phase involvement, and full/part-time assumption.

## 14. EVALUATION_WIN — internal role contract

Translate scoring into `Criterion → Weight/Gate → What evaluator must believe → Proposal response → Evidence required → Build priority`.

Do not merely reproduce the scoring table.

## 15. QUALIFICATION_READINESS — internal role contract

Unify corporate documents, team evidence/CVs, references/case studies, forms and missing proof into one readiness view. Binary appendix evidence is external runtime input; presence in an index is not proof of validity or availability.

## 16. COMMERCIAL_EXPOSURE — internal role contract

Do not invent a price. Explain what the commercial team must understand before pricing: pricing basis, BOQ structure, payment triggers, resource load, third-party costs, licences/infrastructure, support obligations, volumes, acceptance/payment dependencies, cash-flow and margin risks.

## 17. PROPOSAL_STRATEGY — internal role contract

Turn the Summary into a production brief: hero sections, evidence-heavy sections, required artifacts, SME inputs, commercial dependencies, hard-to-win criteria, and sections needing Partner/Director intervention.

## 18. PROPOSAL_GANTT — internal role contract

Back-plan from submission. Include RFP intelligence, clarifications, bid strategy, technical content, team/CVs, evidence, commercial, compliance, legal/security where relevant, council review, red team, artifact/design, Arabic editorial, production, approval and upload buffer.

## 19. CONTRACT_GANTT — internal role contract

High-level award-to-delivery roadmap including mobilization, delivery phases, acceptance, launch/cutover, transition/handover, hypercare/support/operations where relevant. Do not merge the proposal-preparation timeline with the contract-delivery timeline.

## 20. RISKS — internal role contract

Use Partner, Director, Senior PM/Team Manager, relevant PM(s), and Operations/Launch reasoning. A risk must materially affect technical solution, effort/price/margin, staffing, schedule/critical path, acceptance, launch, operations/support, responsibility split, or contractual delivery risk/commitment.

Internal form: `Cause/Trigger → Event → Impact → Proposal Treatment`.

Publish only material risks. Do not restate tender clauses as risks.

## 21. CLARIFICATIONS — internal role contract

Council: Partner → Director → Senior PM as chair → relevant Project Managers → Associate/Analyst → Operations when relevant → specialist SMEs conditionally.

Admission test:
`NOT_ALREADY_ANSWERED + NOT_PLATFORM_OBVIOUS + SCOPE_SPECIFIC + MATERIAL + ACTIONABLE`.

Mandatory question:
**If the client answers A instead of B, what changes in our proposal?**

If nothing material changes in scope, solution, effort, price, team, schedule, acceptance, launch, operations, responsibility split, assumption or qualification: delete the question.

## 22. ASSUMPTIONS_GAPS — internal role contract

Do not merge assumptions into clarifications. Capture assumption, reason, affected proposal components, commercial impact, validation owner, and whether it should become a client clarification.

## 23. AUTHORSHIP_MATURITY — internal role contract

Execute `32_RFP_AUTHORSHIP_AND_PROCUREMENT_MATURITY.md`.

The internal brief must go beyond a generic maturity score. It must state the **likely authoring/assembly model** (`SINGLE_CLIENT_OWNER`, `INTERNAL_MULTI_FUNCTION_TEAM`, `EXTERNAL_ADVISORY_LED`, `HYBRID_COMPILED_PACKAGE`, or `INSUFFICIENT_EVIDENCE`), provide an **authorship confidence score**, show evidence for and against the inference, score the defined procurement-maturity dimensions, and explain the implication for proposal construction, pricing protection and clarifications.

Never state that a named consulting company/person wrote the RFP unless the source explicitly proves it. Authorship is an evidence-based fingerprint, not an accusation.

## 24. BID_DECISION — internal role contract

Evidence-based result: `GO | GO_WITH_CONDITIONS | HOLD | NO_GO_RECOMMENDATION | INSUFFICIENT_INFORMATION`.

Validate the decision object against `schemas/rfp_bid_decision_evidence_v7.schema.json`. Show attractiveness, strategic fit, win potential, delivery confidence, team/evidence readiness, commercial/pricing confidence, schedule pressure, procurement maturity, critical conditions, management actions and next gate. The recommendation is a Council synthesis; no fixed weighted formula may auto-decide the bid.

## Client-facing derivative — separate product, not a logical RFP Summary role

The client-facing derivative may use only externally appropriate roles from the internal brief, typically: Cover, Competition Narrative, Opportunity Snapshot, Client Need/Objectives, Scope Architecture, Delivery Journey, Deliverable Understanding, Team/Delivery model where appropriate, and a close/next-step page.

Never expose internal source gaps, bid strategy, commercial margin exposure, maturity criticism, internal risk debate or bid decision without explicit instruction.

## v2.3 Artifact Intelligence application to the RFP Summary
Every visible analytical page in `INTERNAL_PURSUIT_BRIEF` or `CLIENT_FACING_RFP_UNDERSTANDING` must pass the v2.3 chain:
`Question → Thesis → Evidence → Relationship → Artifact Intent → Archetype/Family → Visual Blueprint → Geometry Handoff → Firewall → Composer → QA`.

The cover is the only non-analytical page role: its engagement-specific generated hero remains a `PRODUCTION_VISUAL_INGREDIENT`, never a generated production slide. Native exact logos, Arabic text, Arabic-Indic numerals, dates, and references are composed separately.

## v2.5 product completion lock
This product is governed by `34_PRODUCT_ROUTER_AND_REGISTRY.md`, `35_PRODUCT_DELIVERY_AND_COMPLETION_CONTRACT.md`, `36_CAPABILITY_PREFLIGHT_AND_TOOL_ROUTING.md`, `37_ARTIFACT_PRODUCTION_ORCHESTRATOR.md`, and `38_RELEASE_COMPLETION_GATE.md`.

`RFP Summary` means the full `INTERNAL_PURSUIT_BRIEF` artifact by default. A content draft, an Artifact Intent set, a Visual Blueprint set, or a generated cover hero alone is an **incomplete intermediate state**.

## v2.6.2 execution proof overlay
Before release, apply `00_CHAT_MIRROR_KERNEL/15_COVER_ART_DIRECTOR.md` and `03_ARTIFACT_ENGINE/43_ARTIFACT_EXECUTION_PROOF_AND_NO_DOWNGRADE_GATE.md`. The existence of Artifact Intelligence rules is not evidence that a page used them. Release requires execution trace plus rendered-page preservation.

## v2.6.3 co-brand release lock
Every branded RFP Summary page, including the cover, must execute `00_CHAT_MIRROR_KERNEL/16_COBRAND_LOGO_DIRECTOR.md`.

Required physical signature: `Rubix | Client` on the left; Rubix far-left, client to the right, same visible/optical height, both verified transparent-background PNGs. Arabic RTL must never reverse this order. Missing or unverifiable client-logo transparency/provenance blocks final branded release; no generated or screenshot fallback is permitted.

## v2.6.4 Understanding Depth overlay
The 24 role architecture remains canonical. Execute `40_RFP_SUMMARY_24_ROLE_DEPTH_CONTRACTS.md` for every applicable role. Role count is stable; physical page count is dynamic. BOQ, Team, Technical Requirements, Evaluation, Qualification, Commercial Exposure, Risks, and Clarifications may expand to multiple pages when required. One-page compression is not a virtue and cannot override evidence depth or artifact strength.

For any multi-page role, execute the Section Golden Board workflow before native composition and preserve the approved visual target through HTML/PDF/PPTX projection.


## v7.0 canonical decision and language overlay
The approved 24-role architecture/order remains unchanged. Execute `69_V7_RFP_SUMMARY_CANONICAL_DECISION_ARCHITECTURE.md`, `70_V7_MONOLINGUAL_OUTPUT_AND_NAMING_AUTHORITY.md`, and `rfp_summary_role_registry_v7.json`. These authorities lock canonical visible names, monolingual output, decision questions, legacy internal-ID aliases, and role 23 authorship fingerprint; they do not add or remove roles.
