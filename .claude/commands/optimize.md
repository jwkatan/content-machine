# Optimize Command

Use this command to perform a final SEO optimization pass on completed articles before publishing.

## Usage
`/optimize [article file or URL]`

**Two input modes:**
- **Local file**: `/optimize content/drafts/25Q4-podcast-analytics/article.md` — optimizes a local draft
- **URL**: `/optimize https://yoursite.com/learn/category/article-slug/` — pulls the live article from the content library database, refreshes it from WordPress, and optimizes it

## What This Command Does
1. Resolves input (local file or URL/slug from content library)
2. Performs comprehensive SEO audit of article
3. Fine-tunes keyword placement and density
4. Optimizes meta elements for SERP performance
5. Validates internal and external links
6. Ensures all SEO best practices are met

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
- `article.md` — Converted markdown (used for the optimization audit)
- `metadata.json` — Meta title, meta description, URL, post ID, status

#### Step 4: Load article content for optimization
- Read `content/workbench/{slug}/article.md` as the article content
- Read `content/workbench/{slug}/metadata.json` for existing meta title, meta description, and URL slug
- Use these as the basis for the full optimization audit below

**Note:** If the article is not found in the database, attempt `sync_article()` with the URL first. If that also fails, inform the user to run `/library sync` to populate the database.

When the input is a **local file path** (contains a file extension like `.md` or starts with a relative/absolute path like `content/drafts/`, `content/rewrites/`, `./`, `/`), proceed directly to the Content Audit using that file.

---

### Year Relevance Check

Before proceeding with the full audit, check if the article title, H1, meta title, or URL slug contains a year reference (e.g., "Best Tools in 2025", "Top 10 Solutions for 2024"). If the referenced year is **not the current year**, flag this as a **high-priority fix** and include a **"Year Refresh" section in the optimization report** that covers:

1. **Year references to update** — List every location where the outdated year appears (title, headings, meta title, meta description, URL slug, body text).
2. **Content likely outdated by the year change** — Scan the article for recommendations, tool/product lists, pricing, statistics, comparisons, rankings, and examples that are tied to the old year. Flag each item that likely needs verification or replacement (e.g., "Section 'Top 5 CI/CD Tools' — list may have new entrants or discontinued products since 2025").
3. **Guidance for `/rewrite`** — Provide specific, actionable notes so that a subsequent `/rewrite` pass knows exactly what substantive content to research and refresh beyond just swapping the year number.

This section should appear as a top-level item in the **Priority Fixes** list and be detailed enough that the rewrite can act on it without re-auditing the article.

---

### Content Audit

#### Keyword Analysis
- **Primary Keyword Density**: Check 1-2% density throughout article
- **Keyword Placement Check**:
  - [ ] In H1 headline
  - [ ] In first 100 words
  - [ ] In at least 2-3 H2 headings
  - [ ] In meta title
  - [ ] In meta description
  - [ ] In URL slug
- **Semantic Variations**: Verify related keywords are used naturally
- **Keyword Stuffing**: Ensure no over-optimization or unnatural usage
- **LSI Keywords**: Confirm latent semantic keywords are present

#### Heading Structure
- **H1**: Only one H1, includes primary keyword
- **H2s**: 4-7 H2 sections, at least 2-3 with keyword variations
- **H3s**: Proper nesting under H2s, descriptive and keyword-rich
- **Hierarchy**: Logical progression, no skipped levels (H1→H3)
- **Length**: Headings are descriptive but concise

#### Content Quality
- **Word Count**: Minimum 2000 words (2500-3000+ preferred)
- **Paragraph Length**: Average 2-4 sentences, no walls of text
- **Sentence Length**: Varied, averaging under 25 words
- **Readability Score**: 8th-10th grade level (Flesch-Kincaid)
- **Active Voice**: Predominantly active voice usage
- **Transition Words**: Smooth flow between sections
- **List Usage**: Bullets/numbers for scannability
- **Formatting**: Bold, italics used appropriately for emphasis

### Link Optimization

