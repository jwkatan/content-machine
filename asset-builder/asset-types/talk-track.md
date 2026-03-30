# Talk Track — Asset Type Template

## Metadata

- **Format**: reference (structured internal document — conversation stages, not flowing prose)
- **Target length**: 2000-3000 words
- **Reading time**: 10-15 minutes (reference, not linear read)
- **Tone**: Direct, practical, no-fluff. "Confident Expert Colleague" from brand voice, aimed at internal enablement. Write like a senior AE coaching a peer — not marketing copy.
- **Brand voice**: Part 1 always. Part 2 always (talk tracks are about positioning [COMPANY] in live conversations).
- **Primary personas (users)**: AEs, SEs, solutions architects
- **Primary personas (targets)**: `architect`, `program_manager`, `cio` (override per project — the buyer personas reps are selling to)

## Purpose

A talk track is a conversation guide for live sales interactions — demos, discovery calls, and follow-up meetings. It is not a script to read verbatim. It provides structure, key phrases, and transitions so reps can navigate conversations confidently while sounding natural. Reps should internalize the flow and adapt language to the moment.

**Distribution**: Internal only. Shared via Slack, Notion, or enablement sessions. Never sent to buyers.

## Knowledge Sources

Load from `$PMM_KNOWLEDGE_PATH`:

| File | When to Load | Approx Tokens |
|------|-------------|---------------|
| `config/teach_product_output.md` | Always | ~8,400 |
| `knowledge_base/messaging/framework.md` | Always | ~5,300 |
| `knowledge_base/messaging/words_that_work.md` | Always | ~3,600 |
| `knowledge_base/sales_enablement/objection_handling.md` | Always | ~4,500 |
| `knowledge_base/personas/[target].md` | Per buyer persona (1-2 files) | ~6,000 each |
| `knowledge_base/competitive/[name].md` | When competitor comes up in deal context | ~10-16K each |

**Per-section loading**: Each conversation stage tags which files it draws from. Phase 2 loads only the tagged files into each section's writing subagent.

## Section Structure

A talk track follows the natural arc of a sales conversation. Sections are sequential stages, not independent modules — each stage sets up the next.

| # | Section | Job | Rep's Question |
|---|---------|-----|----------------|
| 1 | **Opener** | Pattern interrupt — earn the right to a conversation | "How do I get them engaged in the first 30 seconds?" |
| 2 | **Discovery** | Qualify the opportunity and surface pain | "What should I ask to understand their situation?" |
| 3 | **Positioning** | Frame the approach before the product | "How do I explain what we do without sounding like a pitch?" |
| 4 | **Demo Flow** | Show the product through the lens of their pain | "What do I show and what do I say while showing it?" |
| 5 | **Objection Handling** | Address resistance without getting defensive | "What do I say when they push back?" |
| 6 | **Close** | Secure a concrete next step | "How do I end with momentum?" |

### Section Details

**Opener** (150-300 words)

The opener earns attention. It is NOT a pitch, company overview, or agenda slide walkthrough.

- **Pattern interrupt**: Open with a provocative observation, question, or data point that reframes their thinking. Something they haven't heard from the last 5 vendors.
- **Relevance hook**: Connect the interrupt to their specific context (industry, role, company situation). Use persona pain points from PMM files.
- **Permission frame**: Transition to discovery by asking for their perspective, not launching into a monologue.
- Include 2-3 opener variants for different entry points (cold call, warm intro, follow-up from event).
- Format each variant as: **Context** → **What to say** → **Transition to discovery**
- What to avoid: "Thanks for taking the time..." / company history / "Let me tell you about [COMPANY]" / agenda-setting that kills energy.
- Knowledge: messaging/framework, words_that_work, personas

**Discovery** (400-600 words)

Discovery is not interrogation. It's a guided conversation that helps the buyer articulate their own pain — and qualifies the deal for the rep.

- Organize questions by what they uncover, not by topic:
  - **Situation questions** (2-3): Understand their current state. What tools, processes, team structure.
  - **Pain questions** (3-4): Surface the specific problems. Tie to persona pain points from PMM files.
  - **Impact questions** (2-3): Quantify the pain. Cost, time, risk, opportunity cost.
  - **Vision questions** (1-2): What does "solved" look like for them? This sets up positioning.
- For each question, include:
  - The question itself (in natural language, not corporate-speak)
  - **Listen for**: What a good answer sounds like — signals that indicate qualification
  - **Red flag**: What signals a poor fit or stall
  - **Follow-up if...**: Conditional follow-ups based on their response
- What to avoid: Rapid-fire question lists. Leading questions that force your narrative. Questions you could have answered from their website.
- Knowledge: personas, messaging/framework, words_that_work

**Positioning** (300-500 words)

Positioning bridges discovery to demo. The rep takes what they heard and frames the approach — not the product — as the answer.

- **Framework-first structure**: Lead with the principle ("enterprise code understanding requires deterministic analysis as a foundation"), then connect [COMPANY] as the implementation.
- Provide a **30-second version** and a **2-minute version** of the positioning statement. Reps choose based on the conversation flow.
- Include **bridging phrases** that connect specific discovery answers to positioning points. Format: "When they say [X], bridge with [Y]."
- 3 key differentiators, phrased as evaluation criteria the buyer should use (not features [COMPANY] has).
- What to avoid: Feature dumps. "We're the only ones who..." claims. Positioning that doesn't reference what the buyer just told you.
- Knowledge: messaging/framework, teach_product_output, words_that_work

