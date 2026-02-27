# Sales Deck — Asset Type Template

## Metadata

- **Format**: deck
- **Target length**: 12-16 slides (14 is the sweet spot)
- **Presentation time**: 20-30 minutes with discussion
- **Tone**: Confident, direct, buyer-centric. "Boardroom" register from brand voice.
- **Brand voice**: Part 1 always. Part 2 always (sales decks are inherently about Swimm).
- **Primary personas**: `architect`, `program_manager` (override per project)

## Knowledge Sources

Load from `$PMM_KNOWLEDGE_PATH`:

| File | When to Load | Approx Tokens |
|------|-------------|---------------|
| `config/teach_product_output.md` | Always | ~8,400 |
| `knowledge_base/messaging/framework.md` | Always | ~5,300 |
| `knowledge_base/messaging/words_that_work.md` | Always | ~3,600 |
| `knowledge_base/sales_enablement/objection_handling.md` | Always | ~4,500 |
| `knowledge_base/personas/[target].md` | Per audience (1-2 files) | ~6,000 each |

**Per-slide loading**: Most slides need messaging/framework + product. Competitive slides additionally load relevant competitor files. Persona-heavy slides load the target persona.

## Slide Structure

A sales deck follows this sequence. Slides marked (personalize) change per audience segment. Slides marked (optional) can be omitted for shorter presentations.

| # | Slide | Job | Audience Reaction |
|---|-------|-----|--------------------|
| 1 | **Title** | Set the frame - this is about their problem, not our product | "This might be relevant to me" |
| 2 | **The Problem** | Mirror their pain precisely | "They get it" |
| 3 | **Why Now** | Urgency without fear tactics | "This is timely" |
| 4 | **The Gap** | What existing approaches can't solve | "That's exactly where we're stuck" |
| 5 | **The Approach** | Conceptual solution before product | "That makes sense" |
| 6 | **How Swimm Works** | Product overview - concrete, not abstract | "Show me" |
| 7-9 | **Capability Deep Dives** (2-3 slides) | Key capabilities matched to their pain | "This would solve [specific problem]" |
| 10 | **Differentiation** | Why this vs alternatives | "Why not just use [competitor]?" |
| 11 | **Proof** (personalize) | Social proof matched to their segment | "Others like us trust this" |
| 12 | **Enterprise Readiness** | Security, deployment, scale | "Can this work in our environment?" |
| 13 | **Engagement Model** (optional, personalize) | How to get started - POC, pilot, pricing context | "What does this look like practically?" |
| 14 | **Next Step** | One clear action | "I know what to do next" |

### Slide Details

**Slide 1: Title**
- Headline frames the conversation around the buyer's challenge, not Swimm.
- Subheadline provides context: who this is for and what they'll learn.
- No product logo dominating. Swimm branding present but secondary.
- Visual direction: clean, professional, one hero graphic or conceptual image.
- Knowledge: messaging/framework (for positioning framing)

**Slide 2: The Problem** (personalize)
- Headline states the problem in the buyer's own language (use `words_that_work.md`).
- 3-4 pain points as short statements. Use verbatim customer language from persona files.
- One quantified impact point (cost, time, risk).
- Visual direction: simple icons or a before-state illustration.
- Knowledge: personas, words_that_work

**Slide 3: Why Now**
- Headline connects to a market trigger or organizational moment.
- 3 drivers: regulatory, competitive, or operational pressures.
- Frame urgency factually, not with fear tactics.
- Visual direction: timeline, trend graphic, or market data point.
- Knowledge: messaging/framework

**Slide 4: The Gap**
- Headline identifies the structural limitation of current approaches.
- 2-3 comparison points: what current tools do well and where they structurally fail.
- Position the gap as architectural, not a feature deficit.
- Be fair to alternatives - dishonesty loses trust here.
- Visual direction: gap visualization, before/after, or comparison matrix.
- Knowledge: messaging/framework, competitive files (if naming specific alternatives)

**Slide 5: The Approach**
- Headline introduces the principle before the product ("deterministic understanding as the foundation").
- 3 key elements of the approach, framed as requirements for solving the problem.
- Product enters naturally as the implementation of these requirements.
- Visual direction: conceptual architecture or framework diagram.
- Knowledge: teach_product_output, messaging/framework

**Slide 6: How Swimm Works**
- Headline is action-oriented: what Swimm does, in one sentence.
- 4-5 step walkthrough of the core experience: ingest -> analyze -> navigate -> collaborate -> deliver.
- Each step is one line. Speaker notes carry the detail.
- Visual direction: product screenshot sequence or workflow diagram.
- Knowledge: teach_product_output

**Slides 7-9: Capability Deep Dives** (personalize)
- Each slide covers ONE capability matched to ONE buyer pain point.
- Headline: what it solves (buyer language), not what it's called (product language).
- 3-4 bullets: what it does, how it helps, what differentiates it.
- One proof point or example per slide.
- Visual direction: product screenshot or output example.
- Knowledge: teach_product_output, relevant persona

