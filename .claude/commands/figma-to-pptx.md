# Figma to PPTX Command

Convert Figma frames into a high-fidelity PowerPoint presentation that can be opened in Keynote for transitions, talk tracks, and video export.

## Usage
`/figma-to-pptx [optional: output filename or description]`

**Prerequisites:**
- Figma MCP server must be connected
- The user must have the target frames selected in Figma (or provide frame references)
- Screenshots of the frames may be provided in the conversation for visual reference

## What This Command Does
1. Extracts design data from Figma frames via MCP (metadata, variables, screenshots)
2. Recreates each frame as a PPTX slide with precise positioning, colors, fonts, and images
3. Saves a production-quality `.pptx` file ready for Keynote/PowerPoint
4. User adds transitions, animations, and talk track in Keynote, then exports as video

## Process

### Phase 1: Figma Data Extraction

Extract all design data from the selected Figma frames using the MCP tools. Call these in parallel where possible:

#### 1a. Get Metadata (Structure & Layout)
Use the `get_metadata` Figma MCP tool on the selection to retrieve:
- Layer hierarchy (parent/child relationships)
- Layer names and types (frame, text, rectangle, image, group, etc.)
- Positions (x, y) and dimensions (width, height) for every element
- Element IDs for cross-referencing

#### 1b. Get Design Variables (Colors, Fonts, Tokens)
Use the `get_variable_defs` Figma MCP tool to retrieve:
- Color definitions (hex/RGB values, color names)
- Typography tokens (font families, sizes, weights, line heights)
- Spacing tokens
- Any other design system variables in use

#### 1c. Get Screenshots (Visual Reference)
Use the `get_screenshot` Figma MCP tool to capture visual screenshots of:
- Each individual frame (for per-slide verification)
- The overall selection (for context)
These serve as the **ground truth** for verifying fidelity.

#### 1d. Get Design Context (Structured Code Representation)
Use the `get_design_context` Figma MCP tool with `framework: "HTML/CSS"` to get:
- A structured code representation of the design
- CSS-like properties (colors, fonts, borders, shadows, opacity)
- Layout information (flexbox/grid patterns, alignment, spacing)
- This is often the richest data source for recreating visual fidelity

**Important:** If the user also provides screenshots in the conversation, use those as additional visual references. Cross-reference MCP data against screenshots to catch anything the API might miss.

### Phase 2: Design Analysis

Before generating slides, analyze the extracted data to build a complete picture:

#### 2a. Canvas Setup
- Determine the frame dimensions from metadata
- All frames in a Figma presentation are typically the same size
- Map frame dimensions to PPTX slide dimensions (use exact pixel-to-inch conversion: **1 inch = 72 points = 96 CSS pixels**; Figma uses CSS pixels)
- Standard conversions:
  - 1920×1080 Figma frame → 20" × 11.25" (or scale to 10" × 5.625" for 16:9)
  - 1440×900 → 15" × 9.375" (or scale proportionally)
- **Scaling approach**: Determine a scale factor so the slide fits standard dimensions while preserving aspect ratio. Apply this scale factor to ALL element positions and sizes.

#### 2b. Element Inventory
For each frame, catalog every element and its properties:
- **Text elements**: content, font family, font size, font weight, color, alignment, line height, letter spacing
- **Rectangles/shapes**: position, size, fill color, border (color, width, radius), opacity, shadow
- **Images**: position, size, source (extract from Figma if possible, or use screenshot crop)
- **Lines/dividers**: start/end points, color, weight, dash style
- **Groups**: child elements and their relative positions
- **Icons/vectors**: capture as images if complex (SVG → PNG export)

#### 2c. Render Order
Determine the z-order (front-to-back stacking) of elements from the metadata hierarchy. Elements should be added to the slide in back-to-front order so overlapping works correctly.

### Phase 3: PPTX Generation

Generate the PowerPoint file using `python-pptx`. Save the generation script to `temporary/figma-to-pptx/generate.py` for reproducibility.

#### 3a. Python Script Structure
```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import requests
from io import BytesIO
import os

# --- Configuration ---
SCALE_FACTOR = ...  # calculated in Phase 2
SLIDE_WIDTH = Inches(...)
SLIDE_HEIGHT = Inches(...)
OUTPUT_PATH = 'temporary/figma-to-pptx/output.pptx'

# --- Helper Functions ---

def figma_to_inches(px):
    """Convert Figma pixels to inches using scale factor."""
    return Inches(px * SCALE_FACTOR / 96)  # 96 CSS px per inch

def figma_color(hex_or_rgba):
    """Convert Figma color to RGBColor."""
    # Handle hex (#RRGGBB) or RGBA
    ...
    return RGBColor(r, g, b)

def add_text_element(slide, element):
    """Add a text element with precise formatting."""
    ...

def add_shape_element(slide, element):
    """Add a rectangle/shape with fill, border, corner radius."""
    ...

def add_image_element(slide, element):
    """Add an image from file or URL."""
    ...

# --- Build Presentation ---
prs = Presentation()
prs.slide_width = SLIDE_WIDTH
prs.slide_height = SLIDE_HEIGHT

# For each frame, create a slide and add elements in z-order
for frame in frames:
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Set background
    if frame.background:
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = figma_color(frame.background)

    # Add elements back-to-front
    for element in frame.elements:
        if element.type == 'text':
            add_text_element(slide, element)
        elif element.type == 'rectangle':
            add_shape_element(slide, element)
        elif element.type == 'image':
            add_image_element(slide, element)
        # ... etc

prs.save(OUTPUT_PATH)
```

