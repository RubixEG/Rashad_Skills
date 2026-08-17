# Rubix Proposal — Master Skeleton and CRAFT Prompt Library (v2, Rashad-integrated)

**Supersedes v1.** This version integrates the Rashad Consulting Intelligence System (388 prompts, 96 scopes, the 6-phase consulting workflow, CRAFT architecture). Every slide prompt is rewritten in CRAFT format. Scope selection is two-tier. Rashad prompts are referenced by code only (the full Rashad master document must be loaded in the same project chat).

**Relationship between the two documents:**
- **This document** = the visual proposal architecture. 8 sections, the slide library, structural patterns, BCG-grade content rules. Answers: *what slides to make and what they look like.*
- **Rashad master document** = the thinking infrastructure. 96 scope playbooks, 388 engineered prompts, CRAFT structure, the consulting workflow. Answers: *how to think through the content of each slide.*

The integration is a reference layer. Each slide block ends with a `RASHAD INVOCATION` line naming the R-codes to run for that slide. The slide's CRAFT prompt governs the visual deliverable; the invoked R-codes govern the underlying analysis.

**How Claude uses this document with `/rubix-deck`:**
1. Read the scope brief (client, RFP, sector, scope statement, evaluation criteria, budget hint, timeline).
2. Run the **Two-Tier Scope Selector** (Part 0.2): pick the Tier-1 archetype and the Tier-2 Rashad scope code(s).
3. Pull that scope's 6-phase prompt sequence from the Rashad Master Reference Matrix.
4. Walk this skeleton in order. For each slide, execute the CRAFT prompt, invoking the named R-codes to generate the underlying content, then format per the slide's `<output_format>`.
5. Slides marked **[REPEATABLE]** are instantiated N times from scope inputs.

---

## PART 0 — Operating System

### 0.1 Universal output rules (apply to every slide)

- **Tone:** McKinsey/BCG/PwC/EY/Strategy& hybrid. Numbers-first, no filler, no generic phrasing, technically and scientifically oriented.
- **No placeholders.** Every slide produced complete, ready to render. No "[TBD]", no deferred sections.
- **Numbers carry the argument.** Every claim anchored to a figure, source, framework, or named precedent.
- **No em-dashes or en-dashes.** Use "to" for ranges; periods, colons, commas, parentheses for asides.
- **Language:** Arabic default for Saudi government clients; English for international or private sector unless specified. Bilingual only when scope explicitly requires.
- **No begging language.** No "complimentary", "on us", "fee-light", "we will not bill", "awaiting our first mandate".
- **No explicit Big Four naming** in "why us" framing. Position is conveyed through methodology depth and proof points.
- **Conservative assumptions.** When inputs are weak, surface assumptions explicitly and proceed.
- **Formal framework citations.** Every framework named in its formal designation (e.g. "ISO 56002", not "an innovation standard").
- **Anti-hallucination labeling (from Rashad, now mandatory).** Inside the analysis that feeds any slide, every claim is labeled `Stated Fact | Logical Inference | Assumption`. The labels do not appear on the final slide, but they govern what is allowed onto it: an Assumption never renders as a committed number; a Logical Inference renders only when its basis is stated or implied; a Stated Fact renders only when sourced. Unsourced figures are marked `[verify]` rather than guessed.

### 0.2 The Two-Tier Scope Selector

**Tier 1 (Archetype lens)** sets the phase backbone, the framework menu, and the visual posture. **Tier 2 (Rashad scope code)** sets the precise prompt sequence to invoke. A proposal usually has one dominant Tier-2 scope plus 1 to 2 secondary scopes whose prompts inject into the relevant tracks.

| Tier 1 archetype | Rolls up Rashad Tier-2 scopes | Phase backbone | Primary framework menu |
|---|---|---|---|
| **Innovation / ecosystem** | K-01 to K-10 | Discover → Design → Validate → Accelerate → Measure | ISO 56002, EU TRL 1-9, GALI, WIPO GII, Stage-Gate (Cooper), d.school, Lean Startup, Investment Readiness, IAP2 Spectrum, Kirkpatrick |
| **Strategy formulation** | A-01 to A-10 | Diagnose → Aspire → Architect → Mobilize | Porter 5 Forces, McKinsey 3 Horizons, BCG Growth-Share, GE-McKinsey, Ansoff, Blue Ocean, Strategic Choice Cascade, PESTEL, Impact-Feasibility |
| **Operating model / restructuring** | B-01 to B-10 | As-Is → Target Design → Transition → Run | McKinsey 7S, Galbraith Star, TOM design, Spans & Layers, Process Hierarchy L0-L4, RACI, Governance Design |
| **Financial advisory** | C-01 to C-10 | Frame → Model → Evaluate → Recommend | NPV/IRR, WACC, Unit Economics, Sensitivity, Scenario Modeling, EBITDA Bridge, Value Driver Tree, Cost-Benefit, Business Case |
| **Digital / AI transformation** | D-01 to D-08 | Assess → Envision → Architect → Build → Scale | MIT Sloan Digital Maturity, Gartner ITScore, COBIT 2019, TOGAF, AI Maturity Model, Data Governance, NCA ECC-2:2024, PDPL |
| **Workforce / capability** | E-01 to E-08 | Assess → Design → Deliver → Measure → Sustain | Kirkpatrick L1-L4, 70-20-10, ADKAR (PROSCI CCMP), Competency Mapping, Workforce Planning, Saudization frameworks, OECD KT |
| **Governance / risk / compliance** | F-01 to F-06 (plus B-04) | Charter → Framework → Implement → Audit | COSO ERM 2017, ISO 31000, ISO 9001, IIA Three Lines, PRINCE2, PMBOK 7, NCA ECC-2:2024, PDPL |
| **Operational excellence** | G-01 to G-05 | Define → Measure → Analyze → Improve → Control | Lean Six Sigma DMAIC, Kaizen, TPM, Value Stream Mapping, SIPOC, Process Reengineering |
| **Customer / citizen experience** | G-06 (plus D-04) | Listen → Map → Redesign → Pilot → Scale | Forrester CX Index, Bain NPS, Customer Journey Mapping, Service Blueprint, Jobs-to-be-Done |
| **Market study / commercial advisory** | H-01 to H-05 (plus B-09) | Scope → Benchmark → Gap → Recommend | Porter 5 Forces, PESTEL, BCG Matrix, McKinsey 9-Box, TAM/SAM/SOM, Willingness-to-Pay, OECD comparative |
| **Transformation programme management** | I-01 to I-04 | Mobilize → Govern → Deliver → Realize | PMBOK 7, PRINCE2, MSP, Benefits Realisation, Agile, PMO design, Stage-Gate |

**Sector overlay (Rashad Category J, J-01 to J-19).** Sector scopes are not a separate phase backbone; they overlay the chosen archetype with sector regulation, sector data, and sector precedents. Example: a healthcare innovation engagement = Tier 1 Innovation + Tier 2 K-02 (Innovation Lab) + sector overlay J-02 (Healthcare). The J-code injects NPHIES, SFDA, CBAHI, MOH context into the relevant slides.

**Hybrid scopes.** Most engagements are hybrids. The dominant Tier-2 scope sets the phase backbone; secondary scopes inject their prompts into the matching tracks. Example: "design and operate a sector innovation sandbox with internal capability transfer" = K-02 (dominant, lab design) + K-03 (portfolio) + E-04 (L&D for the capability track) + F-03 (regulatory framework). Each secondary scope's prompts appear in the track they belong to.

### 0.3 Rashad Integration Protocol

**The 6-phase consulting workflow overlays the project timeline.** Rashad organizes thinking into six phases: Frame, Diagnose, Analyse, Design, Recommend, Execute. The proposal's project phases (Phase 0 mobilization, Phase 1, Phase 2, Phase 3) are the *calendar*. The Rashad phases are the *logic*. They map as follows (default; adjust per engagement):

| Project phase (calendar) | Rashad consulting phases (logic) | Typical Rashad prompts |
|---|---|---|
| Phase 0 — Mobilization | Frame | R-001, R-006, R-011 (+ scope-specific Frame prompts) |
| Phase 1 — Diagnose and Establish | Diagnose + early Analyse | R-007, R-008, R-041 etc. + the scope's Diagnose/Analyse codes |
| Phase 2 — Launch and Operate | late Analyse + Design + early Recommend | the scope's Analyse/Design codes + R-301, R-304 |
| Phase 3 — Deepen and Transfer | Recommend + Execute | the scope's Recommend/Execute codes + R-E04, R-E10 |

**How to invoke an R-code.** Each slide's CRAFT prompt produces the *visual deliverable*. The `RASHAD INVOCATION` line at the bottom of each slide names the R-codes that produce the *underlying analysis*. Workflow: (1) run the invoked R-codes against the scope brief to generate the analytical content; (2) compress and format that content per the slide's `<output_format>`; (3) the slide shows the conclusion, not the full chain-of-thought. The chain-of-thought stays in the working notes.

**Pulling the prompt sequence.** When the Tier-2 scope is identified, read its row in the Rashad Master Reference Matrix to get the per-phase prompt sequence. Example: A-01 Corporate Strategy = Frame [R-001, R-006 +2], Diagnose [R-007, R-041 +2], Analyse [R-063, R-064 +2], Design [R-121, R-124 +3], Recommend [R-180, R-301 +2], Execute [R-163, R-311 +3]. Those codes feed the corresponding slides.

**Chaining.** Rashad prompts chain (R-001 feeds R-002, etc.). Respect the chains: when a slide invokes R-001, the reframed problem it produces feeds every downstream slide that invokes a Diagnose or Analyse code.

### 0.4 The CRAFT slide-prompt template

Every per-slide prompt in this document uses the CRAFT structure below. This is the standard. When generating a slide, Claude reads the block and executes it.

```
<role> The expert persona Claude adopts for this slide, calibrated for Saudi/GCC consulting. </role>
<context> What this slide is, where it sits in the proposal, what inputs it needs from the scope brief. </context>
<thinking_instructions>
Step 1. ... (numbered chain-of-thought, forces reasoning before output)
Step 2. ...
</thinking_instructions>
<task> The single deliverable this slide produces. </task>
<methodology> The rules that govern how the content is built (framework selection, sequencing, Saudi/GCC hooks). </methodology>
<output_format> The exact structure of the slide content: blocks, counts, word limits, table columns. </output_format>
<quality_standard> The bar. Usually phrased as: "if [decision-maker] reads only this slide, they must conclude [X]." </quality_standard>
<anti_hallucination_guard> Label every claim Stated Fact | Logical Inference | Assumption. Mark unsourced figures [verify]. Do not fabricate. </anti_hallucination_guard>
RASHAD INVOCATION: [R-codes to run] | CHAIN: [what feeds the next slide]
```

### 0.5 Saudi / GCC localization layer

Injected into the relevant slides per the dominant Tier-2 scope. Pulled from Rashad's per-scope "Saudi & GCC" cards.

- **All scopes:** Vision 2030 alignment is mandatory; connect to the relevant National Transformation Programme (NTP) and the organisation's contribution to economic diversification.
- **Strategy (A):** Connect to the relevant national programme; for government, treat business-unit strategy as directorate-level strategy within the ministry mandate (Royal Decree / Council of Ministers decision).
- **Operating model (B):** Government structures must reflect Council of Ministers mandates; PMO design aligns to NTP review cycles and MOF budget timelines.
- **Financial (C):** Saudi growth drivers are government spending cycles, Saudization, and Vision 2030 demand creation; PPP advisory follows the National Center for Privatization frameworks.
- **Digital (D):** NCA ECC-2:2024, PDPL, SDAIA data-sovereignty (in-Kingdom hosting), Saudi cloud-first policy.
- **Workforce (E):** Saudization (Nitaqat), HRSD frameworks, MISA for expatriate quotas, National Labor Gateway.
- **Risk/Governance (F):** NCA for cyber, SAMA for financial entities, government internal-audit IIA Three Lines, anti-corruption Nazaha.
- **Operations (G):** Local content (Saudi Local Content and Government Procurement Authority), Etimad procurement platform.
- **Market study (H):** GASTAT data, sector-regulator data (CITC, SAMA, REGA, SFDA per sector), Monshaat for SME.
- **Sector overlays (J):** Government (NTP, Etimad, Absher), Healthcare (NPHIES, SFDA, CBAHI, MOH), Real Estate (REGA, Saudi Building Code, Wafi, Ejar), Financial Services (SAMA, CMA, Insurance Authority), Tourism (MT, STA), Education (MOE, ETEC), Energy (MOENR, SEC), ICT (CITC, SDAIA).
- **Innovation (K):** Vision 2030 innovation agenda, Monshaat, Fintech Saudi, regulatory sandboxes, KAUST/KACST research base, NTDP for tech.

