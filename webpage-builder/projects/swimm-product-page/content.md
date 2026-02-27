# Swimm Product Page — Content v3

> **Status**: Restructured from prose to web page compositions
> **Date**: 2026-02-24
> **Structural approach**: Each section specifies atomic visual blocks, not paragraphs. Copy is composed as labels, callouts, and annotations — not article text.

---

## Section 1: Hero + Marketecture

**Pattern**: Full-width hero. Text anchors left, marketecture visual dominates right/below.

```
┌─────────────────────────────────────────────────────────────────┐
│  [dark/gradient background, full-width]                         │
│                                                                 │
│  H1: One understanding layer.                                   │
│      For your team and your AI.                                 │
│                                                                 │
│  Subline: Accurate, code-derived understanding                  │
│  of how your applications behave.                               │
│                                                                 │
│  Two-phrase pair (smaller text, muted):                          │
│    Your team navigates and governs it.                          │
│    AI agents consume and execute from it.                       │
│                                                                 │
│  [CTA button: See it on your code]                              │
│                                                                 │
│              [ MARKETECTURE SVG ]                               │
│        Code in → Engine → Capabilities → Delivery               │
│        (this visual IS the hero — 60%+ of section area)         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Section 2: Application Map

**Pattern**: Headline + one-liner → 3-column persona card row → full-width product screenshot → Swimm Assistant mini-callout

```
┌─────────────────────────────────────────────────────────────────┐
│  [light background]                                             │
│                                                                 │
│  H2: Your entire application, navigable in business language    │
│  Subline: Millions of lines of code, organized into browsable   │
│  business domains.                                              │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ [Scope icon]  │  │ [Process icon]│  │ [Code icon]  │          │
│  │               │  │               │  │               │          │
│  │ Modernization │  │ Business      │  │ Engineers     │          │
│  │ leads         │  │ analysts      │  │              │          │
│  │               │  │               │  │              │          │
│  │ See the full  │  │ Navigate to   │  │ Drill from   │          │
│  │ scope         │  │ processes and │  │ domain to    │          │
│  │               │  │ business rules│  │ source code  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────┐        │
│  │          [ APPLICATION MAP SCREENSHOT ]              │        │
│  │   Domain view with business-named domains,           │        │
│  │   process counts, drill-down navigation              │        │
│  │   (screenshot takes 60%+ of section width)           │        │
│  └─────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌──── Swimm Assistant callout (small, anchored to screenshot) ─┐│
│  │ [chat icon] Ask anything in natural language.                ││
│  │ Swimm Assistant — built into the web experience.             ││
│  └──────────────────────────────────────────────────────────────┘│
│                                                                 │
│  Feature pills (small, secondary):                              │
│  [AI summaries] [Dependency graphs] [Business context]          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Section 3: Business Rules & Flows

**Pattern**: Headline → tabbed interface (2 tabs swap copy + screenshot) → persona callout bar

