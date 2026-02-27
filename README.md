# Content Machine -- AI-Powered Content Creation Workspace

A Claude Code workspace that turns Claude into a full content team. Write SEO articles, LinkedIn posts, whitepapers, primers, sales decks, and web pages -- all in your brand voice.

## What It Does

Content Machine provides a complete set of commands and agents for every stage of content creation:

| Command | What it does |
|---------|-------------|
| `/research [topic]` | Keyword and competitive research, produces a research brief |
| `/write [topic]` | Write a full SEO article (2000-3000+ words) with auto-optimization |
| `/rewrite [slug]` | Refresh and update an existing article |
| `/optimize [file]` | Final SEO polish with publishing readiness score |
| `/analyze-existing [URL]` | Audit an existing article with content health score |
| `/linkedin` | Generate LinkedIn ideas from RSS, create posts, send to Slack |
| `/generate-images [file]` | Generate brand-compliant images with Google Gemini |
| `/performance-review` | Data-driven content prioritization using analytics |
| `/library` | Search and manage synced WordPress content |
| `/wordpress-edit` | Edit WordPress articles preserving Gutenberg blocks |
| `/slides` | Create branded Google Slides presentations |
| `/asset` | Create deep content (whitepapers, primers, decks, guides) |
| `/webpage` | Build production-quality web pages |

After writing, specialized agents automatically analyze the content: SEO Optimizer, Meta Creator, Internal Linker, Keyword Mapper, and Editor.

## Core Capabilities

**You don't need any integrations to start.** The core workflow produces local markdown files using just Claude Code and your brand context.

- **SEO Content**: Research, write, optimize, and publish long-form articles
- **LinkedIn**: Generate ideas from trending topics, create posts in company or CEO voice
- **Content Assets**: Whitepapers, primers, solution guides, sales decks via gated 3-phase process
- **Web Pages**: Build homepages, product pages, and use case pages
- **Content Analysis**: Search intent detection, keyword clustering, readability scoring, SEO quality rating
- **WordPress**: Import/export with full Gutenberg block preservation

## Integration Tiers

| Tier | Integration | What it enables | Required? |
|------|------------|----------------|-----------|
| Core | None | `/write`, `/research`, `/rewrite`, `/optimize`, `/linkedin` (local), `/asset` (local markdown) | No integrations needed |
| CMS | WordPress | `/library`, `/wordpress-edit`, publish to WordPress | Optional |
| Analytics | GA4, GSC, DataForSEO | `/performance-review` with real data | Optional (any/all) |
| Visual | Google Gemini API | `/generate-images` | Optional |
| Distribution | Slack | Send LinkedIn posts to Slack for review | Optional |
| Presentations | Google Slides + Apps Script | `/slides` command | Optional |
| Documents | Google Docs + Apps Script | Publish content to Google Docs | Optional |
| Image Hosting | HubSpot | Host images for Slack/web embeds | Optional |

## Getting Started

### Prerequisites
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Python 3.10+

### Quick Start

1. Clone this repository:
```bash
git clone https://github.com/[your-org]/content-machine.git
cd content-machine
```

2. Set up Python environment:
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

3. Configure your company:
```bash
cp data_sources/config/.env.example data_sources/config/.env
# Edit .env with at minimum: COMPANY_NAME, COMPANY_DOMAIN
```

4. Set up your brand context (see `context/` files)

5. Start Claude Code and write:
```bash
claude
# Then use: /write [your topic]
```

For detailed setup instructions, see **[ONBOARDING.md](ONBOARDING.md)**.

## Directory Structure

```
content-machine/
├── .claude/
│   ├── commands/          # Workflow commands (/write, /research, etc.)
│   └── agents/            # Specialized analysis agents
├── context/               # Brand voice, style guide, SEO guidelines
├── data_sources/
│   ├── modules/           # Python integration modules
│   └── config/            # API credentials (.env, not in git)
├── content/
│   ├── drafts/            # New article drafts
│   ├── rewrites/          # Article rewrites
│   ├── research/          # Research briefs
│   ├── topics/            # LinkedIn ideas and topic research
│   ├── published/         # Imported WordPress articles
│   ├── workbench/         # Temporary editing checkouts
│   ├── reviews/           # Content reviews
│   └── assets/            # Deep content projects (whitepapers, primers, decks)
├── asset-builder/         # Asset type templates and configuration
├── webpage-builder/       # Web page builder agents and templates
├── ONBOARDING.md          # Step-by-step setup guide
├── CLAUDE.md              # Claude Code configuration
└── requirements.txt       # Python dependencies
```

## Context Files

The quality of output depends on well-configured context files in `context/`:

| File | Purpose | Priority |
|------|---------|----------|
| `brand-voice.md` | Voice pillars, tone, messaging framework | High |
| `writing-examples.md` | 3-5 exemplary blog posts from your site | High |
| `internal-links-map.md` | Key pages for internal linking strategy | High |
| `features.md` | Product/service features and benefits | High |
| `style-guide.md` | Editorial standards and formatting | Medium |
| `target-keywords.md` | Keyword research by topic cluster | Medium |
| `competitor-analysis.md` | Competitive intelligence | Medium |
| `seo-guidelines.md` | SEO requirements (pre-filled with best practices) | Review |
| `visual-guidelines.md` | Brand colors and visual style for images | Medium |
| `ceo-voice.md` | CEO personal voice for LinkedIn posts | Medium |

## Workflows

### New Article
```
/research [topic]    # Research brief with keywords and competitor analysis
/write [topic]       # Full article with auto-optimization agents
/optimize [file]     # Final SEO polish
```

### Update Existing Content
```
/analyze-existing [URL]   # Content health score and recommendations
/rewrite [topic]          # Refreshed article with change summary
```

### LinkedIn
```
/linkedin ideas           # Generate ideas from RSS feeds
/linkedin post [file]     # Create post, generate image, send to Slack
```

### Deep Content Assets
```
/asset new whitepaper     # 3-phase gated process with human checkpoints
/asset continue           # Resume an in-progress asset
```

## License

[Add your license information]

## Credits

Built with [Claude Code](https://docs.anthropic.com/en/docs/claude-code) by Anthropic.
