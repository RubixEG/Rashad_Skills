# V6.2.2 Capability Modes & Truthfulness Contract

**STATUS: CURRENT CAPABILITY-MODE AUTHORITY**

## Mode owner
Mode is computed by executable capability preflight, not selected by the producer/model. The user/owner may explicitly force a safer downgrade to `ADVISORY`, but neither the producer nor user intent can elevate a failed preflight to `FULL_RUNTIME`.

## Required preflight authority
Execute `01_ACTIVE_RUNTIME/36_CAPABILITY_PREFLIGHT_AND_TOOL_ROUTING.md` before the first production action and whenever a required runtime capability materially changes. Capability existence in source code/documentation is not execution proof.

## Mandatory mode evidence
Persist a schema-valid `mode_declaration.json` conforming to `schemas/mode_declaration.schema.json`. At minimum it records:
- declared mode;
- preflight status;
- required capability checks and evidence references;
- runner/owner of the preflight;
- timestamp;
- relevant authority/config hashes.

No valid `mode_declaration.json` → `ADVISORY` by default. A producer-authored narrative saying “preflight passed” has zero authority.

## FULL_RUNTIME
Allowed only when the required deterministic renderer, independent judge path, proof persistence, file output, and applicable QA/runtime checks are all evidenced as executable and the preflight returns PASS. Only `FULL_RUNTIME` can progress toward machine-certified `RELEASED`.

## ADVISORY
Use when one or more required executable capabilities are unavailable, unproven, or preflight evidence is missing. Rashad may produce evidence analysis, Page Content Packs, graphs, artifact hypotheses, visual blueprints, remediation guidance, and clearly marked draft artifacts. Machine-dependent stages remain `NOT_EXECUTED` / `BLOCKED`; the system may never claim `RELEASED`, `QA PASS`, independent CEQS PASS, or independent Artifact Truth PASS.

### ADVISORY export law
Draft export is permitted for useful review, but any client-shaped `PDF`, `PPTX`, `PNG`, `JPG`, or `HTML` produced in ADVISORY must:
1. contain a visible, non-removable-in-normal-view mark **`DRAFT — NOT RELEASED`** on every page/frame;
2. include `_DRAFT_NOT_RELEASED` in the filename;
3. carry machine state `release_status=ADVISORY_UNVERIFIED`;
4. never be placed in a release/final directory or named `FINAL`, `RELEASED`, `APPROVED`, or equivalent.

If the medium cannot carry the visible mark reliably, export is blocked.

## No capability deadlock
ADVISORY exists so useful non-release intelligence work can continue without either lying about execution or refusing all work.

## Application boundary
The Streamlit/OpenAI code must enforce mode declarations and export marking. This Skill contract does not claim that the current application code already does so.


## Schema-versus-execution truth
A schema-valid `mode_declaration.json` is **necessary but not sufficient evidence that preflight actually executed**. Strings in `evidence_refs` cannot prove themselves. FULL_RUNTIME eligibility therefore requires runtime-verifiable preflight artifacts/request logs/hashes in addition to schema validity. Until application code performs that verification, the package makes no claim of runtime certification.
