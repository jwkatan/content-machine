# Whitepaper — Asset Type Template

## Metadata

- **Format**: prose
- **Target length**: 3000-6000 words (8-15 pages)
- **Reading time**: 15-30 minutes
- **Tone**: Elevated authority - "Authority Under Scrutiny" from brand voice. Grade 9-10 for executive/strategic sections, grade 11-12 for technical sections.
- **Brand voice**: Part 1 always. Part 2 when [your company] is the subject.
- **Primary personas**: `cio`, `architect` (override per project)

## Knowledge Sources

Load from `$PMM_KNOWLEDGE_PATH`:

| File | When to Load | Approx Tokens |
|------|-------------|---------------|
| `config/teach_product_output.md` | Always | ~8,400 |
| `knowledge_base/messaging/framework.md` | Always | ~5,300 |
| `knowledge_base/personas/[target].md` | Per audience (1-2 files) | ~6,000 each |
| `knowledge_base/jtbd/modernization.md` | When topic involves modernization | ~6,300 |
| `knowledge_base/jtbd/maintenance.md` | When topic involves maintenance | ~6,300 |
| `knowledge_base/competitive/[name].md` | When competitors are referenced | ~10-16K each |

**Per-section loading**: The outline (Phase 1) tags each section with which files it needs. Phase 2 loads only the tagged files into each section's writing subagent.

## Section Structure

A whitepaper typically includes 6-8 sections in this sequence. Sections marked (optional) can be omitted based on the topic.

| # | Section | Job | Reader's Question |
|---|---------|-----|--------------------|
| 1 | **Executive Summary** | Stand-alone extract of the entire argument | "Give me the 1-page version" |
| 2 | **The Challenge** | Frame the problem from the buyer's world | "Do you understand my situation?" |
| 3 | **Current Approaches and Their Limits** | Acknowledge what exists and why it falls short | "What have others tried?" |
| 4 | **Solution Framework** | Present the approach (not the product) | "What's the better way?" |
| 5 | **Evidence and Data** | Substantiate with test results, benchmarks, customer data | "Prove it" |
| 6 | **Implementation Considerations** (optional) | Practical path from evaluation to deployment | "How would this work for us?" |
| 7 | **Technology Deep Dive** (optional) | Architecture and technical differentiation | "How does it actually work?" |
| 8 | **Conclusion and Next Steps** | Synthesize argument, clear CTA | "What should I do now?" |

### Section Details

**Executive Summary** (200-400 words)
- Must stand alone as a 1-page extract. This IS the snippet that gets shared.
- State the problem, the key finding, and the implication in that order.
- No product pitch. Frame around the insight, not the vendor.
- Write this LAST, after all other sections are complete.
- Knowledge: none (synthesize from completed sections)

**The Challenge** (400-800 words)
- Start from the buyer's world, not the industry's.
- Use persona pain points and verbatim language from PMM persona files.
- Quantify the problem where possible (cost, time, risk).
- Establish urgency without fear tactics.
- `> [Chart: quantification of the challenge - cost/risk/time data]`
- Knowledge: persona files, jtbd files

**Current Approaches and Their Limits** (400-800 words)
- Honest assessment. Acknowledge what works about existing approaches.
- Identify the structural gap - what the current approaches cannot solve by design.
- Do not name-call competitors. Use category references ("general-purpose AI tools", "static analysis platforms").
- Use field-tested messaging from `messaging/framework.md` for what resonates and what falls flat.
- Knowledge: messaging/framework, competitive files (if relevant)

**Solution Framework** (600-1000 words)
- Present the approach conceptually before introducing the product.
- Lead with the principle (e.g., "deterministic analysis as a foundation") not the feature.
- When the product enters, ground it in the framework - it's an implementation of the approach, not a sales pitch.
- `> [Chart: framework diagram or conceptual architecture]`
- Knowledge: teach_product_output, messaging/framework

**Evidence and Data** (600-1200 words)
- Original data, test results, or customer outcomes. This section earns the whitepaper its authority.
- Every claim gets a data point. No unsupported assertions.
- Include methodology transparency - how was this measured?
- Tables and charts are primary content here, not decoration.
- `> [Chart: primary evidence - test results, benchmark data, customer metrics]`
- `> [Chart: comparison data if applicable]`
- Knowledge: teach_product_output (for test data), specific evidence sources

**Implementation Considerations** (400-600 words, optional)
- Practical: deployment model, integration points, evaluation criteria.
- Include a POC evaluation framework if applicable.
- Address the "will this work in MY environment?" question directly.
- Knowledge: teach_product_output (deployment, integrations)

**Technology Deep Dive** (400-800 words, optional)
- For technical audiences. Can be skipped for executive-focused whitepapers.
- Architecture, language support, security model.
- Differentiate current capabilities from roadmap. Mark anything forward-looking explicitly.
- Knowledge: teach_product_output

**Conclusion and Next Steps** (200-400 words)
- Synthesize - do not restate. Reference the evidence, don't repeat it.
- 3-5 key takeaways as a scannable list.
- Clear next step: demo, POC, consultation, or further reading.
- Knowledge: none (synthesize from completed sections)

## Formatting Rules

- **Paragraphs**: 5-6 lines maximum. Use bullet points liberally in technical/implementation sections.
- **Data visualizations**: Include a `> [Chart: description]` placeholder every 2-3 pages. Minimum 3 charts per whitepaper.
- **Pull quotes**: One per major section from customer verbatims or key findings. Format as `> **"Quote text"** - Attribution`
- **Reading levels**: Executive Summary and Conclusion at grade 9-10. Technical sections at grade 11-12.
- **Citations**: Footnote format for data sources. Number sequentially. Include at end of document.
- **Modular design**: Each major section (2-7) should be extractable as a standalone blog post or LinkedIn carousel. Write section openings that work both in-context and standalone.

## Post-Write Agents

| Agent | Required? | Notes |
|-------|-----------|-------|
| `asset-reviewer` | Yes | Full quality review |
| `persona-reviewer` | Yes | Run with primary persona(s) |
| content scrubber | Yes | Universal post-processor |
| `linkedin-repurposer` | Optional | Generate promotion post |
| `newsletter-repurposer` | Optional | Generate email blurb |
| `internal-linker` | Optional | Only if publishing online (not gated PDF) |

## Quality Checklist

- [ ] Executive summary stands alone as a 1-page extract
- [ ] Every major claim has a data point, customer reference, or cited source
- [ ] No unsupported assertions or marketing-speak
- [ ] Challenge section uses buyer language (check against `words_that_work.md`)
- [ ] Current approaches section is honest about competitor strengths
- [ ] Solution framework leads with principle before product
- [ ] Evidence section includes methodology transparency
- [ ] Charts/data viz placeholders appear every 2-3 pages (minimum 3)
- [ ] No section restates what a prior section already covered
- [ ] Product claims verified against `teach_product_output.md` - no roadmap items presented as shipped
- [ ] Conclusion synthesizes (doesn't restate) and has a clear next step
- [ ] Reading level appropriate per section (exec vs technical)
- [ ] Content scrubber has been run (no em-dashes, no invisible Unicode)
