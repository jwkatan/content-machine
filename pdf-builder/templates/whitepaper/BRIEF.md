# Swimm Whitepaper — Design Specification

This is the source of truth for every visual decision. All measurements were extracted
from the Figma file `UYfMt04X79c7y7YXAhy3DI` (Guides). Figma canvas is 595 × 842px at 72 dpi.

---

## §1 Canvas & print setup

| Property | Value |
|---|---|
| Page size | A4 — `210mm × 297mm` |
| Margins | Zero (full bleed) |
| CSS page rule | `@page { size: A4; margin: 0; }` |
| Puppeteer options | `format: 'A4'`, `printBackground: true`, `preferCSSPageSize: true`, `margin: {top:0, right:0, bottom:0, left:0}` |
| Background printing | `print-color-adjust: exact` + `-webkit-print-color-adjust: exact` on all elements |
| Unit conversion | 1 Figma px = 1 CSS pt (both at 72 dpi) |
| Position system | Absolute %, derived as `(Figma px / canvas dimension) × 100` |

Each page is a `div.page` with `width: 210mm; height: 297mm; position: relative; overflow: hidden; break-after: page`.

---

## §2 Color tokens

These are the only hex values permitted anywhere in the output.

```
--blue-deep-dive:   #1F35FF   (primary brand blue, darkest)
--blue-swimm:       #4154FF   (Swimm Blue — primary CTA, signature color)
--blue-coastal:     #5E6EFF   (body bar, callout border, back cover CTA button)
--blue-shallow:     #8D98FF   (page numbers, muted text)
--blue-feet:        #E4E7FF   (callout bg, graphic placeholder, table header bg)
--yellow-duck:      #FDF150   (energetic accent — use sparingly)
--yellow-shine:     #FFF78E   (secondary yellow — rarely used)
--neutral-charcoal: #1D1E2B   (back cover bg, primary text)
--neutral-gravel:   #2F3142   (secondary dark)
--neutral-tide:     #696B80   (muted / secondary text)
--neutral-wash:     #F4F6FA   (stat tile bg, page wash)
--neutral-white:    #FFFFFF   (page background, text on dark)
```

**Off-palette exceptions (documented, never extend this list):**
- `#D7DBFF` — table borders and body divider line (between --blue-feet and --blue-shallow)
- `#E8EAFF` — cover page grid lines (Figma "Feet in Water 100" variant)

---

## §3 Typography

**Heading font:** `roc-grotesk, sans-serif`
Load via Adobe Fonts TypeKit: `https://use.typekit.net/ghp6lrn.css`
Weights used: 400 (Regular), 700 (Bold)

**Body font:** `'Mulish', sans-serif`
Load via Google Fonts: `https://fonts.googleapis.com/css2?family=Mulish:wght@400;500;600;700;800&display=swap`
Weights used: 400, 500, 600, 700, 800

Both fonts require an internet connection. For offline/CI use, embed as base64 `@font-face` declarations.

**Scale (all sizes in pt):**

| Role | Font | Weight | Size | Line height |
|---|---|---|---|---|
| Cover label ("Whitepaper") | Mulish | 400 | 18pt | 28pt |
| Cover title bold | Roc Grotesk | 700 | 31pt | 35pt |
| Cover title regular | Roc Grotesk | 400 | 31pt | 35pt |
| Body chapter heading | Roc Grotesk | 700 | 24pt | 30pt |
| Body copy | Mulish | 400 | 12pt | 18pt |
| Callout text | Roc Grotesk | 700 | 13pt | 19pt |
| Stat value | Roc Grotesk | 700 | 36pt | 1 (unitless) |
| Stat label | Mulish | 400 | 10pt | 15pt |
| Table header | Mulish | 800 | 12pt | 16pt |
| Table cell | Mulish | 400 | 10pt | 14pt |
| Page number | Roc Grotesk | 700 | 13pt | 16pt |
| Footer logo | — | — | height 5.4mm | — |

