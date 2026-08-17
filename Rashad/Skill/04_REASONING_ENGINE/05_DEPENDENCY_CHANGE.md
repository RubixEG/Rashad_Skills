# Dependency and Change-Impact Engine

## Graph nodes
source facts, requirements, evaluation criteria, assumptions, claims, commitments, win themes, deliverables, workstreams, timeline, team roles, cost drivers, sections, pages, artifacts, compliance entries.

## Change behavior
When an approved upstream node changes:
1. identify affected nodes;
2. mark them stale;
3. produce an impact report;
4. block final compilation;
5. regenerate in dependency order;
6. require reapproval.

No silent inconsistency is permitted.


## v7.4 section-state integration
`SEC-DEP-001` is the section-state authority. Source, requirement, evaluation, scope, timeline, team, evidence, or commercial changes must mark affected Section Contracts/pages `STALE` and recompute readiness in production order.
