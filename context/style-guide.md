# [Company Name] Style Guide

<!-- Instructions: Replace [Company Name] with your company name. Replace product-specific terminology with your own. Keep all generic grammar, formatting, and capitalization guidance as-is — these are universal best practices. -->

This guide defines writing conventions, formatting standards, and editorial guidelines for all [Company Name] content.

## Instructions
This document establishes the style standards for [Company Name] content creation. It complements [brand-voice.md](brand-voice.md) by providing specific formatting and mechanical guidelines. Update as the style guide evolves.

---

## Grammar & Mechanics

### Capitalization

**Headlines & Subheadings**:
- Use **sentence case** (only capitalize first word and proper nouns)
- Example: "How to automate code review for distributed teams"
- Exception: Proper nouns and acronyms always capitalized ([Company Name], API, CI/CD)

**Product Names**:
<!-- Instructions: List your product names and features that should be capitalized. -->
- [Company Name]: Always capitalized
- [Feature Name 1]: Capitalize when referring to the specific feature
- [Feature Name 2]: Capitalize feature names

**Industry Terms**:
<!-- Instructions: List industry terms and their capitalization rules. -->
- API: All caps (acronym)
- CI/CD: All caps (acronym)
- pull request: Lowercase unless starting a sentence
- code review: Lowercase (not a proper noun)

### Numbers

**When to Spell Out**:
- Spell out: One through nine in narrative text
- Use numerals: 10 and above
- Exceptions:
  - Percentages: Always use numerals (5%, 90%)
  - Money: Always use numerals ($5, $500)
  - Measurements: Always use numerals (100 lines of code, 3 files)
  - Statistics: Always use numerals for precision
  - Technical specs: Always use numerals (8-character field, Level 3 complexity)

**Large Numbers**:
- Use commas: 1,000+
- Spell out million/billion: 100 million lines of code
- Use + for approximations: 100+ million, 90%+ faster

### Punctuation

**Oxford Comma**:
- **Yes** - Always use the Oxford comma
- Example: "Analyze pull requests, detect vulnerabilities, and route reviews"

**Em Dashes**:
- Style: Use space-dash-space ( - ) not em dash (-)
- Usage: For parenthetical statements, clarifications, or emphasis
- Example: "Automated review doesn't replace human judgment - it focuses it where it matters most."
- **CRITICAL**: Never use em dash without spaces. Always use " - " with spaces on both sides.

**Quotation Marks**:
- Use straight quotes: "text here"
- For code or technical terms in quotes: Use backticks instead when appropriate
- Example: The `main` branch vs. "code review"

**Ellipses**:
- Three dots: ...
- Use sparingly: Primarily for omitted text in quotes or code examples
- Avoid in regular prose (use em dashes instead for trailing thoughts)

### Abbreviations & Acronyms

**First Use**:
- Spell out on first use with acronym in parentheses
- Example: "Continuous Integration/Continuous Deployment (CI/CD) automates the process..."
- Exceptions for universally known in our audience: API, URL, SEO

**Common Technical Acronyms**:
<!-- Instructions: List the acronyms your content frequently uses. -->
- API: Application Programming Interface
- CI/CD: Continuous Integration/Continuous Deployment
- PR: Pull Request
- LLM: Large Language Model
- AI: Artificial Intelligence
- RBAC: Role-Based Access Control
- SSO: Single Sign-On
- SLA: Service Level Agreement

**Latin Abbreviations**:
- **Avoid** e.g., i.e., etc. in favor of plain English
- Use instead: "for example," "that is," "and more" or "and so on"

---

## Word Choice & Usage

### Preferred Terms

<!-- Instructions: Replace this entire table with your company's preferred vs. avoided terms. -->

**Say This** -> **Not That**:
- code review -> code inspection (industry-standard term)
- pull request -> merge request (unless GitLab-specific context)
- review cycle time -> review latency, review delay
- engineering velocity -> developer speed
- defect prevention -> bug catching (proactive framing)
- review coverage -> review completeness
- code quality -> code health
- automated analysis -> automated scanning (more precise for our approach)
- surface -> find, detect (emphasizes bringing to attention)
- integrate -> plug in, connect (more professional)

### Words to Avoid

