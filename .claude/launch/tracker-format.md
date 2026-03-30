# Tracker Format

## Template

```markdown
# Launch Tracker: [Display Name]

## Launch Info
- **Launch slug**: [slug]
- **PMM path**: [resolved $PMM_KNOWLEDGE_PATH]/launches/[slug]
- **Messaging framework**: [PMM path]/strategy/messaging-framework-llm-optimized.md
- **Launch brief**: [PMM path]/strategy/launch-brief.md
- **Launch date**: [date]
- **Cornerstone brief**: #[N] [Pillar name]
- **Propagation status**: not started
- **Created**: [date]
- **Last session**: [date]

## Brief Inventory

| # | Pillar | Sub | Type | Command | Brief File | Status | Engagement | Blocked By | Output Path |
|---|--------|-----|------|---------|------------|--------|-----------|-----------|-------------|
| 1 | Blog Post | — | thought-leadership | /launch write | blog-post-brief.md | not started | — | — | — |
| 2 | Technical Blog Post | — | thought-leadership | /launch write | technical-blog-post-brief.md | not started | — | — | — |
| 3 | Whitepaper | — | whitepaper | /asset | whitepaper-brief.md | not started | — | — | — |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Dependencies

| Brief # | Depends On | Type | Notes |
|---------|-----------|------|-------|
| 5 | #1 Blog Post | hard | Email uses blog as CTA |
| 6 | #1 Blog Post | soft | Social posts should link to blog |

## Recommended Creation Order

Per PMM content-writer-spec, optimized for dependency resolution:

### Phase 1: Foundation (no dependencies)
[List]

### Phase 2: Anchor Content
[List]

### Phase 3: Distribution (depends on anchor content)
[List]

### Phase 4: Enablement (independent)
[List]

### Phase 5: Events
[List]

## Session Log

| Date | Brief # | Action |
|------|---------|--------|

## Notes

[Free text — add any notes about the launch, decisions made, or issues encountered.]
```

## Status Values

- `awaiting brief` — Phase F hasn't produced this brief yet
- `not started` — Brief exists, ready to work
- `blocked: missing template` — Asset type template doesn't exist yet
- `blocked: awaiting propagation` — Cornerstone complete but propagation not yet done
- `in progress` — Currently being worked on
- `complete` — Finished
- `skipped` — Intentionally skipped (user decided not to produce this asset)

## Propagation Status Values

- `not started` — Cornerstone not yet complete
- `complete` — Learnings extracted and briefs patched
- `re-propagated` — Updated after additional cornerstone iteration

## Engagement Column Values

Set when the user starts work on each brief:

- `collaborative` — All 3 checkpoints (structure + draft + final), unlimited iteration
- `guided` — 2 checkpoints (draft + final), structure handled autonomously
- `autonomous` — 1 checkpoint (final only), agent reviews with human sign-off
- `cornerstone` — Full cornerstone process (all checkpoints + propagation trigger)

## Command Column Values

Blog posts use `/launch write` (self-contained writing process, NOT `/write`). All other pillars use their standard commands:

| Pillar Type | Command |
|-------------|---------|
| Blog Post, Technical Blog Post, Sponsored Content | `/launch write` |
| Whitepaper, Deck, Email, Script, etc. | `/asset` |
| Social Campaign, Employee Social | `/linkedin` |
| Website Updates | `/webpage` |
| Whitepaper Updates | `manual` |

## Multi-Deliverable Tracker Rows

Multi-deliverable pillars expand into sub-rows. Each sub-row tracks independently:

```
| 8 | Product Webinar | 8a: Deck | webinar-deck | /asset | webinar-deck-brief.md | not started | — | — |
| 8 | Product Webinar | 8b: Landing | webinar-landing | /asset | — | not started | #8a (hard) | — |
| 8 | Product Webinar | 8c: Invite 1 | email-campaign | /asset | webinar-invite-brief.md | not started | #8b (hard) | — |
```

## Dependency Rules

- **Hard dependency**: Blocker must be `complete` or `skipped` before the dependent can start
- **Soft dependency**: Can proceed without, but the output will be better if the dependency is complete (link to it, reference it, etc.)
- When checking if a brief is workable: only hard dependencies block execution
