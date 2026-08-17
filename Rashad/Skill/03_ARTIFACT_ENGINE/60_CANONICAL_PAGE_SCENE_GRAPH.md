# Canonical Page Scene Graph

STATUS: HARD FORMAT-MASTER CONTRACT — v2.6.4.2

## Purpose
Provide one canonical object model from which HTML, PDF, and PPTX adapters project the same page rather than redesigning independently.

## Required primitive families
- `TextNode`
- `ShapeNode`
- `ImageNode`
- `ConnectorNode`
- `GroupNode`
- `TableNode`
- `ChartNode`
- `IconNode`
- `ArtifactNode`
- `RegionNode`
- `BrandNode`
- `SourceNode`

## Required properties per object
At minimum:
- stable object ID;
- semantic purpose;
- parent group;
- logical order;
- direction policy;
- mirror policy;
- geometry (`x`, `y`, `width`, `height` after direction resolution);
- z-order;
- safe bounds;
- style token;
- visibility;
- evidence/source relationship where applicable.

## Logical coordinates first
Semantic layout should prefer:
`START`, `END`, `INLINE_START`, `INLINE_END`, `FLOW_START`, `FLOW_END`

Physical left/right coordinates are resolved only after page/component direction is known.

## Adapter rule
HTML/PDF/PPTX adapters consume the same resolved scene graph. An adapter cannot:
- reorder semantic nodes;
- change the artifact family;
- recalculate a different information hierarchy;
- invent a fallback layout;
- independently reinterpret RTL.

## v2.6.4.9 scene-graph timing
The resolved physical scene graph is a **post-concept production freeze**. During visual search, Rashad uses semantic nodes/edges plus the Visual Thought Board; it does not force every concept into fixed x/y coordinates before art-direction approval.
