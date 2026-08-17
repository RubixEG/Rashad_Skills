# Test 22 — BiDi, Connector & Brand Precedence Regression

STATUS: SPECIFICATION TEST — runtime execution evidence required for PASS.

Cases:
- `PAGE_DIRECTION=MIXED` → invalid; use RTL/LTR + directional islands.
- Arabic sequence item 1 physically left without exception → FAIL.
- `(API)` punctuation/run order differs materially between HTML/PDF/PPTX → FAIL parity.
- connector endpoint is calculated before mirroring and lands on wrong node → FAIL topology.
- bidirectional edge loses one arrowhead after RTL resolution → FAIL.
- current mandatory RFP brand requirement conflicts with house default and is explicitly evidenced → mandatory RFP requirement wins.
- current engagement deck proposes alternate co-brand arrangement but no mandatory requirement/owner approval exists → house default remains.
- logo optical visible-height ratio outside 0.98–1.02 → FAIL brand geometry.
- policy document says PASS but no evidence_id exists → truthfulness FAIL; status must be GATE_DEFINED/NOT_EXECUTED.