#### Internal Links (3-5+ required)
- **Quantity**: Count current internal links to your company content
- **Quality**: Verify links are contextually relevant
- **Anchor Text**: Check for keyword-rich, descriptive anchor text
- **Placement**: Natural integration within body content
- **Variety**: Links to different page types (pillar, blog, product, resources)
- **Reference**: Cross-check @context/internal-links-map.md for opportunities
- **Broken Links**: Verify all internal links work

**Recommendations**:
- Where to add additional internal links
- Better anchor text for existing links
- High-priority pages that should be linked

#### External Links (2-3+ required)
- **Quantity**: Count external authority links
- **Authority**: Verify links are to credible, authoritative sources
- **Relevance**: Ensure external links support content claims
- **Freshness**: Check that linked sources are current
- **Broken Links**: Test all external links
- **Link Attributes**: Verify appropriate use of nofollow where needed

**Recommendations**:
- Additional authoritative sources to link
- Outdated links to replace
- Statistics that need source citations

### Meta Element Optimization

#### Meta Title
- **Length**: 50-60 characters (check current length)
- **Keyword**: Primary keyword included naturally
- **Compelling**: Attention-grabbing and click-worthy
- **Brand**: Consider adding "| your company" if space allows
- **Uniqueness**: Distinct from other your company page titles

**Provide**:
- Current meta title analysis
- 3-5 optimized alternative options
- Recommended best choice

#### Meta Description
- **Length**: 150-160 characters (check current length)
- **Keyword**: Primary keyword included
- **Value Prop**: Clear benefit to reader
- **Call-to-Action**: Includes action phrase (learn, discover, find out)
- **Compelling**: Encourages click from SERP
- **Completeness**: Doesn't cut off mid-sentence

**Provide**:
- Current meta description analysis
- 3-5 optimized alternative options
- Recommended best choice

#### URL Slug
- **Length**: Concise but descriptive
- **Keyword**: Primary keyword included
- **Structure**: Lowercase, hyphens between words
- **Brevity**: Shorter is better (3-5 words ideal)
- **Clean**: No stop words (a, the, and) unless necessary

**Provide**:
- Current URL evaluation
- Alternative if improvement needed

### Technical SEO

#### Image Optimization
- **Alt Text**: Note where images need alt text with keywords
- **File Names**: Check that image file names are descriptive
- **Placement**: Images break up text appropriately
- **Relevance**: Images support content points

#### Featured Snippet Opportunity
- **Question Format**: Check if content answers specific question
- **List Format**: Identify list-based content for snippet optimization
- **Table Format**: Note if data could be formatted as table
- **Definition**: Check if concept could be featured snippet
- **Optimization**: Suggest how to structure for snippet capture

#### Schema Markup Suggestions
- **Article Schema**: Recommend article schema elements
- **FAQ Schema**: If Q&A format used
- **How-To Schema**: If step-by-step instructions included

### Brand & Voice

#### your company Alignment
- **Brand Voice**: Verify alignment with @context/brand-voice.md
- **Style Guide**: Check adherence to @context/style-guide.md
- **Messaging**: Ensure messaging reflects your company positioning
- **Product Mentions**: Natural integration of your company features
- **CTA**: Appropriate call-to-action for article intent

#### User Experience
- **Introduction**: Compelling hook that draws reader in
- **Value Delivery**: Article delivers on headline promise
- **Actionability**: Practical takeaways and next steps
- **Conclusion**: Strong summary and clear CTA
- **Scannability**: Easy to skim and find key information

## Output
Provides comprehensive optimization report:

### 1. SEO Score (0-100)
- **Keyword Optimization**: /25
- **Technical SEO**: /25
- **Content Quality**: /25
- **User Experience**: /25
- **Overall Score**: /100

### 2. Priority Fixes
List of critical issues to address before publishing:
- [ ] Fix 1 (High Priority)
- [ ] Fix 2 (High Priority)
- [ ] Fix 3 (Medium Priority)

### 3. Optimization Recommendations
**Quick Wins** (can be done in 5-10 minutes):
- Specific keyword placement adjustments
- Meta element tweaks
- Internal link additions

