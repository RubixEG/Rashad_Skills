# Co-Brand Logo Director — Always-On Production Role

STATUS: ACTIVE HARD ROLE — ALL BRANDED CLIENT-FACING ARTIFACTS

## Mission
Guarantee a stable, exact and repeatable Rubix + Client co-brand signature on every branded client-facing page. Logo placement is a deterministic production responsibility and must never be delegated to image generation or inferred from RTL direction.

## Mandatory physical signature
Use this physical order on the **left side** of the page:

`RUBIX LOGO  |  CLIENT LOGO`

Rules:
- Rubix is the **far-left** logo.
- A thin neutral separator sits between the two marks.
- The client logo sits immediately to the right of the separator.
- RTL content does **not** mirror or reverse this physical logo order.
- The co-brand cluster remains left-aligned on covers and normal branded pages unless the owner explicitly overrides the arrangement for the current engagement.

## Asset format lock
Both logos must be production PNG assets with transparent backgrounds:
- Rubix: exact approved current PNG from `08_BRAND_CURRENT/assets/`.
- Client: engagement-specific verified transparent-background PNG.
- Alpha/transparency must be preserved; no white rectangle or baked background is permitted.
- If the only client source has a solid background, a transparent PNG production derivative may be prepared only when the visible mark can be preserved exactly. Record the source and derivative hash. If exact extraction cannot be guaranteed, final branded release is blocked.
- Never use a generated logo, screenshot crop, web reconstruction, text recreation or remembered mark.

## Size and geometry lock
- Match **visible/optical logo height**, not raw image-canvas height or transparent padding.
- Target visible-height ratio: `0.98–1.02` between Rubix and Client unless the client's official brand standard requires a stricter optical adjustment.
- Preserve each logo's original aspect ratio.
- `contain` only; never `cover`.
- crop = 0.
- mirror = false.
- recolor = false.
- stretch/distortion = 0.
- Align by optical center/baseline so the two marks read as one co-brand signature.
- Transparent padding may be ignored/trimmed for measurement, but external clear space must still satisfy the current brand authority.

## Required QA evidence
Every branded release trace must record:
- `cobrand_role_executed = TRUE`;
- `rubix_asset_path`;
- `rubix_asset_sha256`;
- `rubix_png_rgba_or_alpha = PASS`;
- `client_asset_source`;
- `client_asset_sha256`;
- `client_png_transparency = PASS`;
- `physical_order = RUBIX_LEFT__CLIENT_RIGHT`;
- `cluster_location = LEFT`;
- `separator_present = TRUE`;
- `visible_height_ratio`;
- `aspect_ratio_drift <= 0.5%`;
- `crop = 0`;
- `mirror = false`;
- `recolor = false`;
- `generated_logo_detected = FALSE`.

## Blocking conditions
Final branded release is blocked when:
- either logo is missing where co-branding is required;
- the client logo is not a verified transparent PNG production asset;
- Rubix is not first/far-left;
- RTL mirroring reverses the logo order;
- visible logo heights materially differ;
- either logo is stretched, cropped, recolored, mirrored or generated;
- a baked white/background rectangle is visible around either mark.

## Scope
This role governs logo placement only. It does not change current factual, Artifact Intelligence, Arabic/RTL, theme/color, or proposal authorities.

## v2.6.4.3 override precedence
Default remains physical left-side `Rubix | Client`. Override precedence: (1) current explicit owner instruction; (2) mandatory current RFP/client brand requirement when explicitly evidenced; (3) default Rashad signature. A supplied deck alone is not an override unless it is approved evidence of a mandatory current-engagement requirement. RTL never reverses the signature.
