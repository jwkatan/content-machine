# Construction Techniques

> The HOW manual for the Swimm design system. Every instruction is prescriptive, code-heavy, and copy-pasteable. This document teaches an LLM designer how to physically construct surfaces, layer elements, and compose sections.
>
> For token values, see `tokens.css`. For philosophy, see `design-philosophy.md`. For composition rules, see `composition-rules.md`.

---

## 1. The 3-Layer Surface Model

Every visible surface in the Swimm design system uses exactly 3 layers. No exceptions.

| Layer | Role | CSS Strategy | z-index |
|-------|------|-------------|---------|
| Layer 0 | Background | `position: absolute` or `background-image` | `z-index: 1` |
| Layer 1 | Interactive / State | `::before` or `::after` pseudo-element | `z-index: 1-2` |
| Layer 2 | Content | `position: relative` | `z-index: 2-4` |

**Parent container must always have:** `position: relative; overflow: hidden`

### Complete 3-layer CSS example

```css
/* Parent container — establishes stacking context */
.surface {
  position: relative;
  overflow: hidden;
  border-radius: 0;        /* Always 0 in Swimm */
  box-shadow: none;         /* Never box-shadows */
}

/* Layer 0 — Background (radial gradient, SVG, or flat color) */
.surface {
  background: radial-gradient(
    132.76% 119.84% at 33.95% 0,
    #EAECF9 50%, #D5E3FF 75%, #C6D1F3 100%
  );
}

/* Layer 1 — Interactive overlay (hidden at rest, revealed on hover) */
.surface::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(106deg, #EAECF9 50%, #E2EBFF 75%, #DEE3F6 100%);
  opacity: 0;
  transition: 0.3s ease-in-out;
  z-index: 1;
}

.surface:hover::after {
  opacity: 1;
}

/* Layer 2 — Content (text, buttons, icons) */
.surface .content {
  position: relative;
  z-index: 2;
}
```

**Rules:**
- Layer 0 is ALWAYS present. A surface without a background gradient is a wireframe, not a finished element.
- Layer 1 uses `opacity: 0` at rest and `opacity: 1` on hover. Never toggle `display` or `visibility`.
- Layer 2 content MUST have `position: relative; z-index: 2` or it will render beneath the hover overlay.
- The transition timing is always `0.3s ease-in-out`. No other timing values.

---

## 2. Light Card Construction

A flat solid-color card is a wireframe. Every light-surface card uses the **Light-100 radial gradient**:

```css
background: radial-gradient(
  132.76% 119.84% at 33.95% 0,
  #EAECF9 50%, #D5E3FF 75%, #C6D1F3 100%
);
```

### Token mapping

| Token | Hex | Role in gradient |
|-------|-----|-----------------|
| `--gray-150` | `#EAECF9` | Dominant fill (50%) — the most-used surface color on the entire site |
| `--blue-200` | `#D5E3FF` | Mid bloom (75%) |
| `--gray-250` | `#C6D1F3` | Cool edge (100%) |

### Origin is always asymmetric

The radial origin is `at 33.95% 0` (approximately one-third from the left edge, top). This creates an asymmetric light-source illusion. **Never center the origin** — centered radials look AI-generated.

The oversized radial dimensions (`132.76% 119.84%`) prevent visible gradient edges by extending the gradient past the element boundaries.

### Hover variant: Linear overlay

On hover, overlay Light-200 (a linear gradient) via the `::after` pseudo-element:

```css
.card::after {
  content: "";
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: linear-gradient(106deg, #EAECF9 50%, #E2EBFF 75%, #DEE3F6 100%);
  opacity: 0;
  transition: 0.3s ease-in-out;
  z-index: 1;
}
.card:hover::after { opacity: 1; }
```

### Hover variant: Radial origin shift

Some elements (stat blocks) use the same Light-100 gradient for both rest and hover, but shift the origin point:

```css
/* Resting state — bloom from far left */
.stat-block {
  background: radial-gradient(
    132.76% 119.84% at 13.95% 0,
    #EAECF9 50%, #D5E3FF 75%, #C6D1F3 100%
  );
}

/* Hover state — bloom shifts right */
.stat-block::before {
  content: "";
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: radial-gradient(
    132.76% 119.84% at 33.95% 0,
    #EAECF9 50%, #D5E3FF 75%, #C6D1F3 100%
  );
  opacity: 0;
  transition: 0.3s ease-in-out;
  z-index: 1;
}
.stat-block:hover::before { opacity: 1; }
```

