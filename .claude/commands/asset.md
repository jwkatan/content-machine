# Asset Builder Command

Create deep content assets: whitepapers, primers, solution guides, sales decks, and more. 3-phase gated process with human checkpoints at every transition. Section-by-section writing with subagent isolation for quality.

## Architecture: Agent-Per-Phase

Each phase runs as its own **top-level agent** with fresh context. Phases hand off via files on disk — no conversation context carries between phases.

```
/asset new → Dispatcher (gathers input, creates project, saves to decisions.md)
                ↓ user runs /asset continue
Phase 1 Agent → Reads decisions.md + template + PMM → Produces brief.md → HUMAN CHECKPOINT
                ↓ user runs /asset continue
Phase 2 Agent → Reads decisions.md + brief.md + template → Writes content.md section-by-section → HUMAN CHECKPOINT
                ↓ user runs /asset continue
Phase 3 Agent → Runs agent reviewers → HUMAN REVIEW → (feedback? → revise → re-run agents → HUMAN REVIEW) → User approves
```

**Key rule**: Each phase agent reads ALL context from disk. It never relies on prior conversation. It updates `decisions.md` at checkpoints, then stops. The user runs `/asset continue` to spawn the next phase.

## Usage

```
/asset                              # Dashboard: see active asset projects + status
/asset new "[Title]" [type]         # Start a new asset project
/asset continue                     # Resume work on active project
```

**Asset types**: `whitepaper`, `solution-guide`, `primer`, `use-case-guide`, `competitive-comparison`, `partner-brief`, `product-overview`, `sales-deck`, `webinar-deck`

## Subcommands

### Dashboard (no arguments)

1. Scan `content/assets/` for project folders
2. For each, read `decisions.md` to get current phase and status
3. Display active projects with phase progress and quick actions
4. If no projects exist, show "No active projects" with example `/asset new` command

---

### New (`/asset new "[Title]" [type]`)

**Dispatcher only** — gathers input and saves state. Does NOT start writing. User runs `/asset continue` to begin Phase 1.

**Process:**

1. **Validate asset type** against the supported list. If unrecognized, ask the user.

2. **Derive folder name**: `[YYQ#]-[asset-type]-[topic-slug]`. Ask user to confirm.

3. **Load asset type template** from `asset-builder/asset-types/[type].md`. If missing, stop.

4. **Create project**: `content/assets/[folder-name]/decisions.md` initialized from `asset-builder/templates/decisions-template.md` with project title, asset type, format, and date. Ask user to confirm or override persona(s).

5. **Resolve PMM knowledge path**: Read `PMM_KNOWLEDGE_PATH` from `data_sources/config/.env`. If not set, auto-detect `../marketing-pmm`. If neither found, ask user.

6. **Gather initial context** and save to `## Project Context` in `decisions.md`:
   - Target audience and their current situation
   - Key messages or arguments to make
   - Source material file paths (articles, research briefs, topic ideas, data)
   - Specific competitors or use cases (if applicable)
   - Gated or ungated?

7. Set Phase 1 status to "ready" in `decisions.md`. Confirm to user.

**IMPORTANT**: Do NOT start Phase 1 inline. The dispatcher's job is to gather and persist context, not to generate content.

---

### Continue (`/asset continue`)

1. Scan `content/assets/` for projects
2. If one project → read `decisions.md` → resume at current phase
3. If multiple → show dashboard, ask user to specify
4. **Spawn the appropriate phase agent** (see below)

---

## Phase Agents

Each phase is a **Task agent** (subagent_type: `general-purpose`) spawned with: phase instructions, project folder path, PMM knowledge path, and asset type.

### Model Selection

Opus for quality-critical work (writing prose, critical review). Sonnet for everything else (coordination, structured tasks, revisions).

