# V7.2 — Host-Native RFP Summary Execution Workflow

**STATUS: CURRENT RFP SUMMARY HOST-EXECUTION OVERLAY**

This workflow overlays the current decision workflow and Artifact delivery workflow. It does not replace the canonical 24-role logic.

## Mode preflight
Before Step 06 Cognitive Packets:
1. Resolve `HOST_NATIVE_MODE | API_PROVIDER_MODE | OFFLINE_VALIDATION_MODE`.
2. Record resolution in the execution trace.
3. If the current environment is a model-capable host, use `HOST_NATIVE_MODE`; absence of `OPENAI_API_KEY` is not a reason to enter Offline mode.
4. If Host-Native responses are pending, expose the exact pending invocation contracts and pause; do not mark downstream stages as executed.

## Host-Native cognitive phases
For all applicable analytical roles:
- Phase H1 — Producer requests;
- Phase H2 — routed SME / Executive / Evaluator / Governor requests;
- Phase H3 — constitutional Council requests and Meta-Cognition coverage;
- Phase H4 — Cognitive Lock validation.

The host may batch independent requests within a phase, but each actor/context must retain a unique invocation proof.

## Artifact phases
- Phase A1 — Pre-Concept Artifact Councils;
- Phase A2 — five materially different communication strategies + internal renders;
- Phase A3 — independent initial visual critiques;
- Phase A4 — Top-2 refinements + independent critique;
- Phase A5 — final concept selection;
- Phase A6 — Art Direction Councils;
- Phase A7 — Production Readiness Councils;
- Phase A8 — real `PRODUCTION_PAGE_RENDER`;
- Phase A9 — actual-pixel QA / repair loop;
- Phase A10 — deck-level product QA + exact-file Delivery Dossier.

Concept renders are internal-only. Host-native cognition does not weaken the no-generic-fallback law.

## Debug trace requirement
Every run must persist:
- selected execution mode and reason;
- requested/routed actors;
- executed actors and invocation IDs;
- pending host-native requests;
- Cognitive Packet hashes;
- Artifact strategy/search/selection hashes;
- production render hashes;
- pixel QA verdicts and repair rounds;
- exact output file hash and Delivery Gate verdict.

A failure must name its first blocking stage and must never be rewritten as a later-stage failure.
