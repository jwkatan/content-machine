---
name: google-slides
description: |
  Create branded Google Slides presentations via an Apps Script web app. Use this skill whenever
  you need to create presentations from content — including duplicating the branded template,
  filling placeholder tokens, adding speaker notes, or troubleshooting the integration.
  This is a SEPARATE Apps Script deployment from the Google Docs integration.
allowed-tools:
  - Bash(source .venv/bin/activate && python)
  - Bash(curl)
  - Read
  - Write
  - Edit
---

# Google Slides via Apps Script

This skill creates branded Swimm presentations by duplicating a Google Slides template and filling placeholder tokens with content. All operations happen via HTTP POST to an Apps Script endpoint.

## Architecture

```
Claude Code (Python HTTP client)
  |
  | HTTP POST with JSON payload
  v
Google Apps Script (deployed as web app)
  |
  | SlidesApp + Drive API
  v
Google Slides (branded presentations)
```

- **Approach**: Template-first. The branded template is designed once in Google Slides with placeholder tokens. The script duplicates it and fills tokens programmatically.
- **Authentication**: Shared API key (same pattern as Google Docs integration)
- **State tracking**: Presentation IDs stored in Script Properties

## Prerequisites

1. A deployed Apps Script web app (see `!.claude/skills/google-slides/references/deployment-guide.md`)
2. A branded Google Slides template with placeholder tokens (see Template section)
3. Environment variables in `data_sources/config/.env`:
   - `GSLIDES_APPS_SCRIPT_URL` — the deployed web app URL
   - `GSLIDES_API_KEY` — shared secret matching Script Properties `API_KEY`
   - `GSLIDES_TEMPLATE_ID` — the Google Slides template file ID

## Sending Requests

All interactions use HTTP POST with JSON. Use Python `requests` (not curl — Apps Script redirects break curl).

```python
import requests, os
from dotenv import load_dotenv

load_dotenv("data_sources/config/.env")

url = os.environ["GSLIDES_APPS_SCRIPT_URL"]
api_key = os.environ["GSLIDES_API_KEY"]

response = requests.post(url, json={
    "action": "create",
    "key": api_key,
    "title": "My Presentation",
    "templateId": os.environ["GSLIDES_TEMPLATE_ID"],
    "slides": [
        {
            "layout": "TITLE",
            "tokens": {
                "TITLE": "Presentation Title",
                "SUBTITLE": "A subtitle here"
            },
            "speakerNotes": "Welcome everyone to this presentation."
        }
    ]
})

result = response.json()
# {"presentationId": "1abc...", "url": "https://docs.google.com/...", "slidesCreated": 5}
```

## Available Actions

| Action | Purpose | Required fields |
|--------|---------|----------------|
| `create` | Duplicate template and fill slides | `title`, `templateId`, `slides` |
| `update` | Update tokens in an existing presentation | `presentationId`, `slides` |
| `status` | List tracked presentations | (none beyond `key`) |
| `template` | Return layout info from the template | `templateId` |
| `share` | Make presentation "anyone with link can view" | `presentationId` |
| `tokenize` | One-time template setup: add LAYOUT names + tokens | `templateId`, `slideMap` |

## Slide Payload Format

Each slide in the `slides` array:

```json
{
    "layout": "LAYOUT_NAME",
    "tokens": {
        "TOKEN_NAME": "Replacement text"
    },
    "speakerNotes": "Optional speaker notes for this slide",
    "skip": false
}
```

- `layout`: Which template slide to use (matches slide layout names from the template)
- `tokens`: Key-value pairs where keys match placeholder text in the template (e.g., `{{TITLE}}`)
- `speakerNotes`: Added to the slide's speaker notes section
- `skip`: Set `true` to exclude this template slide from the output

## Template System

### How it works

1. The branded template contains one slide per layout type
2. Each slide has placeholder tokens in text boxes (e.g., `{{TITLE}}`, `{{BODY}}`)
3. On `create`, the script:
   a. Duplicates the entire template via Drive API
   b. Opens the duplicate
   c. For each slide in the payload, finds the matching layout slide and replaces tokens
   d. Deletes any template slides not included in the payload
   e. Sets the presentation title

### Token format

Tokens in the template use double curly braces: `{{TOKEN_NAME}}`

The script does a simple text replacement — the token inherits the formatting (font, size, color, weight) of the placeholder text in the template. This is how branding is preserved.

### Layout catalog

<!-- TEMPLATE_LAYOUTS_START -->
Template ID: `1zVVkqMeFLiRIupg8wO_iPUeKvbi95xtH4D0JBEdyD1E` (31 slides)

