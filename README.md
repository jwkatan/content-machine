# SEO Machine

A specialized Claude Code workspace for creating long-form, SEO-optimized blog content for any business. This system helps you research, write, analyze, and optimize content that ranks well and serves your target audience.

## Overview

SEO Machine is built on Claude Code and provides:
- **Custom Commands**: `/research`, `/write`, `/rewrite`, `/analyze-existing`, `/optimize`, `/performance-review`, `/generate-images`, `/linkedin`, `/wordpress-edit`, `/library`
- **Specialized Agents**: Content analyzer, SEO optimization, meta element creation, internal linking, keyword mapping, editor, performance analysis, LinkedIn repurposing, newsletter repurposing
- **LinkedIn Workflow**: Generate ideas from RSS feeds, create posts with appropriate voice (company vs CEO), send to Slack for review
- **Advanced SEO Analysis**: Search intent detection, keyword density & clustering, content length comparison, readability scoring, SEO quality rating (0-100)
- **Data Integrations**: Google Analytics 4, Google Search Console, DataForSEO for real-time performance insights
- **Context-Driven**: Brand voice, style guide, SEO guidelines, and examples guide all content
- **Workflow Organization**: Structured directories for topics, research, drafts, and published content

## Getting Started

### Prerequisites
- [Claude Code](https://claude.com/claude-code) installed
- Anthropic API account

### Installation

1. Clone this repository:
```bash
git clone https://github.com/[your-username]/seomachine.git
cd seomachine
```

2. Install Python dependencies for analysis modules:
```bash
pip install -r data_sources/requirements.txt
```

This installs:
- Google Analytics/Search Console integrations
- DataForSEO API client
- NLP libraries (nltk, textstat)
- Machine learning (scikit-learn)
- Web scraping tools (beautifulsoup4)
- Google GenAI SDK (for image generation)

3. Open in Claude Code:
```bash
claude-code .
```

4. **Customize Context Files** (Important!):

   All context files are provided as templates. Fill them out with your company's information:

   - `context/brand-voice.md` - Define your brand voice and messaging *(see examples/castos/ for reference)*
   - `context/writing-examples.md` - Add 3-5 exemplary blog posts from your site
   - `context/features.md` - List your product/service features and benefits
   - `context/internal-links-map.md` - Map your key pages for internal linking
   - `context/style-guide.md` - Fill in your style preferences
   - `context/target-keywords.md` - Add your keyword research and topic clusters
   - `context/competitor-analysis.md` - Add competitor analysis and insights
   - `context/seo-guidelines.md` - Review and adjust SEO requirements
   - `context/visual-guidelines.md` - Define brand colors and visual style for image generation
   - `context/ceo-voice.md` - Add CEO writing samples for personal LinkedIn posts

   **Quick Start**: Check out `examples/castos/` to see a complete real-world example of all context files filled out for a podcast hosting SaaS company.

5. **For LinkedIn Workflow** (optional):

   Set up Slack webhook for post notifications:
   ```bash
   # Add to .env file
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ
   ```

   Install RSS dependencies:
   ```bash
   pip install feedparser python-dateutil
   ```

## Workflows

### Creating New Content

#### 1. Start with Research
```
/research [topic]
```

**What it does**:
- Performs keyword research
- Analyzes top 10 competitors
- Identifies content gaps
- Creates comprehensive research brief
- Saves to `/research/` directory

**Example**:
```
/research content marketing strategies for B2B SaaS
```

#### 2. Write the Article
```
/write [topic or research brief]
```

**What it does**:
- Creates 2000-3000+ word SEO-optimized article
- Maintains your brand voice from `context/brand-voice.md`
- Integrates keywords naturally
- Includes internal and external links
- Provides meta elements (title, description, keywords)
- Automatically triggers optimization agents
- Saves to `/drafts/` directory

**Example**:
```
/write content marketing strategies for B2B SaaS
```

**Agent Auto-Execution**:
After writing, these agents automatically analyze the content:
- **SEO Optimizer**: On-page SEO recommendations
- **Meta Creator**: Multiple meta title/description options
- **Internal Linker**: Specific internal linking suggestions
- **Keyword Mapper**: Keyword placement and density analysis

#### 3. Final Optimization
```
/optimize [article file]
```

**What it does**:
- Comprehensive SEO audit
- Validates all elements meet requirements
- Provides final polish recommendations
- Generates publishing readiness score
- Creates optimization report

**Example**:
```
/optimize content/drafts/25Q4-content-marketing-strategies/article-2025-10-29.md
```

### Updating Existing Content

#### 1. Analyze Existing Post
```
/analyze-existing [URL or file path]
```

**What it does**:
- Fetches and analyzes current content
- Evaluates SEO performance
- Identifies outdated information
- Assesses competitive positioning
- Provides content health score (0-100)
- Recommends update priority and scope
- Saves analysis to `/research/` directory

**Examples**:
```
/analyze-existing https://yoursite.com/blog/marketing-guide
/analyze-existing published/24Q1-marketing-guide/article-2024-01-15.md
```

#### 2. Rewrite/Update Content
```
/rewrite [topic or analysis file]
```

**What it does**:
- Updates content based on analysis findings
- Refreshes statistics and examples
- Improves SEO optimization
- Adds new sections to fill gaps
- Maintains what works from original
- Tracks changes made
- Saves to `/rewrites/` directory

**Example**:
```
/rewrite marketing guide
```

### LinkedIn Content Workflow

Create standalone LinkedIn posts from ideas, trending topics, or existing content.

#### 1. Generate Ideas from Trending Topics
```
/linkedin ideas
```

**What it does**:
- Fetches from RSS feeds (Hacker News, TechCrunch, InfoQ)
- Filters for topics relevant to your audience
- Selects 5 most interesting for LinkedIn
- Creates idea files in `/topics/linkedin/ideas/`

**Example from URL**:
```
/linkedin ideas "https://news.ycombinator.com/item?id=12345"
```

#### 2. Create Post from Idea
```
/linkedin post [idea-file]
```

**What it does**:
- Reads idea and determines voice (company vs CEO)
- Loads appropriate voice context
- Generates optimized LinkedIn post
- Creates image (AI illustration for company, quote card for CEO)
- Scrubs AI watermarks
- Sends directly to Slack for CEO review

**Example**:
```
/linkedin post topics/linkedin/ideas/ai-coding-trends-2026-01-29.md
```

#### 3. Track Results
After CEO reviews in Slack:
- **Used it**: Move file to `content/topics/linkedin/published/`
- **Didn't use**: Move file to `content/topics/linkedin/discarded/`

**Voice Modes**:
- **Company posts**: Use `brand-voice.md` - formal, brand-focused
- **CEO posts**: Use `ceo-voice.md` - personal, conversational, authentic

### WordPress Content Workflow

Import, edit, and export content to/from WordPress while preserving Gutenberg block structure.

#### 1. Import from WordPress
```python
from data_sources.modules.wordpress_client import import_from_wordpress

success, folder = import_from_wordpress("https://yoursite.com/blog/article-slug/")
# Creates: published/{slug}/original.html, article.md, metadata.json
```

#### 2. Edit Content
```
/wordpress-edit
```

Use this skill when editing `original.html`. It teaches Claude how to:
- Preserve Gutenberg block structure (`<!-- wp:paragraph -->`, etc.)
- Add, update, or delete blocks correctly
- Handle nested blocks (lists with list-items)

After edits, regenerate the markdown for review:
```python
from data_sources.modules.wordpress_client import regenerate_markdown
regenerate_markdown('content/published/{slug}/')
```

#### 3. Export to WordPress
```python
from data_sources.modules.wordpress_client import export_to_wordpress

# Preview (no actual push)
export_to_wordpress('content/published/{slug}/')

# Actually push to draft
export_to_wordpress('content/published/{slug}/', push=True)
```

**Important**:
- All exports go to **draft** status (never auto-publish)
- Use `original.html` for perfect block round-trip
- Block registry available at `context/wordpress-blocks.json`

## Commands Reference

### `/research [topic]`
Comprehensive keyword and competitive research for new content.

**Output**: Research brief in `/research/brief-[topic]-[date].md`

**Includes**:
- Primary and secondary keywords
- Competitor analysis (top 10)
- Content gaps and opportunities
- Recommended outline
- Internal linking strategy
- Meta elements preview

---

### `/write [topic]`
Create long-form SEO-optimized article (2000-3000+ words).

**Output**: Article in `/drafts/[YYQ#]-[topic-slug]/article-[date].md` (with all reports in same folder)

**Includes**:
- Complete article with H1/H2/H3 structure
- SEO-optimized content
- Internal and external links
- Meta elements (title, description, keywords)
- SEO checklist

**Auto-Triggers**:
- SEO Optimizer agent
- Meta Creator agent
- Internal Linker agent
- Keyword Mapper agent

---

### `/rewrite [topic]`
Update and improve existing content.

**Output**: Updated article in `/rewrites/[YYQ#]-[topic-slug]/article-[date].md` (with change summary in same folder)

**Includes**:
- Rewritten/updated content
- Change summary
- Before/after comparison
- Updated SEO elements

---

### `/analyze-existing [URL or file]`
Analyze existing blog posts for improvement opportunities.

**Output**: Analysis report in `/research/analysis-[topic]-[date].md`

**Includes**:
- Content health score (0-100)
- Quick wins (immediate improvements)
- Strategic improvements
- Rewrite priority and scope
- Research brief for rewrite

---

### `/optimize [file]`
Final SEO optimization pass before publishing.

**Output**: Optimization report in the same folder as the input file (e.g., `/drafts/[YYQ#]-[topic-slug]/optimization-report.md`)

**Includes**:
- SEO score (0-100)
- Priority fixes
- Quick wins
- Meta element options
- Link enhancement suggestions
- Publishing readiness assessment

---

### `/generate-images [article file]`
Generate brand-compliant images for blog articles and social media.

**Output**: Images in `/drafts/[YYQ#]-[topic-slug]/images/`

**Generates**:
- Banner image (1920x960) for blog hero
- LinkedIn image (1080x1080 square) for social sharing
- Metadata file with prompts and alt text

**Workflow**:
1. Proposes image concepts based on article content
2. Waits for user approval before generating
3. Generates images using Google Gemini (Nano Banana)
4. Allows regeneration with feedback if needed

**Requires**:
- Google AI API key (set `GOOGLE_API_KEY` in `.env`)
- Billing enabled on Google AI Studio for image generation
- `context/visual-guidelines.md` configured with brand colors

---

### `/linkedin [subcommand]`
Manage LinkedIn content workflow: generate ideas, create posts, send to Slack.

**Subcommands**:

**Dashboard (no args)**:
```
/linkedin
```
Shows pending ideas, quick actions, and recent posts.

**Generate Ideas from RSS**:
```
/linkedin ideas
```
Fetches trending topics, selects 5 most relevant, creates idea files.

**Generate Idea from URL/Summary**:
```
/linkedin ideas "https://example.com/article"
/linkedin ideas "Summary: AI coding assistants are changing..."
```
Creates single idea file from external content.

**Create Post**:
```
/linkedin post topics/linkedin/ideas/[filename].md
```
Generates post, image, scrubs AI watermarks, sends to Slack.

**Output**: Updated idea file with post content in `content/topics/linkedin/ideas/`

**Voice Selection**:
- `type: company` - Loads `brand-voice.md` only
- `type: ceo` - Loads `ceo-voice.md` only

**Image Generation**:
- Company posts: AI vector illustrations (brand-compliant)
- CEO posts: Simple quote cards or no image (authentic feel)

**Requires**:
- `SLACK_WEBHOOK_URL` in `.env` for Slack notifications
- `context/ceo-voice.md` configured with CEO writing samples

## Agents

Specialized agents that automatically analyze content and provide expert recommendations.

### Content Analyzer (NEW!)
**Purpose**: Comprehensive, data-driven content analysis using 5 specialized modules

**Analyzes**:
- Search intent classification (informational/navigational/transactional/commercial)
- Keyword density and clustering with topic detection
- Content length comparison vs top SERP competitors
- Readability scoring (Flesch Reading Ease, Flesch-Kincaid Grade Level)
- SEO quality rating (0-100 score with category breakdowns)
- Keyword stuffing risk detection
- Passive voice ratio and sentence complexity
- Distribution heatmap showing keyword placement by section

**Output**:
- Executive summary with publishing readiness assessment
- Priority action plan (critical/high priority/optimization)
- Competitive positioning analysis
- Detailed recommendations for each analysis area
- Exact metrics and benchmarks for improvements

**Powered by**:
- `search_intent_analyzer.py` - Search intent detection
- `keyword_analyzer.py` - Keyword density, clustering, LSI keywords
- `content_length_comparator.py` - SERP competitor analysis
- `readability_scorer.py` - Multiple readability metrics
- `seo_quality_rater.py` - Comprehensive SEO scoring

---

### SEO Optimizer
**Purpose**: On-page SEO analysis and optimization recommendations

**Analyzes**:
- Keyword optimization and density
- Content structure and headings
- Internal and external links
- Meta elements
- Readability and user experience
- Featured snippet opportunities

**Output**: SEO score (0-100) with specific improvement recommendations

---

### Meta Creator
**Purpose**: Generate high-converting meta titles and descriptions

**Creates**:
- 5 meta title variations (50-60 chars)
- 5 meta description variations (150-160 chars)
- Testing recommendations
- SERP preview
- Conversion-optimized copy

**Output**: Multiple options with recommendation and reasoning

---

### Internal Linker
**Purpose**: Strategic internal linking recommendations

**Provides**:
- 3-5 specific internal link suggestions
- Exact placement locations
- Anchor text recommendations
- User journey mapping
- SEO impact prediction

**References**: `context/internal-links-map.md`

---

### Keyword Mapper
**Purpose**: Keyword placement and integration analysis

**Analyzes**:
- Keyword density and distribution
- Critical placement checklist
- Natural language integration quality
- LSI keyword coverage
- Cannibalization risk

**Output**: Distribution map, gap analysis, specific revision suggestions

---

### Editor
**Purpose**: Transform technically accurate content into human-sounding, engaging articles

**Analyzes**:
- Voice and personality
- Specificity of examples
- Readability and flow
- Robotic vs. human patterns
- Engagement and storytelling

**Provides**:
- Humanity score (0-100)
- Critical edits with before/after
- Pattern analysis
- Specific rewrites to inject personality
- Readability improvements

**Output**: Editorial report with specific improvements to make content sound human

---

### Performance
**Purpose**: Data-driven content prioritization using real analytics

**Analyzes**:
- Google Analytics traffic and trends
- Google Search Console rankings and CTR
- DataForSEO competitive data
- Quick wins (position 11-20)
- Declining content
- Low CTR opportunities
- Trending topics

**Provides**:
- Priority queue of content tasks
- Opportunity scores (0-100)
- Impact and effort estimates
- Week-by-week roadmap
- Success metrics

**Output**: Comprehensive performance report with actionable priorities

---

### LinkedIn Repurposer
**Purpose**: Transform blog content into engaging LinkedIn posts for professional audiences

**Process**:
- Extracts core business insights from source content
- Identifies data points, statistics, and human stories
- Applies proven LinkedIn hook frameworks (counterintuitive truth, transformation story, industry secret, mistake confession, data revelation)
- Optimizes for LinkedIn algorithm and mobile reading

**Creates**:
- Scroll-stopping hooks (first 2 lines)
- Value-driven post structure with clear paragraphs
- Authority indicators and vulnerability elements
- Engagement-driving questions and CTAs
- Mobile-optimized formatting

**Quality Standards**:
- 900-1,300 characters for optimal engagement
- 8-10 seconds dwell time optimization
- Professional tone with personal authenticity
- No engagement bait or growth hacking

**Output**: Complete LinkedIn post with performance metrics to track

---

### Newsletter Repurposer
**Purpose**: Adapt content for email newsletter engagement and subscriber retention

**Process**:
- Extracts the single most valuable insight from articles
- Maps subscriber mindset and reading context
- Applies inbox psychology principles
- Optimizes for deliverability and mobile reading

**Creates**:
- Subject lines (30-50 characters) using proven frameworks
- Preview text (35-90 characters) that complements subject
- Opening hooks with personal connection
- Core value sections using What/Why/How framework
- Clear CTAs (reply requests, forward prompts, clicks)
- Personal sign-offs

**Quality Standards**:
- Under 2 minutes reading time
- Mobile-first formatting (35-50 character lines)
- No spam trigger words
- Single, clear call-to-action
- Personal feel at scale

**Output**: Complete email with subject line, preview text, body, technical specs, engagement strategy, and optional A/B test variants

## Data Sources

### Integration with Analytics

SEO Machine integrates with real-time data sources to inform content strategy:

**Google Analytics 4**:
- Traffic and engagement metrics
- Conversion tracking
- Trend analysis
- Traffic sources

**Google Search Console**:
- Keyword rankings and positions
- Impressions and clicks
- CTR analysis
- Query performance

**DataForSEO**:
- Competitive rankings
- SERP features
- Keyword metrics
- Competitor gap analysis

### Advanced SEO Analysis Modules (NEW!)

SEO Machine includes 5 specialized Python modules for comprehensive content analysis:

**Search Intent Analyzer** (`search_intent_analyzer.py`):
- Classifies queries into informational, navigational, transactional, or commercial intent
- Analyzes SERP features and content patterns
- Provides confidence scores and content alignment recommendations

**Keyword Analyzer** (`keyword_analyzer.py`):
- Calculates exact keyword density and distribution
- Detects keyword stuffing risk with warnings
- Performs topic clustering using TF-IDF and K-means
- Generates distribution heatmap by section
- Identifies LSI (semantically related) keywords

**SEO Quality Rater** (`seo_quality_rater.py`):
- Rates content against SEO best practices (0-100 score)
- Category breakdowns: content, keywords, meta, structure, links, readability
- Identifies critical issues, warnings, and suggestions
- Determines publishing readiness

**Content Length Comparator** (`content_length_comparator.py`):
- Fetches and analyzes top 10-20 SERP competitor word counts
- Calculates median, 75th percentile, and optimal length
- Shows competitive positioning and gap to target
- Provides data-driven expansion recommendations

**Readability Scorer** (`readability_scorer.py`):
- Flesch Reading Ease and Flesch-Kincaid Grade Level
- Sentence and paragraph structure analysis
- Passive voice detection and ratio calculation
- Complex word identification
- Transition word usage analysis
- Overall readability score (0-100)

All modules can be used directly in Python or through the Content Analyzer agent.

### LinkedIn Workflow Modules (NEW!)

**RSS Aggregator** (`rss_aggregator.py`):
- Fetches from Hacker News, TechCrunch, InfoQ RSS feeds
- Filters by relevance keywords (legacy, AI coding, developer productivity, etc.)
- Scores and ranks articles by Swimm relevance
- Creates structured idea files

**Slack Notifier** (`slack_notifier.py`):
- Sends LinkedIn posts to Slack via incoming webhooks
- Formatted messages with post content and images
- No OAuth required - simple webhook setup

**Content Scrubber** (`content_scrubber.py`):
- Removes AI watermarks (zero-width spaces, format-control characters)
- Replaces em-dashes with contextually appropriate punctuation
- Ensures content appears naturally human-written

See `data_sources/README.md` for setup instructions.

## Directory Structure

```
seomachine/
├── .claude/
│   ├── commands/          # Custom workflow commands
│   │   ├── analyze-existing.md
│   │   ├── research.md
│   │   ├── write.md
│   │   ├── rewrite.md
│   │   ├── optimize.md
│   │   ├── performance-review.md
│   │   ├── generate-images.md
│   │   └── linkedin.md           # LinkedIn content workflow (NEW!)
│   └── agents/            # Specialized analysis agents
│       ├── content-analyzer.md    # Comprehensive analysis
│       ├── seo-optimizer.md
│       ├── meta-creator.md
│       ├── internal-linker.md
│       ├── keyword-mapper.md
│       ├── editor.md
│       ├── performance.md
│       ├── linkedin-repurposer.md # Content to LinkedIn posts
│       └── newsletter-repurposer.md # Content to email newsletters
├── data_sources/          # Analytics integrations
│   ├── modules/          # Python integration modules
│   │   ├── google_analytics.py
│   │   ├── google_search_console.py
│   │   ├── dataforseo.py
│   │   ├── data_aggregator.py
│   │   ├── search_intent_analyzer.py    # NEW!
│   │   ├── keyword_analyzer.py          # NEW!
│   │   ├── seo_quality_rater.py         # NEW!
│   │   ├── content_length_comparator.py # NEW!
│   │   ├── readability_scorer.py        # NEW!
│   │   ├── rss_aggregator.py            # LinkedIn: RSS feed fetching
│   │   ├── slack_notifier.py            # LinkedIn: Slack webhooks
│   │   └── content_scrubber.py          # AI watermark removal
│   ├── config/           # API credentials (not in git)
│   ├── utils/            # Helper functions
│   ├── cache/            # Cached API responses
│   └── README.md         # Setup instructions
├── context/               # Configuration and guidelines
│   ├── brand-voice.md          # Your brand voice and messaging (template)
│   ├── ceo-voice.md            # CEO personal voice for LinkedIn (NEW!)
│   ├── writing-examples.md     # Example blog posts
│   ├── style-guide.md          # Writing style conventions
│   ├── seo-guidelines.md       # SEO requirements
│   ├── target-keywords.md      # Keyword research and clusters
│   ├── internal-links-map.md   # Key pages for internal linking
│   └── competitor-analysis.md  # Competitive intelligence
├── content/topics/                # Raw topic ideas
│   ├── New/              # SEO article ideas
│   ├── Old/              # Completed/archived ideas
│   └── linkedin/         # LinkedIn content workflow
│       ├── ideas/        # Generated ideas waiting to be used
│       ├── content/published/    # CEO used the post
│       └── discarded/    # CEO didn't use the post
├── content/research/              # Research briefs and analysis reports
├── content/drafts/                # Work in progress articles (organized by quarter)
│   └── [YYQ#]-[topic-slug]/  # Quarter prefix groups by time (e.g., 26Q1-marketing)
│       ├── article-[date].md
│       ├── seo-report.md
│       ├── meta-options.md
│       ├── keyword-analysis.md
│       └── link-suggestions.md
├── content/published/             # Final versions ready to publish
│   └── [YYQ#]-[topic-slug]/  # Each published article in its own folder
│       └── article-[date].md
├── content/rewrites/              # Updated existing content
│   └── [YYQ#]-[topic-slug]/  # Each rewrite project in its own folder
│       ├── article-[date].md
│       └── changes-[date].md
└── README.md              # This file
```

## Context Files (Important!)

The quality of your content depends on well-configured context files:

### `context/brand-voice.md`
Defines your brand voice, tone, and messaging framework.

**Must include**:
- Voice pillars
- Tone guidelines by content type
- Core brand messages
- Writing style guidelines
- Terminology preferences

**Purpose**: Ensures all content sounds like your brand

---

### `context/ceo-voice.md` (NEW!)
Personal voice profile for CEO LinkedIn posts. Separate from brand voice to prevent blending.

**Must include**:
- Voice characteristics (personal authority, authenticity)
- Background and expertise areas
- 3-5 actual LinkedIn posts as writing samples
- Signature phrases and patterns
- Topics of authority
- What to avoid

**Purpose**: Ensures CEO posts feel personal and authentic, not corporate

**Note**: Fill in the template with actual CEO writing samples - these are critical for voice matching.

---

### `context/writing-examples.md`
Contains 3-5 exemplary blog posts from your site.

**Must include**:
- Full article content
- What makes each example great
- Key takeaways for voice and structure

**Purpose**: Teaches AI your specific writing style through examples

---

### `context/style-guide.md`
Editorial and formatting standards.

**Must include**:
- Grammar and mechanics rules
- Capitalization conventions
- Formatting standards
- Preferred terminology

**Purpose**: Maintains consistency across all content

---

### `context/seo-guidelines.md`
SEO best practices and requirements.

**Includes**:
- Content length requirements
- Keyword optimization rules
- Meta element standards
- Link strategy guidelines
- Readability requirements

**Purpose**: Ensures all content meets SEO standards

---

### `context/target-keywords.md`
Keyword research organized by topic cluster.

**Must include**:
- Pillar keywords by cluster
- Cluster keywords (subtopics)
- Long-tail variations
- Search intent classification
- Current rankings

**Purpose**: Guides keyword targeting for new content

---

### `context/internal-links-map.md`
Catalog of key pages from your site for internal linking.

**Must include**:
- Product pages and features
- Pillar content URLs
- Top performing blog articles
- Topic cluster mapping
- Recommended anchor text

**Purpose**: Enables strategic internal linking in every article

---

### `context/competitor-analysis.md`
Competitive intelligence and content gaps.

**Must include**:
- Primary competitors
- Their content strategies
- Keyword gaps
- Differentiation opportunities

**Purpose**: Informs content strategy and competitive positioning

## Content Quality Standards

Every article must meet these requirements:

### Content
- [ ] Minimum 2,000 words (2,500-3,000+ preferred)
- [ ] Provides unique value vs. competitors
- [ ] Factually accurate and current
- [ ] Actionable advice for your target audience
- [ ] Brand voice maintained

### SEO
- [ ] Primary keyword density 1-2%
- [ ] Keyword in H1, first 100 words, 2-3 H2s
- [ ] 3-5 internal links with descriptive anchor text
- [ ] 2-3 external authority links
- [ ] Meta title 50-60 characters
- [ ] Meta description 150-160 characters
- [ ] Proper H1>H2>H3 hierarchy

### Readability
- [ ] 8th-10th grade reading level
- [ ] Average sentence length 15-20 words
- [ ] Paragraphs 2-4 sentences
- [ ] Subheadings every 300-400 words
- [ ] Lists and formatting for scannability

### Structure
- [ ] Compelling introduction (hook, problem, promise)
- [ ] Logical section flow
- [ ] Clear conclusion with CTA
- [ ] Examples and data included

## Best Practices

### Before Writing
1. **Research first**: Always run `/research` before `/write`
2. **Review context**: Read `brand-voice.md` and relevant `writing-examples.md`
3. **Check keywords**: Verify target keyword in `target-keywords.md`
4. **Plan internal links**: Review `internal-links-map.md` for linking opportunities

### During Writing
1. **Follow the brief**: Use research brief as your outline
2. **Natural keywords**: Integrate keywords naturally, never force them
3. **Add value**: Every section should provide actionable insights
4. **Use examples**: Include real podcast scenarios and use cases
5. **Cite sources**: Link to statistics and data sources

### After Writing
1. **Review agent output**: Read all agent recommendations carefully
2. **Make improvements**: Address high-priority issues before optimizing
3. **Run optimize**: Use `/optimize` for final polish
4. **Self-edit**: Read article as if you're the target reader
5. **Check quality**: Verify all checklist items met

### For Rewrites
1. **Analyze first**: Run `/analyze-existing` to understand scope
2. **Determine strategy**: Light update vs. major rewrite?
3. **Preserve what works**: Keep effective sections
4. **Focus on gaps**: Add what's missing from competitive content
5. **Update everything**: Stats, examples, screenshots, links

## Workflow Examples

### Example 1: Creating New Content from Scratch

```
# Step 1: Add topic idea
# Create file in topics/ directory with initial thoughts

# Step 2: Research the topic
/research podcast advertising strategies

# Step 3: Review research brief
# Read research/brief-podcast-advertising-strategies-2025-10-15.md

# Step 4: Write article
/write podcast advertising strategies

# Step 5: Review agent feedback
# Read all agent reports in drafts/25Q4-podcast-advertising-strategies/

# Step 6: Make improvements
# Edit article based on agent recommendations

# Step 7: Final optimization
/optimize content/drafts/25Q4-podcast-advertising-strategies/article-2025-10-15.md

# Step 8: Final review and move to published/
# Manual review, then move folder to published/ when ready
```

### Example 2: Updating Existing Content

```
# Step 1: Analyze existing post
/analyze-existing https://yoursite.com/blog/product-comparison

# Step 2: Review analysis
# Read research/analysis-product-comparison-2025-10-29.md
# Check content health score and priority level

# Step 3: Rewrite content
/rewrite product comparison

# Step 4: Review changes
# Read rewrites/25Q4-product-comparison/article-2025-10-29.md
# Review change summary in rewrites/25Q4-product-comparison/changes-2025-10-29.md

# Step 5: Optimize
/optimize rewrites/25Q4-product-comparison/article-2025-10-29.md

# Step 6: Publish
# Move folder to published/ when ready
```

### Example 3: Quick Content Audit

```
# Analyze multiple existing posts to prioritize updates
/analyze-existing https://yoursite.com/blog/post-1
/analyze-existing https://yoursite.com/blog/post-2
/analyze-existing https://yoursite.com/blog/post-3

# Review content health scores
# Prioritize rewrites based on:
# - Lowest scores
# - Highest traffic potential
# - Strategic importance
```

## Tips & Tricks

### Maximizing Content Quality
- **Study examples**: Read your `writing-examples.md` before each writing session
- **Use data**: Always include current statistics and cite sources
- **Be specific**: "40% increase" beats "significant improvement"
- **Show, don't tell**: Use real podcast examples and scenarios
- **Answer questions**: Address "People Also Ask" questions from research

### SEO Optimization
- **Keywords early**: Get primary keyword in first 100 words
- **Natural integration**: Read content aloud - if keywords sound forced, rewrite
- **Vary anchor text**: Don't use same anchor text for all internal links
- **Link strategically**: Link to pillar content and related cluster articles
- **Update regularly**: Refresh top-performing content every 6-12 months

### Workflow Efficiency
- **Batch research**: Research multiple topics in one session
- **Follow structure**: Use consistent article structure from `/write` command
- **Address high-priority first**: Fix critical issues before optimizing details
- **Use agents wisely**: Let agents handle analysis, you focus on writing
- **Build templates**: Save commonly used sections for reuse

### Avoiding Common Mistakes
- ❌ Skipping research phase
- ❌ Ignoring brand voice guidelines
- ❌ Forcing keywords unnaturally
- ❌ Forgetting internal links
- ❌ Not citing data sources
- ❌ Publishing without optimization
- ❌ Copying competitor content instead of differentiating

## Maintenance

### Weekly
- Add new topic ideas to `/topics/`
- Update `target-keywords.md` with new keyword opportunities
- Check for broken links in `internal-links-map.md`

### Monthly
- Review published content performance
- Update `writing-examples.md` if better examples emerge
- Add newly published content to `internal-links-map.md`
- Track competitor activity in `competitor-analysis.md`

### Quarterly
- Full audit of context files
- Update SEO guidelines based on algorithm changes
- Comprehensive competitor analysis refresh
- Review and update topic clusters in `target-keywords.md`

## Troubleshooting

### "Content doesn't sound like my brand"
- **Solution**: Update `context/brand-voice.md` with more specific guidance
- **Solution**: Add more diverse examples to `context/writing-examples.md`
- **Solution**: Reference specific examples when using `/write` command

### "Keyword density too high/low"
- **Solution**: Review `seo-guidelines.md` target density (1-2%)
- **Solution**: Use `/optimize` to get specific keyword placement suggestions
- **Solution**: Use Keyword Mapper agent for distribution analysis

### "Internal links aren't relevant"
- **Solution**: Update `context/internal-links-map.md` with current pages
- **Solution**: Organize by topic cluster for easier agent matching
- **Solution**: Provide more context about what each page covers

### "Articles too similar to competitors"
- **Solution**: Update `competitor-analysis.md` with differentiation opportunities
- **Solution**: Add your unique advantages to `brand-voice.md` and `features.md`
- **Solution**: Reference specific differentiation angles in `/research` command

## Support & Contributions

### Getting Help
- Review this README thoroughly
- Check context files are properly configured
- Consult [Claude Code documentation](https://docs.claude.com/claude-code)

### Contributing
- Report issues via GitHub Issues
- Suggest improvements to commands or agents
- Share successful workflows or tips

## License

[Add your license information]

## Credits

Built with [Claude Code](https://claude.com/claude-code) by Anthropic.

Originally developed for Castos, now available as an open-source tool for any business to streamline long-form SEO content creation.

## Examples & Community

**See It In Action**: Check out `examples/castos/` for a complete real-world example of how a podcast hosting SaaS company uses SEO Machine.

**Contributions Welcome**: Found a bug? Have a feature request? Want to share your own industry example? Contributions and PRs are welcome!

---

**Ready to start creating?**

1. Configure your context files (use the templates as your guide)
2. Run `/research [your topic]`
3. Review the brief
4. Run `/write [your topic]`
5. Publish amazing content!

Happy writing! 📝
