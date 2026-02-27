# Swimm Visual Guidelines

This document defines the visual style, brand colors, and design principles for Swimm content. Reference this when generating images for blog posts, social media, and other visual content.

## Figma Sources

Brand colors: https://www.figma.com/design/4HBgkNt1z4IPrE3VXYLRGl/Website-library-2022

Blog post images (style reference): https://www.figma.com/design/C88Kft2CG6iavNd29Ofnb9/Blogs-Post-Images

---

## Brand Colors

### Primary Blues (Swimm Core)
- **deep-dive**: #1F35FF - Darkest primary, strong emphasis
- **swimm-blue**: #4154FF - Main brand color
- **coastal-shore**: #5E6EFF - Secondary blue
- **shallow-waters**: #8D98FF - Light blue accent
- **feet-in-water**: #E4E7FF - Very light blue, backgrounds

### Accent Purples
- **wave-jammer**: #C95FFF - Bold purple accent
- **high-violet**: #D177FF - Medium purple
- **wide-awake**: #DE9DFF - Light purple
- **safe-zone**: #EDD9FF - Very light purple

### Accent Yellows
- **duck-mode**: #FDF150 - Bold yellow accent
- **rise-n-shine**: #FFF78E - Medium yellow
- **just-hatched**: #FFFAB6 - Light yellow
- **light-as-feather**: #FFFDE5 - Very light yellow

### Neutrals
- **dark-charcoal**: #1D1E2B - Dark backgrounds, text
- **gravel-rocks**: #2F3142 - Secondary dark
- **high-tide**: #878D95 - Medium gray
- **wash-me**: #F4F6FA - Light backgrounds
- **white**: #FFFFFF - Pure white

### Brand Gradients
- **swimm-shades**: #4154FF → #8D98FF (swimm-blue to shallow-waters)
- **beach-time**: #8D98FF → #E4E7FF → #0E68FF (multi-stop blue)
- **pink-hour**: #8D98FF → #E4E7FF → #DE9DFF (blue to purple)
- **shore-to-shore**: #8D98FF → #E4E7FF → #8D98FF (symmetric blue)
- **night-swimming**: #1D1E2B → #4154FF → #1D1E2B (dark with blue center)

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
- **Background**: dark-charcoal (#1D1E2B) as default
- **Base color within shapes**: swimm-blue (#4154FF) - most used after background
- **Accent colors**: rise-n-shine (#FFF78E), high-violet (#D177FF)
- **Stroke colors**: rise-n-shine (#FFF78E), high-violet (#D177FF)
- **Stroke weight**: 1px for outlines and accents (same as grid)

### Composition Rules
- **Edge-to-edge**: Visuals fill the frame completely, OR
- **Two-thirds**: Composition occupies approximately 2/3 of the canvas with breathing room
- Choose based on the energy of the concept - edge-to-edge for dynamic, 2/3 for balanced

---

## Grid Overlay (Optional)

When using a grid overlay to add depth:
- **Dimensions**: 20 columns x 10 rows
- **Color**: #E8EAFF at 50% opacity
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
- **Color palette**: shallow-waters (#8D98FF), deep-dive (#1F35FF), swimm-blue (#4154FF), rise-n-shine (#FFF78E)

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

- **Position**: Bottom-left corner
- **Color**: White (#FFFFFF)
- **Required on**: All banner images
- **File**: `context/assets/swimm-logo-white.svg`

### Logo Zone (for prompt composition)
The logo will be automatically added by the image generator. **Prompts must account for this space:**

- **Logo size**: 228x69 pixels (at 1920x960 resolution)
- **Position**: 69px from left edge, 56px from bottom edge
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

Imagen and some AI models render hex codes as literal text in images. Explicitly explain that the the values given are hex values not text for the image. 


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
