# Launch Command

Orchestrate content production for product launches. Bridges the PMM Researcher project (strategy, messaging, briefs) with this project's content production commands.

**Key rules:**
- PMM briefs REPLACE research — do NOT run `/research` for launch content
- Messaging framework is a hard constraint — Say This / Not This rules must be followed verbatim
- Blog posts use a self-contained writing process (NOT `/write`)
- **Cornerstone-first**: One asset is produced first with full human involvement. All other assets are blocked until the cornerstone is complete and its learnings are propagated.
- **Per-asset engagement**: Each subsequent asset gets the level of human involvement the user chooses (collaborative, guided, or autonomous)
- All outputs go to `content/launches/[launch-slug]/[pillar-slug]/`

## Usage

```
/launch                              # Dashboard: list known launches + progress
/launch new [launch-slug]            # Initialize tracker from PMM launch
/launch status                       # Brief inventory with statuses
/launch work [brief-number]          # Work on a specific brief
/launch propagate                    # Extract cornerstone learnings, patch briefs
/launch continue                     # Pick up next unblocked brief
```

---

## Sub-command Routing

Each sub-command loads its instructions on demand. Read the specified file before executing.

| Sub-command | Action | Read this file |
|-------------|--------|---------------|
| (no args) | Dashboard | `.claude/launch/status.md` |
| `new [slug]` | Initialize tracker + designate cornerstone | `.claude/launch/new.md` |
| `status` | Show progress | `.claude/launch/status.md` |
| `work [N]` | Work on specific brief | Routing logic below |
| `propagate` | Extract learnings, patch briefs | `.claude/launch/propagate.md` |
| `continue` | Pick next brief, dispatch | Routing logic below |

---

## Work / Continue Routing

### For `/launch work [N]`:

1. Read tracker. Identify brief #N.
2. Check brief status:
   - `blocked: awaiting propagation` → "This brief is blocked until the cornerstone is complete and propagation is done. The cornerstone is brief #[X]. Work on the cornerstone first, or run `/launch propagate` if it's already complete."
   - `blocked: missing template` → "Asset type template `[type].md` doesn't exist yet."
   - `awaiting brief` → "Brief file doesn't exist yet. Run Phase F in the PMM project."
   - Unmet hard dependencies → Warn: "Brief #N depends on #X which is [status]. Proceed anyway?"
3. **If the brief is the cornerstone**: Read `.claude/launch/cornerstone.md` and follow its process.
4. **If the brief is NOT the cornerstone**: Check propagation status.
   - If `not started` → "Propagation hasn't been done yet. Run `/launch propagate` first, or work on the cornerstone."
   - If `complete` or `re-propagated` → Ask engagement level (read `.claude/launch/agent-pipeline.md`), then dispatch to the appropriate file below.

### Dispatch by pillar type:

| Pillar Type | Dispatch File |
|-------------|--------------|
| Blog Post, Technical Blog Post, Sponsored Content | `.claude/launch/write-blog.md` |
| Whitepaper, Deck, Email, Video Script, etc. | `.claude/launch/dispatch-asset.md` |
| Social Campaign, Employee Social | `.claude/launch/dispatch-social.md` |
| Website Updates | `.claude/launch/dispatch-webpage.md` |
| Whitepaper Updates | `.claude/launch/dispatch-asset.md` (manual section) |

### For `/launch continue`:

1. Read tracker.
2. If the cornerstone is `in progress`, offer to resume it.
3. If the cornerstone is `complete` but propagation is `not started`, tell user to run `/launch propagate`.
4. Find all briefs where status is `not started` AND all hard dependencies are `complete` or `skipped`.
5. Dispatch to the appropriate file above, asking engagement level first.
6. After completion, update tracker status and output path.

---

## Pillar → Command Mapping

| Pillar | Command | Asset Type | Notes |
|--------|---------|-----------|-------|
| Blog Post | self-contained | thought-leadership | write-blog.md |
| Technical Blog Post | self-contained | thought-leadership | write-blog.md |
| Whitepaper (New) | `/asset` | whitepaper | Single deliverable |
| Whitepaper Updates | manual | — | Content library checkout + edit |
| Customer Launch Email | `/asset` | email-campaign | **Template needed** |
| Social Campaign | `/linkedin` | — | 3 angles × 3-5 variations |
| Employee Social Campaign | `/linkedin` | — | 3-5 employee post templates |
| Product Webinar | `/asset` | webinar-deck + webinar-landing + email-campaign | **Multi-deliverable** |
| Press Release | `/asset` | press-release | **Template needed** |
| Sales Enablement | `/asset` | talk-track + battle-card + discovery-guide + objection-guide | **Multi-deliverable, templates needed** |
| Sales Deck | `/asset` | sales-deck | Single deliverable |
| Partner Enablement | `/asset` | partner-brief + talk-track | **Multi-deliverable, template needed** |
| Sales Outreach | `/asset` | email-campaign | **Template needed** |
| Sponsored Content | self-contained | thought-leadership | write-blog.md |
| Launch Video | `/asset` | video-script | Script deliverable |
| Product Demo Video | `/asset` | video-script | Script + demo flow |
| Social Media Video | `/asset` | video-script | Short-form script |
| Website Updates | `/webpage` | — | Homepage/product page |

### Missing Asset Type Templates

These must be created in `asset-builder/asset-types/` before the corresponding briefs can be executed:

1. `email-campaign.md` — email copy (subject, preview, body, CTA) for drips and one-shots
2. `press-release.md` — structured PR format (headline, dateline, lead, body, boilerplate, contact)
3. `talk-track.md` — sales talk track / demo script
4. `battle-card.md` — competitive battle card (at-a-glance, positioning, objections, landmines)
5. `discovery-guide.md` — discovery questions organized by persona and pain point
6. `objection-guide.md` — objection handling (objection → response → proof point → bridge)
7. `partner-brief.md` — partner positioning overview + co-marketing angles

---

## Output Structure

All launch outputs are centralized under `content/launches/[launch-slug]/`:

```
content/launches/[slug]/
  tracker.md
  blog-post/
  technical-blog-post/
  whitepaper/
  webinar/
    deck/
    landing-page/
    invite-1/ ...
    followup-attended/
    followup-noshow/
  sales-enablement/
    talk-track/
    battle-cards/
    discovery/
    objections/
  social/
    announcement/
    pain-differentiation/
    proof-evidence/
  website/
```

---

## Guardrails

1. **No external research** — Do NOT run `/research` for any launch brief. PMM briefs provide all evidence and angles.
2. **Messaging drift prevention** — Say This / Not This rules go in `## Launch Messaging Constraints` in every decisions.md and research-brief.md. Drift checker runs after every draft.
3. **Blog posts are self-contained** — Blog Post, Technical Blog Post, and Sponsored Content use `.claude/launch/write-blog.md`, NOT `/write`.
4. **Asset process integrity** — `/launch` dispatches to `/asset` but does NOT modify its phase process. The only addition is the messaging constraints section in decisions.md.
5. **Tracker as single source of truth** — All status tracking in `tracker.md`. Each session starts cold from the tracker + PMM files. Update tracker immediately after completing or starting any brief.
6. **Cornerstone gate** — No non-cornerstone asset can begin until the cornerstone is complete AND propagation is done. The tracker enforces this with `blocked: awaiting propagation`.
