# 08 — Final Canonical Proposal Skeleton Resolver

STATUS: HARD CURRENT AUTHORITY — v2.6.4.5
OWNER LOCK: `PSK-OWNER-LOCK-2026-08-12`

## Purpose
Load the correct final proposal skeleton language without allowing any other source to redesign the architecture.

## Language selection
- Arabic proposal / Arabic evaluator-facing deliverable → load `02_IMMUTABLE_AUTHORITIES/FINAL_CANONICAL_PROPOSAL_SKELETON_AR.md`.
- English proposal / English evaluator-facing deliverable → load `02_IMMUTABLE_AUTHORITIES/FINAL_CANONICAL_PROPOSAL_SKELETON_EN.md`.
- Bilingual deliverable → maintain one shared section-ID architecture and produce synchronized Arabic/English formulations; never create two different structures.

## Canonical reader order
1. Cover
2. Table of Contents
3. Section 0 — Compliance Matrix
4. Section 1 — CEO Letter
5. Section 2 — Executive Summary
6. Section 3 — Client Environment
7. Section 4 — Methodology & Implementation Approach
8. Section 5 — Delivery Model & Governance
9. Section 6 — Corporate Capabilities & Experience
10. Section 7 — Appendices
11. Section 8 — Commercial Proposal
12. Close / Contact

The Arabic file owns the professional Arabic labels. The English file owns the professional English labels.

## RFP accommodation — no skeleton mutation
Extract all mandatory RFP forms, headings, schedules, evaluation criteria, envelopes, compliance artifacts and submission instructions. Map them into the locked canonical architecture or add them as mandatory supplemental artifacts/forms without changing Sections 0–8.

If an unavoidable legal/procurement structure conflict would require changing the locked architecture, return `STRUCTURE_CONFLICT_BLOCK`. Do not auto-override the skeleton.

## Production order remains different
The reader order is fixed, but production remains dependency-driven:
- understand RFP/evidence first;
- stabilize solution, methodology, roadmap, governance, team/evidence and commercial logic;
- draft Executive Summary late;
- draft CEO Letter after the Executive Summary;
- finalize Compliance Matrix / TOC / pagination after the content structure is stable.

## Detailed library relationship
`rubix-proposal-master-skeleton-v2.md` may provide CRAFT prompts, slide families and detailed content patterns only after they are mapped to a locked canonical section/subsection ID. It has zero authority to create a different top-level architecture.
