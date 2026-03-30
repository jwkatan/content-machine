# Listicle Refresh Brief

Supplementary rewrite instructions for listicle articles. Use alongside the `/analyze-existing` report — if any SEO-specific recommendation in the analysis report conflicts with this brief, the analysis report takes precedence.

## Background

A January 2026 Google update penalizes low-quality listicles on sites where listicles exceed 10% of the learning center. Swimm is at 15%+ with a -49.47% traffic impact. Sites that grew through this update share the patterns below. Sites that dropped had thin listicles with minimal context beyond the list itself.

## Requirements

### 1. Add Supplementary Content (target ~50% of page)

The article must not be just a list. Roughly half the page should be educational content that stands on its own — helping the reader understand the space, not just scan tool names.

**Before the list, add sections covering:**
- What the problem space is and why it matters to the reader
- Key evaluation criteria — what actually differentiates tools in this category
- A decision framework: how to match a tool to your situation

**After the list, add:**
- Summary comparison or decision guide
- FAQ section if natural questions exist

**"Substantial" means high-quality, not high word-count.** Every sentence must teach the reader something useful or help them make a decision. Do not pad with generic definitions, obvious statements, or restated points. If a section doesn't add genuine insight, cut it. A tighter 300-word intro that gives the reader a real framework beats a 600-word intro that repeats itself.

**Content neutrality in general sections.** All content outside of the Swimm product entry itself must be relevant to the article's topic, not to Swimm's specific positioning. Introductions, evaluation criteria, category intros, FAQs, and conclusions should cover the full breadth of the topic (e.g. all tool categories on a tools article) rather than funneling through Swimm's value proposition. It is fine to mention use cases that Swimm addresses (like application understanding or modernization) alongside other use cases (compilation, IDEs, code quality), but not to frame the entire article around them. The content should not introduce concepts that contradict Swimm's product, but it should read as genuinely educational rather than as marketing content with a list attached. Save Swimm-specific language for the Swimm entry and the closing CTA.

### 2. Categorize the List

Do NOT present tools as a flat numbered list. Group them into meaningful categories based on how the reader actually makes decisions.

**Good categorization examples:**
- By use case: "Best for Enterprise Teams", "Best for Startups"
- By approach: "AI-Powered", "Traditional Platforms", "Open Source"
- By capability: "All-in-One Platforms", "Specialized Tools"

Each category gets a brief intro sentence explaining what unifies the tools in it.

### 3. Update Each List Entry

For every company/tool in the list:

- **Verify it still exists and is active** — remove dead products, add notable new entrants. The list count does not need to stay the same as the original; add new products that have become relevant since the last publish (e.g. new market entrants, products that gained traction in the past year) and remove ones that are no longer active or relevant.
- **Update description** to reflect current product state
- **Key features**: 3-5 bullet points of actual differentiating features
- **Image**: Add a placeholder `[IMAGE: {company-name} product screenshot or logo]` where an image should go. Do not fabricate image URLs.
- **"Best for" statement**: One line on who this tool serves best
- **Link**: Verify the product URL still works
- **Source attribution**: Add `Source: [Company Name](product-page-url)` under the screenshot image, not under the description. The link should point to the company's product page (or the company homepage if only one product). Only one source line per product entry. If there is no screenshot, it is fine to omit the source line rather than placing it elsewhere.
- **No pros/cons or limitations sections** — sites that grew did NOT include these. Focus on what the tool does and who it's for.

### 4. Source Information Only from the Primary Product Page

For each product in the listicle, the **single source of truth** is the product's primary product page (the main marketing/product page on the vendor's website). No other pages — not docs, not blog posts, not pricing pages, not changelogs — should be used for feature claims.

#### Research File Requirement

Before writing any product entry, create a `research.md` file for that product inside the article's working directory (e.g., `drafts/topic/research/product-name.md`). Each research file must contain:

1. **Product page URL** — the exact URL of the primary product page used as the source
2. **Date accessed** — the date the page was visited (e.g., "Accessed: 2026-02-18")
3. **Features list** — every feature claimed in the listicle entry, with:
   - The **exact language** used on the product page to describe the feature
   - The **location on the page** where the language appears (e.g., "hero section", "second feature block", "under the heading 'Key Capabilities'", "in the bullet list below the fold")
