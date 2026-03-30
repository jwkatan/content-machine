# One-Pager — Asset Type Template

## Metadata

- **Format**: layout (distinct from prose and deck — zones on a fixed 2-page canvas, front + back)
- **Target length**: 500-800 words (exactly 2 pages, front + back)
- **Reading time**: 2-3 minutes
- **Tone**: Confident, concise, sales-enablement. "Boardroom" register from brand voice. Every word earns its place.
- **Brand voice**: Part 1 always. Part 2 always (one-pagers are about [COMPANY]).
- **Primary personas**: `architect`, `program_manager` (override per project)

## Knowledge Sources

Load from `$PMM_KNOWLEDGE_PATH`:

| File | When to Load | Approx Tokens |
|------|-------------|---------------|
| `config/teach_product_output.md` | Always | ~8,400 |
| `knowledge_base/messaging/framework.md` | Always | ~5,300 |
| `knowledge_base/messaging/words_that_work.md` | Always | ~3,600 |
| `knowledge_base/personas/[target].md` | Per audience (1 file) | ~6,000 |

**Note**: One-pagers are lean by design. Load only the single persona file that matches the primary audience. Total context: ~23K tokens.

## Section Structure

A one-pager uses content zones rather than flowing sections. Zones are fixed regions on a two-page layout canvas. Every zone must be present. Word counts are binding constraints, not targets.

| Zone | Page | Job | Reader's Reaction | Words |
|------|------|-----|--------------------|-------|
| **Title Block** | Front | Product/solution name + tagline | "I know what this is about" | 10-20 |
| **Intro** | Front | Brief value proposition paragraph | "This is relevant to me" | 40-60 |
| **Capability Grid** | Front | 3-column grid: what the product does | "Here's what it offers" | 120-180 |
| **How It Works** | Front | Visual flow showing the mechanism | "I see how it works" | 30-50 (captions) |
| **Social Proof** | Front | Customer/partner logos or references | "Others trust this" | 0-20 |
| **Business Value** | Back | Why this matters to the organization | "Here's the ROI case" | 100-150 |
| **Deployment** | Back | How fast and easy to get started | "This is practical" | 60-90 |
| **Use Cases** | Back | Category segments or use case circles | "This applies to my world" | 40-60 |
| **Key Metrics** | Back | 3-4 stat tiles with headline numbers | "The numbers are compelling" | 30-40 |
| **Security/Trust** | Back | Security and compliance callouts | "This is enterprise-ready" | 40-60 |
| **CTA** | Back | Clear next step + URL | "I know what to do" | 10-15 |

Total: 500-800 words.

### Zone Details

**Title Block** (10-20 words)
- Product or solution name in large text. One-line tagline directly beneath.
- The tagline is the hook visible from across a conference table — make it earn that distance.
- Lead with what the product does for the buyer, not what it is technically.
- Knowledge: messaging/framework (for approved tagline direction)

**Intro** (40-60 words)
- Exactly 2-3 sentences. No more.
- First sentence leads with the buyer's problem. Last sentence closes with how this solves it.
- No throat-clearing, no company history, no mission statements.
- Knowledge: messaging/framework (for approved problem framing)

**Capability Grid** (120-180 words)
- Exactly 3 columns. Not 2, not 4 — 3.
- Each column has a header (3-5 words) and 3-4 bullets (8-12 words each).
- Describe what the capability does for the buyer, not what the feature is named.
- Columns should be parallel in structure: same number of bullets, similar rhythm.
- Knowledge: teach_product_output (for accurate capability descriptions)

**How It Works** (30-50 words)
- A 3-5 step linear flow. Each step gets a short label (2-4 words) and an optional one-line caption.
- The visual does the heavy lifting — captions clarify, not explain from scratch.
- Placeholder: `> [Visual: step-by-step flow diagram, 3-5 steps with labels]`
- Knowledge: teach_product_output (for accurate process sequencing)

**Social Proof** (0-20 words)
- Logo bar or 1-2 named customer/partner references. Can be logos only with zero words.
- If names are used, attribution must be verifiable. Do not fabricate or approximate.
- Knowledge: none (use only verified references)

