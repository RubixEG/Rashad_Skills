MODULE:
FAILURE_PATTERNS

STATUS:
AUTHORITATIVE (prevention library)

LOAD WHEN:
QA planning; Red Team; release review; after any regression; when designing artifacts, images, brand, RTL, or context assembly; onboarding a fresh chat to avoid known collapse modes.

DEPENDS ON:
16_QA_AND_RELEASE_GATES
10_ARTIFACT_ENGINE
13_RUBIX_DECK_AND_BRAND
03_ENGAGEMENT_RESET_AND_SOURCE_GROUNDING
20_CONTEXT_LOADING_PROTOCOL

DO NOT APPLY TO:
Copying historical failure outputs into a live client proposal as content; treating bad references as current facts.

SUPERSEDES:
Ad-hoc “be careful” reminders without a named failure ID and prevention gate.

CLASSIFICATION:
Reusable anti-pattern library. Historical examples are **BAD_REFERENCE / STYLE_ONLY** learning assets — never current RFP truth.

---

# Failure Patterns Library

Bad historical outputs are valuable when the **why** is recorded. Classify examples:

```text
GOLDEN_REFERENCE | GOOD_REFERENCE | BAD_REFERENCE | STYLE_ONLY
```

Never allow historical examples to become current client facts.

## Canonical failure catalog (KF)


| ID | Symptom | Root cause | Prevention gate / fix |
|---|---|---|---|
| KF-001 | Generic-card fallback | Layout pressure | `generic_artifact_fallbacks=0`; fail closed + artifact replan |
| KF-002 | Wrong/old logo or unequal logo height | Brand asset mishandling | `logo_signature_violations=0`; normalized Rubix\|Client height |
| KF-003 | Black / near-black background | Default dark aesthetics | `near_black_forbidden`; prepress F12 |
| KF-004 | Arabic RTL reversal / LTR numbering | CSS/DOM order inference | `rtl_order_violations=0`; physical coordinate sequence |
| KF-005 | Old client leakage (e.g. MWAN into other RFP) | No engagement reset | Cross-engagement contamination hard fail |
| KF-006 | Image model changes text/numbers | Image used as factual authority | Native text overlays; image creative only |
| KF-007 | PPTX differs from approved visual | Image-to-elements inference | Spec-First Native Twin + zone parity |
| KF-008 | Safety shortens/weakens output | Safety redesign of meaning | Artifact lock; strength delta ≥ 0; Safety cannot change family |
| KF-009 | Duplicate/old skill authorities simultaneous | Multiple SKILL/packages | Single active authority pointer |
| KF-010 | Prompt context too large | Full chat/transcript load | Selective retrieval; never full chat / all 388 / all evidence |
| KF-011 | Invented facts / missing evidence | Generation without lineage | Claim→evidence→source; show MISSING |
| KF-012 | Default Office master / wrong fonts | Missing deck shell | Current deck mandatory; font substitution gate |

## Additional historical failure reasons (master prompt)

Record and reject:

- wrong client  
- wrong logo  
- old deck  
- wrong language  
- LTR Arabic  
- generic cards  
- artifact simplification  
- overflow  
- default PowerPoint  
- poor image text  
- English contamination  
- fake numbers  
- missing semantic nodes  

## Recurring collapse narrative (forensic)

Strong consulting logic repeatedly degraded at render time:

1. Pages became generic cards  
2. Layout “fixes” destroyed semantic relationships  
3. Brand/deck mismatches  
4. Arabic ordered sequences started from the left  
5. Historical decks/clients leaked into new engagements  
6. Strong MWAN outputs risked becoming a false **global** golden baseline  

Global Golden MWAN gate is **REMOVED**. Use Current Engagement Baseline / temporary engagement baseline only when explicitly supplied.

## Context-loading failures

Forbidden assembly modes (hard fail):

```text
full_chat_context_loaded = true
all_388_r_codes_loaded = true
all_96_scopes_loaded = true
all_evidence_library_loaded = true
historical_skill_runtime_dependency = true
Chatgpt Context.md as runtime authority = true
```

Correct pattern: selective repositories + budgeted assembly + retrieval trace.

## Benchmark isolation failures

Failure: leaking evaluation scores / expected verdicts / human baseline scores into Stage A/B/Council/Repair generation prompts.

```text
benchmark_context_leakage must remain 0
```

Generation pack must strip benchmark-only keys. Evaluation context is separate and post-generation.

## Clarification-window failures

Failure: model or engagement boolean decides whether the clarification period is open.

Correct: derive from verified addenda / pack deadlines / tender metadata; otherwise `UNKNOWN`. Closed window uses assumption/dependency/risk routing — not “just ask on Etimad.”

Failure: Etimad-naive clarifications (“how do I submit”, “what is the tender number”) presented as high-value questions.

## Evidence honesty failures

- Treating certificate presence as current validity  
- Ignoring CV role conflicts across external team/evidence sources  
- Using templated case text as verified experience  
- Promoting `NOT_EXTRACTED` clients to named verified clients  
- Loading the entire appendix library “just in case”

## Image / language failures

If image generation introduces English text or malformed Arabic on an Arabic engagement:

```text
DO NOT ACCEPT THE IMAGE AS A RELEASE ARTIFACT
```

Regenerate text-free imagery or overlay native text. Image model never owns language/numeral/RTL authority.

## How to use this library in QA

For each release candidate, scan KF-001…KF-012 and confirm prevention gates. Any CRITICAL severity hit blocks release.

## Source paths

| Path | Role |
|---|---|
| `_forensic_work\master_prompt_extract.txt` (§47, §59) | Historical failure classes + Arabic image test |
| `03_ARTIFACT_ENGINE/20_ARTIFACT_STRENGTH_NON_REGRESSION_AUTHORITY.md` | Artifact-before-Safety policy |
| `01_ACTIVE_RUNTIME/58_DO_NOT_COPY_AND_CONTAMINATION_RULES.md` | Contamination rules |
