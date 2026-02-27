# Swimm Style Guide

This guide defines writing conventions, formatting standards, and editorial guidelines for all Swimm content.

## Instructions
This document establishes the style standards for Swimm content creation. It complements [brand-voice.md](brand-voice.md) by providing specific formatting and mechanical guidelines. Update as the style guide evolves.

---

## Grammar & Mechanics

### Capitalization

**Headlines & Subheadings**:
- Use **sentence case** (only capitalize first word and proper nouns)
- Example: "Extracting business logic from COBOL applications"
- Exception: Proper nouns and acronyms always capitalized (COBOL, Swimm, IBM)

**Product Names**:
- Swimm: Always capitalized
- Swimm Collections: Capitalize "Collections" when referring to the specific feature
- Swimm Context Agent: Capitalize feature names

**Industry Terms**:
- COBOL: All caps (acronym)
- JCL: All caps (acronym)
- mainframe: Lowercase unless starting a sentence
- legacy code: Lowercase (not a proper noun)
- business rule extraction (BRE): Lowercase in general use, spell out acronym on first use
- modernization: Lowercase

### Numbers

**When to Spell Out**:
- Spell out: One through nine in narrative text
- Use numerals: 10 and above
- Exceptions:
  - Percentages: Always use numerals (5%, 90%)
  - Money: Always use numerals ($5, $500)
  - Measurements: Always use numerals (100 lines of code, 3 files)
  - Statistics: Always use numerals for precision (analyzed 100+ million lines of code)
  - Technical specs: Always use numerals (8-character field, Level 3 complexity)

**Large Numbers**:
- Use commas: 1,000+
- Spell out million/billion: 100 million lines of code
- Use + for approximations: 100+ million, 90%+ faster

### Punctuation

**Oxford Comma**:
- **Yes** - Always use the Oxford comma
- Example: "Extract business rules, flows, and dependencies"

**Em Dashes**:
- Style: Use space-dash-space ( - ) not em dash (—)
- Usage: For parenthetical statements, clarifications, or emphasis
- Example: "Legacy applications are expensive to maintain - the actual cost isn't in the code itself - it's in the cognitive load teams carry."
- **CRITICAL**: Never use em dash without spaces (—). Always use " - " with spaces on both sides.

**Quotation Marks**:
- Use straight quotes: "text here"
- For code or technical terms in quotes: Use backticks instead when appropriate
- Example: The `PERFORM` statement vs. "business rules"

**Ellipses**:
- Three dots: ...
- Use sparingly: Primarily for omitted text in quotes or code examples
- Avoid in regular prose (use em dashes instead for trailing thoughts)

### Abbreviations & Acronyms

**First Use**:
- Spell out on first use with acronym in parentheses
- Example: "Business Rule Extraction (BRE) automates the process..."
- Exceptions for universally known in our audience: COBOL, JCL, API, SEO, URL

**Common Technical Acronyms**:
- COBOL: COmmon Business-Oriented Language
- JCL: Job Control Language
- BRE: Business Rule Extraction
- API: Application Programming Interface
- LLM: Large Language Model
- AI: Artificial Intelligence
- SME: Subject Matter Expert

**Latin Abbreviations**:
- **Avoid** e.g., i.e., etc. in favor of plain English
- Use instead: "for example," "that is," "and more" or "and so on"

---

## Word Choice & Usage

### Preferred Terms

**Say This** → **Not That**:
- legacy code → old code, outdated code
- application understanding → documentation, code knowledge
- knowledge capture → documentation creation
- tribal knowledge → undocumented knowledge
- onboarding acceleration → training
- enterprise teams → enterprise clients
- modernization confidence → transformation
- knowledge gap → documentation gap
- business rule extraction (BRE) → rule extraction (use full term on first reference)
- reverse engineering → code analysis (when technically accurate)
- deterministic analysis → static analysis (deterministic is more precise for our approach)
- extract → pull, get (more active and specific)
- generate → create, make (emphasizes automation)

### Words to Avoid

