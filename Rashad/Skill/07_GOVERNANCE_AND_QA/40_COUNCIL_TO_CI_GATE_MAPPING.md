# Council-to-CI Gate Mapping

STATUS: PRODUCTION GOVERNANCE MAPPING — v2.6.4.2

## Principle
Council judgments remain responsible for consulting/semantic quality. Machine-verifiable production rules should also become deterministic CI/build gates in the executable renderer.

## Conceptual gate mapping
- Schema/Page Spec tests → GATE_DEFINED
- Scene Graph identity tests → GATE_DEFINED
- Layout/boundary/collision tests → GATE_DEFINED
- Text Fit tests → GATE_DEFINED
- Font Preflight tests → GATE_DEFINED
- RTL/Bidi tests → GATE_DEFINED
- Directional Structural tests → GATE_DEFINED
- Topology node/edge tests → GATE_DEFINED
- Asset/hash tests → GATE_DEFINED
- Brand/co-brand tests → GATE_DEFINED
- Golden Regression → GATE_DEFINED
- HTML parity → GATE_DEFINED when required
- PDF parity → GATE_DEFINED when required
- PPTX parity → GATE_DEFINED when required

Any hard blocker fails the build/release candidate.

## Governance boundary
A written knowledge file does not execute CI. The actual renderer/runtime must produce the evidence before a machine PASS may be recorded.


## v2.6.4.3 truthfulness rule
This file defines gates; it does not prove they ran. All conceptual statuses are `GATE_DEFINED`. Runtime `PASS` is permitted only with execution evidence and an `evidence_id` under `42_EVIDENCE_BACKED_GATE_STATUS_TAXONOMY.md`.
