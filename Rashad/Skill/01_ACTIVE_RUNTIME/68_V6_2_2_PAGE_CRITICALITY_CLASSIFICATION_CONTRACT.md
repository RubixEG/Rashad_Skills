# V6.2.2 Page Criticality Classification & Anti-Downgrade Contract

**STATUS: CURRENT HARD CRITICALITY AUTHORITY**

## Purpose
Prevent a producer from classifying an analytical page as non-critical merely to avoid exactly-five communication strategies, internal concept search, production rendering, independent actual-pixel judging, or QA.

## Fail-closed classification
A page is **CRITICAL_ANALYTICAL** by default if it contains or interprets any of: management/evaluator question; thesis/implication; RFP evidence; semantic relationships; scope/workstreams; BOQ/deliverables/acceptance; evaluation/win logic; team/capacity; methodology; governance; roadmap/dependencies; technical/data/integration architecture; commercial exposure; risk; clarifications/assumptions; or a management/bid decision.

Only inherently non-analytical page families may be **NON_CRITICAL_NON_ANALYTICAL**: cover, section divider, table of contents/navigation, glossary, static appendix index, or purely administrative/legal notice with no analytical claim.

If classification is ambiguous, classify **CRITICAL_ANALYTICAL**.

## Ownership
- The producer may propose a classification but cannot authoritatively downgrade it.
- Classification must be derived by this contract / runtime classifier from page semantics.
- Owner intent may force a safer upgrade to CRITICAL_ANALYTICAL.
- No owner/user/producer waiver may label an actually analytical page non-critical merely to reduce cost, communication hypotheses, concept candidates, production-render work, judge calls, repair, or QA.

## Required evidence
For FULL_RUNTIME, persist `page_criticality.json` conforming to `schemas/page_criticality.schema.json`. Missing/invalid criticality evidence defaults to `CRITICAL_ANALYTICAL` for any client-facing page that is not an obvious cover/divider/TOC/glossary/static index.

## Consequences
Under current v7.2 (using the inherited v7.1 artifact-delivery foundation), `CRITICAL_ANALYTICAL` requires exactly 5 materially distinct **communication-strategy hypotheses** and internal concept-search evidence. Those concept renders are internal only. Any user-visible artifact additionally requires a real `PRODUCTION_PAGE_RENDER`, independent actual-pixel QA tied to the exact production hash, repair closure, deck-level actual-output QA when applicable, exact-file Delivery Gate, and all mandatory release gates. Inherited Artifact Truth/CEQS measures remain diagnostics where applicable; they never substitute for product-pixel QA.

Criticality is a gate input, not a producer convenience flag.
