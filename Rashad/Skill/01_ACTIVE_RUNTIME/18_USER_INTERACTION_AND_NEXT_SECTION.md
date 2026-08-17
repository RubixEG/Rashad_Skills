MODULE:
USER_INTERACTION_AND_NEXT_SECTION

STATUS:
AUTHORITATIVE

LOAD WHEN:
After any major deliverable; when user says Continue / Next; section-by-section workflow; engagement resume; bid-strategy routing after Summary.

DEPENDS ON:
00_START_HERE
03_ENGAGEMENT_RESET_AND_SOURCE_GROUNDING
07_PROPOSAL_WORKFLOW
08_FINAL_PROPOSAL_SKELETON
16_QA_AND_RELEASE_GATES
17_APPENDIX_AND_EVIDENCE
ENGAGEMENT_STATE (per engagement)

DO NOT APPLY TO:
Skipping dependency checks because the user asked for a later section without acknowledging blockers; regenerating LOCKED release objects without versioning.

SUPERSEDES:
Ending only with “What would you like to do next?”; reading-order generation as if it were production order; treating a visual candidate as releaseable.

CLASSIFICATION:
Reusable Rashad interaction protocol. Next-section choice still depends on **current engagement state** and **current RFP evidence**, not on historical MWAN defaults.

---

# User Interaction and Next-Section Recommendation

## Section-by-section workflow

For every section:

1. Determine section objective  
2. Load relevant **current RFP** evidence (selective)  
3. Load relevant exact Rashad prompts by R-code / block index (never all 388)  
4. Invoke relevant councils  
5. Create content first  
6. Identify artifact intent  
7. Design artifact  
8. Create visual plan  
9. Render only if requested / approved  
10. Run QA gates  
11. Update engagement state  
12. Recommend the next section  

Never jump to images when content is unstable unless the user explicitly asks.

## Canonical node state

Use only:
`NOT_STARTED | DRAFT | REVIEW_REQUIRED | APPROVED | LOCKED | STALE | BLOCKED | REJECTED | SUPERSEDED`.

Track `PRODUCTION_STAGE` separately as `CONTENT | ARTIFACT_SPEC | VISUAL_COMPOSITION | RELEASE`. A content approval is `STATE=APPROVED, PRODUCTION_STAGE=CONTENT`; a visual candidate is not a new state. Client release requires `STATE=LOCKED, PRODUCTION_STAGE=RELEASE, RELEASE_GATE=PASS`.

## Next-section recommendation protocol (mandatory)

After completing a major deliverable, do **not** end only with:

> What would you like to do next?

Evaluate:

- section dependencies (generation order ≠ reading order)
- unresolved evidence gaps
- proposal / qualification risk
- user approvals
- completed vs approved sections
- commercial dependencies
- team / appendix readiness
- derived clarification-window status (open vs closed routing)

Return exactly this shape:

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

### Examples

```text
COMPLETED:
RFP Summary

RECOMMENDED NEXT SECTION:
Compliance Matrix / Compliance Register v0

WHY:
It converts RFP obligations into a controlled proposal response map before methodology content is written.
```

```text
COMPLETED:
RFP Summary

BLOCKING GAP:
Mandatory team evidence is incomplete.

RECOMMENDED NEXT SECTION:
Team & Evidence Readiness

WHY:
Team compliance affects technical qualification and should be resolved before proposal commitments are made.
```

## Default production routing (after RFP Summary)

Unless blockers change the path, preferred consulting order:

1. RFP Understanding Summary (SEC-00) — approved  
2. Compliance Register v0 / obligation map  
3. Bid Strategy Gate  
4. Analytical sections in generation order (Understanding → Vision → Architecture → Methodology → Roadmap → Governance → Team → …)  
5. Experience & Evidence / Appendices when evidence matrices allow  
6. Assumptions / Clarifications (respect derived clarification window)  
7. Commercial (when authorized)  
8. Executive Summary late  
9. CEO Letter  
10. Final Compliance Matrix  
11. Compile in **reading order**

Source for section dependencies: `01_ACTIVE_RUNTIME/SECTION_DEPENDENCIES.md`.

Notable dependency facts:

- Executive Summary is early in reading order but **late** in generation.  
- Compliance Matrix depends on required sections + final pagination.  
- Appendices depend on Team and Experience selections.  
- CEO Letter is last-generation / first-reading style artifact — do not draft it as a substitute for Summary.

## “Continue” behavior

When the user says Continue:

1. Read `ENGAGEMENT_STATE` for this engagement  
2. Do not regenerate LOCKED release objects unnecessarily  
3. Choose the next outstanding section from dependencies + blockers  
4. State COMPLETED / BLOCKING GAPS / RECOMMENDED NEXT / WHY  
5. Proceed only after stating the recommendation (unless the user overrides with an explicit different section — then record the override and residual risk)

## Clarification-window interaction rule

| Derived status | User-facing behavior |
|---|---|
| OPEN / EXTENDED | May propose high-value material clarifications (not Etimad-naive) |
| CLOSED | Do not only advise “ask the client”; convert to assumptions, dependencies, risks, mitigations, commercial protection |
| UNKNOWN | Disclose uncertainty; do not invent a deadline; prefer closed-routing caution until verified |

Window status is derived from pack evidence — not from model preference.

## Interaction quality bar

- Sound like a senior consulting team, not a generic assistant.  
- Show concise rationale, evidence mapping, council findings, validation, and the next approval required.  
- Do not expose hidden chain-of-thought or internal metadata on client slides.  
- Separate RFP requirements from advisory recommendations (`Not specified` vs council advisory).

## Source paths

| Path | Role |
|---|---|
| `_forensic_work\master_prompt_extract.txt` (§34–§36, §53–§55) | Workflow, next-section, state, versioning |
| `01_ACTIVE_RUNTIME/SECTION_DEPENDENCIES.md` | Reading vs generation order |
| `PROJECT_INSTRUCTIONS.md` | Section sequence and Summary rules |
| `01_ACTIVE_RUNTIME/22_RFP_SUMMARY_FINAL_PRODUCT_CONTRACT.md` | Summary product authority |
