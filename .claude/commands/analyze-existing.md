# Analyze Existing Command

Use this command to review and analyze existing your company blog posts for SEO opportunities, content gaps, and improvement areas.

## Usage
`/analyze-existing [URL or file path]`

## What This Command Does
1. Fetches and analyzes existing blog post content
2. Evaluates current SEO performance and optimization
3. Identifies outdated information or statistics
4. Suggests content expansion opportunities
5. Provides actionable improvement recommendations

## Process

### Input Resolution

When the input is a **URL or slug** (starts with `http`, `www.`, a known domain like `swimm.io`, or matches a known slug in the database), resolve the article through the content library before proceeding:

#### Step 1: Extract the slug
- If a full or partial URL is provided (e.g., `https://swimm.io/learn/...`, `www.swimm.io/learn/...`, `swimm.io/learn/...`), extract the slug from the URL path (last non-empty segment)
- If a slug is provided directly (no slashes, no domain), use it as-is

#### Step 2: Sync fresh content from WordPress
```python
from data_sources.modules.content_library import sync_article
success, msg = sync_article('<slug-or-url>')
```
This pulls the latest version from WordPress into the content library database. If a bare domain URL was provided (no `http`), prepend `https://` before passing to `sync_article()`.

#### Step 3: Checkout to workbench
```python
from data_sources.modules.content_library import checkout
success, workbench_path = checkout('<slug>', fresh=False)  # fresh=False since we just synced
```
This creates `content/workbench/{slug}/` with:
- `original.html` — Raw Gutenberg HTML
- `article.md` — Converted markdown (used for analysis)
- `metadata.json` — Meta title, meta description, URL, post ID, status

#### Step 4: Load article content for analysis
- Read `content/workbench/{slug}/article.md` as the article content
- Read `content/workbench/{slug}/metadata.json` for existing meta title, meta description, and URL slug
- Use these as the basis for the full analysis below

**Note:** If the article is not found in the database, attempt `sync_article()` with the URL first. If that also fails, inform the user to run `/library sync` to populate the database.

When the input is a **local file path** (contains a file extension like `.md` or starts with a relative/absolute path like `content/drafts/`, `content/rewrites/`, `./`, `/`), proceed directly to the Content Analysis using that file.

---

### Content Analysis
- **URL/File Input**: Accept either a live URL or local file path
- **Content Extraction**: Pull the full article text, headings, and structure
- **Publication Date Check**: Note when content was originally published
- **Current Relevance**: Identify outdated information, statistics, or references
- **Completeness**: Assess if topic coverage is comprehensive or has gaps

### SEO Audit (Enhanced with New Analysis Tools)
- **Search Intent Analysis** (NEW!): Determine if content matches user search intent (informational/commercial/transactional/navigational)
- **Target Keyword**: Identify primary keyword and variations
- **Keyword Density & Clustering** (NEW!): Deep analysis of keyword density, distribution heatmap, topic clustering, and keyword stuffing risk detection
- **Keyword Placement**: Check H1, H2, first 100 words, meta title/description
- **Heading Structure**: Evaluate H1-H6 hierarchy and keyword integration
- **Content Length Comparison** (NEW!): Compare word count against top 10-20 SERP competitors to determine optimal length
- **Meta Elements**: Review meta title (50-60 chars) and description (150-160 chars)
- **Internal Links**: Count and evaluate quality of internal links (aim for 3-5+)
- **External Links**: Check for authoritative external sources
- **Readability Score** (NEW!): Calculate Flesch Reading Ease, Flesch-Kincaid Grade Level, passive voice ratio, sentence complexity
- **SEO Quality Rating** (NEW!): Overall score (0-100) with category breakdowns for content, keywords, meta, structure, links, and readability

### Competitive Context
- **SERP Position**: Research current ranking for target keywords (if known)
- **Top Competitors**: Identify top 3-5 ranking articles for same keywords
- **Content Gaps**: What do competitors cover that this article doesn't?
- **Competitive Advantage**: What unique angles or insights could differentiate this?

### User Experience
- **Introduction Hook**: Is the opening compelling and clear?
- **Structure**: Does the article flow logically with clear sections?
- **Actionability**: Are there practical takeaways and next steps?
- **Visual Elements**: Note if images, screenshots, or media are mentioned/needed
- **Call-to-Action**: Is there a clear CTA aligned with user intent?

## Output
Provides a comprehensive analysis report with:

### 1. Content Health Score (0-100)
Enhanced with new analysis modules:
- **SEO Quality Rating**: Overall SEO score with category breakdowns
- **Search Intent Alignment**: How well content matches search intent
- **Keyword Optimization**: Density, distribution, clustering analysis
- **Content Length Competitiveness**: Position vs SERP competitors
- **Readability Score**: Flesch scores and grade level
- **Relevance & Freshness**: Outdated content detection
- **User Experience**: Flow, structure, actionability

### 2. Quick Wins
Top 3-5 immediate improvements that can be made quickly:
- Update specific statistics or dates
- Add missing keywords to headings (with exact density recommendations)
- Optimize meta description
- Add internal links to specific pages
- Fix readability issues (sentence length, passive voice)

### 3. Strategic Improvements
Longer-term enhancements for maximum impact:
- **Content expansion**: Based on length comparison with competitors (e.g., "Add 800 words to match top performers")
- **Intent alignment**: Adjust content type to match search intent
- **Topic clustering**: Add missing semantic keywords and related topics
- New sections to add based on competitive gap analysis
- SEO optimization priorities from quality rating

### 4. Detailed Analysis Reports
The new Content Analyzer agent provides:
- **Search intent classification** with confidence scores
- **Keyword density heatmap** by section
- **Topic cluster visualization**
- **Competitive length benchmarks** (min, median, 75th percentile)
- **Readability metrics** (Flesch scores, sentence analysis, passive voice ratio)
- **SEO quality breakdown** by category (0-100 for each)

### 5. Rewrite Recommendations
- **Priority Level**: Low / Medium / High / Critical (based on SEO score and competitive analysis)
- **Estimated Effort**: Light edit / Moderate update / Major rewrite / Complete refresh
- **Expected Impact**: Potential traffic increase, ranking improvement, engagement boost (data-driven estimates)
- **Specific improvements needed**: Exact word count targets, keyword density adjustments, readability fixes

### 6. Research Brief
If a rewrite is recommended, provide initial research brief including:
- Updated target keywords with optimal density targets
- Competitor articles to review with word count benchmarks
- New statistics or data to incorporate
- Trending angles or perspectives
- Search intent alignment strategy
- Optimal content length recommendation (based on SERP analysis)
- Internal linking opportunities

## File Management
After completing the analysis, save the report based on input type:

**For URL/slug input (content library):**
- **File Location**: `content/workbench/[slug]/analysis-report.md`
- **Naming Convention**: Save in the workbench folder alongside the checked-out article
- Example: `content/workbench/podcast-hosting-guide/analysis-report.md`

**For local file input:**
- **File Location**: `content/research/analysis-[post-slug]-[YYYY-MM-DD].md`
- **Naming Convention**: Use lowercase, hyphenated post slug and current date
- Example: `content/research/analysis-podcast-hosting-guide-2025-10-15.md`

- **File Format**: Markdown with scores, recommendations, and action items

## Next Steps
Based on the analysis, the system will suggest:
1. Running `/rewrite [topic]` if content needs significant updates
2. Running `/optimize [file]` if content needs light SEO polish
3. Archiving the post if it's no longer relevant or valuable

This ensures every analysis leads to clear, actionable next steps for improving your company blog content.
