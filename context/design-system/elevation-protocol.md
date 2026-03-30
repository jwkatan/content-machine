# Elevation Protocol

The 10-step process the design-director follows for every visual output.

---

## Step 0: Verify Content

**What to do:** Before designing anything, inventory ALL text content from the source material. Copy every headline, bullet, statistic, product name, model name, technical claim, and call to action into a reference list. This is your canonical copy. It does not change unless the user changes it.

**Files to load:** The source content the user provided (blog post, brief, outline, raw copy, deck content).

**Output:** A complete text inventory: every piece of content that will appear in the final output, listed in order. This is your reference copy for the rest of the process.

**Complete when:** You have a flat list of every text string from the source. At the end of the process (before Step 9), diff your final output against this inventory. Any deviation must be intentional, reported, and justified. If you cannot justify a deviation, revert it.

---

## Step 1: Understand

**What to do:** Ask questions before designing. Do not open any files, do not sketch, do not pick colors. Just listen and ask.

**Questions to ask:**
- What is the purpose of this output?
- Who is the audience?
- What medium? (HTML, Marp, PPTX, one-off visual)
- What content exists already?
- Are there constraints (dimensions, platform, context where it will be viewed)?
- What does success look like?

**Files to load:** None. This is conversation.

**Output:** A clear understanding of purpose, audience, medium, and constraints.

**Complete when:** You can articulate the brief in one sentence. Example: "A 10-slide Marp deck for enterprise engineering leaders that positions Swimm as the understanding platform, using content from the launch blog post."

---

## Step 2: Build Functional

**What to do:** Get the content right first. Structure the information hierarchy: what comes first, what supports what, what is the takeaway. No styling, no colors, no fonts yet. Work in plain text or minimal markdown. This is the skeleton.

**Files to load:**
- The source content the user provided (blog post, brief, outline, raw copy)
- Nothing from `context/design-system/` yet

**Output:** A structured content outline with clear hierarchy: sections, headings, body text, calls to action, data points. Every piece of content has a role (hero, supporting, proof, closer).

**Complete when:** The information architecture is sound. Someone reading the plain outline would understand the argument, the flow, and the emphasis without seeing any design.

---

## Step 3: Apply Brand Foundation

**What to do:** Apply the typographic and color system. Assign heading levels (H1-H5) to each text element. Assign body styles (P1-P4). Set colors by surface. Apply the 8px spacing grid. This alone transforms generic content into branded content.

**Files to load:**
- `context/design-system/font-reference.md` — Type scale, weights, line heights, color pairings by surface
- `context/visual-guidelines.md` — Full color palette, gradient definitions
- `context/design-system/tokens.css` — CSS custom properties for colors, fonts, spacing

**Output:** Content with correct typographic assignments. Every heading uses Regesto Grotesk at the right size/weight. Every body block uses Manrope at the right size/weight. Colors follow the surface rules (Blue 900 headings on light, Gray 50 headings on dark). Spacing uses 8px multiples.

**Complete when:** If you rendered this with only typography, color, and spacing (no elements, no depth, no composition), it would already look unmistakably Swimm-branded and have clear visual hierarchy.

---

## Step 4: Select Elements

**What to do:** Consult the technique catalog. Based on what each section of the output needs to achieve, identify which elements from the library will deliver that effect. Browse YAML metadata files to find the right elements. Do NOT load HTML yet.

**Files to load:**
- `context/design-system/technique-catalog.md` — Maps goals ("create a stunning section background", "present a screenshot professionally") to specific elements
- Element YAML files in `context/design-system/elements/[element-name]/element.yaml` — Browse these for metadata: dimensions, variants, surface type, usage notes
- Do NOT load `element.html` files at this stage

**Output:** A selection list mapping each section of the output to a specific element. Example:
- Hero section: `grad-section` (1440px variant)
- Features section: `product-carousel` (expanding cards)
- Social proof: `quote-block` (desktop variant)
- Closer: `cta-section`

**Hard gate:** If no element in the library matches what you need, STOP and tell the user. Do not proceed with improvised design. Every visual choice must trace back to a specific element in `context/design-system/elements/`. If the library does not have what you need, say so explicitly — do not invent a substitute.

**Complete when:** Every section has an element assignment (or an explicit decision to use no element, relying only on typography and spacing). The selections are justified by the technique catalog, not by guessing.

---

## Step 4.5: Build Composition Plan

**What to do:** Before composing, create a composition plan — a table mapping every section or slide to a specific layout type class. This plan is a reviewable artifact that the design-reviewer will check for diversity and structural quality.

