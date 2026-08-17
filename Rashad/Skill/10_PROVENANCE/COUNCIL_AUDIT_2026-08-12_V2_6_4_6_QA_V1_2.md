# Council Audit — v2.6.4.6 + QA Harness v1.2

## Scope
Validate the integration of the owner-locked Rashad v2.6.4.5 Skill with executable QA Harness v1.2 and close the ten P0 gaps identified in the prior integration audit.

## Council
Consulting Partner; Rashad Product Architect; Proposal Director; Artifact Intelligence Director; Golden Visual Master Director; Rendering Architecture Lead; RTL/BiDi Lead; Topology Lead; Brand Governor; QA/Regression Lead; Prepress/Parity Lead; Evidence Truthfulness Auditor; Non-Regression Auditor; Release Chair.

## Decisions
| P0 gap | v1.2 / v2.6.4.6 resolution | Council status |
|---|---|---|
| Page Spec → QA Spec compiler missing | executable `compile_qa_spec.py` + Skill handoff contract | CLOSED |
| Irrelevant gates block pages | explicit REQUIRED/N_A applicability | CLOSED |
| GVM topology invisible to DOM | hashed semantic topology sidecar, no fake DOM nodes | CLOSED |
| G13 master SHA optional | compiler blocks GVM page without frozen SHA | CLOSED |
| crop/mirror/filter/stretch not measured | G14 transform-integrity gate | CLOSED |
| logo 3%/alpha-any mismatch | 2% tolerance + 5% alpha + optical-center check | CLOSED |
| font profile drift | runtime profile synchronized to Montserrat / Montserrat Arabic; substitutions fail | CLOSED |
| runtime errors weak/unstructured | structured NOT_EXECUTED/BLOCKED evidence + exit code 2 | CLOSED |
| HTML gate called RELEASED | renamed to HTML_PREEXPORT_PASS | CLOSED |
| no PDF/PPTX parity / deck QA | executable raster parity + deck continuity + final aggregator | CLOSED |

## Additional conflict closed
Historical v2.6.4.3 blanket image-isolation wording conflicted with the approved v2.6.4.4 Golden Visual Master strategy. Current authority now states that a full-page Golden Visual Master is an approved governed visual underlay, while exact text/official values/logos/page chrome remain native overlays.

## Runtime validation evidence in this environment
- Harness Python compile: PASS.
- Non-browser unit tests: PASS.
- Page-Spec compiler assertions: PASS.
- G11 sidecar topology direct execution: PASS on valid fixture.
- G14 transform integrity: PASS identity / FAIL mirror as expected.
- Actual PDF raster parity pipeline: PASS on controlled fixture.
- Actual PPTX → LibreOffice → PDF → raster parity: PASS on controlled fixture.
- Deck continuity executable checker: PASS on controlled fixture.
- Browser G01–G14 fresh run: NOT EXECUTED because local Chromium navigation is blocked by administrator policy; structured runtime-block evidence was produced.

## QA runtime profile SHA-256
`0df82f93a9f0c2d58d95135688513f73a7c0856b2301851568eca180b41f89d1`

## Verdict
**GO — INTEGRATED KNOWLEDGE + EXECUTABLE QA COMPANION ARCHITECTURE.**

**Production release for a real engagement remains evidence-dependent**: actual page/browser, fonts, current client logo, Golden Masters, PDF/PPTX exports and deck continuity must run through the external harness.