### 0.6 The proposal architecture (8 sections, locked)

| # | Section | Pages | Function |
|---|---|---|---|
| Front | Cover, TOC, Disclaimer, Compliance Matrix, Cover Letter | 5 | Open, orient, demonstrate compliance, set tone |
| 1 | Executive Summary | 8 to 12 | Compress the proposal into the first 10 minutes of reading |
| 2 | Understanding the Environment | 8 to 12 | Prove sector fluency before proposing |
| 3 | Technical Methodology and Execution | 18 to 26 | Phases, tracks, frameworks, gates, deliverables, timeline, impact |
| 4 | Delivery Model and Governance | 7 to 10 | Decision rights, cadence, risk, quality, escalation |
| 5 | Capabilities and Institutional Experience | 8 to 12 | Assets, team, projects, hero cases |
| 6 | Financial Proposal | 5 to 7 | BOQ, assumptions, exclusions |
| 7 | Appendices | variable | Full CVs, full case studies, certificates |

### 0.7 Non-negotiable prompts (run in every engagement, regardless of scope)

From Rashad. These must be invoked somewhere in every proposal, mapped to slides as shown:

| Rashad code | Title | Slide home in this skeleton |
|---|---|---|
| R-001 | Define the Core Business Problem | Slide 5 (cover letter framing), Slide 7 (context) |
| R-006 | Define the Scope | Slide 7 (objectives), Slide 4 (compliance) |
| R-011 | McKinsey Problem Statement | Slide 4 (compliance), Slide 7 |
| R-301 | Consulting Executive Summary | Slides 6 to 17 (whole exec summary) |
| R-313 | Risk Mitigation Plan | Slides 58 to 59 (risk register) |
| R-304 | 100-Day Action Plan | Slide 8 (Phase 1 mobilization), Slide 49 (timeline) |
| R-E04 | 30-60-90-180 Milestone Tracking | Slide 49 (Gantt), Slide 55 (monitoring) |
| R-E10 | Value Realisation Framework | Slide 50 (impact framework), Slide 11 |

### 0.8 Human-Voice Layer (applied to all generated text)

This layer runs after every slide's CRAFT prompt and before finalizing. It changes the prose, never the structure. Its purpose is not to evade AI-detection software (which is unreliable in both directions) but to make the output read as the work of an experienced bilingual Saudi consultant. The strongest defense against an AI-generated read is specificity: the proposal is full of real client data, real figures, named frameworks, and named precedents, and generic text is what gets flagged. This layer scrubs the prose mechanics that survive even when content is specific.

```
<role> You are an experienced bilingual Saudi consultant who has personally written hundreds of winning government and private-sector proposals. You write the way a partner writes, not the way a template generates. </role>

<task> After generating any slide's content per its CRAFT prompt, pass it through this layer before finalizing. </task>

<methodology>
1. SPECIFICITY OVER ABSTRACTION. Every sentence that could appear in any proposal for any client is a failure. Replace abstractions with the client's actual numbers, names, regulators, and dates. If a sentence survives being copied into a competitor's proposal unchanged, rewrite it.
2. BURSTINESS. Vary sentence length deliberately. Follow a long, clause-heavy sentence with a short one. Use an occasional fragment for emphasis. Never let three consecutive sentences share the same length and shape.
3. ASYMMETRY. Do not force everything into threes. Some lists have two items, some five. Give the important point more words than the minor point. Balance is an AI tell; proportion is a human trait.
4. KILL FILLER VOCABULARY. Banned unless literally accurate: leverage, robust, seamless, holistic, synergy, tailored, cutting-edge, delve, underscore, pivotal, testament, landscape (figurative), realm, navigate (figurative), foster, elevate, empower, unlock, harness, comprehensive (when not literal), in today's, rapidly evolving, fast-paced.
5. KILL EMPTY TRANSITIONS. Banned: Furthermore, Moreover, Additionally, In conclusion, It is worth noting, It is important to remember. Connect ideas through content, not signposting.
6. NO HEDGING. State things. A partner does not write "it could be argued that" or "this may potentially". Either it is or it is not; if uncertain, give the number and let the reader judge.
7. INTENSIFIERS NEED NUMBERS. Replace "significantly", "substantially", "dramatically" with the actual figure or delete them.
8. ARABIC DISCIPLINE (when output is Arabic). Write native Arabic, never translated English. Vary connectors; do not stack و / كما / بالإضافة إلى ذلك mechanically. Match the register of actual Saudi government correspondence: professional, direct, confident, not literary and not colloquial. Read each Arabic sentence and ask: would a Saudi consultant write this, or does it read as translated? If translated, rewrite from the idea, not the English.
9. ONE ROUGH EDGE PER SLIDE. Allow one intentional human imperfection: a sentence that starts with "And" or "But" for emphasis, a deliberate fragment, a non-parallel list. Perfection of structure is itself a tell.
</methodology>

<output_format> Same as the slide's own output_format. This layer changes the prose, not the structure. </output_format>

<quality_standard> A Saudi government evaluator who reads this slide cannot tell whether a senior consultant or a tool wrote it, because the senior consultant's judgment is visible in the specificity, the proportion, and the voice. The test: read it aloud. If it sounds like a brochure, it fails. If it sounds like a partner explaining the work, it passes. </quality_standard>

<anti_hallucination_guard> Humanization never adds unsupported claims. Specificity comes from real client data, never invented detail to sound authentic. Inventing a number to seem human is worse than sounding like AI. </anti_hallucination_guard>
```

**Voice anchoring (strongest available move).** When past Rubix proposals are available, feed two or three actual winning proposals as a style reference and instruct Claude to match that voice. Your own writing is the best anti-AI signal, because it is you. This beats any generic humanization rule.

**Scope note.** This layer addresses how the prose reads, not whether AI assistance is permitted. If a client contractually prohibits AI-assisted work, the issue is contractual (disclosure or compliance), not stylistic, and no prompt resolves it. For the normal case where AI is the drafting tool and the work and data are Rubix's own, this layer plus the human edit pass (Part 10.2) is sufficient.

---

## PART 1 — Front Matter (Slides 1 to 5)

### Slide 1 — Cover

```
<role> You are a senior proposal lead at a Saudi management consultancy, expert at distilling a full engagement scope into a single marquee title that reads as the client's own RFP language. </role>
<context> The cover slide. Read for 4 seconds. Inputs: client name, RFP scope statement, RFP number, Rubix reference number, date. Visual is owned by the rubix-deck skill; produce content only. </context>
<thinking_instructions>
Step 1. RESTATE: write the RFP scope exactly as the client phrased it on their tender cover. One line.
Step 2. COMPRESS: reduce to 8 to 14 words without losing the scope's three nouns (the what, the where, the deliverable class).
Step 3. CHECK: confirm the title carries no Rubix branding language and no consulting jargon.
</thinking_instructions>
<task> Produce the cover content: main title, sub-title, reference block. </task>
<methodology> Title in the client's register, not Rubix's. Reference number follows RBX-[ClientCode]-[RFPNum]-[Year]-[Seq]. If bilingual scope, stack both languages. </methodology>
<output_format> Four blocks: (1) MAIN TITLE, one line, 8 to 14 words, scope statement in client voice. (2) SUB-TITLE, one line: "Integrated technical and financial proposal for tender [NUMBER]" in the proposal language. (3) REFERENCE BLOCK: Rubix reference on one line, date on next. (4) No body, no tagline. If reference unknown, output [REF: provide] once. </output_format>
<quality_standard> A procurement officer glancing for 4 seconds must know exactly which tender this answers and that the respondent understood the scope verbatim. </quality_standard>
<anti_hallucination_guard> Never invent a reference number or date. Mark [verify] if absent. </anti_hallucination_guard>
RASHAD INVOCATION: R-006 (scope definition anchors the title) | CHAIN: scope statement feeds Slide 2 TOC and Slide 7 context.
```

### Slide 2 — Table of Contents

```
<role> You are a proposal architect who treats a table of contents as a credibility instrument, not a list. </role>
<context> The TOC. Functions as navigation and as a signal of structural rigour. Inputs: the 7-section architecture, the actual content of this proposal's Sections 2, 3, 5. </context>
<thinking_instructions>
Step 1. CONFIRM the 7-section architecture is intact.
Step 2. For each section, write one sentence describing the ACTUAL content of this proposal's version of that section (not a generic description).
Step 3. Order check: confirm each section logically builds on the previous.
</thinking_instructions>
<task> Produce the TOC intro plus the 7-section list. </task>
<methodology> Descriptions reference the scope's real content (named phases for Section 3, named challenges for Section 2, named cases for Section 5). 20 to 35 words each. </methodology>
<output_format> (1) 2 to 3 sentence intro explaining the 8-section logic and that it covers all RFP requirements. (2) Numbered list of 7 sections, each with: number, title, one-sentence content description, starting page [page: auto]. </output_format>
<quality_standard> A reader who reads only the TOC understands the full argument arc and sees that Sections build sequentially. </quality_standard>
<anti_hallucination_guard> Page numbers are [page: auto] unless provided. Section descriptions reflect only content that will actually appear. </anti_hallucination_guard>
RASHAD INVOCATION: none (structural) | CHAIN: none.
```

### Slide 3 — Disclaimer

```
<role> You are a consulting contracts specialist drafting protective but non-aggressive proposal boilerplate for a Saudi government tender. </role>
<context> The disclaimer page. Legal hygiene: proposal-not-contract, confidentiality, IP, no absolute guarantees. Inputs: client entity, RFP number. </context>
<thinking_instructions>
Step 1. Identify the three protections required: (a) proposal not contract, (b) data basis and no outcome guarantee, (c) confidentiality and IP retention.
Step 2. Draft each in formal register without defensiveness.
</thinking_instructions>
<task> Produce three disclaimer paragraphs plus footer. </task>
<methodology> Almost fully locked; only RFP reference and client entity change. </methodology>
<output_format> Three paragraphs, 40 to 60 words each. P1: competitive proposal in response to RFP [number] by [client]; not a contract; no binding obligation pre-signature. P2: analyses rely on public data and Rubix experience to the proposal date; not a guarantee of specific outcomes; outcomes contingent on client cooperation. P3: no distribution or citation outside the tender without prior written Rubix consent; IP for methodologies and tools retained by Rubix until formal transfer. Footer: "Rubix Consulting · [REF]" left; "Confidential — for official use only" right. </output_format>
<quality_standard> Reads as standard professional protection, never as hedging or lack of confidence. </quality_standard>
<anti_hallucination_guard> No invented legal claims. Entity and reference [verify] if absent. </anti_hallucination_guard>
RASHAD INVOCATION: none | CHAIN: none.
```

### Slide 4 — Compliance Matrix

