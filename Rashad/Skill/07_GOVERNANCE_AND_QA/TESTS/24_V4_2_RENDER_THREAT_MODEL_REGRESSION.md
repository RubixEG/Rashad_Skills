# Test 24 — v4.2 Render Threat Model Regression

Permanent defect families: header collision; line-fragment overlap; clipped glyph; masked overflow; off-canvas; semantic-parent escape; spacing drift; alignment drift; padding collapse; flex shrink; overscale/underscale; owner/badge drift; z-index occlusion; hidden opacity; mirror/rotate/clip transform; missing node; missing/reversed/detached edge; orphan label; connector-label collision; RTL sequence reversal; font fallback; tofu; table-cell overflow; dense table shrink; bad hero crop; logo aspect/optical mismatch; debug leakage; card-spoof system; visual imbalance; unstable repeat render; 1080p-only master; PDF/PPTX parity drift; required gate with zero testable objects.

Every confirmed production defect must map to a fixture and remain permanently in regression.
