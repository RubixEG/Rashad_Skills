# V2.6.4 Root Cause — Section Visual Parity & RFP Summary Depth

## Finding 1 — the generated visual and the native render were not the same design object
The generated multi-page image reasoned about several pages holistically. The later HTML/PDF was reconstructed from semantic page descriptions and therefore became a new composition rather than a faithful projection. This caused visual hierarchy, whitespace, focal scale, and section rhythm to drift.

## Finding 2 — page-by-page reconstruction loses section-level visual intelligence
When each page is composed independently, the renderer can optimize locally but still create a weak pack: repeated cards, small artifacts, inconsistent emphasis, and no visual narrative across neighboring pages.

## Finding 3 — fixed/simple HTML structures encouraged layout downgrade
HTML/PDF can be deterministic, but only if the geometry is frozen. Responsive layout primitives, automatic wrapping, font differences, and print reflow can change composition even when the content is correct.

## Finding 4 — the 24-role Summary architecture was correct but some roles were under-expanded
The problem was not missing role names. Dense roles such as BOQ, Team, Evaluation, Technical Requirements, Commercial Exposure, Risks, and Clarifications were compressed into high-level synthesis. The fix is a Depth Contract and dynamic multi-page expansion, not additional top-level roles.

## Corrective architecture
`Depth Contract → page analytical contracts → Golden Section Board → Section Visual Charter → frozen page visual targets → deterministic native geometry → fixed-canvas render → visual parity comparison → repair`

## Non-regression principle
V2.6.4 is additive. It does not delete or weaken V2.6.3 authorities, prompt corpus, scopes, mappings, councils, brand locks, cover rules, co-brand rules, Artifact Execution Proof, or completion gates.
