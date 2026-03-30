# Technique Catalog

Visual moves indexed by purpose. Each entry names the technique, points to element(s) in the library, and explains when to use it vs alternatives.

---

## 1. Create a Stunning Section Background

**Element:** `grad-section`
**What it does:** Nested containers each applying the signature gradient create layered border frames. The Blue 900 > Blue 700 > Pink 400 > Yellow 200 > Gray 100 spectrum produces concentric color rings that glow inward. Each nesting level adds padding (~36px), so the gradient appears as a series of borders narrowing toward the content.
**When to use:** Title sections, transition moments, any section that needs to be a showstopper. The visual weight signals "this is the most important thing on the page."
**When NOT to use:** Mid-page for regular content sections. If the section is informational rather than dramatic, use a standard dark or light surface instead.
**Restraint rule:** ONE per page or deck. More than one dilutes the impact -- the technique works because it is rare.
**Mediums:** HTML (direct), Marp (direct as slide background), PPTX (title slide or divider slide background)

---

## 2. Close a Page or Deck Strong

**Element:** `cta-section`
**What it does:** Triple-nested gradient frames (Blue 900 34% > Blue 700 56% > Pink 400 70% > Yellow 200 84% > Gray 100 91%) with a content card inside. The concentric gradient borders create a visual crescendo that frames the final call-to-action. Innermost container is Gray 100 with an H2 heading and CTA button.
**When to use:** The final section of a page or the closing slide of a deck. This is the closer -- it creates visual finality and drives action.
**When NOT to use:** Never mid-page. Never as a general-purpose section wrapper. If the section is not the final CTA, use a standard dark or light surface.
**Restraint rule:** ONE per page or deck, and it must be the last section before the footer.
**Mediums:** HTML (direct), Marp (closing slide), PPTX (closing slide with gradient background)

---

## 3. Add Visual Depth to a Dark Surface

**Elements:** Dot-matrix wave pattern (from `hero-bg` / `background`) + radial gradient overlays with `mix-blend-mode: lighten`
**What it does:** The dot-matrix pattern adds subtle texture (a wave of tiny dots) to Blue 900 surfaces. Radial gradient overlays (using blue tones with lighten blend mode) create areas of brightness that make the surface feel three-dimensional rather than flat. Together they produce depth without competing with content.
**When to use:** Any Blue 900 section that feels flat or lifeless. Particularly effective on hero sections and icon-card dark sections where the content needs a richer backdrop.
**When NOT to use:** On light surfaces (the blending has no visible effect on Gray 100). On sections where simplicity is the point -- sometimes a clean Blue 900 surface is better than a textured one.
**Restraint rule:** None -- this is a subtle enhancement, not a focal technique. Apply wherever dark surfaces need life.
**Mediums:** HTML (direct with CSS background layers), Marp (background image layers), PPTX (background image export)

---

## 4. Present a Screenshot Professionally

**Elements:** Screenshot frame elements (from `visual-home`, `visual-platform`)
**What it does:** The screenshot sits inside a gradient-backed frame using the Blue 400 > Blue 700 linear gradient (242.78deg). The frame has padding (100px horizontal, 80px vertical), and the screenshot fills a white content area within. The gradient frame gives the screenshot visual context and elevation.
**When to use:** Any time a product screenshot, UI mockup, or interface image appears in the design. Screenshots must always be framed.
**When NOT to use:** Never show a raw screenshot floating on a white background. Never use this frame for non-screenshot images (photos, icons, illustrations).
**Restraint rule:** None -- every screenshot needs a frame. The frame treatment is the constant; the screenshot inside is swappable.
**Mediums:** HTML (direct), Marp (image within styled container), PPTX (screenshot placed on gradient-filled shape)

---

## 5. Differentiate Items Visually

