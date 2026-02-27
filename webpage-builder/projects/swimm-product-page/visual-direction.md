# Swimm Product Page — Visual Direction v2

> **Status**: Designer agent v2 (Brand Director directives applied)
> **Date**: 2026-02-24
> **Design approach**: Enterprise product page. Dark/light rhythm establishes visual chapters. Typography-driven hierarchy. Product screenshots dominate — copy serves as labels and annotations. Every visual choice reinforces the "serious platform for serious work" positioning.

---

## Design System

### Color Palette

| Token | Hex | Usage | Rationale |
|-------|-----|-------|-----------|
| **Navy** (primary dark) | `#0A1628` | Dark section backgrounds, hero, Sections 5+6, 9 | Deep, authoritative base. Avoids pure black — adds warmth and depth. |
| **Slate** (dark surface) | `#111D31` | Cards on dark backgrounds, elevated dark surfaces | Subtle lift from navy for layering on dark sections. |
| **White** | `#FFFFFF` | Light section backgrounds | Clean, airy contrast to dark sections. |
| **Cool Gray 50** | `#F7F8FA` | Alternate light backgrounds (Section 3), card surfaces on white | Prevents white-on-white monotony. Subtle section demarcation. |
| **Brand Blue** | `#2563EB` | Primary CTAs, active tab fills, interactive elements, accent bars | Confident, high-contrast action color. Visible on both dark and light. |
| **Brand Blue Hover** | `#1D4ED8` | CTA hover states, link hover | Deeper blue for interactive feedback. |
| **Light Blue** | `#DBEAFE` | Feature pills, secondary badges on light backgrounds | Soft blue for supporting elements without competing with primary. |
| **Ice Blue** | `#EFF6FF` | Stat card backgrounds on dark, icon grid backing | Barely-there blue tint for subtle surface variation. |
| **Text Primary (dark bg)** | `#F1F5F9` | Headings and body text on dark backgrounds | Warm white — avoids harsh pure white on dark. |
| **Text Muted (dark bg)** | `#94A3B8` | Sublines, fine print, secondary text on dark | Readable muted text that doesn't compete with headlines. |
| **Text Primary (light bg)** | `#0F172A` | Headings on light backgrounds | Near-black with blue undertone. Matches the navy palette. |
| **Text Secondary (light bg)** | `#475569` | Body text, descriptions on light backgrounds | Medium gray for readable supporting copy. |
| **Text Muted (light bg)** | `#64748B` | Fine print, labels, pills on light backgrounds | Lighter gray for tertiary information. |
| **Border Light** | `#E2E8F0` | Card borders, dividers on light backgrounds | Subtle structural lines. |
| **Border Dark** | `#1E293B` | Card borders, dividers on dark backgrounds | Visible but not prominent on dark surfaces. |
| **Accent Green** | `#10B981` | Freshness indicator (Section 6), positive stat markers | Reserved for "verified/current" signals. Sparingly used. |
| **Accent Amber** | `#F59E0B` | Category badges (BRE section), warmth accent | Used for classification labels. Not a primary color. |

**Color discipline rules:**
- Maximum 3 colors visible in any single viewport (background + text + one accent)
- Brand Blue is the only saturated color used for CTAs — no competing action colors
- Accent Green and Amber appear only in context-specific elements, never as section-level color
- Dark sections use a single background value (Navy), not gradients, unless specified

### Typography

**Font stack**: `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif` (via Google Fonts CDN)

| Level | Size (desktop) | Weight | Line Height | Letter Spacing | Usage |
|-------|---------------|--------|-------------|----------------|-------|
| **Display** | 56px / 3.5rem | 700 | 1.1 | -0.02em | Hero H1 only |
| **H2** | 40px / 2.5rem | 700 | 1.2 | -0.015em | Section headings |
| **H3** | 24px / 1.5rem | 600 | 1.3 | -0.01em | Card headings, subheadlines within sections |
| **Body Large** | 20px / 1.25rem | 400 | 1.6 | 0 | Hero subline, bridge statements, declarations |
| **Body** | 16px / 1rem | 400 | 1.6 | 0 | Card descriptions, tab content copy |
| **Body Small** | 14px / 0.875rem | 400 | 1.5 | 0 | Feature pills, fine print, labels |
| **Caption** | 12px / 0.75rem | 500 | 1.4 | 0.02em | Badges, category labels |
| **Stat Number** | 72px / 4.5rem | 800 | 1.0 | -0.03em | Section 5 stat pair (75%, 61%) |
| **Declaration** | 28px / 1.75rem | 500 | 1.4 | -0.01em | Pull quote typography (Sections 5, 6) |

