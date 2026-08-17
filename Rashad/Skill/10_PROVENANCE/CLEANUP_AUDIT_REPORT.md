# HISTORICAL CLEANUP AUDIT — SUPERSEDED BY COUNCIL_AUDIT_2026-08-11_V2

# Cleanup Audit Report

## Source archive

- Source: `New Rashad(3).7z`
- Archive size on disk: approximately 491 MB
- Entries scanned: **2,190**
- Uncompressed entry size: **688.8 MB**
- Exact duplicate hash groups: **425**
- Duplicate copies beyond first: **1,039**
- Reclaimable bytes from exact duplicates alone: **52.7 MB**

## Source file-type counts

- `.md`: 787
- `.json`: 462
- `<none>`: 331
- `.py`: 176
- `.png`: 130
- `.pdf`: 82
- `.pyc`: 74
- `.html`: 39
- `.txt`: 28
- `.svg`: 27
- `.pptx`: 17
- `.zip`: 13
- `.ttf`: 8
- `.css`: 3
- `.skill`: 3
- `.ini`: 2
- `.tag`: 1
- `.log`: 1
- `.jpg`: 1
- `.8_artifact_safe_full`: 1
- `.0_18_files_exact`: 1
- `.4`: 1
- `.7_recreated_attachments`: 1
- `.4_recreated_files`: 1


## Removed from the final runtime package

- all `.py` and `.pyc` files;
- all JSON runtime/state/fixture files;
- HTML/CSS render outputs and test fixtures;
- `.pytest_cache`, `__pycache__`, logs, INI/config debris;
- generated `engagements/` run outputs and duplicated runtime/report trees;
- old renderer implementation directories and production-proof code;
- duplicate `RASHAD_CHATBOT_*`, `RASHAD_COMPLETE_DELIVERY` copies where the same Markdown already exists once;
- obsolete skill versions and migration prompts once their active rules were captured in the final authority;
- duplicate Artifact Engine v1 copies;
- raw `Chatgpt Context.md` from production/runtime context;
- historical MWAN/other HTML/PPTX generations and completion reports as active authority;
- historical proposal corpus from the runtime skill package to prevent cross-client contamination (use it externally/on-demand if needed).

## Kept

- one copy of active operational Markdown modules;
- exact Rashad prompt corpus;
- current proposal skeleton authorities;
- current Artifact Engine / reasoning / workflow / service-line knowledge;
- current councils / QA gates;
- latest risk & clarification correction;
- current Rubix brand guide/device authority;
- appendix evidence PDFs/images and evidence indexes;
- distilled decision/supersession/cleanup provenance.

## Why the raw ChatGPT context is not included

It was read and used to reconstruct chronology and accepted/rejected decisions, but including the full transcript in production would reintroduce superseded instructions, rejected outputs, temporary workarounds, and conflicting versions. `FINAL_DECISION_LEDGER.md` is the safe distilled replacement.
