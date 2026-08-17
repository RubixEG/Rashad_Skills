# Artifact Execution Proof & No-Downgrade Gate

STATUS: BLOCKING PRODUCTION AUTHORITY

## Problem prevented
A page must not be called an Artifact Engine page merely because the Artifact Engine exists in knowledge. The page must carry execution evidence proving the Artifact Intelligence chain was actually run and preserved into the rendered page.

## Mandatory execution trace for every visible analytical page
Each page must persist all of the following before composition:
- `page_role_id`
- `management_or_evaluator_question`
- `page_thesis`
- `evidence_refs`
- `information_relationship`
- `artifact_intent_id`
- `semantic_nodes_edges_id`
- `selected_archetype_id`
- `visual_blueprint_id`
- `geometry_handoff_id`
- `artifact_council_session_id`
- `artifact_strength_score`
- `forbidden_fallbacks`
- `rendered_page_qa_id`

Missing any required trace field = `BLOCKED — ARTIFACT EXECUTION NOT PROVEN`.

## No-downgrade rule
Relationship-heavy content may not be rendered as a generic card grid, plain text blocks, or a table merely because those forms are easier to produce.

The following relationships require a relationship-bearing artifact unless the Artifact Council explicitly proves an equivalent-strength alternative:
- hierarchy;
- sequence;
- dependency;
- cause/effect;
- current-to-target;
- lifecycle;
- system/architecture;
- network/ecosystem;
- workstream-to-deliverable;
- criterion-to-win-response;
- risk-to-response;
- requirement-to-evidence;
- quantitative prioritization.

If the deterministic composer cannot preserve the approved artifact topology, the page returns to `ARTIFACT_STAGE`; it must not silently fall back to cards.

## Page-family minimums for RFP Summary
The following RFP Summary roles MUST be visually analytical, not generic containers:
- `SCOPE_ARCHITECTURE`: system/workstream architecture with visible relationships/dependencies.
- `DELIVERY_JOURNEY`: phased journey/track model with dependencies and gates.
- `BOQ_INTELLIGENCE`: compression/mapping model that exposes scope-to-BOQ and acceptance/pricing sensitivity.
- `TEAM_CAPACITY`: capacity/role architecture or evidence matrix with management implication; raw table only as supporting evidence.
- `EVALUATION_WIN`: criterion-to-win-response/evidence architecture.
- `COMMERCIAL_EXPOSURE`: cost-driver/exposure architecture.
- `PROPOSAL_STRATEGY`: build-priority/evidence dependency architecture.
- `RISKS`: risk prioritization + treatment architecture; not a clause list.
- `CLARIFICATIONS`: decision-impact register showing what changes if answer A vs B.
- `AUTHORSHIP_MATURITY`: evidence-for/evidence-against fingerprint + scored maturity view.
- `BID_DECISION`: management decision cockpit/decision tree with conditions and next gate.

## Strength threshold
Before release, Artifact Council must record `artifact_strength_score >= 7/10` for every relationship-heavy page. A lower score forces redesign, not cosmetic QA.

## Evidence-table exception
A raw table is allowed only when the page's dominant information relationship is genuinely tabular evidence. If the management question requires hierarchy, dependency, prioritization, comparison, causality, or sequence, a table alone is insufficient.

## v2.6.4 section-board proof extension
For multi-page sections, execution proof must additionally include `section_visual_board_id`, `section_visual_charter_id`, page-to-board mappings, and Visual Fidelity QA. A set of individually valid pages does not prove section-level artifact quality.
