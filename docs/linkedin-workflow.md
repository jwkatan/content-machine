# LinkedIn Workflow

## Post Generation: 4 Options Model

The `/linkedin post` command always generates **4 distinct post variations** from a single idea file. Each variation uses a different hook, angle, or framing while staying true to the core insight.

### Why 4 Options

- Different hooks resonate differently depending on the audience's mood and feed context
- Gives the CEO real choice instead of take-it-or-leave-it on a single draft
- Variations often surface the strongest framing through comparison
- Reduces back-and-forth iteration cycles

### How It Works

1. **Generate**: 4 variations are created, each with a descriptive label and distinct approach
2. **Review**: All 4 are shown to the operator with character counts
3. **Iterate**: Operator can request rewrites before sending
4. **Send to Slack**: Operator chooses which to send - all, some, or none
   - Default: send all 4 for CEO to pick from
   - Can send a subset if some options clearly don't work
   - Can skip Slack entirely if more iteration is needed
5. **CEO picks**: CEO reviews options in Slack and chooses one to post

### Character Targets by Voice

| Voice | Target | Rationale |
|-------|--------|-----------|
| CEO (`ceo-voice.md`) | 500-700 chars | Shorter, punchier, personal authority |
| Company (`brand-voice.md`) | 900-1200 chars | More room for data points and positioning |

### File Format After Generation

The idea file in `topics/linkedin/ideas/` is updated with all 4 variations:

```
## LinkedIn Post - Option 1: "Label" (XXX chars)
## LinkedIn Post - Option 2: "Label" (XXX chars)
## LinkedIn Post - Option 3: "Label" (XXX chars)
## LinkedIn Post - Option 4: "Label" (XXX chars)
```

Each option is stored in a code block for easy copy-paste.

### Slack Message Format

Each option is sent as a separate Slack message with:
- Option number and label
- Character count
- Full post content

This lets the CEO scroll through and pick without needing to compare inside a single long message.

## Changelog

### 2026-02-12
- **Changed**: `/linkedin post` now generates 4 variations instead of 1
- **Changed**: Slack sending supports all/some/none selection
- **Changed**: CEO character target updated to 500-700 (was 900-1200)
- **Changed**: Idea file format updated to store all 4 options with labels
- **Changed**: Slack messages sent individually per option for easier CEO review