---

## §4 Page specifications

### Page 1 — Cover

**Figma node:** `3614:4` in file `UYfMt04X79c7y7YXAhy3DI`

Background: `#FFFFFF` with a `#E8EAFF` square grid at `7.1mm × 7.1mm` cell size, 1px lines.
```css
background-image:
  linear-gradient(to right, #E8EAFF 1px, transparent 1px),
  linear-gradient(to bottom, #E8EAFF 1px, transparent 1px);
background-size: 7.1mm 7.1mm;
```

Two white gradient fades soften the grid:
- **Top fade**: top 0, height 17%, `linear-gradient(to bottom, #FFFFFF 35%, transparent 100%)`
- **Bottom fade**: bottom 0, height 25%, `linear-gradient(to top, #FFFFFF 35%, transparent 100%)`

**Logo** (`.cover-logo`):
- Position: `top: 6.41%; left: 6.05%`
- `img`: `height: 11mm; width: auto`
- Asset: `Logo.svg` (local)

**Title block** (`.cover-content`):
- Position: `top: 23.04%; left: 11.6%; width: 68.07%`
- Flex column, `gap: 10pt`
- Children:
  - `.cover-label` — "Whitepaper" text — Mulish 400, 18pt/28pt, `#1D1E2B`
  - `.cover-title-block` — contains two `<p>` lines:
    - `.cover-title-bold` — Roc Grotesk 700, 31pt/35pt, `#1D1E2B`
    - `.cover-title-regular` — Roc Grotesk 400, 31pt/35pt, `#1D1E2B`
  - `.cover-asterisk` — `16.5pt × 16.5pt` — Swimm ✳ brand mark (Figma asset URL, expires)

**Wave illustration** (`.cover-wave`):
- Position: `top: 52.14%; left: 0; width: 100%; height: 29.21%`
- Inner `img`: `left: -8.24%; width: 162.69%; object-fit: fill`
- Asset: Figma MCP URL (expires ~7 days). Re-fetch from node `3614:139` in file `UYfMt04X79c7y7YXAhy3DI`.

**How to refresh expiring assets:**
Call `mcp__figma__get_design_context` with `fileKey: UYfMt04X79c7y7YXAhy3DI` and `nodeId: 3614:4`.
The response includes fresh asset URLs for the asterisk and wave.

---

### Page N — Body Content (repeatable)

**Figma nodes:** `3614:140` (text layout), `3614:157` (with diagram + table)
17 body layout variants available — all use the same CSS.

**Structure:**
```
div.page.body-page
├── div.body-bar          (top accent stripe)
├── div.body-content      (main content column)
│   ├── h2.body-heading
│   ├── div.body-text     (one or more)
│   └── [optional blocks — mix as needed per page]
├── div.body-divider
├── div.body-footer-logo
└── span.body-page-num
```

**Layout measurements:**

| Element | CSS |
|---|---|
| `.body-bar` | `top:0; left:0; right:0; height:1.07%` (9px/842), `background: #5E6EFF` |
| `.body-content` | `top:7.01%; left:10.08%; right:11.43%; bottom:13%; flex column; gap:21pt; overflow:hidden` |
| `.body-divider` | `left:10.08%; right:11.43%; bottom:6.89%; height:0; border-top:1px solid #D7DBFF` |
| `.body-footer-logo` | `left:10.08%; bottom:2.02%; img height:5.4mm; width:auto` |
| `.body-page-num` | `right:11.43%; bottom:2.02%; Roc Grotesk 700, 13pt, #8D98FF` |

---

### Body content components (mix on any body page)

**① Chapter heading** — `h2.body-heading`
- Roc Grotesk Bold, 24pt / 30pt, `#1D1E2B`

**② Body text** — `div.body-text`
- Mulish 400, 12pt / 18pt, `#1D1E2B`
- Wraps `<p>` and `<ul>` / `<ol>` elements
- Lists: `padding-left: 18pt`

