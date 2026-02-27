# Competitive Comparison — Asset Type Template

## Metadata

- **Format**: prose
- **Target length**: 2000-2500 words (5-7 pages)
- **Reading time**: 8-12 minutes
- **Tone**: Elevated authority - "Authority Under Scrutiny" from brand voice. Data-driven, fair, and rigorous. Let the evidence lead.
- **Brand voice**: Part 1 always. Part 2 when Swimm is the subject.
- **Primary personas**: `cio`, `architect` (override per project)

## Purpose

A competitive comparison is a follow-up asset - sent after a conversation, demo, or initial engagement. It makes one clear argument with evidence and ends with a reason to continue the conversation. It is not a primer (too introductory) or a whitepaper (too heavy). It is the piece that gets forwarded to the technical evaluator or attached to the deal recap email.

**Distribution**: Mailing list, partner handoff, deal follow-up, post-demo leave-behind.

## Knowledge Sources

Load from `$PMM_KNOWLEDGE_PATH`:

| File | When to Load | Approx Tokens |
|------|-------------|---------------|
| `config/teach_product_output.md` | Always | ~8,400 |
| `knowledge_base/messaging/framework.md` | Always | ~5,300 |
| `knowledge_base/competitive/[competitor].md` | Always (primary competitor) | ~10-16K |
| `knowledge_base/personas/[target].md` | Per audience (1-2 files) | ~6,000 each |
| `knowledge_base/jtbd/modernization.md` | When topic involves modernization | ~6,300 |

**Per-section loading**: The outline (Phase 1) tags each section with which files it needs. Phase 2 loads only the tagged files into each section's writing subagent.

## Section Structure

A competitive comparison has exactly 7 sections. The structure follows a courtroom logic: question, test, evidence, explanation, alternative, mechanism, next step.

| # | Section | Job | Reader's Question | Words |
|---|---------|-----|--------------------|-------|
| 1 | **The Question** | Frame the evaluation clearly and fairly | "What exactly are we comparing?" | 150-250 |
| 2 | **The Test** | Establish methodology and credibility | "How did you test this?" | 200-350 |
| 3 | **The Results** | Present evidence with tables and specifics | "What did you find?" | 500-700 |
| 4 | **Why This Happens** | Explain the structural reason, not a flaw | "Is this fixable or fundamental?" | 300-450 |
| 5 | **What's Actually Required** | Expand the frame beyond the comparison | "What does the real solution look like?" | 300-450 |
| 6 | **The Approach** | Present how deterministic + AI solves this | "How does your approach work?" | 250-400 |
| 7 | **Next Steps** | Clear paths forward for different reader types | "What should I do now?" | 100-150 |

### Section Details

**The Question** (150-250 words)
- Open with the real question buyers are asking - not a strawman.
- Acknowledge the competitor's strengths honestly. This earns trust immediately.
- Frame the comparison as a rigorous evaluation, not a takedown.
- Set up what "good enough" means for enterprise use vs. general use.
- Knowledge: messaging/framework

**The Test** (200-350 words)
- Describe what was tested, on what data, with what methodology.
- Be specific: program names, line counts, number of runs, prompt strategy.
- Transparency about methodology is what separates this from marketing.
- Include any advantages given to the competitor (refined prompts, multiple passes).
- Knowledge: teach_product_output (for test methodology)

**The Results** (500-700 words)
- This is the core of the piece. Lead with the headline numbers.
- Use tables for structured comparisons (coverage, accuracy, consistency).
- Include 2-3 specific accuracy examples that make the gap tangible and memorable.
- Choose examples that would matter to the reader: wrong dollar amounts > wrong variable names.
- Every claim gets a data point. No assertions without evidence.
- `> [Table: headline comparison metrics]`
- `> [Table: detailed accuracy examples]`
- Knowledge: teach_product_output, competitive file

**Why This Happens** (300-450 words)
- Explain the architectural reason for the results - not a bug, a structural limitation.
- This section prevents the "they'll fix it in the next version" objection.
- Frame as fundamental trade-off (context window vs. full codebase), not incompetence.
- Be fair: acknowledge what the approach IS good for, just not this use case.
- Knowledge: competitive file, teach_product_output

**What's Actually Required** (300-450 words)
- Expand beyond the head-to-head comparison to what the job actually needs.
- Understanding enterprise code requires workflows, governance, team alignment - not just analysis output.
- This section widens the frame: even if the competitor's output were perfect, you'd still need X, Y, Z.
- Connect to what the reader's organization actually needs to do with the understanding.
- Knowledge: teach_product_output, messaging/framework, jtbd file (if applicable)

**The Approach** (250-400 words)
- Present the deterministic + AI approach as the mechanism that delivers what's required.
- Lead with the principle, then the product. Brief and concrete.
- Mention key capabilities without turning into a feature list.
- Security/deployment model in one line if relevant (on-prem, bring-your-own-LLM).
- Knowledge: teach_product_output

**Next Steps** (100-150 words)
- 3-4 paths matched to reader type:
  - Technical evaluator: "See detailed test methodology" or "Run a POC on your code"
  - Decision maker: "Talk to our team about [specific evaluation]"
  - Partner: "Explore partnership opportunities"
  - Deeper learning: Link to related whitepaper, blog, or demo
- Specific and actionable, not vague "learn more" language.
- Knowledge: none

## Formatting Rules

- **Paragraphs**: 3-4 sentences maximum. Scannable throughout.
- **Tables**: Minimum 2 tables - one for headline metrics, one for detailed examples. Tables are primary content, not decoration.
- **Data visualizations**: Include `> [Table: description]` or `> [Chart: description]` placeholders where data should be visualized. Minimum 2.
- **Pull quotes**: One pull quote from the results section highlighting the most memorable finding. Format as `> **"Quote text"**`
- **Tone**: Fair throughout. Acknowledge competitor strengths in at least 2 places. The reader should feel they're getting an honest evaluation, not a hit piece.
- **No footnotes**: Evidence is inline. If a claim needs heavy citation, it's too detailed for this format.
- **Competitor naming**: Name the competitor directly. This is an honest evaluation, not a veiled reference. Use category terms ("general-purpose LLM") only when making broader architectural points.

## Post-Write Agents

| Agent | Required? | Notes |
|-------|-----------|-------|
| `asset-reviewer` | Yes | Full quality review |
| `persona-reviewer` | Yes | Run with primary persona(s) |
| content scrubber | Yes | Universal post-processor |
| `linkedin-repurposer` | Optional | Good for promotion |
| `newsletter-repurposer` | Optional | Strong for email distribution |

## Quality Checklist

- [ ] Total word count between 2000-2500 words
- [ ] "The Question" acknowledges competitor strengths honestly
- [ ] "The Test" includes specific methodology details (programs, line counts, runs)
- [ ] "The Results" includes minimum 2 tables with real data
- [ ] 2-3 specific accuracy examples that would matter to the target reader
- [ ] "Why This Happens" explains structural limitations, not bugs or incompetence
- [ ] Competitor strengths acknowledged in at least 2 places
- [ ] "What's Actually Required" expands frame beyond head-to-head comparison
- [ ] "The Approach" leads with principle before product
- [ ] No marketing-speak, fear language, or superlatives without evidence
- [ ] Product claims verified against `teach_product_output.md`
- [ ] Tone is fair and rigorous throughout - would survive scrutiny from a competitor's team
- [ ] Content scrubber has been run
