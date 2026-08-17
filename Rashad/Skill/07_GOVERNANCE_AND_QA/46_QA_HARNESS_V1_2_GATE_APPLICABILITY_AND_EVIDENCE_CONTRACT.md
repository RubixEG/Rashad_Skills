# QA Harness v1.2 Gate Applicability & Evidence Contract

STATUS: HARD EXTERNAL-RUNTIME INTERFACE — v2.6.4.6

The external harness uses the taxonomy:
`GATE_DEFINED | NOT_EXECUTED | PASS | FAIL | BLOCKED | N_A`.

## Applicability
A compiled QA spec must explicitly mark page-specific gates `REQUIRED` or `N_A` where practical. An irrelevant timeline/sequence/co-brand/topology gate must not block a page merely because the page legitimately lacks that feature.

## PASS invariant
Runtime PASS requires actual execution and evidence ID/timestamp. A Markdown-defined test is never execution evidence.

## Current v1.2 browser gates
G01–G14 cover overflow, masked overflow, overlap, containment, structural RTL sequence, numeral purity, resolved font substitution, brand hash, co-brand optical geometry, surface luminance, artifact topology lineage, palette, Golden Master provenance/canvas, and governed asset transform integrity.

## Fixture rule
Harness sample client marks and sample fonts are test fixtures only. Current engagement brand/font authorities must compile the actual QA spec.
