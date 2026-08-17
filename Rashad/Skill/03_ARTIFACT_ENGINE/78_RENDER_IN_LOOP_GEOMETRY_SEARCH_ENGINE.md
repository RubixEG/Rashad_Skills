# 78 — Render-in-the-Loop Geometry Search Engine

Do not render once and repair until it fits. Search.

## Loop
`hypothesis → geometry candidate → render → DOM/pixel metrics → visual critic → mutate → rerender`.

Critical pages should compare multiple geometry candidates where the runtime supports it. Geometry score considers:
- collision / overflow;
- edge crossings and connector length;
- label-to-owner distance;
- visual mass balance;
- dominant-form prominence;
- RTL reading path;
- evidence-to-claim proximity;
- whitespace distribution;
- font legibility;
- card repetition;
- reference grammar compliance.

Freeze geometry only after the winning candidate passes Artifact Truth and CEQS thresholds.
