# One-Pager Content

<!--
  HOW TO USE THIS FILE
  ────────────────────
  Fill in your content below. Claude will read this file and produce a
  brand-approved 2-page PDF that matches the Swimm design spec in BRIEF.md.

  WHAT YOU CONTROL HERE:
  - Product title and subtitle
  - Intro paragraph
  - Capability columns (headers + bullets)
  - Flow diagram steps
  - Logo bar entries
  - Back page: value, deployment, use cases, stats, security, CTA

  WHAT CLAUDE CONTROLS (do not override):
  - Colors, fonts, sizes, spacing — all from BRIEF.md
  - Layout and positioning of every zone
  - Illustration placeholder styling

  This is a FIXED 2-page document. Content must fit within each zone.
  If text overflows a zone, shorten it — do not add pages.

  Sections marked with ✏️ are editable.
  Sections marked with ℹ️ are documentation — read but don't change them.
-->

---
title: "Application Understanding Platform"
subtitle: "Instant clarity for your legacy and mainframe applications"
cta-text: "Learn more at swimm.io"
cta-url: "https://swimm.io/"
logo-bar: "Deloitte, Accenture, HCL, Optum"
---

<!--
  ℹ️ FRONT MATTER
  - title: Displayed large in the top-left header zone
  - subtitle: Displayed below the title in lighter weight
  - cta-text: Text on the back page CTA button
  - cta-url: Link target for the CTA button (non-interactive in PDF)
  - logo-bar: Comma-separated list of names shown in the bottom dark bar
-->


## Front Page

<!--
  ℹ️ FRONT PAGE ZONES
  The front page has 6 zones, each generated from the sections below.
  The illustration zone is auto-generated as a placeholder circle.
  Do not add extra sections — each maps to a fixed CSS zone.
-->

### Intro

Swimm transforms complex legacy codebases into clearly documented, easily navigable knowledge. Engineers gain instant understanding of COBOL, JCL, and mainframe applications without relying on tribal expertise or retiring SMEs.

<!--
  ℹ️ INTRO FORMAT
  2-3 sentences maximum. This zone is constrained to the left 52% of the page
  to avoid overlapping the illustration circle on the right.
-->

### Capabilities

**Analyze and map**
- Automatically scan and map application architectures
- Identify dependencies, data flows, and business rules
- Generate interactive system topology visualizations

**Understand what it does**
- AI-powered code explanations in plain English
- Business logic extraction from COBOL and JCL
- Cross-reference programs, copybooks, and JCL procs

**Prepare knowledge**
- Auto-generate living documentation from source code
- Create onboarding guides for new team members
- Export knowledge to your existing tools and wikis

<!--
  ℹ️ CAPABILITIES FORMAT
  Exactly 3 columns. Each column has:
  - A **bold header** (becomes the column heading with blue-feet background)
  - 3-4 bullet points (keep each to one line for best fit)
  More than 4 bullets per column risks overflow.
-->

### Flow

- 1 | Connect repo | Point Swimm at your source code repository
- 2 | Analyze code | AI scans and maps your entire codebase
- 3 | Generate docs | Living documentation created automatically
- 4 | Share knowledge | Teams access insights through familiar tools

<!--
  ℹ️ FLOW FORMAT
  Each bullet is: step-number | label | caption
  3-5 steps work best. Arrows are auto-generated between steps.
  Keep labels to 2-3 words and captions to one short sentence.
-->

---

## Back Page

<!--
  ℹ️ BACK PAGE ZONES
  The back page has 6 zones. Use cases and stats sit side-by-side.
  Security uses a 2-column grid. CTA is auto-generated from front matter.
-->

### Value

**Unlock the knowledge trapped in your legacy systems**

Organizations running mainframe applications face a critical knowledge crisis. As experienced developers retire, decades of institutional knowledge about complex COBOL systems walks out the door. Manual documentation efforts are slow, expensive, and outdated before they are finished.

Swimm solves this by using AI to automatically analyze, document, and explain legacy code. Teams gain instant clarity into what applications do, how they work, and why they were built that way — without waiting months for manual reverse-engineering.

<!--
  ℹ️ VALUE FORMAT
  A heading (bold text) followed by 1-3 paragraphs.
  This is the largest text zone on the back page (~18% height).
-->

### Deploy

**Deploy in hours, not months**

Swimm connects directly to your source code repositories with zero code changes required. The platform analyzes your codebase in the background, and teams can start querying documentation within hours of setup. No lengthy implementation projects, no professional services engagements, no disruption to existing workflows.

<!--
  ℹ️ DEPLOY FORMAT
  A heading (bold text) followed by 1-2 short paragraphs.
  Keep concise — this zone is ~12% of the page height.
-->

### Use Cases

- COBOL modernization
- Knowledge transfer
- Mainframe migration
- AI-assisted development
- Regulatory compliance
- Developer onboarding

<!--
  ℹ️ USE CASES FORMAT
  Simple bullet list. Each item becomes a rounded pill tag.
  6-8 items work well. Keep each to 2-3 words.
  This zone occupies the left half of the mid-page area.
-->

### Stats

- 79% | of modernization initiatives fail without proper documentation
- 3x | faster developer onboarding for legacy systems
- 2hrs | average time to deploy Swimm

<!--
  ℹ️ STATS FORMAT
  Each bullet is: value | label
  2-4 stats work best. Values can be numbers, percentages, or short strings.
  This zone occupies the right half of the mid-page area (beside Use Cases).
  Uses the same visual pattern as the whitepaper stat tiles but at smaller scale.
-->

### Security

- SOC 2 Type II certified
- On-premise deployment available
- Bring your own LLM (BYOLLM)
- ISO 27001 compliant
- No code leaves your environment
- Role-based access controls

<!--
  ℹ️ SECURITY FORMAT
  Simple bullet list. Each item gets a checkmark decorator.
  Items are laid out in a 2-column grid.
  4-6 items work well. Keep each to one line.
-->

### CTA

Learn more at swimm.io

<!--
  ℹ️ CTA FORMAT
  This text is for reference only. The actual CTA button text and URL
  come from the front matter fields cta-text and cta-url.
  The CTA renders as a centered button in a dark strip at the bottom.
-->