**Marketing Jargon** (Never use these):
- synergize, leverage, disrupt, innovate, transform, revolutionize
- game-changing, cutting-edge, next-generation, best-in-class
- unlock, unleash, empower (overused marketing terms)
- digital transformation (use "modernization" instead)

**Fear Language** (Replace with neutral terms):
- nightmare → challenge, significant issue
- disaster, catastrophe → costly problem, critical risk
- crisis → urgent challenge
- struggle, failing → facing challenges

**Hedging Language** (Remove or rephrase):
- might, could, perhaps, potentially, possibly (be direct instead)
- very, really, actually (usually unnecessary padding)

**Vague Terms** (Replace with specifics):
- better, improved → quantify (90% faster, 50% reduction)
- easy, simple → specific benefits
- powerful, robust → describe actual capabilities

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
  - **Deterministic**: Swimm uses deterministic static analysis to ensure accuracy
  - **Scalable**: Swimm can scale to millions of lines of code
- Do NOT use for: Emphasis within paragraphs, key concepts, or takeaways
- Keep it minimal: Bold should be structural, not emphatic

**Italics**:
- Use for: Emphasis (sparingly), example variable names in narrative
- Example: "The variable *RISK-SCORE* determines the application status."
- Avoid: Don't use for code (use backticks instead)

**Code Formatting (backticks)**:
- Use for: Code snippets, variable names, file names, program names, technical values
- Inline: `PERFORM`, `COBOL`, `EMPENT.CBL`
- Example: "The `PERFORM D THRU E` statement executes paragraphs D through E."

**Underline**:
- Don't use (reserve for links only)

**ALL CAPS**:
- Use only for: Standard acronyms (COBOL, JCL, API, LLM)
- Never use for emphasis or shouting

### Lists

**Bulleted Lists**:
- Use for: Non-sequential items, features, benefits, characteristics
- Capitalization: Sentence case (capitalize first word only)
- Punctuation:
  - Period if complete sentence
  - No period if fragment
  - Maintain parallel structure (all sentences OR all fragments, not mixed)
- Example (standard list):
  - Extract business rules automatically from legacy code
  - Generate visual representations of COBOL screens
  - Trace flows across entire applications
- Example (labeled list with bold labels):
  - **Deterministic**: Swimm uses deterministic static analysis to prevent hallucinations
  - **Scalable**: Swimm can scale to millions of lines of legacy code
  - **Traceable**: Every insight links directly back to source code

**Numbered Lists**:
- Use for: Sequential steps, processes, rankings, ordered priorities
- Format: 1. 2. 3. (with period after number)
- Same capitalization and punctuation rules as bullets
- Example:
  1. Read the code
  2. Analyze the logic
  3. Generate documentation

**Nested Lists**:
- Maximum 2 levels deep for readability
- Use proper indentation
- Maintain consistent marker style

### Links

