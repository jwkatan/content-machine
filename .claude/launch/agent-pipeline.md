# Engagement Levels

Per-asset engagement levels replace the old agent-driven vs checkpoint binary. When starting each non-cornerstone asset, ask the user which level of involvement they want.

## Choosing an Engagement Level

Present this choice when dispatching each brief via `/launch work [N]`:

> "How hands-on do you want to be with this asset?"
>
> 1. **Collaborative** — I review structure, draft, and final (3 checkpoints)
> 2. **Guided** — Claude handles structure, I review draft and final (2 checkpoints)
> 3. **Autonomous** — Claude runs through with agent reviews, I do final sign-off (1 checkpoint)

Record the choice in the tracker's `Engagement` column.

---

## Level 1: Collaborative

**Checkpoints**: Structure + Draft + Final (all 3)

Best for: high-stakes assets, unfamiliar asset types, assets where the user has strong opinions about direction.

### Flow

```
Structure checkpoint
  → User reviews outline/structure
  → Iterate until approved
    ↓
Draft checkpoint
  → User reviews full draft
  → Iterate until approved
    ↓
Final checkpoint
  → Editor agent (with before/after copy)
  → Review agents (drift, CMO, persona)
  → User reviews and approves
```

Each checkpoint allows unlimited iteration. Same pause-and-wait behavior as the cornerstone process.

---

## Level 2: Guided

**Checkpoints**: Draft + Final (2)

Best for: assets where the user trusts the structure from the patched brief but wants to review the actual content.

### Flow

```
Structure (autonomous)
  → Claude reads patched brief + asset type template
  → Creates decisions.md and structural document
  → No pause — proceeds directly to writing
    ↓
Draft checkpoint
  → User reviews full draft
  → Iterate until approved
    ↓
Final checkpoint
  → Editor agent (with before/after copy)
  → Review agents (drift, CMO, persona)
  → User reviews and approves
```

---

## Level 3: Autonomous

**Checkpoints**: Final only (1)

Best for: lower-stakes assets where messaging is locked and the patched briefs provide clear guidance. The user trusts the process but wants to see the final product.

### Flow

```
Structure (autonomous)
  → Claude reads patched brief + asset type template
  → Creates decisions.md and structural document
    ↓
Draft (autonomous)
  → Claude writes full draft
  → Runs content scrubber
    ↓
Final checkpoint
  → Editor agent (with before/after copy)
  → Review agents (drift, CMO, persona)
  → User reviews all agent outputs + final draft
  → Iterate if needed
```

Even in autonomous mode, the final checkpoint is mandatory. No asset ships without human sign-off.

---

## Flow/Sequence Checkpoint (complex assets)

**Applies to**: webinar-deck, video-script, sales-deck, webinar-landing — any asset where sequence/flow matters.

**Regardless of engagement level**, offer a flow/sequence review before the structure checkpoint:

> "This is a [asset type] — the narrative flow matters. Want to review the sequence/flow before I build out the structure? (Recommended)"

If yes: present the proposed flow (slide order, scene sequence, page sections). Iterate until approved. Then proceed to the chosen engagement level's first checkpoint.

If no: proceed directly to the engagement level's flow.

---

## Engagement Level in the Tracker

The tracker's `Engagement` column records:
- `cornerstone` — The designated cornerstone asset
- `collaborative` — Level 1
- `guided` — Level 2
- `autonomous` — Level 3
- `—` — Not yet started (level not chosen)

This persists across sessions so the process can resume correctly.
