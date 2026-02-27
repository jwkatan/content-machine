# [Company Name] Visual Guidelines

<!-- Instructions: Replace ALL color values, Figma URLs, and logo references with your own brand assets. Keep the structure and design principle sections intact — agents reference these when generating images. -->

This document defines the visual style, brand colors, and design principles for [Company Name] content. Reference this when generating images for blog posts, social media, and other visual content.

## Brand Asset Sources

<!-- Instructions: Replace these links with your actual brand library locations. -->

Brand colors: [Link to your brand library or style guide]

Blog post images (style reference): [Link to your design templates or Figma file]

---

## Brand Colors

<!-- Instructions: Replace ALL hex values and color names with your brand colors. Keep the category structure (Primary, Accent, Neutrals, Gradients). -->

### Primary Colors
| Name | Hex | Usage |
|------|-----|-------|
| [primary-dark] | #[XXXXXX] | Darkest primary, strong emphasis |
| [primary-main] | #[XXXXXX] | Main brand color |
| [primary-medium] | #[XXXXXX] | Secondary shade |
| [primary-light] | #[XXXXXX] | Light accent |
| [primary-bg] | #[XXXXXX] | Very light, backgrounds |

### Accent Colors
| Name | Hex | Usage |
|------|-----|-------|
| [accent-bold] | #[XXXXXX] | Bold accent |
| [accent-medium] | #[XXXXXX] | Medium accent |
| [accent-light] | #[XXXXXX] | Light accent |
| [accent-bg] | #[XXXXXX] | Very light accent |

### Secondary Accent Colors (Optional)
| Name | Hex | Usage |
|------|-----|-------|
| [secondary-bold] | #[XXXXXX] | Bold secondary accent |
| [secondary-medium] | #[XXXXXX] | Medium secondary |
| [secondary-light] | #[XXXXXX] | Light secondary |
| [secondary-bg] | #[XXXXXX] | Very light secondary |

### Neutrals
| Name | Hex | Usage |
|------|-----|-------|
| [dark-bg] | #[XXXXXX] | Dark backgrounds, text |
| [dark-secondary] | #[XXXXXX] | Secondary dark |
| [mid-gray] | #[XXXXXX] | Medium gray |
| [light-bg] | #[XXXXXX] | Light backgrounds |
| white | #FFFFFF | Pure white |

### Brand Gradients (Optional)
<!-- Instructions: Define any gradient combinations used in your brand. -->
- [gradient-name-1]: #[XXXXXX] to #[XXXXXX] (description of usage)
- [gradient-name-2]: #[XXXXXX] to #[XXXXXX] (description of usage)

---

## Design Principles

### Core Philosophy
Blog header images should convey **abstract relatability** to the subject matter - conceptual rather than literal representations.

### Style Fundamentals
- **Flat vector shapes**: Clean, geometric forms without 3D effects
- **Solid colors**: Avoid patterns; gradients used sparingly and only when intentional
- **No harsh lighting**: Even, flat illumination
- **Minimalist complexity**: Simple compositions that communicate clearly

### Color Application
<!-- Instructions: Map your brand colors to these usage categories. -->
- **Background**: [dark-bg] (#[XXXXXX]) as default
- **Base color within shapes**: [primary-main] (#[XXXXXX]) - most used after background
- **Accent colors**: [accent-medium] (#[XXXXXX]), [secondary-medium] (#[XXXXXX])
- **Stroke colors**: [accent-medium] (#[XXXXXX]), [secondary-medium] (#[XXXXXX])
- **Stroke weight**: 1px for outlines and accents

### Composition Rules
- **Edge-to-edge**: Visuals fill the frame completely, OR
- **Two-thirds**: Composition occupies approximately 2/3 of the canvas with breathing room
- Choose based on the energy of the concept - edge-to-edge for dynamic, 2/3 for balanced

---

## Grid Overlay (Optional)

When using a grid overlay to add depth:
- **Dimensions**: 20 columns x 10 rows
- **Color**: [light color] at 50% opacity
- **Coverage**: Edge to edge (always full-bleed when used)
- **Line weight**: 1px

The grid is optional - use when it adds visual interest or grounds the composition.

---

## Abstract Data Visualization

When incorporating charts or graphs for data-related topics:

### Approved Chart Types
- Abstract pie charts
- Simple bar graphs
- Line graphs/trends
- Circular/radial representations

### Data Viz Rules
- **No axes**: Charts are purely visual
- **No titles**: No chart titles or headers
- **No labels**: No series labels or data point labels
- **Color palette**: Use your primary and accent colors

Charts are decorative and conceptual - they suggest data/analytics without presenting actual information.

---

## Typography on Images

### Default Behavior
**No text on images by default.**

### When Text is Appropriate
- Series titles (e.g., "Part 1", "Part 2")
- Section identifiers (e.g., "Deep Dive", "Guide")
- Short conceptual labels that enhance meaning

### Text Style Rules
- **Font**: Clean sans-serif (no ornate or stylized fonts)
- **Color**: White (#FFFFFF) or brand colors with high contrast
- **Integration**: Text should feel designed into the composition, not overlaid
- **Avoid**: Full article titles (unless specifically requested), taglines, descriptions

---

## Logo Placement

<!-- Instructions: Update the logo file reference. The LOGO_FILENAME environment variable in your .env file controls which logo file is used. -->

- **Position**: Bottom-left corner
- **Color**: White (#FFFFFF)
- **Required on**: All banner images
- **File**: `context/assets/${LOGO_FILENAME}`

### Logo Zone (for prompt composition)
The logo will be automatically added by the image generator. **Prompts must account for this space:**

- **Logo size**: [Width]x[Height] pixels (at 1920x960 resolution)
- **Position**: [X]px from left edge, [Y]px from bottom edge
- **Clear zone**: Bottom-left ~300x130 pixels to give breathing room
- **In prompts**: Explicitly state "leave bottom-left corner clear for logo placement"
- **Composition tip**: Avoid placing key visual elements in the bottom-left quadrant

---

## What to Avoid

### Visual Anti-Patterns
- **Photorealistic imagery**: Never use photos or photorealistic renders
- **Images of people**: No human figures, faces, or silhouettes
- **Harsh lighting**: No dramatic shadows or lighting effects
- **Overly complex compositions**: Keep element count low
- **Gaussian blur**: No soft blurs or bokeh effects
- **Drop shadows**: No shadows on elements
- **Patterns**: No repeating patterns or textures

### Specific Prohibitions
- Literal representations of concepts (actual code screenshots, literal office scenes)
- Stock photo aesthetics (handshakes, sticky notes, people pointing at screens)
- Matrix-style code rain or floating holograms
- Heavy gradients that dominate the composition
- Cartoonish or playful illustrations (maintain enterprise professionalism)
- Skeuomorphic design elements

### Brand Safety
- No imagery that could be misinterpreted negatively
- No representations of specific people without consent
- No copyrighted characters, logos, or trademarked imagery
- No imagery that excludes or stereotypes any group

---

## Prompt Construction Notes

When constructing prompts for image generation:

### Color References

Some AI image models render hex codes as literal text in images. Explicitly explain that the values given are hex values not text for the image.

### Prompt Approach
Let prompts be constructed dynamically from:
1. The article's core concept (abstract, not literal)
2. These design principles
3. Creative interpretation of how shapes/composition can represent the topic

---

## Output Specifications

### File Formats
- **Banner**: PNG, 1920x960px (16:9)
- **LinkedIn**: PNG, 1080x1080px (1:1 square)
- **Diagrams**: PNG or SVG if vector output available
