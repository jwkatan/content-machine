# Research Command

Use this command to conduct comprehensive research before writing new content.

## Usage
`/research [topic]`

## Content Type Detection

Before researching, determine the content type. Check the idea file (if one exists in `ideas/`) for a **Type** field, or infer from the topic:

- **`seo`** (default): Full SEO keyword research and competitive SERP analysis.
- **`thought-leadership`**: Landscape research focused on existing arguments, prevailing takes, and positioning gaps.

If unclear, ask the user which type to use.

## What This Command Does

### For SEO content (default)
1. Performs keyword research for your industry-related topics
2. Analyzes top-ranking competitor content
3. Identifies content gaps and opportunities
4. Develops unique angle for Swimm perspective
5. Creates detailed research brief for writing

### For thought leadership content
1. Researches what's already been said about this topic (prevailing takes, common frameworks, existing arguments)
2. Identifies positioning gaps - perspectives that are missing, underexplored, or wrong
3. Finds concrete evidence to support or challenge the thesis (industry reports, examples, real-world patterns)
4. Develops the unique angle and argument structure
5. Creates a research brief focused on argument strength, not keyword optimization

---

## SEO Research Process

> Use this process for `seo` content type.

### Keyword Research
- **Primary Keyword**: Identify main target keyword for the topic
- **Search Volume & Difficulty**: Research estimated monthly searches and competition level
- **Keyword Variations**: Find semantic variations and long-tail opportunities
- **Related Questions**: Discover what people are actually asking (People Also Ask, forums, Reddit)
- **Search Intent**: Determine if intent is informational, navigational, commercial, or transactional
- **Topic Cluster**: Identify how this topic fits into Swimm content clusters

### Competitive Analysis
- **Top 10 SERP Review**: Analyze the top 10 ranking articles for target keyword
- **Content Length**: Note word count of top-performing articles (benchmark target)
- **Common Themes**: What topics/sections do all top articles cover?
- **Content Gaps**: What's missing from competitor coverage?
- **Unique Angles**: What perspectives or insights are underexplored?
- **Featured Snippets**: Identify if there's a featured snippet opportunity
- **Domain Authority**: Note which competitors rank (indie blogs vs. major publications)

### Context Integration
- **Swimm Advantage**: How can Swimm product features naturally enhance this content?
- **Brand Alignment**: Check @context/brand-voice.md for messaging fit
- **Existing Content**: Review @context/internal-links-map.md for related Swimm articles
- **Target Keywords**: Cross-reference with @context/target-keywords.md priority list
- **SEO Guidelines**: Ensure research aligns with @context/seo-guidelines.md requirements

### Industry Focus
- **Audience Angle**: How does this topic specifically impact the target audience?
- **Technical Requirements**: Any industry-specific technical considerations?
- **Industry Trends**: Current trends that relate to this topic
- **Use Cases**: Real scenarios where this topic matters for the target audience
- **Pain Points**: Specific challenges the target audience faces with this topic

### Content Planning
- **Recommended Structure**: Outline H2 and H3 headings based on research
- **Content Depth**: Determine target word count (typically 2000-3000+ for SEO)
- **Supporting Evidence**: Identify statistics, studies, or data to include
- **Expert Sources**: Find industry experts or quotes to reference
- **Visual Opportunities**: Suggest images, screenshots, or graphics needed
- **Internal Links**: Map 3-5 key Swimm pages to link to (from @context/internal-links-map.md)
- **External Authority**: Identify 2-3 authoritative external sources to link
- **Structural Integrity**: Each H2/H3 must own a distinct scope - no two sections should cover the same fact, argument, or concept

### Hook Development
- **Introduction Angle**: Compelling way to open the article
- **Value Proposition**: Clear benefit reader will get from article
- **Contrarian Elements**: Any unexpected perspectives to explore
- **Story Opportunities**: Real examples or case studies to feature

---

## Thought Leadership Research Process

> Use this process for `thought-leadership` content type.

### Landscape Analysis
Research what already exists on this topic. The goal is to understand the current conversation so the article can add to it, not repeat it.