| Role | Model |
|------|-------|
| Phase 1 agent + redundancy check | **sonnet** |
| Phase 2 orchestrator | **sonnet** |
| Phase 2 writing subagents | **opus** |
| Phase 3 orchestrator | **sonnet** |
| Phase 3 asset-reviewer + persona-reviewer | **opus** |
| Phase 3 revision subagents | **sonnet** |
| Post-processing (linkedin, newsletter, linker) | **sonnet** |

### Spawn Template

```
"You are the Phase [N] agent for the Asset Builder.

Project folder: content/assets/[folder-name]/
Asset type: [type]
PMM knowledge path: [resolved path]

YOUR INSTRUCTIONS:
[paste the full phase instructions from below]

START by reading: decisions.md, asset type template, brand-voice.md, style-guide.md, [+ phase-specific files]

Execute the phase workflow. At HUMAN CHECKPOINT, update decisions.md and present output to the user."
```

---

### Phase 1: BRIEF (Research + Outline)

**Goal**: Section-by-section outline approved by user before any writing begins.

**Files to read**: `decisions.md`, `asset-builder/asset-types/[type].md`, `context/brand-voice.md` (Part 1 always; Part 2 if Swimm is subject), `context/style-guide.md`, `context/features.md` (if product referenced), all PMM knowledge files from template's Knowledge Sources table, source material files from Project Context.

**Process:**

1. **Read all input files.** Project Context in `decisions.md` has user's goals, audience, key messages, and source material paths.

2. **Research**: Read source material thoroughly. Identify core argument, map evidence, flag knowledge gaps.

3. **Produce outline** → save as `brief.md`. For each section in the template:
   - Section title and number
   - Purpose (from template)
   - Key messages (2-4 bullets)
   - Evidence/data to include
   - PMM knowledge tags (for per-section loading in Phase 2)
   - Word count target
   - Connections to adjacent sections

   For decks: slide-by-slide with headline drafts and bullet sketches.

4. **Redundancy check** (subagent, sonnet): read all outlines in sequence, flag overlapping sections, verify progressive narrative arc.

5. **Update decisions.md**: Phase 1 "complete - pending approval", list PMM files loaded, key decisions.

6. **HUMAN CHECKPOINT**: Present outline.
   - Approve → Phase 1 "approved", Phase 2 "ready". Tell user `/asset continue`.
   - Revise → Update and re-present (max 3 rounds).

---

### Phase 2: WRITE (Section-by-Section Drafting)

**Goal**: Draft the complete asset one section at a time with quality checks between sections.

**Files to read**: `decisions.md`, `brief.md`, `asset-builder/asset-types/[type].md`, `context/brand-voice.md`, `context/style-guide.md`

**Anchor documents** (keep loaded throughout): asset type template, `brief.md`, `decisions.md`, `brand-voice.md`, `style-guide.md`

**CRITICAL: One section at a time via subagents.** Each section gets fresh context to prevent quality degradation.

#### For Prose Assets

##### Per-Section Cycle

**Step 1 — Write (subagent, opus).** Load: `brief.md` (full), asset type template, brand voice + style guide, all prior sections (read-only), PMM knowledge tagged for THIS section only. Instruct: "Identify claims in prior sections. Do not restate. Advance with NEW information."

**Step 2 — Context review.** Read all sections in sequence. Check: opening connects to previous close? Redundancy or contradiction? Consistent tone? If flow breaks → revise before proceeding.

**Step 3 — Accept.** Append to `content.md`. Update `decisions.md` progress.

**Executive Summary** (whitepapers): written LAST. It synthesizes, not previews.

##### After all sections:

1. Run scrubber: `.venv/bin/python -c "from data_sources.modules.content_scrubber import scrub_file; print(scrub_file('content/assets/[folder]/content.md'))"`
2. Update `decisions.md`: Phase 2 "complete - pending approval", section count, word count.
3. **HUMAN CHECKPOINT**: Present draft. Approve → Phase 2 "approved", Phase 3 "ready". Revise → apply via Revision Protocol, re-present.

#### For Deck Assets

##### Per-Slide Cycle

