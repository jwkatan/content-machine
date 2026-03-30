# Objection Guide — Asset Type Template

## Metadata

- **Format**: reference (objection bank organized by category — lookup by situation, not linear reading)
- **Target length**: 2000-3000 words
- **Reading time**: 10-15 minutes (reference, not linear read — reps search by objection category)
- **Tone**: Direct, practical, no-fluff. "Confident Expert Colleague" from brand voice, aimed at internal enablement. Write like a senior AE debriefing after a tough call — honest about what works, what doesn't, and when to walk away.
- **Brand voice**: Part 1 always. Part 2 always (responses position [COMPANY]'s value).
- **Primary personas (users)**: AEs, SDRs, SEs, customer success managers
- **Primary personas (targets)**: `architect`, `program_manager`, `cio` (override per project — the buyer personas raising objections)

## Purpose

An objection guide is a comprehensive reference for handling buyer resistance across all deal stages. Unlike the objection handling section in a talk track (which covers 3-5 objections for a specific conversation type) or a battle card (which covers competitor-specific objections), this guide is the complete library. Reps use it for pre-call preparation, post-call debriefs, and enablement training.

Every objection includes the verbatim language buyers use, the real concern underneath, a structured response framework, and proof that makes the response credible. Organized by category so reps can find what they need fast.

**Distribution**: Internal only. Core enablement document. Referenced in onboarding, QBRs, and deal reviews. Never sent to buyers.

## Knowledge Sources

Load from `$PMM_KNOWLEDGE_PATH`:

| File | When to Load | Approx Tokens |
|------|-------------|---------------|
| `config/teach_product_output.md` | Always | ~8,400 |
| `knowledge_base/messaging/framework.md` | Always | ~5,300 |
| `knowledge_base/messaging/words_that_work.md` | Always | ~3,600 |
| `knowledge_base/sales_enablement/objection_handling.md` | Always (this is the primary source) | ~4,500 |
| `knowledge_base/personas/[target].md` | Per buyer persona (all relevant personas) | ~6,000 each |
| `knowledge_base/competitive/[name].md` | When competitive objections are included | ~10-16K each |
| `knowledge_base/jtbd/modernization.md` | When objections relate to modernization | ~6,300 |
| `knowledge_base/jtbd/maintenance.md` | When objections relate to maintenance | ~6,300 |

**Per-section loading**: Each objection category tags which files it draws from. Phase 2 loads only the tagged files into each category's writing subagent. The `objection_handling.md` file is the foundation — all other sources provide evidence and context for responses.

## Section Structure

Objections are organized by category. Within each category, objections are ordered by frequency (most common first). Each category represents a distinct type of buyer resistance with its own response patterns.

| # | Section | Job | Rep's Question |
|---|---------|-----|----------------|
| 1 | **Price and Value** | Address cost concerns and ROI skepticism | "They think we're too expensive — what do I say?" |
| 2 | **Competition** | Handle competitor comparisons and preferences | "They prefer [competitor] — how do I respond?" |
| 3 | **Timing** | Overcome "not now" and prioritization stalls | "They say the timing isn't right — how do I keep this alive?" |
| 4 | **Technical** | Address capability doubts and integration concerns | "They don't think it'll work in their environment — what do I do?" |
| 5 | **Organizational** | Navigate internal politics, change management, and inertia | "They want it but say their org can't adopt it — how do I help?" |

### Section Details

**Price and Value** (400-600 words)

Cost objections are rarely about the price — they're about whether the buyer believes the value justifies the spend. These responses reframe from cost to cost-of-inaction.

- 3-5 objections, each formatted as:
  - **The objection** (verbatim): How the buyer actually says it. Include variations. E.g., "That's more than we budgeted" / "We can't justify that spend right now" / "Your competitor is half the price."
  - **The underlying concern**: What they're really worried about. E.g., "I can't build a business case that my CFO will approve."
  - **Response framework**:
    - **Acknowledge**: Validate the concern without agreeing with the premise. 1 sentence.
    - **Reframe**: Shift from price to cost of the problem or value of the outcome. 1-2 sentences.
    - **Evidence**: Specific data point, customer metric, or ROI calculation. 1-2 sentences.
    - **Bridge**: Transition to a next step that helps them build the business case. 1 sentence.
  - **Proof point**: Customer quote or metric that demonstrates ROI. Attributed if possible.
  - **When to walk away**: Signal that this deal can't close on value (budget truly doesn't exist, not a priority).
