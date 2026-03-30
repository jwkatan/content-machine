# Email Campaign — Asset Type Template

## Metadata

- **Format**: sequence (one or more emails, each a discrete unit with shared campaign logic)
- **Target length**: 150-300 words body copy per email; campaign strategy section adds 200-400 words
- **Reading time**: 30-60 seconds per email (recipients scan, not read)
- **Tone**: Direct, conversational, action-oriented. "Peer in the hallway" register — not a brochure, not a cold pitch. Warmth scales with relationship: cold outreach is crisper; customer emails are warmer.
- **Brand voice**: Part 1 always. Part 2 always (all emails represent [COMPANY]).
- **Primary personas**: Set per project. Persona determines pain framing, proof selection, and CTA.

## Knowledge Sources

Load from `$PMM_KNOWLEDGE_PATH`:

| File | When to Load | Approx Tokens |
|------|-------------|---------------|
| `knowledge_base/messaging/framework.md` | Always | ~5,300 |
| `knowledge_base/messaging/words_that_work.md` | Always | ~3,600 |
| `knowledge_base/personas/[target].md` | Per audience (1 file) | ~6,000 |
| `config/teach_product_output.md` | When product is featured in email body | ~8,400 |

**Per-email loading**: Each email writing subagent loads messaging/framework, words_that_work, and the persona file. teach_product_output loads only for emails that reference product capabilities directly. Total context per subagent: 9-15K tokens.

## Sequence Variants

This template handles campaigns from 1 to 6+ emails. The section structure table below shows the maximum variant (6-email webinar series). Shorter campaigns use a subset.

**Single email** (customer launch announcement, event invite, product update):
- Campaign Strategy + 1 email. No narrative arc section — the strategy section covers audience and goal.
- Sections used: Campaign Strategy, Email 1.

**3-email drip** (sales outreach, "wake the dead", content nurture):
- Campaign Strategy + Narrative Arc + 3 emails.
- Typical arc: Email 1 = problem awareness, Email 2 = proof/evidence, Email 3 = direct CTA.
- Sections used: Campaign Strategy, Narrative Arc, Emails 1-3.

**6-email webinar series** (3 invites + reminder + 2 follow-ups):
- Campaign Strategy + Narrative Arc + 6 emails. Full structure as shown below.
- Invite arc (Emails 1-3): announce → social proof → urgency/last chance.
- Reminder (Email 4): day-of logistics, no selling.
- Follow-up arc (Emails 5-6): recording + key takeaway → deeper resource + CTA.
- Sections used: Campaign Strategy, Narrative Arc, Emails 1-6.

**Adapting the structure**: When creating the outline in Phase 1, include only the emails needed for the campaign. Mark emails as "(conditional)" in the section structure if they activate only for longer sequences. The Campaign Strategy section always specifies exactly how many emails are in the sequence and what each one does.

## Section Structure

The table below shows the maximum sequence (6-email webinar series). Emails marked (conditional) are omitted for shorter campaigns. Campaign Strategy and Email 1 are always present.

| # | Section | Job | Reader's Question |
|---|---------|-----|--------------------|
| 0 | **Campaign Strategy** | Define audience, sequence length, cadence, goal per email | "What's the plan?" (internal) |
| 0.1 | **Narrative Arc** (conditional: 2+ emails) | Map the through-line across the sequence | "How do these emails connect?" (internal) |
| 1 | **Email 1** | First touch — open the conversation | "Why should I open this?" |
| 2 | **Email 2** (conditional: 2+ emails) | Deepen interest — add proof or a new angle | "Why should I keep reading?" |
| 3 | **Email 3** (conditional: 3+ emails) | Drive action — urgency or direct ask | "What do you want me to do?" |
| 4 | **Email 4** (conditional: 4+ emails — webinar reminder) | Day-of logistics and excitement | "When and where do I show up?" |
| 5 | **Email 5** (conditional: 5+ emails — post-event follow-up 1) | Deliver the recording + one key takeaway | "I missed it / want to rewatch" |
| 6 | **Email 6** (conditional: 6+ emails — post-event follow-up 2) | Deeper resource + conversion CTA | "What should I do next?" |

