# Generate Images Command

Use this command to create brand-compliant images for blog articles and social media.

## Usage
`/generate-images [article-path]`

Example: `/generate-images content/drafts/26Q1-legacy-modernization/article-2026-01-28.md`

## What This Command Does
1. Analyzes article content to understand the topic and key themes
2. Generates 5 banner image variations for user selection
3. User selects winning banner concept
4. Generates matching LinkedIn image based on selected concept
5. Optimizes images for web deployment
6. Saves images with metadata to the article's folder

## Mandatory Outputs
Every run produces:
- **5 Banner variations** (1920x960) - User selects one as final
- **1 LinkedIn image** (1080x1080 square) - Generated after banner selection

---

## Process

### Step 0: Determine Image Output Location

Before generating images, ensure the article has a proper folder structure:

1. **If article is already in a subfolder** (e.g., `content/drafts/26Q1-topic-slug/topic-slug-2026-01-28.md`):
   - Create `images/` subfolder if it doesn't exist: `content/drafts/26Q1-topic-slug/images/`

2. **If article is standalone (legacy)** (e.g., `content/drafts/my-article.md` directly in content/drafts/):
   - Extract slug from filename (e.g., `my-article`)
   - Create folder: `content/drafts/[article-slug]/`
   - **Move the article** into the new folder, preserving filename: `content/drafts/[article-slug]/[article-slug].md`
   - Create `images/` subfolder: `content/drafts/[article-slug]/images/`
   - Inform user: "Moved article to `content/drafts/[article-slug]/` for better organization"

3. **If article is in `content/published/` (standalone)**:
   - Same process: create folder, move article, create `images/`

**Result**: All articles end up in their own folder with an `images/` subfolder, keeping related content organized together.

---

### Step 1: Analyze Article & Generate 5 Banner Variations

**Pre-Generation Review**:
- Read the article content to understand topic, themes, and key concepts
- Review @context/visual-guidelines.md for brand design principles

**Generate 5 Creative Concepts**:
Create 5 diverse banner concepts, each exploring a different abstract representation:
- Vary compositions (edge-to-edge vs 2/3)
- Vary use of optional elements (grid overlay, data viz, text)
- Vary visual metaphors while staying abstract and brand-compliant

**Build prompts dynamically** using visual-guidelines.md principles:
- Describe colors by name (not hex codes)
- Include design principles (flat vector, solid colors, 1px strokes)
- Include what to avoid (no photos, people, blur, shadows)
- Keep concepts abstract and conceptual, not literal
- **Important**: Include "leave bottom-left corner clear for logo placement" in every banner prompt

**Generate all 5 banner images** via `data_sources/modules/image_generator.py`

### Step 2: Present All 5 Banners

Present generated images to user with clickable links:

```
## Generated Banner Variations

5 banner concepts have been generated for "[Article Title]":

### Banner 1: [Concept Title]
**File**: [banner-1-slug-date.png](content/drafts/folder/images/banner-1-slug-date.png)
**Model**: [gemini-3-pro-image-preview or imagen-4.0-generate-001]
**Concept**: [2-3 sentence description of visual approach]
**Elements**: [composition, grid, data viz, text if any]

### Banner 2: [Concept Title]
**File**: [banner-2-slug-date.png](content/drafts/folder/images/banner-2-slug-date.png)
**Model**: [model used]
**Concept**: [2-3 sentence description]
**Elements**: [composition, grid, data viz, text if any]

### Banner 3: [Concept Title]
...

### Banner 4: [Concept Title]
...

### Banner 5: [Concept Title]
...

---

**Select your banner:**
- Type "1" through "5" to select winner
- Type "regenerate 2: [feedback]" to retry a specific concept
- Type "more" to generate 5 new concepts
- Type "combine 1,3" to merge elements from multiple concepts
```

### Step 3: User Selection

Wait for user to select a banner.

**If user selects a number (1-5)**: Mark as winner, proceed to LinkedIn generation
**If user requests regeneration**: Incorporate feedback, regenerate that specific concept
**If user requests "more"**: Generate 5 additional concepts
**If user requests "combine"**: Create new concept merging specified elements

### Step 4: Generate LinkedIn Image

Once banner is selected:

1. **Adapt the winning concept** for square format:
   - Center the composition
   - Ensure it's recognizable at thumbnail sizes
   - Maintain same visual language and color approach

2. **Generate LinkedIn image** (1:1 square)

3. **Present for review**:
```
## LinkedIn Image Generated

Based on your selected banner concept, here's the LinkedIn version:

**File**: [linkedin-slug-date.png](content/drafts/folder/images/linkedin-slug-date.png)
**Model**: [gemini-3-pro-image-preview or imagen-4.0-generate-001]
**Concept**: [How the banner concept was adapted for square format]

---

**Review the LinkedIn image:**
- Type "approve" to proceed to optimization
- Type "regenerate: [feedback]" to try again
```

### Step 5: Optimize for Web

After user approves both images:

1. **Run the optimizer** via `data_sources/modules/image_optimizer.py`:
   ```bash
   .venv/bin/python data_sources/modules/image_optimizer.py --dir [images-folder] --web
   ```