```
┌─────────────────────────────────────────────────────────────────┐
│  [light background, subtle contrast from Section 2]             │
│                                                                 │
│  H2 (centered): Business rules and execution paths              │
│                  — extracted at unlimited depth                  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐       │
│  │ [TAB: Business Rules]  |  [TAB: Execution Paths]     │       │
│  │──────────────────────────────────────────────────────│       │
│  │                                                      │       │
│  │  TAB 1 (active):                                     │       │
│  │  LEFT (40%):                        RIGHT (60%):     │       │
│  │                                                      │       │
│  │  Subheadline:                       [SCREENSHOT:     │       │
│  │  Extracted automatically            Business rules   │       │
│  │  in plain English                   table with       │       │
│  │                                     categories]      │       │
│  │  Category badges:                                    │       │
│  │  [Input] [Calculation]                               │       │
│  │  [Invoking] [Output]                                 │       │
│  │                                                      │       │
│  │  One-liner:                                          │       │
│  │  Traceable to the source                             │       │
│  │  code they were derived from                         │       │
│  │                                                      │       │
│  │──────────────────────────────────────────────────────│       │
│  │                                                      │       │
│  │  TAB 2:                                              │       │
│  │  LEFT (40%):                        RIGHT (60%):     │       │
│  │                                                      │       │
│  │  Subheadline:                       [SCREENSHOT:     │       │
│  │  Entry point to exit.               Flow graph or    │       │
│  │  Every call chain.                  code walkthrough │       │
│  │  Unlimited depth.                   with interleaved │       │
│  │                                     prose + code]    │       │
│  │  One-liner:                                          │       │
│  │  Traced across every                                 │       │
│  │  dependency in the application                       │       │
│  │                                                      │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                 │
│  PERSONA CALLOUT BAR (3-column, centered, smaller text):        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Business      │  │ Engineers    │  │              │          │
│  │ analysts:     │  │ see the      │  │ One source   │          │
│  │ rules in      │  │ complete     │  │ of truth.    │          │
│  │ their language│  │ technical    │  │              │          │
│  │               │  │ picture      │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Section 4: Glossary & Collections

**Pattern**: Headline → split block (Glossary left, Collections right) → bridge statement → mid-page CTA

```
┌─────────────────────────────────────────────────────────────────┐
│  [light background]                                             │
│                                                                 │
│  H2 (centered): Code knowledge meets organizational knowledge   │
│                                                                 │
│  ┌──────────────────────┐    ┌──────────────────────┐           │
│  │ GLOSSARY             │    │ COLLECTIONS          │           │
│  │                      │    │                      │           │
│  │ [Glossary visual:    │    │ [Collections visual: │           │
│  │  code name →         │    │  wiki-style content  │           │
│  │  business term       │    │  with edit cursor    │           │
│  │  transformation]     │    │  and Mermaid diagram]│           │
│  │                      │    │                      │           │
│  │ Cryptic variable     │    │ Editable, goal-      │           │
│  │ names become business│    │ oriented deliverables │           │
│  │ terms automatically. │    │ where SMEs annotate,  │           │
│  │                      │    │ correct, and enrich   │           │
│  │ Feeds into every     │    │ with context that     │           │
│  │ feature — flows,     │    │ only exists in        │           │
│  │ rules, walkthroughs  │    │ people's heads.       │           │
│  │ all use your         │    │                      │           │
│  │ organization's       │    │                      │           │
│  │ language.            │    │                      │           │
│  └──────────────────────┘    └──────────────────────┘           │
│                                                                 │
│  Bridge statement (centered, smaller, transitional):            │
│  What your team verifies and governs becomes                    │
│  the trusted context AI consumes next.                          │
│                                                                 │
│  [CTA ghost button: See how it works]                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Section 5: Context for AI

**Pattern**: Full-width dark background. Centered headline → stat pair → 3-step process row → declaration → product visual. **Begins the 5+6 paired unit.**

```
┌─────────────────────────────────────────────────────────────────┐
│  [dark/gradient background — visual break, begins 5+6 unit]     │
│                                                                 │
│  H2 (centered, light text):                                     │
│  The trusted context AI agents rely on                          │
│  for forward engineering                                        │
│                                                                 │
│  Subline (centered, muted):                                     │
│  AI coding assistants access the same verified understanding    │
│  your team relies on — via MCP.                                 │
│                                                                 │
│  STAT PAIR (large accent numbers, centered):                    │
│  ┌────────────────────┐    ┌────────────────────┐               │
│  │       75%          │    │       61%          │               │
│  │  response time     │    │  cost savings      │               │
│  │  savings           │    │  efficient tokens  │               │
│  └────────────────────┘    └────────────────────┘               │
│  Fine print: Benchmarked with Claude Code                       │
│                                                                 │
│  3-STEP PROCESS (horizontal, connected dots/line):              │
│  ●─────────────────●─────────────────●                          │
│  Generate          Connect any       Verified context           │
│  API key           MCP-compatible    flows to your agents       │
│                    AI tool                                      │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐           │
│  │  [PRODUCT VISUAL: MCP config or Swimm Assistant  │           │
│  │   chat showing a grounded answer — concrete]      │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                 │
│  DECLARATION (pull quote typography, centered):                 │
│  One understanding layer.                                       │
│  Consistent context for humans and AI.                          │
│  This is how the future of engineering works.                   │
│                                                                 │
└── dark background continues into Section 6 ─────────────────────┘
```

