MODULE: ENGAGEMENT_STATE_TEMPLATE
STATUS: AUTHORITATIVE_TEMPLATE — v2.5
LOAD WHEN: After engagement init; at every material milestone; when continuing an engagement.
DEPENDS ON: ENGAGEMENT_INIT_TEMPLATE; SECTION_DEPENDENCIES; 07_GOVERNANCE_AND_QA/19_UNIFIED_STATE_MACHINE.md; 30_OPERATIONAL_SCHEMAS_AND_STATE.md.

# Engagement State Template

Persist one state file per engagement. New chats must read it before assuming progress.

```text
ENGAGEMENT_ID:
CLIENT:
PROJECT:
SECTOR:
RFP_LANGUAGE:
ARABIC_NUMERAL_POLICY: ARABIC_INDIC_IN_ARABIC_PROSE
SOURCE_PACK_MODE:            # SCOPE_ONLY | PARTIAL_RFP_PACK | FULL_RFP_PACK
SOURCE_FILES:
SOURCE_PACK_COMPLETENESS:    # COMPLETE | PARTIAL | SCOPE_ONLY | UNKNOWN
APPENDIX_LIBRARY_STATUS:     # PRESENT | APPENDIX_LIBRARY_MISSING | NOT_INSPECTED
ENGAGEMENT_STATE: NEW
```

## Node progress

Use only canonical `STATE` values from the Unified State Machine. `READINESS` and `PRODUCTION_STAGE` are attributes, not alternate states.

| Node / Product | State | Readiness | Production Stage | Version | Release Gate | Notes |
|---|---|---|---|---|---|---|
| INTERNAL_PURSUIT_BRIEF / RFP Summary | NOT_STARTED | READY | CONTENT |  | NOT_RUN | Delivery contract defaults to ARTIFACT; content stage alone is incomplete |
| Compliance Register v0 | NOT_STARTED | NOT_READY | CONTENT |  | NOT_RUN | |
| Bid Strategy | NOT_STARTED | NOT_READY | CONTENT |  | NOT_RUN | |
| Solution / Client Environment | NOT_STARTED | NOT_READY | CONTENT |  | NOT_RUN | |
| Methodology | NOT_STARTED | NOT_READY | CONTENT |  | NOT_RUN | |
| Delivery & Governance | NOT_STARTED | NOT_READY | CONTENT |  | NOT_RUN | |
| Capabilities & Experience | NOT_STARTED | NOT_READY | CONTENT |  | NOT_RUN | |
| Appendix / Evidence | NOT_STARTED | READY | CONTENT |  | NOT_RUN | Evidence collection may start day one |
| Commercial | NOT_STARTED | NOT_READY | CONTENT |  | NOT_RUN | |
| Executive Summary | NOT_STARTED | NOT_READY | CONTENT |  | NOT_RUN | Finalize late |
| CEO Letter | NOT_STARTED | NOT_READY | CONTENT |  | NOT_RUN | After Executive Summary |
| Final Compliance Matrix | NOT_STARTED | NOT_READY | CONTENT |  | NOT_RUN | After references stabilize |
| Compiled Presentation | NOT_STARTED | NOT_READY | VISUAL_COMPOSITION |  | NOT_RUN | External composer required |

## Open issues
```text
OPEN_ASSUMPTIONS:
CONTRADICTIONS:
MISSING_EVIDENCE:
TEAM_READINESS:
COMMERCIAL_ISSUES:
BLOCKING_GAPS:
```

## Operational ledgers — mandatory sections
Maintain these tables using the schemas under `07_GOVERNANCE_AND_QA/20_*.md` through `26_*.md`:
- `COMPLIANCE_REGISTER`
- `APPROVAL_LEDGER`
- `COUNCIL_SESSION_LEDGER`
- `COUNCIL_FINDING_LEDGER`
- `DEPENDENCY_LEDGER`
- `REVERSE_BID_CALENDAR`
- `PRODUCT_DELIVERY_COMPLETION_LEDGER`
- `CAPABILITY_PREFLIGHT_LEDGER`

## Next action
```text
NEXT_RECOMMENDED_NODE:
WHY:
CURRENT_VERSION:
LAST_UPDATED_UTC:
LAST_DECISION_SOURCE:
```

When user says **Continue**: resolve next actions from dependency readiness + open blocking findings + bid calendar, not chat guesswork or reader order.

## v2.3 Artifact Intelligence ledgers — mandatory when artifacts exist
Maintain:
- `ARTIFACT_INTENT_LEDGER` using `07_GOVERNANCE_AND_QA/27_ARTIFACT_INTENT_LEDGER_SCHEMA.md`
- `VISUAL_BLUEPRINT_LEDGER` using `07_GOVERNANCE_AND_QA/28_VISUAL_BLUEPRINT_LEDGER_SCHEMA.md`
- `GEOMETRY_HANDOFF_LEDGER` using `07_GOVERNANCE_AND_QA/29_GEOMETRY_HANDOFF_LEDGER_SCHEMA.md`
- `ARCHETYPE_SELECTOR_DECISION_LEDGER` using `07_GOVERNANCE_AND_QA/30_ARCHETYPE_SELECTOR_DECISION_LEDGER_SCHEMA.md`

Dependency rule: any change to an approved Artifact Intent hash automatically marks its Visual Blueprint and Geometry Handoff `STALE` until re-approved. Any Visual Blueprint hash change marks Geometry Handoff `STALE`. No stale geometry may enter production.

`DONE` is not a persisted node state. Artifact completion is proven only by the Product Delivery & Completion Ledger + Release Gate.
