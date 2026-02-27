# Swimm Product Page — Decisions & Status

## Status

- **Page type**: product
- **Current phase**: Phase 4: Build
- **Created**: 2026-02-24
- **Last updated**: 2026-02-24
- **Primary audience**: Modernization leads, business analysts, engineers
- **Core positioning**: One place for humans and AI to share consistent, accurate context for modernization

## How to Resume This Project

Run `/webpage continue` — reads this file first, then resumes at current phase.

### Files to Load

| File | Purpose | When |
|------|---------|------|
| `decisions.md` | This file — project state and all decisions | Always first |
| `brief.md` | Approved messaging brief v3 (9 sections) | Phase 2+ |
| `content.md` | Approved content v3 — web page compositions with block-level structure | Phase 3+ |
| `webpage-builder/agents.md` | Agent personas | All phases |
| `context/brand-voice.md` | Brand voice and messaging guidelines | All phases |
| `webpage-builder/web-copy-style.md` | Web copy style tests and discipline | Phases 1-2 |
| `visual-direction.md` | Approved visual direction v2 (design system + section specs) | Phase 4+ |
| Product knowledge base (see below) | Full product context | Phases 1-2, 4 |

**Product knowledge base**: `/Users/jonweidberg/swimm/swimm_content_creation/tests/PMM researcher/config/teach_product_output.md`

Contains: Marketecture (4 layers), 7 features (App Map, BRE, Flows, Glossary, Collections, MCP, Swimm Assistant), technology (deterministic + AI translation, bidirectional linking, freshness), 21+ languages, integrations, deployment (on-prem, SOC 2 + ISO 27001), POC scorecard, packaging/pricing.

## Phase History

| Phase | Status | Approved | Notes |
|-------|--------|----------|-------|
| 1. Brief | complete | approved | Brief v3 approved. 3 PMM<->CMO iterations + major human revision. |
| 2. Content | complete | approved | Content v3 approved. Three iterations: v1 (prose paragraphs), v2 (line breaks), v3 (web page compositions). Website structure specialist review between v2→v3 identified 5 structural problems. v3 restructures all copy into atomic visual blocks. |
| 3. Design | complete | approved | Visual direction v2 approved. Designer v1 → Brand Director (7.8/10, 6 directives) → Designer v2 → Brand Director (8.6/10, ship) → Human approved. |
| 4. Build | complete | awaiting review | All 9 sections built. Real product screenshots from QA integrated. Designer review passed (2 minor fixes applied). Playwright tests: 26/26 passing across 5 viewports. |
| 5. Review | — | — | — |
| 6. Finalize | — | — | — |

## Content v3 Summary

Content is structured as web page compositions, not prose. Each section specifies atomic visual blocks (cards, tabs, grids, pipelines, stat pairs) — not paragraphs.

### Headline Story Arc

1. One understanding layer. For your team and your AI.
2. Your entire application, navigable in business language
3. Business rules and execution paths — extracted at unlimited depth
4. Code knowledge meets organizational knowledge
5. The trusted context AI agents rely on for forward engineering
6. Human governance. Your team controls what AI consumes.
7. Deterministic analysis. AI translation. One engine.
8. Your environment. Your LLM. Your perimeter.
9. See Swimm on your code

### Section Structure Map

| # | Section | Pattern | Background | Key Blocks |
|---|---------|---------|------------|------------|
| 1 | Hero | Text left + SVG dominant | Dark | H1 + subline + phrase pair + CTA + marketecture SVG |
| 2 | App Map | Cards + screenshot + callout | Light | 3-col persona cards + full screenshot + Swimm Assistant callout + feature pills |
| 3 | BRE+Flows | Tabbed interface | Light | 2 tabs swap copy+screenshot + persona callout bar |
| 4 | Glossary+Collections | Split block | Light | 2-col feature split + bridge statement + mid-page CTA |
| 5 | Context for AI | Stats + process + declaration | Dark | Stat pair + 3-step process indicator + product visual + pull quote |
| 6 | Governance | Icon grid + declaration | Dark (continues) | 5-col icon grid + closing declaration + CTA |
| 7 | How It Works | Annotated pipeline | Light | 4-stage pipeline diagram + detail pills + trust statement |
| 8 | Enterprise | Badge/icon grid | Light | 2-row grid (deploy+security / languages+integrations) |
| 9 | Conversion | Centered CTA | Dark | H2 + subline + button + friction reducer |

### Visual Rhythm

Dark → Light → Light → Light → **Dark → Dark** → Light → Light → Dark

### CTA Placement

| Position | CTA Text | Style |
|----------|----------|-------|
| Section 1 (Hero) | See it on your code | Filled, brand color |
| After Section 4 | See how it works | Ghost/outlined |
| After Section 6 | Talk to our team | Ghost, light (dark bg) |
| Section 9 (Conversion) | See Swimm on your code | Filled, larger |

### Key Content Decisions