**Elements:** `differentiation-visual-a`, `differentiation-visual-b`, `differentiation-visual-c`
**What it does:** Layered background treatments that sit behind content blocks. Each variant (A, B, C) provides a distinct visual identity while remaining part of the same family. The treatments use brand gradients and shapes to create visual separation without relying solely on layout spacing.
**When to use:** When presenting multiple content blocks that are structurally similar (same heading + body pattern) but need to feel distinct. Pricing tiers, product editions, service levels, comparison columns.
**When NOT to use:** When items are already differentiated by content type (e.g., a testimonial next to a stat block). When the section has fewer than 2 items -- differentiation requires contrast.
**Restraint rule:** Use A/B/C variants consistently within a section. Do not mix arbitrarily -- A for primary, B for secondary, C for tertiary.
**Mediums:** HTML (direct), Marp (background treatments per slide or per column), PPTX (shape fills behind content)

---

## 6. Show Data or Statistics Impressively

**Element:** `stat-block`
**What it does:** Large numeral rendered in brand blue (Blue 700) using a display size, with a label in body text (Manrope P4) beneath. The oversized number creates visual impact while the label provides context. Desktop and mobile variants handle responsive behavior.
**When to use:** Key metrics, performance numbers, survey results, ROI figures -- any time a number needs to be the hero of a section. Best in groups of 2-4 for visual rhythm.
**When NOT to use:** For numbers that do not carry weight on their own (e.g., "Step 1, Step 2"). For dense data tables -- stat blocks are for isolated hero numbers, not tabular data.
**Restraint rule:** 2-4 stat blocks per section maximum. More than 4 flattens the hierarchy -- nothing feels impressive when everything is big.
**Mediums:** HTML (direct), Marp (horizontal row of stats on one slide), PPTX (stat callouts with large number + label)

---

## 7. Present Features with Engagement

**Elements:** `product-carousel` (expanding cards) or `feature` / `product-features` (accordion with screenshot)
**What it does:** Two patterns depending on content structure:
- **Product Carousel:** Cards that expand on interaction -- collapsed state shows title, hover shows preview, active/expanded state shows full content. All features get equal visual weight.
- **Feature Accordion:** A primary feature with a live screenshot area, plus a vertical list of supporting features. Clicking a list item swaps the screenshot. One feature is always "active."
**When to use:** Carousel when features are equal-weight and each deserves the same visual real estate. Accordion when there is a primary feature to highlight with supporting details, or when features benefit from a live screenshot demonstration.
**When NOT to use:** For fewer than 3 features (too few cards for a carousel; too few items for an accordion). For features that do not have visual content to show -- use icon cards instead.
**Restraint rule:** One interactive feature section per page. Carousel OR accordion, never both on the same page.
**Mediums:** HTML (direct with hover/click interactions), Marp (build sequence: one feature per slide in sequence), PPTX (build sequence across slides)

---

## 8. Add a Testimonial or Quote

**Element:** `quote`
**What it does:** A styled quote block with the testimonial text, attribution (name, title, company), and optional photo. Desktop and mobile variants ensure the quote reads well at any width. Typography uses a larger body size (P2, 24px) for the quote text to set it apart from surrounding content.
**When to use:** Customer testimonials, analyst quotes, executive endorsements, internal leadership quotes. Any time a human voice adds credibility to the surrounding content.
**When NOT to use:** For pull-quotes from the page's own content (that is an editorial pattern, not a testimonial). For long-form quotes that would better work as a blockquote within body copy.
**Restraint rule:** 1-2 quotes per page. A single powerful quote is more credible than a wall of testimonials.
**Mediums:** HTML (direct), Marp (full-slide quote with large text), PPTX (centered quote slide)

---

## 9. Present Icon-Driven Content on Dark

