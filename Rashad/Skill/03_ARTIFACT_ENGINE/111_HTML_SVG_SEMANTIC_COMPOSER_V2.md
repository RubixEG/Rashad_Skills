
# HTML/SVG Semantic Composer v2

## DOM contract
Each analytical page uses semantic IDs:
- `data-page-role`
- `data-content-pack-id`
- `data-artifact-family`
- `data-artifact-node-id`
- `data-artifact-edge-id`
- `data-source-locator`
- `data-direction-zone`

## SVG connector model
Nodes render first. After font load and fixed layout, measure node rectangles and resolve anchor points. Generate connector paths in a dedicated SVG overlay. Store source/target IDs on each edge element.

## Label model
Prefer native HTML labels for Arabic/BiDi text positioned relative to measured SVG/node geometry. Text inside SVG is allowed only when shaping/direction equivalence is proven.

## Layout primitives
- editorial split;
- asymmetrical evidence grid;
- layered architecture;
- operating spine;
- timeline corridor;
- matrix + interpretation rail;
- evidence-to-decision chain;
- decision cockpit;
- dense evidence table;
- case-study proof composition.

No one primitive is universal.
