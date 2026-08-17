# Dependency & Scheduling Model — v2.2

Every material work object is a node. Reader order is never a dependency by itself.

| Field | Required |
|---|---|
| node_id | Yes |
| node_type | Yes — PRODUCT / SECTION / DELIVERABLE / EVIDENCE / DECISION / GATE / TASK |
| state | Yes — canonical node state |
| production_stage | Yes |
| predecessor_ids | When applicable |
| predecessor_condition | When applicable |
| dependency_type | Yes — HARD / SOFT / INFORMATION / APPROVAL / EVIDENCE / SCHEDULE |
| readiness | Derived — READY / NOT_READY |
| owner | Yes |
| due_gate | When applicable |
| stale_propagation_targets | When applicable |

`READINESS=READY` iff all HARD/APPROVAL/EVIDENCE predecessors required for the next production stage satisfy their conditions and no blocking finding applies.

Material upstream change propagates `STALE` to dependent APPROVED/LOCKED nodes.