- **No two consecutive sections use the same structural pattern** — cards, tabs, split blocks, stat pairs, icon grids, pipeline diagrams, badge grids
- **Sections 5+6 are a visual unit** — shared dark background, matching declaration typography, no visual break between them
- **Copy serves as labels and annotations** — not paragraphs. Screenshots and visuals dominate (60%+)
- **Section 3 uses tabs** — highest-stakes content (60% POC weight) gets interactive treatment to separate BRE from Flows
- **Proof points** (75% response time, 61% cost savings — Claude Code benchmark) displayed as large accent numbers in Section 5

## Design Decisions

1. **Marketecture in hero** (PMM + human): Marketecture SVG is the hero visual, 60%+ of section area. Headline anchors positioning; visual does structural storytelling.
2. **AI-forward positioning** (human directive): Section 5 is most strategically important. Paired with Section 6 for "human governance, AI execution."
3. **No "gap" section** (human directive): Technical audience knows the problem.
4. **Web UI primary, IDE secondary** (human directive): IDE is a line item in Section 8.
5. **Swimm Assistant in web experience** (CMO directive): Callout element in Section 2.
6. **Audience**: Modernization leads, BAs, engineers — multi-persona framing throughout.
7. **Feature scope**: Full platform organized by marketecture layers, not feature list.
8. **No product page template**: Structure derived from homepage template. Consider creating product template after project.
9. **Web page compositions, not prose** (human + structure review): Content restructured from paragraphs to atomic visual blocks after website structure specialist identified all 9 sections using identical headline+paragraph pattern. v3 uses 8 distinct structural patterns.
10. **Stat numbers in warm white, not Brand Blue** (Brand Director): 72px stat numbers use `#F1F5F9` for maximum impact; Brand Blue accent bar on left edge of stat card provides color accent without accessibility risk.
11. **Segmented control tabs** (Brand Director): Section 3 tabs use pill-style active state with Brand Blue fill instead of underline — makes interactive element visually distinct from surrounding text hierarchy.
12. **Screenshot hierarchy: primary vs secondary** (Brand Director): Primary screenshots (Sections 2, 5) get browser chrome + full width. Secondary screenshots (Sections 3, 4) are inline, no chrome, tighter crop.
13. **Section 8 unified container** (Brand Director): All enterprise readiness items live within a single parent card with internal dividers — prevents compositional fragmentation.
14. **Section 4→5 hard-edge transition** (Brand Director): Clean hard edge with 100px top padding at Section 5 — no gradient. Chapter change is intentional.

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| Navy (primary dark) | `#0A1628` | Dark section backgrounds (hero, 5+6, conversion) |
| Slate (dark surface) | `#111D31` | Cards and elevated surfaces on dark backgrounds |
| White | `#FFFFFF` | Light section backgrounds (2, 4, 7) |
| Cool Gray 50 | `#F7F8FA` | Alternate light backgrounds (3, 8), card surfaces on white |
| Brand Blue | `#2563EB` | CTAs, active tab fills, accent bars, interactive elements |
| Brand Blue Hover | `#1D4ED8` | CTA and link hover states |
| Light Blue | `#DBEAFE` | Feature pills, secondary badges on light backgrounds |
| Text Primary (dark) | `#F1F5F9` | Headings and stat numbers on dark backgrounds |
| Text Muted (dark) | `#94A3B8` | Sublines, secondary text on dark backgrounds |
| Text Primary (light) | `#0F172A` | Headings on light backgrounds |
| Text Secondary (light) | `#475569` | Body text on light backgrounds |
| Accent Green | `#10B981` | Freshness indicator only (Section 6) |
| Accent Amber | `#F59E0B` | BRE category badges only (Section 3) |

Full palette with rationale: see `visual-direction.md` Design System section.

## Score History

| Version | CMO (/100) | Brand Director (/10) | Key Change |
|---------|-----------|---------------------|------------|

## Human Feedback Log

| Date | Phase | Feedback |
|------|-------|----------|
| 2026-02-24 | 1 | Initial context: product page for Swimm platform. Audience: architect/tech lead. Scope: PMM to decide. |
| 2026-02-24 | 1 | Major revision: remove "gap" section, not dev/architect-centric, AI-forward positioning, marketecture in hero. |
| 2026-02-24 | 1 | Brief v3 approved. |
| 2026-02-24 | 2 | Content v1 feedback: "these are all big blocks of text" — sections read as paragraphs, not web copy. |
| 2026-02-24 | 2 | Content v2 feedback: "this needs to be a website, not a blog article" — requested structure specialist review. |
| 2026-02-24 | 2 | Structure review identified 5 problems: (1) same pattern repeated 9x, (2) multi-item content serialized as prose, (3) no interactive patterns, (4) copy-to-visual ratio inverted, (5) Sections 5+6 structurally identical despite being a unit. |
| 2026-02-24 | 2 | Content v3 approved — restructured as web page compositions with atomic visual blocks. Moving to Phase 3: Design. |
| 2026-02-24 | 3 | Visual direction v2 approved. Moving to Phase 4: Build. |
