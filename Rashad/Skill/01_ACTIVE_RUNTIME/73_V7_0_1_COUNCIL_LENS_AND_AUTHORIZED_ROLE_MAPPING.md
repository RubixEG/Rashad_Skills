# V7.0.1 — Council Lens & Authorized Runtime Role Mapping

**STATUS: LINEAGE / COMPATIBILITY ONLY — current routing uses `73_V7_COUNCIL_LENS_AND_AUTHORIZED_ROLE_MAPPING.md` under v7.0.2**

V7 executive/government/consulting names are **analytical lenses / question bundles**, not a second runtime role registry. The only runtime role IDs are the 29 verified `ROLE-*` identities in `01_ACTIVE_RUNTIME/09_COUNCILS_AND_ROLES.md`.

`council_lens_registry_v7_0_1.json` maps every V7 lens to one or more authorized runtime roles. The router may activate a lens only when that mapping exists. Unknown lens → `BLOCK_COUNCIL_ROUTE_UNRESOLVED`.

An executive lens (for example CEO/GM or CFO) means "challenge the object from this decision perspective"; it does **not** claim that a literal CEO/CFO runtime persona exists. For Independent Judge / Release functions, invocation/context independence remains mandatory even where the mapped `ROLE-*` identities overlap producer-side expertise.

No lens label can increase the authorized runtime role count, grant release authority, or bypass the Council Session/Finding/Approval ledgers.
