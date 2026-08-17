# V7.2 — Host-Native Execution & Provider-Mode Law

**STATUS: CURRENT GLOBAL RUNTIME EXECUTION AUTHORITY**

## Purpose
Rashad must not confuse “Python runtime has no API key” with “the host model cannot execute cognition.” When Rashad runs inside a model-capable host such as ChatGPT, Claude, Codex-like orchestration, or another approved model host, the host itself may execute routed councils/SMEs through the Host-Native bridge.

## Canonical execution modes
Exactly one cognition mode is active per execution boundary:

1. `HOST_NATIVE_MODE`
   - The surrounding host model executes Producer / SME / Executive / Evaluator / Governor / Artifact / QA invocations.
   - No external API key is required.
   - Every invocation must be isolated and return `RASHAD_HOST_NATIVE_RESPONSE_V1` proof bound to the exact `request_key`, `input_hash`, `host_session_id`, and a unique `host_response_id`.
   - A role that is only registered/routed but lacks an accepted host-native response is **NOT EXECUTED**.

2. `API_PROVIDER_MODE`
   - A configured external provider executes isolated invocations.
   - Missing credentials/model configuration fails closed; there is no silent test/fallback provider.

3. `OFFLINE_VALIDATION_MODE`
   - Used only when neither a Host-Native bridge nor an API provider is available, or when explicitly requested.
   - May perform deterministic ingestion, routing, source-grounded content preparation, schemas, audits, and logs.
   - May not claim cognitive council execution, Artifact production, actual-pixel QA, or user-visible Artifact delivery.

`AUTO` resolves in this order: injected Host-Native bridge → configured API provider → Offline Validation.

## Host-Native is execution, not a label
A Host-Native `PASS` has zero authority unless the runtime validates:
- exact request key;
- exact host session;
- source = `HOST_NATIVE_MODEL_EXECUTION`;
- unique host response ID;
- invocation function/council/input-hash binding;
- isolated actor/context identities;
- independent-context proof for judges/Release Chair.

Fake status strings, copied response IDs, wrong request hashes, response replay, cross-session bundles, and producer/judge chaining are hard blocks.

## Chat-host continuation protocol
A host that cannot expose a synchronous callback uses `HostNativeResponseBundleProvider`:

`Runtime emits pending invocation contracts → host executes those contracts → host returns response bundle → runtime replays and re-validates → next phase continues.`

Missing bundle entries return `HOST_NATIVE_PENDING`; they do not degrade to `OFFLINE_VALIDATION_MODE`, API calls, scripted answers, cards, or a generic PPTX.

## Independence boundary
Host-Native isolated judges may approve `USER_VISIBLE_ARTIFACT_DRAFT` quality when all production/pixel/delivery gates pass. They are marked `HOST_ISOLATED_CONTEXT`, not external independence. Production `RELEASED` remains stricter and requires externally independent judgment / release evidence according to the Release Authority.

## Mandatory chain
For analytical artifact work:

`execution-mode resolution → knowledge readiness → expert routing → Producer → executable SME/Executive/Evaluator/Governor ledger → constitutional councils → Cognitive Lock → Artifact councils → communication search → visual judgment → Art Direction → production readiness → production render → actual-pixel QA → repair closure → exact-file delivery`.

No stage may infer execution from the existence of a role, rule, route, title, or `PASS` string.