---

## Section 6: Human Governance & Control

**Pattern**: Continues dark background from Section 5. Headline → 5-column icon grid → deterministic callout → closing declaration → CTA. **Completes the 5+6 unit.**

```
┌── dark background continues from Section 5 ─────────────────────┐
│                                                                 │
│  H2 (centered, light text):                                     │
│  Human governance. Your team controls what AI consumes.         │
│                                                                 │
│  GOVERNANCE GRID (5-column icon row):                           │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐             │
│  │[icon]│  │[icon]│  │[icon]│  │[icon]│  │[icon]│             │
│  │      │  │      │  │      │  │      │  │      │             │
│  │Trace-│  │Fresh-│  │ SME  │  │Edit- │  │Deter-│             │
│  │ability│  │ness  │  │Verify│  │ability│  │minis-│             │
│  │      │  │      │  │      │  │      │  │tic   │             │
│  │Every │  │Analy-│  │Experts│  │Your  │  │No in-│             │
│  │insight│  │sis   │  │verify│  │team  │  │ference│             │
│  │traces│  │matches│  │and   │  │con-  │  │No hal-│             │
│  │to    │  │current│  │approve│  │trols │  │lucina-│             │
│  │source│  │code   │  │      │  │the   │  │tion   │             │
│  │code  │  │version│  │      │  │knowl-│  │      │             │
│  │      │  │      │  │      │  │edge  │  │      │             │
│  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘             │
│                                                                 │
│  CLOSING DECLARATION (matching Section 5's pull quote style):   │
│  Human governance, AI execution —                               │
│  sharing the same trusted foundation.                           │
│                                                                 │
│  [CTA ghost button, light: Talk to our team]                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Section 7: How It Works

**Pattern**: Headline → horizontal pipeline diagram where copy IS the labels → trust statement below

```
┌─────────────────────────────────────────────────────────────────┐
│  [light background — visual break from dark 5+6 unit]           │
│                                                                 │
│  H2 (centered): Deterministic analysis. AI translation.         │
│                  One engine.                                    │
│                                                                 │
│  PIPELINE DIAGRAM (horizontal, annotated):                      │
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ CODE IN  │───>│ STATIC   │───>│STRUCTURAL│───>│   AI     │  │
│  │          │    │ ANALYSIS │    │  GRAPH   │    │TRANSLATE │  │
│  │Uncompiled│    │Determin- │    │Call chains│    │Your LLM  │  │
│  │source    │    │istic     │    │Dependen- │    │turns     │  │
│  │code      │    │parsing   │    │cies      │    │structure │  │
│  │          │    │          │    │Data xform│    │into      │  │
│  │          │    │          │    │Unlimited │    │business  │  │
│  │          │    │          │    │depth     │    │language  │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                                 │
│  Secondary detail pills (below pipeline):                       │
│  [21+ languages] [Mainframe-first] [No compilation]             │
│  [No mainframe access] [Plugin-based] [Your own LLM]            │
│                                                                 │
│  TRUST STATEMENT (centered, smaller text):                      │
│  The engine discovers structure. AI makes it readable.          │
│  The outputs are trustworthy because the foundation is factual. │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Section 8: Enterprise Readiness

**Pattern**: Headline → 2-row icon/badge grid. No prose.

