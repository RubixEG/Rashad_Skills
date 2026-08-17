# Regression Test — RFP Authorship + Arabic Visible Language

## A. Authorship section presence
For `INTERNAL_PURSUIT_BRIEF`, fail if the final brief contains only generic procurement maturity and omits:
- likely authoring model;
- confidence score;
- evidence for;
- counter-evidence;
- scored maturity dimensions;
- bid/pricing/clarification implication.

## B. Unsupported authorship claim
Fail if output states a named consultancy/person authored the RFP without explicit source evidence.

## C. Arabic visible labels
For Arabic engagement, fail if structural visible headings/subheadings contain avoidable English role labels such as:
`Competition Narrative`, `Table of Contents`, `Opportunity Snapshot`, `Key Dates`, `Strategic Reading`, `Win Strategy`, `Management Conclusion`.

## D. Technical-token exception
Do not fail valid isolated tokens such as `AI`, `POC`, `API`, `SLA`, `UAT`, `UI/UX`, product names, standards, code or identifiers.

## E. Numerals/RTL
Existing Production Firewall numeral and physical RTL gates remain unchanged and must also pass.
