# Chromium Fixed-Canvas Renderer Contract

## Purpose
Guarantee that the approved HTML artifact and production PDF share the same layout engine, fonts, dimensions, and component geometry.

## Single rendering authority
Use a pinned Chromium build through Playwright for:
- interactive HTML review;
- HTML golden screenshots;
- production PDF generation.

Do not use WeasyPrint as the production renderer for slide-like proposal artifacts.

## Canonical canvas
Each page is authored at:
- width: `1280px`;
- height: `720px`;
- aspect ratio: `16:9`;
- CSS pixel density: `96 px/in`.

PDF page size:
- width: `13.333333in`;
- height: `7.5in`;
- margin: `0`;
- scale: `1`;
- print background: enabled;
- prefer CSS page size: enabled.

## Mandatory print CSS

```css
@page {
  size: 13.333333in 7.5in;
  margin: 0;
}

html, body {
  margin: 0;
  padding: 0;
  width: 1280px;
  background: #fff;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.slide {
  position: relative;
  width: 1280px;
  height: 720px;
  break-after: page;
  page-break-after: always;
  contain: layout paint;
}
```

## Forbidden layout behavior
- root-level RTL flex/grid geometry;
- `row-reverse` as a substitute for explicit RTL data order;
- CSS `direction` as the only sequence-positioning mechanism;
- sequence numbers or arrows inside generated raster assets;
- `vh`, `vw`, browser-dependent viewport sizing;
- production reliance on `overflow:hidden`;
- text ellipsis for mandatory content;
- print-only font substitution;
- auto-fit title resizing below approved limits;
- CSS counters for Arabic sequence numbers;
- page-wide transform scaling.

## AR-SEQ-001 geometry authority
For Arabic ordered artifacts, preserve semantic data order and assign explicit physical coordinates or grid slots. Do not use `direction: rtl` or `row-reverse` as the ordering algorithm.

Before screenshot or PDF generation, validate:
- horizontal `X(١) > X(٢) > ...`;
- vertical `Y(١) < Y(٢) < ...`;
- diagonal both conditions together;
- every wrapped row starts at its rightmost logical slot.

## Geometry/text separation
Use physical LTR coordinates for reliable PDF geometry. Apply RTL only to Arabic text containers.

```css
.geometry {
  direction: ltr;
  position: relative;
}

.text-ar {
  direction: rtl;
  text-align: right;
  unicode-bidi: plaintext;
  min-width: 0;
}

.numeric-run,
.technical-id {
  direction: ltr;
  unicode-bidi: isolate;
  display: inline-block;
}
```

## Font loading
- load approved fonts from controlled local assets;
- wait for `document.fonts.ready`;
- verify computed font family for representative Arabic and Latin nodes;
- inspect the generated PDF using `pdffonts`;
- reject any unapproved fallback such as Noto or Arimo unless explicitly authorized by the current brand standard.

## PDF generation contract
Use Playwright `page.pdf()` with explicit dimensions. Do not rely on printer defaults.

## Secondary verification
After Chromium generates the PDF:
- rasterize with PDFium at 180–200 DPI;
- rasterize with Poppler at the same DPI;
- compare page dimensions and visual content;
- reject material differences.
