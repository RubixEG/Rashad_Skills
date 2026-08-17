# Version 4 Executable QA Harness v2 Validation

## Machine-executed result
- Clean fixture: **HTML_PREEXPORT_PASS**.
- Clean fixture stress: `FONT_SCALE_108` PASS; `LINE_HEIGHT_108` PASS.
- Repeat-render geometry stability: **PASS (3/3 identical geometry fingerprints)**.
- Broken failure classes blocked: overflow, detached connector, off-canvas, wrong RTL sequence, detached label, debug leakage, card-dominance/no topology, element collision, font fallback, z-index occlusion, malformed divider, alignment drift.
- Previous Version 3 six-page pilot: **BLOCKED on all 6 pages** under the new QA.

## Integration implication
Version 4's QA requirements are not prose-only: the companion executable demonstrates that the specified defect classes can be detected and blocked in rendered HTML.

Executable companion SHA-256: `0164a7a4faa5c5da24547741c439a70dc7ccad7464588b7ec2e1711cca1f6551`.
