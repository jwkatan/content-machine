# Partner Brief — Asset Type Template

## Metadata

- **Format**: prose
- **Target length**: 2500-4000 words (6-10 pages)
- **Reading time**: 12-20 minutes
- **Tone**: Peer-to-peer between companies. Not vendor-to-buyer. The reader is a colleague at a partner organization, not a prospect. Confident and collaborative — "here's how we win together" not "here's why you should sell us."
- **Brand voice**: Part 1 always. Part 2 when describing [COMPANY]'s specific capabilities (but frame within the joint value prop, not standalone).
- **Primary personas**: `partner_sales` (partner's sales team), `partner_architect` (partner's solution architects), `partner_practice_lead` (partner's practice leads) — these are NOT end-buyer personas. Override per partner engagement.

## Knowledge Sources

Load from `$PMM_KNOWLEDGE_PATH`:

| File | When to Load | Approx Tokens |
|------|-------------|---------------|
| `config/teach_product_output.md` | Always | ~8,400 |
| `knowledge_base/messaging/framework.md` | Always | ~5,300 |
| `knowledge_base/messaging/words_that_work.md` | Always | ~3,600 |
| `knowledge_base/partners/[partner_name].md` | When partner-specific file exists | ~4-8K |
| `knowledge_base/personas/[end_buyer].md` | For joint use case framing (1-2 files) | ~6,000 each |
| `knowledge_base/jtbd/modernization.md` | When joint use cases involve modernization | ~6,300 |
| `knowledge_base/jtbd/maintenance.md` | When joint use cases involve maintenance | ~6,300 |

**Per-section loading**: The outline (Phase 1) tags each section with which files it needs. Phase 2 loads only the tagged files into each section's writing subagent.

**Note on partner files**: If no partner-specific file exists in `$PMM_KNOWLEDGE_PATH/knowledge_base/partners/`, the brief should be written as a generic partner template. Flag to the user that a partner-specific knowledge file would strengthen the output.

## Section Structure

A partner brief includes 7 sections in this sequence. No optional sections — partner audiences expect completeness. Each section serves at least two of the three partner reader types (sales, architects, practice leads).

| # | Section | Job | Partner's Question | Primary Reader |
|---|---------|-----|--------------------|----------------|
| 1 | **Partnership Overview** | Define the joint value prop — what neither company delivers alone | "What's in this for us?" | Practice leads |
| 2 | **Partner Positioning** | How the partner should frame this to their clients | "How do I talk about this?" | Sales |
| 3 | **Joint Use Cases** | 2-3 scenarios where partner + product creates measurable client value | "Where does this fit in our engagements?" | Sales, Architects |
| 4 | **Technical Integration Points** | How the product fits into the partner's delivery methodology | "How does this work inside our delivery model?" | Architects |
| 5 | **Co-Marketing Opportunities** | Available assets, joint events, case study potential | "What support do we get?" | Practice leads |
| 6 | **Partner Talk Track** | Condensed positioning: opener, key points, objection handling | "Give me something I can use Monday" | Sales |
| 7 | **Getting Started** | Concrete next steps for activating the partnership | "What do we do now?" | All |

### Section Details

**Partnership Overview** (300-500 words)
- Open with the joint value proposition — what the two companies deliver together that neither delivers alone. This is NOT a product overview.
- Frame the partnership around a shared market opportunity, not a vendor relationship.
- Include: market context (why this partnership matters now), complementary strengths (what each party brings), combined value (what the client gets from the joint offering).
- Avoid: product feature lists, anything that reads like "sell our product for us," unilateral value props that only benefit one side.
- Address the practice lead's question: "Is this worth investing my team's time?"
- `> [Chart: partnership value chain — what each party contributes and what the client receives]`
- Knowledge: messaging/framework, partner file (if available)

**Partner Positioning** (400-600 words)
- This section is fundamentally different from direct sales positioning. The partner is not the buyer — they are the channel.
- Reframe the product's value through the partner's lens: how does this make the partner's existing engagements more valuable, more sticky, or more differentiated?
- Include: positioning statement (2-3 sentences the partner can use verbatim), key differentiators framed as partner advantages (not product features), how this compares to alternatives the partner might also carry or recommend.
- Provide "when to bring this up" triggers — specific client situations or conversations where the partner should introduce the joint offering.
- Avoid: direct-sales language, positioning that competes with the partner's own services, anything that makes the partner feel like a reseller rather than a co-solutioner.
- Knowledge: messaging/framework, words_that_work, partner file

**Joint Use Cases** (600-900 words)
- 2-3 use cases. Each follows a strict structure:
  - **Client situation**: The scenario the partner encounters in their engagement (use the end-buyer persona language, not internal language).
  - **Joint approach**: How partner + product work together to address it. Be specific about who does what.
  - **Expected outcome**: Quantified where possible. Frame as outcomes the partner can cite in their own proposals.
- Use cases must be scenarios where the partnership creates value — not scenarios where the product alone solves the problem.
- Each use case should map to a recognizable engagement type the partner already delivers (e.g., modernization assessment, platform migration, managed services onboarding).
- Avoid: use cases that sideline the partner, outcomes that only benefit the end client without strengthening the partner's position.
- Knowledge: teach_product_output, personas (end-buyer), jtbd files (per use case), partner file

**Technical Integration Points** (400-600 words)
- How the product fits into the partner's delivery methodology — not how the product works in isolation.
- Include: integration with partner delivery phases (discovery, assessment, implementation, handoff), deployment models that work within partner-managed environments, data and access requirements the partner's architects need to plan for, how the product complements (not replaces) the partner's existing toolchain.
- Use a phased structure matching typical partner delivery: Discovery → Assessment → Implementation → Ongoing Support.
- Avoid: deep product architecture (link to technical docs instead), anything that implies the partner's architects can't handle the integration, requirements that would disrupt the partner's standard delivery process.
- `> [Chart: integration touchpoints across partner delivery phases]`
- Knowledge: teach_product_output, partner file

**Co-Marketing Opportunities** (300-500 words)
- Concrete, not aspirational. List what's available now.
- Include: available co-branded assets (with asset types and access details), joint event opportunities (webinars, conference sessions, workshops), case study development process (how to nominate a joint client, timeline, approval flow), MDF or co-investment details if applicable, partner portal or resource hub access.
- Frame each opportunity with the effort required from the partner and the expected return.
- Avoid: vague promises ("we'll work together on marketing"), listing programs that don't exist yet, co-marketing that requires disproportionate partner investment.
- Knowledge: partner file (if available)

**Partner Talk Track** (400-600 words)
- This is the section the partner's sales rep prints and takes into their next client meeting. It must be immediately usable.
- Structure:
  - **Opener** (2-3 sentences): How to introduce the topic naturally within an existing client conversation. Not a cold pitch — a warm pivot from a discussion the partner is already having.
  - **Positioning statement** (2-3 sentences): The joint value prop in language the partner says out loud to their client.
  - **Three key points**: One sentence each. These are the partner's talking points — framed as what the partner delivers (with the product), not what the product does.
  - **Objection handling** (3-4 objections): Objections specific to the partner context — not end-buyer objections. Examples: "We already have a tool for that" (partner's client), "This adds complexity to our delivery" (partner's architects), "What's the margin for us?" (partner's sales leadership).
  - **Closing/transition**: How to move from conversation to next step (joint discovery call, technical assessment, POC).
- Avoid: corporate-speak the partner would never say out loud, objection responses that throw the partner under the bus, talk tracks that only work for one partner reader type.
- Knowledge: messaging/framework, words_that_work, objection_handling (adapt for partner context), partner file

**Getting Started** (200-300 words)
- Concrete activation steps. Not "contact us" — specific actions with owners and timelines.
- Include: partner enablement resources (training, certification if applicable), technical sandbox or demo environment access, first joint engagement playbook (how to identify and pursue the first joint deal), key contacts (partner manager, solutions architect, marketing lead).
- 3-5 numbered steps. Each step has an owner (partner or vendor) and a timeframe.
- Knowledge: partner file (if available)

## Formatting Rules

- **Paragraphs**: 4-5 lines maximum. Use bullet points in technical and co-marketing sections.
- **Data visualizations**: Include a `> [Chart: description]` placeholder in Partnership Overview and Technical Integration Points at minimum. Additional charts welcome in Joint Use Cases.
- **Verbatim blocks**: Partner Positioning and Partner Talk Track should include quoted blocks (`> "..."`) that the partner can use word-for-word. Mark these clearly as ready-to-use language.
- **Reading levels**: Partnership Overview and Co-Marketing at grade 9-10. Technical Integration Points at grade 11-12. Talk Track at grade 8-9 (conversational).
- **Three-audience markers**: Each section heading includes a parenthetical noting the primary reader type. This helps partners route the document internally.
- **No footnotes or citations**: Partner briefs are operational documents, not research papers. Claims should be substantiated in the text itself or linked to supporting assets.
- **Modular design**: The Partner Talk Track and Joint Use Cases sections should be extractable as standalone leave-behinds. Write their openings to work both in-context and standalone.

## Post-Write Agents

| Agent | Required? | Notes |
|-------|-----------|-------|
| `asset-reviewer` | Yes | Focus on partner-centricity — flag anywhere the brief reads like a sales pitch to the partner |
| `persona-reviewer` | Yes | Run with partner personas. Verify the brief serves all three reader types without becoming three documents |
| content scrubber | Yes | Universal post-processor |
| `linkedin-repurposer` | No | Partner briefs are not public-facing |
| `newsletter-repurposer` | No | Not applicable |

## Quality Checklist

- [ ] Partnership Overview frames a joint value prop, not a product pitch
- [ ] Partner Positioning is framed through the partner's lens, not direct-sales language
- [ ] Each joint use case has all three elements: client situation, joint approach, expected outcome
- [ ] Joint use cases show the partner as essential, not optional
- [ ] Technical integration maps to partner delivery phases, not product architecture
- [ ] Co-marketing section lists concrete, currently-available opportunities
- [ ] Talk track is conversational and usable verbatim — read it out loud to verify
- [ ] Objection handling addresses partner-context objections, not end-buyer objections
- [ ] Getting Started section has numbered steps with owners and timeframes
- [ ] No section reads like "sell our product for us" — the tone is peer-to-peer throughout
- [ ] All three partner reader types (sales, architects, practice leads) are served
- [ ] Document routes internally — each section's primary reader is clear
- [ ] Product claims verified against `teach_product_output.md`
- [ ] Content scrubber has been run
