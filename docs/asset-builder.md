# Asset Builder

The Asset Builder creates deep content assets - whitepapers, primers, solution guides, sales decks, and more - using a 3-phase gated process with human checkpoints.

## Quick Start

```
/asset new "Title" whitepaper     # Start a whitepaper project
/asset new "Title" primer         # Start a primer
/asset new "Title" sales-deck     # Start a sales deck
/asset                            # See active projects
/asset continue                   # Resume work
```

## Supported Asset Types

| Type | Format | Length | Description |
|------|--------|--------|-------------|
| `whitepaper` | Prose | 3000-6000 words | Data-driven thought leadership for executive/technical audiences |
| `primer` | Prose | 800-1500 words | 2-3 page overview for anyone new to a topic |
| `sales-deck` | Deck | 12-16 slides | B2B sales presentation with speaker notes |
| `solution-guide` | Prose | 2000-4000 words | Problem-first guide showing transformation path |
| `use-case-guide` | Prose | 1500-3000 words | Specific use case walkthrough |
| `competitive-comparison` | Prose | 1500-3000 words | Evaluation-criteria-led competitive positioning |
| `partner-brief` | Prose | 1000-2000 words | Partner-specific solution overview |
| `product-overview` | Prose | 1500-2500 words | Product capabilities and value proposition |
| `webinar-deck` | Deck | 20-30 slides | Educational presentation with speaker notes |

Templates for `whitepaper`, `primer`, and `sales-deck` are available now. Other types will be added incrementally.

## How It Works

### Agent-Per-Phase Architecture

Each phase runs as its own **top-level agent** with fresh context. Phases hand off via files on disk (`decisions.md`, `brief.md`, `content.md`) — no conversation context carries between phases. This prevents context compaction and quality degradation across a multi-hour asset project.

```
/asset new    → Dispatcher (gathers input, creates project, saves to decisions.md)
/asset continue → Phase 1 Agent → brief.md → HUMAN CHECKPOINT
/asset continue → Phase 2 Agent → content.md → HUMAN CHECKPOINT
/asset continue → Phase 3 Agent → review.md + revisions → HUMAN CHECKPOINT
```

### 3-Phase Workflow

**Phase 1: Brief** - Research the topic and produce a section-by-section outline. Loads PMM knowledge selectively based on the asset type. Human approves the outline before writing begins.

**Phase 2: Write** - Draft content section-by-section (or slide-by-slide for decks). Each section is written by a fresh subagent to prevent quality degradation. Anti-repetition protocol ensures each section advances the argument with new information.

**Phase 3: Review + Revise** - Two independent reviewers (asset-reviewer for quality, persona-reviewer for audience fit) provide feedback. User selects which items to address. Revisions are scoped to individual sections. Maximum 3 revision rounds.

### Key Design Decisions

- **Agent-per-phase isolation**: Each phase gets a fresh agent with clean context. The dispatcher (`/asset new`) gathers all user input into `decisions.md`, then each phase agent reads its inputs from disk. No conversation history carries between phases, eliminating compaction risk.
- **Section-by-section subagents**: Within Phase 2, each section gets a fresh subagent loaded with only what it needs. This prevents context rot (quality degradation in later sections) and keeps token usage manageable.
- **Per-section PMM loading**: The outline tags each section with which PMM knowledge files it needs. Only those files load into the writing subagent. A 6000-word whitepaper never needs all 200K tokens of PMM knowledge at once.
- **Writer/reviewer separation**: The reviewer reads the content cold in a fresh context, catching repetition and drift that the writing agent can't see in its own output.
- **Revision protocol**: Feedback is applied section-by-section via scoped subagents. The full document is never regenerated. Anchor documents (outline, template, decisions.md) stay loaded to prevent drift.

## File Structure

Each project lives in `content/assets/`. The `decisions.md` file is the sole handoff artifact between phases — it contains project context, phase status, and all decisions made:

```
content/assets/26Q1-whitepaper-claude-code-cobol/
  decisions.md       # State file + handoff baton (phase status, project context, revision history)
  brief.md           # Phase 1 output - approved outline
  content.md         # Phase 2 output - the asset itself
  review.md          # Phase 3 - reviewer feedback
```

## PMM Knowledge Integration

Asset content is enriched with product and market intelligence from the PMM researcher project. The path is configured via `PMM_KNOWLEDGE_PATH` in `data_sources/config/.env`.

Available knowledge includes:
- Product capabilities and technology (`config/teach_product_output.md`)
- Messaging framework and customer language (`knowledge_base/messaging/`)
- Buyer personas with real quotes (`knowledge_base/personas/`)
- Jobs to be done (`knowledge_base/jtbd/`)
- Competitive intelligence (`knowledge_base/competitive/`)
- Objection handling (`knowledge_base/sales_enablement/`)

## Adding a New Asset Type

1. Create a template file in `asset-builder/asset-types/[type].md`
2. Follow the pattern from existing templates (whitepaper.md, primer.md, or sales-deck.md)
3. Define: metadata, knowledge sources, section structure, formatting rules, post-write agents, quality checklist
4. The `/asset` command automatically picks up the new template - no command changes needed

## Related Files

- Command: `.claude/commands/asset.md`
- Templates: `asset-builder/asset-types/`
- Agents: `.claude/agents/asset-reviewer.md`, `.claude/agents/persona-reviewer.md`
- State template: `asset-builder/templates/decisions-template.md`
