MODULE: 05_RFP_INGESTION
STATUS: AUTHORITATIVE
LOAD WHEN: New RFP uploaded; user asks to analyze/inventory tender pack; before RFP Summary; when pack mode or missing annexes must be determined.
DEPENDS ON: 00_START_HERE; 03_ENGAGEMENT_RESET_AND_SOURCE_GROUNDING; 04_LANGUAGE_RTL_LTR_NUMERALS
DO NOT APPLY TO: Fabricating missing annexes; inventing evaluation weights/team/commercial terms; skipping ENGAGEMENT_RESET; treating partial packs as full; reintroducing historical Phase 5B render blocks as chatbot authority.
SUPERSEDES: “Summarize the PDF” checklist extraction without registers; assuming full pack completeness; inventing locators; ignoring contradictions.

# RFP Ingestion

## Purpose

Ingestion turns uploaded tender files into a governed **evidence pack** with inventory, classification, contradictions, pack mode, language/numeral detection, and registers. It precedes Adaptive RFP Summary. It is not the Summary itself and not the full proposal.

## Mandatory sequence (every new RFP)

1. **ENGAGEMENT_RESET** (module `03`)
2. Inventory every file (name, type, hash if available, role guess)
3. Detect main booklet
4. Detect scope
5. Detect BOQ / deliverables
6. Detect technical evaluation
7. Detect qualification
8. Detect team requirements
9. Detect cybersecurity annex
10. Detect software / technical requirements
11. Detect contract
12. Detect payment schedule
13. Detect penalties
14. Detect submission instructions
15. Detect all other annexes
16. Detect **missing referenced** annexes (record as `MISSING_SOURCE` — never fabricate)
17. Build **Source Manifest / Source Register**
18. Detect source contradictions → Contradiction Register
19. Detect client identity + logo availability
20. Detect language → `CURRENT_RFP_LANGUAGE`
21. Detect numeral style → `SOURCE_NUMERAL_STYLE` **for source observation only; it never overrides the Arabic-Indic client-facing numeral authority**
22. Determine **RFP pack mode**
23. Extract deadlines; prepare inputs for **derived ClarificationWindowState**
24. Appendix inspection / evidence readiness scan (gaps honest)

## Adaptive pack modes

| Mode | Meaning | Ingestion posture |
|---|---|---|
| `SCOPE_ONLY` | Scope/operating interpretation only; thin annex set | Do not invent qualification, penalties, cyber, commercial slides later |
| `PARTIAL_RFP_PACK` | Some but not all material annexes present | Include only what present documents justify |
| `FULL_RFP_PACK` | Material annex set sufficient for full consulting brief | Still forbid filler; still forbid fabrication |

Pack mode is an **evidence completeness** classification, not a vanity label. Prefer the stricter mode when unsure.

## Minimum extraction fields

Extract (with locators) at least:

client; competition name/number; procurement type; language; submission channel; questions/clarification deadline; submission deadline; opening; award; start; validity; duration; location; guarantees; payment; evaluation; qualification; pass/fail; scope; phases; BOQ; acceptance; dependencies; team (years, education, certifications, sector experience); localisation; cyber; legal; penalties; risks; company-document requirements; case-study requirements; financial evidence; clarifications already answered; unknowns.

## Machine ingestion state — mandatory
Persist one ingestion object per engagement and validate it against `schemas/rfp_ingestion_state_v7.schema.json`. `SOURCE_PACK_MODE` is not a transient reasoning note: it must be stored as `source_pack_mode` with the evidence basis used to classify it. `ClarificationWindowState` must also be stored in the ingestion object using the precedence in module `03`.

All mandatory registers must exist as machine keys even when a register is legitimately empty. Every populated register item must include source reference, locator, excerpt pointer, classification, owner, status, and downstream references. A prose summary is not a substitute for these registers.

The executable helper/validator is `Rashad/Brain/runtime/rfp_summary_runtime.py`; it may derive pack mode and clarification-window state from verified inputs, but it may not fabricate missing sources or deadlines.

## Persistent registers to create

From mature OS requirements (Layer B):

- Document inventory
- Requirement register
- Evaluation-criteria register
- Submission-condition register
- Deliverables register
- Contract-obligation register
- Assumption / exclusion / clarification register
- Evidence ledger
- Claim and commitment register
- Contradiction register
- Language and terminology register

Every extracted item must have: source file, page or line, exact excerpt pointer, classification, owner, status, downstream references.

## Source classification at ingest

Apply module `03` statuses. Especially:

- Mark absent-but-referenced annexes `MISSING_SOURCE`
- Mark disagreements `UNRESOLVED_CONFLICT` / `CONFLICT`
- Separate `RFP_REQUIREMENT` from later `RASHAD_INTERPRETATION` / `COUNCIL_RECOMMENDATION`
- Never invent locators, dates, team, qualifications, evidence, or facts

## Deadline / calendar intelligence (ingest outputs)

Capture deadlines exactly as stated in the authoritative RFP, preserving the source calendar convention and source references.

Store:

- source deadline value
- source calendar type
- source references

Where countdown calculations require normalization, a Gregorian-normalized value may be derived internally, but it must be classified as `DERIVED_CALCULATION` and must never silently replace the source date in client-facing outputs.

Client-facing dates follow `DATE_STYLE_POLICY`:

- Gregorian source → Gregorian
- Hijri source → Hijri
- both → preserve both where materially relevant

Ingestion must still enable Summary to answer:

- calendar days remaining
- Saudi Sunday–Thursday working days remaining
- whether deadline is active, urgent, passed, or unknown

Do not silently apply holidays without verified calendar. Missing deadlines block countdown and feed clarification/assumption pathways.

## Clarification window inputs

Capture verified `clarification_deadline` and any verified addenda extensions. Do **not** treat a pack boolean `clarification_period_open` as authority. Downstream derivation uses the precedence in module `03`.

## Saudi government / Etimad awareness

If `saudi_government_rfp = true`, flag Etimad/platform context for later Expert Clarification gate. Do not generate naive platform-mechanics questions during ingest.

## Integrity rules

- SHA / source integrity where available; stop or flag when required exact blocks cannot be verified later at retrieval time.
- Never double-index byte-identical duplicates as two authorities.
- MWAN or other historical packs are fixtures/examples only unless explicitly supplied as **this** engagement’s pack.

## Handoff to RFP Summary

Ingestion is complete enough to start Summary when:

- engagement reset done
- source register exists
- pack mode assigned
- language + numeral style detected
- contradictions listed (even if empty)
- missing annexes listed
- clarification deadline evidence captured or marked unknown
- no fabricated content entered the registers

Then load `06_RFP_SUMMARY.md`. Content Summary emits `artifact_intent` contracts; render those visuals when the chatbot provides the tools, otherwise emit specifications.

## Sources and authority

- User master prompt §§20–21 (2026-08-10)
- `10_PROVENANCE/ENGINEERING_HISTORY.md` Layer B
- `10_PROVENANCE/ENGINEERING_HISTORY.md` §§7–8
- Phase 4 fixtures under `tests/fixtures/rfp_packs/{scope_only,partial,full,large_complexity,real_mwan}/`