```
┌─────────────────────────────────────────────────────────────────┐
│  [light background]                                             │
│                                                                 │
│  H2 (centered): Your environment. Your LLM. Your perimeter.    │
│                                                                 │
│  ROW 1: Deployment & Security                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ ┌──────────┐ │
│  │ [server icon] │  │ [LLM icon]   │  │ [SOC 2   │ │ [ISO     │ │
│  │               │  │               │  │  badge]  │ │  27001   │ │
│  │ Fully         │  │ Your LLM:    │  │          │ │  badge]  │ │
│  │ on-premise    │  │ Azure OpenAI │  │          │ │          │ │
│  │               │  │ OCI          │  │          │ │          │ │
│  │ No code leaves│  │ Bedrock      │  │          │ │          │ │
│  │ your network  │  │               │  │          │ │          │ │
│  └──────────────┘  └──────────────┘  └──────────┘ └──────────┘ │
│                                                                 │
│  ROW 2: Languages & Integrations                                │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  LANGUAGE LOGO GRID (21+ languages):                  │       │
│  │  [COBOL] [PL/I] [JCL] [Assembler] [RPG]              │       │
│  │  [Java] [C/C++] [C#] [Python] [Go] [+more]           │       │
│  │  Label: 21+ languages, mainframe-first                │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐                     │
│  │ [plugin icon]     │  │ [IDE icons]      │                     │
│  │ Plugin-based      │  │ VS Code          │                     │
│  │ extensibility for │  │ Visual Studio    │                     │
│  │ customer-specific │  │ JetBrains        │                     │
│  │ parsing           │  │ Bidirectional    │                     │
│  │                   │  │ code linking     │                     │
│  └──────────────────┘  └──────────────────┘                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Section 9: Conversion

**Pattern**: Full-width, dark background (mirrors hero). Centered. Minimal.

```
┌─────────────────────────────────────────────────────────────────┐
│  [dark/gradient background — bookends with hero]                │
│                                                                 │
│  H2 (centered, light text):                                     │
│  See Swimm on your code                                        │
│                                                                 │
│  Subline (centered, muted):                                     │
│  One understanding layer for your modernization team            │
│  and your AI tools.                                             │
│                                                                 │
│  [CTA button, large, brand color: See Swimm on your code]      │
│                                                                 │
│  Friction reducer (small text below button):                    │
│  Free evaluation on your codebase                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Structural Summary

| # | Section | Pattern | Background | Key Blocks |
|---|---------|---------|------------|------------|
| 1 | Hero | Text left + SVG dominant | Dark | H1 + subline + phrase pair + CTA + marketecture |
| 2 | App Map | Cards + screenshot + callout | Light | 3-col persona cards + full screenshot + Swimm Assistant callout + feature pills |
| 3 | BRE+Flows | Tabbed interface | Light | 2 tabs (copy + screenshot each) + persona callout bar |
| 4 | Glossary+Collections | Split block | Light | 2-col feature split + bridge statement + CTA |
| 5 | Context for AI | Stat pair + process + declaration | Dark | Stats + 3-step process + visual + pull quote |
| 6 | Governance | Icon grid + declaration | Dark (continues) | 5-col icon grid + closing declaration + CTA |
| 7 | How It Works | Annotated pipeline | Light | 4-stage pipeline diagram + detail pills + trust statement |
| 8 | Enterprise | Badge/icon grid | Light | 2-row grid (deploy+security, languages+integrations) |
| 9 | Conversion | Centered CTA | Dark | H2 + subline + button + friction reducer |

### Visual Rhythm
Dark → Light → Light → Light → **Dark → Dark** → Light → Light → Dark

### Structural Variety
- Cards (Section 2)
- Tabs (Section 3)
- Split blocks (Section 4)
- Stat pairs + process indicators (Section 5)
- Icon grid (Section 6)
- Annotated pipeline (Section 7)
- Badge grid (Section 8)

No two consecutive sections use the same pattern.

---

## Headline Story Arc

1. One understanding layer. For your team and your AI.
2. Your entire application, navigable in business language
3. Business rules and execution paths — extracted at unlimited depth
4. Code knowledge meets organizational knowledge
5. The trusted context AI agents rely on for forward engineering
6. Human governance. Your team controls what AI consumes.
7. Deterministic analysis. AI translation. One engine.
8. Your environment. Your LLM. Your perimeter.
9. See Swimm on your code

---

## CTA Placement

| Position | CTA Text | Style |
|----------|----------|-------|
| Section 1 (Hero) | See it on your code | Filled button, brand color |
| After Section 4 | See how it works | Ghost/outlined button |
| After Section 6 | Talk to our team | Ghost/outlined, light (dark bg) |
| Section 9 (Conversion) | See Swimm on your code | Filled button, larger |
