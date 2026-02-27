# Context Files - Setup Guide

This directory contains the configuration files that define your brand voice, positioning, SEO strategy, and content standards. AI writing agents read these files at runtime to produce content that matches your company's style and strategy.

## What These Files Do

Every file in `context/` is **referenced by agents at runtime**. The section headers and structure are load-bearing - do not rename sections or restructure files without updating the agent configurations that depend on them.

## Files and Their Purpose

| File | Purpose | Priority |
|------|---------|----------|
| `brand-voice.md` | How you write (tone, style, voice) and what you say (positioning, UVPs, messaging) | **1 - Start here** |
| `features.md` | Product features, benefits, competitive differentiators, and conversion messaging | **2 - Second priority** |
| `target-keywords.md` | SEO keyword clusters organized by topic with pillar/cluster/long-tail structure | **3 - Third priority** |
| `internal-links-map.md` | Catalog of pages to link to, organized by topic cluster | **4 - Fourth priority** |
| `writing-examples.md` | 3-5 of your best published articles for voice matching (paste full text) | **5 - Fifth priority** |
| `style-guide.md` | Grammar, formatting, capitalization, and mechanical writing standards | 6 |
| `seo-guidelines.md` | SEO best practices, content length, keyword density, and meta element standards | 7 |
| `competitor-analysis.md` | Competitor landscape, positioning matrix, and content opportunity analysis | 8 |
| `visual-guidelines.md` | Brand colors, design principles, and image generation guidelines | 9 |
| `ceo-voice.md` | CEO/executive LinkedIn voice profile with real writing samples | 10 |

## Recommended Fill-In Order

### Phase 1: Core Identity (Do First)
1. **`brand-voice.md`** - This is the foundation. Everything else builds on your voice and positioning. Replace `[Company Name]` and all Acme Corp examples with your own.
2. **`features.md`** - Your product's features, benefits, and competitive angles. Agents use this for product-aware content.
3. **`target-keywords.md`** - Your SEO keyword strategy. Agents use this to select keywords and build topic clusters.

### Phase 2: Content Infrastructure
4. **`internal-links-map.md`** - Your website's key pages for internal linking. Add real URLs as you publish content.
5. **`writing-examples.md`** - Paste 3-5 of your best published articles. This is critical for voice matching - without examples, content will sound generic.

### Phase 3: Standards and Strategy
6. **`style-guide.md`** - Mostly generic best practices. Customize the product-specific sections.
7. **`seo-guidelines.md`** - Mostly generic SEO best practices. Customize the examples.
8. **`competitor-analysis.md`** - Fill in as you research competitors. Update quarterly.
9. **`visual-guidelines.md`** - Add your brand colors and logo references.
10. **`ceo-voice.md`** - Requires real CEO writing samples. Skip if you don't plan to generate executive LinkedIn content.

## How to Customize

Every file uses HTML comments (`<!-- Instructions: ... -->`) to guide you on what to replace. Look for:

- `[Company Name]` - Replace with your actual company name
- `[FILL IN: ...]` - Sections that need your specific content
- `<!-- Instructions: ... -->` - Detailed guidance on what to change

The Acme Corp examples (a fictional B2B SaaS code review platform) are placeholders showing the expected format and level of detail. Replace them entirely with your own content.

## Important Rules

1. **Keep all section headers** - Agents reference specific headers at runtime. Renaming breaks them.
2. **Keep the file names** - Agent configurations reference these exact filenames.
3. **Don't delete files** - Even if a file is mostly placeholder, agents expect it to exist.
4. **`writing-examples.md` needs real articles** - AI-generated placeholder content provides zero voice-matching value.
5. **`ceo-voice.md` needs real writing samples** - Same reason. Real samples or skip it entirely.

## Other Files

- `assets/` - Brand assets (logos, images) referenced by visual guidelines
- `wordpress-blocks.json` - WordPress Gutenberg block registry (used by publishing workflow)
