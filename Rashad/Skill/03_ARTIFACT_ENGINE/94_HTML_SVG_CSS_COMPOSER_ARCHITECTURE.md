# HTML/SVG/CSS Composer Architecture

## Source of truth
The approved `HTML_SVG_MASTER` is the default production visual master.

## Layer model
1. `canvas` — fixed 16:9 page;
2. `brand-layer` — exact logos / identity;
3. `content-layer` — native text;
4. `artifact-layer` — SVG + HTML composition;
5. `media-layer` — images/illustrations;
6. `annotation-layer` — callouts/evidence/source signals;
7. `footer-layer` — page/source controls.

## CSS token example
```css
:root {
  --rbx-magenta:#A42365;
  --ink:#1A1A1A;
  --secondary:#3D3D3D;
  --muted:#6F6F73;
  --hairline:#E6E2E4;
  --paper:#FFFFFF;
  --warm:#FAF9FA;
}
.slide { width:1920px; height:1080px; position:relative; overflow:hidden; }
```

Per-page semantic accent tokens may be activated only through the Rubix Artifact Palette governor.

## HTML vs SVG responsibilities
Use HTML/CSS for:
- typography;
- macro grids;
- tables where true tables are semantically correct;
- evidence panels;
- labels and annotations.

Use SVG for:
- flows;
- connectors;
- circles/rings;
- timelines;
- Gantts;
- networks;
- matrices with custom geometry;
- architecture bands;
- curves, braces and relationship overlays.

## Prohibitions
- div-only approximation of a relationship-rich artifact;
- responsive layout in production export;
- arbitrary border-radius/card styling as the universal component;
- decorative gradients/neon/glow without approved rationale;
- absolute-positioning every object before the macro composition has been approved.