- **Prevailing takes**: What do most articles, posts, and talks say about this topic? What's the conventional wisdom?
- **Common frameworks**: Are there existing frameworks, models, or mental models that people use to think about this? What's missing from them?
- **Key voices**: Who has written or spoken about this topic credibly? What positions have they taken?
- **Gaps and blind spots**: What perspectives are missing? What questions aren't being asked? Where is the conventional wisdom incomplete or wrong?
- **Counterarguments**: What are the strongest arguments against the position the article will take? These need to be addressed honestly.

### Thesis Development
Develop the article's core argument based on the landscape analysis and idea file.

- **Central thesis**: One clear statement of what the article argues. This should be specific enough that someone could disagree with it.
- **Why now**: Why does this argument matter at this moment? What's changed?
- **What's at stake**: What happens if the reader ignores this perspective?
- **Unique angle**: What does Swimm's experience or perspective add that others can't?

### Evidence Gathering
Find concrete material to support the argument. Thought leadership without evidence is just opinion.

- **Industry patterns**: Real-world examples and patterns that support the thesis
- **Data points**: Statistics, benchmarks, or research findings (with sources)
- **Experience-based evidence**: Scenarios from modernization projects, enterprise transformations, or product building that illustrate the point
- **Analogies and frameworks**: Useful mental models that make the argument concrete and memorable
- **Counterexamples**: Cases where the thesis doesn't hold - acknowledge these for intellectual honesty

### Argument Structure
Plan how the argument builds across the article.

- **Recommended outline**: H2 and H3 headings structured as argument progression (not just topic coverage)
- **Each section's job**: For each H2, state what it needs to prove or establish for the overall argument
- **Trade-offs section**: Where in the article will costs, challenges, and honest limitations be addressed?
- **Structural integrity**: Each H2/H3 must own a distinct scope - no two sections should cover the same fact, argument, or concept

### Context Integration
- **Swimm relevance**: Is Swimm part of the argument, or is this pure industry thought leadership? If Swimm is relevant, where does it fit naturally?
- **Brand alignment**: Check @context/brand-voice.md Part 1 for voice consistency
- **Existing content**: Review @context/internal-links-map.md for related articles (link only if genuinely relevant)

---

## Output

### SEO Research Brief

Provides a comprehensive research brief with:

#### 1. SEO Foundation
- **Primary Keyword**: [keyword] (volume, difficulty)
- **Secondary Keywords**: 3-5 related keywords and variations
- **Target Word Count**: Minimum words needed to compete
- **Featured Snippet Opportunity**: Yes/No, format (paragraph, list, table)

#### 2. Competitive Landscape
- **Top 3 Competitor Articles**: URLs and key takeaways from each
- **Common Sections**: Must-cover topics based on SERP analysis
- **Content Gaps**: Opportunities to provide unique value
- **Differentiation Strategy**: How Swimm can stand out

#### 3. Recommended Outline
```
H1: [Optimized headline with primary keyword]

Introduction
- Hook
- Problem statement
- Value proposition

H2: [Main section 1]
H3: [Subsection]
H3: [Subsection]

H2: [Main section 2]
...

Conclusion
- Key takeaways
- Call to action
```

#### 4. Supporting Elements
- **Statistics to Include**: 5-7 relevant data points with sources
- **Expert Quotes**: Potential sources or existing quotes
- **Examples/Case Studies**: Real scenarios to feature
- **Visual Suggestions**: Screenshots, charts, or graphics needed

#### 5. Internal Linking Strategy
- **Pillar Page**: Main Swimm pillar content to link to
- **Related Articles**: 2-4 relevant blog posts to link
- **Product Pages**: Swimm features to naturally mention
- **Resource Pages**: Tools or guides to reference

#### 6. Meta Elements Preview
- **Meta Title**: Draft optimized title (50-60 characters)
- **Meta Description**: Draft compelling description (150-160 characters)
- **URL Slug**: Recommended URL structure

### Thought Leadership Research Brief

Provides a research brief focused on argument strength:

#### 1. Landscape Summary
- **Prevailing takes**: 3-5 common positions on this topic with representative sources
- **Gaps identified**: What's missing, underexplored, or wrong in the current conversation
- **Key voices**: Who has credibility on this topic and what they've said

