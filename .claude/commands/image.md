# /image — Learning Graphic Designer

Generate deterministic, brand-consistent images for landing pages, email banners, social media, and more. The system learns from templates you create in Figma.

## Usage

```
/image [description of what you need]
```

**Examples:**
```
/image banner for the COBOL competitive comparison landing page
/image email header for the whitepaper download sequence
/image LinkedIn post image for the latest blog
/image social card for the modernization guide
/image inline graphic for the three-stage AI progression section
```

## Workflow

### Phase 1: Understand the Request

Parse the user's request to infer:
- **Use case**: landing page, email banner, blog header, social media, ad, etc.
- **Source asset**: PDF path, blog article slug, or other content
- **Constraints**: Any specific requirements or preferences

Read the template registry to understand available templates:

```python
from data_sources.modules.image_builder import list_templates
templates = list_templates()
```

Output the template registry to understand what's available.

### Phase 2: Present Template Options

**If one template matches:** Show it with Figma thumbnail and ask "Does this template work for your use case?"

**If multiple templates match:** Show all options with thumbnails and ask "Which template fits best, or do you need something new?"

**If no templates match:** Offer to help add a new template from Figma.

To fetch Figma thumbnail for comparison, use `get_screenshot` on the template's Figma file/node.

### Phase 3: Collect Required Inputs

Depending on the template, confirm:
- PDF path (if it's a gated document)
- Output location (default: co-located with source asset)
- Any text customization (rarely needed for the current templates)

**Static templates** (e.g., `ai-stages-progression`) require no inputs — content is baked into the HTML. Pass `inputs={}` when rendering.

### Phase 4: Render

Call the Python wrapper:

```python
from data_sources.modules.image_builder import render_image

result = render_image(
    template_id='gated-document',
    inputs={'pdf_path': 'content/assets/26Q1-competitive-comparison-claude-cobol/[company]-vs-[competitor].pdf'},
    output_path='content/assets/26Q1-competitive-comparison-claude-cobol/landing-page-banner.webp'
)

if result['success']:
    print(f"✓ Generated: {result['path']} ({result['size']} bytes, {result['format']})")
else:
    print(f"✗ Error: {result['error']}")
```

### Phase 5: Adding New Templates (If Needed)

If the user needs a new template that doesn't exist:

1. **Get Figma design context** for the template (using `get_design_context` on the Figma file/node)
2. **Auto-build HTML template** from the Figma design context
3. **Create template.yaml** metadata (name, description, use_cases, output specs)
4. **Register** in the template registry
5. **Test render** with the user's actual content
6. Return the generated template files for the user to review/tweak if needed

---

## Template Registry

All templates live in `image-builder/templates/{template-id}/`:

```
image-builder/templates/
├── gated-document/
│   ├── template.html       # Layout (recreated from Figma)
│   └── template.yaml       # Metadata: output size, format, inputs, Figma source
├── email-banner/           # (added as new templates are created)
│   ├── template.html
│   └── template.yaml
└── ...
```

Each `template.yaml` includes:
- **name** & **description**: For user-facing template selection
- **use_cases**: Keywords to match with the user's request
- **output**: width, height, format (webp/png), lossless flag, background (transparent/color)
- **inputs**: What the template requires (pdf_first_page, text fields, etc.)
- **figma**: Source file + node ID (for future updates)

---

## Output Specifications

**Default output locations** (user can override):

| Use case | Path |
|----------|------|
| Gated document (PDF) | `content/assets/[slug]/landing-page-banner.webp` |
| Blog article | `content/drafts/[slug]/images/banner.png` |
| Blog inline graphic | `content/drafts/[slug]/images/[name].png` |
| Email campaign | `content/assets/[slug]/email-banner.png` |
| Social media | `content/assets/[slug]/social-[platform].png` |
| Ad banner | `content/assets/[slug]/ad-banner.png` |

**File optimization:**
- **WebP**: Lossless compression, smallest file size (for web)
- **PNG**: Lossless, full compatibility (for ads, social, email)
- **Target size**: < 200KB (typical: 50-150KB after optimization)
- **Transparency**: Preserved if template background is transparent

---

## Pre-Built Templates

### `gated-document` — Landing page banner from PDF

```
/image banner for the COBOL competitive comparison landing page
```

Flow: identifies PDF → extracts first page → renders stacked blue border frame → saves as WebP. Requires `pdf_path` input.

### `ai-stages-progression` — Inline blog infographic

Three-column progression diagram (Autocomplete → AI Assistant → AI Agent). Content is baked in — no inputs required. Use for the "how human oversight consolidates" section of articles about AI-driven development.

```
/image inline graphic for the three-stage AI progression
```

Flow: no inputs needed → renders 900×380 PNG → saves to `content/drafts/[slug]/images/[name].png`.

---

## Spawn the Image Designer Agent

For complex requests requiring template selection and guidance:

```
[Task tool with subagent_type: general-purpose]
name: "Image Designer"
prompt: """
You are the Learning Graphic Designer. Your job is to help the user create deterministic,
brand-consistent images using templates.

User's request: [request from Phase 1]

1. Read the template registry (list_templates())
2. Present matching template options with brief descriptions
3. Show Figma thumbnails (get_screenshot) for visual reference if helpful
4. Guide the user to pick one or create a new one
5. Collect any required inputs (PDF path, output location, etc.)
6. Render the image
7. Report success/failure with file size and location

Be conversational and helpful. Ask clarifying questions if the request is ambiguous.
"""
```

Or handle entirely inline if the request is straightforward (e.g., "gated document banner for this PDF").

---

## Notes

- **Deterministic output**: Same template + inputs = identical image every time (pixel-perfect)
- **Learning system**: As you add more templates to Figma, register them in the template registry
- **Brand safe**: All colors, fonts, and layouts come from Figma designs or your brand guidelines
- **Fast workflow**: Gated-document template renders in ~10 seconds (extraction + rendering + optimization)
