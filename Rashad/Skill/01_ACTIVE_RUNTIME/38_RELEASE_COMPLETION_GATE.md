# 38 — Release Completion Gate

STATUS: **HARD RELEASE AUTHORITY — v2.5**

An artifact product may be described as complete only when:
- Product Delivery Contract is satisfied;
- all mandatory page nodes are `LOCKED` at the appropriate stage;
- all Geometry Handoffs are locked and hash-consistent;
- capability preflight passed for the executed route;
- production firewall passed;
- required composition/export actually executed;
- final artifact refs exist;
- semantic/topology/visual/geometry/RTL/numeral/brand QA passed;
- blocking council findings = 0;
- release approval exists.

Forbidden completion claims:
- “done” after content only;
- “artifact created” after hero image only;
- “PPTX/PDF complete” when only a written blueprint/test spec exists;
- “production runtime PASS” from policy documentation alone.

If blocked, say exactly which stage/capability is missing and keep product state `BLOCKED`.
## v2.6.4.2 production completion extension
For final-format artifact products, completion additionally requires the applicable v2.6.4.2 Canonical Page Spec/Scene Graph lineage and the Production Release Gate. An Arabic page with correct Arabic text but incorrect physical ordered flow is not RTL-compliant. Missing topology, silent font fallback, or material adapter redesign blocks release even if the file opens successfully.
