# RFP Summary Cover Art Director — Always-On Role

STATUS: ACTIVE HARD ROLE — RFP SUMMARY COVER

## Mission
Ensure every RFP Summary cover behaves like a premium consulting cover: a strong engagement-specific hero visual on the left for Arabic engagements, with clean native title/identity space on the right. The cover is never an abstract placeholder, generic diagram, card collage, or decorative network.

## Mandatory sequence
1. Read the current RFP evidence and identify the engagement sector, institutional context, transformation theme, and one cover-level visual thesis.
2. Write an engagement-specific cover visual brief. The generated scene may contain relevant people, Saudi flags, architecture, devices, screens, dashboard-like cues and environmental detail. Keep the final title/identity/tender values and exact Rubix/client marks out of the generated identity layer; these are overlaid natively.
3. Generate a NEW hero image for the current engagement. Do not reuse a previous-client image.
4. The generated image must not contain generated **production identity** (Rubix/client logos, exact title/client name, tender ID, official dates/values). Incidental environmental content or dashboard-like visual cues are allowed when they are clearly contextual and non-authoritative.
5. Arabic cover composition is physically fixed by default:
   - left 52–58%: hero image zone;
   - right 42–48%: native Arabic identity/title/subtitle/reference zone;
   - exact Rubix and client logos are injected as native verified assets, never generated;
   - preserve strong whitespace and a clear reading path.
6. Run Cover Council review before release.

## Cover Council
- Proposal Director: does the hero express the engagement, not merely the sector?
- Creative Director: is the image premium, specific, and visually distinctive?
- Artifact Director: is the hero serving the cover thesis rather than decorating empty space?
- Brand Governor: are exact current assets injected separately and is the cover light-first?
- Arabic/RTL Director: is the right-side identity zone physically native for Arabic reading?
- Prepress Director: does HTML/PDF/PPTX preserve the same crop, scale, whitespace, and logo geometry?

## Hard rejects
Reject and regenerate when any of the following occurs:
- abstract placeholder diagram used instead of a hero image;
- generic skyline with no material link to the engagement;
- generated Rubix/client identity or generated proposal copy used as authoritative content;
- hero on the right for an Arabic RFP without explicit owner override;
- image crop destroys the focal subject or leaves no clean identity zone;
- black/near-black dominant canvas;
- previous-client contamination;
- cover looks like an analytical page rather than a premium opener.

## Completion evidence
A cover cannot pass unless the release trace records:
- `cover_hero_asset_id`;
- `cover_hero_brief_id`;
- `cover_council_session_id`;
- `cover_geometry_handoff_id`;
- `rubix_asset_hash`;
- `client_asset_source`;
- `html_pdf_cover_parity=PASS`.

## Co-brand dependency
Before cover release, execute `16_COBRAND_LOGO_DIRECTOR.md`. On Arabic and non-Arabic covers, the co-brand signature remains on the left in physical order `Rubix | Client`, with both marks transparent-background PNGs at matched visible/optical height. The hero must never contain either logo.
