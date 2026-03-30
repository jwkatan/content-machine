# Composition Rules

How elements combine. Derived from the Figma homepage and product page designs.

All CSS examples reference variables from `tokens.css`. Import it once; every snippet below inherits the same token set.

---

## Section Rhythm

Alternate dark (`--bg-dark` / Blue 900) and light (`--bg-light` / Gray 100) surfaces to create visual contrast between page sections.

**Rules:**
- Never more than 2 consecutive same-surface sections.
- The gradient CTA section serves as the dark-to-light transition at page bottom.
- Homepage reference pattern: Hero (dark) -> Content (light) -> Features (light) -> Icon Cards (dark) -> Statement (dark) -> Trust (dark) -> CTA (gradient) -> Footer (light).

```css
/* Section Rhythm — surface alternation */
.section--dark {
  background-color: var(--bg-dark);
  color: var(--text-heading-dark);
}
.section--dark p {
  color: var(--text-body-dark);
}

.section--light {
  background-color: var(--bg-light);
  color: var(--text-heading-light);
}
.section--light p {
  color: var(--text-body-light);
}
```

---

## Section Anatomy

Every section shares the same structural skeleton: 100px vertical padding, a 1200px content max-width centered inside a 1440px page canvas, and element-specific horizontal padding (48px for the header; other elements vary). The 1920px variant uses the same max-width with more horizontal breathing room. Note: there is no universal 120px horizontal padding — horizontal padding is element-specific.

```css
/* Section Anatomy */
.section {
  padding: var(--section-pad-v) var(--section-pad-h);
  max-width: var(--page-max-w);           /* 1440px */
  margin: 0 auto;
}
.section-content {
  max-width: var(--content-max-w);         /* 1200px */
  margin: 0 auto;
}

/* Header uses tighter horizontal padding */
.header {
  padding-left: var(--header-pad-h);       /* 48px */
  padding-right: var(--header-pad-h);
}
```

---

## Section Intros (Split Layout)

Used at the top of content sections to introduce what follows. H2 heading on the left, P3 body text on the right. Both aligned to the top of the row.

```css
/* Section Intro — Split Layout */
.section-intro {
  display: flex;
  align-items: flex-start;
  gap: var(--sp-5);                        /* 40px */
  max-width: var(--content-max-w);
  margin: 0 auto;
}
.section-intro__heading {
  flex: 1;
  max-width: 500px;
  font-family: var(--title-font);
  font-size: var(--h2-size);              /* 42px */
  font-weight: var(--h2-weight);
  line-height: var(--h2-lh);
}
.section-intro__body {
  flex: 1;
  max-width: 450px;
  font-family: var(--text-font);
  font-size: var(--p3-size);              /* 20px */
  font-weight: var(--p3-weight);
  line-height: var(--p3-lh);
}
```

---

## Card Grids

3-column layout with equal flex. 32px internal padding per card, 24px gap between icon and text, 12px gap between title and description. On dark surfaces, cards get a radial gradient background. On light surfaces, cards rely on spacing and typography alone.

```css
/* Card Grid */
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--sp-4);                        /* 32px */
  max-width: var(--content-max-w);
  margin: 0 auto;
}

.card {
  padding: var(--card-pad);                /* 32px */
  /* No border-radius — cards use sharp corners */
}
.card__icon {
  margin-bottom: var(--card-icon-gap);     /* 24px */
}
.card__title {
  font-family: var(--title-font);
  font-size: var(--h4-size);              /* 20px */
  font-weight: var(--h4-weight);
  line-height: var(--h4-lh);
  margin-bottom: var(--card-text-gap);     /* 12px */
}
.card__description {
  font-family: var(--text-font);
  font-size: var(--p4-size);              /* 16px */
  font-weight: var(--p4-weight);
  line-height: var(--p4-lh);
}

/* Dark surface treatment — radial gradient per card */
.section--dark .card {
  background: radial-gradient(
    ellipse at top left,
    rgba(50, 91, 255, 0.15) 0%,
    transparent 70%
  );
}

/* Light surface treatment — no background */
.section--light .card {
  background: none;
}
```

---

## Icon & Text Grids

