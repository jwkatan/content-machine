# Brand Identity

Shared reference for all mediums (web, Marp, PPTX). CSS variable names reference `tokens.css`.

---

## Typography

### Heading Font: Regesto Grotesk

- **CSS:** `'Regesto Grotesk', sans-serif` / `var(--title-font)`
- **Source:** Installed locally; for web delivery, load via TypeKit or self-host
- **Also known as:** "Roc Grotesk" in some Figma comments (same typeface family)

| Style | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| Special | 60px | Light (300) | 85% | Hero large text, typographic statements |
| H1 | 60px | Regular (400) | 110% | Page titles, hero headings |
| H2 | 42px | Regular (400) | 110% | Section headings |
| H3 | 26px | Regular (400) | 110% | Subsection headings, card titles |
| H4 | 20px | Regular (400) | 110% | Small headings, icon card titles |
| H5 | 16px | Regular (400) | 110% | Smallest heading level |

Mobile headings: H1 40px, H2 30px, H3 24px, H4 18px, H5 16px.

### Body Font: Manrope

- **CSS:** `'Manrope', sans-serif` / `var(--text-font)`
- **Source:** Google Fonts
- **Import:** `https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;700&display=swap`

| Style | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| P1 | 18px | Regular (400) | 140% | Standard body text |
| P2 | 24px | Light (300) | 140% | Large body, intro paragraphs |
| P3 | 20px | Light (300) | 140% | Section intro body, subtitle |
| P4 | 16px | Regular (400) | 140% | Small body, card descriptions, footer |

Mobile paragraphs: P1 24px, P2 20px, P3 18px, P4 14px.

**Marp note:** The theme defaults to 20px base body text (P3) for projection readability. P4 (16px) is the minimum for supplementary text on slides.

### Labels (Manrope)

| Style | Size | Weight | Line Height | Letter Spacing | Usage |
|-------|------|--------|-------------|----------------|-------|
| S | 12px | Regular (400) | 140% | -- | Small labels |
| M | 14px | Regular (400) | 100% | -- | Medium labels |
| L | 16px | Regular (400) | 85% | -- | Large labels, buttons |
| XL | 20px | Light (300) | 120% | -- | Extra large labels |
| Eyebrow | 14px | Regular (400) | 100% | 6% (uppercase) | Section eyebrows |
| Footnotes | 12px | Regular (400) | 140% | 1% | Footer credits, fine print |

### Stat Numbers

Stat block numerals use **Manrope Light 300** at 60px — the body font, NOT Regesto Grotesk. The Special style (also 60px/300) is for typographic statements in Regesto Grotesk. These are different elements despite sharing size and weight.


---

## Color Pairings by Surface

| Surface | Background | Heading Color | Body Color | Accent Color |
|---------|-----------|--------------|-----------|-------------|
| Light (Gray 100 `#F3F3FB`) | `var(--bg-light)` | Blue 900 `#1A2761` | Gray 500 `#415992` | Blue 700 `#325BFF` |
| Dark (Blue 900 `#1A2761`) | `var(--bg-dark)` | Gray 50 `#FDFCFE` | Blue 300 `#AFC8FB` | Blue 700 `#325BFF` |

### Warm Color Rule

Pink 400 (`#E99DB1`) and Yellow 200 (`#FFDFBB`) exist **only as gradient transition bands** — the boundary where blue meets white. They appear inside `linear-gradient` and `radial-gradient` stop lists. They are **never** used as:
- `color` (text color)
- `background-color` (flat fill)
- `border-color` (standalone border)

For inline text emphasis, use Blue 700 on light surfaces and Blue 400 on dark surfaces.

### Gray Rule

All neutrals are blue-tinted (Gray palette: `#415992` to `#FDFCFE`). Never use pure grays (`#808080`, `#CCCCCC`, `#333333`).

---

## Anti-Patterns

### CSS-Detectable Patterns (check during review)

**1. Centered-Everything Default**
Centering is reserved for: `title-gradient`, `closing-gradient`, and `dark-statement` slides / CTA bridge sections. All other contexts use left-aligned text. Detection: if >30% of text elements are centered, flag.

