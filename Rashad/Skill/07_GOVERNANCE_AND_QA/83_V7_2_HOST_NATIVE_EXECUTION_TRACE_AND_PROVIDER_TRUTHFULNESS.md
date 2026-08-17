# V7.2 — Host-Native Execution Trace & Provider Truthfulness QA Law

**STATUS: CURRENT GLOBAL QA / TRACE AUTHORITY**


## Execution-mode identity lock
The exact current execution-mode identifiers are `HOST_NATIVE_MODE`, `API_PROVIDER_MODE`, and `OFFLINE_VALIDATION_MODE`. A chat-host run with a model-capable host must resolve to `HOST_NATIVE_MODE` when the host bridge/response bundle is available; absence of an internal Python API key alone is never evidence that cognition is unavailable.

## Required provider QA
Current certification must attack at least:
- Host-Native `PASS` with no proof;
- wrong request key or input binding;
- wrong host session;
- replayed host response ID;
- fake provider/source label;
- independent judge without isolated-context proof;
- host bundle entry for a different input;
- Host-Native mode with no bridge silently falling back to API/test/offline cognition;
- fabricated Cognitive Lock session with fake host proof;
- QA Host-Native response without independent-context proof;
- API mode without configuration pretending to execute;
- Offline mode claiming council/Artifact/QA execution.

## Runtime trace truth
`NOT_EXECUTED`, `HOST_NATIVE_PENDING`, `BLOCKED`, `PASS`, `QA_CANDIDATE_PASS`, and `RELEASED` are distinct states. Logs may never collapse them into a generic success/failure label.

## Product behavior
A model-capable chat host must not return Markdown-only merely because the internal Python process lacks an API key. It must first use the Host-Native bridge. Markdown/source-grounded output is the correct terminal behavior only when the user requested content-only output or when both Host-Native and API cognition are genuinely unavailable/declined.

## Release truth
Host-Native isolated review may support user-visible draft quality. It does not automatically satisfy externally independent production release requirements. Framework tests never substitute for current-engagement pixel/product proof.
