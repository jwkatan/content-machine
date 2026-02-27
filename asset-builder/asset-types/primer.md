# Primer — Asset Type Template

## Metadata

- **Format**: prose
- **Target length**: 800-1500 words (2-3 pages)
- **Reading time**: 5-7 minutes (designed to be read in one sitting)
- **Tone**: Informative reference - accessible but not blog-casual. "Confident Expert Colleague" from brand voice.
- **Brand voice**: Part 1 always. Part 2 when Swimm is the subject.
- **Primary personas**: Dual-audience - serves both decision-makers and technical evaluators simultaneously.

## Knowledge Sources

Load from `$PMM_KNOWLEDGE_PATH`:

| File | When to Load | Approx Tokens |
|------|-------------|---------------|
| `config/teach_product_output.md` | Always | ~8,400 |
| `knowledge_base/messaging/framework.md` | Always | ~5,300 |

**Note**: Primers are intentionally lightweight on PMM knowledge. They introduce a topic, not sell a product. Total context: ~13K tokens.

## Section Structure

A primer has exactly 4 sections. No optional sections - brevity is the format's strength.

| # | Section | Job | Reader's Question |
|---|---------|-----|--------------------|
| 1 | **What It Is** | Define the concept clearly and precisely | "What are we talking about?" |
| 2 | **Why It Matters** | Establish relevance to the reader's world | "Why should I care?" |
| 3 | **How It Works** | Make the mechanism concrete and understandable | "How does this actually work?" |
| 4 | **Next Steps** | Point to deeper resources | "Where do I go from here?" |

### Section Details

**What It Is** (200-400 words)
- Lead with a crisp 1-2 sentence definition. No throat-clearing.
- Provide enough context for someone encountering this topic for the first time.
- If the topic involves 3+ domain-specific terms, include a sidebar glossary:
  ```
  > **Key Terms**
  > - **Term**: Definition
  > - **Term**: Definition
  ```
- Distinguish this concept from adjacent/confusable concepts.
- Knowledge: teach_product_output (for accurate technical grounding)

**Why It Matters** (200-400 words)
- Frame around business impact, not technical novelty.
- Connect to real organizational pain: cost, risk, speed, knowledge loss.
- One concrete example or scenario that makes the stakes tangible.
- Serve both audiences: the decision-maker cares about outcomes, the technical evaluator cares about feasibility.
- Knowledge: messaging/framework (for what resonates)

**How It Works** (300-500 words)
- Conceptual explanation, not a product walkthrough.
- Use a simple progression: input -> process -> output.
- One diagram or visual placeholder: `> [Diagram: conceptual workflow or architecture]`
- If Swimm is relevant, introduce it as "one approach" within the broader concept - not as the point of the section.
- Keep technical depth appropriate for a mixed audience - enough for the architect to nod, not so much that the CIO checks out.
- Knowledge: teach_product_output (if product is relevant)

**Next Steps** (100-200 words)
- 3-4 paths forward, matched to different reader needs:
  - "Read the full whitepaper on [topic]" (deeper learning)
  - "See a live demo" (evaluation)
  - "Talk to our team about [specific use case]" (engagement)
  - "Explore the [related resource]" (adjacent learning)
- Clear, specific links - not vague "learn more" language.
- Knowledge: none

## Formatting Rules

- **Total word count**: 800-1500 words. Do not exceed 1500. If the topic needs more depth, it's a whitepaper, not a primer.
- **Paragraphs**: 3-4 sentences maximum. Scannable by design.
- **One diagram**: Include exactly one `> [Diagram: description]` placeholder in the "How It Works" section.
- **Glossary**: If 3+ domain terms are introduced, include the sidebar glossary in "What It Is."
- **No footnotes**: Primers don't cite sources. If a claim needs citation, it's too detailed for this format.
- **Tone consistency**: Informative throughout. This is a reference document, not a blog post. No casual transitions ("So, let's dive in..."), no rhetorical questions as hooks.

## Post-Write Agents

| Agent | Required? | Notes |
|-------|-----------|-------|
| `asset-reviewer` | Yes | Full quality review |
| `persona-reviewer` | Yes | Run with dual audience in mind |
| content scrubber | Yes | Universal post-processor |
| `linkedin-repurposer` | Optional | Good for awareness posts |
| `newsletter-repurposer` | Optional | Primers make strong email content |

## Quality Checklist

- [ ] Total word count between 800-1500 words
- [ ] "What It Is" opens with a crisp 1-2 sentence definition
- [ ] Glossary sidebar included if 3+ domain terms are introduced
- [ ] "Why It Matters" connects to business impact, not just technical interest
- [ ] "How It Works" includes exactly one diagram placeholder
- [ ] Both decision-makers and technical evaluators can follow the entire document
- [ ] "Next Steps" includes 3-4 specific paths (not vague "learn more")
- [ ] No marketing-speak or product pitch dominates any section
- [ ] Product claims verified against `teach_product_output.md` if product is mentioned
- [ ] Tone is informative reference, not blog-casual
- [ ] Content scrubber has been run