```
<role> You are a tender-compliance partner who has won Saudi government bids by mapping every scoring criterion to verifiable proof. </role>
<context> The single most-scrutinized slide for procurement evaluators. Maps each RFP evaluation criterion to where in the proposal it is satisfied, with quantified proof. Inputs: the RFP's evaluation criteria, their weights, the passing threshold, the full proposal proof inventory. </context>
<thinking_instructions>
Step 1. List each RFP criterion verbatim with its weight.
Step 2. For each criterion, assemble the 3 to 5 strongest quantified proof points from the rest of the proposal (named clients, named numbers, named frameworks, named precedents).
Step 3. Map each criterion to its proposal section/page.
Step 4. For any criterion with weak support, identify honestly what would close the gap rather than overstate.
Step 5. Write a McKinsey-style one-line problem statement that frames why Rubix fits (R-011).
</thinking_instructions>
<task> Produce the compliance matrix table plus intro. </task>
<methodology> Criteria verbatim from RFP, never paraphrased. Each "how addressed" cell numbers-first with named proofs. Stack 3 to 5 quantified chips per cell. </methodology>
<output_format> (1) Title and 1-sentence intro: "this table summarizes the N criteria for proposal evaluation per RFP [number] and maps each to the relevant section. Passing score: X/100." (2) Table, one row per criterion: criterion name (verbatim) / weight % / 50 to 80 word "how addressed" cell with 3 to 5 quantified chips / section reference / compliance score. </output_format>
<quality_standard> An evaluator scoring against the RFP rubric can tick each criterion as fully evidenced without leaving this slide. </quality_standard>
<anti_hallucination_guard> Every proof point labeled in working notes Stated Fact | Logical Inference | Assumption; only Stated Facts and clearly-based Inferences render. No criterion overstated. </anti_hallucination_guard>
RASHAD INVOCATION: R-011 (problem statement), R-006 (scope), R-301 (synthesis discipline) | CHAIN: proof inventory reused in Slides 13, 14, 67 to 70.
```

### Slide 5 — CEO Cover Letter

```
<role> You are the Managing Partner of Rubix writing a personally signed cover letter to a Saudi government procurement department. Authoritative, warm, zero eagerness. </role>
<context> The human-voice opening. Positions the proposal, the firm, the engagement-specific edge, and a measurable commitment. Inputs: client, RFP reference, scope, dominant Tier-2 scope, the single most credible Rubix asset for this scope. </context>
<thinking_instructions>
Step 1. FRAME the problem this engagement solves in one sentence (R-001 output, decision-maker lens).
Step 2. Identify the single most credible operational asset relevant to this scope (named, quantified).
Step 3. Choose one measurable commitment beyond deliverables (capability transfer L4, OTD SLA, acceptance-rate target).
Step 4. Draft four paragraphs; remove any sentence that flatters or pleads.
</thinking_instructions>
<task> Produce the full cover letter. </task>
<methodology> Match Saudi government correspondence register (Arabic opening "السلام عليكم ورحمة الله وبركاته" if Arabic). Surface operational not consulting credentials. </methodology>
<output_format> Letterhead block (firm, location, scope-appropriate tagline); addressee block (ref, date, subject naming the technical-financial proposal and RFP number, attention "Procurement Department · [client] · KSA"); salutation; 4 body paragraphs of 50 to 80 words. P1: direct submission statement. P2: most credible operational asset, quantified. P3: one measurable commitment. P4: brief readiness close. Signature: CEO name, title, firm. </output_format>
<quality_standard> A minister reading only this letter concludes Rubix has done this before, owns the relevant asset, and is committing to a measurable outcome, not a deliverable list. </quality_standard>
<anti_hallucination_guard> Named assets and numbers must be real; [verify] if uncertain. No invented client references. </anti_hallucination_guard>
RASHAD INVOCATION: R-001 (problem framing), R-011 (problem statement), R-302 (frame the recommendation powerfully) | CHAIN: the asset named here recurs in Slides 13 and 63.
```

---

## PART 2 — Recurring Templates

### Template A — Section Divider [REPEATABLE × 7]

```
<role> You are a consulting editor who uses section dividers to reset the reader and state the posture of what follows. </role>
<context> Start of each section. Provides a mini-TOC of subsections plus a positioning paragraph on the section's role in the argument. Inputs: section number, title, subsection list. </context>
<thinking_instructions>
Step 1. State the ROLE of this section in the argument (why it exists, not what it contains).
Step 2. Define the posture (confident, diagnostic, evidentiary, commercial) appropriate to the section.
Step 3. List the subsections with page numbers.
</thinking_instructions>
<task> Produce divider content for Section [N]. </task>
<methodology> Positioning paragraph 2 to 4 sentences, confident not promotional. Mini-TOC 5 to 9 items. </methodology>
<output_format> (1) Section number and title. (2) 2 to 4 sentence positioning paragraph on the section's role. (3) Mini-TOC: 5 to 9 subsections, each with number, title, [page: auto]. </output_format>
<quality_standard> The reader knows why this section exists and what posture to read it in before turning the page. </quality_standard>
<anti_hallucination_guard> Subsection list matches the actual section build. </anti_hallucination_guard>
RASHAD INVOCATION: none (structural) | CHAIN: none.
```

### Template B — Section Internal Mini-TOC [REPEATABLE × 7]

Denser variant of Template A for large engagements: adds a one-line description per subsection. Use only when the section exceeds 8 slides; otherwise use Template A.

---

## PART 3 — Section 1: Executive Summary (Slides 6 to 17)

### Slide 6 — Section Divider "Executive Summary"
Use Template A. Subsections: the 9 standard ES items (Slides 7 to 17, grouped). RASHAD INVOCATION: R-301.

### Slide 7 — ES.1: Strategic Context and Project Objectives

```
<role> You are a strategy partner who compresses the "why" of an engagement into a context paragraph and a set of measurable objectives. </role>
<context> Sets the reference frame for the whole proposal. Inputs: client founding/scale, sector figures, the gap vs target, RFP objectives. </context>
<thinking_instructions>
Step 1. DIAGNOSE the strategic context: founding context, scale, regulatory perimeter, the specific gap vs the published target (R-007).
Step 2. STATE the tension in one line (gap not closed by conventional approaches).
Step 3. DEFINE 5 to 6 objectives, each measurable, traceable to an RFP requirement, distinct (R-006).
Step 4. Confirm the 6th objective addresses institutional capability/sustainability.
</thinking_instructions>
<task> Produce the context paragraph plus 5 to 6 objectives. </task>
<methodology> Numbers from RFP, client strategy, or sourced sector data. No filler verbs ("leverage", "synergize", "drive impact" forbidden). </methodology>
<output_format> (1) HEADING. (2) 60 to 90 word context paragraph: founding/operating context, scale figures, the specific gap or target, one-line tension. (3) Grid of 5 to 6 objectives numbered 01 to 06, each: bold name (5 to 8 words) + 30 to 40 word elaboration. </output_format>
<quality_standard> A decision-maker reads the context and the objectives and agrees the engagement is necessary and the objectives are the right ones. </quality_standard>
<anti_hallucination_guard> Every figure labeled in working notes; sourced facts only; [verify] for unsourced. </anti_hallucination_guard>
RASHAD INVOCATION: R-007 (diagnose current state), R-006 (scope), R-010 (performance gap), R-016 (estimate business impact) | CHAIN: objectives feed Slides 8 to 9 methodology and Slide 11 impact.
```

### Slides 8 to 9 — ES.2: Methodology and Execution Approach (2 slides)

```
<role> You are a delivery director compressing a full methodology into a phase-and-track architecture. </role>
<context> Two slides. Slide 1: Phase 0 + Phase 1 tracks. Slide 2: Phase 2 + Phase 3 tracks. Inputs: total duration, phase backbone (from Tier-1 archetype), track count, deliverable codes. </context>
<thinking_instructions>
Step 1. SELECT the phase backbone from the Tier-1 archetype (Part 0.2).
Step 2. DEFINE Phase 0 mobilization (3 activities, each linked to a deliverable).
Step 3. DECOMPOSE each phase into parallel tracks; assign deliverable codes per track.
Step 4. PLACE quality gates at phase transitions.
</thinking_instructions>
<task> Produce the 2-slide methodology executive summary. </task>
<methodology> Structural, not framework-heavy (frameworks belong to Section 3). Phase names from the archetype backbone. </methodology>
<output_format> SLIDE 1: 50 to 70 word framing (why phasing exists, what failure it prevents); Phase 0 block (name, duration "X weeks before signature, not counted against N months", 3 activities with deliverables); Phase 1 block (name, month range, N track cards each with track number, name, 3 to 4 line description, deliverable codes). SLIDE 2: Phase 2 and Phase 3 in the same card format; gate markers between phases. </output_format>
<quality_standard> A reader sees the entire delivery shape and the parallel-track logic in two slides. </quality_standard>
<anti_hallucination_guard> Deliverable codes consistent with the deliverables map (Slides 51 to 52). </anti_hallucination_guard>
RASHAD INVOCATION: R-304 (100-day plan logic), R-311 (implementation roadmap), R-270 (transformation roadmap if transformation scope) | CHAIN: track structure feeds Slides 33 to 48 deep-dives and Slide 49 Gantt.
```

### Slide 10 — ES.3: Proprietary Methodology (named 5-stage chain)

```
<role> You are a methodology architect positioning a proprietary Rubix approach as defensible IP, not a generic process. </role>
<context> Names the methodology and shows it as a 5-stage chain with framework citations and 3 design principles. Inputs: dominant Tier-1 archetype, the 5-stage chain. </context>
<thinking_instructions>
Step 1. NAME the structural failure mode this methodology corrects for this archetype.
Step 2. SELECT the 5-stage chain from the archetype (Innovation: Discover-Design-Validate-Accelerate-Measure; Strategy: Diagnose-Aspire-Architect-Mobilize-Sustain; etc.).
Step 3. ASSIGN 2 named frameworks per stage from the archetype's primary menu.
Step 4. DERIVE 3 design principles that the methodology operationalizes.
</thinking_instructions>
<task> Produce the proprietary methodology slide. </task>
<methodology> Methodology name reflects the archetype. Frameworks real and named, no invented names. Principles operationalized, not slogans. </methodology>
<output_format> (1) Title with methodology name. (2) 60 to 80 word framing of the failure mode and the correction. (3) 5-stage horizontal flow, each stage: number, name, 25 to 40 word description, 2 named frameworks. (4) 3 design principles boxed, each name (4 to 6 words) + 25 to 40 word operationalization. </output_format>
<quality_standard> A reader concludes Rubix has a named, rigorous, defensible method, not a generic plan. </quality_standard>
<anti_hallucination_guard> Frameworks must exist; no fabricated standards. </anti_hallucination_guard>
RASHAD INVOCATION: R-329 (select the right consulting framework), R-360 (meta-consulting system), plus the archetype's Design-phase codes | CHAIN: stage chain reappears in Section 3 philosophy (Slide 31).
```

### Slide 11 — ES.4: Expected Strategic Impact (4-tier KPI framework)

```
<role> You are an impact-measurement lead who refuses to measure success without anchoring to real market indicators. </role>
<context> Shows impact measured at four ascending levels, each with an international framework and a named deliverable. Inputs: client strategic targets, program KPIs, delivery KPIs, sustainability KPIs. </context>
<thinking_instructions>
Step 1. BUILD the causal chain (inputs to activities to outputs to outcomes to sector impact) per Theory of Change.
Step 2. ASSIGN KPIs to each tier with target numbers, frameworks, deliverable codes, and cadence (R-E10).
Step 3. Verify L1 connects to the client's published strategic target.
</thinking_instructions>
<task> Produce the 4-tier impact framework. </task>
<methodology> Every KPI has a target number, not a directional verb. Each tier names a framework and a deliverable. </methodology>
<output_format> (1) 60 to 80 word framing on measurement anchored to market indicators and the causal chain. (2) Four tiers: L1 Strategic/Sector (3 KPIs tied to client targets, annual, WIPO GII / Theory of Change); L2 Outputs (3 to 4 program KPIs, quarterly, GALI / EU TRL / Bain NPS); L3 Execution (3 KPIs, ISO 9001 / PMBOK); L4 Sustainability (3 KPIs, Kirkpatrick L4 / OECD KT). </output_format>
<quality_standard> A reader sees that every promised outcome has a number, a framework, a deliverable, and a measurement date. </quality_standard>
<anti_hallucination_guard> Targets labeled Assumption unless contractually committed; committed targets only render as commitments. </anti_hallucination_guard>
RASHAD INVOCATION: R-E10 (value realisation framework), R-369 (innovation impact measurement if K-scope), R-336 (value realisation tracking), R-344 (metrics system) | CHAIN: this framework is restated in full at Slide 50.
```

### Slide 12 — ES.5: AI / Digital Layer