This creates subtle movement without changing colors — only the light bloom position shifts from `13.95%` to `33.95%`.

### Full gradient reference (Light family)

| Name | Type | CSS Value | Usage |
|------|------|-----------|-------|
| Light-50 | radial | `radial-gradient(125.72% 101.41% at 33.17% 0, #DEE3F6 0, rgba(225,231,248,0) 100%)` | Section title backgrounds (fades to transparent) |
| Light-100 | radial | `radial-gradient(132.76% 119.84% at 33.95% 0, #EAECF9 50%, #D5E3FF 75%, #C6D1F3 100%)` | Universal card background |
| Light-200 | linear | `linear-gradient(106deg, #EAECF9 50%, #E2EBFF 75%, #DEE3F6 100%)` | Hover overlays on light cards |
| Light-300 | linear | `linear-gradient(135deg, #C6D1F3 0.52%, #AFC8FB 100.52%)` | Active/pressed states |

---

## 3. Dark Surface Depth

**Never use flat Blue-900 (`#1A2761`).** Every dark surface must have depth via SVG radials, dot-grid overlays, or blend-mode layering.

### For Marp slides

**Do NOT manually construct depth for Marp.** The Marp theme handles dark depth automatically. Every `dark-*` slide class has `::before` and `::after` pseudo-elements with exact SVG radial gradients from the Figma element library. Light slides also get automatic depth via the stat-block radial pattern. The HTML/CSS construction below applies to web output only — skip it entirely for Marp.

### For HTML/CSS

Apply SVG radial overlays from the element library. Position them the same way as any texture (see Section 7):

```css
.dark-section {
  position: relative;
  overflow: hidden;
  background: linear-gradient(252deg, #2635A7 0%, #1A2761 100%);
}

/* SVG radial overlay for depth */
.dark-section::before {
  content: "";
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: radial-gradient(
    ellipse 80% 80% at 30% 20%,
    rgba(50, 91, 255, 0.15) 0%,
    transparent 70%
  );
  z-index: 1;
}

.dark-section .content {
  position: relative;
  z-index: 2;
}
```

### Blend modes for dark surfaces

| Blend Mode | CSS | Purpose | Example |
|-----------|-----|---------|---------|
| Lighten | `mix-blend-mode: lighten` | Glow effects on dark backgrounds | SVG radial overlays, accent glows |
| Multiply | `mix-blend-mode: multiply` | Screenshot fade-ins on dark surfaces | Product screenshots fading into dark sections |
| Screen | `mix-blend-mode: screen` | Warm light transitions | Warm-to-cool gradient transitions |

### Active state (light-to-dark transition)

When an element transitions from light (resting) to dark (active):

| Property | Light (resting) | Dark (active) |
|----------|----------------|---------------|
| Background | Light-100 radial | `linear-gradient(252deg, #2635A7 0%, #1A2761 100%)` |
| Heading text | `#1A2761` (Blue-900) | `#FDFCFE` (Gray-50) |
| Body text | `#415992` (Gray-500) | `#AFC8FB` (Blue-300) |
| Hover overlay | `::after` with Light-200, opacity 0 to 1 | `::after { content: none }` (removed entirely) |
| Texture | Small 40x40 SVG icon, `opacity: 1` | Full-bleed Lottie, `opacity: 1` |

---

## 4. Hover Effect Recipe

### Universal pattern

Every interactive element on the site uses this exact construction:

```css
/* Container — establishes clipping context */
.element {
  position: relative;
  overflow: hidden;
}

/* Resting background (Layer 0) */
.element {
  background: radial-gradient(
    132.76% 119.84% at 33.95% 0,
    #EAECF9 50%, #D5E3FF 75%, #C6D1F3 100%
  );
}

/* Hover overlay (Layer 1) — always ::before or ::after */
.element::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(106deg, #EAECF9 50%, #E2EBFF 75%, #DEE3F6 100%);
  opacity: 0;
  transition: 0.3s ease-in-out;
  z-index: 1;
}

.element:hover::after {
  opacity: 1;
}

/* Content (Layer 2) — stays above the overlay */
.element .content {
  position: relative;
  z-index: 2;
}
```

