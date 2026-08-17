# V7.0.1 — Total QA Detector Implementation Contract

**STATUS: LINEAGE / COMPATIBILITY ONLY — current routing uses `79_V7_QA_DETECTOR_IMPLEMENTATION_CONTRACT.md` under v7.0.2**

Every case in `73_V7_VISUAL_AND_EXECUTIVE_FAILURE_TAXONOMY.json` now specifies: detector class, measurement, fail threshold/condition, applicability, minimum measured objects, linked stress fixture(s), permanent test fixture ID, evidence-output shape, execution owner, NOT_INSTRUMENTED behavior and implementation status.

These are **implementation contracts, not claims of executable code**. Until the Streamlit/renderer/QA runtime implements a detector, its status remains `SPECIFIED_NOT_IMPLEMENTED`; a required applicable case cannot become PASS from the specification alone.

Universal rules:
1. `measured_object_count < minimum_measured_objects` → `FAIL_NOT_INSTRUMENTED` for blocking applicable gates.
2. Machine metrics cannot self-certify qualitative consulting/artifact cases; hybrid/visual cases require independent critic evidence in addition to machine features.
3. Threshold overrides are allowed only through a current page/artifact-family authority that explains semantic intent; producer-created convenience overrides are invalid.
4. Repair must preserve content/node/edge/evidence/topology/brand/direction signatures.
5. Every runtime finding references current master/input hashes. Stale evidence is invalid.
6. Every discovered new failure receives a new taxonomy ID and fixture before closure.