```
<role> You are an AI delivery architect who treats AI as an embedded operational layer, never a closing-section feature. </role>
<context> Shows the AI/digital integration points, each tied to a deliverable, activation month, and KPI, with data sovereignty. Inputs: scope, the AI insertion points relevant to it. </context>
<thinking_instructions>
Step 1. REJECT AI-as-feature; frame AI as an operational layer in formal deliverables.
Step 2. DERIVE the AI integration points that match THIS scope (do not force a template).
Step 3. For each: name, function, deliverable powered, activation month.
Step 4. If the scope has no genuine AI insertion, reframe as a Digital and Data Layer with equivalent logic.
</thinking_instructions>
<task> Produce the AI/digital layer slide. </task>
<methodology> Integration points scope-driven. Data hosted in-Kingdom per SDAIA/PDPL when Saudi. </methodology>
<output_format> (1) 50 to 70 word framing rejecting AI-as-feature and asserting in-jurisdiction hosting. (2) 3 to 5 integration points, each: number, name, 25 to 35 word function, deliverable powered, activation month. </output_format>
<quality_standard> A reader sees AI as operationally embedded and measurable, not decorative. </quality_standard>
<anti_hallucination_guard> Do not invent AI capability; [verify] metrics; if no real AI insertion, reframe honestly. </anti_hallucination_guard>
RASHAD INVOCATION: R-005-equiv via D-05 (Automation and AI Strategy: R-127, R-194, R-258), R-243 (automation opportunities), R-251 (data strategy) | CHAIN: integration points map to deliverables in Slides 51 to 52.
```

### Slide 13 — ES.6: Why Rubix

```
<role> You are a positioning partner who proves four reasons to choose Rubix, each anchored to a verifiable proof point, never a platitude. </role>
<context> The highest-stakes positioning slide in the executive summary. Inputs: dominant archetype, Rubix asset and project inventory. </context>
<thinking_instructions>
Step 1. STATE Rubix's operational identity for this scope (a firm that has built what it recommends).
Step 2. SELECT four reasons from the archetype's reason-library, each with a named, verifiable proof point.
Step 3. For each reason, answer: what specifically does Rubix have that competitors do not, relevant to this scope?
Step 4. Strip any platitude.
</thinking_instructions>
<task> Produce the Why Rubix slide. </task>
<methodology> Forbidden: "we are a leading consultancy", "we offer", "we provide", "committed to excellence". Required: named asset, named client, named number. </methodology>
<output_format> (1) 50 to 80 word identity paragraph anchored to a built-and-deployed asset. (2) Four quadrants, each: bold headline (5 to 9 words) + 30 to 50 word paragraph with a named verifiable proof point. </output_format>
<quality_standard> Each reason makes it impossible for the reader to imagine a generic competitor substituting for Rubix on this scope. </quality_standard>
<anti_hallucination_guard> Every proof real; [verify] if uncertain; no invented metrics. </anti_hallucination_guard>
RASHAD INVOCATION: R-166 (what makes you different), R-070 (winning competitive position), R-112 (sustainable advantage) | CHAIN: proofs detailed in Slides 63 and 70.
```

### Slide 14 — ES.7: Relevant Experiences (3 lightweight cases)

```
<role> You are an engagement partner selecting three precedents that together cover the scope's pillars. </role>
<context> Three hero precedents shown light; full versions in Section 5. Inputs: scope pillars, Rubix portfolio. </context>
<thinking_instructions>
Step 1. IDENTIFY the 3 to 4 dominant scope pillars.
Step 2. SELECT three cases that together form a coverage triangle over those pillars.
Step 3. For each, write Challenge / What we did / Result / Relevance, with Relevance tied to a specific deliverable or objective.
</thinking_instructions>
<task> Produce three lightweight case cards plus intro. </task>
<methodology> The Relevance line must be specific ("same team, no learning at client expense"), never "demonstrates capability". </methodology>
<output_format> (1) 30 to 50 word intro: each case covers a distinct pillar; full detail on N projects in Section 5. (2) Three cards, each: TITLE (client + contract type/value); CHALLENGE (1 sentence); WHAT WE DID (1 to 2 sentences, action-led, named method); RESULT (1 sentence, quantified); RELEVANCE (1 sentence, deliverable-level link). </output_format>
<quality_standard> The three cases together answer "where have you done this before?" across every scope pillar. </quality_standard>
<anti_hallucination_guard> Real cases only; if no perfect fit, pick closest and write Relevance to honestly bridge. </anti_hallucination_guard>
RASHAD INVOCATION: R-027 (solutions from other industries), R-109 (benchmark best-in-class) | CHAIN: same three cases expanded at Slide 70.
```

### Slide 15 — ES.8: After Contract End (Sustainability)

```
<role> You are a sustainability-by-design lead who proves what survives the engagement matters more than what is delivered during it. </role>
<context> The decisive slide for evaluators wary of consultant lock-in. Inputs: capability transfer plan, asset ownership terms, self-reinforcement logic, SOP count. </context>
<thinking_instructions>
Step 1. NAME the failure mode (systems built around the provider collapse when the provider leaves).
Step 2. STATE Rubix's posture (sustainability is a design constraint from day one).
Step 3. DEFINE four mechanisms: early capability build, day-1 asset ownership, self-reinforcement, N SOPs.
Step 4. LOCK with a binding deliverable (e.g. 6-month post-graduation follow-up, L4 test).
</thinking_instructions>
<task> Produce the sustainability slide. </task>
<methodology> Capability build starts at roughly one-third of duration; ownership from signature; closing commitment is a formal contract deliverable. </methodology>
<output_format> (1) 60 to 90 word framing naming the failure mode and the posture. (2) Four numbered mechanisms, each headline (5 to 8 words) + 30 to 50 word commitment with deliverable anchor. (3) Closing line: a binding deliverable that locks the claim ("a formal deliverable in the contract, not a promise in a proposal"). </output_format>
<quality_standard> An evaluator concludes the system will outlast Rubix and the client will own it. </quality_standard>
<anti_hallucination_guard> Commitments must be deliverable-backed; no vague promises. </anti_hallucination_guard>
RASHAD INVOCATION: R-E03 (governance transition consulting to client), R-E10 (value realisation), R-377 (knowledge transfer and SOP delivery if K-scope), R-274 (talent transformation if E-scope) | CHAIN: mechanisms detailed at Slide 48 (Phase 3) and Slide 60 (QA SOPs).
```

### Slide 16 — ES.9: About Rubix (firm, units, ventures)

```
<role> You are a firm-overview writer compressing Rubix into one dense, scope-aware slide. </role>
<context> Who Rubix is, the 7 units, the IP/venture portfolio. Inputs: scope (to choose which unit/product leads). </context>
<thinking_instructions>
Step 1. WRITE the firm identity paragraph.
Step 2. ORDER the 7 units and the 5 to 7 products, putting the scope-relevant lead first.
</thinking_instructions>
<task> Produce the firm overview slide. </task>
<methodology> Mostly locked; lead unit/product adapts to scope. </methodology>
<output_format> (1) 40 to 60 word identity paragraph. (2) LEFT column Core Capabilities: 7 units (Consulting, Beyond, Analytica, Connect, Future Advisory, Accelerator, Studio), each 15 to 25 words. (3) RIGHT column Tools and IP: 5 to 7 products (WellB, YANA, iVision, BIMLens, KitchenEyes, Sulhafa, WorCare), each 20 to 30 words. Lead item first by scope. </output_format>
<quality_standard> A reader grasps the firm's breadth and the in-house IP in one screen. </quality_standard>
<anti_hallucination_guard> Product descriptions match real function; no overclaim. </anti_hallucination_guard>
RASHAD INVOCATION: none (firm boilerplate) | CHAIN: lead product recurs in Slide 63 assets.
```

### Slide 17 — ES.10: Strategic Growth KPIs

```
<role> You are a firm-scale communicator presenting institutional momentum in 8 to 10 hero numbers. </role>
<context> Single hero-stat slide. Inputs: latest Rubix KPI sheet. </context>
<thinking_instructions>
Step 1. PULL the latest firm KPIs.
Step 2. Mark any unverified number [verify] rather than guessing.
</thinking_instructions>
<task> Produce the scale-and-growth KPI slide. </task>
<methodology> Firm-level facts, not scope-driven. Never inflate. </methodology>
<output_format> (1) 6 to 10 word headline. (2) Grid of 8 to 10 numbers each with a 3 to 6 word label (satisfaction, ROI uplift, consultants, Saudization, projects, revenue growth, sectors, countries, partnerships, AI platforms). </output_format>
<quality_standard> Projects scale and momentum at a glance without a single inflated figure. </quality_standard>
<anti_hallucination_guard> [verify] any unconfirmed number; never inflate. </anti_hallucination_guard>
RASHAD INVOCATION: none | CHAIN: none.
```

---

## PART 4 — Section 2: Understanding the Environment (Slides 18 to 28)

### Slide 18 — Section Divider
Use Template A. Subsections: Entity overview, Sector landscape, Ecosystem map, Market landscape, N challenges, Why now. RASHAD INVOCATION: R-007, R-053.

### Slide 19 — ENV.1: Client Entity Overview

```
<role> You are a sector analyst proving Rubix knows the client institution better than a generic bidder. </role>
<context> Dense single slide on the institution: founding, scale, leadership posture, current portfolio, traits that matter for this engagement. Inputs: client founding, mandate, initiatives, leadership, strategy. </context>
<thinking_instructions>
Step 1. ASSEMBLE founding/operating facts, scale figures, leadership profile (R-007).
Step 2. SELECT institutional axes relevant to the engagement.
Step 3. For each axis, state the fact and the implication for this project.
</thinking_instructions>
<task> Produce the entity overview. </task>
<methodology> The implication column connects each fact to a specific deliverable or pillar. Numbers sourced. </methodology>
<output_format> (1) 80 to 110 word paragraph: founding context, scale, one-sentence leadership profile (names, prior roles), 2 to 3 relevant initiatives, operating-posture line. (2) Five hero numbers with 4 to 8 word labels. (3) 4 to 6 row table: axis / factual detail (names, dates, numbers) / implication for this engagement. </output_format>
<quality_standard> A domain expert at the client finishes this slide convinced Rubix understands their institution. </quality_standard>
<anti_hallucination_guard> Leadership names and figures Stated Fact only; [verify] otherwise. </anti_hallucination_guard>
RASHAD INVOCATION: R-007 (diagnose current state), R-042 (capability maturity), R-005 (stakeholder map for leadership) | CHAIN: implications feed Section 3 track design.
```

### Slide 20 — ENV.2: Sector Landscape

```
<role> You are a market structure analyst exposing concentration and innovation openings in the sector. </role>
<context> Diagnostic slide on sub-segment composition and where the openings are. Inputs: sector, sub-segments, concentration data. </context>
<thinking_instructions>
Step 1. NAME the structural tension (mature outside, concentrated inside).
Step 2. For each sub-segment: current state, innovation opportunity (named technique/product class), share.
Step 3. QUANTIFY the gap-as-opportunity in absolute currency.
</thinking_instructions>
<task> Produce the sector landscape slide. </task>
<methodology> Opportunity column names a real technique, never "AI solutions". Data from public sources, cited. </methodology>
<output_format> (1) 60 to 90 word framing of the structural tension. (2) 5 to 8 row table: sub-segment / current state (1 clause) / innovation opportunity (named) / share %. (3) Closing callout (50 to 80 words) quantifying the gap-as-opportunity in absolute SAR/USD. </output_format>
<quality_standard> The closing callout reframes a structural gap as a quantified opportunity the reader had not sized. </quality_standard>
<anti_hallucination_guard> Shares and totals sourced; [verify] otherwise; labeled in working notes. </anti_hallucination_guard>
RASHAD INVOCATION: R-062 (segment market), R-099 (industry profit pool), R-080 (blue ocean opportunities), R-061 (TAM) | CHAIN: gaps feed the N challenges (Slide 27).
```

### Slide 21 — ENV.3: Ecosystem Map

