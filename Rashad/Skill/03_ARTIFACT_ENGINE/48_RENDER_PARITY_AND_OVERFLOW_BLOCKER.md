# Render Parity & Overflow Blocker

STATUS: HARD RELEASE BLOCKER

## Purpose
Stop false PASS outcomes where files open successfully but the exported page is visually or semantically different from the approved source model.

## Required render comparison
For each required format:
1. render the final page to pixels at the approved canvas ratio;
2. compare against the approved visual target and Artifact Signature;
3. inspect crop, geometry, text fit, topology, RTL/LTR, margins, brand and visual hierarchy;
4. record deviations by zone and severity.

## Automatic hard fails
- any off-canvas content;
- any clipped or hidden production content;
- any overlapping text not explicitly intended;
- any title/body/footer collision;
- any connector cropped at a container/page edge;
- any label detached from its node/edge;
- any wrong page size or aspect ratio;
- browser/office auto-scaling that changes composition;
- any uncontrolled responsive wrap;
- any font fallback causing materially different line count or hierarchy;
- any major image crop drift;
- any semantic topology loss;
- any wrong RTL sequence or co-brand order;
- any material HTML/PDF/PPTX divergence.

## Repair ladder
1. preserve thesis and Artifact Signature;
2. preserve topology and focal point;
3. repair local geometry;
4. repair text box dimensions / typography within approved limits;
5. rebalance whitespace;
6. split the page if density still exceeds capacity;
7. return to Artifact Architect if artifact family must change.

Never solve parity with global scale-down, clipping, hiding, or generic cards.
