# Press Release — Asset Type Template

## Metadata

- **Format**: structured prose (strict PR format — deviations from convention signal amateur hour to journalists)
- **Target length**: 400-600 words
- **Reading time**: 2-3 minutes
- **Tone**: Factual, third-person, declarative. No marketing hyperbole. No superlatives. The prose should read like a wire service wrote it — Reuters, not a blog post. If a sentence would embarrass you in the Financial Times, cut it.
- **Brand voice**: Part 1 only. Part 2 does not apply — press releases are third-person and do not speak as [COMPANY].
- **Primary personas**: `journalist`, `analyst` (the reader is a reporter or industry analyst deciding whether to cover this)

## Knowledge Sources

Load from `$PMM_KNOWLEDGE_PATH`:

| File | When to Load | Approx Tokens |
|------|-------------|---------------|
| `knowledge_base/messaging/framework.md` | Always | ~5,300 |
| `config/teach_product_output.md` | When announcement involves product capabilities | ~8,400 |
| `knowledge_base/competitive/[name].md` | When announcement positions against market context | ~10-16K each |

**Note**: Press releases are lean and factual. Do not load persona files — the audience is journalists and analysts, not buyers. Do not load words_that_work — PR language follows wire conventions, not marketing messaging. Total context: 5-14K tokens.

## Section Structure

A press release follows a rigid inverted-pyramid structure. Every section is required. Order is non-negotiable — journalists expect this exact sequence and will discard releases that deviate.

| # | Section | Job | Reader's Question |
|---|---------|-----|--------------------|
| 1 | **Headline** | Summarize the entire announcement in one line | "What happened?" |
| 2 | **Subheadline** (optional) | Add one layer of context or scope | "Why does this matter?" |
| 3 | **Dateline** | Establish when and where | "When and where?" |
| 4 | **Lead Paragraph** | Who/what/when/where/why in 1-2 sentences | "Give me the full picture in 10 seconds" |
| 5 | **Body Paragraph 1** | Expand the "what" with context | "Tell me more about what this actually is" |
| 6 | **Executive Quote** | Human voice and strategic framing from leadership | "What does the company think this means?" |
| 7 | **Body Paragraph 2** | Supporting details, customer evidence, market data | "What's the proof?" |
| 8 | **Boilerplate** | Standard company description | "Who is this company?" |
| 9 | **Media Contact** | Who to call for more information | "How do I follow up?" |

### Section Details

**Headline** (8-15 words)
- Factual, not clever. State what happened. "[COMPANY] Launches AI-Powered Code Understanding for COBOL Modernization" — not "The Future of Legacy Code Is Here."
- Present tense for the action verb. This is news, not a retrospective.
- Include the company name and the core announcement. A journalist scanning 200 headlines must understand yours without clicking.
- No colons, no questions, no exclamation marks. No "Announces Partnership to Revolutionize."
- Knowledge: messaging/framework (for accurate positioning language)

**Subheadline** (10-20 words, optional)
- One sentence that adds scope, a key number, or the "so what" that doesn't fit in the headline.
- Italicized by convention. Treated as a deck head in wire format.
- Only include if the headline alone leaves a critical gap. If the headline tells the full story, skip.
- Knowledge: none

**Dateline** (format: CITY, State/Country — Month Day, Year)
- Standard wire format. City in ALL CAPS. Date spelled out.
- Example: `TEL AVIV, Israel — March 5, 2026`
- The dateline precedes the first word of the lead paragraph on the same line, separated by an em dash.
- Knowledge: none

**Lead Paragraph** (30-60 words, 1-2 sentences)
- Answer who, what, when, where, and why. All five. In two sentences or fewer.
- The first sentence is the announcement. The second sentence is the significance.
- If a journalist reads only this paragraph and writes a story from it, the story should be accurate and complete.
- No adjectives that require proof (avoid "leading," "innovative," "groundbreaking"). Let the facts speak.
- Knowledge: messaging/framework

**Body Paragraph 1** (80-120 words)
- Expand the "what." Provide the context a journalist needs to understand the announcement's significance.
- Include: what the product/feature/partnership does, who it's for, and why it matters to the market.
- Quantify where possible: market size, affected user base, performance metrics.
- This paragraph is where you earn the journalist's interest beyond the lead. If the lead is the headline, this is the lede.
- Stay third-person. No "we believe" or "our mission."
- Knowledge: teach_product_output (for accurate capability descriptions), messaging/framework

**Executive Quote** (40-80 words, 1-2 sentences of quote + attribution)
- Attributed to a named executive with title: `"Quote text," said [Full Name], [Title] at [COMPANY].`
- The quote must say something a human would actually say. Not "We are thrilled to announce this groundbreaking solution." A real person would say: "Enterprise teams maintaining 20-year-old COBOL systems need tools built for that specific challenge, not general-purpose AI that guesses."
- The quote carries the strategic interpretation — why this matters for the market, not what the product does (that's Body Paragraph 1's job).
- One quote per press release. Two quotes (e.g., adding a customer or partner) only if the second adds materially different perspective.
- Knowledge: messaging/framework (for strategic framing)

