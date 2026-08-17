# 49 — Page Spec → QA Spec Handoff Contract

STATUS: HARD RUNTIME INTEGRATION CONTRACT — v2.6.4.6

Every page entering executable QA must be compiled from the locked Canonical Page Spec into a format-specific QA spec. The compiler, not a human shortcut, determines gate applicability and semantic lineage.

## Compiler outputs
For each page:
1. `<page_id>.qa.json` — executable gate configuration;
2. `<page_id>.topology.json` — governed semantic nodes/edges for Golden-Master sidecar mode;
3. hashes linking both back to the locked Page Spec/master/brand assets.

## Required compilation rules
- `PAGE_DIRECTION = RTL | LTR` only;
- sequential RTL gate required only when an ordered sequence exists; otherwise `N_A`;
- numeral gate required only when the language/number policy requires it;
- brand/co-brand gates required only when governed marks are present;
- topology gate required only when the page declares an artifact family/topology;
- G13 Golden Master gate required for every GVM page;
- G14 transform-integrity required for GVM and/or governed brand assets;
- Page-Spec font/palette/asset hashes override harness sample fixtures;
- real client logo hash must come from the current engagement asset authority, never the harness fixture.

Compiler failure is a production block, not permission to hand-author a looser QA spec.
