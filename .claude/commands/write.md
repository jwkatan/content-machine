# Write Command

Use this command to create comprehensive long-form blog content.

## Usage
`/write [topic or research brief]`

## Content Type Detection

Before writing, determine the content type. Check the idea file (if one exists in `ideas/`) for a **Type** field, or infer from the topic:

- **`seo`** (default): Keyword-optimized articles designed to rank. Follows full SEO process below.
- **`thought-leadership`**: Position-driven articles that build a framework, take a stance, or explore an idea. Follows the thought leadership process below.

If unclear, ask the user which type to use.

## What This Command Does

### For SEO content (default)
1. Creates complete, well-structured long-form articles (2000-3000+ words)
2. Optimizes content for target keywords and SEO best practices
3. Maintains your brand voice and messaging throughout
4. Integrates internal and external links strategically
5. Includes all meta elements for publishing

### For thought leadership content
1. Creates complete, well-structured long-form articles (1500-2500+ words)
2. Builds a clear argument, framework, or position
3. Maintains your brand voice - especially the "Strategy/Advice" and "Confident Expert Colleague" tones from @context/brand-voice.md
4. Prioritizes clarity of thinking, originality of perspective, and strength of argument over keyword optimization
5. Includes meta elements for publishing (lighter SEO touch)

## Process

### Pre-Writing Review
- **Research Brief**: Review research brief from `/research` command if available
- **Brand Voice**: Check @context/brand-voice.md for tone and messaging
- **Writing Examples**: Study @context/writing-examples.md for style consistency (note: there are both SEO and thought leadership examples)
- **Style Guide**: Follow formatting rules from @context/style-guide.md
- **SEO Guidelines** (SEO content only): Apply requirements from @context/seo-guidelines.md
- **Target Keywords** (SEO content only): Integrate keywords from @context/target-keywords.md naturally
- **Idea File**: If writing from an idea in `ideas/`, read it for concept, angles, and any notes from brainstorming

### Content Structure (SEO)

> Use this structure for `seo` content type.

#### 1. Headline (H1)
- Include primary keyword naturally
- Create compelling, click-worthy title
- Keep under 60 characters for SERP display
- Promise clear value to reader

#### 2. Introduction (150-200 words)
- **Hook**: Open with attention-grabbing statement, question, or statistic
- **Problem**: Clearly articulate the challenge or question
- **Promise**: Tell reader what they'll learn or gain
- **Keyword**: Include primary keyword in first 100 words
- **Credibility**: Establish why you/this article is authoritative

#### 3. Main Body (1800-2500+ words)
- **Logical Flow**: Organize sections in clear, progressive order
- **H2 Sections**: 4-7 main sections covering comprehensive topic scope
- **H3 Subsections**: Break complex sections into digestible pieces
- **Keyword Integration**: Use primary keyword 1-2% density, variations throughout
- **Depth**: Provide thorough, actionable information at each point
- **Examples**: Include real scenarios and use cases relevant to your industry
- **Data**: Reference statistics and studies to support claims
- **Visuals**: Note where images, screenshots, or graphics enhance understanding
- **Lists**: Use bulleted or numbered lists for scannability
- **Formatting**: Bold key concepts, use short paragraphs (2-4 sentences)

#### 4. Conclusion (150-200 words)
- **Recap**: Summarize 3-5 key takeaways
- **Action**: Provide clear next steps for reader
- **CTA**: Include relevant call-to-action (free trial, resource download, demo, etc.)
- **Encouragement**: End on empowering, forward-looking note

### Content Structure (Thought Leadership)

> Use this structure for `thought-leadership` content type.

#### 1. Headline (H1)
- Lead with the idea, position, or framework - not a keyword
- Can be longer than 60 characters if needed for clarity
- Should make the reader think "I want to understand this perspective"
- Sentence case per style guide

#### 2. Opening (150-250 words)
- **Observation**: Open with a tension, pattern, or counterintuitive observation from industry experience
- **Stakes**: Why this matters now - what's at risk or what's changing
- **Thesis**: State the position or framework clearly. The reader should know within 200 words what argument this article is making
- **No keyword stuffing**: Use natural language; SEO is secondary