**Files to load:**
- `context/design-system/composition-rules.md` — Diversity constraints, composition profiles, layout rotation register
- `context/design-system/ai-pattern-blocklist.md` — 15 AI design patterns to consciously avoid
- `context/design-system/construction-techniques.md` — HOW to build surfaces, layer elements, and compose sections

**Steps:**
1. List every section/slide in order.
2. Assign each a layout type class (dark-statement, dark-cards, dark-stats, dark-split, light-screenshot, light-split, light-cards, light-bullets, etc.).
3. Declare a composition profile (Dramatic, Evidence-led, Story arc, Demo-focused, or Comparison) and justify the choice based on content goals.
4. Verify diversity constraints:
   - No two adjacent items use the same layout type
   - Minimum variety threshold met (10+ slides: 6+ types; 6-9: 4+; 3-5: 3+)
   - Surface balance follows the 60-30-10 rule (60% dark, 30% light, 10% gradient)
   - Visual weight alternates in clusters of 2-3 (high-weight: gradient, screenshot, multi-card; low-weight: statement, bullets, divider)
5. Review the plan against the ai-pattern-blocklist.md — does the plan avoid centered-everything, same-layout repetition, predictable card counts, flat dark slides?

**Output:** A composition plan table. Example:

| Slide | Type | Surface | Weight | Notes |
|-------|------|---------|--------|-------|
| 1 | title-gradient | gradient | high | CTA bridge + content card |
| 2 | dark-statement | dark | low | Bold claim, centered |
| 3 | light-cards | light | high | 4 value cards, Light-100 gradient |
| 4 | dark-stats | dark | medium | 3 stat blocks + quote |
| 5 | light-screenshot | light | high | Full-width product shot |
| 6 | dark-split | dark | medium | Text left + screenshot right |

**Complete when:** The plan passes all diversity constraints and the composition profile is declared. If constraints fail, adjust the plan before proceeding to Step 5.

---

## Step 5: Compose

**What to do:** Place the selected elements into a coherent composition following the composition rules. This is where section rhythm, section anatomy, split layouts, card grids, and spatial relationships come together. NOW load the HTML for the selected elements.

**Files to load:**
- `context/design-system/composition-rules.md` — Section rhythm (dark/light alternation), section anatomy (padding, max-widths), card grid patterns, split layout specs, PPTX adaptation rules
- `context/design-system/elements/[selected-element]/element.html` — HTML/CSS for ONLY the elements chosen in Step 4. Never bulk-load all elements.

**Output:** A composed layout where elements are placed in order, surfaces alternate correctly, sections have proper padding and max-widths, and the overall rhythm follows the composition rules. Content from Step 2 is placed into the element structures from Step 4.

**Complete when:** The composition has correct section rhythm (no more than 2 consecutive same-surface sections), proper section anatomy (100px vertical padding, 120px horizontal padding, 1200px content max-width), and each element is used in its intended context. For PPTX/Marp, one web section maps to approximately one slide.

---

## Step 5.5: Construction Audit

**What to do:** Before adding depth, verify every surface in the output follows the 3-layer construction model from `construction-techniques.md`. This is a mechanical check, not a creative pass.

**Files to load:**
- `context/design-system/construction-techniques.md` — The 3-layer model, light card construction, dark surface depth requirements

**Checklist:**
- [ ] Every card on a light surface has `--gradient-light-100` radial gradient background (not flat Gray-100)
- [ ] Gradient origins are asymmetric (~33% from left, 0% from top) — not centered (50% 50%)
- [ ] Every interactive element has a hover/state pseudo-element layer (`::before` or `::after` with `opacity: 0 → 1` transition)
- [ ] Content elements have `position: relative; z-index: 2` to sit above background and interactive layers
- [ ] No two consecutive sections use the same layout pattern (per the Step 4.5 composition plan)
- [ ] All CSS gradients match canonical values from `tokens.css` — no improvised gradient stops

**Output:** A pass/fail for each item. Fix failures immediately before proceeding to Step 6.

**Complete when:** Every surface passes the construction checklist. If any fails, fix before proceeding.

---

## Step 6: Add Depth

**What to do:** Apply the layer that makes the output feel hand-crafted, not template-based. This is the difference between "branded" and "elevated." Use restraint: one hero gradient, not gradients everywhere. One signature moment per section.

**Files to load:**
- The element HTML already loaded in Step 5 (gradient formulas, radial overlay code, dot-matrix patterns are embedded in the element code)
- `context/design-system/design-philosophy.md` — Guides the restraint principle: bold vs. restrained, one hero gradient per composition, depth through layering not quantity
- `context/design-system/construction-techniques.md` — Gradient bridge construction, texture positioning, dark surface depth techniques, the 3-layer model