**Critical rules:**
- The resting gradient and hover gradient are always DIFFERENT. Resting is radial (Light-100). Hover is linear (Light-200).
- Transition is always `0.3s ease-in-out`. Never `0.2s`, never `ease`, never `linear`.
- The `::after` z-index is `1`. Content z-index is `2`. This ensures content is never obscured.
- `overflow: hidden` on the parent clips the pseudo-element to the element bounds.

### Variant: Radial Origin Shift

For stat blocks and elements where color change is undesirable, shift only the gradient origin:

```css
/* Resting: light bloom from far left */
.stat-block {
  background: radial-gradient(
    132.76% 119.84% at 13.95% 0,
    #EAECF9 50%, #D5E3FF 75%, #C6D1F3 100%
  );
}

/* Hover: identical gradient, shifted origin */
.stat-block::before {
  content: "";
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: radial-gradient(
    132.76% 119.84% at 33.95% 0,
    #EAECF9 50%, #D5E3FF 75%, #C6D1F3 100%
  );
  opacity: 0;
  transition: 0.3s ease-in-out;
  z-index: 1;
}

.stat-block:hover::before { opacity: 1; }
.stat-block .content { position: relative; z-index: 2; }
```

The origin shifts from `13.95% 0` (far left) to `33.95% 0` (center-left). The visual effect is a subtle light bloom that slides rightward on hover.

---

## 5. Two-Part Button Construction

The Swimm button is not a single element. It is two adjacent blocks: a text block and an arrow block.

### HTML structure

```html
<a class="main-button">
  <div class="main-button-text">Get a demo</div>
  <div class="main-button-arrow">
    <svg width="14" height="10" viewBox="0 0 14 10" fill="none">
      <path d="M8.5 1L13 5M13 5L8.5 9M13 5H1" stroke="currentColor" stroke-width="1.5"/>
    </svg>
  </div>
</a>
```

### CSS construction

```css
.main-button {
  display: inline-flex;
  align-items: stretch;
  border-radius: 0;
  text-decoration: none;
  cursor: pointer;
}

/* ---- Text Block ---- */
.main-button-text {
  position: relative;
  overflow: hidden;
  z-index: 2;
  height: 34px;
  padding: 10px;
  margin-right: -1px;           /* Eliminates gap between blocks */
  font-family: 'Manrope', sans-serif;
  font-size: 14px;
  font-weight: 400;
  color: #E2EBFF;               /* Blue-100 */
  display: flex;
  align-items: center;
  background: linear-gradient(45deg,
    #2635A7 7.87%,              /* Blue-800 */
    #325BFF 67.64%,             /* Blue-700 */
    #527DFF 94.61%,             /* Blue-600 */
    #6891F9 100%                /* Blue-400 */
  );
}

/* Text block hover overlay */
.main-button-text::before {
  content: "";
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: linear-gradient(45deg,
    #2635A7 15.22%,             /* Blue-800 */
    #325BFF 65.44%,             /* Blue-700 */
    #527DFF 84.41%,             /* Blue-600 */
    #E99DB1 100%                /* Pink-400 — warm accent appears */
  );
  opacity: 0;
  transition: 0.3s ease-in-out;
  z-index: -1;
}

/* ---- Arrow Block ---- */
.main-button-arrow {
  position: relative;
  overflow: hidden;
  z-index: 1;
  width: 36px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #E2EBFF;               /* Blue-100 */
  background: linear-gradient(61deg,
    #2635A7 -111.76%,           /* Blue-800 (offscreen start) */
    #325BFF 36.47%,             /* Blue-700 */
    #527DFF 78.82%,             /* Blue-600 */
    #6891F9 100%                /* Blue-400 */
  );
}

/* Arrow block hover overlay */
.main-button-arrow::before {
  content: "";
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: linear-gradient(61deg,
    #2635A7 -68.06%,            /* Blue-800 */
    #325BFF 24.37%,             /* Blue-700 */
    #E99DB1 74.79%,             /* Pink-400 — warm */
    #FFC381 100%                /* Yellow-300 — warmest at edge */
  );
  opacity: 0;
  transition: 0.3s ease-in-out;
  z-index: -1;
}

/* ---- Hover Behavior ---- */
.main-button:hover .main-button-text::before,
.main-button:hover .main-button-arrow::before {
  opacity: 1;
}

/* ---- Active State ---- */
.main-button:active .main-button-text,
.main-button:active .main-button-arrow {
  background: #325BFF;          /* Blue-700 solid */
}
```