**Strategic Improvements** (more time investment):
- Content expansion opportunities
- Structural reorganization
- Additional research needed

### 4. Optimized Meta Options
**Meta Title Options** (pick one):
1. [Option 1] (58 chars)
2. [Option 2] (59 chars)
3. [Option 3] (60 chars)

**Meta Description Options** (pick one):
1. [Option 1] (157 chars)
2. [Option 2] (158 chars)
3. [Option 3] (160 chars)

### 5. Link Enhancement
**Internal Links to Add**:
- Link to [Page Name] in [Section Name] with anchor text "[suggested text]"
- Link to [Page Name] in [Section Name] with anchor text "[suggested text]"

**External Links to Add**:
- Add source for statistic in [Section Name]: [suggested source]
- Add authority link in [Section Name]: [suggested source]

### 6. Keyword Distribution Map
Visual representation of where primary keyword appears:
- H1: ✓
- First 100 words: ✓
- H2 sections: 2/5 (need 1-2 more)
- Body paragraphs: 15 instances (1.5% density) ✓
- Conclusion: ✓
- Meta title: ✓
- Meta description: ✓

### 7. Final Checklist
- [ ] Primary keyword in H1
- [ ] Primary keyword in first 100 words
- [ ] Primary keyword in 2+ H2 headings
- [ ] Keyword density 1-2%
- [ ] 3-5+ internal links included
- [ ] 2-3+ external authority links
- [ ] Meta title 50-60 characters
- [ ] Meta description 150-160 characters
- [ ] Article 2000+ words
- [ ] Proper H1/H2/H3 hierarchy
- [ ] Readability optimized (8th-10th grade)
- [ ] Images have alt text
- [ ] CTA included
- [ ] Brand voice maintained
- [ ] No broken links
- [ ] Ready to publish

### 8. Publishing Readiness
**Status**: Ready / Needs Minor Fixes / Needs Revision

**Estimated Time to Publishing**: [X minutes/hours]

**Next Steps**:
1. [Specific action needed]
2. [Specific action needed]
3. Move project folder to `/published/` when complete

## File Management
After optimization analysis, save report to the same project folder as the input file:

**For local file input:**
- **File Location**: `content/drafts/[YYQ#]-[topic-slug]/optimization-report.md` (or `content/rewrites/[YYQ#]-[topic-slug]/optimization-report.md`)
- **Naming Convention**: Save in the same folder as the article being optimized
- Example: `content/drafts/25Q4-podcast-analytics/optimization-report.md`

**For URL/slug input (content library):**
- **File Location**: `content/workbench/[slug]/optimization-report.md`
- **Naming Convention**: Save in the workbench folder alongside the checked-out article
- Example: `content/workbench/podcast-analytics-guide/optimization-report.md`

- **File Format**: Markdown with scores, checklists, and recommendations

## Integration with Agents
The `/optimize` command triggers final review from all agents:
- **content-analyzer** (NEW!): Comprehensive analysis with search intent, keyword density & clustering, content length comparison, readability score, and SEO quality rating (0-100)
- **seo-optimizer**: Technical SEO final check
- **meta-creator**: Best meta title/description options
- **internal-linker**: Last opportunity internal linking suggestions
- **keyword-mapper**: Final keyword distribution analysis

### New: Content Analyzer Module
The optimize command now includes advanced SEO analysis:
- **Search Intent**: Verify content matches user search intent (informational/commercial/transactional)
- **Keyword Density & Clustering**: Detailed density analysis, keyword stuffing detection, topic clustering
- **Content Length Comparison**: Compare word count against top 10 SERP competitors
- **Readability Score**: Flesch Reading Ease, Flesch-Kincaid Grade Level, sentence structure analysis
- **SEO Quality Rating**: Overall score (0-100) with category breakdowns and specific recommendations

## Publishing Decision
Based on optimization score:
- **90-100**: Excellent - publish immediately
- **80-89**: Good - minor tweaks recommended but publishable
- **70-79**: Fair - address priority fixes before publishing
- **Below 70**: Needs work - significant improvements required

This ensures every article meets your company quality standards and SEO best practices before going live.