### Section Details

**Campaign Strategy** (200-400 words, internal — not sent)
- **Audience segment**: Who receives this campaign. Be specific: "enterprise architects evaluating AI coding tools" not "developers."
- **Sequence length**: How many emails, with send cadence (e.g., "3 emails over 10 days: Day 0, Day 4, Day 10").
- **Goal per email**: One sentence per email stating its specific job (e.g., "Email 2: establish credibility with a customer proof point").
- **Unsubscribe / fatigue notes**: Flag any sequence-level concerns (e.g., "Emails 3 and 4 are 48h apart — keep Email 3 short to avoid fatigue").
- **Success metrics**: What does success look like? Open rate target, click-through target, reply target (for outreach).
- Knowledge: persona file (for segment definition), messaging/framework (for campaign positioning)

**Narrative Arc** (100-200 words, internal — not sent, conditional: 2+ emails)
- One paragraph describing the through-line: how each email builds on the last.
- Map the emotional arc: curiosity → credibility → urgency. Or: announcement → social proof → scarcity. Name the pattern.
- Each email must stand alone (recipients may skip emails) but reward sequential reading.
- Knowledge: messaging/framework

**Email 1** (150-300 words body copy)
- **Subject line**: Primary + A/B variant. Max 50 characters each. The subject line is 80% of whether the email gets opened — write it like a headline, test it like an ad.
- **Preview text**: 40-90 characters. Complements the subject — do not repeat it. This is the second line visible in the inbox.
- **Body copy**: Open with the recipient's world, not yours. First sentence must earn the second. Lead with a question, a pain point, or a surprising fact — never "I'm reaching out because..."
- **CTA**: One CTA per email. Button text is a verb phrase (e.g., "Watch the demo", "Save your spot"). Link destination must be specific.
- **What to avoid**: No "Dear [First Name]," openings. No paragraphs longer than 3 lines. No multiple CTAs competing for attention. No attachments — link instead.
- Knowledge: messaging/framework, words_that_work, persona file

**Email 2** (150-300 words body copy, conditional: 2+ emails)
- **Subject line**: Primary + A/B variant. Must feel like a continuation, not a repeat.
- **Preview text**: 40-90 characters.
- **Body copy**: Introduce a new angle — proof, evidence, social validation, or a different pain point. Do not restate Email 1's argument. If Email 1 was "here's the problem," Email 2 is "here's proof others solved it."
- **CTA**: Same destination as Email 1, or a lower-commitment alternative (e.g., "Read the case study" vs. "Book a demo").
- Knowledge: messaging/framework, words_that_work, persona file, teach_product_output (if proof involves product)

**Email 3** (150-300 words body copy, conditional: 3+ emails)
- **Subject line**: Primary + A/B variant. Urgency or scarcity framing if appropriate — but factual, not manufactured.
- **Preview text**: 40-90 characters.
- **Body copy**: Direct ask. This email earns its place by being shorter and more pointed than Emails 1-2. Strip everything that isn't driving the action. If a webinar series: this is "last chance to register."
- **CTA**: The primary conversion action. Be explicit about what happens after the click.
- Knowledge: messaging/framework, words_that_work, persona file

**Email 4** (100-200 words body copy, conditional: 4+ emails — webinar reminder)
- **Subject line**: Logistics-first. "Starting in 1 hour: [Webinar Title]" — no clever wordplay.
- **Preview text**: 40-90 characters. Include the join link or time.
- **Body copy**: Time, date, join link, what to expect in 1-2 sentences. No selling. The recipient already registered — respect that decision and help them show up.
- **CTA**: "Join now" with the direct meeting/webinar link. No intermediate landing page.
- Knowledge: none (logistics only)

**Email 5** (150-250 words body copy, conditional: 5+ emails — post-event follow-up 1)
- **Subject line**: Primary + A/B variant. Lead with the recording or the single best takeaway.
- **Preview text**: 40-90 characters.
- **Body copy**: Open with gratitude (one sentence, not gushing). Deliver the recording link immediately — do not bury it. Pull one specific, compelling takeaway from the event to hook non-attendees. Segment if possible: attendees get "here's the recording + slides"; non-attendees get "here's what you missed."
- **CTA**: "Watch the recording" or "Download the slides."
- Knowledge: messaging/framework (for takeaway framing)

