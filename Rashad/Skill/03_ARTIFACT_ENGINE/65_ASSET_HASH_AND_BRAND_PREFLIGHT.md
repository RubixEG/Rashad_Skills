# Asset Hash & Brand Preflight

STATUS: HARD ASSET AUTHORITY — v2.6.4.2

## Required asset record
Every production asset should resolve with:
- `asset_id`
- `authority`
- `source`
- `sha256`
- `width`
- `height`
- `aspect_ratio`
- `alpha/transparency_state`
- `approved_status`
- `usage_policy`

## Logo checks
For Rubix/client logos:
- approved source/hash;
- contain mode;
- crop = 0;
- mirror = false;
- recolor = false;
- stretch = 0;
- aspect ratio preserved;
- clear-space rule preserved;
- optical-height/co-brand rule preserved;
- correct physical order.

## Prohibited sources
- generated logo;
- screenshot crop;
- reconstructed logo;
- remembered logo;
- old proposal mark used as current authority.

Asset failure blocks release; the renderer may not substitute a visually similar asset.

## v2.6.4.3 optical measurement
Co-brand optical-height matching must use `76_OPTICAL_LOGO_MEASUREMENT_ALGORITHM.md`; subjective visual matching alone is not sufficient production evidence.
