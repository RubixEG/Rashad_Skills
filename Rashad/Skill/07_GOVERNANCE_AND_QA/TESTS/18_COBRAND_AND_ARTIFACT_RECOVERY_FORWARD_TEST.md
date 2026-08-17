# Co-Brand Logo & Artifact-Recovery Forward Test

STATUS: BLOCKING REGRESSION TEST

## Test A — Arabic RFP Summary cover
Expected:
- new engagement-specific hero image, text/logo/number/fact free;
- hero occupies the approved left-side visual zone without containing logos;
- native co-brand signature is a separate layer on the left;
- physical order `Rubix | Client`, Rubix far-left;
- both assets are transparent PNGs;
- visible-height ratio is within `0.98–1.02` unless stricter client-brand guidance is documented;
- title/identity remains native and physical RTL;
- HTML/PDF/PPTX projections preserve logo order, scale and transparency.

## Test B — Normal branded analytical page
Expected:
- same co-brand signature remains on the left;
- no RTL reversal;
- no generated/screenshot logo;
- no visible white rectangle around either mark;
- aspect ratio and crop checks pass.

## Test C — Weak artifact recovery
Provide a page rendered as generic cards despite a dependency/system relationship.
Expected:
- release blocked;
- v2.6.2 recovery prompt invoked;
- Artifact Execution Proof gate requires full trace;
- page returns to Artifact stage and is redesigned;
- file existence does not produce PASS.
