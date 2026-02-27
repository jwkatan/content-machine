# Webpage Builder Command

Multi-agent collaborative system for building production-quality web pages. 6-phase process with human checkpoints at every transition. 7 AI agents with distinct viewpoints collaborate and converge.

## Usage

```
/webpage                        # Dashboard: see active projects + status
/webpage new "[Page Name]"      # Start a new page project
/webpage continue               # Resume work on active project
```

## Subcommands

### Dashboard (no arguments)

Show active webpage projects:

```
/webpage
```

**Process:**

1. Scan `webpage-builder/projects/` for project folders (ignore `.gitkeep`)
2. For each project, read its `decisions.md` to get current phase and status
3. Display dashboard:

```
## Webpage Builder Dashboard

### Active Projects
1. swimm-homepage-2026 — Phase 5: Review (V3, CMO: 72/100, BD: 8.2/10)
2. cobol-modernization-usecase — Phase 2: Content (3/8 sections drafted)

### Quick Actions
- Continue: /webpage continue
- New project: /webpage new "Page Name"
```

If no projects exist, show:
```
## Webpage Builder Dashboard

No active projects.

Start one: /webpage new "Swimm Homepage 2026"
```

---

### New (`/webpage new "[Page Name]"`)

Initialize a new page project with scaffolding.

```
/webpage new "Swimm Homepage 2026"
```

**Process:**

1. **Derive folder name** from the page name:
   - Convention: `[company-or-product]-[page-type]-[identifier]`
   - Example: "Swimm Homepage 2026" -> `swimm-homepage-2026`
   - Example: "COBOL Modernization Use Case" -> `cobol-modernization-usecase`
   - Ask user to confirm the folder name

2. **Determine page type**:
   - Ask user: homepage, product, or usecase
   - Load template from `webpage-builder/page-types/[type].md`
   - If template doesn't exist yet, note it and proceed with generic structure

3. **Create project structure**:
   ```
   webpage-builder/projects/[folder-name]/
   ├── decisions.md          # From template, filled with project name and date
   ├── src/
   │   └── .gitkeep
   └── tests/
       └── package.json      # @playwright/test dependency
   ```

4. **Initialize decisions.md** from `webpage-builder/templates/decisions-template.md`:
   - Replace `[Project Name]` with actual name
   - Replace `[date]` with current date
   - Set page type

5. **Create tests/package.json**:
   ```json
   {
     "name": "[folder-name]-tests",
     "private": true,
     "devDependencies": {
       "@playwright/test": "^1.58.2"
     }
   }
   ```

6. **Gather initial context from user**:
   - Page purpose and target audience
   - Key messages or positioning to reinforce
   - Reference URLs or materials (competitor pages, existing content, brand guidelines)
   - Any specific requirements or constraints

7. **Start Phase 1: Brief** (see workflow below)

8. **Confirm to user**:
   ```
   Created project: webpage-builder/projects/swimm-homepage-2026/

   Page type: homepage
   Template: webpage-builder/page-types/homepage.md

   Starting Phase 1: Brief
   ```

---

### Continue (`/webpage continue`)

Resume work on the active project from its last phase.

```
/webpage continue
```

**Process:**

1. Scan `webpage-builder/projects/` for projects
2. If one project -> read its `decisions.md` -> resume at current phase
3. If multiple -> show dashboard, ask user to specify which project
4. Read the project's `decisions.md` to determine:
   - Current phase and sub-step
   - What's been approved
   - Last human feedback
5. Resume the appropriate phase workflow (see below)

---

## Workflow Phases

### Phase 1: BRIEF (Strategy)

**Goal**: Define section-by-section messaging strategy.

**Agents**: PMM (primary), CMO (reviewer)

**Process:**

1. Load page type template from `webpage-builder/page-types/[type].md`
2. Load agent personas from `webpage-builder/agents.md`
3. Load brand voice from `@context/brand-voice.md`
4. Load web copy style guide from `webpage-builder/web-copy-style.md`
5. Using the user's initial context, page type template, brand voice, and web copy style:

6. **PMM agent** writes a section-by-section messaging brief:
   - For each section: what it must accomplish, key messages, what to avoid
   - Narrative arc from first scroll to conversion
   - Buyer persona and mental state at each scroll point

7. **CMO agent** reviews the brief:
   - Positioning strength
   - Narrative arc coherence
   - Competitive differentiation clarity
   - Enterprise credibility
   - Brand voice compliance (Part 1 universal + Part 2 if Swimm-specific)

8. PMM revises based on CMO feedback. **Max 3 PMM<->CMO iterations**, then present to human.