**Element:** `icon-card-dark`
**What it does:** Card with a radial gradient background placed on a Blue 900 surface. Each card contains an icon (32px), title (Regesto H4), and description (Manrope P4). The radial gradient gives each card subtle depth against the dark surface. Laid out in a 3-column grid with 32px internal padding per card.
**When to use:** Capability lists, feature summaries, service categories -- any time 3-6 items need to be presented as a grid on a dark surface with icon-driven visual anchors.
**When NOT to use:** On light surfaces (use the light-surface card variant or plain spacing instead). For content without meaningful icons -- do not force generic icons.
**Restraint rule:** 3 or 6 cards (one or two rows of 3). Avoid 4 or 5 cards -- the 3-column grid creates awkward gaps.
**Mediums:** HTML (direct), Marp (horizontal 3-card layout on dark slide), PPTX (3-card horizontal layout on dark background)

---

## 10. Present Value Propositions

**Element:** `value-visual`
**What it does:** A box design pattern where the frame and visual treatment are the element, and the content inside is swappable. The treatment gives the value proposition visual presence beyond just text on a page -- the box signals "this is a distinct, self-contained promise."
**When to use:** Core value propositions, key benefits, differentiators. When the content represents a promise or outcome that needs to stand apart from descriptive text.
**When NOT to use:** For features (use feature cards or the accordion instead). For items that are descriptive rather than aspirational -- value visuals carry an implicit "here is what you get" weight.
**Restraint rule:** 3-4 per page maximum. Each value proposition should be substantial enough to merit its own visual container.
**Mediums:** HTML (direct), Marp (one value per slide or 2-3 per slide in grid), PPTX (value prop boxes on slide)

---

## 11. Build Trust with Credentials

**Element:** Icon & Text grid layout
**What it does:** A 2-row x 3-column grid with 60px column gap and 32px row gap. Each cell contains an icon (64px square), a title in Regesto Grotesk H4 (20px, Gray 150 on dark), and a description in Manrope P4 (16px, Blue 300 on dark). The grid format presents credentials, certifications, partnerships, or trust signals in a scannable, authoritative layout.
**When to use:** Security certifications, compliance badges, technology partnerships, integration ecosystems, awards. Any time 4-6 credentials need to be displayed as a trust section.
**When NOT to use:** For fewer than 4 items (looks sparse). For items that need long descriptions -- the P4 description should be 1-2 lines maximum.
**Restraint rule:** One trust grid per page. Place after the main content and before the CTA section -- trust signals support the close.
**Mediums:** HTML (direct), Marp (full-slide grid), PPTX (6-cell grid layout on one slide)

---

## 12. Create a Section Header

**Element:** Split layout (section intro pattern)
**What it does:** H2 heading on the left (max-width 500px) with P3 body text on the right (max-width 450-500px). Both are top-aligned within the row. This split creates visual hierarchy -- the heading draws the eye, and the supporting text provides context without competing for attention.
**When to use:** The opening of any content section that needs an introduction. The standard pattern before card grids, feature sections, or screenshot showcases.
**When NOT to use:** For sections that do not need an introduction (e.g., a standalone quote or stat block). For sections where a centered heading is more appropriate (hero sections, CTA sections).
**Restraint rule:** None -- this is a structural pattern, not a decorative one. Use as many section headers as the page needs.
**Mediums:** HTML (direct), Marp (headline-left / text-right slide layout), PPTX (two-column text slide with heading left and body right)

---

## 13. Adapt a Web Section to a Slide

**Element:** PPTX mapping rules (not a single library element -- a set of translation principles)
**What it does:** Maps web sections to slide equivalents so that the same design language works across HTML and presentation formats. The core rule: one web section = one slide. Specific mappings:

| Web Section | Slide Equivalent |
|---|---|
| Hero section | Title slide (gradient background) |
| CTA section | Closing slide (gradient background) |
| Icon card grid (3 cards) | Horizontal 3-card layout on one slide |
| Feature accordion | Build sequence (one feature per slide) |
| Split layout (H2 + P3) | Headline-left / text-right slide |
| Screenshot frame | Full-bleed screenshot on gradient background |
| Stat blocks | Stat row on one slide |
| Quote block | Centered quote slide |

