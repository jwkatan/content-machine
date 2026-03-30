# AI Pattern Blocklist

15 design patterns that LLMs default to, with brand-correct alternatives. Used by both the design-director (avoidance during creation) and the design-reviewer (detection during evaluation).

Referenced design system files: `tokens.css`, `design-philosophy.md`, `composition-rules.md`, `presentation-design.md`, `marp-theme.css`, element library HTML files.

---

## 1. Centered-Everything Default

**What it looks like:** `text-align: center` on headings, paragraphs, and containers throughout the composition. Every line of text sits on a centered axis.

**Why it reveals AI generation:** Centering is the lowest-risk layout choice — it avoids alignment decisions entirely. LLMs default to it because it produces visually "safe" output without requiring spatial reasoning about grid placement.

**Brand-correct alternative:** Left-aligned text with purposeful grid placement. Use the split layout pattern from composition-rules.md (H2 left, P3 right, both `align-items: flex-start`). Centering is reserved for three specific contexts only: `title-gradient` slides, `closing-gradient` slides, and `dark-statement` slides. All other slide types and page sections use left-aligned text.

**Detection method:** Count `text-align: center` declarations across the output. If more than 30% of text elements are centered, flag. Check that centered text appears only inside `title-gradient`, `closing-gradient`, `dark-statement`, or CTA bridge content areas.

---

## 2. Symmetric Card Grid on Every Section

**What it looks like:** Three equal-width cards in a `repeat(3, 1fr)` grid on every section or slide, regardless of whether the content is three parallel items, a single claim, a data point, or a comparison.

**Why it reveals AI generation:** 3-card grids fill space symmetrically and work with any content length. LLMs reach for them because they avoid the harder problem of matching layout to content structure.

**Brand-correct alternative:** Content drives layout (presentation-design.md principle 7). A bold claim uses `dark-statement`. A single metric uses `stat-block`. A feature comparison uses `dark-twocol` or `dark-split`. A process uses `dark-flow`. Card grids are correct only when the content is genuinely 2-4 parallel items of equal weight.

**Detection method:** Count card-grid / card-row occurrences. If more than 40% of slides or sections use a card grid layout, flag. Verify each card grid contains genuinely parallel content.

---

## 3. Uniform Visual Rhythm

**What it looks like:** Every section follows the same structure: heading, paragraph, visual element. No variation in density, layout type, or visual weight across sections.

**Why it reveals AI generation:** LLMs generate sequentially and apply the same template to each section. They lack the global awareness to plan rhythm variation across a full composition.

**Brand-correct alternative:** Follow the narrative arc from presentation-design.md and the 60-30-10 surface rule. Vary slide types: statement, data, screenshot, cards, split, divider. No two consecutive slides should use the same class. Surface alternation (dark-dominant with strategic light breaks) creates the breathing pattern.

**Detection method:** List the slide type class or section layout for each section in order. Flag if any two consecutive entries are identical. Flag if fewer than 3 distinct layout types appear in a composition with 6+ sections.

---

## 4. Decorative-Only Gradients

**What it looks like:** `linear-gradient` or `radial-gradient` applied to card borders, button backgrounds, heading text, and section backgrounds throughout the composition. Multiple gradient sections competing for attention.

**Why it reveals AI generation:** LLMs treat gradients as a universal "polish" layer. They apply them anywhere the output feels visually sparse, without understanding that gradients in this system have specific structural roles.

**Brand-correct alternative:** One hero gradient section per composition (design-philosophy.md restraint principle). Gradients appear only via defined element library patterns: `grad-section` (title), `cta-section` (closing), `--gradient-blue` (screenshot frames), and card radials on dark surfaces. The CTA bridge gradient stops are exact: 34.286%, 56.023%, 70.306%, 83.838%, 91.355%. Do not invent new gradient applications.

**Detection method:** Count unique gradient declarations. Cross-reference each against the element library's canonical set. Any gradient not traceable to a specific element library pattern is improvised and should be flagged.

---

## 5. Flat Dark Slides

**What it looks like:** `background-color: var(--blue-900)` (or `#1A2761`) with text placed directly on it. No pseudo-elements, no SVG radials, no dot-grid pattern. A flat rectangle of navy with white text.

**Why it reveals AI generation:** Adding depth layers requires multi-step CSS composition (pseudo-elements, blend modes, SVG). LLMs take the shortest path: set the background color and move on.

**Brand-correct alternative:** Every dark surface must include at least one depth layer. The marp-theme.css `dark-*` classes provide this automatically via `::before` and `::after` pseudo-elements. For HTML, apply SVG radial overlays from the element library, `background-mesh` dot-grid patterns, or blend-mode layers (`mix-blend-mode: lighten` for glow, `multiply` for fades, `screen` for warm transitions).

**Detection method:** For every dark-surface section or slide, verify at least one depth treatment exists: a `::before`/`::after` with gradient or pattern, an inline SVG radial, or a dot-grid overlay. Bare `background-color` with no depth layer is a failure.

---

## 6. Cookie-Cutter Spacing