9. Save output -> `brief.md`
10. Update `decisions.md`: Phase 1 status, key decisions

11. **HUMAN CHECKPOINT**: Present the brief and ask for approval or redirect.
   - "Approve and move to Phase 2: Content"
   - "Revise: [specific feedback]"

---

### Phase 2: CONTENT (Copy)

**Goal**: Draft section-by-section copy following the approved brief.

**Agents**: Writer (primary), Editor (tightener), PMM (alignment), Designer (visual notes)

**Context loaded**: `@context/brand-voice.md`, `webpage-builder/web-copy-style.md`, approved `brief.md`

**Process:**

**CRITICAL: Sections are written and reviewed ONE AT A TIME, in order.** Do NOT batch or parallelize section drafting. Each section must pass its own review cycle AND a context review against all prior sections before the next section begins. This is the enforced sequence:

#### Per-Section Cycle (repeat for each section in brief order)

**Step 1 — Write.** Writer agent drafts the section copy following the brief, applying:
- BBQ test (clarity) then Boardroom test (precision) — two-pass rule
- VBF hierarchy: Value headline → Benefits supporting → Features only if needed
- Outside-in check: first words reflect buyer's world, not product
- SMIT: one message per section, clearly identifiable

**Step 2 — Edit.** Editor agent tightens and enforces:
- Em-dash discipline (consistent usage)
- No filler words
- Active voice enforcement
- Word count within section budget
- Refrigerator test: reject vague headlines that could describe any product
- "So What?" test: every headline must survive a CIO asking "So what?"
- Curse of Knowledge check: flag insider terms that lack context

**Step 3 — Alignment check.** PMM agent checks messaging alignment with brief and brand voice sequencing (Outcome→Risk→Mechanism).

**Step 4 — Context review (against all prior sections).** Before this section is accepted:
- Extract all H2s written so far (including this one) and read in sequence — does the headline story arc hold?
- Does this section's opening connect to the previous section's close?
- Any redundancy or contradiction with earlier sections?
- Does the tone and rhythm feel consistent with the established voice?
- If flow breaks → rework this section before proceeding. Do NOT move to the next section.

**Step 5 — Accept.** Append the accepted section copy to `content.md`. Only then begin the next section.

**Max 3 agent iterations per section**, then present to human.

#### Designer notes pass

After all sections are individually accepted, the Designer agent does a single pass adding visual requirements and layout implications per section. This is separate from the copy cycle because visual notes depend on the full page context.

#### Final assembly

- Verify `content.md` contains all accepted sections in order
- Update `decisions.md`: Phase 2 status

**HUMAN CHECKPOINT**: Present full content document and ask for approval.

---

### Phase 3: DESIGN (Visual Direction)

**Goal**: Create section-by-section visual direction.

**Agents**: Designer (primary), Brand Director (reviewer)

**Process:**

1. **Designer agent** creates visual direction for each section:
   - Layout structure (grid/flex, column ratios)
   - Color palette with hex values and usage zones
   - Typography hierarchy (sizes, weights, line-heights)
   - Spacing (padding, margins, gutters)
   - Visual elements (graphics, icons, screenshots, SVGs)
   - Responsive behavior at each breakpoint
   - Interaction notes (hover states, animations)

2. **Brand Director agent** reviews:
   - Color discipline (every color justified)
   - Compositional balance across the full page
   - Visual hierarchy (what the eye sees first, second, third)
   - Design system coherence (consistent patterns section-to-section)
   - Typography consistency

3. Designer revises. **Max 3 Designer<->Brand Director iterations**, then present to human.

4. Save output -> `visual-direction.md`
5. Update `decisions.md`: Phase 3 status, color palette, key visual decisions

**HUMAN CHECKPOINT**: Present visual direction and ask for approval.

---

### Phase 4: BUILD (Engineering)

**Goal**: Build a self-contained HTML file implementing the approved content and design.

**Agents**: Engineer (primary), Designer (visual reviewer)

**Technical requirements:**
- Single self-contained HTML file with inline CSS
- CDN for fonts and scripts only (Google Fonts, GSAP, etc.)
- Responsive: mobile-first with tablet/desktop breakpoints
- Accessible: semantic HTML, alt text, aria labels, focus management
- Animations respect `prefers-reduced-motion`
- No external stylesheets or local dependencies

**Process:**

Build section by section:

1. **Engineer agent** builds the section in `src/index.html`
2. **Designer agent** reviews visual implementation against `visual-direction.md`
3. Check visual continuity with previously built sections
4. **Max 3 Engineer<->Designer iterations per section**

After all sections built:

5. Copy `webpage-builder/templates/responsiveness-template.spec.js` to `tests/responsiveness.spec.js`
6. Customize the test template:
   - Fill in SECTIONS array with actual CSS selectors from the built page
   - Fill in CTA_SELECTORS
   - Fill in GRID_SECTIONS
   - Fill in SUBGRID_SECTIONS
   - Fill in SIDE_BY_SIDE_SECTIONS
7. Install Playwright in tests directory: `cd tests && npm install && npx playwright install chromium`
8. Run test suite: `cd tests && npx playwright test responsiveness.spec.js`
9. Fix any failures

10. Update `decisions.md`: Phase 4 status

**HUMAN CHECKPOINT**: Ask user to review the built page in a browser (`open src/index.html`).

---

### Phase 5: REVIEW CYCLE (Polish)

**Goal**: Iterative quality improvement scored by CMO and Brand Director.

**Agents**: CMO (scorer), Brand Director (scorer), Engineer (implementer)

**Ship threshold**: CMO >= 75 AND Brand Director >= 8.0

**Process:**

1. Take Playwright screenshots at 1440px viewport for agent review:
   ```bash
   cd tests && npx playwright test --project=chromium -g "screenshot" || true
   ```
   Or manually screenshot the page in browser.

2. **Run scoring in parallel:**

   **CMO agent** scores (out of 100):
   - Visual impact at a glance
   - Narrative clarity
   - Enterprise gravitas
   - Competitive differentiation
   - Ship/iterate decision

   **Brand Director agent** scores (out of 10):
   - Color discipline
   - Compositional balance
   - Typographic precision
   - Visual density
   - Ship/iterate decision

3. **Synthesize feedback:**
   - Convergent directives (both agents agree) -> apply immediately
   - Divergent directives (agents disagree) -> flag for discussion
   - If both say "ship" and scores meet threshold -> move to Phase 6

4. **Engineer agent** applies convergent directives

5. Track version in `decisions.md` score history table:
   ```
   | V1 | 65 | 7.5 | Initial build |
   ```

6. **Max 3 review iterations**, then human decides:
   - Continue iterating (resets counter)
   - Accept as shipped
   - Redirect with specific feedback

**HUMAN CHECKPOINT**: After each iteration, show scores and ask for direction.

---

### Phase 6: FINALIZE

**Goal**: Ship-ready validation and stable copy.

**Process:**

1. Run full Playwright test suite — all tests must pass:
   ```bash
   cd tests && npx playwright test responsiveness.spec.js
   ```

2. If any images need hosting, upload to HubSpot:
   ```bash
   .venv/bin/python -c "from data_sources.modules.hubspot_uploader import upload_file; print(upload_file('path/to/image.png', 'webpage-builder/[project]/'))"
   ```

3. Run content scrubber on final HTML text content:
   ```bash
   .venv/bin/python -c "from data_sources.modules.content_scrubber import scrub_text; ..."
   ```

4. Save approved version: copy `src/index.html` to `src/index-stable.html`

5. Update `decisions.md`:
   - Phase 6: complete
   - Final scores
   - Final status: shipped

6. **Report to user:**
   ```
   Project finalized: webpage-builder/projects/swimm-homepage-2026/

   Final scores: CMO 82/100, Brand Director 8.9/10
   Tests: 36/36 passing
   Stable copy: src/index-stable.html

   The page is ready for deployment.
   ```

---

## State Management

`decisions.md` is the single state file for each project. It tracks:
- Current phase and sub-step
- What's been approved at each checkpoint
- Score history table (version | CMO | BD | key change)
- Design decisions with rationale
- Human feedback log with dates

When resuming (`/webpage continue`), always read `decisions.md` first to understand where the project stands.

---

## Reference Files

- Brand voice & messaging: `@context/brand-voice.md` **(load for all phases)**
- Web copy style guide: `webpage-builder/web-copy-style.md` **(load for Phases 1-2)**
- Agent personas: `webpage-builder/agents.md`
- Page type templates: `webpage-builder/page-types/[type].md`
- Decisions template: `webpage-builder/templates/decisions-template.md`
- Test template: `webpage-builder/templates/responsiveness-template.spec.js`

## Modules Used

- `data_sources/modules/content_scrubber.py` - Remove AI watermarks from final copy
- `data_sources/modules/hubspot_uploader.py` - Upload images for hosting
- `data_sources/modules/image_generator.py` - Generate images if needed

## Environment Variables

Required in `data_sources/config/.env`:
```
HUBSPOT_ACCESS_TOKEN=pat-eu1-xxxxx     # For image hosting
GOOGLE_API_KEY=xxxxx                    # For image generation (if needed)
```