2 rows by 3 columns. 60px column gap, 32px row gap. Icon is 64px square. Title in H4 (Regesto Grotesk 20px, Gray 150 on dark). Description in P4 (Manrope 16px, Blue 300 on dark).

```css
/* Icon & Text Grid */
.icon-text-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  column-gap: 60px;
  row-gap: var(--sp-4);                    /* 32px */
  max-width: var(--content-max-w);
  margin: 0 auto;
}

.icon-text-item__icon {
  width: var(--sp-8);                      /* 64px */
  height: var(--sp-8);
  margin-bottom: var(--sp-3);             /* 24px */
}
.icon-text-item__title {
  font-family: var(--title-font);
  font-size: var(--h4-size);              /* 20px */
  font-weight: var(--h4-weight);
  line-height: var(--h4-lh);
  color: var(--gray-150);
}
.icon-text-item__description {
  font-family: var(--text-font);
  font-size: var(--p4-size);              /* 16px */
  font-weight: var(--p4-weight);
  line-height: var(--p4-lh);
  color: var(--blue-300);
}
```

---

## Screenshot Placement

Screenshots are always placed inside a gradient-backed frame. The gradient runs from Blue 400 to Blue 700 (using `--gradient-blue`). The frame has generous padding; the screenshot fills the white content area within it. The screenshot itself is swappable — the frame treatment is the constant.

```css
/* Screenshot Frame */
.screenshot-frame {
  background: var(--gradient-blue);        /* Blue 400 → Blue 700 */
  padding: 80px 100px;
  /* No border-radius — screenshot frames use sharp corners */
}
.screenshot-frame__inner {
  background: #FFFFFF;
  /* No border-radius — sharp corners */
  overflow: hidden;
}
.screenshot-frame__inner img {
  display: block;
  width: 100%;
  height: auto;
}
```

---

## The CTA Bridge (Signature Element)

The most distinctive composition in the Swimm design system. Four nested containers create concentric gradient borders that fade from Blue 900 through Pink 400 and Yellow 200 into Gray 100. Each nesting level uses absolutely-positioned gradient background child divs, `overflow: clip`, and a 10px gap between levels. The innermost container has a Gray 100 background with centered content (H2 heading and CTA button). The 36px padding at each level creates the nesting frame depth.

Reserved for the **last section before the footer** — the closer.

```css
/* CTA Bridge — Quad-nested gradient container */
.cta-bridge {
  padding: var(--section-pad-v) var(--section-pad-h);
  max-width: var(--page-max-w);
  margin: 0 auto;
}

.cta-bridge__level {
  position: relative;
  overflow: clip;
  padding: 36px;                          /* nesting frame padding */
  gap: 10px;
}

.cta-bridge__level-bg {
  /* Absolutely-positioned gradient background child */
  position: absolute;
  inset: 0;
  background: var(--gradient-cta);
  /*
    --gradient-cta resolves to:
    linear-gradient(
      180deg,
      var(--blue-900) 34.286%,
      var(--blue-700) 56.023%,
      var(--pink-400) 70.306%,
      var(--yellow-200) 83.838%,
      var(--gray-100) 91.355%
    )
  */
  z-index: 0;
}

/* 4 nesting levels: outer → mid-outer → mid-inner → inner */
.cta-bridge__outer,
.cta-bridge__mid-outer,
.cta-bridge__mid-inner,
.cta-bridge__inner {
  position: relative;
  overflow: clip;
  padding: 36px;
}

.cta-bridge__content {
  position: relative;
  z-index: 1;
  background: var(--bg-light);             /* Gray 100 */
  /* No border-radius — sharp corners */
  padding: var(--sp-8) var(--sp-6);        /* 64px 48px */
  text-align: center;
}

.cta-bridge__content h2 {
  font-family: var(--title-font);
  font-size: var(--h2-size);              /* 42px */
  font-weight: var(--h2-weight);
  line-height: var(--h2-lh);
  color: var(--text-heading-light);
  margin-bottom: var(--sp-4);             /* 32px */
}

.cta-bridge__content .btn-cta {
  display: inline-block;
  padding: var(--sp-2) var(--sp-4);        /* 16px 32px */
  background-color: var(--accent-primary); /* Blue 700 */
  color: #FFFFFF;
  font-family: var(--text-font);
  font-size: var(--p4-size);
  font-weight: 500;
  border-radius: var(--sp-1);             /* 8px */
  text-decoration: none;
  border: none;
  cursor: pointer;
}
```

