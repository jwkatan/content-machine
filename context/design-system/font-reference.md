# Font Reference

Quick-lookup for every text style in the Swimm design system. CSS variable names reference `context/design-system/tokens.css`.

---

## Heading Font: Regesto Grotesk

- **CSS font-family:** `'Regesto Grotesk', sans-serif`
- **CSS variable:** `var(--title-font)`
- **Source:** Installed locally; for web delivery, load via TypeKit or self-host from repo
- **Also known as:** "Roc Grotesk" in some Figma comments and older templates (same typeface family, different display name)

| Style | Size | CSS Size Var | Weight | CSS Weight Var | Line Height | CSS LH Var | Usage |
|-------|------|-------------|--------|---------------|-------------|-----------|-------|
| Special | 60px | `var(--special-size)` | Light (300) | `var(--special-weight)` | 85% | `var(--special-lh)` | Hero large text, typographic statements |
| H1 | 60px | `var(--h1-size)` | Regular (400) | `var(--h1-weight)` | 110% | `var(--h1-lh)` | Page titles, hero headings |
| H2 | 42px | `var(--h2-size)` | Regular (400) | `var(--h2-weight)` | 110% | `var(--h2-lh)` | Section headings |
| H3 | 26px | `var(--h3-size)` | Regular (400) | `var(--h3-weight)` | 110% | `var(--h3-lh)` | Subsection headings, card titles |
| H4 | 20px | `var(--h4-size)` | Regular (400) | `var(--h4-weight)` | 110% | `var(--h4-lh)` | Small headings, icon card titles |
| H5 | 16px | `var(--h5-size)` | Regular (400) | `var(--h5-weight)` | 110% | `var(--h5-lh)` | Smallest heading level |

**Mobile headings:** H1 40px, H2 30px, H3 24px, H4 18px, H5 16px (all Regular, 110% line height).

---

## Body Font: Manrope

- **CSS font-family:** `'Manrope', sans-serif`
- **CSS variable:** `var(--text-font)`
- **Source:** Google Fonts
- **Import URL:** `https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;700&display=swap`

| Style | Size | CSS Size Var | Weight | CSS Weight Var | Line Height | CSS LH Var | Usage |
|-------|------|-------------|--------|---------------|-------------|-----------|-------|
| P1 | 18px | `var(--p1-size)` | Regular (400) | `var(--p1-weight)` | 140% | `var(--p1-lh)` | Standard body text |
| P2 | 24px | `var(--p2-size)` | Light (300) | `var(--p2-weight)` | 140% | `var(--p2-lh)` | Large body, intro paragraphs |
| P3 | 20px | `var(--p3-size)` | Light (300) | `var(--p3-weight)` | 140% | `var(--p3-lh)` | Section intro body, subtitle |
| P4 | 16px | `var(--p4-size)` | Regular (400) | `var(--p4-weight)` | 140% | `var(--p4-lh)` | Small body, card descriptions, footer |

**Mobile paragraphs:** P1 24px Regular, P2 20px Light, P3 18px Light, P4 14px Regular.

---

## Labels (Manrope)

All labels use Manrope (`var(--text-font)`).

| Style | Size | CSS Size Var | Weight | CSS Weight Var | Line Height | CSS LH Var | Letter Spacing | Usage |
|-------|------|-------------|--------|---------------|-------------|-----------|----------------|-------|
| S | 12px | `var(--label-s-size)` | Regular (400) | `var(--label-s-weight)` | 140% | `var(--label-s-lh)` | -- | Small labels |
| M | 14px | `var(--label-m-size)` | Regular (400) | `var(--label-m-weight)` | 100% | `var(--label-m-lh)` | -- | Medium labels |
| L | 16px | `var(--label-l-size)` | Regular (400) | `var(--label-l-weight)` | 85% | `var(--label-l-lh)` | -- | Large labels, buttons |
| XL | 20px | `var(--label-xl-size)` | Light (300) | `var(--label-xl-weight)` | 120% | `var(--label-xl-lh)` | -- | Extra large labels |
| Eyebrow | 14px | -- | Regular (400) | -- | 100% | -- | 6% (uppercase) | Section eyebrows |
| Footnotes | 12px | -- | Regular (400) | -- | 140% | -- | 1% | Footer credits, fine print |

---

## Color Pairings by Surface

Use these pairings to ensure correct contrast on light and dark backgrounds. CSS semantic aliases from `tokens.css` are listed for each role.

| Surface | Background | Heading Color | CSS Heading Var | Body Color | CSS Body Var | Accent Color | CSS Accent Var |
|---------|-----------|--------------|-----------------|-----------|-------------|-------------|---------------|
| Light (Gray 100) | `var(--bg-light)` #F3F3FB | Blue 900 (#1A2761) | `var(--text-heading-light)` | Gray 500 (#415992) | `var(--text-body-light)` | Blue 700 (#325BFF) | `var(--accent-primary)` |
| Dark (Blue 900) | `var(--bg-dark)` #1A2761 | Gray 50 (#FDFCFE) or Gray 150 (#EAECF9) | `var(--text-heading-dark)` | Blue 300 (#AFC8FB) | `var(--text-body-dark)` | Blue 700 (#325BFF) | `var(--accent-primary)` |

---

## Figma Font Override

> **WARNING:** The Figma brand file currently has some headings set to **Manrope** because Regesto Grotesk was not available in the Figma environment. When pulling element HTML from Figma, **ALL heading text** (H1-H5, Special) must be converted to `font-family: var(--title-font)` regardless of what the Figma export shows. The source of truth for font assignment is this reference, not the Figma output.

**Checklist when importing from Figma:**
1. Search for any `font-family: 'Manrope'` on heading elements (h1-h5, .special)
2. Replace with `font-family: var(--title-font)`
3. Verify weight matches the table above (headings are Regular 400 except Special which is Light 300)
4. Body text and labels should remain Manrope -- only headings need the override
