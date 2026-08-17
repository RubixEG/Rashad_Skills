# Rashad Consulting Brain Runtime v3.5 — bound to Skill v7.3

This runtime converts the Skill constitution into executable deliberation while preserving the protected knowledge corpus.

## Execution modes
`HOST_NATIVE_MODE | API_PROVIDER_MODE | OFFLINE_VALIDATION_MODE` are first-class runtime states. `AUTO` prefers an injected host bridge, then a configured API provider, then Offline.

### Host-Native
For ChatGPT/Claude/approved model hosts, `HostNativeProvider` accepts a synchronous host callback and `HostNativeResponseBundleProvider` supports staged continuation when the host cannot expose a callback. No external API key is required. Responses are bound to exact request/input hashes, host session IDs and unique response IDs. Missing responses are `HOST_NATIVE_PENDING`, never fake PASS.

### API
`OpenAIResponsesProvider` remains available when credentials/model are configured. Missing configuration fails closed.

### Offline
Offline validation can ingest, route, validate schemas, run deterministic QA and emit forensic logs, but cannot claim council cognition, Artifact production, pixel QA or user-visible delivery.

## Core chain
`Sources → Grounded Blackboard → execution-mode resolution → Producer → executable Expert Council → Constitutional Councils → Cognitive Lock → Artifact Intelligence → Visual Search → Art Direction → Production Readiness → Production Render → Actual-Pixel QA → Repair → Exact-File Delivery → Release Chair`

## Independence truth
Host-native judges are isolated host contexts and may support user-visible draft quality when all production/pixel/delivery gates pass. They are not labeled externally independent. `RELEASED` remains stricter and requires externally independent judge/release evidence plus parity/proof requirements.

## No fallback
A missing external API key inside a model-capable host is not a reason to create Markdown-only output or a generic cards PPTX. The Host-Native bridge must be attempted first. If no valid cognition path exists, fail closed with exact pending/block logs.

## v7.3 production organ
The runtime now owns `PageCompositionSpec → structurally divergent hypotheses → art direction/imagery → instrumented HTML/SVG composer → Playwright/Chromium production render → semantic-master QA → actual-product geometry/pixel QA → repair → continuity → exact handoff`. A strategy label without a measurable composition has no production authority.
