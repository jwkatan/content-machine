# Design Interrogation Checklist

Run every item before delivering any visual output. Each item is pass/fail.

## Typography

- [ ] Regesto Grotesk for ALL headings (H1-H5, Special)?
- [ ] Manrope for ALL body text, labels, footnotes, buttons?
- [ ] Correct weights? (H1-H5: Regular 400. Special: Light 300. P1/P4: Regular 400. P2/P3: Light 300.)
- [ ] Correct sizes? (H1: 60px, H2: 42px, H3: 26px, H4: 20px, H5: 16px, P1: 18px, P2: 24px, P3: 20px, P4: 16px)
- [ ] Line heights correct? (Headings: 110%. Special: 85%. Body P1-P4: 140%. Labels S: 140%, M: 100%, L: 85%, XL: 120%)

## Color

- [ ] Brand palette only? No off-brand colors?
- [ ] Blue-tinted grays (Gray 500 #415992, Gray 300 #8594BE, etc.) — NOT pure grays?
- [ ] Correct semantic usage? (Light surface: Blue 900 headings, Gray 500 body. Dark surface: Gray 50/150 headings, Blue 300 body)
- [ ] Accent colors used sparingly? (Pink 400, Yellow 200 exist only as narrow transition bands in gradients — never flat fills or standalone accents)

## Gradients

- [ ] Using the signature Blue → Pink → Yellow spectrum where appropriate?
- [ ] Correct multi-stop gradient formulas from the element library (not approximations)?
- [ ] Radial gradients on dark cards following the exact formula?

## Depth & Layering

- [ ] Is there visual depth? (Nested frames, SVG radial gradients, blend modes: `lighten`, `multiply`, `screen`)
- [ ] Are dark surfaces using the dot-grid pattern (`background-mesh`) or SVG radial gradient overlays?
- [ ] Are gradient sections using the nested-container layering technique (4 levels with abs-positioned gradient backgrounds)?
- [ ] No `box-shadow` used? (The system uses zero shadows — all depth comes from SVG radial gradients, blend modes, and opacity layering)

## Spacing

- [ ] Spacing values from tokens.css? (8px grid is a guideline, not strict — 36px and 12px are common off-grid values)
- [ ] Section padding: 100px vertical? (Horizontal padding is element-specific, not a universal 120px)
- [ ] Content max-width: 1200px?
- [ ] Card internals: 32px padding, 24px icon-to-text gap, 12px text stack gap?
- [ ] Cards have sharp corners (no border-radius)? Screenshot frames have sharp corners (no border-radius)?

## Composition

- [ ] Visual hierarchy clear? Not center-everything default?
- [ ] Using split layout where appropriate? (H2 left max-width 500px + P3 right max-width 450-500px)
- [ ] Dark/light surface alternation? Not more than 2 consecutive same-surface sections?

## Surface Treatment

- [ ] Dark surface: Blue 900 bg, Gray 50 headings, Blue 300 body, radial gradient overlays for depth?
- [ ] Light surface: Gray 100 bg, Blue 900 headings, Gray 500 body?
- [ ] Screenshots always framed (gradient background + container), never floating raw?
- [ ] Light-surface cards use Light-100 radial gradient background? (Not flat Gray-100. Every card on a light surface has `--gradient-light-100` as its background.)

## Content Fit

- [ ] Headlines fit their containers?
- [ ] No orphaned words or awkward line breaks?
- [ ] Copy edited for layout without changing meaning?

## Medium-Specific (PPTX/Marp)

- [ ] Web patterns translated to slide constraints (not crammed)?
- [ ] One key idea per slide?
- [ ] Type scale adjusted for projection readability?

## AI Pattern Detection

- [ ] No centered-everything default? (Left-aligned text with purposeful grid placement is the standard. Only title-gradient, closing-gradient, and dark-statement slides center text. If >30% of text elements use `text-align: center`, flag it.)
- [ ] Layout diversity met? (For 10+ slides: at least 6 different slide type classes. For 6-9: at least 4. For 3-5: at least 3.)
- [ ] No consecutive identical layouts? (No two adjacent slides or sections use the same structural pattern — e.g., two card grids in a row, two statement slides in a row.)
- [ ] Dark surfaces have depth beyond flat fill? (Every dark surface has at least one depth treatment: SVG radial overlay, dot-grid pattern, or blend-mode layer. Flat Blue 900 with text is not a finished surface.)
- [ ] All gradients match canonical values? (Every gradient declaration matches a named gradient from tokens.css or an element library formula. No improvised gradient stops.)
- [ ] All font-sizes from the type scale? (Only these values: 60px, 42px, 26px, 24px, 20px, 18px, 16px, 14px, 12px. No 36px, 48px, 52px, 28px, or other invented sizes.)
- [ ] Zero box-shadows? (Grep for `box-shadow` — any occurrence is a failure. All depth uses SVG radials, blend modes, and opacity layering.)
- [ ] Zero border-radius on non-buttons? (All cards, frames, containers have `border-radius: 0`. Sharp corners are the brand signature.)
- [ ] Decorative elements serve the composition? (Every non-text element supports the slide's message or sets emotional tone. Remove what doesn't earn its place.)
- [ ] Color follows 60-30-10 rule? (60% dominant surface — typically Blue 900 dark. 30% secondary surface — typically Gray 100 light. 10% accent — gradient spectrum. Not a monochromatic blue wash.)

## Checklist Handling

- **Auto-fix failures:** Wrong font, wrong color, wrong spacing, wrong line-height — fix directly without escalating.
- **Escalate to user:** Composition doesn't work, layout needs rethinking, content doesn't fit any available element pattern.
- **AI Default failures:** Patterns that technically work but reveal AI generation (flat card backgrounds, centered-everything, symmetric gradients, same layout repeated). These are auto-fixable — the reviewer specifies the exact fix — but should be explicitly flagged as AI defaults in the report so the design-director learns to avoid them.
- **Threshold:** All auto-fixable items must pass. Any structural failure triggers user escalation with specific description of the problem and proposed alternatives.