- What to avoid: Discounting. Apologizing for pricing. Comparing to competitors on price. Promising ROI timelines you can't back up.
- Knowledge: messaging/framework, teach_product_output, objection_handling

**Competition** (400-600 words)

Competitive objections come in two forms: the buyer prefers a competitor, or the buyer is using a competitor's talking points without realizing it. Both need different handling.

- 3-5 objections, each formatted as:
  - **The objection** (verbatim): How the buyer says it. E.g., "We're already evaluating [competitor] and they seem to do the same thing" / "[Competitor] covers this and more."
  - **The underlying concern**: What they're really evaluating. E.g., "I don't want to evaluate another vendor if the one I have is good enough."
  - **Response framework**:
    - **Acknowledge**: Recognize the competitor's strengths genuinely. 1 sentence.
    - **Reframe**: Shift to evaluation criteria that expose the structural difference. 1-2 sentences.
    - **Evidence**: Specific test result, architectural distinction, or customer comparison. 1-2 sentences.
    - **Bridge**: Suggest a side-by-side evaluation or specific test. 1 sentence.
  - **Proof point**: Win story against this competitor type, or head-to-head test result.
  - **Competitor coaching detection**: How to recognize when the buyer is repeating a competitor's script (specific phrases, evaluation criteria that don't make sense organically).
- What to avoid: Bashing competitors. "We're better at everything." Engaging on criteria where the competitor genuinely wins. Getting defensive when the buyer likes the competitor.
- Knowledge: competitive files, messaging/framework, objection_handling, teach_product_output

**Timing** (300-500 words)

Timing objections are the most dangerous because they sound reasonable. "Not right now" is the polite way to kill a deal. These responses separate real timing constraints from polite disinterest.

- 3-4 objections, each formatted as:
  - **The objection** (verbatim): E.g., "We're not ready to evaluate new tools this quarter" / "We have other priorities right now" / "Let's revisit in Q3."
  - **The underlying concern**: Either genuine capacity constraints or lack of perceived urgency.
  - **Response framework**:
    - **Acknowledge**: Respect their priorities. 1 sentence.
    - **Reframe**: Connect to a trigger event, deadline, or cost of waiting. 1-2 sentences.
    - **Evidence**: What happens when organizations delay — specific consequences from customer stories. 1-2 sentences.
    - **Bridge**: Offer a low-commitment next step that keeps the conversation alive without requiring a decision. 1 sentence.
  - **Proof point**: Customer story about the cost of delay, or a market trigger that creates urgency.
  - **Diagnostic**: How to tell if "not now" means "never" — signals to watch for.
- What to avoid: Creating false urgency. "Limited time" pressure tactics. Accepting the timeline without exploring whether it's real. Letting the deal go dormant without a specific follow-up trigger.
- Knowledge: messaging/framework, jtbd files, objection_handling

**Technical** (400-600 words)

Technical objections come from evaluators, architects, and SEs on the buyer side. These are often the most specific and require the most precise responses. Get these wrong and you lose the technical champion.

- 3-5 objections, each formatted as:
  - **The objection** (verbatim): E.g., "We need on-prem and you're cloud-only" / "Does it support [language/framework]?" / "How does it handle [specific edge case]?" / "We tried something similar and it didn't work."
  - **The underlying concern**: Whether it will work in their specific environment and whether they'll be the one stuck if it doesn't.
  - **Response framework**:
    - **Acknowledge**: Take the technical concern seriously — never dismiss. 1 sentence.
    - **Reframe**: Clarify what's possible vs. what's assumed. Correct misinformation precisely. 1-2 sentences.
    - **Evidence**: Specific capability detail, architecture reference, or customer deployment example. 1-2 sentences.
    - **Bridge**: Offer to demonstrate or prove it — POC, technical deep dive, or reference call with a similar deployment. 1 sentence.
  - **Proof point**: Customer deployment that matches their concern (same language, same deployment model, same scale).
  - **SE handoff note**: When this objection requires a solutions engineer to handle instead of an AE. Brief guidance on what to share with the SE.
