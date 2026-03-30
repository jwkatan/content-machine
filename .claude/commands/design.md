# /design — Design Elevation

Create polished, brand-consistent visual outputs using the Swimm design system. Manually invoked for net-new designs — templates, one-off visuals, landing pages, presentations, dashboards. Backed by two specialized agents (design-director for creation, design-reviewer for critique) and an element library of real HTML/CSS code pulled from the Figma brand file.

## Usage

```
/design [description]          Create a new visual output with design elevation
/design review                 Review and elevate an existing draft or output
/design elements               Browse the element library (YAML metadata by category)
/design elements [name]        View a specific element's YAML metadata and HTML code
/design explore [file.md]      Compare a draft against the design system and suggest elevations
```

**Examples:**
```
/design hero section for the modernization landing page
/design presentation deck for the enterprise security pitch
/design review
/design elements
/design elements grad-section
/design explore content/launches/swimm-2/webinar/deck.md
```

## When to Use

- Net-new designs that need to look hand-crafted, not template-based
- New HTML templates, landing page sections, presentation decks
- One-off visuals: dashboards, infographics, promotional pages
- Any visual output where composition, depth, and brand polish matter

## When NOT to Use

- **NEVER** within image-builder rendering flows — image-builder uses its own deterministic templates
- **NEVER** within pdf-builder rendering flows — pdf-builder uses its own deterministic templates
- **NEVER** within launch pipeline flows — launch uses its own pillar dispatchers
- **NOT** for filling finalized Google Slides templates — use `/slides` instead
- **NOT** for AI-generated images — use `/generate-images` instead

Other skills MAY dispatch the design-director agent directly when they want design help (e.g., `/image` can call it for template creation), but this skill does not auto-activate from within those pipelines.

---

## /design [description] — Create Mode

### Phase 1: Understand

Before spawning the design-director agent, gather enough context to write a clear brief. Ask the user:

1. **Purpose** — What is this output for? (landing page hero, pitch deck, dashboard, one-off visual)
2. **Audience** — Who will see it? (enterprise prospects, developers, internal team)
3. **Medium** — What format? (HTML, Marp, PPTX)
4. **Content** — What content exists already? (copy, screenshots, data)
5. **Constraints** — Dimensions, platform, context where it will be viewed?
6. **Success criteria** — What does a great result look like?

Do not proceed until you have answers to at least purpose, audience, and medium. If the user's initial description is clear enough to infer all six, confirm your understanding and move to Phase 2.

### Phase 2: Design

Spawn the design-director agent as a Task (subagent_type: `general-purpose`, model: `opus`):

```
You are the Design Director. Your job is to build a polished, brand-consistent visual output using the Swimm design system.

START by reading these files:
- `.claude/agents/design-director.md` (your full instructions)
- `context/design-system/design-philosophy.md` (visual identity principles)
- `context/design-system/font-reference.md` (typography spec)
- `context/design-system/elevation-protocol.md` (10-step process)
- `context/design-system/construction-techniques.md` (build methods and CSS patterns)
- `context/design-system/ai-pattern-blocklist.md` (AI default patterns to avoid)

FOR MARP OUTPUT — also read these BEFORE composing:
- `context/design-system/marp-theme.css` (MANDATORY — copy full CSS into <style> block, do NOT write CSS from scratch)
- `context/design-system/presentation-design.md` (slide types, sequencing, color balance)

Then follow the elevation-protocol.md 10-step process to create the output.

Request: [user's description]
Medium: [html/marp/pptx]
Audience: [audience from Phase 1]
Constraints: [dimensions, platform, viewing context from Phase 1]
Existing content: [file paths or inline content provided by the user]

When selecting elements (Step 4), read `context/design-system/technique-catalog.md` to find the right techniques, then browse element YAML files in `context/design-system/elements/` for discovery. Load ONLY the selected elements' HTML — never bulk-load all element HTML files.

When composing multi-section layouts (Step 5), read `context/design-system/composition-rules.md`.

CRITICAL FOR MARP: Use the pre-built slide type classes from marp-theme.css. Apply ONE class per slide via <!-- _class: classname -->. Use component HTML classes (card-row, stat-row, screenshot-frame, etc.) for content. NEVER write inline styles for layout, spacing, or centering.

Output the completed visual to the appropriate location based on context (e.g., the user's project directory, content/drafts/, or a path the user specifies).

Present the polished output only. Keep design thinking internal unless the user asks to see it.
```

### Phase 2.5: Diversity Quick-Check

After the design-director completes, scan the output before sending to review:

1. List the slide type class (or section layout pattern) for each section/slide in order
2. Check for **consecutive duplicate slide types** — any two adjacent slides using the same class
3. Check for **layout monotony** — fewer than 3 distinct layout types in compositions with 6+ sections

If either condition triggers, send the output back to the design-director with specific fix instructions:

```
The output has layout diversity issues that must be fixed before review:

[List specific issues, e.g.:]
- Slides 3 and 4 both use `dark-cards` — change one to a different layout type
- Only 2 distinct layouts used across 8 slides — need at least 3 distinct types

Fix these specific issues while preserving all other design choices. Do not redesign — only address the flagged diversity problems.
```

Repeat Phase 2.5 until the diversity check passes, then proceed to Phase 3.

### Phase 3: Review

After the design-director completes, spawn the design-reviewer agent as a Task (subagent_type: `general-purpose`, model: `opus`):

```
You are the Design Reviewer. You did not create this output and have no bias toward it. Your job is to evaluate it against the Swimm brand design system.

START by reading these files:
- `.claude/agents/design-reviewer.md` (your full instructions)
- `context/design-system/interrogation-checklist.md` (pass/fail quality gate)
- `context/design-system/font-reference.md` (typography spec)
- `context/design-system/design-philosophy.md` (visual identity principles)

Then run every item in the interrogation checklist against the output.

Output to review: [path to design-director's output file]
Original request: [user's description from Phase 1]
Medium: [html/marp/pptx]

If checking technique choices, also read `context/design-system/technique-catalog.md`.
If checking composition, also read `context/design-system/composition-rules.md`.

Produce a structured review report with pass/fail per checklist item, critical issues, and a score.
```

### Phase 4: Fix or Deliver

Read the review report and route accordingly:

**All items pass** — Present the polished output to the user. Report the file path, format, and any copy adjustments made during design.

**Auto-fixable failures only** (wrong font, wrong color, wrong spacing, wrong line-height) — Pass the review report back to the design-director agent to apply fixes directly. Then re-run the reviewer on the fixed output. If it passes, deliver.

**Structural failures** (composition does not work, layout needs rethinking, content does not fit any element pattern) — Present the reviewer's findings to the user with the specific problems and 2-3 proposed alternatives. Ask the user how to proceed before re-entering Phase 2.

---

## /design review — Review Mode

For reviewing and elevating an existing draft or output that was not created through the `/design` create flow.

1. Ask the user to identify the output to review. This can be a file path (HTML, Marp, PPTX) or a description of inline content.

2. Spawn the design-reviewer agent as a Task (subagent_type: `general-purpose`, model: `opus`):

```
You are the Design Reviewer. You did not create this output and have no bias toward it. Your job is to evaluate it against the Swimm brand design system.

START by reading these files:
- `.claude/agents/design-reviewer.md` (your full instructions)
- `context/design-system/interrogation-checklist.md` (pass/fail quality gate)
- `context/design-system/font-reference.md` (typography spec)
- `context/design-system/design-philosophy.md` (visual identity principles)

Then run every item in the interrogation checklist against the output.

Output to review: [path to file or inline content]
Context: [any context the user provided about the output's purpose or audience]

If checking technique choices, also read `context/design-system/technique-catalog.md`.
If checking composition, also read `context/design-system/composition-rules.md`.

Produce a structured review report with pass/fail per checklist item, critical issues, and a score.
```

3. Present the review report to the user.

4. If auto-fixable issues were found, offer to apply fixes. If the user agrees, spawn the design-director agent with the review report and the output file to apply targeted fixes only — not a full redesign.

---

## /design elements — Browse Mode

List all available elements from the design system element library.

1. Scan all `element.yaml` files in `context/design-system/elements/*/element.yaml`.

2. Group elements by category and present a summary table:

**Section Templates**

| Element | Description | Surfaces | Mediums |
|---------|-------------|----------|---------|
| `grad-section` | Stunning gradient section with nested layered border frames | dark-to-light-transition | html, marp, pptx |
| `cta-section` | Bottom-of-page closer with triple-nested gradient frames | dark-to-light-transition | html, marp, pptx |
| `hero-background` | Dark navy background with geometric dot-matrix wave pattern | dark | html, marp |
| ... | ... | ... | ... |

**Cards & Content Blocks**

| Element | Description | Surfaces | Mediums |
|---------|-------------|----------|---------|
| `icon-card-dark` | Card with radial gradient background for dark surfaces | dark | html, marp, pptx |
| `stat-block` | Large numeral + label for statistics display | dark, light | html, marp, pptx |
| ... | ... | ... | ... |

