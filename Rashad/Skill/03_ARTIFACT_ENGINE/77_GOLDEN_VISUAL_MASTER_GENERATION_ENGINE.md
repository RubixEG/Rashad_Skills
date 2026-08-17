# Golden Visual Master Generation Engine

STATUS: APPROVED VISUAL-IDEATION / GVM FALLBACK MODE — superseded as default by v2.6.4.9

## Input
Consumes approved:
`Question → Thesis → Evidence → Relationship → Artifact Intent → Nodes/Edges → Artifact Family → Visual Depth → Page Family`.

## Output
One 16:9 generated visual master for one page.

## Prompt composition
Every generation brief contains:
- current page's analytical relationship and visual objective;
- semantic topology described visually, without asking the model to invent facts;
- Deck Visual DNA;
- Style Anchor references;
- Section Anchor reference;
- adjacent-page reference when available;
- exact focal/negative-space zones;
- native-overlay reserve zones;
- anti-card constraints;
- government/consulting tone;
- allowed contextual media.

## Reference-image priority
When the image environment supports reference images, use actual approved anchors rather than relying on descriptive prompt memory. For a normal page, preferred references are:
1. persistent Deck Style Anchor;
2. current Section Anchor;
3. previous approved page master;
4. optional same-family anchor.

## Page-by-page rule
Generate one page master at a time. Do not request an entire 20+ page deck in one image-generation call.

## Batch continuity
Operational batches are normally 4–6 pages. After each batch, run Deck Continuity Council before continuing.

## Regeneration scope
If one page drifts, regenerate that page using the same anchors. Do not restyle the whole deck.

## v2.6.4.9 role
This engine may now act as a **visual concept/reference generator** before HTML/SVG/CSS authoring, as well as a fallback official GVM mode. The output does not force raster production when a stronger governed HTML master can reproduce the concept.
