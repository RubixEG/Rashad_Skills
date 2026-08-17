# V6.2.2 Page Criticality Classification & Anti-Downgrade Contract

**STATUS: CURRENT HARD CRITICALITY AUTHORITY**

## Purpose
Prevent a producer from classifying an analytical page as non-critical merely to avoid exactly-five hypotheses, rendered-candidate search, independent judging, or QA.

## Fail-closed classification
A page is **CRITICAL_ANALYTICAL** by default if it contains or interprets any of: management/evaluator question; thesis/implication; RFP evidence; semantic relationships; scope/workstreams; BOQ/deliverables/acceptance; evaluation/win logic; team/capacity; methodology; governance; roadmap/dependencies; technical/data/integration architecture; commercial exposure; risk; clarifications/assumptions; or a management/bid decision.

Only inherently non-analytical page families may be **NON_CRITICAL_NON_ANALYTICAL**: cover, section divider, table of contents/navigation, glossary, static appendix index, or purely administrative/legal notice with no analytical claim.

If classification is ambiguous, classify **CRITICAL_ANALYTICAL**.

## Ownership
- The producer may propose a classification but cannot authoritatively downgrade it.
- Classification must be derived by this contract / runtime classifier from page semantics.
- Owner intent may force a safer upgrade to CRITICAL_ANALYTICAL.
- No owner/user/producer waiver may label an actually analytical page non-critical merely to reduce cost, hypotheses, rendered candidates, judge calls, or QA.

## Required evidence
For FULL_RUNTIME, persist `page_criticality.json` conforming to `schemas/page_criticality.schema.json`. Missing/invalid criticality evidence defaults to `CRITICAL_ANALYTICAL` for any client-facing page that is not an obvious cover/divider/TOC/glossary/static index.

## Consequences
CRITICAL_ANALYTICAL requires exactly 5 materially distinct exhibit hypotheses, at least 3 actual rendered candidates, independent Artifact Truth ≥90, independent CEQS ≥90 when applicable, and all mandatory executable QA/release gates.

Criticality is a gate input, not a producer convenience flag.