**Interactive Patterns**

| Element | Description | Surfaces | Mediums |
|---------|-------------|----------|---------|
| ... | ... | ... | ... |

**Buttons & Links**

| Element | Description | Surfaces | Mediums |
|---------|-------------|----------|---------|
| `main-button` | Primary CTA button, Blue 700 bg | dark, light | html, marp, pptx |
| ... | ... | ... | ... |

**Screenshot Frames**

| Element | Description | Surfaces | Mediums |
|---------|-------------|----------|---------|
| ... | ... | ... | ... |

**Decorative & Background**

| Element | Description | Surfaces | Mediums |
|---------|-------------|----------|---------|
| ... | ... | ... | ... |

For each element, show: name, description, use cases, surfaces, and mediums — all from the YAML metadata. Do NOT load any HTML files during browse mode.

---

## /design elements [name] — View Element

Show the full metadata and HTML code for a specific element.

1. Read `context/design-system/elements/[name]/element.yaml` and present the full metadata: name, description, Figma source nodes, use cases, when to use, when not to use, swappable slots, surfaces, mediums, and breakpoints.

2. Read `context/design-system/elements/[name]/element.html` and present the full HTML/CSS code.

3. If the element has a Figma source, mention the Figma file and node IDs so the user can reference the original design.

---

## /design explore [file.md] — Comparison Mode

Compare an existing draft or output against the design system and identify elevation opportunities without redesigning.

1. Read the target file at the path the user provides.

2. Load the design system references:
   - `context/design-system/design-philosophy.md`
   - `context/design-system/font-reference.md`
   - `context/design-system/composition-rules.md`
   - `context/design-system/technique-catalog.md`
   - `context/design-system/ai-pattern-blocklist.md`

3. Produce a structured comparison report:

```markdown
# Design System Comparison: [filename]

## Already Brand-Compliant
[List specific elements, patterns, and values that already match the design system. Cite which reference file confirms compliance.]

## Deviations
[List specific deviations from the design system with exact values found vs expected. Group by category: typography, color, spacing, composition, depth.]

## Elevation Opportunities
[For each deviation or gap, recommend specific elevation actions:]
- **[Area]:** [Current state] → [Recommended change]
  - Element recommendation: [specific element from technique-catalog.md or element library]
  - Reference: [design system file that defines the correct approach]

## AI Pattern Flags
[Run the 10-item AI pattern detection from ai-pattern-blocklist.md. List any patterns detected with evidence and the brand-correct alternative.]
```

This mode is read-only analysis — it does not modify the target file. The user decides which elevations to pursue.

---

## Reference File Loading Rules

Context management is explicit. The agents load specific files based on mode — never everything at once.

| File | Create Mode | Review Mode | Browse Mode |
|------|:-----------:|:-----------:|:-----------:|
| `design-philosophy.md` | Always | Always | Always |
| `font-reference.md` | Always | Always | Always |
| `elevation-protocol.md` | Always | Never | Never |
| `interrogation-checklist.md` | Step 7 only | Always | Never |
| `technique-catalog.md` | When selecting elements | When checking technique choices | Always |
| `composition-rules.md` | When composing multi-section layouts | When checking composition | Never |
| Element YAML files | For discovery/selection | For checking element usage | For browsing |
| Element HTML files | Only after specific element is selected | Only to verify implementation | On request |

**Critical constraint:** Element HTML files are NEVER bulk-loaded. The agent browses YAML metadata for selection, then loads only the chosen elements' HTML. A single element's HTML can be 50-200 lines; loading all 30-40 at once would consume context unmanageably.

---

## Notes

- **Manual invocation only** — this skill never auto-activates. It is invoked by the user typing `/design` or by another skill explicitly dispatching the design-director agent.
- **Two-agent separation** — creation and critique are opposing cognitive stances. The design-director creates; the design-reviewer challenges. This prevents rationalization of design choices.
- **Output formats** — HTML (element code used directly), Marp (HTML/CSS-based, element styles translate natively), PPTX (composition rules and design patterns guide python-pptx styling; complex gradients may need simplification for PPTX constraints).
- **Content editing guardrails** — the design-director may adjust copy to fit layouts. Product names are sacred (Swimm, Swimm MCP, Understanding Platform). Small word-level edits are made and reported. Large restructuring changes require user approval first.
- **Element library location** — all elements live in `context/design-system/elements/`. Shared CSS tokens live in `context/design-system/tokens.css`. Reference files live in `context/design-system/`.
