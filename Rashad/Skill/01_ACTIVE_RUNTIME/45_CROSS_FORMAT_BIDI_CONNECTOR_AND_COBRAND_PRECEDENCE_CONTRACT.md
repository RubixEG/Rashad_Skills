# Cross-Format BiDi, Connector & Co-Brand Precedence Contract

STATUS: HARD ACTIVE RUNTIME CONTRACT — v2.6.4.3

## Page direction
`PAGE_DIRECTION = RTL | LTR` only.
Mixed content is represented by `directional_islands[]` / directional zones. There is no page-level `MIXED` state.

## BiDi
Every visible text node declares base direction and optional isolated runs. HTML/PDF/PPTX adapters must preserve the same logical string and expected visual run order for:
- Arabic + Latin acronyms;
- parentheses/brackets;
- slash-separated identifiers;
- URLs and emails;
- Arabic-Indic values adjacent to Latin units;
- technical IDs / ISO / API tokens;
- neutral punctuation.

## Connector semantics
Every edge defines stable ID, source node, target node, source anchor, target anchor, directionality, arrowhead ownership, route policy, and post-direction assertions. Endpoints are calculated after direction resolution.

## Co-brand precedence
1. Current explicit owner instruction.
2. Mandatory current RFP/client brand requirement, when explicitly evidenced.
3. Default Rashad rule: physical left-side `Rubix | Client`, Rubix far-left.
4. Current engagement deck may inform placement only when it is itself approved/evidenced as a mandatory current-engagement brand requirement; it does not independently override owner policy.

RTL never mirrors the co-brand signature.