### Design rationale

- `margin-right: -1px` on the text block eliminates the subpixel gap between the two blocks.
- `border-radius: 0` everywhere. Swimm buttons have no rounding.
- The arrow's hover gradient is warmer (reaches Pink-400 and Yellow-300). This creates directional warmth that pulls the eye toward the action.
- Both `::before` elements go from `opacity: 0` to `opacity: 1` simultaneously on parent hover.

---

## 6. Gradient Bridge (Nested Rectangles)

The gradient bridge is the most complex reusable element. It creates concentric rings of gradient around a content card, producing environmental depth.

### Two variants

| Variant | SVG Asset | Dimensions | Direction |
|---------|----------|-----------|-----------|
| S2 | `cta-bg-element-1.svg` | 2080 x 472px | Bottom-anchored, rings arc upward |
| CTA | `cta-bg-element.svg` | 2016 x 446px | Top-anchored, rings descend downward |

### Layer A: Edge Bars (the "staircase" wings)

8 bars on each side (left and right), symmetrical. Each bar:
- **Width:** 36px (outer) or 35px (innermost)
- **Heights** (decreasing from center outward): 254px, 222px, 173px, 130px, 107px, 39px, 37px, 22px
- **Fill:** Linear gradient with the full accent spectrum

```
Stop 0.00: #FDFCFE (Gray-50)  — opacity 0      (transparent at outer edge)
Stop 0.17: #FFDFBB (Yellow-200) — opacity varies  (warm accent)
Stop 0.42: #E99DB1 (Pink-400)   — opacity varies  (warm accent)
Stop 0.72: #6891F9 (Blue-400)   — opacity 1.0     (solid blue)
Stop 0.88: #325BFF (Blue-700)   — opacity 1.0     (solid blue)
Stop 1.00: #2635A7 (Blue-800)   — opacity 1.0     (deepest blue at inner edge)
```

**Warm color opacity cascades per bar** (from center outward):

| Bar | Distance from center | Yellow/Pink opacity |
|-----|---------------------|-------------------|
| 1 | Closest | 0.8 |
| 2 | | 0.6 |
| 3 | | 0.4 |
| 4 | | 0.2 |
| 5 | | 0.1 |
| 6 | | 0.06 |
| 7 | | 0 (pure blue to transparent) |
| 8 | Outermost | 0 |

This creates the gradient feeling: warm colors closest to center, fading to pure blue on outer bars, fading to transparent at the edges.

### Layer B: Core Gradient Area

A radial gradient filling the central 1440px area:

**S2 version** (radial from bottom):
```
Origin: translate(720, 530.508) — below the visible area
Blue-800 (center) → Blue-700 → Blue-400 → Pink-400 → Yellow-200 → transparent
```

**CTA version** (linear from top):
```
Blue-900 17.5% → Blue-700 39.3% → Pink-400 62.0% → Yellow-200 79.3% → transparent 88.9%
```

### Layer C: Nested Inner Rectangles

3-4 nested rectangles, each progressively narrower, with clip-paths:

| Rectangle | Width | Inset per side |
|-----------|-------|---------------|
| Rect 1 | 1440px | 0 |
| Rect 2 | 1368px | -36px each side |
| Rect 3 | 1296px | -36px each side |
| Rect 4 | 1224px | -36px each side |

Each rect uses the SAME gradient stops but with different y-coordinates. The clip-paths prevent overflow.

### The shared 6-stop accent spectrum

Every gradient bar and ring uses this spectrum. Only opacity and y-coordinates change.

```
Stop 1: #1A2761 (Blue-900)   — 17.5%   (deepest, center of arc)
Stop 2: #325BFF (Blue-700)   — 39.3%   (primary blue)
Stop 3: #E99DB1 (Pink-400)   — 62.0%   (warm pink transition)
Stop 4: #FFDFBB (Yellow-200) — 79.3%   (warm yellow)
Stop 5: #F3F3FB (Gray-100)   — 88.9%   (page background — seamless edge)
Stop 6: transparent           — 100%    (fade out)
```

