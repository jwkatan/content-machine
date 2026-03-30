# PDF Builder — Process & Reference

This directory contains the WeasyPrint-based branded PDF pipeline. WeasyPrint replaced
the previous Puppeteer/HTML renderer after persistent layout reliability issues.

---

## How to render a PDF

```bash
.venv/bin/python3 pdf-builder/render.py input.html output.pdf
```

WeasyPrint must be installed in the project venv. The renderer sets `base_url` to the
HTML file's own directory, so all relative paths in the HTML are resolved from there.

---

## Key file locations

| What | Path |
|------|------|
| Renderer script | `pdf-builder/render.py` |
| Brand SVG/PNG assets | `pdf-builder/assets/` |
| Figma design spec (BRIEF.md) | `pdf-builder/templates/whitepaper/BRIEF.md` |
| Figma file | `[YOUR_FIGMA_FILE_KEY]` (Guides) — access via Figma MCP |
| Local font files | `[YOUR_FONT_PATH]/Mulish-*.ttf` |
| Working test HTML | `pdf-builder/weasyprint-test/[test-file].html` |

### Brand assets (pdf-builder/assets/)

| File | Use |
|------|-----|
| `Logo.svg` | Cover + back cover [COMPANY] logo |
| `asterisk.svg` | Cover page decorative asterisk mark |
| `wave.png` | Cover page wave illustration (bottom band) |

These are permanent local files. Do not replace with Figma CDN URLs — they expire in ~7 days.

---

## Figma design nodes (file [YOUR_FIGMA_FILE_KEY])

| Page element | Figma node |
|---|---|
| Cover page | `3614:4` |
| Body page (text layout) | `3614:140` |
| Body page (with diagram + table) | `3614:157` |
| Back cover | `3614:255` |
| Top accent bar | `3614:157` — `inset-[0_0_98.93%_0]`, 3mm height |

To get exact measurements for any element, use:
```
mcp__figma__get_design_context  fileKey: [YOUR_FIGMA_FILE_KEY]  nodeId: <node>
```

---

## Fonts

All fonts are loaded from local `.ttf` files via `@font-face`. Do NOT use Google Fonts
or Adobe TypeKit URLs — WeasyPrint requires local files or a network connection to a
CORS-permissive host, and CDN fonts are unreliable.

Mulish weights available:
```css
@font-face {
  font-family: 'Mulish';
  src: url('[YOUR_FONT_PATH]/Mulish-Regular.ttf') format('truetype');
  font-weight: 400;
}
/* Repeat for Medium (500), SemiBold (600), Bold (700), ExtraBold (800) */
```

Roc Grotesk (brand heading font) is not available locally. All headings currently use
Mulish ExtraBold (800) as a substitute. Acceptable for PDF output.

---

## Page structure — named pages

Use CSS named pages to isolate the header/footer bar to body pages only:

```css
@page            { size: A4; margin: 0; }   /* default — cover + back cover */
@page cover      { size: A4; margin: 0; }
@page backcover  { size: A4; margin: 0; }
@page body       { ... }                     /* accent bar + footer live here */
```

Assign a page to an element with: `.cover-page { page: cover; }`

---

## Solved difficulties

### 1. Edge-to-edge blue accent bar at page top (y=0)

**Problem:** `border-top: 3mm solid #5E6EFF` on `@page body` with `margin-top: 21mm`
rendered the bar at y=21mm (inside the margin), not at the physical page top. It was
also clipped by left/right margins — not edge-to-edge.

**Root cause:** In CSS Paged Media, `border-top` on `@page` sits between the margin area
and the content area — it can never reach y=0 when a top margin exists.

**Solution:** Zero out all top/left/right margins and use `padding` for content insets:

```css
@page body {
  size: A4;
  margin: 0 0 18mm 0;          /* only bottom margin, for the footer */
  border-top: 3mm solid #5E6EFF;   /* now truly at y=0, full page width */
  padding: 18mm 24mm 0 21mm;   /* pushes content down 18mm + left 21mm + right 24mm */
}
```

With `margin-left: 0` and `margin-right: 0`, the border spans the full physical page
width. The `padding` provides the content insets that would otherwise come from margins.

Footer boxes (`@bottom-left`, `@bottom-right`) with zero left/right margins span the
full page — add `padding-left`/`padding-right` inside them to align with content:

```css
@bottom-left  { padding-left:  21mm; }
@bottom-right { padding-right: 24mm; }
```

---

### 2. Cover page wave image — use top in mm, not bottom: 0

**Problem:** `bottom: 0` on an absolutely-positioned element inside a fixed-height
container did not work reliably in WeasyPrint.

**Solution:** Calculate `top` explicitly: `top: 210.2mm` (= 297mm page height − 86.8mm
wave height). Use absolute mm values throughout cover page positioning.

---

### 3. Cover page grid fades — two separate divs

The Figma cover uses two gradient overlays (top fade, bottom fade), not one. Reproducing
both as separate `position: absolute` divs gives the correct grid fade effect.
A single combined fade looks wrong.

```css
.cover-fade--top    { top: -1.5%; height: 59.3%; background: linear-gradient(to bottom, ...) }
.cover-fade--bottom { top: 43.1%; height: 59.3%; background: linear-gradient(to top,   ...) }
```

---

### 4. Table caption orphan prevention

A table caption at the bottom of a page with the table on the next page looks broken.
Fix with:

```css
.table-caption { break-after: avoid; }
```

---

### 5. Margin boxes rendered as separate segments

An earlier attempt used `@top-left`, `@top-center`, `@top-right` margin boxes colored
blue to create the accent bar. The three boxes rendered as visually separate segments
with gaps. The `margin: 0; border-top` approach (solution #1 above) is simpler and more
reliable.

---

## How to create a new branded PDF

1. Start from `pdf-builder/weasyprint-test/[test-file].html` as the template.
2. Replace the content sections between the `<!-- BODY PAGES -->` comments.
3. Update the cover title (`.cover-title-bold`, `.cover-title-regular`).
4. Save the HTML to the asset folder: `content/assets/[slug]/[slug].html`
5. Update asset paths from `../assets/` to `../../../pdf-builder/assets/`
   (or use absolute paths if the asset is in a different location).
6. Render:
   ```bash
   .venv/bin/python3 pdf-builder/render.py \
     content/assets/[slug]/[slug].html \
     content/assets/[slug]/[slug].pdf
   ```
7. Review with ImageMagick:
   ```bash
   magick -density 150 content/assets/[slug]/[slug].pdf page-%d.png
   ```

---

## Reference — completed PDFs

| Asset | HTML | PDF |
|-------|------|-----|
| [COMPANY] vs. Devin DeepWiki | `content/assets/26Q1-competitive-comparison-deepwiki/[company]-vs-[competitor].html` | same folder, `.pdf` |