**Email 6** (150-250 words body copy, conditional: 6+ emails — post-event follow-up 2)
- **Subject line**: Primary + A/B variant. Frame around the next step, not the event.
- **Preview text**: 40-90 characters.
- **Body copy**: Bridge from the event to a deeper resource (whitepaper, case study, demo). This is the conversion email — the event was the warm-up. One paragraph connecting event theme to the resource, then a direct ask.
- **CTA**: The primary conversion action — demo, trial, consultation, or gated asset download.
- Knowledge: messaging/framework, words_that_work, persona file, teach_product_output (if CTA involves product)

## Markdown Output Format

Each email follows this format within the asset document:

```markdown
---

## Email [N]: [Descriptive Title]

**Send timing**: [Day X / trigger condition]

**Subject line A**: [Primary subject]
**Subject line B**: [A/B variant]
**Preview text**: [40-90 characters]

**Body:**

[Email body copy. Plain text with minimal formatting. Short paragraphs (1-3 sentences). One link per CTA. Personalization tokens in {{double braces}}: {{first_name}}, {{company}}, etc.]

**CTA button**: [Button text] → [destination URL]
```

## Formatting Rules

- **Body copy per email**: 150-300 words. Exceeding 300 words means the email is trying to be a blog post. Cut.
- **Paragraph length**: 1-3 sentences maximum. Email is read on mobile — short paragraphs are not a suggestion.
- **Subject lines**: Max 50 characters each. Always provide A/B variants. The A variant is the hypothesis; B is the contrast.
- **Preview text**: 40-90 characters. Never leave blank — inbox clients will pull the first body sentence, which is rarely optimal.
- **CTA count**: Exactly 1 CTA per email. Secondary links (e.g., "P.S. — check out this case study") count as a CTA. If you have two, pick one.
- **Personalization**: Use {{first_name}} in body, never in subject lines for cold outreach (it triggers spam filters). For customer emails, subject line personalization is acceptable.
- **No images in body**: Email templates handle visual design. The copy document contains text only.
- **No HTML**: Write plain text with line breaks. The email platform applies the template.
- **Sequence numbering**: Emails are numbered sequentially starting at 1 regardless of which conditional emails are included.

## Post-Write Agents

| Agent | Required? | Notes |
|-------|-----------|-------|
| `asset-reviewer` | Yes | Review per-email word count, CTA clarity, subject line length, sequence coherence |
| `persona-reviewer` | Yes | Embody the recipient — react to each email as it arrives in your inbox with 47 other unread messages |
| content scrubber | Yes | Universal post-processor |
| `linkedin-repurposer` | No | Email campaigns are not LinkedIn content |
| `newsletter-repurposer` | No | Email campaigns are the newsletter — no repurposing needed |

## Quality Checklist

- [ ] Campaign Strategy section defines audience, cadence, and goal per email
- [ ] Narrative Arc section (if 2+ emails) maps the through-line across the sequence
- [ ] Every email body is 150-300 words (100-200 for reminder emails)
- [ ] Every subject line is under 50 characters with an A/B variant
- [ ] Every email has preview text (40-90 characters) that complements, not repeats, the subject
- [ ] Exactly 1 CTA per email — no competing links
- [ ] No email opens with "I'm reaching out because..." or "Dear [First Name],"
- [ ] No paragraph longer than 3 sentences anywhere
- [ ] Each email stands alone (skipping an email doesn't break comprehension)
- [ ] Email 1 opens with the recipient's world, not [COMPANY]'s
- [ ] Urgency framing (if used) is factual, not manufactured
- [ ] Reminder email (if present) contains zero selling — logistics only
- [ ] Follow-up emails (if present) deliver value before asking for next action
- [ ] Personalization tokens use {{double braces}} format
- [ ] Product claims verified against `teach_product_output.md`
- [ ] Language checked against `words_that_work.md`
- [ ] Content scrubber has been run
