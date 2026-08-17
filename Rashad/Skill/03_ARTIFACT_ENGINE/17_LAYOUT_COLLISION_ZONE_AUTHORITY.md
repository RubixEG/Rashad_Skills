# LAY-COLL-002 — Independent Text-Zone Collision Authority

## Priority
Priority 0 visual-release authority. This rule strengthens the earlier general overflow/collision rules by defining **independent text zones** and executable collision behavior.

## Absolute rule
No title, body paragraph, number badge, icon, unit label, note, callout, source, or footer may visually occupy another independent element's reading zone.

A page is rejected if any independent zones intersect after final font loading in HTML, PDF raster, or editable PowerPoint.

## Mandatory component contract
A dense card or panel must allocate explicit zones for:
1. marker / number;
2. icon;
3. title;
4. body content;
5. unit / metric / evidence label;
6. annotation or note, when present.

Do not stack these zones using unrelated absolute positions. Prefer grid or explicit bounded slots.

## Resolution sequence
When content does not fit:
1. select a more suitable archetype;
2. reduce supporting copy without losing mandatory facts;
3. increase component height within the page budget;
4. redistribute the page or split it;
5. reduce typography only within approved minimum sizes.

Never hide the error with `overflow:hidden`, clipping, negative margins, transform offsets, or z-index changes.

## Hard fails
- title over body text;
- paragraph over unit label;
- badge or icon over title;
- note/callout over list content;
- footer or source over the page body;
- PDF collision absent in HTML but present after rendering;
- PPTX object boxes intersecting after export.

## Validation
Use bounding boxes after `document.fonts.ready`. Compare independent sibling zones, excluding ancestor/descendant relationships. Repeat after PDF rasterization and PowerPoint export.
