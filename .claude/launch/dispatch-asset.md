# Dispatch: /asset pillars

When the user starts work on an `/asset` brief (whitepapers, decks, emails, video scripts, etc.).

## Process

### Step 1 — Read the PMM brief

Read `[PMM_PATH]/launches/[slug]/briefs/[brief-file].md`. This contains:
- Asset Specification (type, format, audience, length, distribution)
- Approved Launch Messaging (positioning, value prop, pillars, say this/not this)
- Asset-Specific Guidance (role in narrative, key messages, medium-specific, cross-references)
- Evidence to Include (pain points with quotes, proof points, competitive context)
- PMM Knowledge to Load (file paths)

### Step 2 — Read the messaging framework

Read `[PMM_PATH]/launches/[slug]/strategy/messaging-framework-llm-optimized.md`.

### Step 3 — Create the project folder and decisions.md

This step replaces `/asset new` — the launch command IS the dispatcher.

**Output path**: `content/launches/[launch-slug]/[pillar-slug]/`

For multi-deliverable pillars, nest: `content/launches/[launch-slug]/[pillar-slug]/[sub-task-slug]/`

Create `decisions.md` from `asset-builder/templates/decisions-template.md`, populated as follows:

```markdown
# [PMM Brief Title] — Decisions & Status

## Status

- **Asset type**: [from brief's Asset Specification → Type]
- **Format**: [from brief's Asset Specification → Format]
- **Target audience**: [from brief's Asset Specification → Target audience]
- **Current phase**: Phase 1: Brief
- **Created**: [today's date]
- **Last updated**: [today's date]
- **Launch**: [launch-slug] (brief #[N])

## Phase History

| Phase | Status | Approved | Notes |
|-------|--------|----------|-------|
| 1. Brief | ready | — | PMM brief provides strategic input; Phase 1 adds structural outline |
| 2. Write | — | — | — |
| 3. Review | — | — | — |

## Project Context

- **Target audience**: [from brief's Asset Specification → Target audience + brief's Audience Adaptation section]
- **Key messages**: [from brief's Approved Launch Messaging → Messaging Pillars, verbatim]
- **Source material**:
  - PMM launch brief: [absolute path to the brief file]
  - Messaging framework: [absolute path to messaging-framework-llm-optimized.md]
  - [Each file from the brief's PMM Knowledge to Load table, with full paths resolved from $PMM_KNOWLEDGE_PATH]
- **Competitors/use cases**: [from brief's Evidence to Include → Competitive context, if any]
- **Gated or ungated**: [from brief if specified; otherwise ask user]
- **Distribution**: [from brief's Asset Specification → Distribution]
- **Additional notes**: [from brief's Asset-Specific Guidance → Role in Launch Narrative]

## Launch Messaging Constraints

**CRITICAL: These are hard constraints for all phases. Do not deviate, paraphrase, or reinterpret.**

### Positioning Statement
[Verbatim from brief's Approved Launch Messaging → Positioning Statement]

### Value Proposition
[Verbatim from brief's Approved Launch Messaging → Value Proposition]

### Messaging Pillars
[Verbatim from brief's Approved Launch Messaging → Messaging Pillars with all proof points]

### Say This / Not This
[Verbatim from brief's Approved Launch Messaging → Say This / Not This]

### Constraint Instructions
- Phase 1: Produce a section-by-section outline that structures these messages into the asset type template format. Do not introduce new positioning angles. Do not reinterpret the approved messaging. The outline structures HOW to say it — the messaging above defines WHAT to say.
- Phase 2: Write content that stays within these messaging boundaries. Use the evidence provided in the brief. Do not add unsourced claims or invent new proof points.
- Phase 3 reviewers: Flag any deviation from the Say This / Not This rules.

## Evidence Provided

[From brief's Evidence to Include section — pain points with verbatim quotes, proof points, competitive context, customer language]

## Cross-Reference Placeholders

[From brief's Cross-References section — list each referenced launch asset with its tracker status]
- "[Asset name]" (#[brief number]) — Status: [from tracker]. Output: [path if complete, "pending" if not]

## Key Decisions

[Tracked as decisions are made. Each entry includes rationale and what drove it.]

## PMM Knowledge Loaded

[List each file from the brief's PMM Knowledge to Load table]

## Human Feedback Log

[Captured at each checkpoint.]
```

### Step 4 — Update tracker

Set status to `in progress`, output path to the project folder.

### Step 5 — Proceed based on engagement level

The engagement level was chosen when the user ran `/launch work [N]` (see `.claude/launch/agent-pipeline.md`).

- **Collaborative**: Tell user: "Project initialized from launch brief #[N]. Run `/asset continue` to start Phase 1 (structure review)."
- **Guided**: Proceed directly through Phase 1 (structure) autonomously, then pause at Phase 2 (draft) for user review. Tell user: "Structure complete. Run `/asset continue` to review the draft."
- **Autonomous**: Proceed through Phase 1 and Phase 2 autonomously with agent reviews. Pause at Phase 3 (final) for user sign-off. Tell user: "Draft complete with agent reviews. Run `/asset continue` to review the final version."

For complex assets (webinar-deck, video-script, sales-deck), offer the flow/sequence checkpoint regardless of engagement level (see `.claude/launch/agent-pipeline.md`).

## Manual pillars (Whitepaper Updates)

1. **Read the PMM brief** for update guidance (which messaging to align, what to change).
2. **Identify the whitepaper to update** using the content library:
   ```python
   from data_sources.modules.content_library import search
   print(search('[whitepaper title]'))
   ```
3. **Checkout** for editing:
   ```python
   from data_sources.modules.content_library import checkout
   print(checkout('[slug]'))
   ```
4. **Apply updates** following the brief's guidance, constrained by the messaging framework.
5. **Checkin** (with user confirmation for push):
   ```python
   from data_sources.modules.content_library import checkin
   print(checkin('[slug]', push=True))
   ```
6. **Update tracker.**