**Marketing Jargon** (Never use these):
- synergize, leverage, disrupt, innovate, transform, revolutionize
- game-changing, cutting-edge, next-generation, best-in-class
- unlock, unleash, empower (overused marketing terms)
- digital transformation (use "modernization" or specific term instead)

**Fear Language** (Replace with neutral terms):
- nightmare -> challenge, significant issue
- disaster, catastrophe -> costly problem, critical risk
- crisis -> urgent challenge
- struggle, failing -> facing challenges

**Hedging Language** (Remove or rephrase):
- might, could, perhaps, potentially, possibly (be direct instead)
- very, really, actually (usually unnecessary padding)

**Vague Terms** (Replace with specifics):
- better, improved -> quantify (60% faster, 50% reduction)
- easy, simple -> specific benefits
- powerful, robust -> describe actual capabilities

### Inclusive Language
- Use gender-neutral language: "they" instead of "he/she"
- "Developer" or "engineer" instead of gendered terms
- Avoid idioms that may not translate globally
- Be mindful of accessibility in descriptions

---

## Formatting Standards

### Text Formatting

**Bold**:
- Use for: Headers and the first word/phrase in labeled list items
- Example in labeled lists:
  - **Automated**: [Company Name] analyzes PRs automatically on every push
  - **Scalable**: [Company Name] handles repositories of any size
- Do NOT use for: Emphasis within paragraphs, key concepts, or takeaways
- Keep it minimal: Bold should be structural, not emphatic

**Italics**:
- Use for: Emphasis (sparingly), example variable names in narrative
- Avoid: Don't use for code (use backticks instead)

**Code Formatting (backticks)**:
- Use for: Code snippets, variable names, file names, program names, technical values
- Inline: `main`, `develop`, `package.json`
- Example: "The `pre-commit` hook runs analysis before each push."

**Underline**:
- Don't use (reserve for links only)

**ALL CAPS**:
- Use only for: Standard acronyms (API, CI/CD, PR, LLM)
- Never use for emphasis or shouting

### Lists

**Bulleted Lists**:
- Use for: Non-sequential items, features, benefits, characteristics
- Capitalization: Sentence case (capitalize first word only)
- Punctuation:
  - Period if complete sentence
  - No period if fragment
  - Maintain parallel structure (all sentences OR all fragments, not mixed)

**Numbered Lists**:
- Use for: Sequential steps, processes, rankings, ordered priorities
- Format: 1. 2. 3. (with period after number)
- Same capitalization and punctuation rules as bullets

**Nested Lists**:
- Maximum 2 levels deep for readability
- Use proper indentation
- Maintain consistent marker style

### Links

