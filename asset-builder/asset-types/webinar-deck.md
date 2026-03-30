# Webinar Deck — Asset Type Template

## Metadata

- **Format**: deck
- **Target length**: 20-25 slides
- **Presentation time**: 30-45 minutes live or recorded
- **Tone**: Expert-peer, not boardroom. "Conference keynote" register — authoritative but approachable.
- **Brand voice**: Part 1 always. Part 2: always for product webinars, conditional for thought leadership, minimal for panel.
- **Primary personas**: `program_manager`, `architect` (override per project)

## Webinar Types

The `decisions.md` for each project specifies the type. The slide structure adapts accordingly.

| Type | [COMPANY] Presence | Demo? | Example |
|------|---------------|-------|---------|
| **Product webinar** | Central — [COMPANY] is the subject | Yes, live demo section | "Deep Dive: How [COMPANY] Powers AI Modernization" |
| **Thought leadership** | Light or absent — ideas lead, [COMPANY] mentioned in closing/CTA only | No | "Why Business Rules Are the Real Bottleneck in Legacy Modernization" |
| **Panel / industry** | Contextual — [COMPANY] referenced as one perspective among many | No | "The Future of Agentic Development: A Panel Discussion" |

## Knowledge Sources

Load from `$PMM_KNOWLEDGE_PATH`:

| File | When to Load | Approx Tokens |
|------|-------------|---------------|
| `config/teach_product_output.md` | Always for product webinars; conditional for thought leadership | ~8,400 |
| `knowledge_base/messaging/framework.md` | Always | ~5,300 |
| `knowledge_base/messaging/words_that_work.md` | Always | ~3,600 |
| `knowledge_base/personas/[target].md` | Per audience (1-2 files) | ~6,000 each |
| `knowledge_base/sales_enablement/objection_handling.md` | Product webinars only | ~4,500 |

**Per-slide loading**: Thought leadership slides load messaging/framework heavily and may not need product files at all. Panel slides load personas for each panelist perspective.

## Slide Structure

A webinar deck follows a narrative arc across six phases. Slides marked (product webinar only) are replaced per type as noted. All slides must work both live and as a recording.

| # | Slide | Job | Audience Reaction |
|---|-------|-----|-------------------|
| 1 | **Title** | Set the frame — establish topic, speaker, and what attendees will leave with | "This is worth my time" |
| 2 | **Agenda** | Preview the arc — build anticipation and commitment to stay | "I know what's coming" |
| 3 | **Speaker Intro** | Establish authority and relatable credibility, not a resume | "They've lived this problem" |
| 4 | **The Problem / Market Context** | Articulate the central tension at industry scale | "This is exactly what we're dealing with" |
| 5 | **Why Now** | Connect the problem to a specific, urgent moment in time | "This can't wait" |
| 6 | **The Stakes** | Make the cost of inaction concrete without fear tactics | "We need to get this right" |
| 7 | **What Most Teams Get Wrong** | Flip a common assumption or challenge received wisdom | "Hm, I hadn't thought about it that way" |
| 8 | **The Framework / Conceptual Approach** | Introduce a mental model that reframes the problem | "That's a useful way to think about this" |
| 9 | **Framework in Practice** | Ground the model with a concrete example or data point | "I can picture this in our environment" |
| 10 | **[Product / Evidence / Discussion]** *(type-specific, see below)* | Deep dive — product, case study, or panel discussion | "Now I understand how this actually works" |
| 11 | **[Product / Evidence / Discussion continued]** *(type-specific)* | | |
| 12 | **[Product / Evidence / Discussion continued]** *(type-specific)* | | |
| 13 | **[Demo transition — product webinar only]** | Hand off to live demo; set context and what to watch for | "I know what to focus on" |
| 14 | **[Demo — product webinar only]** | Placeholder slide displayed during live demo section | "Show me" |
| 15 | **[Post-demo / Synthesis]** | Reconnect demo or evidence back to the conceptual framework | "I see how it all fits together" |
| 16 | **Customer Story / Proof** | Named example with quantified outcome | "Others in our position have done this" |
| 17 | **Metrics / Data Point** | One headline number that anchors the business case | "The ROI is real" |
| 18 | **Competitive Context** *(optional — product webinar / thought leadership)* | Position the approach against alternatives honestly | "I understand why this is different" |
| 19 | **Objections Addressed** *(optional — product webinar only)* | Handle top objections before Q&A surfaces them | "They've anticipated my concern" |
| 20 | **Key Takeaways** | Distill to 3 headline truths the audience will remember | "I know what I just learned" |
| 21 | **Recommended Next Steps** | Concrete, non-pushy actions mapped to audience role | "I know what to do with this" |
| 22 | **Resources / Follow-up** | Point to companion assets: landing page, blog, guide, demo request | "I can go deeper" |
| 23 | **CTA** | One clear action — demo request, content download, or community join | "I know how to engage" |
| 24 | **Q&A** | Signal transition; not a blank slide | "Now I can ask" |
| 25 | **Thank You / Close** | Warm close with speaker contact and recording availability note | "I'm glad I attended" |

