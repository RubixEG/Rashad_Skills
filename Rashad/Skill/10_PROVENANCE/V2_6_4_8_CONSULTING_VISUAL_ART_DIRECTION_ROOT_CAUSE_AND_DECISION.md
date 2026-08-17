# V2.6.4.8 Root Cause and Decision Record

## Why this release exists
The quality gap was not caused mainly by renderer capability. The larger issue was **pre-generation visual reasoning drift**:
- Rashad described pages in analytical terms that the image model interpreted as generic tech infographics;
- the model was not consistently conditioned with accepted MWAN/current-deck references;
- the palette was under-governed, allowing excessive colors;
- the system moved too directly from artifact logic to page generation without concept competition;
- deck-level rhythm and page role were under-governed.

## Decision
Do not abandon the image-first Golden Visual Master approach. Strengthen it through:
1. consulting visual art direction;
2. concept competition before generation;
3. reference-conditioned generation;
4. palette/color-budget governance;
5. deck-rhythm governance;
6. explicit cover-left editorial hero lock.

## Expected result
Bring Rashad's generated visuals materially closer to the consulting-grade outputs historically achieved through direct page-by-page image generation, while preserving governance and QA discipline.
