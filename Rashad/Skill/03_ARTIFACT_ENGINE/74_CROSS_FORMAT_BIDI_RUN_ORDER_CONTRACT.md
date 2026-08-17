# Cross-Format BiDi Run-Order Contract

STATUS: HARD TYPOGRAPHY/DIRECTION CONTRACT — v2.6.4.3

## Canonical text representation
Each `TextNode` carries:
- `logical_text`;
- `base_direction = RTL | LTR`;
- `runs[]` with `run_id`, text, language/script, direction, isolation policy;
- `expected_visual_run_order[]` for regression evidence where mixed direction is material.

## Required cases
Define and test run order for:
- Arabic sentence with `(API)` / `(ISO 27001)`;
- Arabic + URL/email;
- Arabic-Indic number + `GB`, `API`, `KPI`, `%`, `/`;
- parentheses/brackets around LTR identifiers;
- colon/dash/slash neutral punctuation;
- technical IDs that must remain byte-for-byte LTR.

## Cross-format invariant
HTML, PDF and PPTX must preserve the same logical text and materially equivalent visual run order. If an adapter cannot preserve the required order, the affected text node fails production parity.

## Prohibition
Do not fix BiDi by reversing string contents. Do not treat right alignment as evidence of correct BiDi.