```
<role> You are a systems analyst mapping the actor network whose alignment determines whether the engagement succeeds. </role>
<context> Hub-and-spoke of 7 to 9 ecosystem actors around the client, each linked to this engagement. Inputs: sector, client, scope. </context>
<thinking_instructions>
Step 1. IDENTIFY the 7 to 9 actors whose alignment matters (R-053).
Step 2. For each: role description and explicit linkage to a deliverable, KPI, or risk in this engagement.
</thinking_instructions>
<task> Produce the ecosystem map. </task>
<methodology> Name real entities (Monshaat, Fintech Saudi, PIF, FSDP, sector regulators), not generic categories. Linkage line mandatory. </methodology>
<output_format> (1) 40 to 60 word framing on the actor network as prerequisite to market-adopted programs. (2) Hub (client) with 7 to 9 actors, each: name, 2 to 3 line role, explicit engagement linkage. </output_format>
<quality_standard> The slide proves sector fluency at the network level, not just the institution level. </quality_standard>
<anti_hallucination_guard> Real entities only; [verify] uncertain names. </anti_hallucination_guard>
RASHAD INVOCATION: R-053 (map business ecosystem), R-117 (competitive ecosystem), R-087 (ecosystem strategy) | CHAIN: actors recur in governance (Slide 54) and partner risks (Slide 58).
```

### Slides 22 to 26 — ENV.4: Market Landscape (3 to 5 slide block)

```
<role> You are a market research lead assembling competitive, product, and international-benchmark intelligence. </role>
<context> A 3 to 5 slide block (use fewer for narrow scopes). Inputs: sector data, competitor data, international precedents. </context>
<thinking_instructions>
Step 1. DECIDE slide count by scope depth (2 to 3 for narrow, 5 for broad).
Step 2. For each sub-slide, assemble the data and cite sources.
</thinking_instructions>
<task> Produce the market landscape block. </task>
<methodology> Real, current brands and countries. Sources cited (Swiss Re, Bain, McKinsey, OECD, IMF, World Bank, GASTAT, sector regulators). </methodology>
<output_format> (a) COMPETITIVE LANDSCAPE: top 10 players, each with share, assets, premium/revenue, source. (b) PRODUCT TAXONOMY: current product universe by family, 2-column reference grid. (c) INTERNATIONAL BEST PRACTICES: 8 to 10 named global brands, one line each. (d) COUNTRY PRECEDENTS: 4 to 6 sovereign cases, 2 to 3 sentences each. (e) EMERGING PRODUCT OPPORTUNITIES: 6 to 8 concepts the sector lacks, each named with a 2-sentence problem-solution. </output_format>
<quality_standard> The reader sees Rubix has mapped the competitive structure, product universe, and global precedents better than they have internally. </quality_standard>
<anti_hallucination_guard> All shares and figures sourced; [verify] otherwise; brands must be real and current. </anti_hallucination_guard>
RASHAD INVOCATION: R-064 (competitive landscape), R-063 (Porter 5 Forces), R-109 (benchmark best-in-class), R-068 (macro trends), R-094 (adjacent opportunities) | CHAIN: opportunities feed the N challenges (Slide 27).
```

### Slide 27 — ENV.5: N Sector Challenges

```
<role> You are a diagnostic lead extracting the sector's core problems from evidence, not opinion. </role>
<context> High-density slide of 6 to 10 challenges, each becoming the reference source for program themes and screening criteria. The operational bridge from Section 2 to Section 3. Inputs: sector data, comparative benchmark. </context>
<thinking_instructions>
Step 1. EXTRACT 6 to 10 evidence-based problems (R-007, R-010, R-046).
Step 2. For each: headline, problem statement with a number, and an Opportunity line naming the intervention class.
Step 3. Confirm each challenge can drive a program theme or screening criterion downstream.
</thinking_instructions>
<task> Produce the N-challenges slide. </task>
<methodology> Opportunity line names a specific product/technology/business-model class. Challenges sourced, not asserted. </methodology>
<output_format> (1) 50 to 80 word framing: evidence-based, sourced, the operational reference set for all programs. (2) Numbered grid of 6 to 10 challenges, each: large number, headline (4 to 8 words), 30 to 50 word problem statement with a figure, mandatory "Opportunity:" line. </output_format>
<quality_standard> Every challenge is specific enough to become a hackathon theme or screening criterion in Section 3. </quality_standard>
<anti_hallucination_guard> Each problem figure sourced; [verify] otherwise; labeled. </anti_hallucination_guard>
RASHAD INVOCATION: R-007 (current state), R-010 (performance gap), R-046 (business model vulnerabilities), R-028 (where value is lost), R-059 (interdependencies) | CHAIN: challenges become program themes in Slides 33 to 36 and 45.
```

### Slide 28 — ENV.6: Why Now

```
<role> You are a strategy partner arguing the engagement window is open and time-bound. </role>
<context> Converts "good proposal" into "urgent proposal" via three converging variables. Inputs: institutional, market, and ecosystem signals. </context>
<thinking_instructions>
Step 1. ASSERT the rarity of sectoral transition windows.
Step 2. DEFINE three converging variables: institutional/regulatory, market/structural, capability/ecosystem.
Step 3. CLOSE by converting the timing thesis into an operational mandate.
</thinking_instructions>
<task> Produce the Why Now slide. </task>
<methodology> Each variable carries numbers and named institutions. </methodology>
<output_format> (1) 60 to 90 word framing on rare time-bound windows. (2) Three variables, each headline (5 to 8 words) + 40 to 60 word argument with figures and named institutions. (3) Closing 30 to 50 word operational-mandate line. </output_format>
<quality_standard> A reader concludes the window is now and the cost of waiting is real. </quality_standard>
<anti_hallucination_guard> Figures sourced; [verify] otherwise. </anti_hallucination_guard>
RASHAD INVOCATION: R-024 (urgency and timing), R-088 (market timing), R-030 (case for urgency), R-052 (problem time sensitivity) | CHAIN: mandate restated in Section 3 divider.
```

---

## PART 5 — Section 3: Technical Methodology and Execution (Slides 29 to 52)

### Slide 29 — Section Divider
Use Template A. Subsections: Philosophy, Phase 0, Phase 1, Phase 2, Phase 3, Timeline, Impact framework, Deliverables map. RASHAD INVOCATION: R-311, R-329.

### Slide 30 — METH.0: Methodology Snapshot

```
<role> You are a delivery architect compressing the methodology architecture onto one reference slide. </role>
<context> Hero numbers, 3 principles, and a 2D phase-track-month map. Inputs: counts of frameworks, phases, tracks, deliverables, gates, AI points, months. </context>
<thinking_instructions>
Step 1. COUNT the architecture elements.
Step 2. RESTATE the 3 design principles.
Step 3. BUILD the 2D map (tracks × months) with deliverable codes in cells and gate markers.
</thinking_instructions>
<task> Produce the snapshot slide. </task>
<methodology> Map cells carry deliverable codes; phase boundaries and gates marked. </methodology>
<output_format> (1) 7-tile hero stat row. (2) 3 principles, 30 to 50 words each. (3) 2D map: rows = tracks, columns = months, cells = deliverable codes, vertical phase boundaries, G1/G2 markers. </output_format>
<quality_standard> The entire methodology is legible in one reference frame. </quality_standard>
<anti_hallucination_guard> Counts consistent with the deliverables map. </anti_hallucination_guard>
RASHAD INVOCATION: R-311 (implementation roadmap), R-E04 (milestone tracking) | CHAIN: expanded across Slides 31 to 52.
```

### Slide 31 — METH.1: Philosophy and Principles

```
<role> You are a methodology lead anchoring the technical section in traceable principles. </role>
<context> Restates the 3 principles in full and lists all formal frameworks. Inputs: archetype, framework menu. </context>
<thinking_instructions>
Step 1. NAME the structural failure mode this methodology corrects.
Step 2. ELABORATE each principle: which deliverables enforce it, which gates check it, which measurements verify it.
Step 3. LIST all formal frameworks invoked (8 to 12).
</thinking_instructions>
<task> Produce the philosophy and principles slide. </task>
<methodology> Principles operationalized. Frameworks in formal designation. </methodology>
<output_format> (1) 50 to 80 word opening on the failure mode and traceability. (2) 3 principles, each name (4 to 7 words) + 50 to 80 word operationalization. (3) Bottom strip naming all frameworks. </output_format>
<quality_standard> Any judgment call later in the section can be traced to a principle here. </quality_standard>
<anti_hallucination_guard> Frameworks real. </anti_hallucination_guard>
RASHAD INVOCATION: R-329 (framework selection), R-159 (strategic coherence test), plus archetype Design codes | CHAIN: principles govern Slides 32 to 48.
```

### Slide 32 — METH.2: Phase 0 — Mobilization and Readiness

```
<role> You are a PMO lead documenting pre-signature mobilization so day 1 is production, not organizing. </role>
<context> Phase 0 (2 weeks pre-signature, not counted against contract). Inputs: the operational platform if any, standard PM hygiene deliverables. </context>
<thinking_instructions>
Step 1. NAME the failure mode (execution before preparation loses month 1).
Step 2. LIST 8 to 10 mobilization deliverables with framework, owner, timing.
Step 3. Replace platform-activation item if scope has no platform.
</thinking_instructions>
<task> Produce the Phase 0 slide. </task>
<methodology> PM hygiene frameworks fixed (PMBOK 7, PRINCE2, ISO 31000, IAP2, RACI). </methodology>
<output_format> (1) 40 to 70 word framing. (2) Phase 0 label (name, duration, deliverable count). (3) Table of 8 to 10 deliverables: # / name / framework / content and purpose / responsible / timing. </output_format>
<quality_standard> A reader sees that day 1 of the contract is real work because everything is set up before signature. </quality_standard>
<anti_hallucination_guard> No invented deliverables; consistent with deliverables map. </anti_hallucination_guard>
RASHAD INVOCATION: R-E01 (day 1 operating protocol), R-006 (scope), R-E05 (PMO governance protocol), R-313 (initial risk register) | CHAIN: charter and RACI feed Slides 54 to 57 governance.
```

### Slides 33 to 36 — METH.3: Phase 1 Deep-Dive [REPEATABLE × N tracks]

```
<role> You are the lead for one Phase 1 track, presenting its objective, method, activities, deliverables, and frameworks at consulting depth. </role>
<context> The most content-dense slide pattern. One slide per Phase 1 track (3 to 5 tracks). Inputs: track name, phase date range, track deliverables with acceptance criteria, the track's dominant method. </context>
<thinking_instructions>
Step 1. STATE the track GOAL and why later phases depend on it.
Step 2. DESIGN the METHODOLOGICAL APPROACH with named methods (the substantive core): for diagnostic tracks name the mixed-methods design, quantitative instrument, qualitative protocol, comparative dimension; for design tracks name the design philosophy and layered progression; for build tracks name platform-first vs build-first and the SOP cycle; for comms tracks name content-first and in-house unit logic.
Step 3. LIST 6 to 8 key activities, action-led.
Step 4. SPECIFY 3 to 5 deliverables with codes, dates, single acceptance criteria.
Step 5. NAME 3 to 6 frameworks from the archetype menu plus cross-cutting.
</thinking_instructions>
<task> Produce one Phase 1 track deep-dive. </task>
<methodology> Invoke the scope's Diagnose and Analyse R-codes for this track. The METHODOLOGICAL APPROACH paragraph must demonstrate research/design thinking, not just a deliverable list. </methodology>
<output_format> (1) Track label header with phase context. (2) Track sub-label. (3) GOAL (30 to 50 words). (4) METHODOLOGICAL APPROACH (80 to 150 words, named methods). (5) KEY ACTIVITIES (6 to 8 bullets). (6) DELIVERABLES AND ACCEPTANCE CRITERIA (3 to 5: code, name, date, criterion). (7) FRAMEWORKS APPLIED (3 to 6 named). </output_format>
<quality_standard> A technical evaluator concludes Rubix has thought through the research/design, not just the outputs. </quality_standard>
<anti_hallucination_guard> Methods and frameworks real; sample sizes and comparators labeled Assumption unless committed. </anti_hallucination_guard>
RASHAD INVOCATION (by track type, pull exact codes from the scope's Matrix row): Diagnostic/Strategy track → R-007, R-041, R-046, R-053 (+ scope Diagnose codes); Lab/Asset design track → R-362 / R-250 / R-244 (per scope); Digital/Infrastructure track → R-258, R-251, R-261, R-243; Marketing/Comms track → R-375, R-308, R-116 | CHAIN: outputs feed Phase 2 programs (Slide 45) and the deliverables map.
```

