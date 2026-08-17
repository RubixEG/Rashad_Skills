# Rubix Artifact Palette — Hard Color Authority

STATUS: CURRENT ARTIFACT PALETTE — USER-REQUESTED 2026-08-11
OWNER: Theme & Color Governor

The palette is derived from verified Rubix brand colors but adapted for a **light-first consulting artifact system**. It is not permission to use every color on every page.

## 1. Hard canvas rule

Allowed full-slide canvases:
- `#FFFFFF` — White, primary canvas
- `#FAF9FA` — Warm neutral light (artifact extension)
- `#F8EDF3` — Magenta 8% tint
- `#F5EEF5` — Purple 8% tint, conditional
- `#F0F4FA` — Blue 8% tint, conditional
- `#EBF4F5` — Teal 8% tint, conditional

**Forbidden:** `#000000`, `#0F0F12`, near-black, deep navy, deep magenta, or any dark full-slide background. No black background slides. This is a hard release gate unless the user explicitly changes the rule.

## 2. Core identity
- Brand anchor / thesis / active navigation: `#A42365` Magenta
- Primary text: `#1A1A1A`
- Secondary text: `#3D3D3D`
- Muted/meta: `#6F6F73`
- Hairline: `#E6E2E4`
- White: `#FFFFFF`

## 3. Semantic accent colors
Use only when the information relationship benefits from differentiation.

| Semantic use | Strong | 15% tint | 8% tint |
|---|---|---|---|
| Brand / primary emphasis | `#A42365` | `#F1DEE8` | `#F8EDF3` |
| Innovation / AI / transformation | `#822B83` | `#ECDFEC` | `#F5EEF5` |
| Operations / process / sustainability | `#077381` | `#DAEAEC` | `#EBF4F5` |
| Data / evidence / information | `#407ABE` | `#E2EBF5` | `#F0F4FA` |
| Attention / deadline / cost driver | `#F15A26` | `#FDE6DE` | `#FEF2EE` |
| Critical risk / failure / non-compliance | `#D32A45` | `#F8DFE3` | `#FBEEF0` |
| Governance / institutional anchor | `#203B70` | `#DEE2EA` | `#EDEFF4` |

## 4. Usage law
- One page normally uses **one brand anchor + at most one semantic accent family**.
- Multi-workstream diagrams may use up to 4 semantic colors only when color encodes stable meaning.
- Magenta remains the brand anchor; secondary colors must not compete with the page thesis.
- Avoid rainbow charts, arbitrary color cycling and decorative color.
- No gradients by default. A photographic/image gradient for readability is allowed only as an overlay treatment, not as a brand palette.
- Red is reserved for genuine risk/failure; orange for attention/cost/time; do not use either decoratively.
- Prefer tints for fields/cards/backgrounds and strong colors for nodes, labels, connectors and highlights.

## 5. Legacy color normalization
Old deck variants such as `#A32365`, `#A21D62`, `#9C0454`, `#DE2E79` are treated as historical template drift. New Rashad artifacts normalize the primary brand anchor to **`#A42365`** unless a current asset itself requires another exact pixel value.

## 6. Theme & Color Governor hard gate
Release fails when:
- a full-slide black/near-black/dark canvas appears;
- an unapproved hex appears without a documented visual reason;
- old client colors contaminate a new engagement;
- secondary accents exceed their semantic role;
- color is used as decoration without analytical meaning;
- logo color is altered;
- theme changes artifact meaning or weakens evidence hierarchy.

## v2.6.4.9 HTML/SVG integration
Expose palette values as CSS variables, but activate only the page's approved semantic accent family. A page may not use the full palette merely because the variables exist. The default visual target is white/off-white + charcoal + Rubix magenta + at most one semantic accent family.