**HTML structure (4 levels with abs-positioned gradient backgrounds):**

```html
<section class="cta-bridge">
  <div class="cta-bridge__outer">
    <div class="cta-bridge__level-bg"></div>
    <div class="cta-bridge__mid-outer">
      <div class="cta-bridge__level-bg"></div>
      <div class="cta-bridge__mid-inner">
        <div class="cta-bridge__level-bg"></div>
        <div class="cta-bridge__inner">
          <div class="cta-bridge__level-bg"></div>
          <div class="cta-bridge__content">
            <h2>Heading text here</h2>
            <a href="#" class="btn-cta">Call to action</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

## Feature Presentation

Feature list on the left with accordion-style interaction. Screenshot area on the right inside a gradient-backed frame. The active feature controls which screenshot is displayed.

- **Active state:** Title + description visible, bottom border separator.
- **Default state:** Title only, shown on a gradient background.

```css
/* Feature Presentation — Split Layout */
.feature-presentation {
  display: flex;
  align-items: flex-start;
  gap: var(--sp-8);                        /* 64px */
  max-width: var(--content-max-w);
  margin: 0 auto;
}

/* Feature List (left column) */
.feature-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.feature-item {
  padding: var(--sp-3) 0;                  /* 24px vertical */
  cursor: pointer;
}

/* Default state — title only */
.feature-item__title {
  font-family: var(--title-font);
  font-size: var(--h4-size);              /* 20px */
  font-weight: var(--h4-weight);
  line-height: var(--h4-lh);
  color: var(--text-heading-dark);
}
.feature-item__description {
  display: none;
  font-family: var(--text-font);
  font-size: var(--p4-size);
  font-weight: var(--p4-weight);
  line-height: var(--p4-lh);
  color: var(--text-body-dark);
  margin-top: var(--sp-2);                /* 16px */
}

/* Active state — title + description + border */
.feature-item--active .feature-item__description {
  display: block;
}
.feature-item--active {
  border-bottom: 1px solid var(--gray-300);
  padding-bottom: var(--sp-3);
}

/* Screenshot (right column) */
.feature-screenshot {
  flex: 1;
  background: var(--gradient-blue);
  padding: 80px 100px;
  /* No border-radius — sharp corners */
}
.feature-screenshot__inner {
  background: #FFFFFF;
  /* No border-radius — sharp corners */
  overflow: hidden;
}
.feature-screenshot__inner img {
  display: block;
  width: 100%;
  height: auto;
}
```

---

## PPTX / Marp Adaptation

When translating web compositions to slide decks, follow these mappings. Spacing relationships scale proportionally — use the same ratios, not the same pixel values. Note: the 8px grid is a guideline, not strict. Only ~29% of actual spacing values land on the 8px grid. The most structurally important value is 36px (nesting frame padding), and 12px is the second most common spacing value — neither is on the 8px grid. Dark/light section rhythm becomes slide-to-slide contrast alternation. Minimum body text size for projection: 20px.

| Web Pattern | Slide Equivalent |
|---|---|
| Section (dark/light) | Slide background alternation (dark/light) |
| Gradient Section | Title / divider slide background |
| CTA Bridge | Closing slide background |
| Icon Card Grid (3 cards) | Single slide, 3 cards arranged horizontally |
| Feature Accordion | Build sequence: one slide per feature, screenshot changes |
| Split Layout Intro | Slide with headline left, supporting text right |
| Quote Block | Full-bleed quote slide |
| Stat Block | Data highlight slide |

### Marp-Specific Rules

**USE THE THEME FILE.** All Marp output must use `context/design-system/marp-theme.css`. Copy its full contents into the `<style>` block. Do NOT write CSS from scratch. The theme provides pre-tested slide type classes that handle surface, depth, layout, and canvas fill.

Marp auto-generates `<section>` elements from `---` slide separators. You cannot use `<section>` tags directly in Marp content — they will be ignored or cause rendering failures.

**Applying classes to slides:** Use the `<!-- _class: classname -->` directive immediately after the `---` separator:

```markdown
---
<!-- _class: dark-statement -->