**Output:** The composition from Step 5 with depth treatments applied:
- Gradient backgrounds where appropriate (one hero gradient, not everywhere)
- Radial overlays on dark cards (using the exact formula from the element code)
- Nested-container layering for gradient frame effects
- Dot-matrix wave patterns for dark surface texture
- Proper shadows on light surfaces
- Screenshots always framed (gradient background + container), never floating raw

**Complete when:** The output has visible depth and spatial interest. Dark surfaces are not flat. Light surfaces have appropriate shadow/elevation. There is at least one moment of visual intensity (the hero gradient or signature element), and the rest shows restraint. The output could not be mistaken for a default template.

---

## Step 7: Run Interrogation Checklist

**What to do:** Load and run every item in the interrogation checklist. This is a systematic pass/fail review against the brand system. Fix auto-fixable items immediately. Flag structural issues for the user.

The interrogation checklist now includes an **AI Pattern Detection** section (10 items) in addition to the existing typography, color, gradient, depth, spacing, composition, surface treatment, content fit, and medium-specific checks. Pay particular attention to the AI pattern items — they catch the most common LLM design defaults (centered-everything, flat cards, symmetric gradients, same layout repeated, improvised CSS).

**Files to load:**
- `context/design-system/interrogation-checklist.md` — Full checklist including AI Pattern Detection section
- `context/design-system/ai-pattern-blocklist.md` — Reference for understanding flagged AI patterns

**Output:** A pass/fail result for every checklist item. Auto-fixable failures are corrected inline:
- Wrong font: fix to correct font family
- Wrong color: fix to correct hex value
- Wrong spacing: fix to correct 8px grid value
- Wrong line-height or weight: fix to correct value

Structural failures are documented with a specific description and proposed alternatives:
- Composition does not work for this content
- Layout needs rethinking for the medium
- Content does not fit any available element pattern

**Complete when:** All auto-fixable items pass. If there are structural failures, they are documented with clear descriptions and at least one proposed alternative each. The design-director does not present the output until all auto-fixable items are resolved.

---

## Step 8: Content Fit

**What to do:** Fit copy into layouts. The default is VERBATIM. Your job is to make the layout work for the content, not to rewrite the content for the layout.

**Files to load:** None additional. Work with the composed output from Steps 5-7. Refer back to the text inventory from Step 0.

**Output:** Copy that fits its containers with minimal or zero changes from the source.

### Content Editing Guardrails

**DEFAULT IS VERBATIM.** Preserve ALL user-provided text exactly as written.

The only allowed changes:

1. **Inserting line breaks** for layout fit (e.g., forcing a break to avoid orphans or improve card alignment).
2. **Removing 1-3 words** if text literally overflows a container and no layout adjustment can solve it.

That is the complete list. There are no other allowed changes.

**NEVER reword.** Do not rephrase, synonym-swap, tighten, or "improve" copy.
**NEVER add content.** Do not insert words, sentences, bullets, or sections that are not in the source.
**NEVER change facts, statistics, product names, model names, or technical claims.** Swimm, Swimm MCP, Understanding Platform, Opus 4.6, and any other proper nouns, version numbers, or factual claims are immutable. If the source says "Opus 4.6", the output says "Opus 4.6" — not "Sonnet", not "Claude", not any other substitution.

**Report every single change you make, no matter how small.** Even a removed "the" must be reported: "Removed 'the' from [original phrase] to fit [container]."

**If text doesn't fit a layout, adjust the LAYOUT not the text.** Choose a different element, reduce font size within the type scale, switch to a wider variant, or split across two slides/sections. Changing the layout is always preferred over changing the words.

**Large structural changes (restructuring): ask first.** Removing a section, reordering the argument flow, combining two sections into one, splitting a section into multiple slides, or changing what information is emphasized are large changes. When a large change is needed, explain the constraint and propose the change.

**Verification:** Before completing this step, diff every text string in the output against the Step 0 inventory. Any deviation must be listed, justified, and reported to the user.

**Complete when:** All copy fits its containers. Every change (no matter how small) has been reported. Product names, model names, statistics, and factual claims are unchanged. The Step 0 inventory diff shows zero unreported deviations.

---

## Step 9: Present

**What to do:** Show the polished output to the user. Design thinking (why you chose this element, why this rhythm, why this gradient here) stays internal unless the user specifically asks to see the rationale. The output speaks for itself.

**Files to load:** None. This is delivery.

**Output:** The final visual output (HTML file, Marp deck, PPTX, or rendered image) ready for use. If the design-reviewer (run in Step 7 or dispatched separately) flagged structural issues that were not resolved, surface those to the user with the proposed alternatives.

**Complete when:** The user has the output. If there were structural issues, the user has been told what they are and what the alternatives look like. The design-director does not silently ship known problems.
