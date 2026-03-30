# Competitive Comparison — Asset Type Template

## Metadata

- **Format**: prose
- **Target length**: 1200-1800 words (2-3 pages)
- **Reading time**: 5-8 minutes
- **Tone**: Elevated authority - "Authority Under Scrutiny" from brand voice. Data-driven, fair, and rigorous. Let the evidence lead.
- **Brand voice**: Part 1 always. Part 2 when [COMPANY] is the subject.
- **Primary personas**: `cio`, `architect` (override per project)
- **Modes**: This template supports two modes depending on the project:
  - **Test-based**: Built around a specific benchmark or evaluation [COMPANY] conducted against the competitor. Sections 2-3 present methodology and results.
  - **Research-based**: Built around architectural analysis, capability mapping, or publicly available information. Sections 2-3 present the evaluation framework and findings.

## Purpose

A competitive comparison overcomes the objection that a different product can solve the same problem. It makes one clear argument with evidence. It is not a primer (too introductory) or a whitepaper (too heavy). It is the piece that gets forwarded to the technical evaluator or attached to the deal recap email.

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

**Note**: Personas, competitive files, and JTBD files are base knowledge — not guaranteed to be complete or fully accurate. Use as a starting point alongside any supplemental materials provided in the project prompt.

**Per-section loading**: The outline (Phase 1) tags each section with which files it needs. Phase 2 loads only the tagged files into each section's writing subagent.

## Section Structure

A competitive comparison has exactly 6 sections. The structure follows a courtroom logic: question, evaluation, evidence, explanation, requirements, mechanism.

| # | Section | Job | Reader's Question | Words |
|---|---------|-----|--------------------|-------|
| 1 | **The Question** | Frame the evaluation clearly and fairly | "What exactly are we comparing?" | 100-200 |
| 2 | **The Evaluation** | Establish how this was assessed | "How do you know?" | 150-300 |
| 3 | **The Evidence** | Present findings with tables and specifics | "What did you find?" | 350-500 |
| 4 | **Why This Happens** | Explain the structural reason, not a flaw | "Is this fixable or fundamental?" | 200-350 |
| 5 | **What's Actually Required** | Expand the frame beyond the comparison | "What does the real solution look like?" | 200-300 |
| 6 | **The Approach** | Present how deterministic + AI solves this | "How does your approach work?" | 200-350 |

### Section Details

**The Question** (100-200 words)
- Open with the real question buyers are asking - not a strawman.
- Frame the comparison as a rigorous evaluation, not a takedown.
- Set up what "good enough" means for enterprise use vs. general use.
- Do not over-index on acknowledging competitor strengths. If the competitor is genuinely strong somewhere relevant, say so briefly. Do not fabricate or exaggerate praise — it reduces trust instead of building it.
- Knowledge: messaging/framework

**The Evaluation** (150-300 words)
- *Test-based mode*: Describe what was tested, on what data, with what methodology. Be specific: program names, line counts, number of runs, prompt strategy. Include any advantages given to the competitor (refined prompts, multiple passes). Transparency about methodology is what separates this from marketing.
- *Research-based mode*: Describe the evaluation framework — what capabilities were compared, what criteria were used, what sources inform the analysis.
- Knowledge: competitive file, supplemental project materials (test methodology lives in supplemental materials, not in teach_product_output)

**The Evidence** (350-500 words)
- This is the core of the piece. Lead with the headline findings.
- Use tables for structured comparisons (coverage, accuracy, consistency, or capability mapping depending on mode).
- Include 2-3 specific examples that make the gap tangible and memorable.
- Choose examples that would matter to the reader: wrong dollar amounts > wrong variable names.
- Every claim gets a data point. No assertions without evidence.
- `> [Table: headline comparison metrics]`
- `> [Table: detailed examples]`
- Knowledge: teach_product_output, competitive file