### CSS/HTML approximation (for Marp and non-SVG contexts)

When the pre-rendered SVG is not available, use nested `<div>` elements:

```html
<!-- Outermost ring — full spectrum, full opacity -->
<div style="
  background: linear-gradient(180deg,
    #1A2761 17%, #325BFF 39%,
    #E99DB1 62%, #FFDFBB 79%,
    #F3F3FB 89%);
  padding: 36px;
">
  <!-- Middle ring — warm colors at reduced opacity -->
  <div style="
    background: linear-gradient(180deg,
      #2635A7 17%, #325BFF 39%,
      rgba(233,157,177,0.6) 62%, rgba(255,223,187,0.6) 79%,
      #F3F3FB 89%);
    padding: 36px;
  ">
    <!-- Content card — page background color -->
    <div style="
      background: #F3F3FB;
      padding: 64px 100px;
    ">
      <!-- heading + body here -->
    </div>
  </div>
</div>
```

**The key principle:** Each ring uses the same gradient stops but warm colors (Pink, Yellow) reduce in opacity for outer rings. The content card uses the page background color (`#F3F3FB`) to appear "cut in" to the gradient environment.

---

## 7. Texture Positioning

### Self-masking principle

Swimm textures are NOT clipped or masked by CSS. The SVG/Lottie asset itself fades to transparent internally — visual interest concentrates in one area and dissolves outward. CSS only anchors the corner.

### Universal texture positioning recipe

```css
.card {
  position: relative;
  overflow: hidden;
}

.texture {
  position: absolute;
  top: 0;
  right: 0;             /* Anchor to top-right corner */
  z-index: 1;           /* Above background, below content */
  opacity: 0.7;         /* Subtle: 0.7. Featured: 1.0 */
  pointer-events: none;
  /* Width can exceed the card — overflow:hidden on parent clips it */
}

.content {
  position: relative;
  z-index: 2;           /* Always above texture */
}
```

### Texture Type 1: Geometric Icon / Dot Matrix

**Small (closed state):** 40 x 40px SVG

- Differentiation-A: 3x3 grid of 4px squares + 10px center square
- Differentiation-B: 3x3 grid of stroked 12px cells with 2px filled dots
- Differentiation-C: Radial lines from a center 8px square
- Fill color: `#325BFF` (Blue-700)

**Large (active state):** 648 x 192px Lottie animation

- 5 layers, 60fps, 330 frames (5.5s loop)
- Positioning: `position: absolute; top: 0; right: 0; width: 100%; pointer-events: none`
- Visual content concentrates in upper-right

**Transition between states:**

```css
/* Closed state */
.icon-small { opacity: 1; transition: opacity 0.3s ease-in-out; }
.lottie-large { opacity: 0; transition: opacity 0.3s ease-in-out; }

/* Active state */
.active .icon-small { opacity: 0; }
.active .lottie-large { opacity: 1; }
```

### Texture Type 2: Mesh-Grid Dot Field

**Asset:** `mesh-grid-1.svg` (832 x 248px)

- Hundreds of individual `<path>` elements
- Each dot has a uniquely calculated fill:
  - Left edge: `#FFFFFF` (pure white, dots ~0.1px — nearly invisible)
  - Middle: `#FAF8FA` (faint blue tint, dots ~0.2px)
  - Right edge: `#EDEBF5` (blue-purple, dots ~0.5px — clearly visible)
- Dots grow in both SIZE and COLOR SATURATION from left to right
- Positioning: `position: absolute; top: 0; right: 0; opacity: 0.7; z-index: 1`

### Texture Type 3: Directional Bar Illustrations

**Asset:** e.g. `ValueAccurate-1.svg` (330 x 218px)

- Horizontal bars anchored to top-right corner
- Each bar extends leftward with gradient fill: `Blue-900 → Blue-700 → Blue-600 → transparent`
- Bars widen as they descend (stepped waterfall)
- Thin connecting lines: `stroke: #2635A7; stroke-width: 0.75px`

**Positioning:**