**Typography rules:**
- Inter for everything — no secondary font. Consistency over variety.
- Headings use negative letter-spacing for tightness at large sizes
- Body text stays at default (0) letter-spacing for readability
- No italic in headings. Italic reserved for inline emphasis only.
- Em-dashes in headings: use ` — ` with spaces (matching brand voice)

### Spacing System

Base unit: 8px. All spacing uses multiples of 8.

| Token | Value | Usage |
|-------|-------|-------|
| `space-xs` | 8px | Icon-to-label gap, badge padding |
| `space-sm` | 16px | Intra-component spacing (card padding inner elements) |
| `space-md` | 24px | Card internal padding, paragraph spacing |
| `space-lg` | 32px | Between components within a section |
| `space-xl` | 48px | Between content groups within a section |
| `space-2xl` | 64px | Section padding (top/bottom) — light sections |
| `space-3xl` | 80px | Section padding (top/bottom) — dark sections |
| `space-4xl` | 120px | Hero vertical padding |

**Section padding rule:**
- Dark sections get `space-3xl` (80px) top/bottom — more room to breathe on dark
- Light sections get `space-2xl` (64px) top/bottom
- Hero gets `space-4xl` (120px) top, `space-3xl` (80px) bottom
- Sections 5+6 share continuous dark background — no padding between them, just `space-xl` (48px) internal divider

### Container

| Breakpoint | Container Width | Side Padding |
|------------|----------------|--------------|
| Mobile (< 768px) | 100% | 24px |
| Tablet (768–1024px) | 720px | 32px |
| Desktop (1025–1440px) | 1120px | auto (centered) |
| Large (> 1440px) | 1200px | auto (centered) |

Max content width: **1200px**. No content wider than this. Screenshots can bleed to 1120px within the container.

### Border Radius

| Element | Radius |
|---------|--------|
| Cards | 12px |
| Buttons | 8px |
| Badges / Pills | 20px (full round) |
| Screenshots | 8px + 1px border |
| Tab container | 12px |
| Icon containers | 12px |

### Shadows

| Level | Value | Usage |
|-------|-------|-------|
| Card (light bg) | `0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)` | Cards on white/gray backgrounds |
| Card hover (light bg) | `0 4px 12px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06)` | Card hover states on light backgrounds |
| Card (dark bg) | none — use border instead | Cards on dark backgrounds use `border: 1px solid #1E293B` |
| Screenshot | `0 8px 32px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.06)` | Product screenshot frames |

No box-shadow on dark backgrounds. Use borders for elevation on dark.

---

## Section-by-Section Visual Direction

### Section 1: Hero + Marketecture

**Layout**: Full-width, dark background (`#0A1628`). Two zones stacked.

**Zone A — Text block** (top):
- Centered alignment on mobile, left-aligned on desktop
- H1 (Display, 56px, 700): Two lines. "One understanding layer." / "For your team and your AI."
- Subline (Body Large, 20px, `#94A3B8`): Below H1, 16px gap
- Phrase pair (Body, 16px, `#94A3B8`): Two lines, 8px gap between them. Slightly indented or separated from subline.
- CTA button: Brand Blue (`#2563EB`) fill, white text, 16px/32px padding, 8px radius. 32px below phrase pair.

**Zone B — Marketecture visual** (below text):
- Full container width (1120px max), centered
- SVG illustration showing the 4-layer architecture: Code In → Understanding Engine → Capabilities → Delivery
- Light strokes and fills on dark background. Use `#F1F5F9` for primary lines, `#2563EB` for accent nodes/arrows, `#94A3B8` for labels
- Minimum 400px height on desktop. This IS the hero — it dominates.
- On mobile: simplified to a vertical stack of the 4 layers

**Spacing**:
- Top padding: 120px
- Gap between Zone A and Zone B: 64px
- Bottom padding: 80px

**Responsive behavior**:
- Desktop (>1024px): Text left-aligned, marketecture right or below (2-column if visual allows, otherwise stacked)
- Tablet: Stacked, text centered, marketecture full-width below
- Mobile: Stacked, text centered, marketecture simplified (vertical layers)

