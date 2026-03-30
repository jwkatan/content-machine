# Image Builder System

Deterministic branded image generation for landing pages, email banners, social media, and more.

## What Is Image Builder?

Unlike `/generate-images` (which creates novel AI-generated imagery), Image Builder renders **pixel-perfect, brand-consistent images** from HTML/CSS templates designed in Figma.

- **Deterministic**: Same template + inputs = identical output every time
- **Brand-safe**: Colors, fonts, layouts come from Figma designs
- **Web-optimized**: Lossless WebP or PNG, < 200KB typical file size
- **Learning**: New templates can be added as you need them

## How It Works

```
User request → Template selection → Collect inputs → Render (Node.js) → Optimize → Output
  (/image)     (match to registry)  (PDF, paths)    (Puppeteer+sharp)  (compress)  (PNG/WebP)
```

### The Pipeline

1. **User invokes** `/image [description]`
2. **Agent matches** the request to available templates
3. **User selects** a template (or creates a new one)
4. **Agent collects** required inputs (PDF path, output location, etc.)
5. **Node.js renderer** extracts images, populates templates, screenshots HTML
6. **Sharp optimizer** compresses to WebP/PNG
7. **Output**: `path/to/image.webp` (~100KB, transparent background, etc.)

## Directory Structure

```
image-builder/
├── package.json              # npm dependencies
├── render.js                 # HTML → PNG/WebP renderer (Puppeteer + sharp)
├── pdf-to-image.js          # PDF first-page extractor
└── templates/
    ├── gated-document/       # Pre-built template
    │   ├── template.html     # HTML/CSS layout
    │   └── template.yaml     # Metadata & specs
    ├── email-banner/         # (created as needed)
    │   ├── template.html
    │   └── template.yaml
    └── ... (more templates as you create them)

data_sources/modules/
└── image_builder.py          # Python wrapper (list templates, render)

.claude/commands/
└── image.md                  # /image slash command definition

.claude/agents/
└── image-designer.md         # Helper agent for template selection

docs/
└── image-builder.md          # This file
```

## Using Image Builder

### Quick Start: Render a Gated Document Image

```bash
/image landing page banner for the COBOL whitepaper
```

Flow:
1. Agent identifies HTML file at `content/assets/26Q1-.../[company]-vs-[competitor].html`
2. Agent shows the pre-built `gated-document` template
3. User confirms
4. Image renders → saved to `content/assets/26Q1-.../landing-page-banner.webp`

### Template Selection

The agent will:
- **1 matching template**: Show it and ask "Does this work?"
- **Multiple matches**: Show all with Figma previews and ask "Which fits?"
- **No matches**: Offer to create a new template

To see all available templates:

```python
from data_sources.modules.image_builder import list_templates
for t in list_templates():
    print(f"{t['id']}: {t['name']}")
    print(f"  Use cases: {', '.join(t['use_cases'])}")
```

### Adding New Templates

When you need a template that doesn't exist:

1. **Design in Figma** (following your brand guidelines)
2. **Share the Figma file + node ID** with Claude
3. **Agent extracts design** → auto-builds HTML template
4. **You review** the HTML, tweak if needed
5. **Agent registers** the template in the registry
6. **Render** your first image with the new template

Example workflow:
```
/image email header for customer onboarding sequence
→ "No existing email template. Let's create one from Figma."
→ User: "Here's the design: https://figma.com/design/ABC?node-id=123:456"
→ Agent auto-builds HTML, shows preview
→ User reviews and approves
→ Agent registers in registry
→ Agent renders the image
```

## Template Anatomy

Each template is a folder in `image-builder/templates/{template-id}/`:

### `template.yaml` (Metadata)

```yaml
name: "Gated Document Landing Page"
description: "Stacked card effect for whitepaper/guide landing pages"

# Keywords for template matching
use_cases:
  - landing-page
  - gated-document
  - whitepaper
  - guide
  - competitive-comparison

# Output specifications
output:
  width: 1206
  height: 1562
  format: webp        # webp for web, png for ads/social
  lossless: true      # always use lossless compression
  background: transparent  # or hex color like #FFFFFF

# What the template needs as inputs
inputs:
  pdf_first_page: true  # extract first page of PDF
  # other inputs might be: text fields, custom colors, etc.

# Figma source (for future updates)
figma:
  file: [YOUR_FIGMA_FILE_KEY]
  node: "3650:497"
  last_synced: "2026-03-04"
```

### `template.html` (Layout)

HTML/CSS with `{{PLACEHOLDER}}` tokens:

```html
<img src="{{PDF_FIRST_PAGE_BASE64}}" alt="Document cover">
```

Common placeholders:
- `{{PDF_FIRST_PAGE_BASE64}}`: First page of PDF, embedded as data URI
- `{{TITLE}}`: Text field
- `{{SUBTITLE}}`: Text field
- `{{BACKGROUND_COLOR}}`: Hex color

## Gated-Document Template

Pre-built for landing pages of whitepapers, guides, competitive comparisons, etc.