4. **Product image** — note whether a usable product image (screenshot, product UI visual, or hero image) exists on that page. If yes, record the image URL or describe its location. If no suitable product image exists on the page, note that and fall back to the `[IMAGE: ...]` placeholder.

**Example `research.md` entry:**

```markdown
# Acme Tool

**Source page:** https://acme.com/product
**Accessed:** 2026-02-18

## Features

1. **AI-powered code review**
   - Page language: "Automated code review powered by AI that catches bugs before they ship"
   - Location: Hero section, main headline and subheadline

2. **Real-time collaboration**
   - Page language: "Collaborate with your team in real-time with shared editing sessions"
   - Location: Second feature block, under the heading "Built for Teams"

3. **GitHub and GitLab integration**
   - Page language: "Native integrations with GitHub, GitLab, and Bitbucket"
   - Location: Integrations section, bullet list

## Product Image

- Usable image found: Yes
- Description: Product UI screenshot showing the code review dashboard
- Location on page: Hero section, right side
```

#### Sourcing Rules

- **ONLY features visible on the primary product page may be included in the listicle entry.** If a feature is not mentioned on that page, it does not go in the article — even if you know the product has it from other sources.
- The product page URL becomes the **source link** at the bottom of each listicle entry (the `Source: [Company Name](url)` line).
- **For the product image**: first check whether the product page contains a product screenshot, UI visual, or hero image suitable for representing the tool. If yes, use it (or note it for image sourcing). If no suitable image exists on the page, use the `[IMAGE: ...]` placeholder.
- **Do NOT use** third-party reviews, comparison sites, blog roundups, G2/Capterra/TrustRadius reviews, documentation sites, or other secondary sources for product descriptions or feature claims.
- Third-party sources (industry reports, analyst research) are acceptable for discovering which tools exist in a space, but all product details must be verified against the vendor's primary product page before including them.

### 5. Accuracy Verification

After the rewrite is complete, run `/review-content` on the finished article. Listicle refreshes are high-risk for inaccurate claims because:
- Tool features change frequently — descriptions may be outdated
- Pricing and plans shift without notice
- Marketing claims from vendor sites should not be restated as fact without context
- New entrants may have been missed; removed products may still be listed

The `/review-content` pass should cross-reference each product entry against its `research.md` file to confirm that every feature claim traces back to exact language on the product page.

The `/review-content` pass must complete before the article is considered done.

## Checklist

Each list entry:
- [ ] `research.md` file created with source page URL, date accessed, exact feature language, and page locations
- [ ] Verified as current and active
- [ ] Description and features sourced exclusively from the primary product page
- [ ] 3-5 differentiating feature bullets (each traceable to `research.md`)
- [ ] Product image sourced from the product page, or `[IMAGE: ...]` placeholder if none available
- [ ] "Best for" positioning statement
- [ ] Source link points to the primary product page used in research
- [ ] Source attribution with company name linked to product page

Overall article:
- [ ] Supplementary content is ~50% of total page (quality, not filler)
- [ ] List is divided into categories (not flat)
- [ ] Updated for 2026 (no stale year references)
- [ ] `/review-content` pass completed
- [ ] Meets SEO requirements (per `/analyze-existing` report)

## What NOT to Do

- Do NOT add pros/cons or limitations sections
- Do NOT keep a flat numbered list
- Do NOT write thin entries (1-2 sentences per tool)
- Do NOT pad supplementary content with filler to hit a word count
- Do NOT fabricate image URLs — use placeholders
- Do NOT source product descriptions or features from anywhere other than the primary product page
- Do NOT include features you know a product has if they are not on the primary product page
- Do NOT write a product entry without first completing its `research.md` file
- Do NOT restate vendor marketing claims as fact without context
- Do NOT add "Related content: Read our guide to..." links within individual tool entries — these are added by the internal linker agent separately and should not appear inline in the listicle body

## Usage

```
/rewrite [url or file] follow supplementary instructions in @context/listicle-refresh-brief.md
```

Delete this file when all listicle refreshes are complete.