**What it looks like:** The same `padding` and `gap` value (often `24px` or `32px`) applied uniformly to every element — cards, sections, grids, text stacks. All spacing identical.

**Why it reveals AI generation:** LLMs pick one "reasonable" spacing value and repeat it, avoiding the cognitive load of context-specific spacing decisions.

**Brand-correct alternative:** Follow element-specific spacing from tokens.css and composition-rules.md. Cards: 32px padding (`--card-pad`), 24px icon-to-text gap (`--card-icon-gap`), 12px text stack gap (`--card-text-gap`). Sections: 100px vertical padding (`--section-pad-v`). CTA bridge nesting: 36px per level. Icon-text grids: 60px column gap, 32px row gap. The system uses intentional off-grid values (36px, 12px, 10px) that create visual tension.

**Detection method:** Extract all `gap`, `padding`, and `margin` values. If all values are identical or drawn from fewer than 3 distinct values, flag. Check that card internals use the 32/24/12 trio, not a single repeated value.

---

## 7. Decorative Elements Without Purpose

**What it looks like:** Shapes, icons, dividers, abstract SVGs, or gradient blobs added to slides or sections that serve no compositional function. Elements appear because the space "felt empty."

**Why it reveals AI generation:** LLMs add elements to avoid producing output that looks "incomplete." They cannot evaluate whether an element supports the message because they lack visual judgment.

**Brand-correct alternative:** Signal-to-noise ratio principle from presentation-design.md. Every element either supports the message (signal) or distracts from it (noise). Depth treatments (radials, dot-grids) are signal when they create mood. Random decorative shapes are noise. When in doubt, remove — the strongest Swimm compositions are the ones where every remaining element earns its place.

**Detection method:** For each non-text, non-image element, answer: "Does this help the audience understand THIS slide's point?" If the element could be removed without changing comprehension or emotional tone, it is noise. Flag it.

---

## 8. Predictable Accent Placement

**What it looks like:** Blue 700 (`#325BFF`) applied formulaically to every heading, every button, and the first word of every paragraph. Pink 400 and Yellow 200 used as standalone text colors or flat card backgrounds.

**Why it reveals AI generation:** LLMs apply accent colors by rule ("make headings the accent color") rather than by compositional judgment. They also extract warm palette colors and use them independently, missing that Pink 400 and Yellow 200 are gradient transition bands.

**Brand-correct alternative:** Blue 700 is for primary action buttons and selective emphasis, not every heading. Headings on dark surfaces use Gray 50 (`--text-heading-dark`). Body text on dark uses Blue 300 (`--text-body-dark`). Pink 400 and Yellow 200 exist only as transition stops within the signature gradient spectrum — they never appear as flat fills, standalone text colors, or card backgrounds.

**Detection method:** Check that Pink 400 (`#E99DB1`) and Yellow 200 (`#FFDFBB`) appear only inside `linear-gradient` or `radial-gradient` stop lists, never as `color`, `background-color`, or `border-color` values. Verify Blue 700 is not applied to more than 2-3 non-button elements per composition.

---

## 9. Rounded Corners

**What it looks like:** `border-radius` on cards, containers, frames, image wrappers, and buttons. Values typically 8px, 12px, or 16px — borrowed from Material Design or Tailwind defaults.

**Why it reveals AI generation:** Every major CSS framework defaults to rounded corners. LLMs absorb this from training data and apply `border-radius` reflexively to anything that looks like a card or container.

**Brand-correct alternative:** Zero `border-radius` on ALL cards, frames, containers, and buttons. Sharp corners are the brand's geometric signature. Composition-rules.md explicitly comments `/* No border-radius — cards use sharp corners */` on every card, frame, and screenshot container. The only exception is the CTA button inside the CTA bridge (8px radius per composition-rules.md).

**Detection method:** Grep for `border-radius` in the output. Any occurrence outside of the CTA bridge button is a failure. Zero tolerance.

---

## 10. Box-Shadow Depth

**What it looks like:** `box-shadow: 0 4px 12px rgba(0,0,0,0.1)` or similar elevation shadows on cards, containers, or floating elements.

**Why it reveals AI generation:** Box-shadow is the universal LLM depth mechanism. Every CSS framework uses it. LLMs have no awareness that this design system explicitly forbids it.

**Brand-correct alternative:** Depth is achieved through SVG radial gradients with transform matrices, CSS dot-grid patterns from `background-mesh`, opacity layering, and blend modes (`mix-blend-mode: lighten`, `multiply`, `screen`). A card on a gradient surface on a dark background creates three visual planes from simple parts — no shadows needed. Design-philosophy.md lists box-shadows as an explicit anti-pattern.

**Detection method:** Grep for `box-shadow` in the output. Any occurrence is a failure. Zero tolerance.

---

## 11. Heading-Paragraph-Heading-Paragraph Monotony

**What it looks like:** Every section or slide follows the identical structure: H2 heading, one paragraph of body text, optional image. No stat blocks, no split intros, no icon grids, no quote treatments.

**Why it reveals AI generation:** Heading-paragraph is the most common HTML pattern in training data. LLMs generate the most statistically probable structure for every content block, producing uniform output regardless of content type.

