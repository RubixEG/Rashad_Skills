# Theme & Color Hard Lock

## Role: Theme & Color Governor

This is an executed blocking role under the Artifact / Brand / RTL Production Council.

Responsibilities:
1. Load `RUBIX_ARTIFACT_PALETTE.md` before any client-facing rendering.
2. Reject black/near-black full-slide backgrounds.
3. Reject legacy deck colors/layouts that conflict with current light-first authority.
4. Validate one-anchor/one-semantic-accent discipline.
5. Validate logo asset provenance and physical geometry.
6. Ensure secondary colors encode meaning rather than decoration.
7. Prevent safety repairs from changing artifact meaning.

Release metric: `theme_color_governor = PASS` is mandatory for every rendered artifact.

## v2.1 release dependency
Theme/Color Governor runs inside `29_PRODUCTION_EXECUTION_FIREWALL.md`; its failure blocks the render action itself, not only final release.


## v2.2 deterministic background test
For an sRGB background color with channels 0–255: normalize `c = channel/255`; linearize `c_lin = c/12.92` when `c ≤ 0.04045`, otherwise `((c+0.055)/1.055)^2.4`; compute WCAG relative luminance `Y = 0.2126 R_lin + 0.7152 G_lin + 0.0722 B_lin`.

`near-black = Y ≤ 0.04`. A dominant full-slide/page background meeting this threshold is a hard fail. This mathematical threshold does not authorize other dark full-slide treatments; the Rubix artifact system remains light-first.
