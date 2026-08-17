# Rendering Stress QA & Parity Release Gate

STATUS: BLOCKING RELEASE GATE

A client-facing page cannot release until all required checks are PASS:
- canvas / aspect ratio;
- margins / page-edge containment;
- text fit / font stability;
- overflow / overlap / clipping;
- artifact topology / node-edge integrity;
- RTL/LTR / bidi / ordered-flow correctness;
- numeral policy;
- logo/co-brand integrity;
- image crop/resolution;
- table/chart/diagram readability;
- HTML/PDF/PPTX parity where required;
- visual inspection of rendered pixels.

Required record:
`RENDER_STRESS_QA = PASS | FAIL`

Any unresolved hard failure blocks Release Gate 10 regardless of all other scores.
