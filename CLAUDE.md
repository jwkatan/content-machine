# Content Machine - Claude Code Configuration

## Python Environment

**Always use the project's virtual environment for Python commands:**

```bash
.venv/bin/python    # Use this instead of python3
.venv/bin/pip       # Use this instead of pip3
```

The venv has all required dependencies installed:
- python-dotenv
- google-genai
- feedparser
- requests

## Key Directories

- `data_sources/config/.env` - Environment variables (API keys, webhooks)
- `data_sources/modules/` - Python modules for data fetching and processing
- `context/` - Voice and brand guidelines
- `context/wordpress-blocks.json` - WordPress Gutenberg block registry
- `data_sources/db/` - Content library databases (queryable mirror of WordPress, gitignored)
- `docs/` - Project documentation (CHANGELOG, CONTRIBUTING, setup guides, etc.)
- `content/` - All writing workflow directories:
  - `content/drafts/` - New article drafts
  - `content/rewrites/` - Article rewrites
  - `content/research/` - Research briefs
  - `content/topics/` - LinkedIn ideas and topic research
  - `content/published/` - Legacy imported WordPress articles
  - `content/workbench/` - Temporary checkout for articles being edited (gitignored)
  - `content/reviews/` - Content reviews (gitignored)
  - `content/assets/` - Deep content projects: whitepapers, primers, decks, guides (gitignored)
- `asset-builder/` - Asset type templates and configuration for `/asset` command
  - `asset-builder/asset-types/` - Per-type templates (whitepaper, primer, sales-deck, etc.)
  - `asset-builder/templates/` - Shared templates (decisions-template.md)

## WordPress Configuration

Environment variables in `data_sources/config/.env`:

```bash
WORDPRESS_SITE_URL=https://yoursite.com
WORDPRESS_USERNAME=your-username
WORDPRESS_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx

## Common Commands

```bash
# Generate image
.venv/bin/python -c "from data_sources.modules.image_generator import generate_image; ..."

# Send to Slack
.venv/bin/python -c "from data_sources.modules.slack_notifier import send_linkedin_post; ..."

# Fetch RSS feeds
.venv/bin/python -c "from data_sources.modules.rss_aggregator import RSSAggregator; ..."

# WordPress: Import article
.venv/bin/python -c "from data_sources.modules.wordpress_client import import_from_wordpress; print(import_from_wordpress('https://yoursite.com/blog/slug/'))"

# WordPress: Export to draft (preview only)
.venv/bin/python -c "from data_sources.modules.wordpress_client import export_to_wordpress; print(export_to_wordpress('content/published/slug/'))"

# WordPress: Export to draft (actually push)
.venv/bin/python -c "from data_sources.modules.wordpress_client import export_to_wordpress; print(export_to_wordpress('content/published/slug/', push=True))"

# WordPress: Regenerate markdown after edits
.venv/bin/python -c "from data_sources.modules.wordpress_client import regenerate_markdown; print(regenerate_markdown('content/published/slug/'))"

# Content Library: Sync all articles from WordPress
.venv/bin/python -c "from data_sources.modules.content_library import init_db, sync_all; init_db(); sync_all()"

# Content Library: Search articles
.venv/bin/python -c "from data_sources.modules.content_library import search; print(search('query'))"

# Content Library: Checkout article for editing
.venv/bin/python -c "from data_sources.modules.content_library import checkout; print(checkout('slug'))"

# Content Library: Checkin and push to WordPress
.venv/bin/python -c "from data_sources.modules.content_library import checkin; print(checkin('slug', push=True))"

# WordPress: Publish new markdown as learn article (preview)
.venv/bin/python -c "from data_sources.modules.wordpress_client import publish_markdown; print(publish_markdown('content/drafts/topic/article.md'))"

# WordPress: Publish new markdown as learn article (actually push)
.venv/bin/python -c "from data_sources.modules.wordpress_client import publish_markdown; print(publish_markdown('content/drafts/topic/article.md', post_type='article', push=True))"

# WordPress: Publish new markdown as blog post (actually push)
.venv/bin/python -c "from data_sources.modules.wordpress_client import publish_markdown; print(publish_markdown('content/drafts/topic/article.md', post_type='posts', push=True))"

# Run Gutenberg conversion tests
.venv/bin/python -m pytest tests/test_gutenberg_conversion.py -v
```

## Workflow Guardrail

If executing a command or skill leads to a situation that feels fundamentally wrong - where the end result would be materially different from what the user asked for - stop and ask before continuing.

## Webpage Builder

Build production-quality web pages (homepages, product pages, use case pages) using a multi-agent collaborative process.

- Command: `/webpage`, `/webpage new`, `/webpage continue`
- Projects live in `webpage-builder/projects/[descriptive-name]/`
- Agent personas: `webpage-builder/agents.md`
- Page type templates: `webpage-builder/page-types/`
- Separate from blog/SEO workflows — does not affect `/write`, `/linkedin`, `/optimize`

## Asset Builder

Create deep content assets (whitepapers, primers, solution guides, sales decks, competitive comparisons, etc.) using a 3-phase gated process with human checkpoints.

- Command: `/asset`, `/asset new`, `/asset continue`
- Projects live in `content/assets/[YYQ#-type-slug]/`
- Asset type templates: `asset-builder/asset-types/`
- Review agents: `.claude/agents/asset-reviewer.md`, `.claude/agents/persona-reviewer.md`
- Uses PMM knowledge from `$PMM_KNOWLEDGE_PATH` (set in `.env`)
- Separate from blog/SEO workflows — does not affect `/write`, `/linkedin`, `/optimize`

## Changelog

Every change to a core process, module, or workflow must include an entry in `docs/CHANGELOG.md`. This includes changes to Python modules in `data_sources/modules/`, publishing workflows, skill commands, and agent configurations. Write a brief entry describing the problem, fix, and impact.

## Collaborator Guidelines

Files in `.claude/commands/`, `.claude/agents/`, `context/`, and `data_sources/modules/` define the shared process and brand voice. **Do not modify these files.** Treat them as read-only reference material. If something seems wrong or outdated, flag it with the project owner rather than editing directly.

When starting a session, run `git pull` to get the latest process updates.

**Safe working directories** (all gitignored — write freely):
- `content/drafts/` — New article drafts
- `content/rewrites/` — Article rewrites
- `content/topics/` — LinkedIn ideas and topic research
- `content/research/` — Research briefs
- `content/workbench/` — Temporary editing checkouts
- `content/reviews/` — Content reviews
- `content/assets/` — Deep content projects (whitepapers, primers, decks, guides)
- `webpage-builder/projects/` — Webpage project work

## Reading WordPress Articles

When given a URL from your WordPress site, always use `import_from_wordpress` (not WebFetch) to get the content.

## WordPress Safety

**Never publish or delete WordPress content without explicit user confirmation.**

- `export_to_wordpress(..., push=True)` — Always confirm before running
- `publish_markdown(..., push=True)` — Always confirm before running
- `checkin(..., push=True)` — Always confirm before running
- Any WordPress delete operation — Always confirm before running

Preview operations (without `push=True`) are safe to run freely.

## Documentation

- Content Library system: see `docs/content-library.md`
- WordPress block evaluation: see `docs/wordpress-block-evaluation.md`
- Asset Builder system: see `docs/asset-builder.md`
