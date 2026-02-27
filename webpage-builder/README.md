# Webpage Builder

Multi-agent collaborative system for building production-quality web pages.

## Quick Start

```
/webpage                        # Dashboard: see active projects + status
/webpage new "Page Name"        # Start a new page project
/webpage continue               # Resume work on active project
```

## How It Works

6-phase process with human checkpoints at every transition:

1. **Brief** — PMM + CMO define messaging strategy
2. **Content** — Writer + Editor draft section copy, PMM reviews alignment
3. **Design** — Designer + Brand Director create visual direction
4. **Build** — Engineer builds self-contained HTML, Designer reviews each section
5. **Review** — CMO (scores /100) + Brand Director (scores /10) evaluate, Engineer iterates
6. **Finalize** — Tests pass, images uploaded, stable copy saved

7 AI agents with different viewpoints collaborate and converge toward better outcomes. Agent-to-agent loops are capped at 3 iterations before requesting human input.

## Adding Page Types

Add a new markdown file to `page-types/` defining section structure and rules. Current types:
- `homepage.md` — Homepage with hero, value prop, capabilities, credibility, CTA

Planned:
- `product.md` — Product pages
- `usecase.md` — Use case pages

## Project Structure

Each project in `projects/` follows this structure:

```
projects/swimm-homepage-2026/
├── decisions.md              # State, decisions, score history
├── brief.md                  # Messaging brief (Phase 1)
├── content.md                # Section copy (Phase 2)
├── visual-direction.md       # Design specs (Phase 3)
├── src/
│   ├── index.html            # Active build
│   └── index-stable.html     # Last approved version
└── tests/
    ├── package.json
    └── responsiveness.spec.js
```

## Naming Convention

Project folders: `[company-or-product]-[page-type]-[identifier]`

Examples: `swimm-homepage-2026`, `cobol-modernization-usecase`, `application-understanding-product`
