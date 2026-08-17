# 29 — Artifact Council Execution v2.3

STATUS: OPERATIONAL GOVERNANCE AUTHORITY
PURPOSE: Make artifact design a reviewed consulting decision, not an aesthetic preference.

## Council seats mapped to existing Rashad roles
- **Consulting Director** — `ROLE-DIRECTOR`: owns page argument and evaluator relevance.
- **Information Architect** — `ROLE-ARTIFACT`: owns information relationship, nodes, edges, and topology.
- **Artifact Director** — `ROLE-ARTIFACT`: owns artifact family/archetype and non-regression.
- **Visual Director** — `ROLE-STORY + ROLE-ARTIFACT`: owns hierarchy, rhythm, focal point, and composition intent.
- **Brand / Theme Governor** — `ROLE-BRAND-QA + ROLE-THEME-COLOR`: owns current identity and palette discipline after artifact lock.
- **Arabic / RTL Production SME** — `ROLE-BRAND-QA + ROLE-PREPRESS`: owns physical RTL, mixed LTR tokens, Arabic numerals, and native composition.
- **QA / Release SME** — `ROLE-QA`: owns semantic and production acceptance checks.

No new competing governance vocabulary is introduced; these are functional seats mapped to the existing role registry.

## Artifact Council gates

### GATE A — Meaning
Required:
- question;
- thesis;
- evidence;
- implication;
- relationship confidence.

Block if the page has no material question or is only decorative.

### GATE B — Topology
Required:
- artifact family/archetype;
- semantic nodes;
- semantic edges;
- reading path;
- focal point;
- density class;
- forbidden fallback.

Block generic-card collapse or semantic edge loss.

### GATE C — Visual Ideation (optional)
If image ideation is useful, authorize `INTERNAL_VISUAL_CONCEPT` only under `28_IMAGE_IDEATION_INTERFACE.md`.

### GATE D — Visual Blueprint
Approve geometry logic, regions, anchors, whitespace, RTL order, brand application plan, and production requirements.

### GATE E — Production Firewall
Run `01_ACTIVE_RUNTIME/29_PRODUCTION_EXECUTION_FIREWALL.md`. No Council may waive a failed firewall gate.

### GATE F — Release QA
Validate semantic fidelity + visual quality + RTL/numerals + brand + collision/overflow + editability.

## Quorum
Artifact Intent lock requires:
- ROLE-DIRECTOR or delegated proposal owner;
- ROLE-ARTIFACT;
- no unresolved critical ROLE-QA finding.

Visual Blueprint lock additionally requires:
- ROLE-BRAND-QA or ROLE-THEME-COLOR for branded pages;
- ROLE-PREPRESS/RTL reviewer for Arabic production.

All decisions must be stored in the existing Council Session/Finding and Approval Ledgers.
