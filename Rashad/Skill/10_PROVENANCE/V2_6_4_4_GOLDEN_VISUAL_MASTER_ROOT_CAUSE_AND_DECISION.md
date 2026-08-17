# v2.6.4.4 Root Cause & Strategy Decision

## Trigger
The v2.6.4.3 REDF test produced a visually weaker, card-heavy PDF even though the consulting/artifact knowledge was stronger. The strict image-isolation policy rejected full-page generated composition, forcing the available native renderer to reconstruct strong artifacts with generic primitives. Co-brand execution also failed visually: the client mark appeared weak and the two logos were not treated as one optical signature.

## Owner correction
- contextual Saudi flag and dashboard/device visuals are allowed;
- page-by-page image generation had previously produced stronger consulting visuals;
- long-deck generation must remain coherent beyond 20 pages and across continuation turns;
- exact logo alignment/strength and non-card artifact quality remain mandatory.

## Decision
Adopt a hybrid production strategy: full-page **Golden Visual Master** generation one page at a time, persistent anchor/continuity control, then exact native text/brand overlay. Reduce the native composer's role instead of asking it to redraw consulting artifacts from scratch.
