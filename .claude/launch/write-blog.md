# Launch Blog Writing

Self-contained process for writing launch blog posts. Does NOT invoke `/write`. Has its own structure, quality standards, and review agents.

## When This Runs

The coordinator dispatches here for Blog Post, Technical Blog Post, and Sponsored Content pillars. This file provides the structure and format rules; the cornerstone process (`.claude/launch/cornerstone.md`) or engagement level (`.claude/launch/agent-pipeline.md`) controls the checkpoint flow.

## Output Path

All files go to `content/launches/[launch-slug]/[pillar-slug]/`:
- `decisions.md`
- `research-brief.md`
- `[slug]-[YYYY-MM-DD].md` (the article)
- `[slug]-pre-edit-[YYYY-MM-DD].md` (pre-editor snapshot for before/after comparison)
- `messaging-drift-check.md`
- `cmo-review.md`
- `persona-review-[persona].md` (one per target persona)
- `argument-review.md`
- `cross-pillar-links.md`

---

## Checkpoint 1: Structure

### Step 1 — Read the PMM brief + messaging framework

Read `[PMM_PATH]/launches/[slug]/briefs/[brief-file].md` and `[PMM_PATH]/launches/[slug]/strategy/messaging-framework-llm-optimized.md`.

### Step 2 — Create the project folder

Create `content/launches/[launch-slug]/[pillar-slug]/`.

### Step 3 — Create decisions.md

```markdown
# [PMM Brief Title] — Decisions & Status

## Article Info
- **Topic**: [from brief]
- **Launch Content Format**: [announcement | technical-deep-dive]
- **Target audience**: [from brief]
- **Launch**: [launch-slug] (brief #[N])
- **Created**: [today's date]
- **Last updated**: [today's date]

## Current Status
- [ ] Research brief created
- [ ] Pre-writing reads complete
- [ ] First draft written
- [ ] Content scrubber run
- [ ] Editor agent run
- [ ] Messaging drift check: [pending]
- [ ] CMO review: [pending]
- [ ] Persona reviews: [pending]
- [ ] Argument review: [pending]
- [ ] Cross-pillar links: [pending]

## Launch Messaging Constraints

**CRITICAL: Hard constraints. Do not deviate, paraphrase, or reinterpret.**

### Positioning Statement
[Verbatim from brief]

### Value Proposition
[Verbatim from brief]

### Messaging Pillars
[Verbatim from brief's Messaging Pillars with all proof points]

### Say This / Not This
[Verbatim from brief]

### Constraint
Write within these messaging boundaries. The article should advance the launch narrative, not create a new one. Do not introduce new positioning angles. Do not add unsourced claims.

## Evidence Provided
[From brief's Evidence section — pain points with verbatim quotes, proof points, competitive context, customer language]

## Cross-Reference Placeholders
[From brief's Cross-References section — list each referenced launch asset with tracker status]

## Key Decisions

| # | Decision | Rationale | Date |
|---|----------|-----------|------|

**Rule: Rewrites that contradict a previous decision require user confirmation before proceeding.**

## Human Feedback Log

| Date | Feedback (verbatim) | Action Taken |
|------|---------------------|--------------|
```

### Step 4 — Create research-brief.md

