# Content Machine -- Onboarding Guide

## What is Content Machine?

Content Machine is a Claude Code workspace that turns Claude into a full content team. It writes SEO articles, LinkedIn posts, whitepapers, primers, sales decks, and web pages -- all in your brand voice.

**You don't need any integrations to start.** The core workflow produces local markdown files using just Claude Code and your brand context.

## Quick Start (15 minutes)

### Step 1: Python Environment

Create a virtual environment for the project:

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
# or: .venv\Scripts\activate  # Windows
```

If `python3` is not found, try `python`. You need Python 3.10 or higher.

### Step 2: Install Dependencies

```bash
.venv/bin/pip install -r requirements.txt
```

### Step 3: Core Configuration

```bash
cp data_sources/config/.env.example data_sources/config/.env
```

Open `data_sources/config/.env` and fill in the required fields:

```bash
COMPANY_NAME=Your Company Name
COMPANY_DOMAIN=yourcompany.com
LOGO_FILENAME=company-logo-white.svg
```

Everything else is optional. See the `.env.example` comments for what each integration enables.

### Step 4: Set Up Your Brand Context

The `context/` directory contains template files that teach Claude your brand voice. Fill them in this priority order:

| Priority | File | What to add |
|----------|------|-------------|
| 1 | `context/brand-voice.md` | Your voice pillars, tone guidelines, messaging framework, do's and don'ts |
| 2 | `context/writing-examples.md` | 3-5 complete blog posts from your site that represent your best writing |
| 3 | `context/features.md` | Your product/service features, benefits, and key differentiators |
| 4 | `context/internal-links-map.md` | Key pages from your site organized by topic cluster, with URLs |
| 5 | `context/style-guide.md` | Grammar rules, capitalization, formatting, terminology preferences |
| 6 | `context/target-keywords.md` | Your keyword research organized by topic cluster |
| 7 | `context/competitor-analysis.md` | Main competitors, their content strategies, gaps to exploit |
| 8 | `context/visual-guidelines.md` | Brand colors, visual style for AI image generation |
| 9 | `context/ceo-voice.md` | CEO writing samples for personal LinkedIn posts |

**Tip**: You can fill in just #1-3 to start writing immediately. The rest can be added over time.

### Step 5: Write Your First Article

Open Claude Code in the project directory:

```bash
claude
```

Then run:

```
/write [your topic]
```

For example: `/write content marketing strategies for B2B SaaS`

Claude will produce a full article in `content/drafts/` with SEO optimization reports.

## Optional Integrations

Each integration is self-contained. Set up only what you need.

### WordPress (CMS)

Enables: `/library`, `/wordpress-edit`, publish/import articles

1. In WordPress, go to Users > Profile > Application Passwords
2. Create a new application password
3. Add to `.env`:
```bash
WORDPRESS_SITE_URL=https://yoursite.com
WORDPRESS_USERNAME=your-username
WORDPRESS_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

4. Sync your content library:
```bash
.venv/bin/python -c "from data_sources.modules.content_library import init_db, sync_all; init_db(); sync_all()"
```

### Google Analytics 4 (Analytics)

Enables: Real traffic data in `/performance-review`

1. In Google Cloud Console, enable the Google Analytics Data API
2. Create a service account and download the JSON key
3. Add the service account email to your GA4 property (Viewer role)
4. Add to `.env`:
```bash
GA4_PROPERTY_ID=your_property_id
GA4_CREDENTIALS_PATH=./credentials/ga4-credentials.json
```

### Google Search Console (Analytics)

Enables: Keyword rankings and CTR data in `/performance-review`

1. Enable the Search Console API in Google Cloud Console
2. Add your service account to Search Console (Owner or Full access)
3. Add to `.env`:
```bash
GSC_SITE_URL=https://yoursite.com/
GSC_CREDENTIALS_PATH=./credentials/gsc-credentials.json
```

### DataForSEO (Analytics)

Enables: Competitive ranking data in `/performance-review`

