# Rashad v6.2 — Skill Remediation Change Register

**Date:** 2026-08-13  
**Base:** Rashad Proposal OS v6.1 Execution-Proof Consulting Exhibit Lock  
**New:** Rashad Proposal OS v6.2 Skill Authority & Reference Integrity Lock

## Scope
This release fixes the **Skill/package layer only**. It does not modify the Streamlit/OpenAI application code or the external QA runtime.

## Why v6.2 exists
The audits found that the knowledge corpus is strong but active retrieval could still surface legacy modules claiming HIGHEST CURRENT authority, old concept-count rules, a 7.2MB prompt monolith, and asset claims that were stronger than the package contents. v6.2 resolves those package-level ambiguities without deleting lineage.

## Changes
- Added one v6.2 Active Authority Registry and machine-readable Active Authority Manifest.
- Added Retrieval Exclusion Registry; the 7.2MB prompt master remains preserved but is bulk-retrieval excluded.
- Rebuilt the compact always-on context to remove V4/V5/current-route contamination.
- Converted legacy Active Runtime START_HERE into a compatibility redirect; original body preserved under provenance snapshots.
- Added path-qualified authority identity rule; duplicate numeric prefixes no longer act as authority IDs.
- Locked critical analytical pages to **exactly five materially distinct hypotheses**.
- Added FULL_RUNTIME vs ADVISORY capability modes to prevent capability deadlock or fake release.
- Added explicit Producer ≠ Judge truth to the Skill layer.
- Added font asset contract; no font binaries are claimed or bundled.
- Corrected icon-language truth: the package ships no SVG icon binaries; the SVG pipeline remains the standard.
- Added machine-readable `tokens.json` / `tokens.css` derived from the current Rubix palette.
- Added external appendix/company-evidence readiness contract.
- Added asset inventories and explicit code-remediation boundary.

## Non-destructive result
- Files removed from v6.1: **0**.
- Existing files modified: **18**.
- New files before final reports/manifest regeneration: **22**.
- Protected prompt/scopes/mappings and current Rubix PNG assets remain byte-for-byte unchanged.


## v6.2.1 successor note
This v6.2 register is historical. Independent red-team review found residual legacy-reactivation and mode-binding gaps; see `V6_2_1_SKILL_HARDENING_CHANGE_REGISTER.md`.