```markdown
# Research Brief: [Topic from PMM Brief]

## LAUNCH CONSTRAINT: Do Not Add External Research

This brief is the complete source of truth for this article. Generated from the approved launch messaging.

**DO NOT:**
- Run `/research` on this topic
- Add web research, SERP analysis, or external sources
- Introduce new angles, frameworks, or positioning not in the approved messaging
- Add statistics or claims not provided in the Evidence section

## Launch Context
- **Launch slug**: [slug]
- **Tracker**: content/launches/[slug]/tracker.md
- **Launch date**: [from tracker]
- **Pillar role**: [from brief's Role in Launch Narrative]

## Content Type
launch

## Launch Content Format
[announcement | technical-deep-dive]

## Launch Messaging Constraints

### Positioning Statement
[Verbatim from brief]

### Value Proposition
[Verbatim from brief]

### Messaging Pillars
[Verbatim from brief's Messaging Pillars with all proof points]

### Say This / Not This
[Verbatim from brief]

## Thesis and Position
[From brief's Key Messages. Synthesize into a clear thesis + 2-3 supporting arguments.]

## Recommended Outline

**IMPORTANT: The outline structure depends on the Launch Content Format above.**

### If announcement format:

Inverted pyramid. The article MUST lead with the news — what is being launched or announced. Do NOT start with industry context, background, market trends, or "the vision". The reader should know what's new in the first sentence.

#### H1: [State the announcement or the key claim — not background]

#### H2 sections:
1. [What's new and why it matters — the announcement itself, expanded]
2. [Why this is different / why now — supporting evidence from brief]
3. [How it works — capabilities, proof points]
4. [What this means for the reader — forward-looking]

Do NOT build a thought-leadership essay (context → problem → solution → how-it-works). That buries the news. Lead with the news, then support it.

### If technical-deep-dive format:

Lead with the problem or architecture insight.

#### H1: [The problem or technical insight]

#### H2 sections:
1. [The problem in concrete terms]
2. [Technical approach — architecture, design decisions]
3. [Evidence — benchmarks, code examples, comparisons]
4. [Implications and what's next]

## Evidence

### Pain Points
[Verbatim customer quotes from brief]

### Proof Points
[Metrics, customer outcomes from brief]

### Competitive Context
[If relevant, from brief]

### Customer Language
[Key phrases to use naturally]

## Visual Placeholders
Where the brief specifies screenshots, diagrams, or product visuals:
- [Location]: <!-- [SCREENSHOT: description] -->

## Launch CTA
- **Primary CTA**: [from brief — e.g., contact page, demo request]
- **Secondary CTA**: [if applicable — whitepaper download, webinar registration]

## PMM Knowledge Files
[Paths resolved from $PMM_KNOWLEDGE_PATH]

## Meta Elements
- **Topic**: [from brief]
- **Suggested slug**: /blog/[derived from topic]
- **Target audience**: [from brief]
- **Distribution**: [from brief]

## Cross-References
[From brief — this article's role + related launch assets]
```

### Step 5 — Update tracker

Set status to `in progress`, output path to `content/launches/[slug]/[pillar-slug]/`.

### Step 6 — Present structure to user

Show the research brief (thesis, outline, evidence mapping) for review.

**PAUSE: Wait for user feedback.** (Cornerstone and Collaborative engagement levels pause here. Guided and Autonomous proceed directly to Checkpoint 2.)

---

## Checkpoint 2: Writing

### Pre-writing reads (required)

Before writing, read:
1. `context/launch-writing-examples.md` (study the structure and patterns — especially the "Patterns Across All Examples" section)
2. `context/brand-voice.md` (Part 1 + Part 2 — this IS product content)
3. The research brief (just created)
4. The messaging framework (path in decisions.md)
5. `context/style-guide.md`

### Writing structure — Announcement format

Use for Blog Post and Sponsored Content. Inverted pyramid: lead with the news.

- **H1**: Lead with the news or the key claim. Not background, not context.
- **Opening** (100-150 words): First sentence IS the news. No preamble. State what's being announced and why it matters. A busy executive should get the key message in 30 seconds.
- **Body** (800-1,200 words): 3-4 H2 sections following the research brief's outline structure. Each section advances the argument — no filler sections.
- **Visual placeholders**: Insert `<!-- [SCREENSHOT: description] -->` where the brief specifies product visuals, diagrams, or graphics.
- **Conclusion** (100-150 words): Forward-looking. Hard CTA. No summary of what you just said.
- **Total**: 1,000-1,500 words

### Writing structure — Technical deep-dive format

Use for Technical Blog Post. Lead with the problem or architecture decision.

