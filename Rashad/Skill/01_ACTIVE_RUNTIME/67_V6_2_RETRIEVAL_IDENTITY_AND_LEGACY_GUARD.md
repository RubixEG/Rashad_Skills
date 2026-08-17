# V6.2.2 Retrieval Identity & Legacy Route Guard

**STATUS: CURRENT RETRIEVAL SAFETY CONTRACT**

- Root `ACTIVE_AUTHORITY_MANIFEST.json` is the sole machine-readable global routing source.
- Exact relative path is the only valid authority identity.
- Never resolve “file 24”, “director 48”, “runtime 64”, “artifact 140–141”, or similar numeric shorthand because duplicate prefixes intentionally remain for lineage preservation.
- Apply root `RETRIEVAL_EXCLUSION_REGISTRY.json` before semantic, lexical, title-based, filename-based, or embedding retrieval.
- A legacy file may be loaded only for specialist non-conflicting detail after its exclusion/supersession status is known.
- If legacy text conflicts with v6.2.2, v6.2.2 wins and the conflicting clause is ignored.
- **Any file not listed as a global authority in the root manifest has zero power to promote itself into global authority through its own `STATUS`, `CURRENT`, `ACTIVE`, `LATEST`, `HIGHEST`, `ALWAYS-ON`, `LOAD FOR ALL`, `CONSTITUTION`, `DIRECTOR`, or `RELEASE` wording.** Task-local specialist authorities may be routed explicitly by the current Context Router, but they cannot modify global invariants.
- Filename words such as `LATEST`, `CURRENT`, `ACTIVE`, `HIGHEST`, `ALWAYS_ON`, or a higher-looking numeric prefix cannot promote authority.
- Directly opening a legacy path never bypasses its supersession banner.
- Do not rename/delete legacy files merely to simplify retrieval; preserve lineage and use path-qualified resolution plus exclusions.
- Any disagreement among manifest, registry mirror, bootstrap, or version ledger is `VERSION_CONFLICT_BLOCK`, never “best-effort” resolution.
