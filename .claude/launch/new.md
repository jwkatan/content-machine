# /launch new [launch-slug]

Initialize a tracker from a PMM Researcher launch. This is the bridge step between PMM strategy and content production.

## PMM Path Resolution

1. Read `PMM_KNOWLEDGE_PATH` from `data_sources/config/.env`
2. Construct: `[PMM_KNOWLEDGE_PATH]/launches/[launch-slug]/`
3. Verify the directory exists
4. All PMM file paths in tracker and downstream files should use absolute resolved paths (not `$PMM_KNOWLEDGE_PATH` variables) so agents can read them directly

## Process

1. **Resolve PMM path**: Read `PMM_KNOWLEDGE_PATH` from `data_sources/config/.env`. Construct launches path: `[PMM_KNOWLEDGE_PATH]/launches/[launch-slug]/`.

2. **Validate launch exists**: Check that the directory exists. If not, list available launches from `[PMM_KNOWLEDGE_PATH]/launches/` and ask user to pick.

3. **Read launch metadata**: Read `_internal/context.md` for launch name, date, summary, and current phase status.

4. **Read pillars checklist**: Read `execution/pillars-checklist.md`. Extract all pillars with their:
   - Name and description
   - Tasks list
   - Cross-reference annotations (lines starting with `*Cross-references:` or `*Serial dependency:`)

5. **Check for briefs**: List files in `briefs/` directory.
   - If briefs exist: match each brief file to a pillar by filename convention (`[pillar-slug]-brief.md`)
   - If `briefs/` is empty: Phase F hasn't run yet. Mark all rows as `awaiting brief`
   - If `_content-writer-spec.md` exists: read it and use its mapping guidance

6. **Check for missing asset type templates**: For each pillar, look up the asset type in the pillar mapping table (in the coordinator). Check if `asset-builder/asset-types/[type].md` exists. If not, mark as `blocked: missing template`.

7. **Build dependency map**: Parse cross-reference annotations from pillars-checklist:
   - `*Serial dependency:` → hard dependency (must complete first)
   - `*Cross-references:` with "uses X as CTA" or "must be complete first" → hard dependency
   - `*Cross-references:` with "can link to", "can embed", "should link" → soft dependency

8. **Expand multi-deliverable pillars**: Some pillars produce multiple outputs (see below). Create sub-rows in the tracker.

9. **Write tracker**: Create `content/launches/[launch-slug]/tracker.md` (see tracker-format.md for format).

10. **Designate cornerstone**: Ask the user which brief is the cornerstone asset — the first piece that gets produced with full human involvement, whose learnings propagate to all other briefs.
    - **Default suggestion**: Blog Post (brief #1). Explain: "The blog post is usually the cornerstone — it's where the real messaging gets forged through editing. All other assets will be blocked until the cornerstone is complete and its learnings are propagated to the remaining briefs."
    - If the user picks a different brief, that's fine. Record the choice.
    - Set the cornerstone brief's engagement to `cornerstone` in the tracker.
    - Set all other briefs to `blocked: awaiting propagation` unless they were already `awaiting brief` or `blocked: missing template`.
    - Set `Propagation status` to `not started` in Launch Info.

11. **Report**: Show brief inventory, cornerstone designation, blocked items, dependency map, and next steps. Explain that the next step is `/launch work [cornerstone-brief-number]`.

## Re-running (when tracker already exists)

If re-running `/launch new` after Phase F completes:
- Read existing tracker
- Preserve existing status values (`in progress`, `complete`, `skipped`)
- Update only `awaiting brief` rows that now have corresponding brief files → change to `not started`
- Add any new pillars that appeared
- Report what changed

## Multi-Deliverable Expansion

Some pillars produce multiple outputs from a single PMM brief. Expand these into sub-rows:

### Product Webinar
| Sub | Type | Command |
|-----|------|---------|
| Deck | webinar-deck | `/asset` |
| Landing Page | webinar-landing | `/asset` |
| Invite Email 1 | email-campaign | `/asset` |
| Invite Email 2 | email-campaign | `/asset` |
| Invite Email 3 | email-campaign | `/asset` |
| Reminder Email | email-campaign | `/asset` |
| Follow-up: Attended | email-campaign | `/asset` |
| Follow-up: No-Show | email-campaign | `/asset` |

### Sales Enablement
| Sub | Type | Command |
|-----|------|---------|
| Talk Track | talk-track | `/asset` |
| Battle Cards | battle-card | `/asset` |
| Discovery Questions | discovery-guide | `/asset` |
| Objection Handling | objection-guide | `/asset` |

### Partner Enablement
| Sub | Type | Command |
|-----|------|---------|
| Partner Brief | partner-brief | `/asset` |
| Partner Talk Track | talk-track | `/asset` |

Each sub-deliverable gets its own `decisions.md` and output path. The PMM brief covers the full pillar — extract the relevant subset for each sub-deliverable.

## Output Structure

All outputs go to `content/launches/[launch-slug]/[pillar-slug]/`.

For multi-deliverable pillars, nest sub-tasks:
```
content/launches/[slug]/
  blog-post/
  technical-blog-post/
  whitepaper/
  webinar/
    deck/
    landing-page/
    invite-1/
    invite-2/
    invite-3/
    reminder/
    followup-attended/
    followup-noshow/
  sales-enablement/
    talk-track/
    battle-cards/
    discovery/
    objections/
  partner-enablement/
    partner-brief/
    talk-track/
  social/
    announcement/
    pain-differentiation/
    proof-evidence/
  website/
```
