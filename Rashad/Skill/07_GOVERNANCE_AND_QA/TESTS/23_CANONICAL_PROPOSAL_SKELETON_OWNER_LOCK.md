# Test 23 — Canonical Proposal Skeleton Owner Lock

STATUS: HARD REGRESSION SPECIFICATION — v2.6.4.5

## Required assertions
1. English and Arabic canonical files contain the same structural IDs: `0`, `1`, `2.1–2.5`, `3.1–3.4`, `4.1–4.7`, `5.1–5.4`, `6.1–6.3`, `7.1–7.3`, `8.1–8.3`.
2. Cover and Table of Contents precede Section 0.
3. Appendices remain Section 7.
4. Commercial Proposal remains Section 8.
5. Close / Contact remains after Section 8.
6. RFP mandatory forms may be supplemental or mapped, but cannot automatically rename/reorder/delete canonical IDs.
7. Any unresolved legal structure conflict returns `STRUCTURE_CONFLICT_BLOCK`.
8. `rubix-proposal-master-skeleton-v2.md` cannot override canonical section architecture.
9. Arabic and English wording may differ stylistically but must remain semantically aligned by ID.
10. Any future automatic skeleton rewrite without a new explicit owner instruction is FAIL.
