# Swimm Visual Guidelines

This document defines the visual style, brand colors, and design principles for Swimm content. Reference this when generating images for blog posts, social media, and other visual content.

## Figma Sources

Brand system: https://www.figma.com/design/epnCa2oEzyBli5hF8YI8Ed/Swimm-brand?node-id=3911-9336

---

## Brand Colors

### Blues (Primary Palette)
- **Blue 900**: #1A2761 - Deepest navy, dark backgrounds, text
- **Blue 800**: #2635A7 - Secondary dark blue
- **Blue 700**: #325BFF - Main brand blue (primary action, emphasis)
- **Blue 600**: #527DFF - Secondary blue
- **Blue 400**: #6891F9 - Medium blue accent
- **Blue 300**: #AFC8FB - Light blue
- **Blue 200**: #D5E3FF - Very light blue
- **Blue 100**: #E2EBFF - Lightest blue, backgrounds

### Grays (Blue-tinted Neutrals)
- **Gray 500**: #415992 - Dark gray (headings, strong text)
- **Gray 300**: #8594BE - Medium gray (secondary text)
- **Gray 250**: #C6D1F3 - Light-medium gray (borders, dividers)
- **Gray 200**: #DEE3F6 - Light gray
- **Gray 150**: #EAECF9 - Very light gray
- **Gray 100**: #F3F3FB - Near-white (light backgrounds)
- **Gray 50**: #FDFCFE - Off-white
- **Gray 50 0%**: #FDFCFE00 - Transparent off-white (gradient endpoints)

### Accent: Pink
- **Pink 400**: #E99DB1 - Warm pink accent

### Accent: Yellow
- **Yellow 300**: #FFC381 - Warm amber accent
- **Yellow 200**: #FFDFBB - Light peach/amber

### Brand Gradients

