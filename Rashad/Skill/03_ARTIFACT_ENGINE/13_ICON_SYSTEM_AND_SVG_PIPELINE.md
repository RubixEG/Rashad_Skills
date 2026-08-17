# Rubix Proposal Icon System and SVG Pipeline

## Objective
Provide one coherent, reusable, editable icon family for proposal artifacts instead of mixing random icon libraries.

## Base standard
- SVG 1.1-compatible markup.
- `viewBox="0 0 24 24"`.
- transparent background.
- default `fill="none"`.
- `stroke="currentColor"`.
- stroke width `1.8`.
- round linecaps and joins.
- no text, raster images, filters, or external dependencies.

## Production workflow
1. Identify semantic need.
2. Reuse an approved icon when available.
3. Generate an icon concept only when the family lacks the concept.
4. Redraw/vector-clean the concept into the base standard.
5. Check optical alignment and recognizability at 18, 24, and 32 px.
6. Register icon ID, title, service line, and approved contexts.
7. Export as individual SVG and optional sprite symbol.

## PowerPoint behavior
Icons should be inserted as SVG or reconstructed as native paths where the compiler supports it. They must remain recolorable and independently selectable.

## Semantic rules
- icons guide scanning; they do not replace a full analytical artifact;
- use one icon per role, capability, or control block where helpful;
- do not use icons for every bullet;
- do not substitute an icon cloud for architecture, lifecycle, or decision logic;
- avoid culturally ambiguous or overly decorative symbols.

## Family governance
New icons must pass:
- stroke and geometry consistency;
- semantic clarity;
- light/dark contrast;
- Arabic RTL suitability;
- small-size readability;
- absence of embedded branding.
