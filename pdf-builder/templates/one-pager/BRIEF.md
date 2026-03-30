# Swimm One-Pager — Design Specification

This is the source of truth for every visual decision. The one-pager is a fixed
2-page (front/back) sales enablement document with positioned zones instead of
flowing chapters. Layout derived from the Figma one-pager design.
Figma canvas is 595 x 842px at 72 dpi (A4).

---

## S1 Canvas & print setup

| Property | Value |
|---|---|
| Page size | A4 — `210mm x 297mm` |
| Margins | Zero (full bleed) |
| CSS page rule | `@page { size: A4; margin: 0; }` |
| Puppeteer options | `format: 'A4'`, `printBackground: true`, `preferCSSPageSize: true`, `margin: {top:0, right:0, bottom:0, left:0}` |
| Background printing | `print-color-adjust: exact` + `-webkit-print-color-adjust: exact` on all elements |
| Unit conversion | 1 Figma px = 1 CSS pt (both at 72 dpi) |
| Position system | Absolute %, derived as `(Figma px / canvas dimension) x 100` |
| Page count | Exactly 2 pages (front + back). No repeatable body pages. |

Each page is a `div.page` with `width: 210mm; height: 297mm; position: relative; overflow: hidden; break-after: page`.

---

## S2 Color tokens

These are the only hex values permitted anywhere in the output.
Identical to the whitepaper palette — no additions, no changes.

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
- `#D7DBFF` — divider lines and borders (between --blue-feet and --blue-shallow)
- `#E8EAFF` — light accent background areas

---

## S3 Typography

**Heading font:** `roc-grotesk, sans-serif`
Load via Adobe Fonts TypeKit: `https://use.typekit.net/ghp6lrn.css`
Weights used: 400 (Regular), 700 (Bold)

**Body font:** `'Mulish', sans-serif`
Load via Google Fonts: `https://fonts.googleapis.com/css2?family=Mulish:wght@400;500;600;700;800&display=swap`
Weights used: 400, 500, 600, 700, 800

Both fonts require an internet connection. For offline/CI use, embed as base64 `@font-face` declarations.

**Scale (all sizes in pt) — optimized for high-density 2-page layout:**

| Role | Font | Weight | Size | Line height |
|---|---|---|---|---|
| Product title | Roc Grotesk | 700 | 28pt | 34pt |
| Subtitle | Roc Grotesk | 400 | 14pt | 20pt |
| Section heading | Roc Grotesk | 700 | 16pt | 22pt |
| Column header | Mulish | 700 | 11pt | 16pt |
| Body / bullet text | Mulish | 400 | 9pt | 14pt |
| Stat value | Roc Grotesk | 700 | 24pt | 1 (unitless) |
| Stat label | Mulish | 400 | 8pt | 12pt |
| Logo bar text | Mulish | 600 | 7pt | 10pt |
| CTA button text | Roc Grotesk | 700 | 14pt | 18pt |
| Intro text | Mulish | 400 | 10pt | 15pt |
| Flow step label | Roc Grotesk | 700 | 9pt | 13pt |
| Flow step caption | Mulish | 400 | 8pt | 11pt |
| Security bullet | Mulish | 400 | 9pt | 13pt |
| Back section heading | Roc Grotesk | 700 | 14pt | 18pt |
| Back body text | Mulish | 400 | 9pt | 14pt |

---

## S4 Page specifications

### Page 1 — Front

Background: `#FFFFFF` (solid white, no grid pattern).

The front page is divided into positioned zones. All positions expressed as %
of the 595 x 842 canvas.

**Header zone** (`.onepager-header`):
- Position: `top: 4%; left: 6%; right: 6%`
- Flex row, `justify-content: space-between; align-items: flex-start`
- Left: product title + subtitle stack
- Right: Swimm logo (`height: 9mm; width: auto`)

**Product title** (`.onepager-title`):
- Font: Roc Grotesk 700, 28pt / 34pt, `#1D1E2B`
- Max width: 60% of page width (to leave room for illustration)

**Subtitle** (`.onepager-subtitle`):
- Font: Roc Grotesk 400, 14pt / 20pt, `#696B80`
- Directly below title, `margin-top: 4pt`

**Logo** (`.onepager-logo`):
- Position: within header, right-aligned
- `img: height: 9mm; width: auto`

**Intro paragraph** (`.onepager-intro`):
- Position: `top: 15%; left: 6%; width: 52%`
- Font: Mulish 400, 10pt / 15pt, `#1D1E2B`
- 2-3 sentences describing the value proposition

**Illustration placeholder** (`.onepager-illustration`):
- Position: `top: 5%; right: 6%; width: 30%; height: 22%`
- Circular clip: `border-radius: 50%`
- Background: `#E4E7FF`
- `display: flex; align-items: center; justify-content: center`
- Overlaps header zone on the right side

**Section heading** (`.onepager-section-heading`):
- Position: `top: 29%; left: 6%; right: 6%`
- Font: Roc Grotesk 700, 16pt / 22pt, `#1D1E2B`
- Optional bottom border: `2pt solid #4154FF`, `padding-bottom: 6pt`