1. Sign up at [dataforseo.com](https://dataforseo.com/)
2. Add to `.env`:
```bash
DATAFORSEO_LOGIN=your_email@example.com
DATAFORSEO_PASSWORD=your_api_password
```

### Google Gemini (Visual)

Enables: `/generate-images` for AI image generation

1. Get an API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Enable billing for image generation access
3. Add to `.env`:
```bash
GOOGLE_API_KEY=your_gemini_api_key
```

### Slack (Distribution)

Enables: Send LinkedIn posts to Slack for CEO review

1. Create an Incoming Webhook in your Slack workspace
2. Add to `.env`:
```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/yyy/zzz
```

### Google Slides (Presentations)

Enables: `/slides` command for branded presentations

1. Deploy the Apps Script from `config/gslides_publisher_apps_script.js`
2. Create a Google Slides template with `{{TOKEN}}` placeholders
3. Add to `.env`:
```bash
GSLIDES_APPS_SCRIPT_URL=https://script.google.com/macros/s/your-id/exec
GSLIDES_API_KEY=your-api-key
GSLIDES_TEMPLATE_ID=your-template-id
```

See `docs/COLLABORATOR-ONBOARDING.md` for detailed Apps Script deployment steps.

### Google Docs (Documents)

Enables: Publish content to Google Docs

1. Deploy the Apps Script from `config/gdocs_publisher_apps_script.js`
2. Add to `.env`:
```bash
GDOCS_APPS_SCRIPT_URL=https://script.google.com/macros/s/your-id/exec
GDOCS_API_KEY=your-api-key
```

### HubSpot (Image Hosting)

Enables: Host images for Slack/web embeds

1. Create a HubSpot access token with file manager permissions
2. Add to `.env`:
```bash
HUBSPOT_ACCESS_TOKEN=your-hubspot-access-token
```

### PMM Knowledge Base (Asset Builder)

Enables: More targeted whitepapers, primers, and decks via `/asset`

1. Create or clone a repo with personas, messaging, and competitive intel
2. Add to `.env`:
```bash
PMM_KNOWLEDGE_PATH=/path/to/your-pmm-repo
```

The `/asset` command works without this but produces less targeted content.

## Command Reference

| Command | What it does | Output location |
|---------|-------------|-----------------|
| `/research [topic]` | Keyword and competitive research | `content/research/` |
| `/write [topic]` | Full SEO article with auto-optimization | `content/drafts/` |
| `/rewrite [topic]` | Update existing content | `content/rewrites/` |
| `/optimize [file]` | Final SEO polish and readiness score | Same folder as input |
| `/analyze-existing [URL]` | Audit existing content | `content/research/` |
| `/linkedin` | LinkedIn dashboard and workflow | `content/topics/linkedin/` |
| `/generate-images [file]` | AI image generation | `images/` subfolder |
| `/performance-review` | Analytics-driven content priorities | `content/research/` |
| `/library` | Search and manage content library | Terminal output |
| `/wordpress-edit` | Edit WordPress articles | `content/published/` |
| `/slides` | Create Google Slides presentations | Google Drive |
| `/asset` | Deep content assets (whitepapers, etc.) | `content/assets/` |
| `/webpage` | Build web pages | `webpage-builder/projects/` |
| `/onboard` | Interactive setup wizard | Configures project |

## Context File Reference

| File | What it does | Priority |
|------|-------------|----------|
| `brand-voice.md` | Defines voice pillars, tone, and messaging so all content sounds like your brand | High -- fill first |
| `writing-examples.md` | 3-5 exemplary posts that teach Claude your specific writing style | High -- fill first |
| `features.md` | Product/service features and benefits for accurate content | High -- fill first |
| `internal-links-map.md` | Key pages organized by topic cluster for strategic internal linking | High |
| `style-guide.md` | Grammar, capitalization, formatting, and terminology preferences | Medium |
| `target-keywords.md` | Keyword research organized by topic cluster for targeting | Medium |
| `competitor-analysis.md` | Competitive intelligence for differentiation | Medium |
| `seo-guidelines.md` | SEO best practices (pre-filled, review and adjust) | Review |
| `visual-guidelines.md` | Brand colors and visual style for AI-generated images | Medium |
| `ceo-voice.md` | CEO writing samples for authentic personal LinkedIn posts | Medium |
| `wordpress-blocks.json` | WordPress Gutenberg block registry (auto-maintained) | Do not edit |

## Verification

Run this to check your setup:

```bash
.venv/bin/python -c "
from dotenv import load_dotenv
import os
load_dotenv('data_sources/config/.env')

checks = [
    ('Python env', True),
    ('Company name', os.environ.get('COMPANY_NAME', '')),
    ('WordPress', bool(os.environ.get('WORDPRESS_APP_PASSWORD', ''))),
    ('GA4', bool(os.environ.get('GA4_PROPERTY_ID', ''))),
    ('GSC', bool(os.environ.get('GSC_SITE_URL', ''))),
    ('DataForSEO', bool(os.environ.get('DATAFORSEO_LOGIN', ''))),
    ('Gemini', bool(os.environ.get('GOOGLE_API_KEY', ''))),
    ('Slack', bool(os.environ.get('SLACK_WEBHOOK_URL', ''))),
    ('Google Slides', bool(os.environ.get('GSLIDES_APPS_SCRIPT_URL', ''))),
    ('Google Docs', bool(os.environ.get('GDOCS_APPS_SCRIPT_URL', ''))),
    ('PMM Knowledge', os.path.isdir(os.environ.get('PMM_KNOWLEDGE_PATH', '/nonexistent'))),
]

for name, status in checks:
    icon = 'OK' if status else 'SKIP'
    print(f'  [{icon}] {name}')
"
```

Items marked `SKIP` are optional integrations you can set up later.