**Anchor Text**:
- Descriptive (tell reader where they're going)
- Keyword-rich when appropriate for SEO
- 2-6 words typically
- Good: "Learn more about automated code review"
- Bad: "Click here" or "Read more"

**Link Formatting**:
- Use markdown format: `[anchor text](url)`
- External links: Open in new tab when implemented
- Internal links: Use relative paths
- No "link" or "here" as anchor text

### Code & Technical Elements

**Inline Code**:
- Use backticks for: Code snippets, program names, file names, variable names, commands
- Example: "Your `pre-commit` hook runs `acme-review analyze` on staged changes."

**Code Blocks**:
- Use for: Multi-line code, configuration examples, CLI commands
- Include language identifier: ```yaml or ```python
- Provide context before code blocks
- Keep examples focused and relevant

### Callout Boxes / Notes

**When to Use**:
- Important warnings or caveats
- Key insights or takeaways
- Technical notes that clarify
- Pro tips for advanced users

**Types**:
- **Note**: General information worth highlighting
- **Warning**: Something that could cause issues
- **Example**: Concrete illustration of a concept
- **Key Insight**: Critical takeaway

---

## Content Structure

### Article Introduction
**Standard Structure** (150-250 words):
1. **Hook** (1-2 sentences): Grab attention with relevant problem, statistic, or compelling statement
2. **Problem** (2-3 sentences): What challenge does this address?
3. **Promise** (2-3 sentences): What will reader learn or achieve?
4. **Credibility** (optional, 1 sentence): Why trust this source?

**Keyword Placement**:
- Include primary keyword in first 100 words
- Natural integration, never forced

### Section Length
- **Minimum**: 150 words per section
- **Maximum**: 500 words per section (break into subsections if longer)
- **Ideal**: 250-350 words per main section
- Use white space generously for readability

### Conclusion
**Standard Structure** (150-200 words):
1. **Recap** (3-5 points or brief paragraph): Summarize key takeaways
2. **Action** (1-2 sentences): What should reader do next?
3. **CTA** (1-2 sentences): Clear call-to-action
   - Request-focused: "Request a demo" or "Try [Company Name] on your codebase"
   - Never: "Sign up now!" or urgency manipulation
4. **Forward-looking** (optional, 1 sentence): Encouraging or connecting thought

---

## SEO-Specific Style

### Meta Titles
- 50-60 characters including spaces
- Include primary keyword
- Include "| [Company Name]" if space allows
- No ending punctuation
- Example: "Automate Code Review for Faster Shipping | Acme Corp"

### Meta Descriptions
- 150-160 characters including spaces
- Include primary keyword naturally
- Include benefit or value proposition
- End with complete thought

### URL Slugs
- Lowercase only
- Hyphens between words (not underscores)
- Include primary keyword
- 3-6 words ideal
- Remove articles (a, an, the) when possible
- Format: `/blog/automate-code-review-guide`

### Alt Text
- Describe what image shows concisely
- Include keyword naturally if relevant to the image
- 125 characters or less
- No "image of" or "picture of" (implied)

---

## Dates & Time

**Date Format**:
- Use: Month DD, YYYY
- Example: January 15, 2026
- In metadata: YYYY-MM-DD (2026-01-15)

**Time**:
- 12-hour format with a.m./p.m.: 3:00 p.m.
- Use lowercase with periods: a.m., p.m.

**Time Zones**:
- Specify when relevant: "3:00 p.m. EST"
- Use abbreviations: EST, PST, UTC

---

## Statistics & Data

### Citing Sources
- Always cite statistics with sources
- Format: "According to [Source], [statistic]."
- Link to original source when possible
- Include year of data: "In 2025, engineering teams spent..."
- For internal data: "[Company Name] analysis of [X] repositories shows..."

### Presenting Numbers
- Round large numbers: "100 million" not "100,234,567"
- Use % symbol: 90% (not "percent")
- Use specific metrics: "60% faster" not "much faster"
- Include commas: 10,000 not 10000
- Quantify whenever possible

---

## Images & Media

### Image Requirements
- Use relevant screenshots and diagrams when helpful
- Maintain consistent style and quality
- All images require descriptive alt text
- File naming: descriptive-name-with-hyphens.png

### Image Captions
- Optional - use when image needs context
- Sentence case
- End with period if complete sentence
- Placement: Below image

### Screenshots
- Crop to show only relevant portion
- Add arrows/highlights to draw attention to key elements
- Ensure text is readable
- Alt text describes what's shown and why it matters

### Diagrams & Flowcharts
- Keep design clean and simple
- Use consistent visual language
- Always provide context in surrounding text
- Alt text describes key finding or concept shown

---

## Brand-Specific Guidelines

### [Company Name] Product References

<!-- Instructions: Replace all product and feature references with your own. -->

**[Company Name] Platform**:
- "[Company Name]" (not "the [Company Name] platform" unless needed for clarity)
- "[Company Name]'s analysis engine"

**Features** (capitalize when referring to specific features):
<!-- Instructions: List your feature names that should be capitalized. -->
- [Feature Name 1]
- [Feature Name 2]
- [Feature Name 3]

**Technical Approach**:
<!-- Instructions: Describe your unique technical approach in 2-3 bullet points. -->
- "[Your unique approach]" (your key differentiator)
- "[Your analysis method]" (not generic terms)

### Competitor References
- **Approach**: Name competitors when relevant and factual
- Be fair and objective
- Focus on differentiation, not criticism
- Never disparage or use fear tactics

---

## Accessibility

### Screen Reader Friendly
- Descriptive link text (never "click here")
- Alt text for all images
- Proper heading hierarchy (H1 -> H2 -> H3, never skip levels)
- Meaningful section headers that describe content

### Plain Language
- Write at 10th-12th grade level (enterprise audience but still clear)
- Define technical terms on first use
- Use short sentences: 15-25 words average
- Short paragraphs: 2-4 sentences
- Break complex ideas into digestible steps

---

## Voice & Tone Reminders

### Core Voice Characteristics
1. Authoritative but accessible
2. Direct and active
3. Professional B2B without jargon
4. Customer-centric
5. Technically credible

### Tone Variations
- **How-to content**: Direct, instructional, step-by-step
- **Strategic content**: Authoritative, framework-oriented, actionable
- **Technical deep dives**: Precise, detailed, educational
- **Product content**: Benefit-focused, specific, evidence-based

### Writing Style Specifics
- **Vary sentence length**: Mix short punchy sentences with substantive explanations
- **Active voice**: Default to active voice with strong verbs
- **No hedging**: Be direct and confident
- **Specific over vague**: Use concrete examples and quantified outcomes
- **Customer as hero**: They solve problems; we enable them

---

## Editing Checklist

Before publishing any content:

**Grammar & Mechanics**:
- [ ] Spelling checked
- [ ] Grammar checked
- [ ] Oxford comma used consistently
- [ ] Em dashes formatted as " - " with spaces
- [ ] Numbers formatted correctly (spelled out 1-9, numerals 10+)
- [ ] Dates formatted correctly (Month DD, YYYY)
- [ ] Acronyms spelled out on first use

**Style**:
- [ ] Capitalization follows guidelines (sentence case for headings)
- [ ] Preferred terminology used
- [ ] No marketing jargon or fear language
- [ ] No hedging language (might, could, perhaps)
- [ ] Bold only used for headers and labeled list items (not for emphasis)
- [ ] Backticks used for all code/technical terms
- [ ] Links are descriptive
- [ ] Voice and tone appropriate for content type

**Structure**:
- [ ] Strong introduction (hook, problem, promise)
- [ ] Logical section flow with clear transitions
- [ ] Proper heading hierarchy (H1 -> H2 -> H3)
- [ ] Effective conclusion with clear next steps
- [ ] Appropriate section lengths (150-500 words)
- [ ] Generous white space and paragraph breaks

**SEO**:
- [ ] Primary keyword in first 100 words
- [ ] Keywords integrated naturally throughout
- [ ] Meta title optimized (50-60 chars)
- [ ] Meta description optimized (150-160 chars)
- [ ] URL slug optimized (3-6 words, lowercase, hyphens)
- [ ] Internal links included where relevant
- [ ] External links to credible sources
- [ ] All images have descriptive alt text
- [ ] Heading structure supports topic authority

**Quality**:
- [ ] Factually accurate
- [ ] Statistics cited with sources
- [ ] No broken links
- [ ] Provides genuine, actionable value
- [ ] Technical details verified
- [ ] Code examples tested (if applicable)
- [ ] Ready for publication

**[Company Name]-Specific**:
- [ ] Customer-centric framing (they're heroes, not the problem)
- [ ] Quantified benefits where possible
- [ ] Technical credibility demonstrated
- [ ] Differentiators highlighted appropriately
- [ ] Product mentions feel natural, not forced
- [ ] No exclamation marks (unless absolutely necessary)
- [ ] No emojis

---

## Updates & Maintenance

**Style Guide Version**: 1.0
**Last Updated**: [Date]
**Next Review**: Quarterly

This style guide is a living document. Update as [Company Name] brand and voice evolve.

**Questions or Additions?**
If you encounter a style question not covered here, make a decision based on the brand voice principles, document it, and add it to this guide for future reference.

---

## Quick Reference

### Common Style Decisions
- **Headings**: Sentence case
- **Oxford comma**: Yes, always
- **Em dashes**: Space-dash-space ( - )
- **Numbers**: Spell out 1-9, numerals 10+
- **Acronyms**: Spell out first use
- **Code/technical terms**: Use `backticks`
- **Links**: Descriptive anchor text
- **Tone**: Authoritative but accessible
- **Customer framing**: They're heroes solving challenges
- **Quantification**: Always prefer specific metrics over vague claims

### Never Use
- Marketing jargon (synergize, leverage, disrupt, unlock, etc.)
- Fear language (nightmare, disaster, crisis)
- Hedging (might, could, perhaps, potentially)
- Exclamation marks (except when truly necessary)
- "Click here" or "Read more" as link text
- Emojis in professional content
