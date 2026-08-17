# Golden Master Underlay Fidelity Contract

STATUS: HARD PRODUCTION-FIDELITY AUTHORITY — v2.6.4.4

## Underlay identity
Every approved master has:
- `visual_master_id`;
- source file path;
- SHA-256;
- native width/height;
- approved crop = full canvas unless explicitly recorded;
- page/section IDs;
- Style Anchor lineage.

## Final projection
The production page uses the exact approved master bytes as a fixed full-canvas underlay or an explicitly approved deterministic crop. Do not regenerate the image at export time.

## Allowed overlays
Only governed native text, exact logos, source/evidence labels, page number, and accessibility/interaction metadata.

## Forbidden transformations
- repaint/recolor;
- AI edit after lock without new master ID;
- mirror;
- non-uniform stretch;
- hidden clipping of master content;
- format-specific redesign;
- replacing the master with a native card reconstruction.

## QA expectation
The runtime QA should verify master file hash/provenance and canvas placement in addition to normal text/brand/RTL checks.

## v2.6.4.6 executable checks
Use G13 for master hash/canvas placement and G14 for mirror/filter/clip/crop/aspect-ratio integrity. For GVM topology use the governed sidecar contract `81_GVM_SEMANTIC_TOPOLOGY_SIDECAR_CONTRACT.md`; do not add fake hidden DOM topology.

## v2.6.4.9 production-mode priority
This contract applies when `MASTER_MODE = GVM_RASTER_MASTER`. For the default `MASTER_MODE = HTML_SVG_MASTER`, the frozen browser-rendered HTML/SVG/CSS composition is the visual source of truth and cross-format parity is measured against its approved raster.