**Approach:**
- Takes an HTML asset file as input and screenshots it directly at landing page dimensions
- No template composition — preserves the original HTML formatting and styling

**Output specs:**
- Canvas: 1206 × 1562px (web-optimized aspect ratio)
- Format: WebP (lossless compression)
- File size: ~50-100KB
- White background

**Required input:**
- `html_path`: Path to the HTML asset file

**Example:**
```python
from data_sources.modules.image_builder import render_image

result = render_image(
    template_id='gated-document',
    inputs={'html_path': 'content/assets/YYQ#-[asset-type]-[slug]/[company]-vs-[competitor].html'},
    output_path='content/assets/YYQ#-[asset-type]-[slug]/landing-page-banner.webp'
)
```

**Figma source:** [Guides file, node 3650:497](https://www.figma.com/design/[YOUR_FIGMA_FILE_KEY]/Guides?node-id=3650-497)

## Python API

```python
from data_sources.modules.image_builder import list_templates, render_image, get_template

# List all templates
templates = list_templates()

# Get a specific template's metadata
template = get_template('gated-document')
print(template['metadata'])  # YAML as dict

# Render an image
result = render_image(
    template_id='gated-document',
    inputs={'pdf_path': 'path/to/file.pdf'},
    output_path='path/to/output.webp'
)

if result['success']:
    print(f"✓ {result['path']} ({result['size']} bytes)")
else:
    print(f"✗ {result['error']}")
```

## File Optimization Details

**WebP (web-optimized):**
- Lossless compression
- ~70% smaller than PNG
- Supported in all modern browsers
- Recommended for website usage

**PNG (full compatibility):**
- Lossless compression
- Larger file size (~150KB vs ~80KB WebP)
- Recommended for ads, social media, email

**Optimization pipeline:**
1. Puppeteer screenshots HTML at requested dimensions
2. Sharp converts to target format (WebP/PNG)
3. Metadata stripped (EXIF, color profiles, etc.)
4. Compression applied (PNG: level 9, WebP: lossless)

**Target file sizes:**
- Landing page banner: < 150KB
- Email header: < 100KB
- Social media card: < 80KB

## Performance

Typical render times (for gated-document template):
- PDF extraction: ~2-3 seconds
- HTML rendering: ~3-4 seconds
- Optimization: ~1-2 seconds
- **Total: ~7-10 seconds**

## Brand Guidelines in Templates

Templates follow [[COMPANY] Visual Guidelines](../context/visual-guidelines.md):

- **Colors**: From brand palette (brand-primary, brand-text, etc.)
- **Fonts**: Roc Grotesk (TypeKit) + Mulish (Google Fonts)
- **Spacing**: 8px grid
- **Background**: Transparent or brand-text (#1D1E2B)
- **Shadows**: Subtle drop-shadows only (no harsh effects)
- **Style**: Flat design, no gradients unless intentional

## Troubleshooting

### "Template not found"
- Check template ID is correct
- Run `list_templates()` to see available templates

### "PDF file not found"
- Verify PDF path is absolute or relative to project root
- Check file permissions (readable)

### "Render failed"
- Check Node.js dependencies: `npm install` in `image-builder/`
- Verify output directory exists and is writable
- Check system has available disk space

### "Image looks wrong"
- Review the template HTML
- Check font loading (TypeKit + Google Fonts available online)
- Verify placeholder values are correct (especially for text fields)

## Creating New Templates

### Step 1: Design in Figma

Create your design following your brand guidelines. Document:
- Exact dimensions (width × height)
- Which elements are variable (text fields, colors, images)
- Placeholder locations

### Step 2: Share with Claude

```
/image I need a new [type] template. Here's the Figma design:
[Figma URL with node ID]
```

### Step 3: Agent Auto-Builds

Claude will:
1. Fetch design context from Figma
2. Extract colors, fonts, dimensions
3. Build HTML template with placeholders
4. Create template.yaml
5. Show preview for your review

### Step 4: Review & Register

You can:
- Accept the auto-generated HTML as-is
- Edit the HTML file before registering
- Ask for modifications

Once approved, the template is added to `image-builder/templates/{id}/` and ready to use.

## Examples

### Example 1: Gated Document (Pre-built)

```bash
/image landing page image for the COBOL competitive comparison
```

Result: `content/assets/26Q1-.../landing-page-banner.webp` (1206×1562, ~120KB)

### Example 2: Email Header (To be created)

```bash
/image email header for the welcome sequence
```

Result: New template created, registered, and first image rendered.

### Example 3: Social Media (To be created)

```bash
/image LinkedIn post image for our latest blog
```

Result: Agent guides through dimensions (typically 1080×1080), template creation, render.

## See Also

- [Visual Guidelines](../context/visual-guidelines.md) — Brand colors, fonts, design principles
- [[COMPANY] Logo](../context/assets/logo-white.svg) — White logo for dark backgrounds
- `/image` command — User-facing interface
- Image Designer agent — Template selection helper
