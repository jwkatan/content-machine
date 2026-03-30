# HubSpot Marketing Email Updates

Internal reference for updating existing HubSpot marketing emails via the PATCH API. Load this when working with email content, subject lines, or styling in HubSpot.

## API Endpoint

```
PATCH /marketing/v3/emails/{emailId}
```

**Docs**: https://developers.hubspot.com/docs/api-reference/marketing-marketing-emails-v3/marketing-emails/patch-marketing-v3-emails-emailId

## Safe Update Pattern

**Always update in place. Never construct content from scratch.**

1. **GET** the email to read its current content structure
2. **Modify** only the fields you need within that structure
3. **PATCH** back with the modified object

This preserves the template mode, editor-side changes, and widget structure. Constructing a new content object from scratch risks losing manual editor changes and breaking the template.

## Using update_email()

The `update_email()` function in `data_sources/modules/hubspot_client.py` wraps the safe GET-modify-PATCH pattern. It supports two modes:

### Simple Mode

Update common fields without touching the content structure directly. The function auto-detects the template mode and places HTML into the correct widget.

```python
from data_sources.modules.hubspot_client import HubSpotClient

client = HubSpotClient()

# Preview (no API write)
success, preview = client.update_email(
    email_id='372297849071',
    html='<p>New body content here</p>',
    subject='Updated subject line',
    from_name='[EXECUTIVE_NAME]',
    push=False,
)
print(preview)

# Apply changes
success, result = client.update_email(
    email_id='372297849071',
    html='<p>New body content here</p>',
    subject='Updated subject line',
    from_name='[EXECUTIVE_NAME]',
    push=True,
)
```

In simple mode, `html` is placed into:
- **DnD emails**: the `module-1-0-0` widget (Rich text area)
- **Design Manager emails**: the `hs_email_body` widget

### Advanced Mode

Pass a raw `updates` dict for full control over the PATCH payload. Use this when updating style settings, widget properties, or fields not covered by simple mode.

```python
success, result = client.update_email(
    email_id='372297849071',
    updates={
        'content': modified_content_dict,
        'name': 'Renamed email',
    },
    push=True,
)
```

You can combine both modes — simple fields (`subject`, `from_name`) merge with the `updates` dict.

## Two Template Modes

Every HubSpot email uses one of two template modes. **Never switch between them via PATCH.**

| Mode | templatePath | Content structure | Use for |
|------|-------------|-------------------|---------|
| DnD (Drag & Drop) | `@hubspot/email/dnd/Start_from_scratch.html` | `{flexAreas, widgets, styleSettings, templatePath}` | Marketing emails with banner, CTA button, styled layout |
| Design Manager | `Custom/email/Plain-text-email.html` | `{templatePath, widgets: {hs_email_body: ...}}` | Personal-style emails that look like they came from a person |

### How to identify the mode

GET the email and inspect `content.templatePath`:
- Contains `@hubspot/email/dnd/` → DnD mode
- Contains `Custom/email/` → Design Manager mode

## DnD Widget Module IDs

When editing DnD email content, widgets are identified by module ID:

| Widget | Module ID | Module name | Key properties |
|--------|-----------|-------------|----------------|
| Image | 1367093 | `@hubspot/image_email` | `src`, `alt`, `width` |
| Rich text | 1155639 | `@hubspot/rich_text` | `html` (the body content) |
| Button | 1976948 | Native CTA button | `destination`, `text`, `background_color` |
| Footer | 2869621 | `@hubspot/email_footer` | Standard unsubscribe footer |
| Divider | 2191110 | — | Visual separator |

## Brand Style Settings

Use these values in `content.styleSettings` for DnD emails:

| Property | Value | Notes |
|----------|-------|-------|
| Background color | `#F6F7FF` | Light lavender body background |
| Button color | `#4154FF` | Coastal-shore brand blue |
| Button border radius | `8px` | Rounded corners |
| Body border color | `#DBDFFF` | Subtle border around content area |
| Body border width | `1.5px` | |
| Link color | `#4154FF` | Matches button color |
| Text color | `#1D1E2B` | Near-black for readability |
| Font | Helvetica, Arial, sans-serif | 14px base size |

## Email Copy Style Conventions

### Marketing style (DnD template)

- No greeting — jump straight into the content
- Bold labels on bullet items (e.g., **Real-time sync**: keeps docs current)
- CTA button with action text ("Save your seat", "Download the guide")
- Generous whitespace between sections

### Personal style (Design Manager template)

- Opens with `Hi {{ contact.firstname }},`
- Short, conversational tone
- First names when mentioning colleagues
- Inline links instead of CTA buttons
- Sign-off with bold name + title (e.g., **[EXECUTIVE_NAME]**, [EXECUTIVE_TITLE] at [COMPANY])

## Updatable Fields

Fields that can be included in the PATCH payload:

| Field | Type | Notes |
|-------|------|-------|
| `content` | Object | The full content structure (template mode specific) |
| `subject` | String | Email subject line |
| `from` | Object | `{fromName, replyTo}` |
| `name` | String | Internal email name (visible in HubSpot UI, not to recipients) |
| `subcategory` | String | `batch_email` or `automated` — **cannot be changed after creation** |
| `state` | String | `DRAFT`, `PUBLISHED`, etc. |
| `publishDate` | String | ISO timestamp for scheduled send |
| `folderIdV2` | String | Move email to a different folder |
| `campaign` | String | HubSpot campaign ID |
| `language` | String | e.g., `en` |
| `to` | Object | Recipient list targeting |
| `sendOnPublish` | Boolean | Whether to send immediately on publish |
| `archived` | Boolean | Archive or unarchive the email |

## What Breaks

- **Switching template modes** (DnD to Design Manager or vice versa) via content PATCH — causes "template is missing" error
- **Changing `subcategory`** after creation (e.g., `batch` to `automated`) — silently ignored
- **Constructing content from scratch** instead of modifying the GET response — risks losing flexArea layout, widget order, and editor-side changes

## Reference

- Python client: `data_sources/modules/hubspot_client.py` (`update_email` method)
- Email creation: `create_marketing_email` method in the same file
- Autoresponder builder: `build_autoresponder_email_content` function
- Landing page pipeline: `setup_landing_page_pipeline` orchestrator