**Step 1 — Write (subagent, opus).** Load: `brief.md`, asset type template, brand voice + style guide, prior slides, PMM for this slide. Instruct: "Headlines 8-12 words. Bullets 10-15 words. Speaker notes 50-150 words."

**Step 2 — Narrative arc check.** Headlines build a story? Speaker notes transition naturally? Density appropriate?

**Step 3 — Accept.** Append to `content.md`. Update `decisions.md`.

##### After all slides:

1. Run scrubber. **Headline story test**: headlines alone should tell the complete story.
2. Update `decisions.md`: Phase 2 "complete - pending approval".
3. **HUMAN CHECKPOINT**: same as prose.

---

### Phase 3: REVIEW + REVISE + FINALIZE

**Goal**: Agent review, user review, revision loop until user approves.

**Files to read**: `decisions.md`, `content.md`, `brief.md`, `asset-builder/asset-types/[type].md`, `context/brand-voice.md`, `context/style-guide.md`

**CRITICAL**: The asset is NEVER marked complete until the user explicitly approves. Agent review completion ≠ project completion.

#### Step 1: Agent Review

1. **Asset-reviewer** (subagent, opus): Load `content.md`, template, `brief.md`. Instructions: `.claude/agents/asset-reviewer.md`. Save as `review.md`.
2. **Persona-reviewer** (subagent, opus): Load `content.md`, `brief.md`, persona file from `$PMM_KNOWLEDGE_PATH/knowledge_base/personas/[persona].md`. Instructions: `.claude/agents/persona-reviewer.md`. Append to `review.md`. Run one per target persona.
3. Present agent feedback. Update decisions.md: "Agent review round N complete — awaiting user review."

#### Step 2: User Review (HUMAN CHECKPOINT)

Present content to user. User decides:
- **Approve** → Phase 3 "approved", project "complete". Proceed to post-processing.
- **Feedback** → Proceed to Step 3.

#### Step 3: Revise

Apply user feedback via Revision Protocol (below).

#### Step 4: Re-review Loop

Return to Step 1. Loop until user approves (max 3 rounds).

#### After User Approval

1. **Optional post-processing** (ask user, all sonnet): `linkedin-repurposer`, `newsletter-repurposer`, `internal-linker` (only if publishing online).
2. **Optional PDF generation** (ask user): For prose assets, offer branded PDF output. Requires a PDF-format `content.md` (see `pdf-builder/templates/{type}/content-sample.md` for format). Run: `.venv/bin/python -c "from data_sources.modules.pdf_builder import generate_pdf; print(generate_pdf('path/to/content.md', 'path/to/output.pdf', 'whitepaper'))"`. Update `decisions.md` PDF Output section with result.
3. Update `decisions.md`: final status, revision history.
4. Report: asset type, word count, sections, review rounds, file list.

---

## Revision Protocol

Prevents drift when applying feedback from reviewers or user.

1. **Scoped edits, not full rewrites.** Target individual sections only.

2. **Revision subagents (sonnet).** Each gets: `brief.md` (anchors intent), asset type template (anchors tone), full `content.md` (read-only context), only feedback for THIS section. Returns revised section text only.

3. **Splice and log.** Replace section in `content.md`. Log in `decisions.md` Revision History: round, phase, sections changed, feedback source, summary.

4. **Diff-based re-review.** Reviewers see only changed sections (before/after), not the full document.

5. **3-round cap.** Escalate to user if issues persist.

6. **Anchor documents stay loaded.** Phase agent always holds: `brief.md`, `decisions.md`, asset type template. Heavy content stays in subagent contexts.

---

## PMM Knowledge Path

Resolve from `PMM_KNOWLEDGE_PATH` in `data_sources/config/.env`. Fallback: auto-detect `../marketing-pmm`. If neither found, ask user.

## Forward-Looking Guardrail

Always verify product claims against `$PMM_KNOWLEDGE_PATH/config/teach_product_output.md`. Do not present roadmap items or aspirational features as shipped functionality.
