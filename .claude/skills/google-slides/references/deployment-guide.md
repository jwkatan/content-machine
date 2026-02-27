# Google Slides Apps Script - Deployment Guide

## Initial Setup

1. Go to [script.google.com](https://script.google.com) -> New project
2. Name it "Content Machine Slides Publisher" (or similar)
3. Paste the code from `config/gslides_publisher_apps_script.js`
4. Go to **Project Settings** (gear) -> **Script Properties** -> Add:
   - `API_KEY` = (generate a random string, e.g., `openssl rand -base64 32`)
5. **Deploy** -> **New deployment** -> **Web app**
   - Execute as: **Me** (USER_DEPLOYING)
   - Access: **Anyone** (ANYONE_ANONYMOUS)
6. Approve the OAuth consent screen (will request Drive + Slides + external request permissions)
7. Copy the deployment URL to `data_sources/config/.env` as `GSLIDES_APPS_SCRIPT_URL`
8. Copy the API_KEY value to `.env` as `GSLIDES_API_KEY`

## Template Setup

1. Create your branded Google Slides template in Google Slides
2. Add placeholder tokens in text boxes using `{{TOKEN_NAME}}` format
3. Add `LAYOUT:LAYOUT_NAME` as the first line of speaker notes on each slide (required for slide identification)
4. Copy the template's file ID from the URL: `https://docs.google.com/presentation/d/FILE_ID/edit`
5. Add to `.env` as `GSLIDES_TEMPLATE_ID`

## Required OAuth Scopes

This script needs TWO scopes:

| Scope | Used by | Purpose |
|-------|---------|---------|
| `https://www.googleapis.com/auth/presentations` | `SlidesApp` | Read/write presentations |
| `https://www.googleapis.com/auth/drive` | `DriveApp` | Template duplication (`makeCopy`), file sharing |

These are requested automatically when you deploy and authorize.

### Manifest (appsscript.json)

If you need to set scopes manually:

1. In the Apps Script editor, click **Project Settings** (gear icon)
2. Check **Show "appsscript.json" manifest file in editor**
3. Edit `appsscript.json`:

```json
{
  "timeZone": "America/New_York",
  "dependencies": {},
  "oauthScopes": [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive"
  ],
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "webapp": {
    "executeAs": "USER_DEPLOYING",
    "access": "ANYONE_ANONYMOUS"
  }
}
```

Note: We do NOT use the Advanced Slides Service (`Slides` with capital S). We use `SlidesApp` (the native Apps Script service) which has a simpler API for our template-based approach.

## Available Actions

### `create` — Create a new presentation

Duplicates a template and fills placeholder tokens with content.

```python
response = requests.post(url, json={
    "action": "create",
    "key": api_key,
    "title": "Deck Title",
    "templateId": template_id,
    "slides": [
        {
            "layout": "LAYOUT_NAME",
            "tokens": {"TITLE": "Hello", "SUBTITLE": "World"},
            "speakerNotes": "Optional notes for this slide"
        }
    ]
})
# Returns: { presentationId, url, title, slidesCreated }
```

- Slides are reordered to match the payload order
- Template slides not included in the payload are deleted
- Set `"skip": true` on a slide to exclude it

### `update` — Update an existing presentation

Replace tokens in specific slides of an already-created presentation.

```python
response = requests.post(url, json={
    "action": "update",
    "key": api_key,
    "presentationId": "abc123...",
    "slides": [
        {"slideIndex": 0, "tokens": {"TITLE": "New Title"}, "speakerNotes": "Updated notes"}
    ]
})
# Returns: { presentationId, slidesUpdated }
```

### `share` — Make a presentation publicly viewable

Sets "anyone with the link can view" on a presentation. Useful for sharing with stakeholders or for visual review.

```python
response = requests.post(url, json={
    "action": "share",
    "key": api_key,
    "presentationId": "abc123..."
})
# Returns: { presentationId, url, shared: true }
```

### `status` — List tracked presentations

Returns all presentations created by this script (tracked via Script Properties).

```python
response = requests.post(url, json={"action": "status", "key": api_key})
# Returns: { presentations: [{ name, presentationId, url }, ...] }
```

### `template` — Analyze a template

Returns layout names, tokens, and text box dimensions for every slide in a template.

```python
response = requests.post(url, json={
    "action": "template",
    "key": api_key,
    "templateId": template_id
})
# Returns: { templateId, slideCount, layouts: [{ index, layout, tokens, textBoxes }, ...] }
```

### `tokenize` — Set up a new template (one-time)

Adds `LAYOUT:` names to speaker notes and replaces placeholder text with `{{TOKEN}}` markers. This is a one-time setup action when preparing a new template.

```python
response = requests.post(url, json={
    "action": "tokenize",
    "key": api_key,
    "templateId": template_id,
    "slideMap": [
        {
            "index": 0,
            "layout": "TITLE_SLIDE",
            "replacements": [
                {"find": "Presentation Title", "token": "TITLE"},
                {"find": "Subtitle text", "token": "SUBTITLE"}
            ]
        }
    ]
})
# Returns: { templateId, slidesProcessed, results: [...] }
```

The `nth` parameter (0-based) targets only the Nth matching shape when multiple shapes contain the same text:
```python
{"find": "Header text", "token": "COL_1_HEAD", "nth": 0}  # First match
{"find": "Header text", "token": "COL_2_HEAD", "nth": 0}  # Next match (first is already replaced)
```

## Updating Code

After changing the Apps Script code:
1. Paste new code in the editor
2. **Deploy** -> **Manage deployments** -> Edit (pencil icon) -> **New version** -> **Deploy**
3. The URL stays the same when using "New version" on an existing deployment

## Re-authorization

When adding new features that require additional OAuth scopes:

1. Update `appsscript.json` with the new scope (see manifest section above)
2. In the editor, click **Run** on any function (e.g., `doGet`) -> approve the authorization popup
3. Deploy a new version

## Testing the Endpoint

```python
import requests, os
from dotenv import load_dotenv

load_dotenv("data_sources/config/.env")

url = os.environ["GSLIDES_APPS_SCRIPT_URL"]
api_key = os.environ["GSLIDES_API_KEY"]

# Test: GET returns service info (no auth needed)
r = requests.get(url)
print(r.json())

# Test: status action
r = requests.post(url, json={"action": "status", "key": api_key})
print(r.json())

# Test: template analysis
r = requests.post(url, json={
    "action": "template",
    "key": api_key,
    "templateId": os.environ["GSLIDES_TEMPLATE_ID"]
})
print(r.json())
```

## Environment Variables Summary

Add these to `data_sources/config/.env`:

```bash
# Google Slides integration (separate from Google Docs)
GSLIDES_APPS_SCRIPT_URL=https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec
GSLIDES_API_KEY=your-generated-api-key
GSLIDES_TEMPLATE_ID=your-template-file-id

# Optional: additional templates
GSLIDES_BFSI_TEMPLATE_ID=your-bfsi-template-file-id
```

## Templates

Two branded templates are currently set up:

| Template | Env var | Slides | Use case |
|----------|---------|--------|----------|
| Brand Deck | `GSLIDES_TEMPLATE_ID` | 31 | General presentations, marketing, thought leadership |
| BFSI Sales Deck | `GSLIDES_BFSI_TEMPLATE_ID` | 46 | Enterprise sales for Banking/Financial Services |

Full layout catalogs: see `!.claude/skills/google-slides/references/template-layouts.md`

## Visual Review (Slide Screenshots)

To visually inspect generated presentations, use the `share` action + PDF export approach:

```python
import requests, os
from dotenv import load_dotenv

load_dotenv("data_sources/config/.env")

url = os.environ["GSLIDES_APPS_SCRIPT_URL"]
api_key = os.environ["GSLIDES_API_KEY"]
pres_id = "YOUR_PRESENTATION_ID"

# 1. Make it publicly viewable
requests.post(url, json={"action": "share", "key": api_key, "presentationId": pres_id})

# 2. Download as PDF via Google's public export URL
pdf = requests.get(f"https://docs.google.com/presentation/d/{pres_id}/export/pdf")
with open("/tmp/deck.pdf", "wb") as f:
    f.write(pdf.content)

# 3. Convert to PNGs (requires poppler: brew install poppler)
# pdftoppm -png -r 150 /tmp/deck.pdf /tmp/slide
```

This approach only needs the `presentations` and `drive` scopes (no `script.external_request`). The `share` action sets the file to "anyone with link can view", then the standard Google Slides export URL works without authentication.
