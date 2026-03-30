# /launch propagate

Extract learnings from the completed cornerstone asset and update the remaining briefs. This ensures that the real messaging — forged through heavy human editing — flows to every other asset in the launch.

## When This Runs

After the cornerstone brief is marked `complete`. The coordinator routes here when the user runs `/launch propagate`.

## Prerequisites

- Cornerstone brief must be `complete`
- The cornerstone's `decisions.md` must have a populated Key Decisions table and Human Feedback Log

---

## Step 1: Extract Learnings

Read the cornerstone's outputs:
1. `decisions.md` — Key Decisions table + Human Feedback Log
2. The finished cornerstone content (article, brief, etc.)
3. The original PMM brief that was used as input
4. The messaging framework

Compare the finished content and decisions against the original PMM brief. Produce a **Messaging Evolution Summary** organized by category:

```markdown
## Messaging Evolution Summary

### Terminology Changes
[What terms were changed and why. E.g., "platform" not "web app" (decision #11)]

### Framing Changes
[How the narrative framing shifted. E.g., "AI is NOT the enabler; [COMPANY]'s [key differentiator] is" (decision #4)]

### Positioning Refinements
- Updated positioning statement: [if changed from original]
- Updated value proposition: [if changed from original]
- New Say This additions: [phrases that emerged during editing]
- New Not This additions: [phrases that were explicitly rejected]

### Structural Learnings
[What worked structurally. E.g., "Product-forward with feature showcase beats concept repetition" (decision #22). Note: only propagate structural learnings to asset types where they're relevant.]

### Evidence Adjustments
- Added: [proof points, data, examples that were added or elevated]
- Dropped: [evidence that was cut or de-emphasized]
- Reframed: [evidence that was repositioned]
```

Present the summary to the user.

**PAUSE: Wait for user to review and adjust the extraction.**

The user may correct the extraction, add context, or remove items that shouldn't propagate. Iterate until they approve.

---

## Step 2: Triage — Brief Patching vs. Framework Update

Analyze the changes and recommend one of:

**"Brief patching is sufficient"** — Recommend this when:
- Changes are terminology refinements (word choices, phrase preferences)
- Framing shifts are specific to how the story is told, not what the product IS
- Evidence was added/dropped but the core proof points remain
- Say This / Not This got additions but the overall messaging pillars are intact

**"The messaging framework needs updating"** — Recommend this when:
- The value proposition was fundamentally reworded or repositioned
- Core messaging pillars were reordered, dropped, or replaced
- The positioning statement shifted meaningfully
- The product's core narrative changed (not just how it's told, but what it IS)

Present your recommendation with specific reasoning. Example:

> "I recommend **brief patching**. The core messaging pillars and value prop are intact — you refined terminology ('platform' not 'web app'), tightened the framing (AI as enabler → context control as enabler), and added evidence specificity. These are refinements that can be applied per-brief without changing the framework."

Or:

> "I recommend **updating the messaging framework**. Decision #4 ('AI is NOT the enabler') contradicts the framework's current positioning that leads with AI capabilities. Decision #21 reframes the entire value prop around factory economics. These aren't refinements — they're a repositioning that should be reflected at the framework level."

**PAUSE: Wait for user to decide.**

---

## Step 3: Execute Updates

### If brief patching (most common):

For each pending asset brief in `[PMM_PATH]/launches/[slug]/briefs/`:

1. Read the brief file
2. Update the `Approved Launch Messaging` section:
   - Apply terminology changes to positioning statement, value prop, messaging pillars, Say This / Not This
   - Add new Say This / Not This entries from the extraction
   - Update evidence references if relevant to this asset type
3. Add a `## Cornerstone Learnings` section at the bottom with:
   - Only the learnings RELEVANT to this asset type (filter by relevance — see table below)
   - Source attribution: "From cornerstone [pillar name], decision #N"
4. Present the changes for the current brief to the user

**PAUSE: Wait for user approval before saving each brief.**

Save the patched brief. Move to the next one.

### If framework update:

1. Read the messaging framework file
2. Propose specific updates to: positioning statement, value proposition, messaging pillars, Say This / Not This
3. Present changes to user

**PAUSE: Wait for user approval before saving.**

Save the updated framework. Then proceed with brief patching as above (the briefs now reference the updated framework, but still need terminology and evidence patches).

### Relevance Filtering

Not every cornerstone learning applies to every asset type. Use this guide:

| Learning Category | Applies To | Does NOT Apply To |
|------------------|-----------|------------------|
| Terminology changes | All asset types | — |
| Positioning refinements | All asset types | — |
| Say This / Not This additions | All asset types | — |
| Framing changes | Blog, whitepaper, sponsored, press release, webinar deck | Battle card, discovery guide, objection guide |
| Structural learnings | Same-format assets (blog→blog, whitepaper→whitepaper) | Different-format assets |
| Evidence additions | Assets covering same topic area | Unrelated pillar assets |
| Evidence drops | All asset types (if something was dropped, it shouldn't appear elsewhere) | — |

When in doubt about relevance, include the learning with a note: "From cornerstone — apply if relevant to this asset's scope."

---

## Step 4: Update Tracker

1. Set `Propagation status` to `complete` in Launch Info
2. Change all `blocked: awaiting propagation` briefs to `not started` (unless they have other blockers like missing templates or unmet hard dependencies)
3. Add a session log entry: `[date] | — | Propagation complete. [N] briefs patched. [Framework updated / Framework unchanged.]`
4. Report: show the updated brief inventory with new statuses, and recommend which briefs to start next

---

## Re-propagation

If the user continues iterating on the cornerstone after propagation (more feedback rounds, additional decisions), they can run `/launch propagate` again:

1. Read the cornerstone's decisions.md — identify decisions made AFTER the last propagation (by date)
2. Extract only the NEW learnings
3. For briefs not yet started: patch with new learnings (same process as above)
4. For briefs already in progress: warn the user: "Brief #N ([pillar]) is already in progress. New cornerstone learnings: [summary]. Review the in-progress asset's decisions.md and apply relevant updates manually."
5. Update `Propagation status` to `re-propagated`