#### 2. Thesis and Position
- **Central thesis**: Clear statement of what the article will argue
- **Why this matters now**: What's changed that makes this argument timely
- **Unique angle**: What Swimm's experience or perspective adds

#### 3. Recommended Outline
```
H1: [Headline that captures the position or framework]

Opening
- Observation or tension
- Stakes
- Thesis statement

H2: [Argument section 1 - what it needs to establish]
H3: [Supporting point]

H2: [Argument section 2]
...

H2: [Trade-offs and honest limitations]

Conclusion
- Synthesis
- Forward-looking implications
```

#### 4. Evidence and Supporting Material
- **Data points**: Statistics or research with sources
- **Industry patterns**: Real-world examples that support the argument
- **Counterarguments to address**: Strongest objections and how to handle them
- **Analogies or frameworks**: Mental models that make the argument concrete

#### 5. Meta Elements Preview
- **Meta Title**: Draft title (can exceed 60 characters if clarity requires it)
- **Meta Description**: Draft compelling description (150-160 characters)
- **URL Slug**: Recommended URL structure

## File Management
After completing the research, automatically save the brief to:
- **File Location**: `content/research/brief-[topic-slug]-[YYYY-MM-DD].md`
- **File Format**: Markdown with clear sections and structured data
- **Naming Convention**: Use lowercase, hyphenated topic slug and current date

Example: `content/research/brief-podcast-editing-software-2025-10-15.md`

## Automatic Structural Review

After saving the research brief, **automatically** launch a Task subagent to review the outline for structural redundancy before the brief is considered complete.

### What the Subagent Does
The subagent runs the structural redundancy check from `/review-content` (Step 2) against the Recommended Outline of the brief:

1. **Map each H2/H3's scope** — What facts, arguments, and concepts does each section plan to cover?
2. **Cross-compare for overlap** — Identify any fact, statistic, or argument that would appear in more than one section
3. **Flag scope collisions** — Sections whose topics substantially overlap (e.g., two sections both covering "deterministic understanding + AI" from different angles)
4. **Recommend fixes** — For each redundancy, state which section should own the content and what the overlapping section should cover instead

### How to Launch
Use the Task tool with `subagent_type: "general-purpose"`:
- **Input**: The full Recommended Outline section from the brief, plus the article title
- **Prompt**: Review this outline for structural redundancy. For each H2/H3, list its core scope. Flag any sections that share facts, arguments, or overlapping concepts. For each overlap, recommend which section should own the content and what the other section should cover instead. Return a short report with findings and recommended outline adjustments.

### Handling Results
- **No redundancies found**: Proceed — the brief is complete as-is
- **Redundancies found**: Apply the subagent's consolidation recommendations to the outline, then validate before re-saving:

  **For SEO content**, validate against SEO constraints:
  1. **H2 count**: The revised outline must retain 4-7 H2 sections. If a merge drops below 4, split a dense section or introduce a new angle from the competitive gaps analysis.
  2. **Keyword placement**: The primary keyword or variations must appear in at least 2-3 H2 titles. If a merge removes a keyword-bearing H2, redistribute the keyword into the merged title or another H2.
  3. **Content gap coverage**: Every competitive gap identified in the Competitive Landscape section must still have a home in the outline. If a merge orphans a gap, assign it to the most relevant remaining section.
  4. **Word count**: Consolidation frees word budget. Reallocate the saved words toward deeper coverage in remaining sections rather than cutting total length.

  **For thought leadership content**, validate against argument quality:
  1. **H2 count**: The revised outline should have 3-5 H2 sections. Fewer, deeper sections are better than broad coverage.
  2. **Argument progression**: Each remaining H2 must advance the argument. If a merge creates a section that's just "more information" without advancing the thesis, restructure.
  3. **Trade-offs coverage**: Ensure the outline still has a clear home for honest costs and counterarguments.

  After validation, re-save the updated brief. Note in the brief that a structural review was performed and what was changed.

## Next Steps
The research brief serves as the foundation for:
1. Running `/write [topic]` to create the article
2. Reference material for maintaining focus throughout writing
3. For SEO content: checklist to ensure all competitive gaps are addressed
4. For thought leadership: anchor for argument structure and positioning

This ensures every article is built on solid research and clear strategic positioning.