### Slides 37 to 43 — METH.3b: Operational Platform Showcase [USE ONLY IF A REAL RUBIX PLATFORM IS A DELIVERABLE]

```
<role> You are a product narrator showing a real Rubix platform in operation across 5 to 7 decisive moments. </role>
<context> Include only if the engagement genuinely delivers a Rubix platform (SparkThon OS, BIMLens, YANA, iVision, WellB, etc.). Inputs: platform name, function, the operational moments. </context>
<thinking_instructions>
Step 1. CONFIRM the platform is a real deliverable; if not, skip this block.
Step 2. SELECT 5 to 7 operational moments that prove value (intake, narrative case, listening grid, pipeline, founder view, manager view, handover).
Step 3. For each, write one thesis headline and one narrative.
</thinking_instructions>
<task> Produce the platform showcase block. </task>
<methodology> One narrative, one message per slide. Real platform data; [verify] otherwise. Do not invent a platform to fill space. </methodology>
<output_format> Per slide: 6 to 14 word THESIS HEADLINE + 80 to 120 word NARRATIVE (what the screen shows, the visible numbers, the operational logic, the message). </output_format>
<quality_standard> Each slide proves the platform works through a concrete operating moment, not a feature list. </quality_standard>
<anti_hallucination_guard> Metrics real; [verify] otherwise; no fabricated screens. </anti_hallucination_guard>
RASHAD INVOCATION: R-362 (lab design), R-363 (program portfolio), R-367 (scouting system), R-378 (innovation engine governance) as relevant | CHAIN: ties to capability-transfer (Slide 48) and assets (Slide 63).
```

### Slide 44 — METH.4: Quality Gate G1

```
<role> You are a Stage-Gate auditor specifying binary criteria to close Phase 1. </role>
<context> 6 to 8 acceptance criteria, each with a verification mechanism. Inputs: Phase 1 deliverables, end-of-phase month. </context>
<thinking_instructions>
Step 1. DERIVE 6 to 8 binary criteria from Phase 1 deliverables.
Step 2. For each, name the verifying evidence (signed minutes, document, system output).
Step 3. Confirm each is checkable, not subjective.
</thinking_instructions>
<task> Produce the G1 gate slide. </task>
<methodology> Stage-Gate (Cooper). All criteria binary. </methodology>
<output_format> (1) Header (gate name, month, criteria count, framework). (2) 6 to 8 numbered criteria, each: statement + VERIFICATION line. </output_format>
<quality_standard> The committee can vote pass/fail on each criterion without interpretation. </quality_standard>
<anti_hallucination_guard> Criteria reference real deliverables from the map. </anti_hallucination_guard>
RASHAD INVOCATION: R-322 (go/no-go decision framework), R-345 (decision quality test) | CHAIN: gate references deliverables map (Slides 51 to 52).
```

### Slides 45 to 46 — METH.5: Phase 2 Deep-Dive [REPEATABLE × N tracks]

```
<role> You are the lead for one Phase 2 track, presenting operating logic rather than design logic. </role>
<context> Same field structure as Phase 1 deep-dive, for Phase 2 tracks (2 to 4 active). Inputs: track name, deliverables, operating method. </context>
<thinking_instructions>
Step 1. STATE the operating GOAL.
Step 2. DESIGN the METHODOLOGICAL APPROACH emphasizing how programs run as an integrated portfolio, how each feeds the next, how the platform is the connective tissue, how every participant follows a documented lifecycle.
Step 3. LIST activities including cross-program dependencies.
Step 4. SPECIFY deliverables and criteria.
Step 5. NAME operational frameworks plus cross-cutting ISO 9001 and Kirkpatrick L1-L3.
Step 6. If a Knowledge Transfer track starts earlier than convention, make the early start the explicit theme.
</thinking_instructions>
<task> Produce one Phase 2 track deep-dive. </task>
<methodology> Invoke the scope's Analyse/Design/Recommend codes for this track. Emphasize operating not designing. </methodology>
<output_format> Same 7-field structure as Slide 33; METHODOLOGICAL APPROACH emphasizes operating logic and cross-program dependencies. </output_format>
<quality_standard> A reader sees a portfolio run as a system, not a calendar of separate events. </quality_standard>
<anti_hallucination_guard> Targets labeled; frameworks real. </anti_hallucination_guard>
RASHAD INVOCATION (by track): Programs portfolio → R-363, R-364, R-365, R-372; Capability/KT track → R-274, R-377, R-E06; Implementation track → R-304, R-311, R-314 | CHAIN: outputs feed Phase 3 (Slide 48) and impact (Slide 50).
```

### Slide 47 — METH.6: Quality Gate G2
Same CRAFT structure as Slide 44, adapted to Phase 2 → Phase 3 criteria. RASHAD INVOCATION: R-322, R-345, R-347 (transformation progress review).

### Slide 48 — METH.7: Phase 3 Deep-Dive

```
<role> You are the lead for Phase 3, showing how the methodology winds down operationally while winding up client independence. </role>
<context> Phase 3 (Deepen / Knowledge Transfer / Sustainability). Inputs: second-cohort logic, KT plan, post-graduation follow-up, independence test. </context>
<thinking_instructions>
Step 1. STATE the GOAL (operational independence by month N).
Step 2. DESIGN the METHODOLOGICAL APPROACH: second cohorts use accumulated reputation and data; formal KT follows Kirkpatrick L1-L4 sequentially; post-graduation follow-up as a contractual deliverable; independence test in final months.
Step 3. LIST activities, deliverables, frameworks.
</thinking_instructions>
<task> Produce the Phase 3 deep-dive. </task>
<methodology> Frameworks: Kirkpatrick L1-L4, PROSCI CCMP, WIPO GII, GALI Post-Program, Theory of Change. </methodology>
<output_format> Same 7-field structure as Slide 33; approach emphasizes wind-down plus independence. </output_format>
<quality_standard> A reader sees independence is tested and proven, not assumed. </quality_standard>
<anti_hallucination_guard> Independence metrics labeled; commitments deliverable-backed. </anti_hallucination_guard>
RASHAD INVOCATION: R-E03 (governance transition), R-377 (KT and SOP delivery), R-E10 (value realisation), R-274 (talent transformation), R-373 (graduate GTM if K-scope) | CHAIN: ties to sustainability (Slide 15) and value (Slide 50).
```

### Slide 49 — METH.8: Timeline (Gantt)

```
<role> You are a planning lead rendering all tracks across all months in one Gantt. </role>
<context> Single-slide Gantt with phases, gates, deliverable codes. Inputs: duration, tracks, deliverable target months. </context>
<thinking_instructions>
Step 1. LAY OUT tracks as rows, months as columns.
Step 2. PLACE deliverable codes in their target cells.
Step 3. MARK Phase 0 pre-column, phase boundaries, G1/G2.
</thinking_instructions>
<task> Produce the Gantt slide. </task>
<methodology> Dense and immediately readable; ongoing tracks marked with continuous bars. </methodology>
<output_format> Title; grid (track rows × month columns); deliverable codes in cells; phase boundaries and gate markers. </output_format>
<quality_standard> A reader can trace any deliverable to its month and any month to its active tracks. </quality_standard>
<anti_hallucination_guard> Dates consistent with the deliverables map. </anti_hallucination_guard>
RASHAD INVOCATION: R-E04 (30-60-90-180 milestones), R-149 (strategic milestones), R-311 (roadmap) | CHAIN: milestones feed monitoring (Slide 55).
```

### Slide 50 — METH.9: Impact Measurement Framework (full)

```
<role> You are an impact lead presenting the full Theory of Change framework that Slide 11 introduced. </role>
<context> Formal home of the 4-tier impact framework, each KPI fully specified. Inputs: same as Slide 11 plus deliverable codes. </context>
<thinking_instructions>
Step 1. WALK the causal chain explicitly.
Step 2. For each tier, give every KPI a target number, a deliverable code, a framework, a cadence (R-E10).
</thinking_instructions>
<task> Produce the full impact framework. </task>
<methodology> Fuller than Slide 11: each KPI gets target + deliverable + framework. </methodology>
<output_format> (1) 60 to 90 word framing naming Theory of Change and the causal chain. (2) Four tiers (L1 to L4) each with 3 to 4 KPIs (target, deliverable code, framework, cadence). </output_format>
<quality_standard> Every promised outcome is measurable, dated, framework-anchored, and deliverable-linked. </quality_standard>
<anti_hallucination_guard> Targets labeled Assumption unless committed. </anti_hallucination_guard>
RASHAD INVOCATION: R-E10 (value realisation), R-369 (innovation impact if K-scope), R-336 (value tracking), R-344 (metrics system) | CHAIN: consistent with Slide 11; KPIs reported in Slide 55.
```

### Slides 51 to 52 — METH.10: Complete Deliverables Map

```
<role> You are a delivery controller producing the canonical deliverables reference table. </role>
<context> 1 to 2 dense tables listing all deliverables. Every other slide's deliverable codes point here. Inputs: all deliverables. </context>
<thinking_instructions>
Step 1. LIST every deliverable in code order.
Step 2. For each: track, phase, target date, acceptance criterion (binary), framework.
Step 3. CHECK consistency with every phase deep-dive and the BOQ.
</thinking_instructions>
<task> Produce the deliverables map. </task>
<methodology> Acceptance criterion is a checkable binary statement. </methodology>
<output_format> 1 or 2 tables: Code / name / track / phase / target date / acceptance criterion / framework; 14 to 15 rows per slide. </output_format>
<quality_standard> Any deliverable code anywhere in the proposal resolves to a row here with a checkable criterion. </quality_standard>
<anti_hallucination_guard> Cross-checked against deep-dives and BOQ; no orphan codes. </anti_hallucination_guard>
RASHAD INVOCATION: R-E04 (milestone tracking), R-311 (roadmap) | CHAIN: priced in Slides 72 to 74; gated in Slides 44, 47.
```

---

## PART 6 — Section 4: Delivery Model and Governance (Slides 53 to 61)

### Slide 53 — Section Divider
Use Template A. Subsections: Three-tier governance, RACI, Risk (ISO 31000), QA (ISO 9001), Escalation. RASHAD INVOCATION: R-264, R-E05.

### Slide 54 — GOV.1: Three-Tier Governance

```
<role> You are a governance designer distributing decision rights across three tiers. </role>
<context> Strategic / Tactical / Operational governance with authority scope and cadence. Inputs: client and Rubix roles, scope. </context>
<thinking_instructions>
Step 1. NAME the failure mode of single-level governance.
Step 2. DEFINE three tiers: body, members, decision rights, cadence.
Step 3. Confirm escalation logic between tiers.
</thinking_instructions>
<task> Produce the three-tier governance slide. </task>
<methodology> Each tier resolves its scope and escalates only beyond it. </methodology>
<output_format> (1) 50 to 70 word framing. (2) Three tier blocks (Strategic / Tactical / Operational), each: body name, members, 4 to 7 decision rights, cadence. </output_format>
<quality_standard> A reader sees exactly who decides what and why bottlenecks will not form at the top. </quality_standard>
<anti_hallucination_guard> Named members real; [verify] otherwise. </anti_hallucination_guard>
RASHAD INVOCATION: R-264 (governance structure), R-043 (who decides what), R-E05 (PMO governance protocol) | CHAIN: roles feed RACI (Slides 56 to 57) and escalation (Slide 61).
```

### Slide 55 — GOV.1b: Meeting and Monitoring Mechanisms

```
<role> You are a PMO lead formalizing the meeting cadence. </role>
<context> Weekly / monthly / quarterly mechanisms. Inputs: governance tiers from Slide 54. </context>
<thinking_instructions>
Step 1. DEFINE each cadence: attendees, agenda, output document.
</thinking_instructions>
<task> Produce the monitoring mechanisms slide. </task>
<methodology> Each meeting produces a named output document. </methodology>
<output_format> Three blocks (Weekly / Monthly / Quarterly), each: meeting name, attendees, agenda topics, output document. </output_format>
<quality_standard> A reader sees a disciplined operating rhythm with documented outputs. </quality_standard>
<anti_hallucination_guard> Consistent with Slide 54. </anti_hallucination_guard>
RASHAD INVOCATION: R-E04 (milestone tracking), R-E09 (communication cadence), R-318 (quarterly strategic review) | CHAIN: ties to Gantt (Slide 49).
```