#### 3. Main Body (1200-2000+ words)
- **Argument-driven structure**: Each H2 should advance the argument or build a piece of the framework - not just cover a subtopic
- **H2 Sections**: 3-5 main sections (fewer, deeper sections rather than broad coverage)
- **Honest costs**: Address trade-offs, challenges, and counterarguments directly. Do not present a one-sided case
- **Concrete grounding**: Use real scenarios, examples from experience, or specific industry patterns to support abstract concepts
- **Frameworks over advice**: Where possible, give the reader a mental model they can apply, not just a list of tips
- **Varied evidence**: Draw from experience, industry patterns, technical realities, and logical reasoning - not just statistics
- **Formatting**: Short paragraphs (2-4 sentences), varied sentence length, no filler

#### 4. Conclusion (100-200 words)
- **Synthesis**: Bring the argument to a clear landing - what should the reader take away?
- **Honest ending**: Acknowledge open questions or unresolved tensions where they exist
- **Forward-looking**: Point toward what comes next for the reader or the industry
- **CTA**: Optional and lighter touch - a demo request or related resource, not a hard sell

### SEO Optimization (SEO content only)

> Skip this section entirely for thought leadership content.

#### Keyword Placement
- H1 headline
- First paragraph (within first 100 words)
- At least 2-3 H2 headings
- Naturally throughout body (1-2% density)
- Meta title and description
- URL slug

#### Internal Linking (3-5+ links)
- Reference @context/internal-links-map.md for key pages
- Link to relevant pillar content from your site
- Link to related blog articles
- Link to product/service pages where natural
- Use descriptive anchor text with keywords

#### External Linking (2-3 links)
- Link to authoritative sources for statistics
- Reference industry research or studies
- Link to tools or resources mentioned
- Build credibility with quality sources

#### Readability
- Keep sentences under 25 words average
- Use transition words between sections
- Vary sentence length for rhythm
- Write at 8th-10th grade reading level
- Use active voice predominantly
- Break up text with subheadings every 300-400 words

### Linking (Thought Leadership)

> For thought leadership content, linking is lighter and more natural.

- **Internal links**: 1-3 where genuinely relevant. Do not force links to meet a quota.
- **External links**: 1-2 to authoritative sources, research, or frameworks referenced. Only link if it genuinely supports the argument.
- **No keyword-driven anchor text**: Use natural, descriptive link text.

### Target Audience Focus
- **Audience Perspective**: Write for your target audience (defined in @context/brand-voice.md)
- **Practical Application**: Show how information applies to their specific challenges
- **Product Integration** (SEO): Naturally mention how your features solve problems (reference @context/features.md)
- **Product Integration** (Thought Leadership): Product mentions are optional. If Swimm is relevant to the argument, include it naturally. If the article makes a stronger case without product mentions, leave them out. Use Part 1 of brand voice only unless Swimm is genuinely part of the argument.
- **Industry Context**: Reference relevant trends and best practices
- **Technical Accuracy**: Ensure terminology and processes are correct for your industry

### Brand Voice Consistency
- Maintain your brand tone (reference @context/brand-voice.md for specifics)
- Follow your established voice pillars
- Use messaging framework from your context files
- Apply terminology preferences consistently
- For SEO content: Match tone to content type (how-to, strategy, news, etc.)
- For thought leadership: Use the "Strategy/Advice Content" or "Confident Expert Colleague" tone. Write as someone who has earned the perspective through experience, not as someone optimizing for search.

## Output
Provides a complete, publish-ready article including:

### 1. Article Content
Full markdown-formatted article with:
- H1 headline
- Introduction
- Body sections with H2/H3 structure
- Conclusion with CTA
- Proper formatting and styling

### 2. Meta Elements

#### SEO content
```
---
Meta Title: [50-60 character optimized title]
Meta Description: [150-160 character compelling description]
Primary Keyword: [main target keyword]
Secondary Keywords: [keyword1, keyword2, keyword3]
URL Slug: /blog/[optimized-slug]
Internal Links: [list of pages linked from your site]
External Links: [list of external sources]
Word Count: [actual word count]
Content Type: seo
---
```

