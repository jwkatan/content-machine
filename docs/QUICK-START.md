# Quick Start Guide

Get Content Machine running in **10 minutes** ⚡

## Step 1: Install Dependencies (2 min)

```bash
# Install Python dependencies for analysis modules
pip install -r requirements.txt
```

## Step 2: Configure Context Files (5 min)

Fill out these **3 essential files** with your company info:

### 1. Brand Voice (`context/brand-voice.md`)
- Define 3-5 voice pillars
- Add tone guidelines
- Include do's and don'ts

**Tip**: Check your existing brand materials for inspiration

### 2. Features (`context/features.md`)
- List your product/service features
- Add value propositions
- Include key differentiators

### 3. Writing Examples (`context/writing-examples.md`)
- Copy/paste 3-5 of your best blog posts
- Include full content (not just excerpts)
- Note what makes each example great

**Optional but recommended**:
- `internal-links-map.md` - Map your key pages
- `target-keywords.md` - Add keyword research

## Step 3: Create Your First Article (3 min)

```bash
# Open in Claude Code
claude-code .

# Research a topic
/research [your topic]

# Review the research brief in /research/ directory

# Write the article
/write [your topic]

# Check /drafts/ for your article + optimization reports
```

## That's It! 🎉

You now have:
- ✅ A comprehensive, SEO-optimized article (2000+ words)
- ✅ Meta elements (title, description, keywords)
- ✅ SEO optimization report
- ✅ Internal linking suggestions
- ✅ Keyword analysis

## Next Steps

**To publish:**
1. Review the article in `/drafts/`
2. Make any final edits
3. Copy to your CMS
4. Publish and watch it rank!

**To improve quality:**
- Add more writing examples to `context/writing-examples.md`
- Refine your brand voice in `context/brand-voice.md`
- Map more internal links in `context/internal-links-map.md`

## Common Commands

```bash
/research [topic]           # Research before writing
/write [topic]              # Create new article
/analyze-existing [URL]     # Analyze existing post
/rewrite [topic]            # Update old content
/optimize [file]            # Final SEO polish
```

## Need Help?

- 📖 **Full Documentation**: See README.md
- **Full Documentation**: See ONBOARDING.md for detailed setup
- 🐛 **Issues**: https://github.com/[your-username]/content-machine/issues

---

**Pro Tip**: The quality of your output depends on the quality of your context files. Spend time filling them out thoroughly!