### Type-Specific Deep Dive (Slides 10-14)

**Product webinar** — Slides 10-12 are capability deep dives; Slide 13 is a demo transition; Slide 14 is a demo placeholder:
- Each deep-dive slide covers one capability mapped to one audience pain
- Slide 13: "Here's what we're going to show you in the demo — watch for [X]"
- Slide 14: Simple title card + context bullets displayed during demo

**Thought leadership** — Slides 10-12 are evidence and case study deep dives; no demo slides:
- Each slide develops one proof point for the framework
- Replace demo transition and demo placeholder with a third evidence slide

**Panel / industry** — Slides 10-12 are discussion prompts with one per panelist or topic rotation; no demo slides:
- Each slide poses a question or tension point for the panel to address
- Replace demo slides with a closing synthesis from the moderator

### Slide Details

**Slide 1: Title**
- Headline is the webinar title — a bold claim or sharp question, not a product description.
- Subheadline: who this is for + what they'll leave with (one sentence).
- Speaker name(s) and title(s).
- Visual direction: strong single image or conceptual graphic; [COMPANY] branding present but not dominant.
- Companion asset note: headline and subheadline seed the webinar invite email subject and preview text.
- Knowledge: messaging/framework

**Slide 2: Agenda**
- 4-6 agenda items as short active phrases, not topic labels.
- Estimated time per section optional but useful for longer webinars.
- Frame as "by the end of this session, you'll know how to…" rather than "we will cover…"
- Visual direction: simple numbered list with light iconography; no tables.
- Knowledge: none

**Slide 3: Speaker Intro**
- 3-4 lines maximum. Lead with what makes the speaker credible for *this* topic, not a full bio.
- One personal or field anecdote hook if available.
- For panel: introduce all speakers here; 2-3 lines each.
- Visual direction: headshot(s) with name and title overlay; clean, modern layout.
- Knowledge: none

**Slide 4: The Problem / Market Context**
- Headline states the industry-level tension at scale.
- 3-4 pain articulations using verbatim-style language from `words_that_work.md`.
- One market signal or data point to anchor the problem externally.
- Visual direction: market data visualization, industry landscape graphic, or before-state illustration.
- Knowledge: messaging/framework, words_that_work

**Slide 5: Why Now**
- Headline connects the problem to a specific inflection point (technology shift, regulatory pressure, organizational trigger).
- 3 drivers: present as forces, not warnings.
- Avoid fear framing; use factual urgency.
- Visual direction: timeline, trend line, or market moment graphic.
- Knowledge: messaging/framework

**Slide 6: The Stakes**
- Headline names the cost of staying on the current path.
- 2-3 concrete cost dimensions: time, risk, competitive disadvantage.
- At least one quantified point.
- Visual direction: contrast illustration (current state vs. ideal state), or single headline metric.
- Knowledge: messaging/framework, words_that_work

**Slide 7: What Most Teams Get Wrong**
- Headline challenges a specific, common assumption.
- Flip format: "Teams believe [X]. The reality is [Y]."
- Keep this slide intellectually honest — the audience may believe the thing you're challenging.
- Visual direction: split panel (myth vs. reality), or single provocative statement with supporting context.
- Knowledge: messaging/framework, personas

**Slide 8: The Framework / Conceptual Approach**
- Introduce the mental model that reframes how the audience should think about the problem.
- Name the framework if it has a name; keep it simple (3 components max).
- Product enters here only for product webinars; thought leadership keeps it tool-agnostic.
- Visual direction: framework diagram, 2x2, or layered architecture graphic.
- Knowledge: messaging/framework, teach_product_output (product webinar only)

**Slide 9: Framework in Practice**
- Ground the model in a concrete example — a real use case, anonymized scenario, or data point.
- Show how the framework applies, not just what it is.
- 3-4 bullets or a brief step-by-step application.
- Visual direction: annotated example, before/after flow, or application diagram.
- Knowledge: teach_product_output (product webinar), personas

