# Current Rubix Logo Routing Authority

## Embedded approved assets
- `assets/rubix-master-current-light.png` — use when the deliverable represents Rubix as a whole or multiple sub-brands.
- `assets/rubix-consulting-current-light.png` — default for consulting proposals when Rubix Consulting is the submitting entity.
- `assets/rubix-connect-current-light.png`
- `assets/rubix-studio-current-light.png`
- `assets/rubix-analytica-current-light.png`
- `assets/rubix-accelerator-current-light.png`
- `assets/rubix-beyond-current-light.png`
- `assets/rubix-official-device-current.png` — secondary motif only; never a substitute for the full logo.

## Hard rules
- Never generate a Rubix logo.
- Never reuse a logo from historical proposal screenshots/PDFs.
- Never recolor or mirror the logo.
- Default Rashad canvas is light; therefore the light-background logo variants are authoritative for core production.
- The client logo is engagement-specific, validated separately, and must not be permanently stored in the core skill.
- Co-brand physical signature: **Rubix left | Client right** by default. Override precedence is: current explicit owner instruction → mandatory current-RFP/client brand requirement when explicitly evidenced → house default. A supplied engagement deck may override only when it is approved evidence of a mandatory current-engagement brand requirement; it does not independently override owner policy. Do not mirror solely because content is RTL.

## v2.1 injection gate
The logo is a **production asset**, never a semantic prompt instruction. Telling an image model “use the Rubix logo” is prohibited. The composer must load the exact file bytes from the selected asset path.

For consulting proposals, default to `assets/rubix-consulting-current-light.png`. If the runtime cannot place that exact asset as a separate object/layer, branded production is blocked. Approximate text, recreated marks, screenshot crops, and generated logos are not fallbacks.


## v2.2 provenance and geometry validation
Do not compare resized rendered pixels to the source asset byte-for-byte. Validate:
- source file SHA-256 provenance before placement;
- logical asset ID and submitting Rubix entity;
- aspect-ratio drift ≤ 0.5%;
- crop = 0, mirror = false, recolor = false;
- clear space ≥ 0.25 × visible logo height on each side unless a stricter source rule is known;
- visible full-wordmark height ≥ 0.28 in on a 16:9 slide or equivalent legibility floor;
- no safe-area/footer collision.

## v2.6.3 deterministic co-brand signature
For every branded client-facing page, the authoritative physical signature is:
`Rubix logo | Client logo`

- cluster location = left;
- Rubix = far-left / first mark;
- client = to the right of the separator;
- RTL does not mirror the signature;
- both production assets must be PNG with transparent background;
- normalize by visible/optical height, target ratio `0.98–1.02`;
- preserve aspect ratio, crop=0, mirror=false, recolor=false, stretch=0;
- client logo is engagement-specific and must carry source/provenance plus a production-asset hash;
- if a verified transparent client PNG cannot be produced without altering the visible mark, final branded release is blocked.