#### Thought leadership content
```
---
Meta Title: [50-60 character optimized title]
Meta Description: [150-160 character compelling description]
Topic: [central idea or thesis]
URL Slug: /blog/[optimized-slug]
Internal Links: [list of pages linked, if any]
External Links: [list of external sources, if any]
Word Count: [actual word count]
Content Type: thought-leadership
---
```

### 3. Quality Checklist

#### SEO Checklist (SEO content only)
- [ ] Primary keyword in H1
- [ ] Primary keyword in first 100 words
- [ ] Primary keyword in 2+ H2 headings
- [ ] Keyword density 1-2%
- [ ] 3-5+ internal links included
- [ ] 2-3 external authority links
- [ ] Meta title 50-60 characters
- [ ] Meta description 150-160 characters
- [ ] Article 2000+ words
- [ ] Proper H2/H3 hierarchy
- [ ] Readability optimized
- [ ] CTA included

#### Thought Leadership Checklist (thought leadership content only)
- [ ] Clear thesis or position stated within first 200 words
- [ ] Each H2 advances the argument (not just a subtopic)
- [ ] Trade-offs and counterarguments addressed honestly
- [ ] Grounded in concrete examples, scenarios, or experience
- [ ] Framework or mental model the reader can apply
- [ ] No keyword stuffing or forced SEO patterns
- [ ] Brand voice maintained (Part 1 of brand-voice.md)
- [ ] Article 1500+ words
- [ ] Proper H2/H3 hierarchy
- [ ] Meta title and description included
- [ ] CTA included (can be lighter touch)