- What to avoid: Overpromising capabilities. Guessing at technical details — if you don't know, say "I'll get our SE to confirm." Dismissing edge cases as irrelevant. Using "we're building that" for shipped-product questions.
- Knowledge: teach_product_output, objection_handling

**Organizational** (300-500 words)

Organizational objections are about the buyer's company, not about [COMPANY]. Change management, adoption risk, stakeholder alignment, and internal politics. The rep can't solve these alone — but they can arm their champion.

- 3-4 objections, each formatted as:
  - **The objection** (verbatim): E.g., "Getting buy-in from engineering leadership will be hard" / "We've had bad experiences adopting new tools" / "My team won't use another tool" / "We need consensus across three teams."
  - **The underlying concern**: The buyer believes in the solution but doesn't believe their organization will adopt it.
  - **Response framework**:
    - **Acknowledge**: Validate that adoption is a real challenge. 1 sentence.
    - **Reframe**: Share how other organizations navigated the same concern. 1-2 sentences.
    - **Evidence**: Specific adoption strategy, onboarding timeline, or change management approach from a customer reference. 1-2 sentences.
    - **Bridge**: Offer to help build the internal case — materials, reference calls, or a joint session with stakeholders. 1 sentence.
  - **Proof point**: Customer story about successful adoption in a similar organization.
  - **Champion arming**: Specific materials or talking points to give the buyer so THEY can handle the internal objection. This is the most valuable part — what do you put in their hands?
- What to avoid: Minimizing the difficulty of internal change. "It's easy to adopt" (it's never easy). Ignoring the political dimension. Pushing the champion to sell harder instead of helping them navigate.
- Knowledge: personas (for org dynamics), teach_product_output (for deployment/adoption), objection_handling

## Formatting Rules

- **Category headers visible**: Reps scan by category. Each category header is prominent and includes a one-line description of what it covers.
- **Verbatim objections bolded**: The "The objection" line uses the buyer's exact words so reps recognize the objection when they hear it. Include 2-3 phrasing variations.
- **Response framework consistent**: Every objection follows Acknowledge → Reframe → Evidence → Bridge. No exceptions. Consistency makes this usable under pressure.
- **Proof points are specific**: No generic "customers report improved outcomes." Every proof point has a name/industry, a number, and a context.
- **Walk-away and diagnostic signals**: Include signals for when the objection reveals a genuine deal-breaker vs. a solvable concern. Reps need to know when to push and when to qualify out.
- **No marketing copy**: This is a coaching document. Be blunt. "This objection usually means they're not a fit" is more useful than a diplomatic non-answer.
- **Cross-references**: Where an objection in one category connects to another (e.g., a pricing objection that's really a competition objection), add a brief cross-reference note.

## Post-Write Agents

| Agent | Required? | Notes |
|-------|-----------|-------|
| `asset-reviewer` | Yes | Focus on response quality, proof point specificity, and framework consistency |
| `persona-reviewer` | Yes | Run with all target buyer personas to validate objection authenticity |
| content scrubber | Yes | Universal post-processor |
| `linkedin-repurposer` | No | Internal document — not for external promotion |
| `newsletter-repurposer` | No | Not applicable |

## Quality Checklist

- [ ] Total word count between 2000-3000 words
- [ ] All 5 objection categories covered (price/value, competition, timing, technical, organizational)
- [ ] Each category has 3-5 objections ordered by frequency
- [ ] Every objection includes verbatim buyer language with phrasing variations
- [ ] Every objection identifies the underlying concern, not just the surface statement
- [ ] Every response follows the Acknowledge → Reframe → Evidence → Bridge framework
- [ ] Every objection has a specific, attributed proof point (not generic outcomes)
- [ ] Technical objections include SE handoff guidance where appropriate
- [ ] Organizational objections include champion-arming materials
- [ ] At least 2 objections include walk-away signals (when the objection reveals a genuine deal-breaker)
- [ ] Competitive objections include coaching-detection signals
- [ ] No defensive or dismissive responses
- [ ] Product claims verified against `teach_product_output.md`
- [ ] Cross-references included where objections span categories
- [ ] Content scrubber has been run
