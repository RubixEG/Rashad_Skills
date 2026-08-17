# Text Fit & Font Preflight Engine

STATUS: HARD TYPOGRAPHY PRODUCTION AUTHORITY — v2.6.4.2

## Text-fit measurements
The runtime must evaluate actual rendered:
- text width;
- text height;
- line count;
- line/paragraph spacing;
- bounding box;
- available region;
- minimum font threshold;
- Arabic shaping;
- mixed-direction behavior.

`actual_text_height <= available_text_height` must be proven, not assumed.

## Fit-repair order
When content does not fit:
1. improve line breaking;
2. adjust local spacing inside approved tolerance;
3. expand the region if geometry permits;
4. rebalance secondary content without changing analytical hierarchy;
5. split the logical role into additional physical pages;
6. fail and return upstream.

## Forbidden fit strategies
- random font shrinking;
- font collapse below approved minimum;
- hidden/scrolling production text;
- removal of evidence or labels;
- clipping;
- replacing the artifact with a simpler family.

## Font preflight
Before rendering:
- required font is available;
- Arabic shaping support is verified;
- font metrics are verified;
- no silent fallback has occurred.

Silent font substitution that changes geometry is a hard blocker.