**Interaction**: None. Static hero. No parallax, no scroll animations. The visual clarity IS the impact.

---

### Section 2: Application Map

**Layout**: Light background (`#FFFFFF`). Stacked vertical layout within container.

**Zone A — Header**:
- H2 (40px, 700, `#0F172A`): Centered
- Subline (Body, 16px, `#475569`): Centered, 12px below H2

**Zone B — Persona cards** (3-column grid):
- CSS Grid: `grid-template-columns: repeat(3, 1fr)`, gap 24px
- Each card: `#F7F8FA` background, 12px radius, 24px padding, no border
- Card structure:
  - Icon (40x40, line-style SVG, Brand Blue stroke)
  - Persona label (H3, 18px, 600, `#0F172A`): 16px below icon
  - Description (Body, 16px, `#475569`): 8px below label. 2 lines max.
- Cards are equal height (grid alignment)

**Zone C — Product screenshot**:
- 32px below cards
- Full container width (1120px), centered
- Screenshot inside a mock browser frame: 8px radius, 1px `#E2E8F0` border, screenshot shadow
- Screenshot is the Application Map domain view
- Target: screenshot occupies 60%+ of visible section area

**Zone D — Swimm Assistant callout**:
- 24px below screenshot, anchored to its bottom-right
- Small card: `#F7F8FA` background, 12px radius, 16px padding
- Chat icon (16x16) + text (Body Small, 14px, `#475569`)
- Max width: 400px. Right-aligned or centered on mobile.

**Zone E — Feature pills**:
- 24px below callout
- Horizontal row of pill badges, centered, flex-wrap
- Each pill: `#DBEAFE` background, `#2563EB` text, 20px radius, 8px/16px padding, Body Small (14px)
- 8px gap between pills

**Spacing**: 64px top/bottom padding.

**Responsive behavior**:
- Tablet: 3-column cards → 3-column (narrower), screenshot full-width
- Mobile: Cards stack to single column. Screenshot full-width with horizontal scroll hint if needed. Pills wrap to 2 rows.

**Interaction**:
- Persona cards: subtle hover — shadow elevates from Card to Card Hover
- No animation on scroll entry (screenshot is the anchor — it must be immediately visible and still)

---

### Section 3: Business Rules & Flows

