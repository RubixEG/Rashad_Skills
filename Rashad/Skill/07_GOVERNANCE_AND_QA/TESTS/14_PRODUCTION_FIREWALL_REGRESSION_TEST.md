# 14 — Production Firewall Regression Test

STATUS: HARD GATE — v2.1

A build fails if any test below fails.

## Logo
- A prompt saying “generate a Rubix-branded slide” must **not** cause the image model to create the logo.
- Exact consulting logo bytes must be injected from `08_BRAND_CURRENT/assets/rubix-consulting-current-light.png`.
- Recreated, typed, remembered, screenshot-derived, or generated logos = FAIL.

## Full-slide image
- Image model may produce hero/illustration only.
- Any generated image containing production title/body/labels/logo/page number/table/timeline/analytical diagram = FAIL.

## Arabic RTL
- First ordered item physically rightmost.
- Timeline/process direction is RTL unless a source-specific exception is explicitly justified.
- Latin acronyms stay internally LTR.

## Numerals
Arabic natural-language content must render `٠١٢٣٤٥٦٧٨٩`.

Fail examples: `24 موردًا`, `30 نموذجًا`, `12 شهرًا`, `70%` inside Arabic prose.
Pass examples: `٢٤ موردًا`, `٣٠ نموذجًا`, `١٢ شهرًا`, `٧٠٪`.

Exact URLs/emails/code/hashes/reference identifiers may retain raw digits where alteration would break correctness.

## Theme
- Black/near-black full-slide background = FAIL.
- Legacy dark master fallback = FAIL.

## Runtime honesty
If a deterministic composer is unavailable, expected result is `BLOCKED — DETERMINISTIC RASHAD PRODUCTION COMPOSER NOT AVAILABLE`, not a generic full-slide image.
