# Production Element Instrumentation Contract

Executable QA requires every important production object to be machine-addressable.

## Required attributes
- Page: `data-rashad-page`, `data-page-mode`, `data-page-family`.
- Region: `data-region-id`, optional `data-region-role`.
- Node: `data-node-id`, `data-node-role`.
- Edge: `data-edge-id`, `data-source`, `data-target`, `data-directionality`, optional source/target anchors.
- Label: `data-label-id`, `data-label-for`.
- Layer: `data-layer-id`, `data-layer-role`, `data-layer-order`.
- Divider: `data-divider-id`, optional group/axis.
- Alignment: `data-align-group`, `data-align-axis`.
- Spacing sequence: `data-spacing-group`.
- Governed asset: `data-asset-id`, `data-asset-sha256`, `data-asset-policy`.
- Intentional overlap: `data-overlap-policy="ALLOW"` with reason.

Missing required instrumentation on an analytical/artifact page is a QA failure, not an excuse to skip the check.
