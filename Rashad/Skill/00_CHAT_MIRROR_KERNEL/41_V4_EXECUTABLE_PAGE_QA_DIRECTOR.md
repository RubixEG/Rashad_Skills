# V4 Executable Page QA Director

Production QA is a machine-assisted inspection of the actual rendered page.

Required dimensions:
- page size / safe area;
- text run bounds and scroll overflow;
- hidden/masked overflow;
- unrelated element collisions;
- region containment;
- z-index and visual occlusion;
- alignment/grid/spacing rhythm;
- divider placement;
- font availability and no silent substitution;
- glyph/text corruption signals;
- RTL/LTR/BiDi structure;
- node existence and location;
- edge existence and endpoint attachment;
- arrowhead ownership/direction;
- label attachment;
- governed image/logo transforms;
- palette and surface luminance;
- card-dominance downgrade;
- whole-page balance/density;
- internal/debug metadata leakage;
- deterministic repeated render;
- stress mutation tolerance;
- final PDF/PPTX raster parity.

A single hard failure blocks release.