**Anchor Text**:
- Descriptive (tell reader where they're going)
- Keyword-rich when appropriate for SEO
- 2-6 words typically
- ✅ "Learn more about business rule extraction"
- ❌ "Click here" or "Read more"

**Link Formatting**:
- Use markdown format: `[anchor text](url)`
- External links: Open in new tab when implemented
- Internal links: Use relative paths
- No "link" or "here" as anchor text

### Code & Technical Elements

**Inline Code**:
- Use backticks for: Code snippets, program names, file names, variable names, commands
- Example: "Your program `CBACT04C` processes account balances using the `INTEREST-RATE` variable."

**Code Blocks**:
- Use for: Multi-line code, COBOL programs, configuration examples
- Include language identifier: ```cobol or ```python
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
   - Example: "COBOL still powers 80% of in-person credit card transactions."
2. **Problem** (2-3 sentences): What challenge does this address?
   - Example: "Legacy modernization stalls when teams don't understand what exists."
3. **Promise** (2-3 sentences): What will reader learn or achieve?
   - Example: "This guide shows how to extract business rules from complex legacy code."
4. **Credibility** (optional, 1 sentence): Why trust this source?
   - Example: "At Swimm, we've analyzed 100+ million lines of COBOL code."

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
   - Request-focused: "Request a demo" or "Try Swimm on your codebase"
   - Never: "Sign up now!" or urgency manipulation
4. **Forward-looking** (optional, 1 sentence): Encouraging or connecting thought

---

## SEO-Specific Style

### Meta Titles
- 50-60 characters including spaces
- Include primary keyword
- Include "| Swimm" if space allows
- No ending punctuation
- Example: "Extract COBOL Business Rules Automatically | Swimm"

### Meta Descriptions
- 150-160 characters including spaces
- Include primary keyword naturally
- Include benefit or value proposition
- End with complete thought
- Example: "Learn how to extract business logic from legacy COBOL applications automatically. Swimm analyzes code to generate human-readable business rules in hours, not weeks."

### URL Slugs
- Lowercase only
- Hyphens between words (not underscores)
- Include primary keyword
- 3-6 words ideal
- Remove articles (a, an, the) when possible
- Format: `/blog/extract-cobol-business-rules`

### Alt Text
- Describe what image shows concisely
- Include keyword naturally if relevant to the image
- 125 characters or less
- No "image of" or "picture of" (implied)
- Example: "COBOL code snippet showing PERFORM statement with GOTO"

---

## Dates & Time

**Date Format**:
- Use: Month DD, YYYY
- Example: January 15, 2025
- In metadata: YYYY-MM-DD (2025-01-15)

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
- Include year of data: "In 2024, enterprises spent..."
- For internal data: "Swimm has analyzed 100+ million lines of code"

### Presenting Numbers
- Round large numbers: "100 million" not "100,234,567"
- Use % symbol: 90% (not "percent")
- Use specific metrics: "90% faster" not "much faster"
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

### Swimm Product References

**Swimm Platform**:
- "Swimm" (not "the Swimm platform" unless needed for clarity)
- "Swimm's analysis engine"
- "Swimm Collections"

**Features** (capitalize when referring to specific features):
- Business Rule Extraction
- Flow Analysis
- Visual Screen Generation
- Terminology Extraction
- Application Mapping
- Collections
- Context Agent
- Collections Agent

**Technical Approach**:
- "Deterministic + AI approach" (our unique differentiator)
- "Deterministic analysis" (not just "static analysis")
- "Application understanding" (our broader value proposition)

### Technology References

**Legacy Technologies**:
- COBOL (all caps)
- JCL (all caps)
- mainframe (lowercase)
- Refer respectfully - these are critical business systems, not "outdated junk"

**Modern Technologies**:
- AI (all caps)
- LLM (all caps, spell out on first use: Large Language Model)
- API (all caps)

### Competitor References
- **Approach**: Name competitors when relevant and factual
- Be fair and objective
- Focus on differentiation, not criticism
- Example: "Unlike raw LLMs that can hallucinate, Swimm's deterministic analysis ensures..."
- Never disparage or use fear tactics

---

## Accessibility

### Screen Reader Friendly
- Descriptive link text (never "click here")
- Alt text for all images
- Proper heading hierarchy (H1 → H2 → H3, never skip levels)
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
- [ ] Preferred terminology used (legacy code, application understanding, etc.)
- [ ] No marketing jargon or fear language
- [ ] No hedging language (might, could, perhaps)
- [ ] Bold only used for headers and labeled list items (not for emphasis)
- [ ] Backticks used for all code/technical terms
- [ ] Links are descriptive
- [ ] Voice and tone appropriate for content type

**Structure**:
- [ ] Strong introduction (hook, problem, promise)
- [ ] Logical section flow with clear transitions
- [ ] Proper heading hierarchy (H1 → H2 → H3)
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

**Swimm-Specific**:
- [ ] Customer-centric framing (they're heroes, not the problem)
- [ ] Quantified benefits where possible (90% faster, 50% reduction, etc.)
- [ ] Technical credibility demonstrated
- [ ] Differentiators highlighted appropriately
- [ ] Product mentions feel natural, not forced
- [ ] No exclamation marks (unless absolutely necessary)
- [ ] No emojis

---

## Updates & Maintenance

**Style Guide Version**: 1.0
**Last Updated**: December 2025
**Next Review**: Quarterly

This style guide is a living document. Update as Swimm brand and voice evolve.

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