## File Management
After completing the article, automatically save to a project subfolder:
- **Folder**: `content/drafts/[YYQ#]-[topic-slug]/` (create if it doesn't exist)
- **File Location**: `content/drafts/[YYQ#]-[topic-slug]/[topic-slug]-[YYYY-MM-DD].md`
- **File Format**: Markdown with frontmatter and formatted content
- **Naming Convention**: Quarter prefix (e.g., 26Q1) + topic slug for folder, topic slug + date in filename

Example: `content/drafts/25Q4-content-marketing-strategies/content-marketing-strategies-2025-10-29.md`

## Automatic Content Scrubbing
**IMPORTANT**: Immediately after saving the article file, automatically scrub the content to remove AI watermarks:

1. Run the content scrubber on the saved file:
```python
import sys
sys.path.append('data_sources/modules')
from content_scrubber import scrub_file

# Scrub the file (overwrites with cleaned version)
scrub_file('content/drafts/[YYQ#]-[topic-slug]/[topic-slug]-[YYYY-MM-DD].md', verbose=True)
```

2. This removes:
   - All invisible Unicode watermarks (zero-width spaces, format-control characters, etc.)
   - Em-dashes, replaced with contextually appropriate punctuation

3. The scrubbing happens silently and automatically - no user action required

**Result**: Content is clean of AI watermarks before agents analyze it.

## Automatic Agent Execution
After saving the main article, execute optimization agents based on content type.

### SEO content: run all agents

#### 1. Content Analyzer Agent
- **Agent**: `content-analyzer`
- **Input**: Full article, meta elements, keywords, SERP data (if available)
- **Output**: Comprehensive analysis covering search intent, keyword density, content length comparison, readability score, and SEO quality rating
- **File**: `content/drafts/[YYQ#]-[topic-slug]/content-analysis.md`

This new agent uses 5 specialized analysis modules:
- Search intent analysis
- Keyword density & clustering
- Content length vs competitors
- Readability scoring (Flesch scores)
- SEO quality rating (0-100)

#### 2. SEO Optimizer Agent
- **Agent**: `seo-optimizer`
- **Input**: Full article content
- **Output**: SEO optimization report and suggestions
- **File**: `content/drafts/[YYQ#]-[topic-slug]/seo-report.md`

#### 3. Meta Creator Agent
- **Agent**: `meta-creator`
- **Input**: Article content and primary keyword
- **Output**: Multiple meta title/description options
- **File**: `content/drafts/[YYQ#]-[topic-slug]/meta-options.md`

#### 4. Internal Linker Agent
- **Agent**: `internal-linker`
- **Input**: Article content
- **Output**: Specific internal linking recommendations
- **File**: `content/drafts/[YYQ#]-[topic-slug]/link-suggestions.md`

#### 5. Keyword Mapper Agent
- **Agent**: `keyword-mapper`
- **Input**: Article and target keywords
- **Output**: Keyword placement analysis and improvements
- **File**: `content/drafts/[YYQ#]-[topic-slug]/keyword-analysis.md`

#### 6. LinkedIn Repurposer Agent
- **Agent**: `linkedin-repurposer`
- **Input**: Article content
- **Output**: LinkedIn post appended as "## LinkedIn Post" section at the end of the article
- **File**: Same as main article (append to `content/drafts/[YYQ#]-[topic-slug]/article-[YYYY-MM-DD].md`)

#### 7. Newsletter Repurposer Agent
- **Agent**: `newsletter-repurposer`
- **Input**: Article content
- **Output**: Newsletter email appended as "## Newsletter" section at the end of the article
- **File**: Same as main article (append to `content/drafts/[YYQ#]-[topic-slug]/article-[YYYY-MM-DD].md`)

### Thought leadership content: run selected agents only

Skip SEO-focused agents (Content Analyzer, SEO Optimizer, Keyword Mapper). Run:

#### 1. Argument Reviewer Agent
- **Agent**: `argument-reviewer` (use `general-purpose` subagent)
- **Input**: Full article content and the idea file (if available)
- **Prompt**: Review this thought leadership article for argument quality. Evaluate: (1) Is the thesis clear and stated early? (2) Does each section advance the argument or just fill space? (3) Are trade-offs and counterarguments addressed honestly? (4) Is the article grounded in concrete examples, not just abstractions? (5) Does it give the reader a framework or mental model they can apply? (6) Are there sections that repeat points already made? Provide specific, actionable feedback.
- **Output**: Argument quality review with specific suggestions
- **File**: `content/drafts/[YYQ#]-[topic-slug]/argument-review.md`

#### 2. Meta Creator Agent
- **Agent**: `meta-creator`
- **Input**: Article content and central topic/thesis
- **Output**: Multiple meta title/description options
- **File**: `content/drafts/[YYQ#]-[topic-slug]/meta-options.md`

#### 3. Internal Linker Agent
- **Agent**: `internal-linker`
- **Input**: Article content
- **Output**: Internal linking suggestions (lighter touch - only genuinely relevant links)
- **File**: `content/drafts/[YYQ#]-[topic-slug]/link-suggestions.md`

#### 4. LinkedIn Repurposer Agent
- **Agent**: `linkedin-repurposer`
- **Input**: Article content
- **Output**: LinkedIn post appended as "## LinkedIn Post" section at the end of the article
- **File**: Same as main article (append to `content/drafts/[YYQ#]-[topic-slug]/article-[YYYY-MM-DD].md`)

#### 5. Newsletter Repurposer Agent
- **Agent**: `newsletter-repurposer`
- **Input**: Article content
- **Output**: Newsletter email appended as "## Newsletter" section at the end of the article
- **File**: Same as main article (append to `content/drafts/[YYQ#]-[topic-slug]/article-[YYYY-MM-DD].md`)


## Quality Standards

### SEO content
Every SEO article must meet these requirements:
- Minimum 2000 words (2500-3000+ preferred)
- Proper H1/H2/H3 hierarchy
- Primary keyword naturally integrated
- 3-5 internal links to your site content
- 2-3 external authoritative links
- Compelling meta title and description
- Clear introduction and conclusion
- Actionable, valuable information
- Brand voice maintained (from @context/brand-voice.md)
- Target audience focused
- Publish-ready quality

### Thought leadership content
Every thought leadership article must meet these requirements:
- Minimum 1500 words (2000-2500 preferred)
- Proper H1/H2/H3 hierarchy
- Clear thesis or position stated early
- Argument advances through each section (no filler sections)
- Trade-offs and counterarguments addressed honestly
- Grounded in concrete examples, experience, or industry patterns
- Framework or mental model the reader can apply
- Internal links only where genuinely relevant (not required)
- Compelling meta title and description
- Brand voice maintained (Part 1 of @context/brand-voice.md; Part 2 only if Swimm is part of the argument)
- Target audience focused
- Publish-ready quality

Both content types ensure articles provide genuine value to the target audience.