### Slides 56 to 57 — GOV.2: RACI Matrix

```
<role> You are a delivery controller allocating responsibility for every deliverable and decision. </role>
<context> Full RACI across deliverables and governance decisions. Inputs: deliverables map, role list. </context>
<thinking_instructions>
Step 1. LIST deliverables and decisions as rows.
Step 2. ASSIGN R/A/C/I per role column; exactly one A per row.
Step 3. GROUP rows under phase headers.
</thinking_instructions>
<task> Produce the RACI matrix slides. </task>
<methodology> One Accountable per row. Cover critical governance decisions (G1, G2, scope change, L4 approval). </methodology>
<output_format> (1) 30 to 50 word framing. (2) R/A/C/I legend. (3) 1 to 2 tables grouped by phase: rows = deliverables/decisions; columns = 5 to 8 roles; cells = R/A/C/I. </output_format>
<quality_standard> No deliverable or decision lacks a single accountable owner. </quality_standard>
<anti_hallucination_guard> Roles consistent with Slide 54; deliverables consistent with map. </anti_hallucination_guard>
RASHAD INVOCATION: R-043 (who decides what), R-264 (governance), R-317 (accountability framework) | CHAIN: governance decisions reference gates (Slides 44, 47).
```

### Slides 58 to 59 — GOV.3: Risk Management (ISO 31000) [REPEATABLE × 2]

```
<role> You are a risk lead running a proactive, pre-loaded risk process, not a worst-case archive. </role>
<context> 5 to 8 named risks, each with probability, impact, mitigation, response, early warning. Inputs: scope-specific risks. </context>
<thinking_instructions>
Step 1. IDENTIFY 5 to 8 scope-specific risks (R-313, R-046, R-287).
Step 2. For each: probability + rationale, impact, mitigation tied to a deliverable/gate, response procedure, quantified early-warning indicator.
Step 3. Confirm each risk has a pre-assigned treatment (avoid/mitigate/accept/transfer).
</thinking_instructions>
<task> Produce the risk register slides. </task>
<methodology> Risks scope-driven, not generic. Early-warning indicators quantified. </methodology>
<output_format> (1) 40 to 60 word framing on continuous proactive risk management and the four treatments. (2) 5 to 8 risk cards: name (specific failure mode), probability + rationale, impact, mitigation (deliverable-linked), response, quantified early-warning. (3) Closing line: register is live, updated weekly, summarized each quarter, auto-escalated per Section 5.5. </output_format>
<quality_standard> Each risk has a pre-defined response that triggers on a measurable signal, before the risk materializes. </quality_standard>
<anti_hallucination_guard> Probabilities labeled Logical Inference or Assumption; no false precision. </anti_hallucination_guard>
RASHAD INVOCATION: R-313 (risk mitigation plan), R-046 (business model vulnerabilities), R-287 (operational risks), R-E07 (real-time implementation risk), R-296 (risk management framework) | CHAIN: register summarized in quarterly reports (Slide 50 L2) and escalation (Slide 61).
```

### Slide 60 — GOV.4: Quality Assurance (ISO 9001)

```
<role> You are a QA lead ensuring every deliverable arrives ready to approve, not ready to debate. </role>
<context> Internal 6-step quality cycle plus two quality criteria sets. Inputs: deliverable types, QA roles. </context>
<thinking_instructions>
Step 1. STATE the principle (protect client review time).
Step 2. DEFINE the 6-step cycle (production, internal review, PD review, delivery, client review SLA, formal approval).
Step 3. DEFINE quality criteria for documentary vs operational deliverables.
</thinking_instructions>
<task> Produce the QA slide. </task>
<methodology> SLA: 7 working days first comments, 3 days second, then silent acceptance. </methodology>
<output_format> (1) 40 to 60 word framing. (2) 6-step cycle. (3) Two criteria sets side-by-side (documentary: complete, accurate-sourced, consistent, actionable, documented; operational: SOP-compliant, KPI ≥85%, NPS ≥80%, logged, OTD ≥95%). </output_format>
<quality_standard> A reader sees errors are caught internally so client meetings approve, not correct. </quality_standard>
<anti_hallucination_guard> SLA and thresholds stated as commitments only if contractually held. </anti_hallucination_guard>
RASHAD INVOCATION: R-289 (quality management system), R-E04 (milestone tracking), R-345 (decision quality) | CHAIN: SOP count ties to sustainability (Slide 15).
```

### Slide 61 — GOV.5: Escalation Mechanisms

```
<role> You are a delivery governor defining when issues stay vs escalate, with binding time windows. </role>
<context> Four escalation levels with triggers and SLAs. Inputs: governance tiers. </context>
<thinking_instructions>
Step 1. STATE the failure mode (authority ambiguity causes delay).
Step 2. DEFINE four levels: trigger, handler, response SLA, resolution SLA.
</thinking_instructions>
<task> Produce the escalation slide. </task>
<methodology> Binding time windows per level. </methodology>
<output_format> (1) 30 to 50 word framing. (2) Four levels (Operational / Tactical / Strategic / Exceptional), each: trigger, handler, response time, resolution time. </output_format>
<quality_standard> A reader sees no issue can stall in ambiguity; each has an owner and a clock. </quality_standard>
<anti_hallucination_guard> SLAs consistent with QA (Slide 60) and governance (Slide 54). </anti_hallucination_guard>
RASHAD INVOCATION: R-309 (manage resistance), R-E07 (real-time risk), R-043 (who decides what) | CHAIN: ties to risk auto-escalation (Slides 58 to 59).
```

---

## PART 7 — Section 5: Capabilities and Institutional Experience (Slides 62 to 70)

### Slide 62 — Section Divider
Use Template A. Subsections: Institutional assets, Team structure, Team profiles, Reference portfolio, Hero cases. RASHAD INVOCATION: R-166.

### Slide 63 — CAP.1: Institutional Assets and Tools

```
<role> You are a capabilities lead inventorying assets that are already in production, not roadmapped. </role>
<context> 4 to 6 asset cards proving the client funds a deployment, not a build. Inputs: archetype, Rubix asset catalog. </context>
<thinking_instructions>
Step 1. SELECT 4 to 6 assets that map to scope from the catalog (SparkThon OS, BIMLens, YANA, iVision, KitchenEyes, WellB, Sulhafa, WorCare, AI Pulse Cairo, Rubix Excavation USA, Rubix Connect).
Step 2. For each: what it is, who has used it, where hosted, what it produces for THIS engagement, status tags.
</thinking_instructions>
<task> Produce the institutional assets slide. </task>
<methodology> Each asset card makes substitution by a generic alternative impossible. </methodology>
<output_format> (1) 50 to 70 word framing (assets in production, deployment not build). (2) 4 to 6 cards: name + category, 60 to 90 word description, "What it produces for this project" (3 to 5 outputs), 3 to 5 status tags. </output_format>
<quality_standard> A reader concludes Rubix brings operational capacity, not promises. </quality_standard>
<anti_hallucination_guard> Asset claims real; [verify] usage numbers; engineered-for vs in-production distinguished. </anti_hallucination_guard>
RASHAD INVOCATION: R-135 (core capabilities), R-081 (competitive moat) | CHAIN: assets recur in Why Rubix (Slide 13) and platform showcase (Slides 37 to 43).
```

### Slide 64 — CAP.2: Team Structure and Roles

```
<role> You are an org designer presenting the engagement team as a clear reporting structure. </role>
<context> Lightweight org diagram. Inputs: team size, roles, named leads. </context>
<thinking_instructions>
Step 1. PLACE CEO sponsor, Program Director, and 6 to 10 functional leads.
Step 2. For each lead, a one-line scope naming owned tracks/deliverables.
</thinking_instructions>
<task> Produce the team structure slide. </task>
<methodology> Roles adapt to scope (e.g. enterprise architect for digital, strategy partner for strategy). </methodology>
<output_format> Org diagram: CEO sponsor top, Program Director, then 6 to 10 leads each with role and one-line scope. </output_format>
<quality_standard> A reader sees a complete, scope-fit team with clear ownership. </quality_standard>
<anti_hallucination_guard> Named individuals real; roles match actual capability. </anti_hallucination_guard>
RASHAD INVOCATION: R-244 (org structure), R-043 (who decides what) | CHAIN: leads detailed in Slides 65 to 66 and CVs in Slides 79 to 85.
```

### Slides 65 to 66 — CAP.3: Detailed Team Profiles [REPEATABLE × 4 to 8 leads]

```
<role> You are a talent lead presenting why each named lead is the right person for this specific scope. </role>
<context> 3 to 4 profiles per slide. Inputs: name, role, years, dedication, prior relevant work, certifications. </context>
<thinking_instructions>
Step 1. WRITE a scope-relevant bio (not generic).
Step 2. LIST certifications.
Step 3. CITE 2 to 3 prior projects that map to this scope.
Step 4. STATE the role in this project (owned deliverables).
</thinking_instructions>
<task> Produce one team profile card. </task>
<methodology> Each profile answers: why this person for this scope? </methodology>
<output_format> Header (name, role, "N+ years, full-time"); BIO (30 to 50 words); CERTIFICATIONS (3 to 4); RELEVANT PROJECTS (2 to 3 bullets, real); ROLE IN THIS PROJECT (owned deliverables). </output_format>
<quality_standard> Each profile justifies the person against the scope, not in the abstract. </quality_standard>
<anti_hallucination_guard> Career facts real; [verify] otherwise; no invented projects. </anti_hallucination_guard>
RASHAD INVOCATION: R-135 (core capabilities), R-147 (capability gap) | CHAIN: full CVs at Slides 79 to 85.
```

### Slides 67 to 69 — CAP.4: Reference Project Portfolio

```
<role> You are an engagement historian presenting the full track record with a relevance line on every project. </role>
<context> 20 to 30 row project table across 2 to 3 slides. Inputs: project list with clients, categories, outputs, years. </context>
<thinking_instructions>
Step 1. ASSEMBLE the portfolio with real clients (or generalized category if confidential).
Step 2. For each, write a non-generic relevance line.
Step 3. OMIT any project whose relevance is weak rather than including with vague relevance.
Step 4. ADD 5 hero stats summarizing the portfolio.
</thinking_instructions>
<task> Produce the portfolio block. </task>
<methodology> Every row has a specific relevance line. </methodology>
<output_format> (1) 5 hero stats on slide 1. (2) Table: # / project + client / category / description and outputs (1 to 2 sentences) / relevance (1 specific sentence) / year. 14 to 15 rows per slide. </output_format>
<quality_standard> Every project visibly connects to this scope; none is filler. </quality_standard>
<anti_hallucination_guard> Real clients or honest generalization; values [verify] if uncertain. </anti_hallucination_guard>
RASHAD INVOCATION: R-109 (benchmark), R-027 (cross-industry solutions) | CHAIN: top 3 expanded at Slide 70.
```

### Slide 70 — CAP.5: Most Relevant Cases (3 hero precedents)

```
<role> You are an engagement partner presenting three detailed precedents that cover the scope's pillars. </role>
<context> Full-detail versions of the three cases from Slide 14. Inputs: case context, approach, result, relevance. </context>
<thinking_instructions>
Step 1. For each case: Challenge, Approach (methodology-rich), Result (quantified), Relevance (deliverable-level).
Step 2. Confirm the three cover the scope's primary pillars.
</thinking_instructions>
<task> Produce three full hero cases. </task>
<methodology> Approach names specific frameworks and sequences; Relevance ties to specific deliverable codes. </methodology>
<output_format> Three cards: TITLE (project + client + contract type + duration); CHALLENGE (40 to 60 words); APPROACH (40 to 60 words, methodology-rich); RESULT (30 to 50 words, quantified); RELEVANCE (30 to 50 words, deliverable-linked). </output_format>
<quality_standard> The three cases together answer "where have you done exactly this?" with proof. </quality_standard>
<anti_hallucination_guard> Real cases; values [verify] if uncertain; honest relevance bridges. </anti_hallucination_guard>
RASHAD INVOCATION: R-027 (cross-industry), R-109 (benchmark), R-226 (investment thesis logic for PPP cases) | CHAIN: consistent with Slide 14 light versions.
```

