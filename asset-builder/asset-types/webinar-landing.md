# Webinar Landing — Landing Page Template

## Metadata

- **Format**: landing-page (conversion-focused registration/replay page)
- **WordPress post type**: `webinar`
- **Taxonomy**: `webinar_category` (Webinar=137)
- **Surfaces**: WordPress page + HubSpot form + autoresponder email

## Page Content

### Title
The webinar title. Displayed as H1 in the hero. Keep concise — no "Webinar:" prefix (the category badge handles that).

### Meta Description (SEO)
1-2 sentences for search engines. Focus on what the viewer will learn.

### Webinar Description
1-2 sentences shown in the form section. Frames the value proposition of attending/watching.

### Speakers (1-3)
Each speaker needs:
- **Name**: Full name
- **Position**: Title + company (e.g., "Head of product, [COMPANY]")
- **Portrait photo**: WordPress media ID (portrait crop for mobile)
- **Square photo**: WordPress media ID (square crop for desktop)
- **Decoration**: Visual style — `hidden`, `yellow`, `blue`, `purple`

### YouTube Video ID
For recorded webinars only. The 11-character YouTube video ID (e.g., `kv4y9uXCqFk`). Leave empty for upcoming webinars.

### Key Takeaways (3)
Numbered cards in "What you'll learn" section. Each has:
- **Title**: 3-5 words
- **Description**: 1 sentence, under 20 words

---

## HubSpot Form Configuration

### Form Name
For HubSpot dashboard. Format: `Webinar - {Title}`.

### Form Fields
Standard fields for webinar registration:
- First name (required)
- Last name (required)
- Email (required)
- Company name (required)

### Registration vs Replay
- **Upcoming webinar**: Form is for registration. Submit button: "Register now"
- **Recorded webinar**: Form gates access to the replay. Submit button: "Watch now"

---

## Autoresponder Email

### For Upcoming Webinars
- **Subject**: "You're registered: {Webinar title}"
- **Body**: Confirmation + date/time + calendar link + "Add to calendar" CTA
- **From**: [COMPANY]

### For Recorded Webinars
- **Subject**: "Your webinar replay: {Webinar title}"
- **Body**: Thank you + direct link to the replay page
- **From**: [COMPANY]

---

## WordPress Block Structure

The page content consists of exactly 2 Gutenberg blocks:

### Block 1: `gp/webinar-form`
Hero section with form + speaker photos. Key data fields:
- `hubspot_form_id` — Created by HubSpot client
- `speakers` — Number of speakers (integer)
- Per speaker: `speakers_N_name`, `speakers_N_position`, `speakers_N_portrait_photo`, `speakers_N_square_photo`, `speakers_N_decoration`
- `speaker_text_color` — "dark" (default)
- `youtube_video_id` — YouTube ID or empty
- `webinar_description` — Short description text
- `title_type`: "h1", `title_style`: "h3"
- `subheader`: "0"

### Block 2: `gp/white-number-blocks`
Numbered takeaways section. Key data fields:
- `section_title` — "What you'll learn"
- `section_blocks` — 3 (number of items)
- `blocks_columns` — "3"
- `blocks_style` — "style-2"
- `blocks_mark` — "number"
- Per item: `section_blocks_N_title`, `section_blocks_N_text`, `section_blocks_N_title_style` ("h5")

## Publishing — Automated Pipeline

Use `setup_landing_page_pipeline()` to create everything in one step:

```python
from data_sources.modules.hubspot_client import setup_landing_page_pipeline

# Preview first (no side effects)
success, preview = setup_landing_page_pipeline(
    page_type="webinar",
    title="...",
    excerpt="...",
    slug="...",
    meta_description="...",
    page_content={
        "speakers": [
            {"name": "...", "position": "...", "portrait_photo": 0, "square_photo": 0},
        ],
        "takeaways": [
            {"title": "...", "text": "..."},
            {"title": "...", "text": "..."},
            {"title": "...", "text": "..."},
        ],
        "youtube_video_id": "",  # empty for upcoming, ID for recorded
    },
    salesforce_campaign_id="701Q500000...",  # Always ask user for this
    push=False,
)
print(preview)

# Then push=True with user confirmation
```

The pipeline handles: HubSpot form → autoresponder email (in gated document folder) → contact list (in webinar folder) → workflow (add-to-list → send email → Salesforce campaign → delay 4h, disabled) → WordPress draft.

**Important:** Always ask the user for the Salesforce campaign ID before running the pipeline.

## Quality Checklist

- [ ] Title is concise and action-oriented
- [ ] Webinar description clearly states what viewer will learn
- [ ] All speakers have both portrait and square photos uploaded
- [ ] Exactly 3 key takeaways with scannable titles
- [ ] YouTube video ID set (for recorded) or empty (for upcoming)
- [ ] HubSpot form created with correct fields
- [ ] Autoresponder email matches webinar type (upcoming vs recorded)
- [ ] Meta description is under 160 characters
- [ ] Page created as WordPress draft (not published)
- [ ] Workflow created (disabled) — enable after manual review
