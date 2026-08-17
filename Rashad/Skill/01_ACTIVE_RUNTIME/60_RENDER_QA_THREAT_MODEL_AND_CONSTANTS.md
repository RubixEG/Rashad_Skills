# Render QA Threat Model & Constants

STATUS: HARD PRODUCTION CONTRACT

## Failure surfaces
Every production page must be evaluated across all applicable surfaces:
1. Canvas / viewport / safe areas.
2. Header stack and title reflow.
3. Text line fragments, wrapping, glyphs, baseline and line-height.
4. Font resolution, fallback and font-metric drift.
5. Overflow, masked overflow, clipping and ellipsis.
6. Element collision, containment and parent/region escape.
7. Alignment, padding, margin, gap and spacing rhythm.
8. Micro-element owner/anchor containment: badges, KPIs, icons, markers, chips, footnotes.
9. Layer/z-index/opacity/occlusion.
10. Transforms: scale, translate, rotate, mirror, clip-path, filter.
11. Nodes / edges / labels / topology truth.
12. Connector endpoint, direction, arrowhead, route, branch and label placement.
13. RTL/LTR/BiDi, ordered sequence and mixed-direction islands.
14. Dividers, rails, grids and separators.
15. Tables, matrices, charts, legends and dense evidence blocks.
16. Images, hero crops, logos, aspect ratio, optical bounds and transparency padding.
17. Card dominance and fake higher-order-artifact declarations.
18. Whole-page visual mass, density, focal hierarchy and whitespace balance.
19. Debug/internal metadata leakage.
20. Deterministic repeat render / late-font race.
21. Stress mutation response.
22. Final master raster quality.
23. PDF/PPTX parity from the same master.

## No finite bug list is sufficient
Any newly discovered defect becomes a regression fixture. Metamorphic stress is required to expose unknown combinations rather than waiting for a production sample.
