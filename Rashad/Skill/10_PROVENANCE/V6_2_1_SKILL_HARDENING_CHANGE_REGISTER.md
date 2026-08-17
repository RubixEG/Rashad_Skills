# Rashad v6.2.1 — Skill Hardening Change Register

**Date:** 2026-08-14  
**Base:** v6.2 Skill Authority & Reference Integrity Lock  
**Scope:** Skill/package only; application code and external QA runtime untouched.

## Independent red-team findings closed
- Updated stale root `VERSION.md` from v6.1 to v6.2.1.
- Neutralized and globally excluded V5 `47` and V5 `62` live authority/reactivation paths.
- Marked historical `23_VISUAL_PRODUCTION_POLICY_LATEST` as non-current and excluded it from global retrieval.
- Bannered/excluded remaining verified 3–4/3–5 legacy concept-count modules.
- Made root `ACTIVE_AUTHORITY_MANIFEST.json` the sole machine global-routing source of truth.
- Added authority binding/drift sidecar plus startup mismatch blocking contract.
- Replaced numeric shorthand in startup/current authority graph with exact paths.
- Bound FULL_RUNTIME to exact capability-preflight authority and schema-valid mode evidence.
- Added mandatory visible + filename `DRAFT — NOT RELEASED` marking for ADVISORY exports.
- Removed critical-page rendered-candidate exemption loophole.
- Unified current Artifact Truth release floor to ≥90 in CEQS/current V6 workflow.
- Restored explicit prompt-injection firewall in Current Authority Graph.
- Added long-session page/section/resume re-anchoring.
- Completed missing semantic 8% color tokens.
- Formalized Arabic-Indic numeral authority over historical golden-reference digit styling.
- Recorded golden exemplars, playbook enrichment, external evidence and runtime/QA work as explicit backlog rather than silently dropping them.

## Non-destructive doctrine
Protected prompt shards, scopes, mappings and current Rubix PNG binaries are not modified by this patch. Legacy files are preserved; conflicting directives are bannered/excluded rather than deleted.