```css
.value-card {
  background-image: url('ValueAccurate-1.svg');
  background-position: right 0 top 0;
  background-size: contain;
  background-repeat: no-repeat;
}
```

### Texture Type 4: Environment Gradient SVGs

The largest textures (2016-2080px wide). These are the gradient bridge assets (see Section 6). Positioned behind entire sections, not individual cards.

```css
.section-bg-svg {
  position: absolute;
  z-index: 1;
  width: 2080px;                    /* Asset's natural width */
  left: 50%;
  transform: translateX(-50%);      /* Center horizontally */
  object-fit: cover;
  top: 0;                           /* CTA variant: top-anchored */
  /* bottom: 0;                     S2 variant: bottom-anchored */
}
```

---

## 8. Card-in-Gradient-Environment

This technique makes a content card appear "cut into" a gradient section, not floating above it.

### The trick

The content card has the **same background color as the page** (`#F3F3FB`, Gray-100). The section behind it has a gradient. The gradient is only visible in the gap between the card edge and the section edge.

### Complete structure

```
Section
├── position: relative; overflow: hidden; background: #F3F3FB
│
├── SVG/gradient background
│   └── position: absolute; z-index: 1
│       width: 2016-2080px; left: 50%; transform: translateX(-50%)
│       object-fit: cover
│
├── Container
│   └── position: relative; z-index: 4; max-width: 1440px; margin: 0 auto
│
│   └── Content card
│       └── background: #F3F3FB; padding: 100px; max-width: 1152px
│           border-radius: 0; display: grid
```

### CSS implementation

```css
.gradient-section {
  position: relative;
  overflow: hidden;
  background: #F3F3FB;           /* Gray-100 — page background */
}

.gradient-section .bg-svg {
  position: absolute;
  z-index: 1;
  width: 2016px;
  height: 450px;
  left: 50%;
  transform: translateX(-50%);
  object-fit: cover;
  top: 0;
}

.gradient-section .container {
  position: relative;
  z-index: 4;
  max-width: 1440px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gradient-section .content-card {
  background: #F3F3FB;           /* Same as page — "cut in" effect */
  padding: 64px 100px;
  max-width: 1152px;
  width: 100%;
  border-radius: 0;
  text-align: center;
}
```

**Why this works:** Because the card and page share the same background color, the card has no visible border or edge against the page. The gradient is only visible in the padding gap between the card and the section wrapper. The card appears to be a window through the gradient into the page surface below.

---

## 9. Section Composition

### Full-bleed section pattern

Every section spans the full viewport width, even when nested inside a constrained parent:

```css
.section {
  width: 100vw;
  left: 50%;
  transform: translateX(-50%);
  position: relative;
  overflow: hidden;
  background: #F3F3FB;           /* Gray-100 */
}
```

### Width hierarchy

| Level | Width | Token / Value | Usage |
|-------|-------|--------------|-------|
| Viewport | 100vw | — | Section wrapper |
| SVG environment | 2016-2080px | — | Gradient bridge background |
| Page canvas | 1440px | `--page-max-w` | Outer container max-width |
| Content max | 1200px | `--content-max-w` | Default content max-width |
| Content card | 1152px | — | Inner content card max-width |
| Small container | 1040px | — | Stats, quotes, constrained sections |

### Section padding reference

| Context | Desktop | Tablet | Mobile |
|---------|---------|--------|--------|
| Hero content | 180px top | 100px top | 50px top |
| Content card (S2, CTA) | 100px | 60px 36px | 40px 24px |
| Section gap (S3) | 140px top, 100px bottom | 60px | 60px 20px 30px |
| Stats (S5) | 50px 20px | 30px 20px | 30px 20px |

### Grid layouts

| Pattern | CSS | Gap | Usage |
|---------|-----|-----|-------|
| Equal thirds | `grid-template-columns: repeat(3, 1fr)` | `0` | Value cards, stat blocks |
| Trust grid | `grid-template-columns: 288px 288px 288px` | `32px` column, `48px` row | Icon + text items (6-up) |
| Split content | `grid-template-columns: 1fr 1fr` | `52px` | Heading left + description right |
| Title + accordion | `grid-template-columns: repeat(3, minmax(0, 1fr))` | `0` | Title col 1, accordion cols 2-3 |

