# Discovery Guide — Asset Type Template

## Metadata

- **Format**: reference (question bank organized by persona and situation — not a script, not prose)
- **Target length**: 2000-3000 words
- **Reading time**: 10-15 minutes (reference, not linear read — reps navigate by situation)
- **Tone**: Direct, practical, no-fluff. "Confident Expert Colleague" from brand voice, aimed at internal enablement. Write like a senior AE coaching on discovery technique — teach the thinking behind the questions, not just the questions.
- **Brand voice**: Part 1 always. Part 2 always (questions are designed to surface pain that [COMPANY] solves).
- **Primary personas (users)**: AEs, SDRs, SEs
- **Primary personas (targets)**: `architect`, `program_manager`, `cio` (override per project — the buyer personas reps are discovering)

## Purpose

A discovery guide is a question bank that helps reps navigate discovery conversations by situation, not a rigid script to follow top-to-bottom. Reps choose questions based on who they're talking to, what stage the buyer is in, and what signals they're getting. Every question is designed to surface information that qualifies the deal and sets up [COMPANY]'s positioning — but the questions themselves should feel like genuinely helpful exploration, not a vendor interrogation.

**Distribution**: Internal only. Bookmarked by reps, referenced in pre-call planning. Never sent to buyers.

## Knowledge Sources

Load from `$PMM_KNOWLEDGE_PATH`:

| File | When to Load | Approx Tokens |
|------|-------------|---------------|
| `config/teach_product_output.md` | Always | ~8,400 |
| `knowledge_base/messaging/framework.md` | Always | ~5,300 |
| `knowledge_base/messaging/words_that_work.md` | Always | ~3,600 |
| `knowledge_base/personas/[target].md` | Per buyer persona (all relevant personas) | ~6,000 each |
| `knowledge_base/jtbd/modernization.md` | When discovery involves modernization initiatives | ~6,300 |
| `knowledge_base/jtbd/maintenance.md` | When discovery involves maintenance workflows | ~6,300 |

**Per-section loading**: Each question category tags which files it draws from. Phase 2 loads only the tagged files into each section's writing subagent. Persona files are critical here — the questions are built from persona pain points.

## Section Structure

Questions are organized by buyer stage, not by topic. Each stage represents a different depth of conversation. Reps start at the stage that matches where the buyer is and go deeper.

| # | Section | Job | Rep's Question |
|---|---------|-----|----------------|
| 1 | **Problem Awareness** | Confirm the buyer recognizes the problem | "Do they even know they have this problem?" |
| 2 | **Current State** | Map their existing tools, processes, and pain | "What are they working with today?" |
| 3 | **Impact Quantification** | Attach numbers to the pain | "How big is this problem in dollars, time, or risk?" |
| 4 | **Decision Process** | Understand who decides, how, and when | "How does this organization buy?" |
| 5 | **Timeline and Urgency** | Identify triggers and deadlines | "Is there a forcing function?" |
| 6 | **Persona-Specific Questions** | Targeted questions by buyer role | "What do I ask THIS person specifically?" |

### Section Details

**Problem Awareness** (250-400 words)

These questions test whether the buyer has already recognized the problem or needs help seeing it. Use these early in cold outreach or first meetings.

- 4-6 questions, each formatted as:
  - **Ask**: The question in natural, conversational language.
  - **Listen for**: What a good answer sounds like — signals that the buyer is problem-aware and a fit.
  - **Red flag**: Signals that this isn't a real pain point or the buyer isn't ready.
  - **If they say "yes"**: Follow-up question that goes deeper.
  - **If they say "no" or "not really"**: Pivot question that reframes or seeds the problem.
- Questions should surface whether the buyer has experienced the pain (not whether they know the category exists).
- Include at least one question that uses the buyer's language for the problem (from `words_that_work.md`), not vendor terminology.
- What to avoid: Questions that educate before qualifying. Leading questions that assume the answer. "Are you experiencing challenges with X?" (too generic).
- Knowledge: personas, words_that_work, messaging/framework

**Current State** (350-500 words)

These questions map the buyer's existing tools, processes, team structure, and workarounds. This is where you understand what you're displacing or augmenting.

- 5-7 questions, each formatted as:
  - **Ask**: The question.
  - **Listen for**: What tells you the current state is broken or limited.
  - **Red flag**: Signals that the current state is "good enough" (deal may stall).
  - **Follow-up if...**: Conditional follow-ups based on their specific tools or processes.
- Cover these dimensions:
  - **Tools**: What they use today for the job [COMPANY] does.
  - **Process**: How they handle the workflow currently (manual, automated, ad hoc).
  - **Team**: Who is involved and who bears the pain.
  - **Workarounds**: What they've built or bought to compensate for gaps.
- Include questions that expose the cost of the current state without being leading.
- What to avoid: Asking about tools you should already know from research. Questions that sound like a competitor audit. "What don't you like about [tool]?" (too adversarial).
- Knowledge: personas, teach_product_output (to understand what dimensions matter)

**Impact Quantification** (300-450 words)

These questions help the buyer (and the rep) put a number on the pain. Numbers close deals — stories open doors, but budgets need math.

- 4-6 questions, each formatted as:
  - **Ask**: The question.
  - **Listen for**: Specific numbers, timeframes, or consequences.
  - **If they can't quantify**: A reframing question that helps them estimate (e.g., "If you had to guess, how many hours per week does your team spend on [X]?").
  - **Calculator note**: How to translate their answer into a business case number (e.g., "Multiply hours × average loaded cost × 52 weeks").