#### Gradients/Light (subtle backgrounds)
- **Light 50**: RADIAL - Gray 200 (#DEE3F6) → #E1E7F600
- **Light 100**: RADIAL - Gray 150 (#EAECF9) → Blue 200 (#D5E3FF) → Gray 250 (#C6D1F3)
- **Light 200**: LINEAR - Gray 150 (#EAECF9) → Blue 100 (#E2EBFF) → Gray 200 (#DEE3F6)
- **Light 300**: LINEAR - Gray 250 (#C6D1F3) → Blue 300 (#AFC8FB)

#### Gradients/Blue (brand emphasis)
- **Blue 100**: LINEAR - Blue 400 (#6891F9) → Blue 700 (#325BFF)
- **Blue 200**: LINEAR - Blue 400 (#6891F9) → Blue 700 (#325BFF)

#### Gradients/Accent (signature multi-stop spectrum)
- **Accent 50**: LINEAR - Blue 700 (#325BFF) → Pink 400 (#E99DB1)
- **Accent 100**: LINEAR - Blue 900 (#1A2761) → Blue 800 (#2635A7) → Blue 700 (#325BFF) → Blue 600 (#527DFF) → Blue 400 (#6891F9) → Pink 400 (#E99DB1) → Yellow 200 (#FFDFBB) → Gray 50 (#FDFCFE)
- **Accent 200**: LINEAR - Gray 50 0% (#FDFCFE00) → Yellow 200 (#FFDFBB) → Pink 400 (#E99DB1) → Blue 400 (#6891F9) → Blue 700 (#325BFF) → Blue 800 (#2635A7)
- **Accent 300**: LINEAR - Blue 900 (#1A2761) → Blue 700 (#325BFF) → Pink 400 (#E99DB1) → Yellow 200 (#FFDFBB) → Gray 100 (#F3F3FB)
- **Accent 400**: RADIAL - Blue 800 (#2635A7) → Blue 700 (#325BFF) → Blue 400 (#6891F9) → Pink 400 (#E99DB1) → Yellow 200 (#FFDFBB) → Gray 50 0% (#FDFCFE00)
- **Accent 500**: LINEAR - Blue 900 (#1A2761) → Blue 700 (#325BFF) → Pink 400 (#E99DB1) → Yellow 200 (#FFDFBB) → Gray 100 (#F3F3FB)
- **Accent 600**: LINEAR - Gray 50 (#FDFCFE) → Yellow 200 (#FFDFBB) → Pink 400 (#E99DB1) → Blue 400 (#6891F9) → Blue 600 (#527DFF) → Blue 700 (#325BFF) → Blue 800 (#2635A7) → Blue 900 (#1A2761)
- **Accent 700**: LINEAR - #FFDFB800 → Yellow 200 (#FFDFBB) → Pink 400 (#E99DB1) → Blue 400 (#6891F9) → Blue 700 (#325BFF) → Blue 800 (#2635A7)

### Gradient CSS Formulas

All named gradients are defined as CSS custom properties in `tokens.css`. These are the exact values — do not approximate.

**Light Gradients (card/panel backgrounds):**
- **Light-50:** `radial-gradient(125.72% 101.41% at 33.17% 0, #DEE3F6 0%, rgba(225,231,248,0) 100%)` — Section title backgrounds, fades to transparent
- **Light-100:** `radial-gradient(132.76% 119.84% at 33.95% 0, #EAECF9 50%, #D5E3FF 75%, #C6D1F3 100%)` — **Universal card background.** Used on every card, stat block, accordion trigger, value card, and quote panel on light surfaces. The asymmetric origin (~33% from left) creates a directional light-source illusion.
- **Light-200:** `linear-gradient(106deg, #EAECF9 50%, #E2EBFF 75%, #DEE3F6 100%)` — Hover overlays on light cards
- **Light-300:** `linear-gradient(135deg, #C6D1F3 0.52%, #AFC8FB 100.52%)` — Active/pressed states

**Blue Gradients (borders and accent lines):**
- **Blue-100:** `linear-gradient(252deg, #6891F9 -24.15%, #325BFF 60.2%)` — 2px top border on accordion items

**Accent Gradients (full brand spectrum):**
- **Accent-300:** `linear-gradient(180deg, #1A2761 0%, #325BFF 0%, #E99DB1 55.31%, #FFDFBB 83.84%, #F3F3FB 100%)` — Mobile CTA overlay
- **Accent-500:** `radial-gradient(113.06% 100% at 50% -0.06%, #1A2761 43.96%, #325BFF 53.45%, #E99DB1 68.28%, #FFDFBB 76.58%, #F3F3FB 83.7%)` — Mobile CTA background
- **Accent-700:** `linear-gradient(270deg, rgba(255,223,187,0) -35.47%, #FFDFBB -11.77%, #E99DB1 23.64%, #6891F9 66.2%, #325BFF 90.14%, #2635A7 106.54%)` — 4px divider bar (stats section, dropdown menus)

**WordPress Preset Gradients:**
- **Swimm:** `linear-gradient(135deg, #4154FF 0.21%, #8D98FF 100.21%)` — Hero banners
- **Beach:** `linear-gradient(45deg, #8D98FF 0%, #E4E7FF 36.46%, #E4E7FF 54.69%, #FFF78E 100%)` — Decorative light
- **Pink:** `linear-gradient(45deg, #8D98FF 0%, #E4E7FF 36.46%, #E4E7FF 54.69%, #DE9DFF 100%)` — Decorative variant
- **Shore:** `linear-gradient(45deg, #8D98FF 0%, #E4E7FF 36.46%, #E4E7FF 60.94%, #8D98FF 100%)` — Neutral light

---

## Typography

### Headings — Regesto Grotesk

| Level   | Size  | Weight  | Line Height | Letter Spacing |
|---------|-------|---------|-------------|----------------|
| Special | 60px  | Light   | 85%         | 0%             |
| H1      | 60px  | Regular | 110%        | 0%             |
| H2      | 42px  | Regular | 110%        | 0%             |
| H3      | 26px  | Regular | 110%        | 0%             |
| H4      | 20px  | Regular | 110%        | 0%             |
| H5      | 16px  | Regular | 110%        | 0%             |

**Mobile headings:** H1 40px, H2 30px, H3 24px, H4 18px, H5 16px (all Regular, 110% line height)

### Paragraphs — Manrope

| Level | Size  | Weight  | Line Height | Letter Spacing |
|-------|-------|---------|-------------|----------------|
| P1    | 18px  | Regular | 140%        | 0%             |
| P2    | 24px  | Light   | 140%        | 0%             |
| P3    | 20px  | Light   | 140%        | 0%             |
| P4    | 16px  | Regular | 140%        | 0%             |

**Mobile paragraphs:** P1 24px Regular, P2 20px Light, P3 18px Light, P4 14px Regular

### Labels — Manrope

| Level     | Size  | Weight  | Line Height | Letter Spacing | Transform |
|-----------|-------|---------|-------------|----------------|-----------|
| S         | 12px  | Regular | 140%        | 0%             | -         |
| M         | 14px  | Regular | 100%        | 0%             | -         |
| L         | 16px  | Regular | 85%         | 0%             | -         |
| XL        | 20px  | Light   | 120%        | 0%             | -         |
| Eyebrows  | 14px  | Regular | 100%        | 6%             | Uppercase |
| Footnotes | 12px  | Regular | 140%        | 1%             | -         |

---

## Design Principles

### Core Philosophy
Blog header images should convey **abstract relatability** to the subject matter - conceptual rather than literal representations.

### Style Fundamentals
- **Geometric shapes**: Clean diamonds, layered rectangular frames, perspective grids
- **Dot matrix patterns**: Like a grid but with dots that fade in density and shift from blue to pink/amber
- **Warm-to-cool spectrum**: Signature visual identity uses gradients flowing from Blue 900 through Pink 400 to Yellow 200
- **Layered depth**: Multiple stacked/nested frames with varying opacity create visual depth
- **Minimalist complexity**: Simple compositions that communicate clearly

### Color Application
- **Dark backgrounds**: Blue 900 (#1A2761) as default
- **Primary accent within shapes**: Blue 700 (#325BFF) - main brand blue
- **Warm accents**: Pink 400 (#E99DB1), Yellow 200 (#FFDFBB), Yellow 300 (#FFC381)
- **Stroke colors**: Blue 700, Blue 400 for borders and frame outlines
- **Stroke weight**: 1px for outlines and accents

### Composition Rules
- **Edge-to-edge**: Visuals fill the frame completely, OR
- **Two-thirds**: Composition occupies approximately 2/3 of the canvas with breathing room
- Choose based on the energy of the concept - edge-to-edge for dynamic, 2/3 for balanced

---

## Background Mesh (Dot Matrix)

When using a background pattern to add depth:
- **Style**: Dot matrix (small circles arranged in a grid)
- **Colors**: Blue 300 (#AFC8FB) to Blue 700 (#325BFF), with Pink 400 (#E99DB1) accents
- **Density**: Fades from dense (bottom-right or edges) to sparse (center or top-left)
- **Opacity**: Varies from ~20% to 100% based on position
- **Coverage**: Partial - typically concentrated in one corner or edge, not full-bleed

The dot matrix is optional - use when it adds visual interest or grounds the composition.

---

## Abstract Data Visualization

When incorporating charts or graphs for data-related topics:

### Approved Chart Types
- Abstract pie charts
- Simple bar graphs
- Line graphs/trends
- Circular/radial representations

### Data Viz Rules
- **No axes**: Charts are purely visual
- **No titles**: No chart titles or headers
- **No labels**: No series labels or data point labels
- **Color palette**: Blue 400 (#6891F9), Blue 700 (#325BFF), Blue 900 (#1A2761), Pink 400 (#E99DB1), Yellow 200 (#FFDFBB)

Charts are decorative and conceptual - they suggest data/analytics without presenting actual information.

---

## Typography on Images

### Default Behavior
**No text on images by default.**

### When Text is Appropriate
- Series titles (e.g., "Part 1", "Part 2")
- Section identifiers (e.g., "Deep Dive", "Guide")
- Short conceptual labels that enhance meaning

### Text Style Rules
- **Font**: Regesto Grotesk for headings, Manrope for body/labels
- **Color**: White (#FFFFFF) or brand colors with high contrast
- **Integration**: Text should feel designed into the composition, not overlaid
- **Avoid**: Full article titles (unless specifically requested), taglines, descriptions

---

## Logo Placement

- **Position**: Bottom-left corner
- **Color**: White (#FFFFFF)
- **Required on**: All banner images
- **File**: `context/assets/swimm-logo-white.svg`

### Logo Zone (for prompt composition)
The logo will be automatically added by the image generator. **Prompts must account for this space:**

- **Logo size**: 228x69 pixels (at 1920x960 resolution)
- **Position**: 69px from left edge, 56px from bottom edge
- **Clear zone**: Bottom-left ~300x130 pixels to give breathing room
- **In prompts**: Explicitly state "leave bottom-left corner clear for logo placement"
- **Composition tip**: Avoid placing key visual elements in the bottom-left quadrant

---

## What to Avoid

### Visual Anti-Patterns
- **Photorealistic imagery**: Never use photos or photorealistic renders
- **Images of people**: No human figures, faces, or silhouettes
- **Harsh lighting**: No dramatic shadows or lighting effects
- **Overly complex compositions**: Keep element count low
- **Gaussian blur**: No soft blurs or bokeh effects
- **Repeating patterns or textures**: Keep backgrounds clean

### Specific Prohibitions
- Stock photo aesthetics (handshakes, sticky notes, people pointing at screens)
- Matrix-style code rain or floating holograms
- Heavy gradients that dominate the composition
- Cartoonish or playful illustrations (maintain enterprise professionalism)
- Skeuomorphic design elements

### Brand Safety
- No imagery that could be misinterpreted negatively
- No representations of specific people without consent
- No copyrighted characters, logos, or trademarked imagery
- No imagery that excludes or stereotypes any group

---


## Output Specifications

### File Formats
- **Blog Banner**: PNG, 1920x960px (16:9)
- **LinkedIn**: PNG, 1080x1080px (1:1 square) of 1200x627
- **Diagrams**: PNG or SVG if vector output usuable