**Business Value** (100-150 words)
- 2-3 short paragraphs, or a heading followed by bullets.
- Frame entirely around outcomes: cost reduction, engineering velocity, risk mitigation, knowledge retention.
- No feature descriptions here — this zone translates capabilities into organizational impact.
- Address the economic buyer directly; this is the zone the program manager reads first.
- Knowledge: messaging/framework (for outcome language)

**Deployment** (60-90 words)
- Open with a "deploy in hours/days" frame — time-to-value is the lead.
- 3-4 bullets covering: deployment model (cloud/on-prem/hybrid), key integrations, time-to-value, what's not required.
- Reassure the reader that adoption does not require a large lift.
- Knowledge: teach_product_output (for accurate deployment specs)

**Use Cases** (40-60 words)
- 4-6 category labels with optional one-line descriptions (1 sentence each).
- Rendered as circles, cards, or tags — each label is a named scenario, not a generic category.
- Anchor to recognizable contexts the target persona encounters in their role.
- Knowledge: personas/[target] (for what scenarios resonate)

**Key Metrics** (30-40 words)
- 3-4 stat tiles. Each tile: one specific number + one short label.
- Format per tile: `value | label` — e.g., `10x | faster onboarding`.
- Numbers must be defensible. Use only stats that appear in approved PMM sources.
- Knowledge: teach_product_output, messaging/framework (for approved stats)

**Security/Trust** (40-60 words)
- 3-5 bullets. Short and scannable — one clause each.
- Cover: deployment model security, data handling, compliance certifications, access controls.
- Signals enterprise readiness without requiring a full security review to read.
- Knowledge: teach_product_output (for accurate security claims)

**CTA** (10-15 words)
- Single, specific action. One URL. No secondary links.
- "Learn more at [your-domain.com]" is acceptable floor; a specific destination URL is better.
- Knowledge: none

## Formatting Rules

- **Total word count**: 500-800 words. Exceeding the upper bound means it's a primer, not a one-pager. Cut before you publish.
- **Bullet discipline**: Every bullet is 8-12 words maximum. If a bullet exceeds 12 words, split or cut.
- **Paragraph length**: No paragraph longer than 3 sentences anywhere in the document.
- **Capability grid**: Always exactly 3 columns. Layout collapses with 2 or 4.
- **Stats tiles**: Always 3-4 tiles. Fewer looks sparse; more overwhelms the zone.
- **Visuals**: One visual placeholder per page — flow diagram on front, process or use-case visual on back.
- **No footnotes**: One-pagers do not cite sources inline. If a claim requires a footnote, it's too hedged for this format — either strengthen it or remove it.
- **No pull quotes**: Pull quotes belong in long-form. This format has no room.

## Post-Write Agents

| Agent | Required? | Notes |
|-------|-----------|-------|
| `asset-reviewer` | Yes | Focus on density, clarity, and zone completeness |
| `persona-reviewer` | Yes | Run with primary persona |
| content scrubber | Yes | Universal post-processor |
| `linkedin-repurposer` | No | One-pagers don't typically get LinkedIn promotion |
| `newsletter-repurposer` | No | Not applicable |

## Quality Checklist

- [ ] Total word count between 500-800 words
- [ ] Title block is punchy and readable at arm's length
- [ ] Intro paragraph is 2-3 sentences and leads with the buyer's problem
- [ ] Capability grid has exactly 3 columns with 3-4 bullets each
- [ ] Every bullet is 8-12 words maximum
- [ ] How It Works flow has 3-5 labeled steps with a visual placeholder
- [ ] Business Value section focuses on outcomes, not features
- [ ] Stats tiles have 3-4 items with specific, sourced numbers
- [ ] Security section covers deployment model and compliance
- [ ] CTA is specific and actionable with a single URL
- [ ] No marketing-speak or superlatives without supporting evidence
- [ ] Product claims verified against `teach_product_output.md`
- [ ] Social proof references are verifiable (no fabricated attributions)
- [ ] Content scrubber has been run
- [ ] Content fits within 2-page layout (front + back)