---

## PART 8 — Section 6: Financial Proposal (Slides 71 to 76)

### Slide 71 — Section Divider
Use Template A. Subsections: BOQ, Assumptions, Exclusions. RASHAD INVOCATION: R-181, R-194.

### Slides 72 to 74 — FIN.1: BOQ Pricing Table

```
<role> You are a commercial lead pricing every deliverable transparently and traceably. </role>
<context> Full Bill of Quantities, 1 to 3 slides. Inputs: deliverables, Rubix cost model, VAT rate. </context>
<thinking_instructions>
Step 1. PRICE each deliverable from the cost model.
Step 2. COMPUTE subtotal, VAT, total.
Step 3. WRITE totals in formal Arabic words where applicable.
</thinking_instructions>
<task> Produce the BOQ table. </task>
<methodology> Every line maps to a deliverable; pricing from the cost model, never invented. </methodology>
<output_format> Table: D# / deliverable name (verbatim per RFP) / unit / quantity / unit price SAR / total SAR / total in words. Footer: subtotal, VAT 15%, total inclusive, total in words. </output_format>
<quality_standard> Every riyal traces to a deliverable the client verifies before payment. </quality_standard>
<anti_hallucination_guard> Pricing [price: provide from cost model] if absent; never fabricate figures. </anti_hallucination_guard>
RASHAD INVOCATION: R-181 (business case structure), R-194 (cost-benefit), R-185 (cost structure model) | CHAIN: line items map to deliverables (Slides 51 to 52).
```

### Slide 75 — FIN.2: Pricing Assumptions

```
<role> You are a commercial lead naming the operational assumptions pricing depends on. </role>
<context> Four assumption categories. Inputs: scope, delivery model. </context>
<thinking_instructions>
Step 1. STATE that material changes reopen pricing fairly.
Step 2. LIST assumptions in four categories: Location/Infrastructure, Operational Cooperation, Scope/Deliverables, Recruitment/Participation.
</thinking_instructions>
<task> Produce the assumptions slide. </task>
<methodology> Assumptions concrete and checkable; each protects against a specific commercial risk. </methodology>
<output_format> (1) 30 to 50 word framing. (2) Four categories, each with 3 to 5 specific assumptions. </output_format>
<quality_standard> A reader sees the commercial basis is explicit and fair to both sides. </quality_standard>
<anti_hallucination_guard> Assumptions match the delivery model and exclusions. </anti_hallucination_guard>
RASHAD INVOCATION: R-006 (scope), R-338 (articulate trade-offs), R-218 (financial risk register) | CHAIN: ties to exclusions (Slide 76) and change process (Slide 61).
```

### Slide 76 — FIN.3: Exclusions

```
<role> You are a commercial lead making out-of-scope items explicit to prevent disputes. </role>
<context> 8 to 10 exclusions plus a change-order closing line. Inputs: scope, deliverables. </context>
<thinking_instructions>
Step 1. LIST 8 to 10 exclusions with 30 to 40 word explanations.
Step 2. CLOSE with the change-order mechanism.
</thinking_instructions>
<task> Produce the exclusions slide. </task>
<methodology> Exclusions scope-adapted; closing line points to Section 5.5 change process. </methodology>
<output_format> (1) 30 to 50 word framing. (2) 8 to 10 exclusion items, each 30 to 40 words. (3) Closing line: anything not in deliverables and not excluded is handled via Change Order, repriced and approved before execution. </output_format>
<quality_standard> A reader sees no hidden scope; the commercial perimeter is unambiguous. </quality_standard>
<anti_hallucination_guard> Exclusions consistent with deliverables and assumptions. </anti_hallucination_guard>
RASHAD INVOCATION: R-006 (scope boundary), R-338 (trade-offs) | CHAIN: ties to assumptions (Slide 75) and escalation (Slide 61).
```

---

## PART 9 — Section 7: Appendices (Slides 77 to 125)

### Slide 77 — Section Divider for Appendices
Use Template A. Subsections: Implementation Team, Case Studies, Official Documents. RASHAD INVOCATION: none.

### Slide 78 — Appendix 1 Cover: Implementation Team
Mini-cover with 1 to 2 sentence framing. RASHAD INVOCATION: none.

### Slides 79 to 85 — APP.1: Full Team CVs [REPEATABLE × N members]

```
<role> You are a CV writer producing a substantive one-pager per team member. </role>
<context> Full CV per member. Inputs: name, role, education, certifications, career history. </context>
<thinking_instructions>
Step 1. WRITE the bio with the scope-relevant depth and quantified outcomes.
Step 2. LIST education and certifications with institutions and years.
Step 3. DETAIL 5 to 8 career roles, each with a quantified outcome.
</thinking_instructions>
<task> Produce one full CV slide. </task>
<methodology> Real career data only; every role has at least one quantified outcome. </methodology>
<output_format> Header (name, role); Qualifications and Certifications list; Bio (90 to 130 words); Professional Experience (5 to 8 roles, each title/employer/dates + 30 to 50 word description with a number). </output_format>
<quality_standard> A reader sees a credible, quantified career arc relevant to the engagement. </quality_standard>
<anti_hallucination_guard> Never invent credentials, employers, or outcomes; [verify] uncertain items. </anti_hallucination_guard>
RASHAD INVOCATION: none (HR content) | CHAIN: summarized in Slides 65 to 66.
```

### Slide 86 — Appendix 2 Cover: Case Studies
Mini-cover. RASHAD INVOCATION: none.

### Slides 87 to 112 — APP.2: Full Case Studies [REPEATABLE × N projects]

```
<role> You are a case-study writer producing a full one-slide study per reference project. </role>
<context> One slide per project. Inputs: client, duration, context, scope of work, deliverables, impact. </context>
<thinking_instructions>
Step 1. WRITE the project context (operating environment, why Rubix was engaged).
Step 2. LIST scope of work, key deliverables, achieved impact.
Step 3. Use real entity names or honest generalization if confidential.
</thinking_instructions>
<task> Produce one full case study slide. </task>
<methodology> Quantified impact where possible; never fabricate. </methodology>
<output_format> Header (project number, eyebrow); client + duration; PROJECT CONTEXT (80 to 130 words); SCOPE OF WORK (5 to 8 bullets, action-led); KEY DELIVERABLES (5 to 8 bullets, named outputs); ACHIEVED IMPACT (5 to 8 bullets, quantified); bottom navigation strip of all N studies. </output_format>
<quality_standard> Each study reads as a real, verifiable engagement with concrete outcomes. </quality_standard>
<anti_hallucination_guard> Real client and details; [verify] values; generalize honestly if confidential. </anti_hallucination_guard>
RASHAD INVOCATION: R-109 (benchmark), R-239 (value creation framing) | CHAIN: hero subset surfaced in Slides 14 and 70.
```

### Slide 113 — Appendix 3 Cover: Official Documents and Certificates
Mini-cover. RASHAD INVOCATION: none.

### Slides 114 to 124 — APP.3: Official Documents and Certificates [REPEATABLE × N documents]

```
<role> You are a compliance archivist presenting official Rubix documents. </role>
<context> One slide per document (CR, VAT, ISO, accreditations, awards). Inputs: document name, image, issuer, validity. </context>
<thinking_instructions>
Step 1. NAME the document and what it attests.
Step 2. STATE issuer and validity.
</thinking_instructions>
<task> Produce one certificate slide. </task>
<methodology> Real documents only. </methodology>
<output_format> Title strip; document name; 1 to 3 line description (what it attests, issuer, validity). </output_format>
<quality_standard> Each document visibly supports a compliance or credibility claim made earlier. </quality_standard>
<anti_hallucination_guard> Real documents; [verify] validity dates. </anti_hallucination_guard>
RASHAD INVOCATION: none | CHAIN: supports compliance matrix (Slide 4).
```

### Slide 125 — Closing Slide

```
<role> You are a proposal closer producing a single confident line. </role>
<context> Clean closer. Inputs: proposal posture. </context>
<task> Produce a one-line closing statement (default: "Ready from day one." in the proposal language). </task>
<output_format> One line, no body. </output_format>
<quality_standard> Confident, brief, no eagerness. </quality_standard>
<anti_hallucination_guard> none. </anti_hallucination_guard>
RASHAD INVOCATION: none | CHAIN: none.
```

---

## PART 10 — Master Rules and Operating Checklist

### 10.1 Before generating any slide
1. Read the scope brief completely.
2. Run the Two-Tier Scope Selector: Tier-1 archetype (phase backbone + framework menu) and Tier-2 Rashad scope code(s).
3. Pull the Tier-2 scope's 6-phase prompt sequence from the Rashad Master Reference Matrix.
4. Map the 6 consulting phases onto the project phases (Part 0.3).
5. Pre-decide deliverable count (20 to 30), phase count (3 to 4 + Phase 0), track count (3 to 6), gate count (2 to 3).
6. Decide which Rubix assets are scope-relevant.
7. Load the Saudi/GCC localization hooks for the dominant scope (Part 0.5).

### 10.2 During generation
- Each slide is a complete CRAFT execution, not a placeholder.
- The slide's CRAFT prompt produces the visual deliverable; the invoked R-codes produce the underlying analysis.
- Every framework named in formal designation.
- Every claim quantified or anchored; anti-hallucination labels applied in working notes; unsourced figures [verify].
- No em-dashes/en-dashes; no begging language; no Big Four naming.
- Arabic-first for Saudi government; bilingual only when scope requires.
- Apply the Human-Voice Layer (Part 0.8) to every slide's prose before finalizing.

### 10.2a Human edit pass (mandatory before delivery)
No prompt fully replaces a human read. Before the proposal is delivered, the operator reads the generated text (Arabic aloud) and rewrites by hand any sentence that reads as translated, templated, or generic. Ten minutes of partner-level editing per section does more than any humanization rule, and it confirms genuine authorship of the deliverable. Where past winning Rubix proposals exist, anchor voice to them (Part 0.8) rather than relying on the generic layer alone.

### 10.3 Non-negotiable prompts (must appear somewhere)
Confirm all eight are invoked: R-001 (Slides 5, 7), R-006 (Slides 4, 7), R-011 (Slide 4), R-301 (Slides 6 to 17), R-313 (Slides 58 to 59), R-304 (Slides 8, 49), R-E04 (Slides 49, 55), R-E10 (Slides 11, 50).

### 10.4 After generating the full set
- Deliverables map (Slides 51 to 52) consistent with every phase deep-dive and the BOQ.
- Quality gates reference real deliverables.
- RACI covers all deliverables and decisions; one Accountable per row.
- Impact KPIs consistent between Slide 11 and Slide 50.
- Hero cases consistent between Slide 14 and Slide 70.
- Every invoked R-code chained correctly (R-001 reframe flows to all Diagnose/Analyse slides).
- Anti-hallucination pass: no Assumption rendered as a committed number; no unsourced figure unmarked.

### 10.5 Adaptive scaling
- Small proposal (10 to 15 slides): keep architecture, compress. Front matter 2; exec summary becomes the whole proposal 5 to 8; methodology 3 to 5; governance/capabilities/financial 1 to 2 each; appendix 0 to 2.
- Large proposal (60 to 100 slides): expand each section proportionally; architecture stays.

### 10.6 Versioning
Each Rashad cross-reference is valid against the Rashad Master Document version loaded in the project. If Rashad is renumbered or extended, re-verify the R-code references. Stamp the pairing in the chat (e.g. "skeleton v2 paired with Rashad v2026.04").

---

**End of master skeleton v2.**

This document and the Rashad Master Document are designed to be loaded together in the `rubix-deck` project. This document governs the slide architecture and CRAFT prompts; Rashad governs the underlying analytical prompts invoked per slide. Together they form the complete Rubix proposal generation system.
