# Presentation Design Guide

Rules and patterns specific to designing slide decks (Marp, PPTX). Read this file whenever the output medium is a presentation. This supplements — does not replace — the general design system files.

---

## How to Think Like a Presentation Designer

Before touching any tool, internalize these principles from the best presentation design thinkers (Duarte, Reynolds, and design school fundamentals). These are not optional — they are the difference between "slides with brand colors" and "a designed presentation."

### 1. Signal-to-Noise Ratio (Garr Reynolds)

Every element on a slide either supports the message (signal) or distracts from it (noise). Your job is to maximize signal and eliminate noise. Ask for every element: "Does this help the audience understand the point of THIS slide?" If not, remove it.

- A decorative gradient that creates mood = signal (it sets emotional tone)
- A decorative gradient that distracts from the data = noise
- A branded frame around a screenshot = signal (it makes the screenshot feel intentional)
- Three different visual treatments on one slide = noise (the audience doesn't know where to look)

### 2. One Idea Per Slide

Each slide communicates exactly ONE concept. If you find yourself thinking "this slide also needs to mention..." — that's a second slide. The audience processes one idea at a time. Cramming two ideas into one slide means neither lands.

### 3. The Audience is the Hero (Nancy Duarte)

The presentation exists to move the audience from their current state to a new understanding. Every slide should advance that journey. The structure is: establish what IS → create tension about what's WRONG → reveal what COULD BE → show proof → call to action.

### 4. Gestalt Principles on Slides

These are fundamental laws of visual perception. Violating them makes slides feel "off" even if the audience can't explain why.

- **Proximity:** Elements that are close together are perceived as related. Group related text, separate unrelated content with space. A heading must be closer to its body text than to the previous section.
- **Alignment:** Everything must align to something. Left-align body text. Align card edges. Align stat block tops. Misalignment feels chaotic even at a subconscious level.
- **Repetition:** Consistent treatment across similar elements creates coherence. All stat blocks should look the same. All section dividers should share a pattern. Repetition builds the "design system" feeling.
- **Contrast:** The most important element should have the highest contrast. If everything is bold, nothing is bold. Create hierarchy through size, weight, and color contrast — not by making everything big.

### 5. Restraint is the Design Choice

The temptation is to add more: more gradients, more colors, more visual elements. Professional designers remove. Every slide should feel like you took things away until only the essential remains. One hero gradient per deck. One accent color moment per slide. One focal point per composition.

### 6. Visual Rhythm Across the Deck

A deck is not 16 independent slides — it's a visual sequence. Each slide should feel like the next frame in a story. This means:
- Consistent typography and spacing creates the baseline rhythm
- Varying layouts prevents monotony (but within the same visual family)
- Surface color changes (dark → light) create the "breathing" pattern
- The title and closing slides bookend with the strongest visual treatment
- The middle slides build intensity gradually, not randomly

### 7. Content Drives Layout, Not the Other Way Around

Never choose a layout first and force content into it. Read the content, understand its structure (is it 3 parallel items? a comparison? a bold claim? data?), then select the layout that serves that structure. A slide with 3 bullet points is a card grid. A slide with one bold statement is a typographic statement. A slide with a screenshot is a split layout.

---

## The 60-30-10 Color Rule for Slides

Apply this ratio to the ENTIRE DECK, not individual slides:

- **60% — Dominant surface:** This is your primary background. For Swimm, use Blue 900 (`#1A2761`) as the dominant. Most slides should have a dark navy base.
- **30% — Secondary surface:** Light slides for breathing room. Use Gray 100 (`#F3F3FB`). Roughly 1 in 3 slides should be light.
- **10% — Accent:** The signature gradient spectrum (Blue → Pink → Yellow) and Blue 700 (`#325BFF`) as interactive accent. Used on title slide, closing slide, badges, and CTA buttons. (Stat numerals use Blue 300 or Blue 900 from the primary palette, not warm accent colors.) Never more than 2-3 slides in a 16-slide deck should feature the full gradient treatment.

**What this means in practice for a 16-slide deck:**
- ~10 dark slides (Blue 900)
- ~4-5 light slides (Gray 100)
- ~1-2 gradient/accent slides (title + closing)

**Common mistake:** Alternating dark/light 50/50 creates a strobe effect. The dark surface should DOMINATE, with light slides providing strategic breathing room — not equal airtime.

---

## Slide Type Catalog

Every slide in a deck must be one of these types. Each type has a specific layout, visual treatment, and purpose.

### 1. Title Slide
- **Purpose:** First impression. Sets tone and energy.
- **Layout:** Centered content card on gradient background (grad-section pattern)
- **Elements:** H1 title, P3 subtitle, speaker names in Label style
- **Surface:** Gradient (the ONE hero gradient in the deck)
- **Swimm pattern:** Gradient ring frames from `grad-section` element

### 2. Section Divider
- **Purpose:** Signals a topic shift. Gives audience a mental reset.
- **Layout:** Centered H2 heading with generous vertical padding. Add a visual element — never bare text.
- **Elements:** H2 heading, optional P3 subheading, MUST have a depth treatment (radial overlay, warm gradient pseudo-element, or background texture)
- **Surface:** Dark with depth
- **Swimm pattern:** In Marp, use the `dark-divider` slide class — it provides automatic depth (strong center SVG radial) plus a hero wave gradient bar at the bottom. No manual depth construction needed. For HTML/web output, use `hero-background` solid gradient columns or CTA gradient at low opacity as background treatment.

### 3. Statement Slide
- **Purpose:** A bold claim or quote that should land with impact.
- **Layout:** Large typographic statement, left-aligned or centered. Text should fill at least 50% of the slide width.
- **Elements:** H1 or Special (60px) for the statement text, P3 for supporting context
- **Surface:** Dark with depth — the statement needs dramatic framing
- **Swimm pattern:** `hero-background` solid gradient columns + warm gradient overlay. Consider highlighting a key word in Pink 400.

### 4. Data / Stats Slide
- **Purpose:** Present metrics, benchmarks, or key numbers.
- **Layout:** Horizontal row of stat blocks (2-4 per slide). Each stat is a card with large numeral + label.
- **Elements:** `stat-block` element. Numbers in Manrope (`var(--text-font)`) at 60px, weight 300. Labels in P4. Note: stat numbers use the body font (Manrope), not the heading font (Regesto Grotesk).
- **Surface:** Dark preferred (stat numerals pop against dark). Light acceptable.
- **Swimm pattern:** `stat-block` with radial gradient per card on dark, subtle radial on light

### 5. Content + Screenshot Slide
- **Purpose:** Show the product alongside explanation.
- **Layout:** Split — text on one side (40%), screenshot in gradient frame on the other (60%). OR full-width screenshot with heading above/below.
- **Elements:** `screenshot-platform-map` or `screenshot-home-flow` frame element. H2 heading, P4 body.
- **Surface:** Light preferred (screenshots need contrast)
- **Swimm pattern:** Blue 400→700 gradient frame (242.78deg) with white inner card

### 6. Multi-Image Slide
- **Purpose:** Show multiple screenshots or visuals together (e.g., before/after, feature comparison).
- **Layout:** Grid or row of framed images. If source has 3 images, show ALL 3 — do not reduce to 1. Use equal-width columns.
- **Elements:** Multiple `screenshot-home-flow` frames side by side, scaled to fit. H2 heading above.
- **Surface:** Light
- **Rule:** NEVER convert a multi-image slide to a single-image slide. If the source has 3 images, the output has 3 image placeholders. Reduce frame size to fit, not image count.

### 7. Card Grid Slide
- **Purpose:** Present 2-4 parallel items (features, pillars, benefits).
- **Layout:** Horizontal row of equal-width cards. 2-4 cards per row.
- **Elements:** `icon-card-dark` for dark surface, `value-visual` for light surface. Each card: icon/badge + H3 title + P4 description. Cards on light surfaces use the Light-100 radial gradient (`--gradient-light-100`) as their background, not flat fills.
- **Surface:** Dark preferred for icon cards, light for value visuals
- **Swimm pattern:** Radial gradient per card on dark. Badges for labels (NEW, PROVEN).

### 8. List / Bullet Slide
- **Purpose:** Present a set of points, features, or items.
- **Layout:** Left-aligned heading + bulleted items below. Or icon-text grid (2-3 columns) for more visual weight.
- **Elements:** `icon-text` element for icon+text pairs. Or simple styled bullets.
- **Surface:** Either. Use `icon-text` grid on dark for more visual interest.
- **Swimm pattern:** 64px icons with H4 title + P4 description per item

### 9. Two-Column / Comparison Slide
- **Purpose:** Compare two concepts, show before/after, or present two parallel ideas.
- **Layout:** Two equal columns with clear visual separation. Can use numbered sections (1, 2) or labeled columns.
- **Elements:** Feature tags/chips for categorization, H3 titles per column, P4 descriptions
- **Surface:** Either
- **Swimm pattern:** Use `feature` element active/default states, or `accordion-block-1` pattern

### 10. Closing / CTA Slide
- **Purpose:** Final impression. Call to action.
- **Layout:** Centered content card on CTA bridge gradient (triple-nested gradient frames)
- **Elements:** `cta-section` element. H2 heading + optional P3 subtitle + CTA button.
- **Surface:** Gradient (the CTA bridge — reserved for the final slide only)
- **Swimm pattern:** Triple-nested gradient with exact stops: 34.286%, 56.023%, 70.306%, 83.838%, 91.355%

### 11. Accordion / Feature Reveal Slide

**When to use:** Presenting multi-item content where each item has a title, description, and optional visual. Vertical or horizontal accordion patterns from the website.

**Construction:** On a dark surface, start with all items in their closed state (title + small icon visible). One item is active (expanded) — it shows the full description and a larger visual or animation. The active item uses a dark gradient background (`linear-gradient(252deg, Blue-800 → Blue-900)`), while closed items use Light-100 gradient backgrounds.

**Layout variants:**
- **Vertical:** Title occupies column 1, accordion items span columns 2-3. Active item has dark background, closed items have light backgrounds with small icons at right.
- **Horizontal:** Items arranged in a row. Closed items are narrow (220px). Active item expands wide (690px) with a visual panel.

**Text treatment:** Active item title: Gray-50, Regesto Grotesk 20px, weight 400. Description: Blue-300, Manrope 16px, weight 400. Closed item title: Blue-900, Regesto Grotesk 20px.

---

## Slide Sequencing Rules

### Narrative Arc
A presentation follows an emotional arc. The slide types should support it:

1. **Open strong** — Title slide (gradient) → Statement or problem setup
2. **Build tension** — Data slides, problem slides, evidence
3. **Reveal solution** — Product overview (card grid), feature details
4. **Show proof** — Screenshots, demos, comparisons
5. **Close strong** — Vision statement → CTA/closing slide (gradient)

### Surface Rhythm for Presentations
Unlike web pages (which alternate dark/light roughly equally), presentations should be DARK-DOMINANT:

- Dark is the default surface. It creates focus and drama.
- Light slides are strategic interruptions for breathing room and screenshot visibility.
- Gradient slides bookend the deck (title + closing).

**Pattern for a 16-slide deck:**
```
Gradient → Dark → Light → Dark → Dark → Dark → Light → Dark → Light → Dark → Light → Dark → Dark → Dark → Light → Gradient
```

Note: 3 consecutive dark slides are acceptable in presentations (unlike web where max is 2) because each slide is a discrete moment. The key is that each dark slide has a DIFFERENT visual treatment.

### Transition Rules
- After a section divider, the next slide should be a different surface (divider is dark → next is light, or vice versa)
- After 3 consecutive dark slides, insert a light slide for breathing room
- Never place two gradient slides adjacent to each other
- Screenshot slides are almost always light (screenshots need contrast)

### Layout Rotation Register

Before composing a deck, build a composition plan mapping each slide to a type class. Verify diversity constraints:
- No two adjacent slides use the same type class
- Minimum variety: 10+ slides need 6+ types, 6-9 need 4+, 3-5 need 3+
- Surface balance: ~60% dark, ~30% light, ~10% gradient
- Visual weight alternation: high-weight and low-weight slides alternate in clusters of 2-3

Declare a composition profile (Dramatic, Evidence-led, Story arc, Demo-focused, or Comparison) from `composition-rules.md` and justify the choice based on content goals.

---

## Layout Patterns

### Split Layout (50/50 or 40/60)
```
┌─────────────────┬───────────────────┐
│                 │                   │
│   Heading       │   Screenshot      │
│   Body text     │   in gradient     │
│                 │   frame           │
│                 │                   │
└─────────────────┴───────────────────┘
```
**When:** Content + screenshot, concept + visual, text + image

### Card Grid (2-4 columns)
```
┌──────────┬──────────┬──────────┐
│  Card 1  │  Card 2  │  Card 3  │
│  Icon    │  Icon    │  Icon    │
│  Title   │  Title   │  Title   │
│  Desc    │  Desc    │  Desc    │
└──────────┴──────────┴──────────┘
```
**When:** Parallel items (features, pillars, benefits)

### Multi-Image Grid
```
┌──────────┬──────────┬──────────┐
│  Frame 1 │  Frame 2 │  Frame 3 │
│  [img]   │  [img]   │  [img]   │
│  Label   │  Label   │  Label   │
└──────────┴──────────┴──────────┘
```
**When:** Multiple screenshots. PRESERVE the count from source. If source has 3 images → 3 frames.

### Centered Statement
```
┌─────────────────────────────────────┐
│                                     │
│         "Bold statement             │
│          goes here"                 │
│                                     │
│   Supporting context in smaller     │
│   text below the statement.         │
│                                     │
└─────────────────────────────────────┘
```
**When:** Quotes, bold claims, section dividers. Must have depth treatment on background.

### Full-Width Screenshot
```
┌─────────────────────────────────────┐
│   Heading                           │
│  ┌─────────────────────────────┐    │
│  │                             │    │
│  │   [Screenshot in frame]     │    │
│  │                             │    │
│  └─────────────────────────────┘    │
│   Caption or label                  │
└─────────────────────────────────────┘
```
**When:** Single important screenshot that needs full attention

### Stat Row
```
┌─────────────────────────────────────┐
│   Heading                           │
│  ┌──────┐  ┌──────┐  ┌──────┐      │
│  │ 35%  │  │ 70%  │  │ 42%  │      │
│  │cover │  │accur │  │vari  │      │
│  └──────┘  └──────┘  └──────┘      │
└─────────────────────────────────────┘
```
**When:** Key metrics, benchmark results, data highlights

---

## Content Preservation for Presentations

When converting source content to slides:

1. **Preserve all text verbatim.** Do not rewrite, summarize, or "improve" slide copy.
2. **Preserve image count.** If a source slide has 3 images, the output has 3 image placeholders. Never reduce image count to simplify layout.
3. **Preserve information structure.** If source has 3 bullet points, output has 3 items (as bullets, cards, or icon-text pairs — but always 3).
4. **Preserve the narrative order.** Slides should follow the same sequence as the source.
5. **Map source content to slide types.** Each source slide maps to one slide type from the catalog. Choose the type that best fits the content structure.

---

## Marp-Specific Technical Notes

### Class Application
Use `<!-- _class: classname -->` after `---` separator. Never use `<section>` tags.

### Dark Slide Depth (Required)
Every dark slide must have depth. The Marp theme handles this automatically — every `dark-*` class has `::before` and `::after` pseudo-elements with exact SVG radial gradients (using Figma transform matrices, embedded as data-URIs). These are the same SVG-based gradients used on the web, not CSS approximations. You do not need to manually add depth to Marp slides.

For custom depth beyond what the theme provides, embed inline SVG radial gradients rather than inventing new CSS radial-gradient formulas. No `box-shadow` is used anywhere in the system.

### Font Loading
```css
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;700&display=swap');

@font-face {
  font-family: 'Regesto Grotesk';
  src: local('Regesto Grotesk'), local('Roc Grotesk');
  font-weight: 300;
}
@font-face {
  font-family: 'Regesto Grotesk';
  src: local('Regesto Grotesk'), local('Roc Grotesk');
  font-weight: 400;
}
```

### Gradient Frame for Screenshots
```css
.screenshot-frame {
  background: linear-gradient(242.78deg, var(--blue-400) 24.153%, var(--blue-700) 60.201%);
  /* No border-radius — sharp corners per design system */
  padding: 8px;
  border-left: 8px solid var(--blue-800);
}
.screenshot-frame__inner {
  background: white;
  /* No border-radius — sharp corners */
  width: 100%;
  height: 100%;
}
```

### Projection Typography
All body text minimum 20px. Headings: H1 60px, H2 42px, H3 26px, H4 20px. No custom sizes.