### Title slides
| Layout | Tokens | Notes |
|--------|--------|-------|
| `TITLE_DARK` | `TITLE` | Main title, dark background |
| `TITLE_GRAPHIC` | *(none)* | Title with decorative graphic, dark bg |
| `TITLE_CENTER_LIGHT` | `TITLE`, `SUBTITLE` | Centered title + subtitle, light bg |
| `TITLE_CENTER_DARK` | `TITLE`, `SUBTITLE` | Centered title + subtitle, dark bg |

### Agenda slides
| Layout | Tokens | Notes |
|--------|--------|-------|
| `AGENDA_DARK` | `HEADING`, `ITEM_01`-`ITEM_06` | 6-item agenda grid, dark bg |
| `AGENDA_LIGHT` | `HEADING`, `ITEM_01`-`ITEM_06` | 6-item agenda grid, light bg |

### Content slides (title + open area for images/diagrams)
| Layout | Tokens | Notes |
|--------|--------|-------|
| `CONTENT_DARK_A` | `TITLE` | Dark bg, variant A |
| `CONTENT_DARK_B` | `TITLE` | Dark bg, variant B |
| `CONTENT_LIGHT_A` | `TITLE` | Light bg, variant A |
| `CONTENT_LIGHT_B` | `TITLE` | Light bg, variant B |
| `CONTENT_ACCENT` | `TITLE` | Accent color bg |

### Numbered list slides (3 items with descriptions)
| Layout | Tokens | Notes |
|--------|--------|-------|
| `NUMBERED_LIST_DARK` | `TITLE`, `SUBTITLE`, `NUM_1`-`NUM_3`, `DESC_1`-`DESC_3` | Dark bg |
| `NUMBERED_LIST_LIGHT` | `TITLE`, `SUBTITLE`, `NUM_1`-`NUM_3`, `DESC_1`-`DESC_3` | Light bg |

### Column slides
| Layout | Tokens | Notes |
|--------|--------|-------|
| `FOUR_COL` | `COL_1`-`COL_4` | 4 columns, no title |
| `FOUR_COL_TITLED` | `TITLE`, `COL_1`-`COL_4` | 4 columns with title |

### Timeline slides
| Layout | Tokens | Notes |
|--------|--------|-------|
| `TIMELINE_DARK` | `TITLE`, `TL_HEAD_1`-`TL_HEAD_4`, `TL_SUB_1`-`TL_SUB_4` | 4-item timeline, dark bg |
| `TIMELINE_LIGHT` | `TITLE`, `TL_HEAD_1`-`TL_HEAD_4`, `TL_SUB_1`-`TL_SUB_4` | 4-item timeline, light bg |
| `TIMELINE_YEARS_DARK` | `TITLE`, `YEAR_1`-`YEAR_6` | 6-year timeline, dark bg |
| `TIMELINE_YEARS_LIGHT` | `TITLE`, `YEAR_1`-`YEAR_6` | 6-year timeline, light bg |

### Special slides
| Layout | Tokens | Notes |
|--------|--------|-------|
| `LOGOS_DARK` | `TITLE` | Logo showcase, dark bg |
| `LOGOS_LIGHT` | `TITLE` | Logo showcase, light bg |
| `ICON_DARK` | *(none)* | Break/divider with icon |
| `BREAK_A` | *(none)* | Visual break, variant A |
| `BREAK_B` | *(none)* | Visual break, variant B |
| `IMAGE_A` | *(none)* | Full image slide, variant A |
| `IMAGE_B` | *(none)* | Full image slide, variant B |
| `IMAGE_C` | *(none)* | Full image slide, variant C |
| `DEMO_DARK` | `TITLE` | Demo section, dark bg |
| `DEMO_LIGHT` | `TITLE` | Demo section, light bg |
| `THANK_YOU_DARK` | `TITLE` | Closing slide, dark bg |
| `THANK_YOU_LIGHT` | `TITLE` | Closing slide, light bg |

### Layout selection guidance
- **Opening**: Use `TITLE_DARK` or `TITLE_CENTER_DARK` for the first slide
- **Structure**: Use `AGENDA_DARK` or `AGENDA_LIGHT` for the deck outline
- **Key points**: Use `NUMBERED_LIST_*` for 3 main takeaways
- **Comparisons**: Use `FOUR_COL_TITLED` for side-by-side items
- **Progress/history**: Use `TIMELINE_*` for chronological content
- **Breaks**: Use `BREAK_A/B` or `ICON_DARK` between major sections
- **Closing**: Use `THANK_YOU_DARK` or `THANK_YOU_LIGHT`
- **Dark vs Light**: Alternate for visual variety, or stay consistent with brand preference

### BFSI Sales Deck (Template 2)