#### 3b. Element Mapping Reference

**Text elements:**
```python
textbox = slide.shapes.add_textbox(left, top, width, height)
tf = textbox.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.alignment = PP_ALIGN.LEFT  # or CENTER, RIGHT
run = p.add_run()
run.text = "..."
run.font.name = "Inter"  # Match Figma font
run.font.size = Pt(16)
run.font.bold = True
run.font.color.rgb = RGBColor(51, 51, 51)
```

**Rectangles with rounded corners:**
```python
# python-pptx doesn't expose corner radius directly
# Use ROUNDED_RECTANGLE for rounded, RECTANGLE for sharp
shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if corner_radius > 0 else MSO_SHAPE.RECTANGLE
shape = slide.shapes.add_shape(shape_type, left, top, width, height)
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(r, g, b)
shape.fill.transparency = 1.0 - opacity  # Figma opacity → PPTX transparency
shape.line.color.rgb = RGBColor(r, g, b)
shape.line.width = Pt(border_width)
# For no border:
shape.line.fill.background()
```

**Images:**
```python
# From local file (e.g., screenshots saved from Figma)
pic = slide.shapes.add_picture(img_path, left, top, width=width, height=height)

# From URL (download first)
response = requests.get(image_url)
pic = slide.shapes.add_picture(BytesIO(response.content), left, top, width=width)
```

**Backgrounds:**
```python
# Solid color
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = RGBColor(r, g, b)

# Image background (full-bleed frame screenshot as fallback)
slide.background.fill.picture('path/to/bg.png')
```

#### 3c. Font Mapping
Figma fonts may not be available on the system. Use this mapping for common substitutions:
- Inter → Inter (usually available) or Helvetica Neue
- Roboto → Roboto or Arial
- SF Pro → SF Pro Display (macOS) or Helvetica Neue
- Montserrat → Montserrat or Arial
- Open Sans → Open Sans or Calibri
- Any custom font → note it in the output and suggest the user install it

#### 3d. Handling Complex Elements
Some Figma elements don't have direct PPTX equivalents:

- **Shadows**: python-pptx has limited shadow support. Note if shadows are present and suggest adding them manually in Keynote.
- **Blur effects**: Not supported. Note for manual addition.
- **Complex gradients**: Limited support. Use solid color approximation or note for manual fix.
- **SVG icons/vectors**: Export as PNG from Figma screenshot and embed as image.
- **Masks/clips**: Not directly supported. Use screenshot crop as fallback.
- **Auto-layout (Flexbox)**: Calculate absolute positions from the metadata rather than trying to replicate layout rules.

### Phase 4: Verification & Refinement

#### 4a. Visual Comparison
After generating the PPTX:
1. Compare each slide against the Figma screenshots captured in Phase 1
2. Note any discrepancies (missing elements, color mismatches, positioning errors)
3. List what looks correct and what needs adjustment

#### 4b. Fidelity Report
Provide a brief report to the user:
- Total slides generated
- Elements successfully recreated vs. elements that need manual touch-up
- Any fonts that may need to be installed
- Suggestions for transitions to add in Keynote (based on the frame flow)

#### 4c. Iterate if Needed
If the user identifies issues:
- Re-extract specific data from Figma MCP
- Adjust the generation script
- Regenerate the PPTX

### Phase 5: Keynote Workflow Guide

After delivering the PPTX, provide the user with next steps:

1. **Open in Keynote**: Double-click the `.pptx` file → opens in Keynote automatically on macOS
2. **Add transitions**: Select slides → Animate panel → choose transitions (Magic Move works great between similar frames)
3. **Set timing**: Adjust slide duration and transition speed
4. **Record talk track**: Play → Record Slideshow → narrate over slides
5. **Export as video**: File → Export To → Movie → choose resolution (1080p or 4K)

## Output

### 1. Generated Files
- **PPTX file**: `temporary/figma-to-pptx/[name].pptx`
- **Generation script**: `temporary/figma-to-pptx/generate.py` (for reproducibility/tweaking)
- **Extracted images**: `temporary/figma-to-pptx/images/` (any images downloaded from Figma)

### 2. Fidelity Report
Summary of:
- Slides generated: [count]
- Elements recreated: [count]
- Manual touch-ups needed: [list]
- Missing fonts: [list]
- Transition suggestions: [list]

## File Management
- **Folder**: `temporary/figma-to-pptx/`
- **Output file**: `temporary/figma-to-pptx/[descriptive-name].pptx`
- **Script**: `temporary/figma-to-pptx/generate.py`
- **Images**: `temporary/figma-to-pptx/images/`

## Important Notes

### What This Command Can Recreate with High Fidelity
- Text (fonts, sizes, colors, weights, alignment)
- Rectangles and basic shapes (fills, borders, rounded corners)
- Images and photos
- Solid and simple gradient backgrounds
- Element positioning and sizing
- Opacity/transparency
- Z-order/layering

### What May Need Manual Touch-Up in Keynote
- Drop shadows and blur effects
- Complex gradients (multi-stop, radial)
- SVG icons (embedded as raster images — may need re-insertion for crisp scaling)
- Mask/clip effects
- Line spacing fine-tuning

### What This Command Does NOT Do
- Add slide transitions (do this in Keynote — it's better there anyway)
- Add animations (do this in Keynote)
- Add audio/talk track (record in Keynote after)
- Export video (Keynote handles this)

## python-pptx Reference
The generation script uses `python-pptx` (installed in `.venv`). Key imports:
```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
```

Run with: `.venv/bin/python temporary/figma-to-pptx/generate.py`