**Brand-correct alternative:** Vary structures per content type. A section intro uses the split layout (heading left, body right). Key metrics use `stat-block` rows. Feature lists use icon-text grids or accordion patterns. Bold claims use `dark-statement` (large typography, no body paragraph). Comparisons use two-column layouts. The slide type catalog in presentation-design.md maps 10 distinct content types to specific layouts.

**Detection method:** In multi-section compositions (6+ sections), count distinct structural patterns. If fewer than 3 different patterns appear, flag. Check that stat content uses stat blocks, not heading-paragraph pairs.

---

## 12. Empty White Space Masking Empty Design

**What it looks like:** Enormous margins and padding creating the illusion of minimalist design. Content occupies a small centered rectangle surrounded by untreated space. The canvas is technically "full" but visually empty.

**Why it reveals AI generation:** LLMs produce content in a small logical block and surround it with spacing. They lack the ability to assess whether the full canvas has been addressed — they treat layout as a text-centering problem, not a spatial composition problem.

**Brand-correct alternative:** Fill the canvas. Use depth treatments (gradient overlays, dot-grid patterns) on unused areas. The theme's slide type classes use `justify-content: center` to vertically center content, but card rows, stat rows, and split layouts should use the full available width. Every surface has structure — even "empty" space should carry a subtle gradient or faint dot pattern (design-philosophy.md).

**Detection method:** Visual inspection: does content occupy at least 40% of the canvas area? For slides, verify that card rows span the full content width and that backgrounds include depth treatments rather than flat color with large empty margins.

---

## 13. Identical Typography Treatment

**What it looks like:** All headings at the same size (often 32px or 36px). All body text at the same weight. No variation in the type scale across the composition. Everything reads at the same visual level.

**Why it reveals AI generation:** LLMs pick one heading size and apply it everywhere. They don't model typographic hierarchy as a system — they model it as "headings are bigger than body text."

**Brand-correct alternative:** Use the full type scale from tokens.css. H1: 60px (title/closing only). H2: 42px (section headings). H3: 26px (card titles, subsection headings). H4: 20px (small headings, feature item titles). H5: 16px (labels). Body uses P1-P4 (18px, 24px, 20px, 16px). Weight variation: 300 for data numerals and large body text, 400 for standard text, 500 for button labels. At least 3 distinct heading sizes should appear in any multi-section composition.

**Detection method:** Extract all `font-size` values applied to headings. If fewer than 3 distinct sizes appear in a composition with 6+ sections, flag. Verify H1 appears only on title and closing slides.

---

## 14. Monochromatic Blue Wash

**What it looks like:** Blue 700 or Blue 900 applied to backgrounds, headings, body text, borders, and accents simultaneously. The entire composition reads as a single blue tone with no surface differentiation.

**Why it reveals AI generation:** Blue is the primary brand color, so LLMs oversample it. They apply the same blue to every role (background, text, accent) without understanding that each context requires a different shade with a specific semantic purpose.

**Brand-correct alternative:** Apply the 60-30-10 rule. Blue 900 is the 60% dominant surface (dark backgrounds). Gray 100 is the 30% secondary surface (light sections). The gradient spectrum (Blue 700 through Pink 400 to Yellow 200) is the 10% accent. Within dark surfaces: headings use Gray 50/Gray 150 (`--text-heading-dark`), body text uses Blue 300 (`--text-body-dark`), not Blue 700. Within light surfaces: headings use Blue 900 (`--text-heading-light`), body text uses Gray 500 (`--text-body-light`). Grays are always blue-tinted (the Gray palette runs `#415992` to `#FDFCFE`), never pure gray.

**Detection method:** Check semantic color application per surface type. On dark surfaces, verify headings are Gray 50 (not Blue 700) and body is Blue 300 (not Blue 900). On light surfaces, verify body is Gray 500 (not Blue 700). Flag any use of pure grays (`#808080`, `#CCCCCC`, `#333333`).

---

## 15. Improvised CSS

**What it looks like:** New CSS properties, gradient formulas, or spacing values that are plausible but do not match any element in the design system. Custom `radial-gradient()` with invented stop percentages. Gradient directions that approximate but don't match the canonical values (e.g., `240deg` instead of `242.78deg`).

**Why it reveals AI generation:** LLMs generate CSS by statistical prediction, producing values that look reasonable but are not copied from the source. They approximate rather than replicate, because they don't have a mechanism to "look up" exact values during generation.

**Brand-correct alternative:** Copy exact values from the element library HTML files and tokens.css. The CTA gradient uses stops at 34.286%, 56.023%, 70.306%, 83.838%, 91.355% — not rounded approximations. The screenshot frame gradient is `242.78deg`, not `240deg` or `245deg`. Card radials use `rgba(50, 91, 255, 0.15)` at top-left, not invented opacity values. Every CSS value must trace back to a canonical source.

**Detection method:** Diff generated gradient stop percentages, angles, color values, and spacing against canonical element library values. Flag any value that does not appear in tokens.css, composition-rules.md, or the element library HTML files. Rounded or approximate values (e.g., `35%` instead of `34.286%`) indicate improvisation.