- **H1**: Lead with the problem or the technical insight
- **Longer** (1,500-2,500 words). Code examples and technical detail welcome.
- Follow the research brief's outline for section structure.
- Visual placeholders for architecture diagrams where relevant.
- Hard CTA at the end (demo/contact).

### Brief fidelity rules

- Follow the brief's intent strongly. The brief defines WHAT to say and the structure.
- Rewording for craft is encouraged. Drifting from the messaging is not.
- All evidence comes from the brief's Evidence section. No unsourced claims.
- Value proposition must appear verbatim somewhere in the article.
- All Say This phrases should be present or faithfully represented.
- No Not This phrases should appear.

### Content scrubber

After writing, run the content scrubber:
- Replace em-dashes (—) with regular dashes (-)
- Remove "delve", "landscape", "paradigm", "tapestry", "comprehensive", "robust"
- Remove "It's worth noting", "It's important to", "Interestingly"
- Flag "This isn't X. It's Y" pivot pattern — keep at most one instance per article

Save cleaned version in place.

### Present draft to user

**PAUSE: Wait for user feedback.** (Cornerstone, Collaborative, and Guided engagement levels pause here. Autonomous proceeds directly to Checkpoint 3.)

---

## Checkpoint 3: Final

### Step 1 — Editor Agent

1. **Preserve pre-edit copy**: Copy the article to `[slug]-pre-edit-[YYYY-MM-DD].md` in the same folder.
2. **Spawn editor agent**: `.claude/agents/editor.md` on the working copy. The editor makes direct edits to improve humanity, voice, specificity, and engagement.
3. **Present edited version** to user. Note that the pre-edit copy exists for comparison.

**PAUSE: Wait for user feedback on editor changes.** If the user wants to restore something the editor removed, pull it from the pre-edit copy.

### Step 2 — Messaging Drift Checker

Spawn agent: `.claude/agents/messaging-drift-checker.md`
Input: The article + decisions.md (for messaging constraints)
Output: `messaging-drift-check.md`

If FAIL: Fix the identified deviations before proceeding.

### Step 3 — CMO Reviewer

Spawn agent: `.claude/agents/cmo-reviewer.md`
Input: The article + decisions.md
Output: `cmo-review.md`

### Step 4 — Persona Reviewer

Spawn agent: `.claude/agents/persona-reviewer.md`
Run once per target persona listed in the research brief's Target audience.
Load persona file from `$PMM_KNOWLEDGE_PATH/knowledge_base/personas/[persona].md`.
Input: The article + persona file + decisions.md
Output: `persona-review-[persona].md` (one per persona)

### Step 5 — Argument Reviewer

Review the article for argument quality. Evaluate:
1. Is the thesis clear and stated early?
2. Does each section advance the argument or just fill space?
3. Are trade-offs and counterarguments addressed honestly?
4. Is the article grounded in concrete examples from the evidence provided?
5. Does it give the reader a framework or mental model they can apply?
6. Are there sections that repeat points already made?
7. Do all claims trace back to the Evidence Provided section?

Output: `argument-review.md`

### Step 6 — Cross-Pillar Linker

Spawn agent: `.claude/agents/cross-pillar-linker.md`
Input: The article + tracker.md
Output: `cross-pillar-links.md`

### Step 7 — Present review results to user

**PAUSE: Wait for user feedback on reviews.**

### Step 8 — Update decisions.md

Mark all review checkboxes. Update status.

### Step 9 — Update tracker

Set status to `complete`, confirm output path.

---

## Iteration Protocol

When the user provides feedback at any checkpoint:

1. Log the feedback verbatim in decisions.md → Human Feedback Log
2. Check if the feedback contradicts any existing Key Decision. If yes, ask user to confirm before proceeding.
3. Apply the feedback
4. Re-run the content scrubber
5. Re-run the messaging drift checker (drift can creep in during revisions)
6. Update decisions.md status
