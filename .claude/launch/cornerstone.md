# Cornerstone Process

The cornerstone is the first asset produced in a launch. It gets full human involvement — every checkpoint, unlimited iteration. The real messaging gets forged here. Once complete, its learnings propagate to all other briefs before any other asset begins.

## When This Runs

The coordinator dispatches here when the user starts work on the brief designated as the cornerstone in the tracker.

## Identifying the Asset Type

The cornerstone is usually a blog post, but the user may designate any brief. Determine the asset type from the tracker and load the appropriate writing process:

| Cornerstone Type | Writing Process |
|-----------------|----------------|
| Blog Post, Technical Blog Post, Sponsored Content | Read `.claude/launch/write-blog.md` for structure + format rules |
| Any `/asset` type (whitepaper, video-script, etc.) | Read `asset-builder/asset-types/[type].md` for structure |
| Social Campaign | Read `.claude/launch/dispatch-social.md` |

The checkpoint process below applies regardless of asset type. The writing/structure rules come from the type-specific file above.

---

## Checkpoint 0: Flow / Sequence (complex assets only)

**Applies to**: webinar-deck, video-script, sales-deck, webinar-landing (any asset where the sequence/flow matters more than individual sections).

**Skip for**: blog posts, whitepapers, email campaigns, battle cards, one-pagers.

1. Read the PMM brief + messaging framework.
2. Propose the narrative arc, scene sequence, slide flow, or page sections — depending on asset type.
3. Present to user for review.

**PAUSE: Wait for user feedback.**

Iterate until the user approves the flow. Each round:
- Log feedback in decisions.md → Human Feedback Log
- Revise the flow
- Present updated version

When approved: record flow decisions in decisions.md → Key Decisions. Proceed to Checkpoint 1.

---

## Checkpoint 1: Structure

1. **Read inputs**:
   - PMM brief: `[PMM_PATH]/launches/[slug]/briefs/[brief-file].md`
   - Messaging framework: `[PMM_PATH]/launches/[slug]/strategy/messaging-framework-llm-optimized.md`
   - Type-specific process file (see table above)
   - `context/brand-voice.md` (Part 1 + Part 2)
   - `context/style-guide.md`
   - For blog posts: `context/launch-writing-examples.md`

2. **Create project folder**: `content/launches/[launch-slug]/[pillar-slug]/`

3. **Create decisions.md**: Use the format from `write-blog.md` (Step 3) for blog types, or `dispatch-asset.md` (Step 3) for asset types. Include the `## Launch Messaging Constraints` section with verbatim messaging from the brief.

4. **Create the structural document**:
   - For blog posts: `research-brief.md` with thesis, outline, evidence mapping
   - For assets: `brief.md` with section-by-section outline following the asset type template

5. **Present structure to user for review.**

**PAUSE: Wait for user feedback.**

Iterate until the user approves. Each round:
- Log feedback verbatim in decisions.md → Human Feedback Log
- Check if feedback contradicts an existing Key Decision — ask for confirmation if yes
- Revise the structure
- Present updated version

When approved: update decisions.md status. Proceed to Checkpoint 2.

---

## Checkpoint 2: Rough Draft

1. **Pre-writing reads** (for blog posts):
   - `context/launch-writing-examples.md`
   - `context/brand-voice.md`
   - The research brief
   - The messaging framework
   - `context/style-guide.md`

2. **Write the full draft** following the approved structure and the type-specific writing process.

3. **Run content scrubber**: Replace em-dashes, remove AI watermarks ("delve", "landscape", "paradigm", etc.), flag "This isn't X. It's Y" pattern.

4. **Present draft to user for review.**

**PAUSE: Wait for user feedback.**

Iterate until the user approves. Each round:
- Log feedback verbatim in decisions.md → Human Feedback Log
- Check if feedback contradicts an existing Key Decision — ask for confirmation if yes
- Apply the feedback
- Re-run content scrubber
- Present updated version

When approved: update decisions.md status. Proceed to Checkpoint 3.

---

## Checkpoint 3: Final

1. **Preserve pre-edit copy**: Copy the article to `[slug]-pre-edit-[date].md` in the same folder. This is the "before" snapshot for comparison.

2. **Run editor agent**: Spawn `.claude/agents/editor.md` on the working copy. The editor makes direct edits to improve humanity, voice, specificity, and engagement. The pre-edit copy lets the user compare before/after and recover anything the editor stripped.

3. **Present edited version to user.** Point out that the pre-edit copy exists for comparison.

**PAUSE: Wait for user feedback on editor changes.**

If the user wants to restore something the editor removed, pull it from the pre-edit copy. Iterate as needed.

4. **Run review agents** (in sequence, save each to the project folder):
   - **Messaging Drift Checker**: Spawn `.claude/agents/messaging-drift-checker.md`. Input: article + decisions.md. Output: `messaging-drift-check.md`. If FAIL: fix deviations before proceeding.
   - **CMO Reviewer**: Spawn `.claude/agents/cmo-reviewer.md`. Input: article + decisions.md. Output: `cmo-review.md`.
   - **Persona Reviewer**: Spawn `.claude/agents/persona-reviewer.md`, once per target persona. Input: article + persona file + decisions.md. Output: `persona-review-[persona].md`.
   - **Argument Reviewer**: Evaluate thesis clarity, section progression, evidence grounding, repetition. Output: `argument-review.md`.
   - **Cross-Pillar Linker**: Spawn `.claude/agents/cross-pillar-linker.md`. Input: article + tracker.md. Output: `cross-pillar-links.md`.

5. **Present review results to user.**

**PAUSE: Wait for user feedback on reviews.**

Iterate as needed. Each round: apply feedback, re-run scrubber, re-run drift checker (drift can creep in during revisions).

6. **When user approves final version**:
   - Mark all review checkboxes in decisions.md
   - Update tracker: set status to `complete`, engagement to `cornerstone`
   - Tell user: "Cornerstone complete. Run `/launch propagate` to extract learnings and update the remaining briefs."

---

## Decision Tracking

Every decision made during the cornerstone process gets logged in decisions.md → Key Decisions:

| # | Decision | Rationale | Date |
|---|----------|-----------|------|

**Rule**: Rewrites that contradict a previous decision require user confirmation before proceeding.

All human feedback is logged verbatim in the Human Feedback Log. This log is the primary input for the propagation step — it captures WHY the messaging evolved, not just WHAT changed.

---

## After Completion

The cornerstone's decisions.md now contains the institutional memory of how messaging evolved. The propagation step (`.claude/launch/propagate.md`) reads this to extract learnings and patch the remaining briefs.

**Do not start any other asset** until propagation is complete. All non-cornerstone briefs remain `blocked: awaiting propagation` until then.