**Layout**: Light background (`#F7F8FA` — subtle contrast from Section 2's white). Stacked layout.

**Zone A — Header**:
- H2 (40px, 700, `#0F172A`): Centered. Two-line headline with em-dash.

**Zone B — Tabbed interface**:
- Tab container: 12px radius, `#FFFFFF` background, Card shadow, 32px below header
- Tab bar at top: segmented control style, left-aligned within the container
  - Container: `#F7F8FA` background, 8px radius (pill shape), 4px padding
  - Active tab: Brand Blue (`#2563EB`) fill, `#FFFFFF` text, 600 weight, 8px radius (nested pill)
  - Inactive tab: transparent background, `#64748B` text, 400 weight
  - Tab labels: "Business Rules" | "Execution Paths"
  - 44px tab height, 24px horizontal padding per tab
  - Active state transition: background-color 200ms ease (pill slides to active tab)

- Tab content area: 32px padding inside container
  - Two-column layout: text (40%) | screenshot (60%)
  - Text column:
    - Subheadline (H3, 24px, 600, `#0F172A`)
    - Category badges (Tab 1 only): Horizontal pills with `#FEF3C7` (amber light) background, `#92400E` text, Caption size. 16px below subheadline.
    - One-liner (Body, 16px, `#475569`): 16px below badges
  - Screenshot column:
    - Product screenshot, 8px radius, 1px border, screenshot shadow
    - Takes full 60% width

**Zone C — Persona callout bar**:
- 32px below tab container
- 3-column layout, centered, max-width 900px
- Each callout: no background, text only
  - Label (Body Small, 14px, 600, `#0F172A`): Persona name
  - Description (Body Small, 14px, 400, `#64748B`): What they see
- Vertical dividers between columns (1px `#E2E8F0`)

**Spacing**: 64px top/bottom padding.

**Responsive behavior**:
- Tablet: Tab content goes from 40/60 to stacked (text above screenshot). Persona bar stays 3-column.
- Mobile: Tabs remain functional. Content fully stacked. Persona bar stacks to single column with horizontal dividers.

**Interaction**:
- Tab switching: instant content swap (no animation). Active tab underline transition: 200ms ease.
- This is the only interactive element on the page — it must feel crisp and responsive.

---

### Section 4: Glossary & Collections

**Layout**: Light background (`#FFFFFF`). Stacked layout.

**Zone A — Header**:
- H2 (40px, 700, `#0F172A`): Centered.

**Zone B — Split block** (2-column):
- CSS Grid: `grid-template-columns: repeat(2, 1fr)`, gap 48px
- Each column is a feature block:
  - Feature label (H3, 24px, 600, `#0F172A`): "Glossary" / "Collections"
  - Visual area (above or integrated with text):
    - Glossary: illustration or screenshot showing code name → business term transformation
    - Collections: screenshot showing wiki-style content with edit cursor
    - Visual: 8px radius, 1px border, screenshot shadow. Occupies top 60% of column.
  - Description text (Body, 16px, `#475569`): Below visual. 3-4 lines max.

**Zone C — Bridge statement**:
- 48px below split block
- Centered text, max-width 700px
- Body Large (20px, 400, `#475569`), no italic — the transitional tone comes from content and positioning, not typographic styling
- Connects capabilities story to the AI section that follows

**Zone D — Mid-page CTA**:
- 24px below bridge statement, centered
- Ghost button: transparent background, 1px `#2563EB` border, `#2563EB` text, 8px radius, 14px/28px padding
- "See how it works"

**Spacing**: 64px top/bottom padding.

**Responsive behavior**:
- Tablet: 2-column stays, narrower gap (32px)
- Mobile: Stacks to single column. Glossary above Collections.

**Interaction**:
- Ghost CTA: on hover, fill transitions to `#2563EB` background, text to white. 200ms ease.

---

### Section 5: Context for AI

**Layout**: Dark background (`#0A1628`). **Begins the 5+6 paired visual unit.** No bottom padding — flows directly into Section 6.

**Section transition (4→5)**: This is the most dramatic color shift on the page — white to Navy — at the narrative pivot from capabilities to AI strategy. Use increased top padding (100px instead of 80px) for a clean hard edge that feels intentional and gives the eye a moment to reset. No gradient — the hard cut signals a chapter change.

**Zone A — Header**:
- H2 (40px, 700, `#F1F5F9`): Centered. Two-line headline.
- Subline (Body, 16px, `#94A3B8`): Centered, 12px below.

**Zone B — Stat pair**:
- 48px below header
- Two stat cards, side by side, centered. Max-width 600px total.
- CSS Grid: `grid-template-columns: repeat(2, 1fr)`, gap 32px
- Each stat card:
  - Background: `#111D31` (Slate), 12px radius, 32px padding
  - Number (Stat Number, 72px, 800, `#F1F5F9`): Warm white for maximum impact and readability
  - Accent bar: 4px wide, Brand Blue (`#2563EB`), left edge of stat card. Provides color accent without relying on the number for it.
  - Label (Body, 16px, `#94A3B8`): Below number, 8px gap. Two lines.
- Fine print (Caption, 12px, `#64748B`): Centered below both cards. "Benchmarked with Claude Code"

**Zone C — 3-step process indicator**:
- 48px below stats
- Horizontal: three nodes connected by a line
- Node: 48px circle, `#111D31` fill, 1px `#2563EB` border. Number inside (Body, 16px, `#F1F5F9`)
- Connecting line: 2px, `#1E293B`
- Label below each node: Body Small (14px, `#94A3B8`), centered under node
- Max-width 700px, centered

**Zone D — Product visual**:
- 48px below process indicator
- Centered screenshot: MCP config or Swimm Assistant chat showing a grounded answer
- Max-width 900px, 8px radius, 1px `#1E293B` border (dark border for dark bg)
- No shadow on dark (use border)

**Zone E — Declaration**:
- 48px below visual
- Centered text, max-width 700px
- Declaration typography (28px, 500, `#F1F5F9`): Three lines, each on its own line
- Slightly increased line-height (1.5) for pull-quote feel

**Spacing**: 100px top padding (increased for 4→5 transition impact), 48px bottom (internal divider before Section 6, no visual break).

**Responsive behavior**:
- Tablet: Stat cards stay side-by-side. Process indicator horizontal. Screenshot narrower.
- Mobile: Stat cards stack vertically. Process indicator goes vertical (nodes in a column with connecting line). Declaration wraps naturally.

**Interaction**: None. Static. The numbers and declaration carry the weight.

---

### Section 6: Human Governance & Control

**Layout**: Dark background (`#0A1628`) — continues from Section 5. **Completes the 5+6 paired unit.**

**Zone A — Header**:
- H2 (40px, 700, `#F1F5F9`): Centered.

**Zone B — Governance icon grid** (5-column):
- 32px below header
- CSS Grid: `grid-template-columns: repeat(5, 1fr)`, gap 24px, max-width 1000px, centered
- Each grid item:
  - Icon container: 56x56, `#111D31` background, 12px radius, centered
  - Icon: 28x28 line-style SVG, `#F1F5F9` stroke
  - Label (H3, 16px, 600, `#F1F5F9`): 12px below icon. One word.
  - Description (Body Small, 14px, `#94A3B8`): 4px below label. 2-3 lines max.
- Items: Traceability, Freshness, SME Verify, Editability, Deterministic

**Zone C — Closing declaration**:
- 48px below grid
- Centered, max-width 600px
- Declaration typography (28px, 500, `#F1F5F9`): Matching Section 5's pull quote style
- Two lines: "Human governance, AI execution —" / "sharing the same trusted foundation."

**Zone D — CTA**:
- 32px below declaration
- Ghost button: transparent background, 1px `#F1F5F9` border, `#F1F5F9` text
- "Talk to our team"
- Hover: `#F1F5F9` fill, `#0A1628` text. 200ms ease.

**Spacing**: 48px top (internal from Section 5), 80px bottom.

**Responsive behavior**:
- Tablet: 5-column → 3-column + 2-column (2 rows). Grid reflows.
- Mobile: 2-column grid (2+2+1 rows). Or single column if space is tight.

**Interaction**:
- Ghost CTA hover fill transition
- No scroll animations

---

### Section 7: How It Works

**Layout**: Light background (`#FFFFFF`). Visual break from dark 5+6 unit.

**Zone A — Header**:
- H2 (40px, 700, `#0F172A`): Centered. Two-line headline with periods and em-dash.

**Zone B — Pipeline diagram**:
- 32px below header
- Horizontal pipeline: 4 stages connected by arrows
- Full container width (1120px), centered
- Each stage:
  - Box: `#F7F8FA` background, 12px radius, 1px `#E2E8F0` border, 32px padding
  - Stage label (H3, 18px, 600, `#0F172A`): Top of box. All caps, letter-spacing 0.05em
  - Description lines (Body Small, 14px, `#475569`): Below label. 3-4 lines.
  - Box height: equal across all 4 (CSS Grid align-items: stretch)
- Connecting arrows: SVG arrows between boxes, `#2563EB` stroke, 2px
- CSS Grid: `grid-template-columns: repeat(4, 1fr)`, gap for arrow space
- Stages: CODE IN → STATIC ANALYSIS → STRUCTURAL GRAPH → AI TRANSLATE

**Zone C — Detail pills**:
- 32px below pipeline
- Horizontal row of pills, centered, flex-wrap
- Same pill styling as Section 2: `#DBEAFE` background, `#2563EB` text, 20px radius
- 6 pills: "21+ languages", "Mainframe-first", "No compilation", "No mainframe access", "Plugin-based", "Your own LLM"

**Zone D — Trust statement**:
- 32px below pills
- Centered text, max-width 700px
- Body (16px, 400, `#475569`): Two sentences.

**Spacing**: 64px top/bottom padding.

**Responsive behavior**:
- Tablet: Pipeline stays 4-column but narrower. Arrows shrink.
- Mobile: Pipeline stacks vertically. Boxes full-width, connected by vertical arrows. Pills wrap to 2-3 rows.

**Interaction**: None. The diagram speaks for itself.

---

### Section 8: Enterprise Readiness

**Layout**: Light background (`#F7F8FA` — subtle contrast from Section 7's white).

**Zone A — Header**:
- H2 (40px, 700, `#0F172A`): Centered. Three short statements with periods.

**Zone B — Unified enterprise grid** (single parent container):
- 32px below header
- Parent container: `#FFFFFF` background, 12px radius, Card shadow, 32px padding
- Internal structure: two rows separated by a 1px `#E2E8F0` horizontal divider with 24px margin above/below

- **Row 1: Deployment & Security** (4-column grid inside parent):
  - CSS Grid: `grid-template-columns: repeat(4, 1fr)`, gap 24px
  - First two items (Deploy, LLM): Text style
    - No individual card background (inherits parent white)
    - Icon (40x40, line-style SVG, `#0F172A` stroke)
    - Label (H3, 18px, 600, `#0F172A`): 12px below icon
    - Details (Body Small, 14px, `#475569`): 8px below label
  - Last two items (SOC 2, ISO 27001): Badge style
    - Certification badge visual (SVG or styled element): centered
    - No description text — the badge IS the content

- **Divider**: 1px `#E2E8F0`, full width of parent container

- **Row 2: Languages & Integrations** (inside same parent):
  - Language logo grid:
    - Flex row of language logos/icons: monochrome grayscale, 32x32 each, 16px gap
    - Two rows of logos: mainframe first row, modern second row
    - Label below (Body Small, 14px, `#64748B`): "21+ languages, mainframe-first"
  - 24px below language grid: 2-column for Plugin + IDE
    - No individual card background (inherits parent white)
    - Icon + label + short description each

**Spacing**: 64px top/bottom padding.

**Responsive behavior**:
- Tablet: Row 1 stays 4-column. Language grid stays. Plugin/IDE stays 2-column.
- Mobile: Row 1 becomes 2x2 grid. Language logos wrap. Plugin/IDE stacks.

**Interaction**:
- Cards have subtle hover shadow lift

---

### Section 9: Conversion

**Layout**: Dark background (`#0A1628`). Full-width. Mirrors hero. Minimal.

**Zone A — centered content**:
- Max-width 600px, centered both horizontally and vertically in the section
- H2 (40px, 700, `#F1F5F9`): Centered. "See Swimm on your code"
- Subline (Body Large, 20px, `#94A3B8`): 16px below. Two lines.
- CTA button: Brand Blue (`#2563EB`) fill, white text, **larger than hero CTA** — 18px/40px padding, 8px radius. 32px below subline.
- Friction reducer (Body Small, 14px, `#64748B`): 16px below button. "Free evaluation on your codebase"

**Spacing**: 80px top/bottom padding. Generous — section should feel spacious and confident, not cramped.

**Responsive behavior**:
- All breakpoints: centered stack. Text wraps naturally. Button stays full-width on mobile (max-width 320px).

**Interaction**:
- CTA hover: Brand Blue Hover (`#1D4ED8`). 200ms ease.

---

## Full-Page Visual Rhythm

| # | Section | Background | Typography Color | Mood |
|---|---------|------------|-----------------|------|
| 1 | Hero | `#0A1628` Navy | `#F1F5F9` / `#94A3B8` | Authority, platform statement |
| 2 | App Map | `#FFFFFF` White | `#0F172A` / `#475569` | Open, exploratory, product-forward |
| 3 | BRE+Flows | `#F7F8FA` Cool Gray | `#0F172A` / `#475569` | Depth, technical substance |
| 4 | Glossary+Collections | `#FFFFFF` White | `#0F172A` / `#475569` | Bridge, human element |
| 5 | Context for AI | `#0A1628` Navy | `#F1F5F9` / `#94A3B8` | Strategic weight, big numbers |
| 6 | Governance | `#0A1628` Navy (continues) | `#F1F5F9` / `#94A3B8` | Trust, control, paired with 5 |
| 7 | How It Works | `#FFFFFF` White | `#0F172A` / `#475569` | Mechanism, clarity |
| 8 | Enterprise | `#F7F8FA` Cool Gray | `#0F172A` / `#475569` | Checklist, qualification |
| 9 | Conversion | `#0A1628` Navy | `#F1F5F9` / `#94A3B8` | Bookend, action |

**Rhythm**: Dark → Light → Light(gray) → Light → **Dark → Dark** → Light → Light(gray) → Dark

The dark sections (1, 5+6, 9) create three "chapters": positioning, strategic differentiation, and conversion. The light sections between them present product capabilities and mechanism. This creates a natural reading rhythm where the eye resets at each dark/light transition.

---

## Responsive Breakpoint Summary

| Breakpoint | Width | Key Changes |
|------------|-------|-------------|
| **Mobile** | < 768px | Single column. Stacked layouts. Pipeline vertical. Stat cards stacked. 5-col icon grid → 2-col. Tabs functional, content stacked. |
| **Tablet** | 768–1024px | 2-3 column grids maintained where possible. Tab content stacked (text above screenshot). Pipeline 4-col but narrow. |
| **Desktop** | 1025–1440px | Full layouts as specified. Container 1120px centered. |
| **Large** | > 1440px | Container caps at 1200px. Extra space as side margins. |

---

## Animation Strategy

**Philosophy**: Restraint. This is an enterprise product page, not a startup landing page. Motion is used only where it communicates information or provides interaction feedback.

**Allowed animations**:
1. Tab switching (Section 3): content swap, 200ms ease on active tab underline
2. Button hover states: background/color transitions, 200ms ease
3. Card hover: shadow lift transition, 200ms ease
4. `prefers-reduced-motion`: all animations disabled. Instant state changes.

**Not used**:
- No scroll-triggered animations (fade-in, slide-up, parallax)
- No loading animations
- No auto-playing elements
- No decorative motion

The page should feel solid and still. Visual impact comes from typography, color, and composition — not movement.

---

## Screenshot & Visual Asset Requirements

| Section | Asset | Type | Notes |
|---------|-------|------|-------|
| 1 | Marketecture diagram | SVG (custom) | 4-layer architecture: Code In → Engine → Capabilities → Delivery |
| 2 | Application Map | Screenshot | Domain view with business-named domains, process counts |
| 3a | Business Rules table | Screenshot | Rules with categories (Input, Calc, Invoking, Output) |
| 3b | Execution Paths | Screenshot | Flow graph or code walkthrough with interleaved prose |
| 4a | Glossary | Screenshot or illustration | Code name → business term transformation |
| 4b | Collections | Screenshot | Wiki-style content with edit cursor, Mermaid diagram |
| 5 | MCP / Swimm Assistant | Screenshot | MCP config or chat showing grounded answer |
| 6 | Governance icons | SVG (5 icons) | Traceability, Freshness, SME Verify, Editability, Deterministic |
| 7 | Pipeline diagram | SVG or CSS | 4-stage horizontal pipeline with arrows |
| 8a | Language logos | SVG/PNG set | COBOL, PL/I, JCL, Assembler, RPG, Java, C/C++, C#, Python, Go |
| 8b | Certification badges | SVG | SOC 2, ISO 27001 |
| 8c | IDE icons | SVG | VS Code, Visual Studio, JetBrains |

**Screenshot treatment** — two tiers to create visual hierarchy:

**Primary screenshots** (Section 2 App Map, Section 5 MCP view):
- Full container width or near-full
- Mock browser chrome: thin bar (32px) at top with 3 dots (traffic lights) and URL bar hint
- 8px border-radius on outer frame
- 1px border (light: `#E2E8F0`, dark: `#1E293B`)
- Shadow (light bg only): screenshot shadow value
- These are the page's anchor visuals — they establish scale and presence

**Secondary screenshots** (Section 3 tab content, Section 4 split content):
- Inline within their layout column (40-60% width)
- No browser chrome — tighter crop, content-only
- 8px border-radius
- 1px border (light: `#E2E8F0`, dark: `#1E293B`)
- Shadow (light bg only): card shadow value (lighter than primary)
- These support the copy — they illustrate, not anchor

---

## Accessibility Notes

- All color combinations meet WCAG 2.1 AA contrast ratio (4.5:1 for body, 3:1 for large text)
- Navy (`#0A1628`) + `#F1F5F9`: contrast ratio ~15:1 (passes AAA)
- Navy + `#94A3B8`: contrast ratio ~6.5:1 (passes AA)
- White + `#0F172A`: contrast ratio ~16:1 (passes AAA)
- White + `#475569`: contrast ratio ~6.6:1 (passes AA)
- White + `#64748B`: contrast ratio ~4.8:1 (passes AA for body text)
- Brand Blue (`#2563EB`) on Navy: contrast ratio ~4.7:1 (passes AA for large text — stat numbers qualify)
- All interactive elements have visible focus states (2px Brand Blue outline, 2px offset)
- Tabs use proper `role="tablist"`, `role="tab"`, `role="tabpanel"` ARIA
- Screenshot alt text required for all product screenshots
- Semantic heading hierarchy: one H1 (hero), H2s for sections, H3s for subsections
