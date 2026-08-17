# Current Brand & Deck Forensic Audit — 2026-08-11

## Sources inspected
- `rubix-brand(20260811-103333).skill`
- `rubix-deck(20260811-103315).zip`
- Arabic and English proposal templates contained in the brand skill

## Brand package inventory
The brand skill contains 63 entries including current master/sub-brand logos, brand/background imagery, Arabic/English proposal templates, font binaries, 2026 corporate brochures and brand guideline material.

### Migration decision
**EXTRACT, DO NOT EMBED WHOLE PACKAGE.** The portable Rashad core keeps normalized knowledge and approved light-background logo/device assets only. PDFs, fonts and PPTX templates are excluded.

## Proposal template inspection
Both Arabic and English proposal templates contain:
- 55 slides
- 2 masters
- 19 layouts
- 16:9 canvas (`12192000 × 6858000` EMU)
- cover, disclaimer/menu, multiple divider layouts and standard content layouts

### Visual findings
The templates contain strong current Rubix identity cues, but also behaviors that would damage the user-approved Artifact-first system if treated as rigid production authority:

1. **Dark cover/divider dependence.** Several templates use deep magenta/black fields. This conflicts with the user hard rule: no black/near-black slides.
2. **Magenta drift.** Template fills include several near-magenta values such as `#A32365`, `#9C0454`, `#DE2E79`, `#A21D62`, while the current brand guideline identifies `#A42365` as the primary magenta. Rashad normalizes the brand anchor to `#A42365`.
3. **Template-first risk.** The deck provides named divider/content layouts, but Rashad must select an information relationship/artifact before composition; it must never choose a page because a layout already exists.
4. **Useful light-page grammar.** White/light pages demonstrate useful hierarchy, table discipline, section navigation, image framing and magenta emphasis. These may be abstracted as visual grammar.
5. **Typography evidence.** Montserrat / Montserrat Arabic are the intended families. Font files are intentionally not included in the portable skill.

## Deck ZIP inspection
The `rubix-deck` archive contains 87 entries including Python builders, a fixed proposal implementation, CSS/rendering logic, appendix data/images, logos/fonts and sub-skills.

### Migration decision
- **KEEP AS KNOWLEDGE:** alignment principles, hierarchy, magenta brand cue, 16:9 geometry, RTL awareness, visual rhythm lessons.
- **REJECT AS RUNTIME AUTHORITY:** Python builders, `reference_build.py`, fixed proposal skeleton, dark-slide defaults, client/content data, generic-builder fallback.

## Final ruling
The current brand is authoritative for identity. The current deck is **not** a mandatory template shell. The safe pipeline is:

`Artifact Intent → Composition → Rubix Artifact Palette → Current Logo → RTL/Geometry → QA`.

The renderer may recreate or adapt a composition, but it may not weaken the artifact merely to fit a deck layout.