**Demo Flow** (500-800 words)

The demo is not a product tour. It's 3-5 key moments that connect product capability to buyer pain, delivered in a narrative sequence.

- Structure each moment as:
  - **Moment name**: A descriptive label (e.g., "The First Understanding" not "Dashboard Overview")
  - **What to show**: Specific screen, feature, or output. Be concrete — "Show the dependency graph for their sample COBOL program" not "Show the analysis."
  - **What to say**: The narration that connects what's on screen to their pain. 2-3 sentences.
  - **Pause point**: Where to stop and ask the buyer a question to keep them engaged.
  - **If they ask...**: Anticipated questions at this moment and how to handle them.
- 3-5 moments total. More than 5 loses focus. Fewer than 3 lacks substance.
- Include a **demo personalization checklist**: what to customize before the call based on what you learned in discovery (industry, language, use case).
- What to avoid: Showing every feature. Reading the UI aloud. Skipping buyer engagement. Demo-ing without tying back to discovery findings.
- Knowledge: teach_product_output, personas

**Objection Handling** (400-600 words)

Cover the top 3-5 objections reps encounter at this deal stage. These are the objections that come up during or immediately after a demo, not procurement-stage objections.

- Structure each objection as:
  - **The objection**: Verbatim how buyers say it (not the sanitized version).
  - **What they're really saying**: The underlying concern behind the words.
  - **Response**: Acknowledge → Reframe → Evidence → Bridge to next step. 3-5 sentences.
  - **Proof point**: A specific customer reference, metric, or example that makes the response concrete.
- Prioritize objections by frequency and deal-killing potential.
- Include objections specific to the competitor context if this talk track targets a competitive situation.
- What to avoid: Defensive responses. "That's a great question" stalling. Dismissing the concern. Over-explaining.
- Knowledge: objection_handling, competitive files (if relevant), teach_product_output

**Close** (200-300 words)

The close secures a concrete next step. Not "let us know" — a specific action with a date.

- Provide 3 close options matched to buyer signals:
  - **High interest**: Technical deep dive or POC proposal. Include the specific ask and timeline.
  - **Moderate interest**: Follow-up meeting with additional stakeholders. Include who to invite and why.
  - **Low interest / stall**: Micro-commitment that keeps the door open (send a relevant case study, intro to a reference customer).
- For each option, include:
  - **Signal that indicates this close**: What the buyer said or did that tells you which close to use.
  - **What to say**: The specific language for the ask.
  - **Calendar commitment**: How to get a date on the calendar before hanging up.
- What to avoid: "I'll send over some materials" without a follow-up date. Asking "what do you think?" as a close. Leaving without a defined next step.
- Knowledge: none (synthesize from conversation context)

## Formatting Rules

- **Conversation-ready language**: Everything in "What to say" sections should sound like a human talking, not a brochure. Read it aloud — if it sounds stilted, rewrite it.
- **Scannable structure**: Reps glance at this mid-call. Use bold headers, short bullets, and clear labels. No dense paragraphs.
- **Variants over scripts**: Provide 2-3 variants for key moments (openers, positioning statements, closes) so reps can choose what fits their style.
- **Conditional logic**: Use "If they say X → respond with Y" format liberally. Real conversations branch.
- **Bold key phrases**: Bold the specific phrases reps should internalize — the 5-10 word chunks that are worth memorizing.
- **No marketing copy**: This is an internal tool. Strip all buyer-facing polish. Be blunt about what works and what doesn't.

## Post-Write Agents

| Agent | Required? | Notes |
|-------|-----------|-------|
| `asset-reviewer` | Yes | Focus on conversation flow, practical usability, and authenticity of language |
| `persona-reviewer` | Yes | Run with target buyer persona(s) to validate pain point accuracy |
| content scrubber | Yes | Universal post-processor |
| `linkedin-repurposer` | No | Internal document — not for external promotion |
| `newsletter-repurposer` | No | Not applicable |

## Quality Checklist

- [ ] Total word count between 2000-3000 words
- [ ] Opener uses a pattern interrupt, not a pitch or agenda
- [ ] Discovery questions organized by what they uncover, with listen-for signals
- [ ] Positioning leads with framework/principle before product
- [ ] Positioning includes both 30-second and 2-minute versions
- [ ] Demo flow has 3-5 moments, each with show + say + pause point
- [ ] Demo includes personalization checklist
- [ ] Objection handling covers top 3-5 objections with verbatim buyer language
- [ ] Each objection follows acknowledge → reframe → evidence → bridge structure
- [ ] Close provides 3 options matched to buyer signal levels
- [ ] Every close option gets a specific date/calendar commitment
- [ ] Language sounds conversational when read aloud
- [ ] Key phrases are bolded for quick reference mid-call
- [ ] Product claims verified against `teach_product_output.md`
- [ ] Content scrubber has been run