**Why This Happens** (200-350 words)
- Explain the architectural reason for the results - not a bug, a structural limitation.
- This section prevents the "they'll fix it in the next version" objection.
- Frame as fundamental trade-off, not incompetence. The usual gap is that LLMs are probabilistic and struggle with discovery and full coverage — not context window limits.
- Where the competitor's approach genuinely works better (modern codebases, new projects, small scope changes), acknowledge it honestly — but only when accurate and relevant. Do not force praise.
- Knowledge: competitive file, teach_product_output

**What's Actually Required** (200-300 words)
- Expand beyond the head-to-head comparison to what the job actually needs.
- Keep this section tight. The point is to widen the frame, not to repeat the messaging framework.
- Before writing: check whether the competitor claims to offer the same capabilities (governance, workflows, team alignment). If they do, address that claim directly rather than presenting these as uncontested differentiators. The section falls flat if the reader thinks "but [competitor] says they do that too."
- Connect to what the reader's organization actually needs to do with the understanding.
- Knowledge: teach_product_output, messaging/framework, jtbd file (if applicable)

**The Approach** (200-350 words)
- Present the deterministic + AI approach as the mechanism that delivers what's required.
- Lead with the principle, then the product. Brief and concrete.
- Mention key capabilities without turning into a feature list.
- Security/deployment model in one line if relevant (on-prem, bring-your-own-LLM).
- Knowledge: teach_product_output

## Formatting Rules

- **Paragraphs**: 2-4 sentences maximum. Scannable throughout.
- **Tables**: Minimum 2 tables - one for headline metrics, one for detailed examples. Tables are primary content, not decoration. An optional third table comparing features, functionality, or applicability may be included in "The Approach" or "What's Actually Required" when there is enough information to support it.
- **Data visualizations**: Include `> [Table: description]` or `> [Chart: description]` placeholders where data should be visualized. Minimum 2.
- **Pull quotes**: One pull quote from the evidence section highlighting the most memorable finding. Format as `> **"Quote text"**`
- **Tone**: Fair throughout. The reader should feel they're getting an honest evaluation, not a hit piece. Acknowledge competitor strengths when accurate and relevant — not as a forced exercise. Do not praise the competitor in areas that contradict the need for [COMPANY].
- **Footnotes**: Allowed for source citations (repo locations, blog references, related assets). Keep them light — if a claim needs heavy citation, it's too detailed for this format.
- **Competitor naming**: Name the competitor directly. This is an honest evaluation, not a veiled reference. Use category terms ("general-purpose LLM") only when making broader architectural points.
- **No customer or partner references**: Knowledge base files may contain customer names, partner names, or case study details. These must never appear in the asset. No quotes, no named references, no implied identification.

## Post-Write Agents

| Agent | Required? | Notes |
|-------|-----------|-------|
| `asset-reviewer` | Yes | Full quality review |
| `/scrub` | Yes | Content scrubber — universal post-processor |
| `/review-content` | Yes | Run with explicit list of all knowledge sources and supplemental materials provided for this project. The reviewer uses these to verify accuracy of reproduced data, claims, and statistics. |

## Quality Checklist

- [ ] Total word count between 1200-1800 words
- [ ] "The Question" frames the evaluation fairly without forced competitor praise
- [ ] "The Evaluation" includes specific methodology or evaluation framework details
- [ ] "The Evidence" includes minimum 2 tables with real data or structured findings
- [ ] 2-3 specific examples that would matter to the target reader
- [ ] "Why This Happens" explains structural limitations (probabilistic output, discovery gaps), not bugs or incompetence
- [ ] "What's Actually Required" checks whether competitor claims overlapping capabilities before asserting differentiators
- [ ] "The Approach" leads with principle before product
- [ ] No marketing-speak, fear language, or superlatives without evidence
- [ ] No customer names, partner names, or case study references leaked from knowledge base
- [ ] Product claims verified against `teach_product_output.md`
- [ ] Tone is fair and rigorous throughout - would survive scrutiny from a competitor's team
- [ ] `/scrub` has been run
- [ ] `/review-content` has been run with source list