**Slides 10-12: Deep Dive (type-specific)**
- See "Type-Specific Deep Dive" section above.
- Each slide covers one idea at depth. Do not combine multiple points on one slide.
- Visual direction: product screenshot, evidence table, or discussion prompt card (per type).
- Knowledge: teach_product_output (product webinar), personas

**Slide 13: Demo Transition (product webinar only)**
- Headline: "Now let's see this in action."
- 2-3 bullets telling the audience what to watch for specifically during the demo.
- Sets up success criteria so the demo reads as evidence, not a tour.
- Speaker notes: explicit handoff language — "I'm going to share my screen now and walk you through [X]."
- Visual direction: simple transition card; title + context bullets only.
- Knowledge: teach_product_output

**Slide 14: Demo Placeholder (product webinar only)**
- Displayed on screen while live demo runs.
- Headline: "Live Demo: [capability being shown]"
- 2-3 "watch for" bullets repeated from Slide 13.
- Speaker notes: full demo script outline — what to show, in what order, with recovery notes if something fails.
- Visual direction: branded placeholder with demo title; uncluttered.
- Knowledge: teach_product_output

**Slide 15: Post-Demo / Synthesis**
- Reconnect what was just shown (or the evidence just presented) back to the conceptual framework from Slide 8.
- 2-3 synthesis points: "What you just saw demonstrates [framework principle]."
- Speaker notes: carry the bridging narrative explicitly.
- Visual direction: abbreviated version of the framework diagram from Slide 8, annotated with demo callouts.
- Knowledge: messaging/framework

**Slide 16: Customer Story / Proof**
- Named account if available; anonymized industry reference if not.
- One-sentence situation + 2-3 quantified outcomes.
- One direct customer quote (attributed: name, title, company or "a [industry] organization").
- Companion asset note: this story seeds the webinar follow-up email and landing page proof section.
- Visual direction: customer logo (if approved), quote card, metric callout boxes.
- Knowledge: personas (for segment-appropriate proof selection)

**Slide 17: Metrics / Data Point**
- One headline number that anchors the business case.
- Supporting context (how measured, sample size, or source) in speaker notes, not on slide.
- Visual direction: large typographic metric with minimal framing; single-focus layout.
- Knowledge: messaging/framework

**Slide 18: Competitive Context (optional)**
- For product webinars: position [COMPANY]'s structural advantage vs. alternatives honestly.
- For thought leadership: compare approaches or frameworks, tool-agnostic.
- Omit for panel — panelists introduce their own perspectives.
- 3 evaluation criteria that favor the recommended approach; be specific, not generic.
- Visual direction: comparison table or approach contrast diagram.
- Knowledge: messaging/framework, competitive files (product webinar)

**Slide 19: Objections Addressed (optional — product webinar only)**
- Handle 2-3 top objections proactively, before Q&A.
- Format: "You might be wondering…" + direct, honest answer.
- Pull from `objection_handling.md` for the target audience.
- Visual direction: Q&A card format or simple two-column layout.
- Knowledge: objection_handling, personas

**Slide 20: Key Takeaways**
- Exactly 3 takeaways. No more.
- Each takeaway is a complete, standalone sentence — not a topic label.
- Takeaways should be memorable and quotable.
- Companion asset note: these three lines become the webinar landing page "what you'll learn" bullets and the follow-up email subject line candidates.
- Visual direction: three cards or numbered statement blocks; clean and high-contrast.
- Knowledge: messaging/framework

**Slide 21: Recommended Next Steps**
- 2-3 concrete actions, mapped to audience role where possible.
- Non-pushy: frame as "if you want to go deeper" rather than a sales sequence.
- Differentiate actions by readiness: explore → evaluate → engage.
- Visual direction: tiered action graphic or simple bulleted list with role icons.
- Knowledge: personas

**Slide 22: Resources / Follow-up**
- List 3-5 companion resources: whitepaper, blog post, guide, demo request link.
- Include the webinar recording link placeholder (fill post-event).
- Companion asset note: this list drives the follow-up email resource section.
- Visual direction: resource cards with titles and type labels; clean grid.
- Knowledge: none

**Slide 23: CTA**
- One clear action. Match to webinar type:
  - Product webinar: "Request a demo" or "Start a POC"
  - Thought leadership: "Download the guide" or "Read the full report"
  - Panel: "Join the community" or "Continue the conversation"
