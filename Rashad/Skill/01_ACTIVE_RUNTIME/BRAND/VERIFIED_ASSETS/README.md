MODULE: VERIFIED_ASSETS_INDEX
STATUS: POINTER_ONLY — NO BINARY ASSET COPIES
LOAD WHEN: Verifying Rubix identity or current client co-brand assets.
DEPENDS ON: `01_ACTIVE_RUNTIME/BRAND/DECK_AUTHORITY.md`; `01_ACTIVE_RUNTIME/BRAND/DESIGN_TOKENS.md`; current engagement source register.
DO NOT APPLY TO: Treating a filename, historical deck, generated image, or stale ZIP asset as automatically current.
SUPERSEDES: Logo generation, prior-client logo reuse, and unverified asset substitution.

# Verified assets protocol

This Markdown-only package intentionally does not duplicate binary logos, fonts, decks, or client assets.

Before use, record:

- exact asset path and checksum where available;
- owner/source and approval status;
- current client identity;
- aspect ratio, transparency, and clear-space checks;
- whether the asset is current, stale, reference-only, or blocked.

Rubix brand binaries remain separate. Client logos belong to the current engagement and must never become permanent cross-engagement sources. Missing verification blocks co-branding.