2. **Output files**:
   - `banner_web.webp` - Optimized to 1920x960, ~100-150KB
   - LinkedIn: Use original `linkedin.png` (LinkedIn compresses on upload)

3. **Report results**:
   ```
   ## Optimized Images for Web

   Original files preserved for high-quality use.
   Web-optimized versions created:

   | Image | Original | Optimized | Reduction |
   |-------|----------|-----------|-----------|
   | Banner | 2.5MB | 217KB | 91% |

   **Files ready for use.**
   ```

4. **Save generation log** (`images/generation-log.md`) with:
   - All prompts used for each variation
   - Which model generated each image
   - Final selected images with alt text
   - Feedback sections for learning/improvement

5. **Cleanup**: Optionally remove non-selected banner variations

---

## Output Structure

### File Naming Convention
Files follow the pattern: `[imagetype]-[article-slug]-[YYYY-MM-DD].[ext]`

During generation (5 variations):
- `banner-1-[slug]-[date].png`
- `banner-2-[slug]-[date].png`
- `banner-3-[slug]-[date].png`
- `banner-4-[slug]-[date].png`
- `banner-5-[slug]-[date].png`

Final files:
- `banner-[slug]-[date].png` (selected winner)
- `banner-[slug]-[date]_web.webp`
- `linkedin-[slug]-[date].png`

### File Organization
```
content/drafts/[YYQ#]-[topic-slug]/
├── [topic-slug]-[YYYY-MM-DD].md
├── images/
│   ├── banner-[slug]-[date].png       # Selected banner (high-res)
│   ├── banner-[slug]-[date]_web.webp  # Blog-optimized
│   ├── linkedin-[slug]-[date].png     # LinkedIn (use as-is)
│   └── generation-log.md              # Prompts, models, feedback
└── [other agent outputs...]
```

### Generation Log Format (`images/generation-log.md`)
```markdown
# Image Generation Log

Article: [article filename]
Generated: [YYYY-MM-DD HH:MM]

---

## All Prompts Used

### Banner Variations

#### Banner 1: [Concept Title]
- **Model**: [gemini-3-pro-image-preview / imagen-4.0-generate-001]
- **Selected**: [Yes/No]
- **Prompt**:
```
[Full prompt text used for generation]
```

#### Banner 2: [Concept Title]
- **Model**: [model used]
- **Selected**: [Yes/No]
- **Prompt**:
```
[Full prompt text]
```

[Repeat for all 5 variations]

### LinkedIn Image
- **Model**: [model used]
- **Prompt**:
```
[Full prompt text]
```

---

## Final Selected Images

### Banner
- **File**: banner-[slug]-[date].png
- **Variation**: #[N] of 5
- **Model**: [model used]
- **Alt Text**: [descriptive alt text for accessibility]

### LinkedIn
- **File**: linkedin-[slug]-[date].png
- **Model**: [model used]
- **Alt Text**: [descriptive alt text for accessibility]

---

## Feedback & Learning

### What Worked Well
- [Note successful elements, colors, compositions]

### What Didn't Work
- [Note issues, off-brand elements, model quirks]

### Suggestions for Improvement
- [Ideas for better prompts, different approaches]

### Model Performance
- **Gemini 3 Pro**: [Success/Failed/Timed out] - [notes]
- **Imagen Fallback**: [Used/Not needed] - [notes]
```

---

## Context Files Used
- @context/visual-guidelines.md - Brand design principles, colors, what to avoid

## Requirements
- **GOOGLE_API_KEY**: Required in environment for image generation
- **Python modules**:
  - `data_sources/modules/image_generator.py` - Image generation
  - `data_sources/modules/image_optimizer.py` - Web optimization (requires Pillow)

---

## Quality Standards

### Brand Compliance
- Images must follow design principles in visual-guidelines.md
- Style: flat vector, solid colors, abstract representations
- No photos, people, blur, shadows, or complex compositions

### Technical Requirements

**Source files** (high-res):
- Banner: 2816x1536 pixels (16:9, 2K) - PNG, ~2-3MB
- LinkedIn: 2048x2048 pixels (1:1, 2K) - PNG, ~2-3MB

**Web-optimized files**:
- Banner: 1920x960 pixels - WebP 85% quality, ~100-150KB

**Social media**:
- LinkedIn: Upload original PNG directly - LinkedIn compresses on their end

### Accessibility
- Every image must have descriptive alt text
- Alt text should describe visual content, not start with "Image of"
- Alt text should be under 125 characters when possible

---

## Error Handling

### If generation fails:
- Report the error clearly
- Suggest checking API key configuration
- Offer to retry

### If generation is off-brand:
- User can provide feedback for regeneration
- Iterate until satisfactory

### If article path invalid:
- Report file not found
- Suggest checking the path

---

## Tips for Better Results

1. **Be specific in feedback**: "Make the shapes more geometric" is better than "I don't like it"
2. **Reference the guidelines**: If something is off-brand, mention which principle it violates
3. **Iterate thoughtfully**: Usually 1-2 regenerations with good feedback produce great results
4. **Review all 5 variations**: Sometimes unexpected concepts work best