- QR code or short URL acceptable.
- Visual direction: single CTA button prominence; no competing elements.
- Knowledge: none

**Slide 24: Q&A**
- Headline: "Questions?" — not a blank slide.
- 2-3 "if you're wondering about X, ask us" prompts to seed the Q&A.
- Speaker notes: pre-written answers to the 3 most likely questions.
- Visual direction: simple branded card; speaker photo(s) optional.
- Knowledge: objection_handling (product webinar)

**Slide 25: Thank You / Close**
- Warm close: thank the audience for their time and engagement.
- Recording availability: "This webinar will be available at [URL] within [X] business days."
- Speaker contact information (LinkedIn or email).
- Visual direction: clean close card; [COMPANY] branding at full weight.
- Knowledge: none

## Markdown Output Format

Each slide follows this format:

```markdown
---

## Slide [N]: [Title]
**Type**: [Title / Agenda / Content / Framework / Demo / Proof / Synthesis / CTA]
**Webinar type note**: [If this slide differs by webinar type, note the variation here]

**Headline**: [10-15 words; confident and declarative]

**Subheadline**: [15-25 words, optional]

- Bullet point one (10-15 words)
- Bullet point two
- Bullet point three

> **Speaker notes**: [100-200 words. This carries the full narrative the presenter speaks. Include transition to next slide. For demo slides, include demo script outline.]

> **Visual direction**: [What should be on screen: diagram type, screenshot reference, layout notes, image generation prompt if applicable.]

> **Companion asset note**: [If this slide maps to webinar landing page talking points, invite email hooks, or follow-up email content, note the connection here.]
```

## Formatting Rules

- **Slide count**: 20-25 slides. Thought leadership and panel can tighten to 20; product webinars with a live demo section typically run 23-25.
- **One idea per slide**: If a slide makes two points, split it.
- **Headlines do the work**: Someone reading only headlines should understand the full story arc.
- **Bullet discipline**: 3-5 bullets per content slide. Each bullet is 10-15 words max.
- **Speaker notes are mandatory**: Every slide gets 100-200 words of speaker notes. Notes carry the narrative; slides carry the visual anchor.
- **No polls or interactive beats**: Q&A at the end only. Do not embed audience participation prompts mid-presentation.
- **Demo transitions must be explicit**: For product webinars, Slide 13 and Slide 14 must have explicit handoff and recovery language in speaker notes.
- **Recording-friendly**: Every slide must be fully self-explanatory without a live presenter. Assume 60% of viewers will watch the recording.
- **Companion asset notes**: Where slides map to landing page copy, invite email, or follow-up email, note the connection explicitly.
- **No "Thank You" slide as a closer**: Slide 25 is a warm close, not a dead end — recording link and speaker contact are required.

## Post-Write Agents

| Agent | Required? | Notes |
|-------|-----------|-------|
| `asset-reviewer` | Yes | Evaluate narrative arc, headline progression, information density |
| `persona-reviewer` | Yes | Run with primary audience persona(s) |
| content scrubber | Yes | Universal post-processor |
| `linkedin-repurposer` | Conditional | Use for thought leadership and product webinars; skip for panel |
| `newsletter-repurposer` | Conditional | Use if webinar maps to a newsletter send |

## Quality Checklist

- [ ] Slide count between 20-25
- [ ] Webinar type declared in `decisions.md` and deck structure matches (product / thought leadership / panel)
- [ ] Reading only headlines tells the complete story arc
- [ ] Every slide has one idea, not two
- [ ] All content slides have 3-5 bullets (10-15 words each)
- [ ] Every slide has speaker notes (100-200 words)
- [ ] No polls or interactive beats mid-presentation
- [ ] Demo transition slide (13) and demo placeholder (14) present for product webinars; replaced correctly for other types
- [ ] Slide 20 (Takeaways) has exactly 3 memorable, standalone sentences
- [ ] Proof slide (16) has a named or attributed reference with quantified outcomes
- [ ] Companion asset notes present on Slides 1, 16, 20, and 22
- [ ] Recording-friendly: every slide readable without live presenter
- [ ] Speaker notes on demo slides include script outline and recovery notes (product webinar only)
- [ ] CTA on Slide 23 matches webinar type
- [ ] Slide 25 includes recording URL placeholder and speaker contact
- [ ] Brand voice level matches webinar type (full for product, conditional for thought leadership, minimal for panel)
- [ ] Product claims verified against `teach_product_output.md` (product webinar only)
- [ ] Content scrubber has been run
