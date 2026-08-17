# v6.2 Open Code Defect Boundary — Deliberately Not Fixed Here

**STATUS: CODE REMEDIATION PENDING**

The Skill package must not claim that the following application/runtime defects are fixed. They were identified by the 2026-08-13 code audit and belong to the later code-remediation phase:

## P0
1. Release gate may consume producer Artifact Truth / fail to enforce independent score ownership.
2. Anti-gaming attacks A22/A23 were tautological and did not exercise the release gate.
3. Source coverage can vacuously report COMPLETE when evidence-indexed count is zero.

## P1 / major runtime issues
4. Mock multimodal critic path can drop the visual payload, preventing normal CEQS progression.
5. Re-ingesting identical bytes can corrupt a valid source record / self-reference duplicate state.
6. Stale proof invalidation is not fully hash-enforced.
7. Judge-model tier configuration/independence needs runtime verification and explicit policy.
8. State-journal load trust requires hard validation.

## Verification still pending
- Live OpenAI API smoke test.
- Live image API verification.
- Full post-CEQS QA reachability.
- External QA folder re-audit/integration.
- Six-page Gold Pilot certification.

v6.2 fixes Skill authority/reference truth only; these items remain release blockers until code remediation and re-audit.
