# Gated Download — Landing Page Template

## Metadata

- **Format**: landing-page (not prose — a conversion-focused page with form + content preview)
- **WordPress post type**: `download`
- **Taxonomy**: `download_category` (Guide=125, Primer=145, White paper=147)
- **Surfaces**: WordPress page + HubSpot form + autoresponder email

## Page Content

### Title
The page title. Displayed as H1 in the hero section. Format: `{Type}: {Title}` (e.g., "White paper: Closing the COBOL knowledge gap with [COMPANY]").

### Meta Description (SEO)
1-2 sentences for search engines. Concise value proposition.

### Excerpt
Short description shown below the title on the page and in resource center cards.

### Featured Image
Cover image shown alongside the form. Typically a mockup of the document cover.

### Category
One of: `Guide`, `Primer`, `White paper` (maps to download_category taxonomy).

### Benefit Cards (3)
Displayed in the "In the {type}" section below the form. Each card has:
- **Icon**: WordPress media ID (reuse existing blue=1886, violet=1887, yellow=1888 or upload new)
- **Title**: 2-4 words
- **Description**: 1 sentence, under 15 words

---

## HubSpot Form Configuration

### Form Name
For HubSpot dashboard identification. Format: `Download - {Title}`.

### Form Fields
Standard fields for gated downloads:
- First name (required)
- Last name (required)
- Email (required)
- Company name (required)
- Job title (optional — include for high-value assets like whitepapers)

### Thank You Message
Shown inline after form submission. Includes:
- **Title**: e.g., "Thanks for requesting the white paper!"
- **Body**: 1-2 sentences + download link. Format: "You can download it here. We will also send a copy to your email address.\n\n[Download the {type}](PDF_URL)"

---

## Autoresponder Email

### Subject Line
e.g., "Your white paper: Closing the COBOL knowledge gap"

### Email Body
- Thank the reader for their interest
- Brief 1-sentence recap of what the document covers
- Direct download link (prominent CTA button)
- Optional: "Questions? Reply to this email" closer

### From
- Name: [COMPANY]
- Email: (default from .env)

---

## WordPress Block Structure

The page content consists of exactly 2 Gutenberg blocks:

### Block 1: `gp/download-form`
Hero section with form. Key data fields:
- `hubspot_form_id` — Created by HubSpot client
- `thank_you_title` — From "Thank You Message" above
- `thank_you_text` — HTML with download link
- `title_type`: "h1", `title_style`: "h3"
- `section_id`: "download-form"

### Block 2: `gp/white-blocks`
Benefit cards section. Key data fields:
- `section_title` — "In the {type}" (e.g., "In the white paper")
- `section_blocks` — 3 (number of cards)
- `blocks_width` — "one-third"
- Per card: `section_blocks_N_title`, `section_blocks_N_text`, `section_blocks_N_image`

## Publishing — Automated Pipeline

Use `setup_landing_page_pipeline()` to create everything in one step:

```python
from data_sources.modules.hubspot_client import setup_landing_page_pipeline

# Preview first (no side effects)
success, preview = setup_landing_page_pipeline(
    page_type="download",
    title="White paper: ...",
    excerpt="...",
    slug="white-paper-...",
    meta_description="...",
    pdf_path="content/assets/.../document.pdf",
    page_content={
        "benefit_cards": [
            {"title": "...", "text": "..."},
            {"title": "...", "text": "..."},
            {"title": "...", "text": "..."},
        ]
    },
    salesforce_campaign_id="701Q500000...",  # Always ask user for this
    push=False,
)
print(preview)

# Then push=True with user confirmation
```

The pipeline handles: PDF upload → HubSpot form → autoresponder email (in gated document folder) → contact list (in gated document folder) → workflow (add-to-list → send email → Salesforce campaign → delay 4h, disabled) → WordPress draft.

**Important:** Always ask the user for the Salesforce campaign ID before running the pipeline.

## Quality Checklist

- [ ] Title follows `{Type}: {Descriptive title}` format
- [ ] Excerpt is compelling and under 30 words
- [ ] Exactly 3 benefit cards with short, scannable titles
- [ ] Featured image is a document cover mockup
- [ ] HubSpot form ID has been created and connected
- [ ] Thank-you message includes working download link
- [ ] Autoresponder email has download link and correct subject
- [ ] PDF has been uploaded to HubSpot CDN
- [ ] Meta description is under 160 characters
- [ ] Page created as WordPress draft (not published)
- [ ] Workflow created (disabled) — enable after manual review