### Complete section example (stat block section)

```css
/* Section wrapper */
.stats-section {
  width: 100vw;
  left: 50%;
  transform: translateX(-50%);
  position: relative;
  overflow: hidden;
  background: #F3F3FB;
  padding: 50px 20px;
}

/* Inner container */
.stats-container {
  max-width: 1040px;
  margin: 0 auto;
  position: relative;
}

/* Gradient top border (Accent-700) */
.stats-container::before {
  content: "";
  position: absolute;
  top: -4px;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(270deg,
    rgba(255,223,187,0) -35.47%,
    #FFDFBB -11.77%,
    #E99DB1 23.64%,
    #6891F9 66.2%,
    #325BFF 90.14%,
    #2635A7 106.54%
  );
}

/* 3-column grid, no gap */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0;
}

/* Individual stat block */
.stat-block {
  position: relative;
  overflow: hidden;
  padding: 38px 48px;
  background: radial-gradient(
    132.76% 119.84% at 13.95% 0,
    #EAECF9 50%, #D5E3FF 75%, #C6D1F3 100%
  );
}

/* Stat number — Manrope Light 300, NOT Regesto Grotesk */
.stat-number {
  font-family: 'Manrope', sans-serif;
  font-size: 60px;
  font-weight: 300;
  line-height: 0.85;
  color: #1A2761;
}

/* Stat suffix (%, +) */
.stat-suffix {
  font-family: 'Manrope', sans-serif;
  font-size: 38.7px;
  font-weight: 300;
}

/* Stat description */
.stat-description {
  font-family: 'Manrope', sans-serif;
  font-size: 20px;
  font-weight: 300;
  color: #415992;
}
```

---

## 10. Responsive Breakpoints

| Breakpoint | Name | Key Changes |
|-----------|------|-------------|
| <=1384px | Large desktop | Footer column gap reduces, accordion height reduces |
| <=1199px | Tablet landscape | Content max-width: 768-900px, horizontal accordion collapses to vertical |
| <=991px | Tablet | Mobile nav activates, hero font: 56px, grids go single-column |
| <=767px | Mobile landscape | H1: 48px, H2: 40px, content padding: 40px 24px, SVG gradient bridge replaced with CSS fallback |
| <=544px | Mobile | H1: 40px, hero width: calc(100% - 48px), stat grid: 1 column |
| <=425px | Small mobile | H1: 28px, nav buttons: min-width 120px |

### Mobile gradient bridge fallback

On mobile (<=767px), the SVG gradient bridge is hidden (`display: none`) and replaced with a CSS radial gradient:

```css
@media (max-width: 767px) {
  .gradient-section .bg-svg {
    display: none;
  }

  .gradient-section {
    background: radial-gradient(
      113.06% 100% at 50% -0.06%,
      #1A2761 43.96%,
      #325BFF 53.45%,
      #E99DB1 68.28%,
      #FFDFBB 76.58%,
      #F3F3FB 83.7%
    );
  }
}
```

### Responsive typography scale

```css
@media (max-width: 991px) {
  h1 { font-size: 56px; }
}

@media (max-width: 767px) {
  h1 { font-size: 48px; }
  h2 { font-size: 40px; }
}

@media (max-width: 544px) {
  h1 { font-size: 40px; }
}

@media (max-width: 425px) {
  h1 { font-size: 28px; }
}
```

### Responsive content padding

```css
@media (max-width: 767px) {
  .content-card {
    padding: 40px 24px;         /* Down from 100px / 64px 100px */
  }
}

@media (max-width: 544px) {
  .hero-content {
    width: calc(100% - 48px);   /* 24px margin each side */
  }

  .stats-grid {
    grid-template-columns: 1fr; /* Single column */
  }
}

@media (max-width: 425px) {
  .nav-button {
    min-width: 120px;
  }
}
```

### Responsive grid collapse order

1. **>1199px:** All grids at full column count
2. **<=1199px:** Horizontal accordion collapses to vertical stack. Content max-width narrows to 768-900px.
3. **<=991px:** 3-column grids (value cards, stats, trust grid) collapse to 1 column. Split content (1fr 1fr) stacks vertically.
4. **<=544px:** All remaining multi-column layouts go single-column.