**2. Symmetric Card Grid Overuse**
Card grids are correct only when content is genuinely 2-4 parallel items of equal weight. A bold claim uses a statement layout. A single metric uses a stat block. A comparison uses two-column. Detection: if >40% of slides/sections use card grids, flag.

**3. Uniform Visual Rhythm**
No two consecutive slides/sections use the same layout type. Vary: statement, data, screenshot, cards, split, divider. Detection: flag consecutive identical layout types, or fewer than 3 distinct types in 6+ sections.

**4. Decorative-Only Gradients**
One hero gradient section per composition. Gradients appear only via defined element library patterns (grad-section, cta-section, screenshot frames, card radials). Do not invent new gradient applications. Detection: any gradient not traceable to the element library is improvised.

**5. Flat Dark Surfaces**
Every dark surface must have depth. In Marp, the theme handles this automatically — every `dark-*` class has SVG radial pseudo-elements. In HTML, apply SVG radials from the element library. Detection: bare `background-color` with no depth layer is a failure.

**6. Cookie-Cutter Spacing**
Use element-specific spacing from tokens.css. Cards: 32px padding, 24px icon gap, 12px text gap. CTA nesting: 36px per level. Detection: if fewer than 3 distinct spacing values, flag.

**7. Predictable Accent Placement**
Blue 700 is for buttons and selective emphasis, not every heading. Pink 400 and Yellow 200 only inside gradient stops (see Warm Color Rule above). Detection: Pink 400/Yellow 200 outside gradient stop lists is a failure.

**8. Rounded Corners**
Zero `border-radius` on all cards, frames, containers, and buttons. Sharp corners are the brand signature. Detection: any `border-radius` occurrence is a failure. Zero tolerance.

**9. Box-Shadow Depth**
Depth comes from SVG radial gradients, blend modes (`lighten`, `multiply`, `screen`), and opacity layering. Detection: any `box-shadow` occurrence is a failure. Zero tolerance.

**10. Heading-Paragraph Monotony**
Vary structures: split intros, stat blocks, icon grids, quote treatments, two-column comparisons, flow diagrams. Detection: if fewer than 3 structural patterns in 6+ sections, flag.

**11. Empty White Space**
Fill the canvas. Card rows and stat rows should use full available width. Backgrounds include depth treatments. Detection: content occupying <40% of canvas area.

**12. Identical Typography**
Use the full type scale. At least 3 distinct heading sizes in any multi-section composition. H1 appears only on title/closing slides. Detection: fewer than 3 heading sizes in 6+ sections.

**13. Monochromatic Blue Wash**
Apply the 60-30-10 rule. Dark surfaces (60%): Gray 50 headings + Blue 300 body. Light surfaces (30%): Blue 900 headings + Gray 500 body. Gradient accent (10%). Detection: same blue shade used for background, headings, and body text simultaneously.

**14. Improvised CSS**
Copy exact values from element library and tokens.css. CTA gradient stops: 34.286%, 56.023%, 70.306%, 83.838%, 91.355%. Screenshot frame gradient: 239.66deg. Detection: any value not traceable to a canonical source.

**15. Flat Light Card Backgrounds**
Every card on a light surface gets the Light-100 radial gradient (`--gradient-light-100`), not flat Gray-100. Radial origin must be asymmetric (~33% from left, 0% from top). Detection: solid background on light cards, or centered gradient origin (50% 50%).

### Content-Type Guardrails (not CSS-detectable)

- **Stock-feeling layouts** — No handshake imagery, sticky-note boards, or people-pointing-at-screens. If it could be a Shutterstock result, reject it.
- **Photorealistic imagery or human figures** — The brand is abstract and geometric. No photos, no faces, no silhouettes.
- **Gaussian blur or bokeh effects** — Depth comes from layering and opacity, not soft focus.
- **Cartoonish or playful illustration** — Maintain enterprise tone. No mascots, no rounded-corner pastel friendliness.
- **Skeuomorphic elements** — No faux-3D buttons, drop shadows mimicking physical objects, or textured surfaces.
- **Repeating wallpaper patterns** — Dot-matrix patterns are organic and vary in density. Tiled or repeating textures look mechanical and cheap.
- **Heavy gradients that dominate** — Gradients support the composition, they do not become it.