**When to use:** Any time a web page design needs a presentation counterpart, or when building a deck that should feel like the website.
**When NOT to use:** When creating a presentation from scratch that has no web counterpart -- in that case, use the slide patterns directly from the technique catalog entries above.
**Restraint rule:** Do not cram multiple web sections into one slide. The "one section = one slide" rule exists to prevent information overload. If a web section is too dense for one slide, split it into multiple slides.
**Mediums:** PPTX (primary), Marp (direct translation)

---

### 14. Add a Gradient Accent Border

**When to use:** Visual separation between sections, above stat blocks, above dropdown menus. Creates a signature brand divider that implies elevation.

**Element:** Accent-700 gradient (`--gradient-accent-700`), applied as a `::before` pseudo-element.

**Construction:**
```css
.container { position: relative; }
.container::before {
  content: "";
  position: absolute;
  top: -4px;
  left: 0;
  width: 100%;
  height: 4px;
  background: var(--gradient-accent-700);
}
```

**Surface:** Works on both dark and light surfaces. The gradient runs 270deg: Yellow → Pink → Blue (warm to cool, left to right).

**See also:** `construction-techniques.md` Section 6 (Gradient Bridge) for the full nested-rectangle version.

---

### 15. Create a Card-in-Environment Composition

**When to use:** CTA sections, hero callouts, key messaging sections where you want the content to feel embedded in the gradient environment rather than floating above it.

**Element:** Gradient bridge SVG (or CSS approximation) + content card with page-matching background.

**Construction:** The content card uses `background: var(--bg-light)` — the same color as the page. Placed inside a section with a gradient background (SVG or CSS), the gradient is visible only in the gap between the card edge and the section edge. The card appears "cut into" the gradient, not floating.

**Layout:**
- Section: `position: relative; overflow: hidden; background: var(--bg-light)`
- SVG background: `position: absolute; z-index: 1`
- Container: `position: relative; z-index: 4; max-width: 1440px`
- Content card: `background: var(--bg-light); padding: 64px 100px; max-width: 1152px`

**Surface:** The gradient environment is the accent; the card is the light surface.

---

### 16. Add Subtle Texture to a Card

**When to use:** Quote blocks, accordion items, value cards. Adds organic visual interest without competing with content.

**Element:** Mesh-grid SVG, dot-matrix SVG, or directional bar SVG. All are self-masking — the asset fades to transparent internally.

**Construction:**
```css
.card { position: relative; overflow: hidden; }
.card .texture {
  position: absolute;
  top: 0;
  right: 0;       /* anchor to the corner where the texture concentrates */
  z-index: 1;
  opacity: 0.7;   /* subtle: 0.7, featured: 1.0 */
  pointer-events: none;
}
.card .content { position: relative; z-index: 2; }
```

**Key principle:** The asset itself controls where it's visible (via gradient-to-transparent fills). CSS just says "anchor this corner." The texture does not cover the full card uniformly — it concentrates in one area and fades.

---

### 17. Build a Two-Part CTA Button

**When to use:** Primary calls to action that need directional energy. The arrow block creates visual momentum toward the action.

**Element:** `main-button-component` — two adjacent blocks (text + arrow), each with gradient backgrounds and hover overlays.

**Construction:** See `construction-techniques.md` Section 5 for full gradient formulas. Key properties:
- Text block: height 34px, padding 10px, Blue gradient, `z-index: 2`
- Arrow block: width 36px, height 34px, Blue gradient (different angle), `z-index: 1`
- Both: `border-radius: 0`, `margin-right: -1px` (eliminates gap)
- Hover: `::before` pseudo-elements on both blocks transition from `opacity: 0` to `opacity: 1`, revealing a warmer gradient (Blue→Pink on text, Blue→Pink→Yellow on arrow)

**Surface:** Works on both dark and light surfaces. On dark surfaces, ensure the button has sufficient contrast.
