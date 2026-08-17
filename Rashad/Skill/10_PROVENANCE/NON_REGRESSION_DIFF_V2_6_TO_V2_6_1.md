# Non-Regression Diff — v2.6 → v2.6.1

## Purpose
Verify that the English-rule normalization revision is non-destructive and limited to the Chat Mirror language layer.

## Result
- Baseline files excluding Manifest: **832**
- v2.6.1 files excluding Manifest before this report/validation regeneration: **833**
- Unchanged baseline files: **828**
- Modified baseline files: **4**
- Added files at comparison point: **1**
- Removed baseline files: **0**
- Protected prompt/scope/mapping/brand files checked: **588**
- Protected files changed: **0**

## Modified baseline files
- `00_CHAT_MIRROR_KERNEL/00_RASHAD_BOOTSTRAP.md`
- `00_CHAT_MIRROR_KERNEL/13_OWNER_DECISION_LEDGER.md`
- `00_CHAT_MIRROR_KERNEL/14_COMPILED_ALWAYS_ON_CONTEXT.md`
- `VERSION.md`

## Added files at comparison point
- `10_PROVENANCE/CHAT_MIRROR_LANGUAGE_NORMALIZATION_AUDIT_2026-08-11.md`

## Removed files
None.

## Verdict
**PASS — NON-DESTRUCTIVE LANGUAGE NORMALIZATION.**