Template ID: `1LFFg8mfM8HI_xJgJwjhQngf_fONFM58QDNuzElTLkPc` (46 slides)

Use case: Enterprise sales presentations for BFSI (Banking, Financial Services, Insurance) prospects.

**Full layout catalog**: See `!.claude/skills/google-slides/references/template-layouts.md`

Key layout categories: Title & Structure, Problem/Solution, Business Context, Architecture, Implementation, Proof & Results, Pillar Deep-Dives, Social Proof, Analysis & Comparison, Team & Roadmap, Appendix & Closing.

Typical BFSI sales deck flow:
1. `BFSI_TITLE_A` — Customer name + date
2. `AGENDA` — 4-5 topics
3. `STATEMENT` — Bold opening claim
4. `PROBLEM` — Their pain point
5. `SOLUTION` — Your answer
6. `OUTCOMES_METRICS` — 3 headline numbers
7. `DIFFERENTIATORS` — Why Swimm specifically
8. `CASE_STUDY_3COL` or `CUSTOMER_QUOTE` — Proof
9. `PILOT` — How to start
10. `THANK_YOU_A` — Close with contact info

Adjust for audience: add `WHY_NOW`/`STAKES` for executives, `INTEGRATION`/`CONTROLS` for technical, `PILLAR_*` deep-dives when you have more time.
<!-- TEMPLATE_LAYOUTS_END -->

## Text Constraints

<!-- TEXT_CONSTRAINTS_START -->
**Text size limits will be documented here after analyzing the template.**

Each layout has physical text box dimensions that limit how much text fits.
Exceeding these limits causes text overflow (text shrinks or gets cut off in Google Slides).
<!-- TEXT_CONSTRAINTS_END -->

## Critical Learnings

### 1. POST redirects — use Python, not curl

Same as Google Docs: Apps Script redirects POST requests (302). `curl -L` converts to GET. Always use Python `requests`.

### 2. Template duplication preserves all formatting

`DriveApp.getFileById(id).makeCopy(title)` creates an exact copy including all formatting, images, shapes, and master slide styles. This is why the template approach works for branding.

### 3. Token replacement inherits formatting

`shape.getText().replaceAllText('{{TOKEN}}', 'New text')` keeps the original text formatting. The replacement text takes on the font, size, color, and weight of the placeholder — no need to apply styles programmatically.

### 4. Bullet lists in token replacement

For body text with bullets, use newline-separated text. The template's text box should already have bullet formatting applied to the placeholder. The replacement text will inherit the bullet style.

If the template placeholder is NOT bulleted, you cannot add bullets via simple token replacement — the text box style would need to be modified via the Slides API `insertText` + `createParagraphBullets`.

### 5. Speaker notes via SlidesApp

```javascript
slide.getNotesPage().getSpeakerNotesShape().getText().setText(notes);
```

### 6. replaceAllText is case-INSENSITIVE by default

`shape.getText().replaceAllText(find, replace)` does case-insensitive matching. Replacing "Header" also matches "header" inside "Sub header". This caused token corruption during template setup.

**Mitigation**: When tokenizing repeated text that shares substrings, use sequential `nth=0` replacements — after each replacement the matched text is gone from that shape, so the next `nth=0` targets the next unreplaced shape. For mixed-case conflicts, replace the more specific/longer string first.

### 7. ASCII only in Apps Script code

Same as Google Docs: Unicode characters get mangled by clipboard. Use only ASCII in the script source.

### 8. Slide deletion must go in reverse order

When removing unused template slides, delete from last to first. Deleting a slide shifts the indices of subsequent slides.

### 9. Drive API scope required

Unlike the Docs integration (which only needs `documents` scope), Slides needs:
- `https://www.googleapis.com/auth/presentations` — for SlidesApp
- `https://www.googleapis.com/auth/drive` — for DriveApp.makeCopy() and sharing

### 10. Visual review via share + PDF export

To visually inspect generated slides, use `share` action to make the deck public, then download via Google's export URL (`/export/pdf`). Convert to PNGs with `pdftoppm` (from `poppler`). This avoids needing `UrlFetchApp` or extra OAuth scopes in the Apps Script. See deployment guide for full code.

## Extending the Apps Script

1. Read the current code at `config/gslides_publisher_apps_script.js`
2. Add new handler functions and wire into `doPost` switch
3. Present the updated script to the user for deployment
4. User deploys: **Deploy** -> **Manage deployments** -> Edit -> **New version** -> **Deploy**

## Reference Files

- Deployment guide: `!.claude/skills/google-slides/references/deployment-guide.md`
- Full Apps Script code: `config/gslides_publisher_apps_script.js`
- Template analysis: `!.claude/skills/google-slides/references/template-layouts.md` (created after template review)
