# Battle Card — Asset Type Template

## Metadata

- **Format**: reference (single-page-feel scannable document — tables, bullets, and quick-hit sections, not prose)
- **Target length**: 1500-2500 words
- **Reading time**: 5-8 minutes (designed for mid-call scanning, not linear reading)
- **Tone**: Direct, practical, no-fluff. "Confident Expert Colleague" from brand voice, aimed at internal enablement. Write like a senior AE briefing a teammate before a competitive deal — honest about strengths and weaknesses.
- **Brand voice**: Part 1 always. Part 2 always (battle cards are about positioning [COMPANY] against a specific competitor).
- **Primary personas (users)**: AEs, SEs, solutions architects
- **Primary personas (targets)**: `architect`, `program_manager`, `cio` (override per project — the buyer personas involved in the competitive deal)

## Purpose

A battle card is a quick-reference competitive guide that reps use during and between sales conversations. It answers: "How do we win against [competitor]?" Reps pull this up mid-call when a competitor is mentioned, or review it before a meeting where a competitor is in the deal. It must be scannable in under 60 seconds for the key insight a rep needs right now.

**Distribution**: Internal only. Pinned in deal-specific Slack channels, linked from CRM competitor fields, printed for QBRs. Never sent to buyers.

## Knowledge Sources

Load from `$PMM_KNOWLEDGE_PATH`:

| File | When to Load | Approx Tokens |
|------|-------------|---------------|
| `config/teach_product_output.md` | Always | ~8,400 |
| `knowledge_base/messaging/framework.md` | Always | ~5,300 |
| `knowledge_base/messaging/words_that_work.md` | Always | ~3,600 |
| `knowledge_base/sales_enablement/objection_handling.md` | Always | ~4,500 |
| `knowledge_base/competitive/[competitor].md` | Always (this is the primary source) | ~10-16K |
| `knowledge_base/personas/[target].md` | Per buyer persona (1-2 files) | ~6,000 each |

**Per-section loading**: Most sections need the competitive file + messaging/framework. The objection handling section additionally loads objection_handling. Landmines and trap questions draw heavily from the competitive file.

## Section Structure

A battle card has exactly 7 sections. The structure prioritizes speed of access — reps scan from top to bottom but may jump to any section mid-call.

| # | Section | Job | Rep's Question |
|---|---------|-----|----------------|
| 1 | **At-a-Glance** | Side-by-side comparison in 30 seconds | "How do we compare on the key criteria?" |
| 2 | **Positioning** | Why us vs. them — the narrative | "What's our story against this competitor?" |
| 3 | **Competitive Landmines** | Questions to plant that expose competitor weaknesses | "What should I ask that makes them uncomfortable?" |
| 4 | **Objection Handling** | Competitor-specific objections and responses | "What do I say when the buyer brings up [competitor advantage]?" |
| 5 | **Proof Points** | Win stories and metrics | "Where have we beaten them before?" |
| 6 | **Trap Questions to Avoid** | Questions the competitor plants against us | "What questions should I watch out for?" |
| 7 | **Quick Reference** | Key stats, links, and resources | "Where do I go for more detail?" |

### Section Details

**At-a-Glance** (200-350 words)

A comparison table that a rep can scan in 30 seconds. This is the section they look at mid-call when the competitor comes up.

- Format as a table with 8-12 evaluation criteria rows and 3 columns: Criteria | [COMPANY] | [Competitor].
- Choose criteria that matter to the buyer, not criteria that make us look good. Include areas where the competitor is strong.
- Use specific language, not checkmarks or generic ratings. "Full codebase analysis, deterministic" not "Yes" or "Strong."
- Bold the 3-4 rows where [COMPANY] has the clearest structural advantage.
- Include a 1-2 sentence **bottom line** below the table: the single most important thing to remember about this competitor.
- What to avoid: Cherry-picked criteria. Checkmark comparisons that look biased. Vague ratings like "Good" / "Better."
- Knowledge: competitive file, teach_product_output

**Positioning** (200-400 words)

The narrative for why a buyer should choose [COMPANY] over this competitor. Not a feature comparison — a framing argument.

