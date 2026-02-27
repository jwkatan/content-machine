# Content Machine Onboarding

Guide a new user through setting up Content Machine for their company.

## Process

1. **Check Python environment**: Verify `.venv` exists. If not, guide the user through creating it:
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

2. **Check environment file**: Verify `data_sources/config/.env` exists. If not, copy from `.env.example` and help the user fill in the required values:
   - `COMPANY_NAME` -- their company name
   - `COMPANY_DOMAIN` -- their website domain
   - `LOGO_FILENAME` -- their logo filename (for PDF/slide generation)

   Ask for all required values in a single prompt. Do not ask for optional integrations unless the user volunteers them.

3. **Walk through context files**: For each file in `context/`, in priority order:
   - `brand-voice.md` -- Voice pillars, tone, messaging. **Critical for quality output.**
   - `writing-examples.md` -- 3-5 exemplary blog posts. **How Claude learns your style.**
   - `features.md` -- Product/service features and benefits.
   - `internal-links-map.md` -- Key pages for internal linking.
   - `style-guide.md` -- Grammar, capitalization, formatting.
   - `target-keywords.md` -- Keyword research by topic cluster.
   - `competitor-analysis.md` -- Competitive intelligence.
   - `visual-guidelines.md` -- Brand colors for image generation.
   - `ceo-voice.md` -- CEO writing samples for LinkedIn.

   For each file:
   1. Read the current template content
   2. Explain what it needs in one sentence
   3. Ask if they want to fill it in now or skip for later
   4. If they want to fill it in, help them populate it based on their input

4. **Quick verification**: Check that `.env` has the required core variables set and at least `brand-voice.md` is not all placeholder content.

5. **Suggest first article**: Recommend running `/write [topic]` with a topic relevant to their business to test the system end-to-end.

## Important Notes

- Do not modify files in `.claude/commands/`, `.claude/agents/`, or `data_sources/modules/`.
- Context files in `context/` are safe to edit during onboarding -- that is the whole point.
- Optional integrations (WordPress, analytics, Slack, etc.) can be set up later. Point users to `ONBOARDING.md` for detailed instructions.
- If the user provides a URL to their website, offer to analyze it to help populate context files.