**③ Graphic / image** — `div.body-graphic`
- Background: `#E4E7FF` (--blue-feet)
- `min-height: 40mm; display:flex; align-items:center; justify-content:center`
- Inner label: `.body-graphic__label` — Mulish 600, 9pt, uppercase, letter-spacing 0.08em, `#8D98FF`
- To show an actual image: add `<img src="path/to/image.png" style="width:100%;height:auto">` inside

**④ Callout box** — `div.body-callout`
- Background: `#E4E7FF`; `border-left: 3pt solid #5E6EFF`; `padding: 13pt 16pt`
- Text: Roc Grotesk Bold, 13pt / 19pt, `#1D1E2B`

**⑤ Stats row** — `div.body-stats` containing `div.body-stat` tiles
- Row: `display:flex; gap:24pt`
- Each tile: `flex:1; padding:13pt 16pt; background:#F4F6FA; flex-column; gap:4pt`
- `.body-stat__value` — Roc Grotesk 700, 36pt, `#5E6EFF`
- `.body-stat__label` — Mulish 400, 10pt / 15pt, `#1D1E2B`
- Max 3 tiles per row before layout breaks

**⑥ Data table** — `table.body-table`
- `width:100%; border-collapse:collapse`
- `<th>`: background `#E4E7FF`, border `1px solid #D7DBFF`, Mulish 800, 12pt/16pt, `padding:8pt 10pt`
- `<td>`: border `1px solid #D7DBFF`, Mulish 400, 10pt/14pt, `vertical-align:top`, `padding:8pt 10pt`

---

### Page Last — Back Cover

**Figma node:** `3614:255` in file `UYfMt04X79c7y7YXAhy3DI`

Background: `#1D1E2B` (--neutral-charcoal), full bleed.

**Content block** (`.back-cover-content`):
- Position: `left:17.48%; top:27.55%; width:65.04%` (from Figma: left=104px, top=232px, width=387px)
- Flex column, `align-items:center`

**Logo** (`.back-cover-logo`):
- `img: height:38pt; width:auto; filter:brightness(0) invert(1)` (makes dark SVG white)
- Asset: `Logo.svg` (local)
- `margin-bottom: 33pt` below logo to tagline

**Tagline** (`.back-cover-tagline`):
- Mulish 400, 12pt / 18pt, `#FFFFFF`, `text-align:center`
- `margin-bottom: 37pt` below tagline to CTA button

**CTA button** (`.back-cover-cta`):
- `display:flex; align-items:center; justify-content:center`
- `width:268pt; height:44pt`
- Background: `#5E6EFF` (--blue-coastal)
- `border-radius: 10.304pt`
- `box-shadow: 0 0 10.304pt rgba(0,0,0,0.16)`
- Text: Roc Grotesk 700, 16pt, `#FFFFFF`
- Render as `<a href="...">` — non-interactive in PDF but semantically correct

**Decorative hand/cursor icon** (`.back-cover-hand`):
- Position: `left:47.39%; top:47.39%` (overlays the CTA button)
- `width:5.21%` (31px / 595px)
- Asset: `Hand icon.svg` (local, permanent)

---

## §5 Spacing grid

All spacing follows an 8pt grid:

```
--sp-1:  8px    --sp-5: 40px
--sp-2: 16px    --sp-6: 48px
--sp-3: 24px    --sp-7: 56px
--sp-4: 32px    --sp-8: 64px
```

---

## §6 What "pixel perfect" means

An output passes brand review when:

1. All hex values are exact matches from §2 — no approximations
2. Typography sizes and weights match §3 exactly — measure in pt
3. Layout percentages match §4 within 0.5% tolerance
4. Fonts render as Roc Grotesk (headings) and Mulish (body) — not fallbacks
5. Page dimensions are exactly A4 (210mm × 297mm) with zero margins
6. Backgrounds, gradients, and colors all appear in the PDF (not stripped by print settings)
