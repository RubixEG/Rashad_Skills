# Deterministic Rashad Retrieval Authority — v2.2

The immutable master document remains the provenance source. Runtime execution retrieves **one exact sharded Markdown file by ID**, not a reconstructed prompt from title/semantic memory.

## R-code execution
1. Resolve exact code, e.g. `R-313`.
2. Load `PROMPTS/R-313.md`.
3. Optionally verify its SHA-256 and master line/byte range in `R_CODE_INDEX.md`.
4. Execute the exact body; never paraphrase/reconstruct.

## Scope execution
1. Resolve scope ID, e.g. `K-01`.
2. Load `SCOPES/K-01.md` for exact scope definition.
3. Load `MAPPINGS/K-01.md` for the exact six-phase playbook.
4. Retrieve each listed R-code from `PROMPTS/`.

## Integrity
Expected counts: `388 prompts`, `96 scopes`, `96 scope mappings`. Missing/duplicate IDs block exact-prompt execution.

No Python/JSON runtime index is required; filenames + Markdown indexes are the deterministic retrieval contract.
