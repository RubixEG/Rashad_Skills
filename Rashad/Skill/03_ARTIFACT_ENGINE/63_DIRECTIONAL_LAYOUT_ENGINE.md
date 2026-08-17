# Directional Layout Engine

STATUS: HARD STRUCTURAL RTL/LTR AUTHORITY — v2.6.4.2

## Core principle
**RTL is not text alignment. RTL is physical reading geometry.**

A page with correctly shaped Arabic text but an unjustified left-to-right ordered visual sequence is not RTL compliant.

## Required policies
Every page defines:
- `PAGE_DIRECTION = RTL | LTR`
- `FLOW_DIRECTION = RTL | LTR | PRESERVE`

Every component/zone defines:
- `COMPONENT_DIRECTION = AUTO | RTL | LTR | PRESERVE`
- `MIRROR_POLICY = MIRROR_STRUCTURE | MIRROR_SEQUENCE_ONLY | PRESERVE_STRUCTURE | NEVER_MIRROR`

## Required sub-engines
1. Page Direction Resolver
2. Logical Start/End Mapper
3. Sequence Mirroring Engine
4. Grid Order Resolver
5. Timeline Direction Resolver
6. Process Direction Resolver
7. Connector Rebuilder
8. Mixed RTL/LTR Island Manager
9. Directional Zone Manager
10. No-Mirror Exception Registry
11. RTL Structural QA

## Ordered Arabic structures
Unless a documented exception exists, the logical first item appears at the physical right for:
- sequential cards/elements;
- process stages;
- phase journeys;
- numbered stages;
- timelines and milestones;
- horizontal delivery flows;
- transformation/maturity sequences;
- ordered workstreams.

Semantic order remains stable internally. Only physical placement changes.

## Connector order
Never draw connectors and then apply a blind CSS mirror.

Correct pipeline:
`Semantic Graph → Resolve Direction → Resolve Node Geometry → Recalculate Connector Endpoints → Render Connectors → Structural QA`

## Mixed-direction islands
An RTL page may contain LTR or preserved zones. Each zone must declare its own policy.

## Hard fail
Arabic ordered content beginning physically from the left without an approved exception is a hard release blocker.

## v2.6.4.3 clarification — no page-level MIXED
`PAGE_DIRECTION` is exactly `RTL | LTR`. Mixed-direction pages are modeled with `directional_islands[]` / zones. This removes ambiguity between page direction and component direction.

Cross-format mixed text follows `74_CROSS_FORMAT_BIDI_RUN_ORDER_CONTRACT.md`. Connector ownership/anchors/routes follow `75_CONNECTOR_SEMANTICS_AND_ENDPOINT_CONTRACT.md`.
