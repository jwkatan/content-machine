# /launch status

Display the current state of a launch.

## Process

1. If only one launch tracker exists in `content/launches/`, use it. If multiple, ask user which one.
2. Read `tracker.md`
3. Show:
   - **Cornerstone**: Brief #[N] ([pillar name]) — [status]. Propagation: [status].
   - **Progress bar**: N complete / M total (X blocked, Y in progress)
   - **Brief inventory table**: all rows with current status and engagement level
   - **Blocked items**: list what's blocked and why (missing template, unmet dependency, awaiting propagation)
   - **Recommended next**: If cornerstone incomplete → "Finish the cornerstone." If propagation not done → "Run `/launch propagate`." Otherwise → lowest-numbered unblocked `not started` brief.

## Dashboard (no arguments to /launch)

1. Scan `content/launches/` for tracker files
2. For each, read `tracker.md` and show:
   - Launch name, date, overall progress (N/M complete)
   - Cornerstone status and propagation status
   - Blocked items count (missing templates, unmet dependencies)
3. If no launches, show: "No active launches. Run `/launch new [slug]` to import from PMM."
