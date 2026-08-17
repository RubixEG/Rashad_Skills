# SEC-DEP-001 — Bid Strategy / Dependency Gate Test

STATUS: ACTIVE REGRESSION TEST — v2.5

1. Approved RFP Summary without Bid Strategy approval keeps proposal workstreams that depend on Bid Strategy blocked.
2. Bid Strategy approval makes every proposal node eligible **only when its own material dependencies are ready**.
3. Reader numbering does not create a dependency: Section 4 may draft before Section 3 approval when the Dependency Ledger shows no material dependency between them.
4. If Section 4 depends materially on an approved/locked output from Section 3, it remains blocked until that dependency is satisfied.
5. Executive Summary and CEO Letter remain late-synthesis nodes because their Dependency Ledger entries require stabilized upstream proposal content, not because of section numbering.