- Cover these impact dimensions:
  - **Time**: Hours/weeks lost to the current problem.
  - **Cost**: Direct spend or opportunity cost.
  - **Risk**: What breaks or fails when the problem isn't solved.
  - **Velocity**: How much faster things could move (projects, releases, decisions).
- What to avoid: Asking for numbers they don't have (be ready with estimation frames). Making the buyer feel interrogated about finances. Questions that sound like you're building their ROI slide for them (even though you are).
- Knowledge: personas, messaging/framework, jtbd files (for quantification benchmarks)

**Decision Process** (250-400 words)

These questions map the buying process — who's involved, how decisions are made, and what can derail the deal. Critical for deal qualification and multi-threading.

- 4-6 questions, each formatted as:
  - **Ask**: The question.
  - **Listen for**: Clear process, identified stakeholders, allocated budget.
  - **Red flag**: No process, single-threaded champion, "we'll figure it out" energy.
  - **Follow-up if...**: Conditional follow-ups based on org type (enterprise vs. mid-market).
- Cover these dimensions:
  - **Stakeholders**: Who evaluates, who decides, who signs.
  - **Process**: How they've bought similar solutions before.
  - **Budget**: Whether budget is allocated, needs to be requested, or is discretionary.
  - **Blockers**: What has killed similar initiatives in the past.
- What to avoid: "Who's the decision maker?" (too blunt — ask about process and the names emerge). Asking about budget too early. Questions that make the buyer feel like they're being qualified (even though they are).
- Knowledge: personas (for typical org structures)

**Timeline and Urgency** (200-350 words)

These questions identify whether there's a forcing function — a deadline, trigger event, or consequence that creates urgency. Without urgency, deals stall.

- 3-5 questions, each formatted as:
  - **Ask**: The question.
  - **Listen for**: Specific dates, events, or consequences tied to inaction.
  - **If no urgency exists**: Questions that surface latent urgency (regulatory changes, competitive pressure, leadership mandates).
  - **Urgency amplifier**: A follow-up that connects the timeline to the impact they already described.
- Cover these trigger types:
  - **External**: Regulatory deadlines, audit dates, contract renewals.
  - **Internal**: Leadership mandates, budget cycles, project timelines.
  - **Competitive**: Competitor moves, market shifts, talent loss.
- What to avoid: "When are you looking to make a decision?" (gives them permission to say "no rush"). Creating false urgency. Questions that pressure rather than explore.
- Knowledge: messaging/framework (for market triggers), jtbd files

**Persona-Specific Questions** (400-600 words)

A quick-reference bank of 3-5 targeted questions per buyer persona. Reps jump to this section when they know who they're meeting with and want persona-relevant questions fast.

- Organize as sub-sections by persona (e.g., **For the Architect**, **For the Program Manager**, **For the CIO**).
- Each persona block includes:
  - **Their primary concern**: One sentence — what this person cares about most.
  - **3-5 questions**: Tailored to their specific pain points, priorities, and language.
  - **Watch for**: The key signal from this persona that indicates a strong fit.
  - **Avoid**: Topics or framings that don't resonate with this persona.
- Pull questions directly from persona pain points in PMM files. Use their language, not ours.
- What to avoid: Generic questions that work for anyone. Over-indexing on one persona. Questions that a more junior role couldn't ask without sounding presumptuous.
- Knowledge: personas (primary source), words_that_work

## Formatting Rules

- **Navigation-first**: Reps jump to the section they need. Every section opens with a bold one-line description of when to use it.
- **Consistent question format**: Every question block follows the same structure (Ask → Listen for → Red flag / Follow-up). No exceptions. Consistency is what makes this usable at speed.
- **Natural language**: Questions must sound like something a human would say in conversation. Read every question aloud — if it sounds like a survey, rewrite it.
- **Conditional logic everywhere**: "If they say X → ask Y" is the most valuable part of this document. Real conversations branch — this guide should branch with them.
- **Bold the questions**: The "Ask" line is bolded in every block so reps can scan for questions visually.
- **No marketing copy**: This is an internal coaching tool. Be direct about what signals are good, bad, and ugly.
- **Persona labels visible**: When questions are persona-specific, tag them so reps can filter mentally.

## Post-Write Agents

| Agent | Required? | Notes |
|-------|-----------|-------|
| `asset-reviewer` | Yes | Focus on question quality, conditional logic, and practical usability |
| `persona-reviewer` | Yes | Run with all target buyer personas to validate question relevance |
| content scrubber | Yes | Universal post-processor |
| `linkedin-repurposer` | No | Internal document — not for external promotion |
| `newsletter-repurposer` | No | Not applicable |

## Quality Checklist

- [ ] Total word count between 2000-3000 words
- [ ] Every question follows the consistent format (Ask → Listen for → Red flag / Follow-up)
- [ ] Questions sound conversational when read aloud
- [ ] Problem awareness section tests for pain, not category awareness
- [ ] Current state section covers tools, process, team, and workarounds
- [ ] Impact quantification includes estimation frames for when buyers can't quantify
- [ ] Decision process uncovers stakeholders without asking "who's the decision maker?"
- [ ] Timeline section surfaces forcing functions, not just preferences
- [ ] Persona-specific section covers at least 2 buyer personas with 3-5 questions each
- [ ] Conditional follow-ups ("if they say X") appear throughout
- [ ] At least one question per section uses buyer language from `words_that_work.md`
- [ ] No leading questions that assume the answer
- [ ] No generic questions answerable from the buyer's website
- [ ] Product positioning is absent — questions discover, they don't sell
- [ ] Content scrubber has been run
