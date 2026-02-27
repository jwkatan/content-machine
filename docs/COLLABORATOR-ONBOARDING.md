# Collaborator Onboarding

## Getting Started

1. Clone both repos into the same parent folder:

```bash
git clone https://github.com/swimmio/marketing-content-writer.git
git clone https://github.com/swimmio/marketing-pmm.git
cd marketing-content-writer
```

2. Open a Claude Code session in the `marketing-content-writer` directory and give it this document. Claude will handle the rest of the setup for you.

## Setup Instructions for Claude

Run these steps in order. Automate everything you can. Only ask the user for input where marked **[ASK USER]**. After each step, confirm success before moving on.

### Step 1: Python Environment

```bash
python3 -m venv .venv
.venv/bin/pip install -r data_sources/requirements.txt
```

If `python3` is not found, try `python`. If neither works, tell the user to install Python 3.10+ first.

### Step 2: Core Credentials

Copy the example env file if it doesn't already exist:

```bash
[ -f data_sources/config/.env ] || cp data_sources/config/.env.example data_sources/config/.env
```

**[ASK USER]** for ALL of the following in a single prompt (don't ask one at a time):

- `WORDPRESS_SITE_URL` — Their WordPress site URL (e.g., `https://example.com`)
- `WORDPRESS_USERNAME` — WordPress username
- `WORDPRESS_APP_PASSWORD` — WordPress application password (created at wp-admin > Users > Profile > Application Passwords)
- `COMPANY_NAME` — Company name
- `COMPANY_DOMAIN` — Company domain (e.g., `example.com`)

Write all values into `data_sources/config/.env`. The other values (GA4, GSC, DataForSEO, Slack, HubSpot) are optional — skip them unless the user volunteers them.

### Step 3: PMM Knowledge Base

Auto-detect the `marketing-pmm` repo as a sibling directory and set the path. No user input needed if they followed the clone instructions.

```bash
PMM_PATH="$(cd .. && pwd)/marketing-pmm"
if [ -d "$PMM_PATH/knowledge_base" ]; then
  grep -q 'PMM_KNOWLEDGE_PATH' data_sources/config/.env 2>/dev/null || \
    echo -e "\n# PMM Knowledge Base (Asset Builder)\nPMM_KNOWLEDGE_PATH=$PMM_PATH" >> data_sources/config/.env
  echo "PMM knowledge base found at: $PMM_PATH"
else
  echo "PMM repo not found at $PMM_PATH"
fi
```

If the PMM repo is not found, tell the user the `/asset` command requires it and suggest cloning it as a sibling. If they cloned it elsewhere, **[ASK USER]** for the path and set `PMM_KNOWLEDGE_PATH` manually.

### Step 4: Google Docs Integration (optional)

The Google Docs integration publishes content to Google Docs via an Apps Script web app. This is a **separate** deployment from Google Slides.

**What Claude does:**
- Generate an API key: `openssl rand -base64 32`
- Copy the Apps Script code to clipboard from `config/gdocs_publisher_apps_script.js`
- Add env vars to `.env` once the user provides the deployment URL

**[ASK USER]** to perform these steps in their browser (Claude cannot access the Apps Script editor):

1. Go to [script.google.com](https://script.google.com) → **New project** → name it "Swimm Docs Publisher"
2. Paste the code Claude copied to their clipboard
3. Click **Services** (+) → Add **Google Docs API v1** (userSymbol: `Docs`)
4. Go to **Project Settings** (gear) → **Script Properties** → Add property:
   - Name: `API_KEY`, Value: `<the key Claude generated>`
5. **Deploy** → **New deployment** → **Web app**:
   - Execute as: **Me**
   - Access: **Anyone**
6. Approve the OAuth consent screen
7. Copy the **deployment URL** back to Claude

Once the user provides the URL, write these to `.env`:
```
GDOCS_APPS_SCRIPT_URL=<deployment URL from user>
GDOCS_API_KEY=<the key you generated>
```

**Verify** (run automatically):
```bash
.venv/bin/python -c "
import requests, os; from dotenv import load_dotenv; load_dotenv('data_sources/config/.env')
r = requests.post(os.environ['GDOCS_APPS_SCRIPT_URL'], json={'action': 'status', 'key': os.environ['GDOCS_API_KEY']})
print('Google Docs:', r.json())
"
```

### Step 5: Google Slides Integration (optional)

The `/slides` command creates branded Google Slides presentations via a **separate** Apps Script web app.

**What Claude does:**
- Generate an API key: `openssl rand -base64 32`
- Copy the Apps Script code to clipboard from `config/gslides_publisher_apps_script.js`
- Add env vars to `.env` once the user provides the deployment URL

**[ASK USER]** to perform these steps in their browser:

1. Go to [script.google.com](https://script.google.com) → **New project** → name it "Swimm Slides Publisher"
2. Paste the code Claude copied to their clipboard
3. Go to **Project Settings** (gear) → **Script Properties** → Add property:
   - Name: `API_KEY`, Value: `<the key Claude generated>`
4. **Deploy** → **New deployment** → **Web app**:
   - Execute as: **Me**
   - Access: **Anyone**
5. Approve the OAuth consent screen (will request Drive + Slides permissions)
6. Copy the **deployment URL** back to Claude

Once the user provides the URL, write these to `.env`:
```
GSLIDES_APPS_SCRIPT_URL=<deployment URL from user>
GSLIDES_API_KEY=<the key you generated>
GSLIDES_TEMPLATE_ID=1zVVkqMeFLiRIupg8wO_iPUeKvbi95xtH4D0JBEdyD1E
GSLIDES_BFSI_TEMPLATE_ID=1LFFg8mfM8HI_xJgJwjhQngf_fONFM58QDNuzElTLkPc
```

The template IDs are shared Google Slides templates with `{{TOKEN}}` placeholders. They're the same for all collaborators.

**Verify** (run automatically):
```bash
.venv/bin/python -c "
import requests, os; from dotenv import load_dotenv; load_dotenv('data_sources/config/.env')
r = requests.post(os.environ['GSLIDES_APPS_SCRIPT_URL'], json={'action': 'status', 'key': os.environ['GSLIDES_API_KEY']})
print('Google Slides:', r.json())
"
```

**Optional:** For visual review of generated slides, install poppler: `brew install poppler` (macOS) or `apt-get install poppler-utils` (Linux). This enables PDF-to-PNG conversion for inspecting slide layouts programmatically. See `.claude/skills/google-slides/references/deployment-guide.md` for details.

### Step 6: Content Library (optional)

If WordPress credentials are set up, sync the content library automatically:

```bash
.venv/bin/python -c "from data_sources.modules.content_library import init_db, sync_all; init_db(); sync_all()"
```

This creates a local searchable database of all published articles. It can be re-run anytime to get the latest content.

### Step 7: Final Verification

Run all checks in one go:

```bash
.venv/bin/python -c "
from dotenv import load_dotenv
import os
load_dotenv('data_sources/config/.env')

checks = []

# Core
checks.append(('Python env', True))
checks.append(('Company', os.environ.get('COMPANY_NAME', '')))
checks.append(('WordPress', bool(os.environ.get('WORDPRESS_APP_PASSWORD', ''))))

# PMM
checks.append(('PMM Knowledge', os.path.isdir(os.environ.get('PMM_KNOWLEDGE_PATH', '/nonexistent'))))

# Google Docs
checks.append(('Google Docs', bool(os.environ.get('GDOCS_APPS_SCRIPT_URL', ''))))

# Google Slides
checks.append(('Google Slides', bool(os.environ.get('GSLIDES_APPS_SCRIPT_URL', ''))))

for name, status in checks:
    icon = 'OK' if status else 'SKIP'
    print(f'  [{icon}] {name}')
"
```

Report the results to the user. Steps marked SKIP are optional — the user can set them up later.

---

## How to Use This Tool

You're set up. Here are the commands you can use:

| Command | What it does |
|---------|-------------|
| `/write [topic]` | Write a new SEO article from scratch |
| `/research [topic]` | Research a topic before writing |
| `/rewrite [slug]` | Refresh/update an existing article |
| `/optimize [file]` | Polish and optimize a draft |
| `/linkedin` | Create LinkedIn content |
| `/slides` | Create branded Google Slides presentations |
| `/analyze-existing [URL]` | Analyze an existing article |
| `/library` | Search and manage the content library |
| `/webpage` | Build a web page |
| `/asset` | Create deep content (whitepapers, primers, decks, guides) |
| `/performance-review` | Review content performance |

### Typical workflow

1. `/research [topic]` — generates a research brief in `research/`
2. `/write [topic]` — creates a full article in `drafts/`
3. Review the draft, ask Claude to make edits
4. When ready, tell Claude to publish — it will ask you to confirm before pushing to WordPress

### Staying up to date

When your project owner updates the process, context, or PMM knowledge, pull both repos:

```bash
git pull && cd ../marketing-pmm && git pull && cd ../marketing-content-writer
```

Or just tell Claude: "pull latest updates" (for this repo) or "pull PMM updates" (for the knowledge base).

## Important Rules

- **Do not modify** files in `.claude/commands/`, `.claude/agents/`, `context/`, or `data_sources/modules/`. These define the shared process. If something seems wrong, flag it with the project owner.
- **WordPress publishing** always requires your explicit confirmation. Claude will show you a preview and ask before pushing anything live.
- **Your work** goes into `drafts/`, `rewrites/`, `topics/`, `research/`, `workbench/`, and `content/assets/`. These are your local workspace — write freely.
