# Dispatch: /linkedin pillars (Social Campaign, Employee Social)

## Process

### Step 1 — Read the PMM brief

### Step 2 — Create idea files

The PMM brief for social campaigns specifies 3 angles (announcement, pain/differentiation, proof/evidence). Create one idea file per angle in `content/launches/[launch-slug]/social/[angle-slug]/`:

```markdown
# Launch: [Launch Name] — [Angle Name]

## Source
PMM Researcher /launch-strategy brief: [path to brief]
Launch: [launch-slug], Brief #[N]

## LAUNCH CONSTRAINT
Write within the approved messaging below. Do not introduce new angles.

## Angle
[Description of this angle from the brief]

## Messaging Constraints
### Positioning Statement
[Verbatim]

### Key Messages for This Angle
[Which messaging pillars to emphasize, from brief's guidance per angle]

### Say This / Not This
[Relevant subset]

## Evidence for This Angle
[Curated evidence relevant to this specific angle]

## Post Type
[ceo / company — from brief if specified, otherwise ask]
```

### Step 3 — Run `/linkedin post [idea-file]` for each idea file to generate 3-5 variations.

### Step 4 — Update tracker

Set status to `complete`, output path to `content/launches/[slug]/social/[angle-slug]/`.