**Body Paragraph 2** (80-120 words)
- Supporting details that strengthen the announcement. Choose the strongest available:
  - Customer evidence: a named customer, a deployment stat, or a use case.
  - Market data: industry research, analyst citation, or market sizing that contextualizes the announcement.
  - Technical detail: architecture or capability detail that differentiates, stated factually.
- If customer evidence is available, lead with it. Named customers beat anonymous references. Specific numbers beat qualitative claims.
- This paragraph answers the skeptic's "prove it" without being defensive.
- Knowledge: teach_product_output, competitive files (if market positioning is relevant)

**Boilerplate** (40-80 words)
- Standard company description paragraph. Reused across all press releases with minimal variation.
- Load from PMM if available at `$PMM_KNOWLEDGE_PATH/knowledge_base/messaging/boilerplate.md`. If not available, write a factual 2-3 sentence description: what the company does, who it serves, and where it's headquartered.
- Format: `**About [COMPANY]**` header followed by the description paragraph.
- Ends with the company URL.
- Do not customize per announcement — the boilerplate is a fixed asset. Flag with the project owner if it needs updating.
- Knowledge: messaging/framework (for approved company description)

**Media Contact** (structured block, not prose)
- Format:
  ```
  **Media Contact**
  [Full Name]
  [Title]
  [Email]
  [Phone — optional]
  ```
- If no media contact is specified in the brief, use a placeholder: `[Media contact TBD — confirm before distribution]`.
- Knowledge: none

## Markdown Output Format

```markdown
# [Headline]

*[Subheadline — if included]*

**[CITY, State/Country — Month Day, Year]** — [Lead paragraph text continues on the same line as the dateline.]

[Body Paragraph 1]

"[Executive quote text]," said [Full Name], [Title] at [COMPANY].

[Body Paragraph 2]

**About [COMPANY]**

[Boilerplate text. Company URL.]

**Media Contact**
[Name]
[Title]
[Email]
```

## Formatting Rules

- **Total word count**: 400-600 words. Press releases that exceed 600 words do not get read. Cut before you send.
- **Paragraph length**: No paragraph longer than 4 sentences. Most paragraphs are 2-3 sentences.
- **Third-person throughout**: No "we," "our," or "us" outside of direct quotes. The company is always "[COMPANY]," never "we."
- **Present tense for announcements**: "[COMPANY] launches..." not "[COMPANY] has launched..." or "[COMPANY] is launching..."
- **Quote formatting**: Use said, not "stated," "commented," "shared," or "expressed." "Said" is invisible to journalists — everything else draws attention to itself.
- **No superlatives without proof**: "Leading," "best-in-class," "groundbreaking," "innovative," "revolutionary" — all banned unless accompanied by a verifiable third-party citation in the same sentence.
- **No exclamation marks**: Anywhere. Ever.
- **Numbers**: Spell out one through nine. Use numerals for 10 and above. Percentages always use numerals + "%."
- **Company references**: First mention is "[COMPANY]" with a brief descriptor if needed. Subsequent mentions are "[COMPANY]" or "the company." Never "they."
- **One announcement per release**: If there are two announcements, write two press releases. A press release that tries to announce a product launch AND a partnership AND a funding round will get none of them covered.
- **No jargon without definition**: If a term wouldn't be understood by a general business journalist, define it in parentheses on first use or cut it.

## Post-Write Agents

| Agent | Required? | Notes |
|-------|-----------|-------|
| `asset-reviewer` | Yes | Verify word count, inverted-pyramid structure, quote authenticity, no superlatives without citations |
| `persona-reviewer` | Yes | Embody a tech journalist receiving this in a press inbox with 50 other releases today. Would you open it? Would you cover it? |
| content scrubber | Yes | Universal post-processor |
| `linkedin-repurposer` | Optional | Generate an executive LinkedIn post announcing the news (different voice than the PR) |
| `newsletter-repurposer` | No | Press releases are not newsletter content |

## Quality Checklist

- [ ] Total word count between 400-600 words
- [ ] Headline is factual, present-tense, 8-15 words, includes company name
- [ ] No colons, questions, or exclamation marks in the headline
- [ ] Dateline follows wire format: CITY, State/Country — Month Day, Year
- [ ] Lead paragraph answers who/what/when/where/why in 1-2 sentences
- [ ] Lead paragraph contains no adjectives that require proof ("leading," "innovative," etc.)
- [ ] Body Paragraph 1 expands the "what" with quantified context
- [ ] Executive quote sounds like something a human would actually say
- [ ] Quote attribution uses "said" — not "stated," "commented," "shared"
- [ ] Body Paragraph 2 includes customer evidence, market data, or specific technical differentiation
- [ ] Entire document is third-person (no "we/our/us" outside direct quotes)
- [ ] No superlatives without verifiable third-party citations
- [ ] No exclamation marks anywhere
- [ ] Numbers follow AP style (spell out 1-9, numerals for 10+)
- [ ] Boilerplate is standard and ends with company URL
- [ ] Media contact block is present (or marked TBD)
- [ ] One announcement only — not bundling multiple news items
- [ ] Product claims verified against `teach_product_output.md`
- [ ] Content scrubber has been run
