# 49 — V6 Unified Release & QA Director

**Status:** ACTIVE — NO-WAIVER production authority

A capability existing in documentation or source code does not mean it ran. Release is valid only when one unified QA run emits evidence for every required gate.

## Unified QA contract
The production runtime must invoke one release path that covers:
- schema + referential validation;
- evidence/content checks;
- artifact-truth checks;
- consulting-exhibit quality checks;
- canvas/bounds/overflow/line-fragment/collision checks;
- owner/anchor/alignment/spacing/padding/divider/layer/z-index checks;
- font/glyph/type-scale/contrast/palette/logo checks;
- structural RTL/BiDi and directional-island checks;
- expected nodes/edges/endpoints/labels/topology checks;
- final screenshot pixel inspection;
- Arabic and structural stress matrix;
- repair-safety signature comparison when repair occurred;
- deck anti-template / rhythm / repetition checks;
- PDF and PPTX parity against the same approved final page masters.

`PASS` is illegal when a required gate measured zero applicable objects. `NOT_EXECUTED` and runtime inability are release blockers, not qualified passes.