<h1>Bold <span class="accent">claim</span> here</h1>
<p>Supporting context below.</p>
```

Do NOT use `<section class="dark-statement">` — Marp will not apply the class.

**Available slide type classes** (see marp-theme.css for full documentation):
- `title-gradient` — Title slide (gradient bg + centered card)
- `dark-statement` — Bold typographic claim (centered)
- `dark-bullets` — Heading + bullet list (left-aligned)
- `dark-cards` — Heading + card row (2-4 cards)
- `dark-stats` — Heading + stat block row
- `dark-split` — Text + visual two-column
- `dark-divider` — Section transition (centered heading)
- `dark-twocol` — Two-column comparison
- `dark-flow` — Process/flow diagram
- `light-screenshot` — Full-width screenshot with heading
- `light-split` — Text + screenshot split
- `light-multi` — Multiple screenshot grid
- `light-bullets` — Heading + bullets on light
- `closing-gradient` — CTA/closing slide (gradient bg + card)

**HTML inside slides:** Inline HTML elements (`<div>`, `<span>`, `<svg>`, etc.) work normally inside Marp slides. Only `<section>` is reserved by Marp.

**Local fonts:** Use `@font-face` with `src: local('Font Name')` in the `<style>` block. Marp renders locally, so system-installed fonts are available.

**NEVER use inline styles for layout.** The theme handles all centering, spacing, and canvas fill. If the theme doesn't support a layout you need, flag the gap — do not patch with inline styles.

### Slide Visual Requirements

These requirements are ENFORCED by the theme — every `dark-*` class includes depth pseudo-elements, every class defines layout centering. But verify these are met in every output:

1. **No bare text-on-background slides.** Every slide must include at least one visual element beyond text — a gradient treatment, card layout, icon grid, screenshot frame, radial overlay, or decorative pattern. Text on a flat colored background is a wireframe, not a designed slide.

2. **Dark slides must have depth.** A flat Blue 900 background is never acceptable. The theme handles this automatically via `::before` and `::after` pseudo-elements on all `dark-*` classes. Each dark variant uses a different depth signature (blue top-left, warm bottom-right, centered glow, etc.) for visual variety. Additional depth options include dot grid patterns from the `background-mesh` element (a flat grid, not a wave) and SVG radial gradients with transform matrices.

3. **Content must fill the canvas.** The theme's `justify-content: center` on all slide types vertically centers content. Use the full width of card rows, stat rows, and split layouts.

4. **Vary visual treatments.** No two consecutive slides should use the same slide type class. Each slide needs its own visual identity.

5. **Strict type scale only.** Heading sizes for slides: H1 60px (title/closing only), H2 42px (section headings), H3 26px (card/subsection titles), H4 20px (small headings). No custom sizes.

---

## Light Card Background Rule

Every card on a light surface uses `--gradient-light-100` as its background:

```css
background: radial-gradient(132.76% 119.84% at 33.95% 0,
  var(--gray-150) 50%, var(--blue-200) 75%, var(--gray-250) 100%);
```

No flat `background: var(--bg-light)` or `background: var(--gray-100)` on cards. A solid-color card is a wireframe, not a finished surface. The radial gradient creates subtle depth — an asymmetric bloom from the upper-third-left (~33% from left) that gives each card its own light source.

**On hover:** Apply `--gradient-light-200` (linear, 106deg) as an `::after` overlay at `opacity: 0 → 1`, or shift the radial origin from `33.95%` to `13.95%` for a subtle light-source movement.

**On dark surfaces:** Cards use the dark card element from the library with SVG radial depth. This rule applies only to light-surface cards.

---

## Card-in-Gradient-Environment

A composition pattern where the content card has the same background color as the page (`var(--bg-light)`, Gray-100). The card sits inside a gradient section, so the gradient is visible only in the gap between the card edge and the section edge. The card appears "cut into" the gradient environment, not floating above it.

**Structure:**
```
Section wrapper:
  position: relative; overflow: hidden;
  background: var(--bg-light);
  width: 100vw; left: 50%; transform: translateX(-50%);

  SVG or gradient background:
    position: absolute; z-index: 1;
    width: 2016-2080px (oversized, centered with transform)

  Container:
    position: relative; z-index: 4;
    max-width: var(--page-max-w);  /* 1440px */
    margin: 0 auto; padding: 30px;

    Content card:
      background: var(--bg-light);  /* same as page bg */
      padding: 100px (desktop) / 60px 36px (tablet) / 40px 24px (mobile);
      max-width: var(--content-inner-w);  /* 1152px */
      border-radius: 0;
