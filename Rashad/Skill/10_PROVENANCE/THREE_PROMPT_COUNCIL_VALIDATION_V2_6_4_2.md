# Three-Prompt Council Validation — v2.6.4.2

DATE: 2026-08-12
BASELINE: v2.6.4.1 Rendering QA & Consulting Visual Excellence

## Prompt 1 — Rendering QA & Consulting Visual Excellence
**Verdict: KEEP / STRENGTHEN.**

Reasoning:
- correctly separates pre-render consulting visual quality from post-render production fidelity;
- preserves artifact topology and prevents safe-but-generic pages from passing;
- already forms an active v2.6.4.1 authority and remains intact.

Integration action:
- retained all v2.6.4.1 modules;
- connected them to the new canonical renderer contracts and final release gate.

## Prompt 2 — Deterministic Production Renderer / Compiler Architecture
**Verdict: KEEP AS RUNTIME CONTRACT; EXECUTABLE IMPLEMENTATION REMAINS EXTERNAL.**

Accepted elements:
- Canonical Page Spec;
- Canonical Scene Graph;
- fixed canvas;
- deterministic geometry/collision detection;
- measured text fit and font preflight;
- artifact topology validator;
- shared HTML/PDF/PPTX scene graph;
- independent raster QA;
- visual regression/parity;
- Golden Regression suite;
- bug-to-regression policy;
- Council-to-CI concept.

Conflict resolution:
The source previously advised keeping v2.6.4.1 rather than creating v2.6.4.2. The owner's current explicit instruction requests a new version, which supersedes that advisory. The architecture itself is preserved.

## Prompt 3 — Structural RTL / Directional Layout Engine
**Verdict: KEEP AS HARD PRODUCTION AUTHORITY.**

Accepted elements:
- RTL as physical geometry rather than alignment;
- logical START/END coordinates;
- component-level direction/mirror policies;
- ordered Arabic sequences starting physically right;
- directional zones and LTR islands;
- connector rebuilding after direction resolution;
- no-mirror registry;
- structural RTL regression tests;
- Rubix | Client fixed left and never mirrored.

## Explicitly excluded
GPTS/Custom-GPT packaging, GPTS installation guides, GPTS bootstrap instructions, and GPTS-specific knowledge-pack requirements from the longer source prompt are not part of v2.6.4.2.

## Council verdict
**GO — NON-DESTRUCTIVE INTEGRATION.**

Condition: executable renderer tests may be claimed as PASS only when an actual runtime produced the evidence.