**Slide 10: Differentiation**
- Headline positions Swimm's structural advantage.
- 3 differentiation points. Lead with evaluation criteria that favor Swimm's approach.
- Handle the top objection for this audience (from `objection_handling.md`).
- Be specific: "deterministic vs probabilistic" not "better than competitors."
- Visual direction: comparison table or conceptual contrast diagram.
- Knowledge: messaging/framework, objection_handling, competitive files

**Slide 11: Proof** (personalize)
- Headline cites a specific result or customer reference.
- Named account if available, anonymized industry reference if not.
- 1-2 proof point numbers (quantified outcomes).
- One customer quote (attributed: name, title, company).
- Visual direction: customer logo, quote card, metric callouts.
- Knowledge: personas (for segment-appropriate proof)

**Slide 12: Enterprise Readiness**
- Headline reassures: "Built for enterprise requirements."
- 4-6 checklist items: on-prem deployment, SOC 2, ISO 27001, BYOLLM, language coverage, IDE plugins.
- This slide exists to prevent the "sounds great but won't work here" objection.
- Visual direction: certification badges, icon checklist, deployment diagram.
- Knowledge: teach_product_output (deployment, security sections)

**Slide 13: Engagement Model** (optional, personalize)
- How to get started: POC structure, timeline, evaluation criteria.
- Reference the POC evaluation scorecard from product knowledge.
- Pricing context if appropriate (LoC-based, tiered) - not exact numbers unless post-NDA.
- Visual direction: timeline or process graphic.
- Knowledge: teach_product_output (pricing, user journeys)

**Slide 14: Next Step**
- Headline is a specific action, not "Thank You" or "Questions?"
- One clear CTA: "Schedule a technical deep dive" / "Start a 2-week POC" / "Meet with your solutions architect."
- Contact information and follow-up commitment.
- Visual direction: clean, single CTA button prominence. No clutter.
- Knowledge: none

## Markdown Output Format

Each slide follows this format:

```markdown
---

## Slide [N]: [Title]
**Type**: [Title / Content / Comparison / Proof / CTA]

**Headline**: [8-12 words, buyer-centric]

**Subheadline**: [15-25 words, optional]

- Bullet point one (10-15 words)
- Bullet point two
- Bullet point three

> **Speaker notes**: [50-150 words. This carries the narrative - what the presenter says that the slide doesn't show. Include transition to next slide.]

> **Visual direction**: [What should be on screen: diagram type, screenshot reference, icon suggestions, layout notes.]

> **Personalization note**: [If this slide changes per segment, describe what changes and for whom.]
```

## Formatting Rules

- **Slide count**: 12-16 slides. 14 is the target. If you need more, combine content. If you need fewer, the presentation may lack substance.
- **One idea per slide**: If a slide makes two points, split it.
- **Headlines do the work**: Someone reading only headlines should understand the full story arc.
- **Bullet discipline**: 3-5 bullets per content slide. Each bullet is 10-15 words max.
- **Speaker notes are mandatory**: Every slide gets 50-150 words of speaker notes. The notes carry the narrative; slides carry the visual anchor.
- **Personalization markers**: Slides marked (personalize) include a `> **Personalization note**:` explaining what changes per segment.
- **Internal resale test**: Every slide must be skim-able and self-explanatory without a presenter. The prospect's champion will present this to their boss.
- **No "Thank You" slide**: End with a next step, not a pleasantry.

## Post-Write Agents

| Agent | Required? | Notes |
|-------|-----------|-------|
| `asset-reviewer` | Yes | Evaluate headline progression, information density, narrative arc |
| `persona-reviewer` | Yes | Run with target sales persona(s) |
| content scrubber | Yes | Universal post-processor |
| `linkedin-repurposer` | No | Sales decks don't typically get LinkedIn promotion |
| `newsletter-repurposer` | No | Not applicable |

## Quality Checklist

- [ ] Slide count between 12-16
- [ ] Reading only headlines tells the complete story
- [ ] Every slide has one idea, not two
- [ ] All content slides have 3-5 bullets (10-15 words each)
- [ ] Every slide has speaker notes (50-150 words)
- [ ] Problem slide uses buyer's own language (checked against `words_that_work.md`)
- [ ] Differentiation slide handles the top audience objection
- [ ] Proof slide has a named/attributed reference
- [ ] Enterprise readiness covers deployment, security, and scale
- [ ] Personalized slides are marked with personalization notes
- [ ] No slide requires the presenter to explain what it means (internal resale test)
- [ ] Last slide is a specific next step, not "Thank You"
- [ ] Product claims verified against `teach_product_output.md`
- [ ] Content scrubber has been run
