MODULE:
CONTEXT_LOADING_PROTOCOL

STATUS:
AUTHORITATIVE

LOAD WHEN:
Every user request (as the recipe selector); engagement init; Continue; Summary; section work; appendix matching; visual generation; QA.

DEPENDS ON:
00_START_HERE
01_RASHAD_CORE
02_AUTHORITY_AND_DECISIONS
03_ENGAGEMENT_RESET_AND_SOURCE_GROUNDING
ENGAGEMENT_STATE (when resuming)

DO NOT APPLY TO:
Dumping entire project sources “to be safe”; paraphrasing all 388 prompts into context; attaching Chatgpt Context.md as runtime knowledge.

SUPERSEDES:
Maximal context packing; full-corpus loads; embedding/vector “retrieve everything” approaches for Rashad exact prompts.

CLASSIFICATION:
Reusable retrieval protocol. **Current RFP files** are loaded per engagement; reusable modules are loaded by recipe; evidence library is loaded by match caps only.

---

# Context Loading Protocol

## Optimization target

```text
HIGH FIDELITY
+ HIGH RETRIEVABILITY
+ LOW CONTAMINATION
+ CLEAR AUTHORITY
+ PORTABILITY
+ CONSISTENT CONSULTING QUALITY
```

Do not optimize for smallest possible context.  
Do not optimize for maximal context size.

## Hard never-load rules

Never automatically load:

| Forbidden | Why |
|---|---|
| Full chat / historical chat provenance (see `10_PROVENANCE/ENGINEERING_HISTORY.md`) as runtime authority | KF-010; contamination; non-selective |
| All 388 R-codes | Exact bodies only by selective R-code / block index |
| All 96 scopes | Load the active scope(s) only |
| Entire evidence / CV / case / cert library | Cap matched candidates; show gaps |
| All historical engagements | Cross-engagement contamination |
| Historical skills / obsolete SKILL packages as active authority | KF-009 |
| Global Golden MWAN as generation authority | Gate removed; evaluation-only when explicit |
| Benchmark scores / expected verdicts in generation context | Benchmark isolation |
| CEO Letter / Commercial / unrelated section prompts | Unless that section is in scope |
| All proposal examples | Load classified references only when needed |

Proof pattern from Phase 2+3 retrieval sample for one RFP Summary request:

- R-codes retrieved: **3** (not 388)  
- Scopes: **1**  
- Evidence objects: capped appendix hits (not full library)  
- `full_chat_context_loaded = false`  
- `all_388_r_codes_loaded = false`

## Authority layers (keep separate in assembly)

1. **Project Instructions** — how to behave  
2. **RASHAD_PROJECT_SOURCES modules** — what Rashad knows (reusable)  
3. **Current RFP pack** — what is true for this engagement  
4. **Reusable Rubix evidence indexes** — candidate proof assets (not automatic truth)  
5. **ENGAGEMENT_STATE** — what is already done/approved  

## Deterministic recipes

### Recipe: RFP Summary

**User request example:** “Give me the RFP Summary.”

**LOAD:**

```text
00_START_HERE
01_RASHAD_CORE
03_ENGAGEMENT_RESET_AND_SOURCE_GROUNDING
04_LANGUAGE_RTL_LTR_NUMERALS
05_RFP_INGESTION
06_RFP_SUMMARY
09_COUNCILS_AND_ROLES
10_ARTIFACT_ENGINE
11_ARTIFACT_FAMILIES
16_QA_AND_RELEASE_GATES
18_USER_INTERACTION_AND_NEXT_SECTION
20_CONTEXT_LOADING_PROTOCOL
CURRENT_RFP_SOURCES (full active pack inventory, selective page extracts)
derived ClarificationWindowState
selective R-codes for Summary (e.g. R-001 family as mapped — never all 388)
```

**DO NOT LOAD:**