- Lead with the **evaluation frame**: the criteria a buyer should use to evaluate solutions in this category. Frame criteria that structurally favor [COMPANY]'s approach.
- **Why us**: 3 key reasons, each in 1-2 sentences. Lead with the principle, not the feature.
- **Where they win**: 1-2 honest acknowledgments of competitor strengths. This builds credibility with the rep AND prepares them for when buyers raise these points.
- **The structural gap**: The one fundamental architectural or approach difference that makes this a category distinction, not a feature gap. This is the insight that prevents "they'll catch up."
- What to avoid: Feature-for-feature comparison (that's the table above). Dismissing the competitor. Marketing language that a rep wouldn't say in conversation.
- Knowledge: messaging/framework, competitive file, teach_product_output

**Competitive Landmines** (200-350 words)

Questions reps should plant in conversations that expose competitor weaknesses. These are not aggressive — they're legitimate evaluation questions that any thoughtful buyer should ask.

- 4-6 landmine questions, each formatted as:
  - **Ask**: The question in natural language (how a rep would actually say it).
  - **Why it works**: What this question exposes about the competitor's approach.
  - **Expected competitor response**: What the competitor will likely say.
  - **Follow-up**: The question to ask next that deepens the exposure.
- Questions should be framed as good evaluation practice, not as traps. The buyer should feel like they're getting smart advice, not being manipulated.
- Sequence from easy (early in evaluation) to pointed (after demo or POC).
- What to avoid: Gotcha questions that make the rep look adversarial. Questions the competitor could easily turn around on us.
- Knowledge: competitive file, teach_product_output

**Objection Handling** (300-500 words)

Competitor-specific objections — the things buyers say when advocating for the competitor or questioning [COMPANY]'s fit relative to them.

- 3-5 objections, each formatted as:
  - **The objection**: Verbatim how buyers say it (e.g., "We're already using [competitor] and it's working fine").
  - **What they're really saying**: The underlying concern.
  - **Response**: Acknowledge → Reframe → Evidence → Bridge. 3-5 sentences.
  - **Proof point**: Specific customer reference, metric, or test result.
- These are different from general objection handling — they are specific to the competitive dynamic.
- Include the "they're free / cheaper" objection if applicable.
- What to avoid: Bashing the competitor. Defensive postures. Responses that require the buyer to take your word for it without evidence.
- Knowledge: objection_handling, competitive file, teach_product_output

**Proof Points** (200-350 words)

Competitive win stories and metrics that demonstrate [COMPANY] winning against this specific competitor.

- 2-3 win stories, each formatted as:
  - **Account**: Named if approved, anonymized with industry/size if not (e.g., "Fortune 500 financial services").
  - **Situation**: 1 sentence — what they were evaluating and why.
  - **Competitor**: What the competitor offered and where it fell short.
  - **Outcome**: What [COMPANY] delivered — specific metrics if available.
  - **Quotable**: One sentence a rep can use in conversation (attributed if possible).
- Include 2-3 standalone metrics that quantify the gap (e.g., "95% accuracy vs. 31% in controlled test on COBOL inventory program").
- What to avoid: Fabricated or unverifiable stories. Vague "better results" without specifics. Stories that only work for one niche use case.
- Knowledge: competitive file, teach_product_output

**Trap Questions to Avoid** (150-250 words)

Questions the competitor plants against [COMPANY], or evaluation criteria that play to their strengths and our weaknesses.

- 3-5 trap questions, each formatted as:
  - **The question**: How the buyer phrases it (often coached by the competitor).
  - **Why it's a trap**: What assumption or evaluation frame it sets up.
  - **How to redirect**: Acknowledge the question, reframe the evaluation criteria, and pivot to ground where [COMPANY] is strong. 2-3 sentences.
- Be honest about areas where the question has merit — teach the rep to navigate, not dodge.
- What to avoid: Pretending we have no weaknesses. Telling reps to avoid answering. Responses that sound evasive.
- Knowledge: competitive file, teach_product_output

**Quick Reference** (100-150 words)

A fast-lookup footer with essential data points and links.

- **Competitor overview**: 2-3 sentences — what they are, who uses them, their pitch.
- **Their pricing model**: One line (if publicly available or known).
- **Key resources**: Links to competitive analysis doc, demo environment, relevant case studies, SE support channel.
- **Last updated**: Date — battle cards go stale fast.
- Knowledge: competitive file

## Formatting Rules

- **Scannable above all**: Every section must be skimmable in under 60 seconds. If a section requires careful reading to extract value, restructure it.
- **Tables over paragraphs**: Use tables for comparison data, question/answer pairs, and any structured information.
- **Bold key phrases**: Bold the specific words and phrases reps should use or remember.
- **One-line summaries**: Each section opens with a bold one-line summary that captures the key takeaway.
- **No marketing copy**: This is locker-room material. Be direct, even blunt. "They're strong on X" not "While [competitor] offers certain capabilities in X..."
- **Honest about weaknesses**: Include at least 2 specific areas where the competitor legitimately wins. Reps who are blindsided by competitor strengths lose trust with buyers.
- **Print-friendly**: Reps print battle cards. Ensure formatting works without color or complex layouts.

## Post-Write Agents

| Agent | Required? | Notes |
|-------|-----------|-------|
| `asset-reviewer` | Yes | Focus on scannability, honesty of positioning, and practical usability mid-call |
| `persona-reviewer` | Yes | Run with target buyer persona(s) to validate objections and proof points |
| content scrubber | Yes | Universal post-processor |
| `linkedin-repurposer` | No | Internal document — not for external promotion |
| `newsletter-repurposer` | No | Not applicable |

## Quality Checklist

- [ ] Total word count between 1500-2500 words
- [ ] At-a-glance table has 8-12 criteria with specific language (not checkmarks)
- [ ] At-a-glance includes areas where competitor is strong
- [ ] Positioning includes "where they win" acknowledgment
- [ ] Positioning identifies a structural gap, not just feature differences
- [ ] Competitive landmines are legitimate evaluation questions, not gotchas
- [ ] Each landmine has ask + why it works + expected response + follow-up
- [ ] Objection handling covers 3-5 competitor-specific objections
- [ ] Each objection follows acknowledge → reframe → evidence → bridge structure
- [ ] Proof points include 2-3 win stories with specific metrics
- [ ] Trap questions teach reps to redirect, not dodge
- [ ] At least 2 honest competitor strengths acknowledged across the document
- [ ] Every section is skimmable in under 60 seconds
- [ ] Product claims verified against `teach_product_output.md`
- [ ] Competitive claims verified against `competitive/[competitor].md`
- [ ] Quick reference includes last-updated date
- [ ] Content scrubber has been run
