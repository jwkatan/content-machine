# Landing Pages: WordPress Field Mapping

Discovery date: 2026-03-01

## Architecture

Both `download` and `webinar` landing pages use **custom `gp/*` Gutenberg blocks** with JSON data attributes. There are NO ACF custom fields or post meta — all content lives inside block comments in the post content.

This means creating a landing page = constructing the correct `<!-- wp:gp/block-name {...json...} /-->` markup and POSTing it as the post content via the WordPress REST API.

## Post Types

| Type | REST endpoint | URL pattern | Taxonomy |
|------|--------------|-------------|----------|
| `download` | `/wp-json/wp/v2/download` | `/resources/downloadables/{slug}` | `download_category` |
| `webinar` | `/wp-json/wp/v2/webinar` | `/webinars/{slug}` | `webinar_category` |

## Download Categories

| ID | Name | Slug | Count |
|----|------|------|-------|
| 125 | Guide | guide | 6 |
| 145 | Primer | primer | 1 |
| 147 | White paper | white-paper | 1 |

## Webinar Categories

| ID | Name | Slug | Count |
|----|------|------|-------|
| 137 | Webinar | webinar | 4 |

---

## Gated Download Page Structure

Uses 2 blocks:

### Block 1: `gp/download-form`

The hero + form + featured image section.

```json
{
  "name": "gp/download-form",
  "data": {
    "title_type": "h1",
    "title_style": "h3",
    "hubspot_form_id": "2663abcc-bec5-427d-9ee6-2c7f90740a30",
    "thank_you_icon": "",
    "thank_you_title": "Thanks for requesting the white paper!",
    "thank_you_text": "You can download it here. We will also send a copy to your email address.\r\n\r\n<a href=\"https://...pdf\">Download the white paper</a>",
    "section_id": "download-form"
  },
  "mode": "preview"
}
```

**Content fields:**
- `hubspot_form_id` — HubSpot form GUID
- `thank_you_title` — Shown after form submission
- `thank_you_text` — HTML with download link to the PDF (hosted on HubSpot CDN)
- `title_type` / `title_style` — Heading tag and visual style

**Note:** The page title and excerpt come from the WordPress post title/excerpt fields, not from this block.

### Block 2: `gp/white-blocks`

The "In the white paper" benefits section with icon cards.

```json
{
  "name": "gp/white-blocks",
  "data": {
    "section_title": "In the white paper",
    "type": "h2",
    "style": "h2",
    "content_animation": "none",
    "section_blocks": 3,
    "blocks_align": "left",
    "blocks_width": "one-third",

    "section_blocks_0_image": 1886,
    "section_blocks_0_title": "Understanding COBOL",
    "section_blocks_0_text": "End the knowledge gap of old, complex applications",
    "section_blocks_0_label": "",
    "section_blocks_0_label_color": "blue",

    "section_blocks_1_image": 1887,
    "section_blocks_1_title": "Extracting business rules",
    "section_blocks_1_text": "Discover all your business rules across applications",

    "section_blocks_2_image": 1888,
    "section_blocks_2_title": "Trust",
    "section_blocks_2_text": "Learn why you can rely on [COMPANY] for accuracy, and completeness"
  },
  "mode": "edit"
}
```

**Content fields (per block N):**
- `section_blocks_N_title` — Card heading
- `section_blocks_N_text` — Card description
- `section_blocks_N_image` — WordPress media ID for icon
- `section_blocks_N_label` — Optional badge text
- `section_blocks_N_label_color` — Badge color (blue, etc.)
- `section_blocks` — Total number of blocks (integer)
- `blocks_width` — `one-third`, `one-half`, etc.

---

## Webinar Landing Page Structure

Uses 2 blocks:

### Block 1: `gp/webinar-form`

The hero + form + speaker photos section.

```json
{
  "name": "gp/webinar-form",
  "data": {
    "title_type": "h1",
    "title_style": "h3",
    "subheader": "0",
    "hubspot_form_id": "f4249c0d-04fc-4480-86cc-ae9f74fd2527",
    "speakers": 2,

    "speakers_0_portrait_photo": 5155,
    "speakers_0_square_photo": 5155,
    "speakers_0_name": "Inbal Gilead",
    "speakers_0_position": "Head of product, [COMPANY]",
    "speakers_0_decoration": "hidden",

    "speakers_1_portrait_photo": 4186,
    "speakers_1_square_photo": 3824,
    "speakers_1_name": "Gilad Navot",
    "speakers_1_position": "CPO, [COMPANY]",
    "speakers_1_decoration": "yellow",

    "speaker_text_color": "dark",
    "youtube_video_id": "kv4y9uXCqFk",
    "webinar_description": "AI won't modernize your mainframe if it can't understand it. [COMPANY] gives enterprises the missing foundation: reliable application understanding."
  },
  "mode": "preview"
}
```

**Content fields:**
- `hubspot_form_id` — HubSpot form GUID
- `speakers` — Number of speakers (integer)
- `speakers_N_name` — Speaker name
- `speakers_N_position` — Speaker title + company
- `speakers_N_portrait_photo` — WordPress media ID (portrait crop)
- `speakers_N_square_photo` — WordPress media ID (square crop)
- `speakers_N_decoration` — Visual decoration style: `hidden`, `yellow`, `blue`, etc.
- `youtube_video_id` — YouTube video ID for recorded webinars
- `webinar_description` — Short description text
- `speaker_text_color` — `dark` or `light`

### Block 2: `gp/white-number-blocks`

Numbered "What you'll learn" section.

```json
{
  "name": "gp/white-number-blocks",
  "data": {
    "section_title": "What you'll learn",
    "type": "h2",
    "style": "h2",
    "content_animation": "none",
    "section_blocks": 3,
    "blocks_columns": "3",
    "blocks_style": "style-2",
    "blocks_mark": "number",

    "section_blocks_0_title": "Why AI stalls",
    "section_blocks_0_text": "LLMs alone don't provide essential visibility into legacy systems.",
    "section_blocks_0_title_style": "h5",

    "section_blocks_1_title": "How [COMPANY] helps",
    "section_blocks_1_text": "How a hybrid approach gives an accurate and reliable understanding.",

    "section_blocks_2_title": "See it live",
    "section_blocks_2_text": "Demo of [COMPANY] unblocking human and AI teams for faster progress."
  },
  "mode": "edit"
}
```

**Content fields (per block N):**
- `section_blocks_N_title` — Numbered item heading
- `section_blocks_N_text` — Numbered item description
- `section_blocks_N_title_style` — Heading style (`h5`, etc.)
- `section_blocks` — Total count
- `blocks_columns` — Column layout (`3`, `2`, etc.)
- `blocks_mark` — `number` for numbered, other options may exist

---

## HubSpot Configuration

- **Portal ID**: `HUBSPOT_PORTAL_ID` (env var)
- **Region**: `HUBSPOT_REGION` (env var, default: `na1`)
- **Download form**: created per-asset via `create_landing_page_form()`
- **Webinar form**: created per-asset via `create_landing_page_form(form_type='webinar')`

Each landing page gets its own HubSpot form (unique form ID per page).

## WordPress Post Fields Used

Both types use standard WordPress fields:
- `title` — Page title (rendered in hero)
- `excerpt` — Short description (used for SEO/cards)
- `featured_media` — Featured image (WordPress media ID; download pages use this, webinars may not)
- `{type}_category` — Taxonomy term IDs
- `slug` — URL slug
- `status` — Always create as `draft`

## Screenshots

- Gated download: `docs/screenshot-gated-download.png`
- Webinar landing: `docs/screenshot-webinar-landing.png`