```text
all historical engagements
all CVs / all cases / all certs
CEO Letter prompts
Commercial section
all proposal examples
Chatgpt Context.md
benchmark evaluation baselines into generation
```

Optional capped evidence: readiness gaps / team requirement match slice only.

### Recipe: Continue / next section

**LOAD:**

```text
ENGAGEMENT_STATE
18_USER_INTERACTION_AND_NEXT_SECTION
07_PROPOSAL_WORKFLOW
08_FINAL_PROPOSAL_SKELETON (dependency map)
section-specific module + matched R-codes
CURRENT_RFP evidence slice for that section
16_QA_AND_RELEASE_GATES
```

### Recipe: Team / appendix readiness

**LOAD:**

```text
17_APPENDIX_AND_EVIDENCE
EVIDENCE/EVIDENCE_INDEX
EVIDENCE/TEAM_INDEX and/or CASE_STUDY_INDEX and/or CERTIFICATION_INDEX (as needed)
CURRENT_RFP team/document requirements
08 appendix gates A0–A1 first
```

**DO NOT LOAD:** entire PDF binaries into prompt; load index rows + selected page locators.

### Recipe: Visual / artifact page

**LOAD:**

```text
10_ARTIFACT_ENGINE
11_ARTIFACT_FAMILIES
12_STORYTELLING_AND_VISUAL_INTELLIGENCE
13_RUBIX_DECK_AND_BRAND
14_IMAGE_GENERATION_POLICY / 15_IMAGE_BATCH_AND_PHASE_POLICY (if images)
04_LANGUAGE_RTL_LTR_NUMERALS
16_QA_AND_RELEASE_GATES
19_FAILURE_PATTERNS
approved page/artifact contract for this engagement
```

**DO NOT LOAD:** unrelated section content; evaluation benchmark scores.

### Recipe: Release candidate

**LOAD:**

```text
16_QA_AND_RELEASE_GATES
19_FAILURE_PATTERNS
relevant brand/language/geometry contracts
appendix A3 if appendix in pack
parity rules if PDF/PPTX
```

### Recipe: Fresh engagement init

**LOAD:**

```text
00_START_HERE
03_ENGAGEMENT_RESET_AND_SOURCE_GROUNDING
05_RFP_INGESTION
CURRENT_RFP_SOURCES only for the new client
empty/new ENGAGEMENT_STATE
```

Hard fail if prior client facts remain in working state.

## Benchmark isolation in loading

| Context | Allowed |
|---|---|
| GENERATION_CONTEXT | RFP facts, selected prompts, councils, artifact vocabulary, derived clarification window — **no** dimension_scores / expected_verdict / human evaluator scores / quality_targets as generation targets |
| EVALUATION_CONTEXT | Generated output + optional human-approved baseline for independent parity — post-generation only |

```text
benchmark_context_leakage = 0
```

## Derived clarification window in loading

Always compute/attach `ClarificationWindowState` from pack evidence when Summary or clarifications are in scope. Do not load a stale boolean as authority.

Precedence: verified addendum → verified pack deadline → verified tender metadata → `UNKNOWN`.

## Module metadata contract

Every source module begins with:

```text
MODULE:
STATUS:
LOAD WHEN:
DEPENDS ON:
DO NOT APPLY TO:
SUPERSEDES:
```

Use metadata for retrieval; do not load modules whose LOAD WHEN does not match the request.

## Image batch loading note

If user requests a large visual set (e.g. 28 pages), plan phases (e.g. 1–20 then 21–28) and run QA between phases — do not load all image briefs and all section prompts at once without phase gates.

## Source paths

| Path | Role |
|---|---|
| `_forensic_work\master_prompt_extract.txt` (§48–§50, §58, §60) | Architecture, recipes, migration test |
| `EXTERNAL_ENGAGEMENT_DEPENDENCY::SOURCE_INVENTORY_AND_FILE_GUIDE.md` | What is engagement-local vs bundled |