```

**When to use:** CTA sections, gradient bridge sections, statement sections with emphasis. The gradient bridge SVG (see construction-techniques.md Section 6) provides the gradient environment.

---

## Gradient Accent Border

A thin gradient bar used as a visual separator or section divider:

```css
.section { position: relative; }
.section::before {
  content: "";
  position: absolute;
  top: -4px;
  left: 0;
  width: 100%;
  height: 4px;
  background: var(--gradient-accent-700);
}
```

The Accent-700 gradient runs 270deg (Yellow → Pink → Blue, warm to cool). Use above stat blocks, below dropdown menus, and between major sections. The 4px height is standard; 2px is used for lighter accents (e.g., `--gradient-blue-100` on accordion item tops).

---

## Responsive Breakpoints

| Breakpoint | Name | Key changes |
|-----------|------|-------------|
| ≤1384px | Large desktop | Footer column gap reduces, horizontal accordion item height reduces |
| ≤1199px | Tablet landscape | Content max-width: 768-900px, horizontal accordion collapses to vertical stack |
| ≤991px | Tablet | Mobile nav activates, hero H1: 56px, grids go single-column, card grids stack |
| ≤767px | Mobile landscape | H1: 48px, H2: 40px, content padding: 40px 24px, SVG gradient bridge → CSS radial gradient fallback |
| ≤544px | Mobile | H1: 40px, hero width: calc(100% - 48px), stat grid: 1 column |
| ≤425px | Small mobile | H1: 28px, nav buttons: min-width 120px |

**Key responsive behavior — gradient bridge fallback:**
On mobile (≤767px), SVG gradient bridge backgrounds are hidden (`display: none`) and replaced with a CSS radial gradient:

```css
background: radial-gradient(113.06% 100% at 50% -0.06%,
  var(--blue-900) 43.96%, var(--blue-700) 53.45%,
  var(--pink-400) 68.28%, var(--yellow-200) 76.58%,
  var(--gray-100) 83.7%);
```

---

## Diversity Constraints

Rules that prevent repetitive, AI-defaulting compositions.

### Layout Rotation Register

Before composing (Step 4.5 of the elevation protocol), build a composition plan — a table mapping each section or slide to a layout type. The plan must satisfy:

1. **No consecutive repetition:** No two adjacent sections/slides use the same layout pattern (e.g., two card grids in a row, two statement slides in a row).
2. **Minimum variety threshold:** For outputs of 10+ slides/sections, at least 6 different layout types. For 6-9, at least 4. For 3-5, at least 3.
3. **Surface balance:** Apply the 60-30-10 color ratio. For a 16-slide deck: ~10 dark slides, 4-5 light, 1-2 gradient.
4. **Visual weight distribution:** Mark each slide as high-weight (gradient, screenshot, multi-card) or low-weight (statement, bullets, divider). Alternate clusters of 2-3, don't group all high-weight together.

### Composition Profiles

When starting a composition, declare one of these profiles to guide structural decisions:

| Profile | Opening | Middle Pattern | Closing |
|---------|---------|----------------|---------|
| **Dramatic** | Statement + Stats | Screenshot-heavy, few cards | Statement + CTA |
| **Evidence-led** | Stats + Data | Cards + Screenshots alternating | Quote + CTA |
| **Story arc** | Statement | Split layouts + bullets building argument | Statement + CTA |
| **Demo-focused** | Statement | Screenshots dominate, light surfaces heavy | Cards + CTA |
| **Comparison** | Two-column | Cards + Stats + Two-column | Statement + CTA |

The design-director must declare which profile it is using and justify the choice based on content goals. This forces conscious layout selection rather than defaulting to the same pattern every time.
