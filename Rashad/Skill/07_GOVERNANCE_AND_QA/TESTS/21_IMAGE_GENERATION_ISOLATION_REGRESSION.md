# Test 21 — Image Generation Isolation Regression

STATUS: SPECIFICATION TEST — runtime execution evidence required for PASS.

Cases:
1. Hero request receives full slide/RFP context and generates a slide → expected `REJECTED_CONTAMINATED`.
2. Generated asset contains pseudo-text or numeral → reject.
3. Generated asset invents Rubix/client-like logo → reject.
4. Generated asset contains cards/table/footer/page number → reject for production-asset mode.
5. Isolated wide editorial asset with no forbidden baked content → eligible for Asset QA.
6. Environment cannot isolate context for a high-risk production asset → `BLOCKED_CONTEXT_NOT_ISOLATABLE` or reference-only.
7. Image tool exists but deterministic composer does not → production rendering remains BLOCKED.

