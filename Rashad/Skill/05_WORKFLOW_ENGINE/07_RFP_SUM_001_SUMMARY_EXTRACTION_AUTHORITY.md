# RFP-SUM-001 — RFP Understanding Summary Extraction Authority

## Status
Priority-1 extraction invariant and Bid Strategy release blocker.

## Purpose
Create a complete, source-traceable internal understanding of the procurement before proposal strategy or section drafting. The summary is not a client-facing Executive Summary.

## Locator rule
Required facts may appear in the main booklet, detailed scope, appendices, BOQ, evaluation sheets, team specifications, contract, cybersecurity requirements, penalties, clarification responses, or other attachments.

The engine must search by meaning and synonyms. It must not assume:
- fixed page numbers;
- fixed section numbers;
- one document contains everything;
- the RFP's table of contents is complete;
- annexes repeat the main booklet accurately.

## Mandatory extraction groups when present

### A. Identity and competition control
- current government/client logo for summary presentation;
- government entity name from authoritative definitions/identity pages;
- competition/project name;
- tender or qualification type and level;
- reference number, version, issue date, document price, language, currency, and submission method.

### B. Schedule and duration
Extract and distinguish:
- last date for questions and clarifications;
- proposal submission deadline;
- bid opening date/time;
- award/notification date;
- service commencement date;
- offer validity;
- contract/project duration;
- extension rules when stated.

Preserve the source calendar and label Hijri/Gregorian explicitly. Do not convert or infer dates unless authorized.

### C. Scope and location
- project purpose and institutional context;
- objectives;
- detailed scope boundary;
- place(s) of performance and onsite requirements;
- location-related cost implications;
- named systems, stakeholders, sites, channels, volumes, and dependencies.

### D. Phase and workstream architecture
For every phase/workstream extract:
1. source sequence number and title;
2. what the phase contains;
3. activities and responsibilities;
4. output(s) for the phase;
5. inputs/dependencies;
6. acceptance or transition logic when stated.

#### Sequence integrity check
The source order may be incomplete or logically weak. Never silently rewrite it.

Maintain both:
- `source_sequence` — exactly as the RFP states;
- `analytical_dependency_sequence` — the logically inferred order, clearly labeled as analysis.

When they differ, create a clarification or bid-risk item and explain why.

### E. BOQ and outputs
- locate BOQ even when it exists only in annexes;
- extract every line item, unit, quantity, output type, and description;
- map each line to its phase/workstream;
- identify outputs in scope text that are absent from the BOQ and vice versa;
- record any pricing sensitivity.

### F. Training and knowledge transfer
- required training modes;
- audience and quantity when stated;
- deliverables such as manuals, workshops, shadowing, train-the-trainer, or operational handover;
- relationship to acceptance and long-term independence;
- cost/resource implications.

### G. Evaluation and qualification
- pass/fail gates;
- technical and financial weights;
- detailed criteria and subweights;
- thresholds;
- qualification ratios and financial standing;
- formulas and tie-break rules;
- contradictory weights or thresholds across documents.

### H. Mandatory team
- every role, quantity, education, experience, certifications, nationality/localization, and availability rule;
- replacement time and approval requirements;
- team evidence and CV instructions;
- gaps where team capability is required but no formal table exists.

### I. Submission package and compliance
- legal and statutory documents;
- technical response documents;
- financial response documents;
- separate file/multiple envelope requirements;
- signatures, stamps, encryption, naming, formats, and validity rules;
- subcontracting, consortium, local content, guarantee, and eligibility rules.

### J. Contractual, security, and operational controls
- penalties and aggregate caps;
- payment and milestone rules;
- quality plan, safety, SLAs, acceptance, reporting, and records;
- confidentiality, NDA, access, offboarding, secure deletion, incident reporting, cyber requirements, data/privacy, and third-party clauses;
- support, maintenance, warranty, and operational obligations.

### K. Contradictions, gaps, and clarification questions
- missing annexes;
- conflicting dates, durations, weights, quantities, test counts, or responsibilities;
- undefined acceptance criteria;
- dependencies assigned to the client but not described;
- ambiguous commitments or cost drivers.

### L. Bid implications and exact section mapping
- evaluator priorities;
- proof requirements;
- major solution implications;
- cost/schedule/team implications;
- concise mapping only to the exact approved top-level deck section names.

Do not invent or rename top-level sections.

### M. Authorship fingerprint and procurement maturity — internal product only
Build evidence for the authoring/assembly model without claiming a named author unless explicitly sourced. Capture terminology/style consistency, scope/BOQ/evaluation/team/acceptance alignment, annex modularity, technical/commercial depth consistency, contradictions and handoff seams. Execute `01_ACTIVE_RUNTIME/32_RFP_AUTHORSHIP_AND_PROCUREMENT_MATURITY.md`.

## Minimum source-search strategy
Search all uploaded files for semantic variants of:
- entity, government entity, definitions, client;
- dates, questions, submission, opening, award, start, duration;
- scope, objectives, phases, workstreams, deliverables;
- BOQ, quantities, prices, output, report, model, dashboard;
- training, transfer, handover;
- evaluation, pass/fail, weights, qualification;
- team, manpower, personnel, CV, certification;
- cyber, confidentiality, NDA, access, deletion, incident;
- penalties, delay, deficiency, SLA, quality, safety;
- annex, attachment, clarification, contract.

## Summary approval gate
The summary cannot be approved until:
- all required groups are `FOUND`, `NOT_PRESENT`, `CONFLICTED`, or `MISSING_ATTACHMENT`;
- every material fact has a source reference;
- every conflict is visible;
- the phase order has passed the sequence-integrity check;
- BOQ, evaluation, team, training, schedule, location, penalties, and security are not omitted when present;
- the internal brief includes the authorship fingerprint/procurement-maturity assessment or explicitly records `INSUFFICIENT_EVIDENCE`;
- Arabic visible structural labels pass `33_ARABIC_VISIBLE_LANGUAGE_PURITY_GATE.md`;
- the user confirms or corrects the summary.

## Hard fails
- relying on a fixed page or section number from another RFP;
- ignoring annexes;
- omitting a key date or duration that exists;
- omitting place of performance when it may affect cost;
- omitting BOQ, evaluation, team, or training when present;
- silently correcting conflicting facts;
- silently reordering phases;
- treating a short RFP introduction as sufficient understanding when detailed objectives/phases provide the real meaning;
- presenting analysis as a source fact;
- calling the RFP Understanding Summary an Executive Summary.
