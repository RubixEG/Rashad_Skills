# 43 — Production Renderer Reference Architecture

STATUS: IMPLEMENTATION BLUEPRINT — KNOWLEDGE AUTHORITY — v2.6.4.2

## Purpose
Describe the executable renderer that should implement Rashad's production contracts. This file is an implementation specification, not executable code.

## Recommended runtime structure
`rashad-renderer/`
- `schemas/` — page_spec, artifact_spec, geometry_spec, scene_graph contracts
- `layout/` — direction resolver, geometry engine, collision detector, text fit, connector routing, topology
- `renderers/` — HTML, PDF, PPTX adapters consuming the same resolved scene graph
- `qa/` — overflow, typography, direction, topology, brand, visual regression, parity
- `assets/` — verified runtime asset registry
- `tests/` — unit/integration/regression tests
- `golden_baselines/` — approved renderer regression baselines

## Six implementation milestones
1. Canonical Page Scene Graph.
2. Deterministic Geometry + Text Fit + Directional RTL/LTR.
3. Artifact Topology Validator.
4. HTML/PDF/PPTX adapters from the same Scene Graph.
5. Screenshot/raster-based Visual Regression.
6. Golden Test Suite + CI/Release Gate.

## Separation of duties
- Renderer builds the candidate.
- Independent QA validates the final pixels/structure.
- The same component must not be allowed to self-attest without independent evidence for critical release checks.

## Compiler invariant
The renderer executes the locked specification. It does not make new consulting decisions.