**Capability grid** (`.onepager-capabilities`):
- Position: `top: 35%; left: 6%; right: 6%`
- CSS Grid: `grid-template-columns: 1fr 1fr 1fr; gap: 16pt`
- Each column (`.capability-column`):
  - Header (`.capability-header`): Mulish 700, 11pt / 16pt, `#1D1E2B`
  - Background highlight on header: `#E4E7FF`, `padding: 6pt 8pt`
  - Bullets (`.capability-list`): Mulish 400, 9pt / 14pt, `#1D1E2B`
  - List style: `padding-left: 12pt`

**Flow diagram** (`.onepager-flow`):
- Position: `top: 62%; left: 6%; right: 6%`
- Flex row: `display: flex; align-items: flex-start; justify-content: space-between`
- Each step (`.flow-step`):
  - `flex: 1; text-align: center`
  - Icon/number circle: `width: 32pt; height: 32pt; border-radius: 50%`
  - Background: `#4154FF`; color: `#FFFFFF`
  - Label: Roc Grotesk 700, 9pt / 13pt, `#1D1E2B`, `margin-top: 6pt`
  - Caption: Mulish 400, 8pt / 11pt, `#696B80`
- Arrow connectors between steps:
  - `.flow-arrow`: `width: 24pt; color: #8D98FF; font-size: 14pt`
  - Vertically centered with step circles

**Logo bar** (`.onepager-logobar`):
- Position: `bottom: 0; left: 0; right: 0; height: 7%`
- Background: `#1D1E2B`
- Flex row, centered: `display: flex; align-items: center; justify-content: center; gap: 32pt`
- Each logo item: Mulish 600, 7pt / 10pt, `#FFFFFF`, uppercase, `letter-spacing: 0.1em`
- Alternatively, logo images: `height: 14pt; filter: brightness(0) invert(1)`

---

### Page 2 — Back

Background: `#FFFFFF` (solid white).

**Top accent bar** (`.onepager-back-bar`):
- `top: 0; left: 0; right: 0; height: 1.07%`
- Background: `#5E6EFF` (--blue-coastal)

**Business value section** (`.onepager-value`):
- Position: `top: 4%; left: 6%; right: 6%`
- Heading: Roc Grotesk 700, 14pt / 18pt, `#1D1E2B`
- Body: Mulish 400, 9pt / 14pt, `#1D1E2B`
- Height: approximately 18% of page

**Deployment section** (`.onepager-deploy`):
- Position: `top: 24%; left: 6%; right: 6%`
- Heading: Roc Grotesk 700, 14pt / 18pt, `#1D1E2B`
- Body: Mulish 400, 9pt / 14pt, `#1D1E2B`
- Height: approximately 12% of page

**Use cases section** (`.onepager-usecases`):
- Position: `top: 40%; left: 6%; right: 48%` (left half)
- Heading: Roc Grotesk 700, 14pt / 18pt, `#1D1E2B`
- Tags: `display: flex; flex-wrap: wrap; gap: 8pt`
- Each tag (`.usecase-tag`):
  - `padding: 5pt 12pt; border-radius: 16pt`
  - Background: `#E4E7FF`; color: `#1D1E2B`
  - Font: Mulish 600, 8pt / 12pt

**Stats section** (`.onepager-stats`):
- Position: `top: 40%; left: 54%; right: 6%` (right half, beside use cases)
- `display: flex; flex-direction: column; gap: 12pt`
- Each stat tile (`.onepager-stat`):
  - `padding: 10pt 12pt; background: #F4F6FA`
  - Value: Roc Grotesk 700, 24pt, `#5E6EFF`
  - Label: Mulish 400, 8pt / 12pt, `#1D1E2B`

**Security section** (`.onepager-security`):
- Position: `top: 68%; left: 6%; right: 6%`
- Heading: Roc Grotesk 700, 14pt / 18pt, `#1D1E2B`
- List: `display: grid; grid-template-columns: 1fr 1fr; gap: 6pt 24pt`
- Each item: Mulish 400, 9pt / 13pt, `#1D1E2B`
- Checkmark decorator: `::before` pseudo-element, color `#5E6EFF`

**CTA section** (`.onepager-cta`):
- Position: `bottom: 0; left: 0; right: 0; height: 12%`
- Background: `#1D1E2B`
- `display: flex; align-items: center; justify-content: center`
- CTA button (`.onepager-cta-button`):
  - `padding: 10pt 32pt; border-radius: 10.304pt`
  - Background: `#5E6EFF`; color: `#FFFFFF`
  - Font: Roc Grotesk 700, 14pt / 18pt
  - `box-shadow: 0 0 10.304pt rgba(0,0,0,0.16)`
  - Render as `<a href="...">` — non-interactive in PDF but semantically correct

---

## S5 Spacing grid

All spacing follows an 8pt grid (identical to whitepaper):

```
--sp-1:  8px    --sp-5: 40px
--sp-2: 16px    --sp-6: 48px
--sp-3: 24px    --sp-7: 56px
--sp-4: 32px    --sp-8: 64px
```

---

## S6 What "pixel perfect" means

An output passes brand review when:

1. All hex values are exact matches from S2 — no approximations
2. Typography sizes and weights match S3 exactly — measure in pt
3. Layout percentages match S4 within 0.5% tolerance
4. Fonts render as Roc Grotesk (headings) and Mulish (body) — not fallbacks
5. Page dimensions are exactly A4 (210mm x 297mm) with zero margins
6. Backgrounds, gradients, and colors all appear in the PDF (not stripped by print settings)
7. Exactly 2 pages — no more, no fewer. Content must fit within fixed zones.
8. No zone overlap — every zone must stay within its allocated region
