# LinkedIn Command

Manage LinkedIn content workflow: generate ideas, create posts, and send to Slack for CEO review.

## Usage

```
/linkedin                           # Dashboard: show pending ideas
/linkedin post [idea-file]          # Create post from idea, send to Slack
/linkedin ideas                     # Generate trending ideas from RSS feeds
/linkedin ideas "[url or summary]"  # Create idea from external content
```

## Subcommands

### Dashboard (no arguments)

Show pending LinkedIn ideas:

```
/linkedin
```

**Output format:**
```
## LinkedIn Dashboard

### Ideas (X pending in content/topics/linkedin/ideas/)
1. [ceo] ai-coding-costs-2026-01-29.md - "AI coding costs are rising"
2. [company] legacy-modernization-trends-2026-01-29.md - "Legacy modernization trends"
3. [ceo] developer-productivity-2026-01-28.md - "Why developer productivity metrics fail"

### Quick Actions
- Pick one: /linkedin post content/topics/linkedin/ideas/[filename].md
- Generate more: /linkedin ideas
- Create manual: /linkedin ideas "Your idea summary here"

### Recently Published (last 5)
[List from content/topics/linkedin/published/]
```

---

### Post (`/linkedin post [file]`)

Generate 4 LinkedIn post variations from an idea file and send selected options to Slack for CEO review.

```
/linkedin post content/topics/linkedin/ideas/ai-coding-costs-2026-01-29.md
```

**Process:**

1. **Read idea file** and extract:
   - `type:` (company or ceo) - determines voice
   - Core insight and angle
   - Source/origin information

2. **Determine voice mode**:
   - If `type: company` - Load ONLY `@context/brand-voice.md`
   - If `type: ceo` - Load ONLY `@context/ceo-voice.md`
   - If `type: undecided` - Ask user before proceeding

3. **Generate 4 post variations**, each with a distinct angle or hook:
   - Apply loaded voice context
   - Follow hook framework and structure
   - Each variation should take a different approach (e.g., different metaphor, different opening, different framing)
   - Give each variation a short descriptive label (e.g., "Two Clocks", "The Quiet Phase")
   - Target character count by voice:
     - CEO posts: 500-700 characters (per ceo-voice.md)
     - Company posts: 900-1200 characters

4. **Run content scrubber** on all 4 via `data_sources/modules/content_scrubber.py`:
   - Remove AI watermarks (zero-width spaces, em-dashes)
   - Clean invisible Unicode characters

5. **Present all 4 options** with labels and character counts:
   - Display each variation in a code block for easy reading
   - Show character count for each
   - Allow user to iterate on any option before proceeding

6. **Ask which to send to Slack**:
   - Options: **All** (send all 4 for CEO to pick), **Select** (choose specific ones), **None** (skip Slack)
   - Default suggestion: send all for CEO selection

7. **Send selected options to Slack** via `data_sources/modules/slack_notifier.py`:
   - Each option sent as a separate Slack message with its label and character count
   - Format: `*Option N - [Label] (XXX chars):*` followed by post content

8. **Update idea file** with all generated content:
   - Add `## LinkedIn Post - Option N: "[Label]"` sections (each in a code block)
   - Add `posted_to_slack: YYYY-MM-DD` to frontmatter with note on how many sent

9. **Confirm to user**:
   ```
   Posted N options to Slack (#linkedin-content)

   File: content/topics/linkedin/ideas/ai-coding-costs-2026-01-29.md
   Type: CEO post

   After CEO picks one:
   - Used it: mv content/topics/linkedin/ideas/[file] content/topics/linkedin/published/
   - Didn't use: mv content/topics/linkedin/ideas/[file] content/topics/linkedin/discarded/
   ```

---

### Ideas - Generate from RSS (`/linkedin ideas`)

Fetch trending topics from RSS feeds, read full articles, and present curated candidates.

```
/linkedin ideas
```

**Process:**

1. **Fetch RSS feeds** via `data_sources/modules/rss_aggregator.py`:
   - Planet Mainframe, TechChannel, IT Jungle (mainframe/legacy)
   - Finextra (BFSI), CIO.com, ComputerWeekly (enterprise IT)
   - The Register, The New Stack, InfoQ, Pragmatic Engineer (tech)

2. **Apply exclusion filters only** (NOT keyword scoring):
   - Remove: webinars, sponsored content, vendor announcements
   - Remove: non-English content, product launches
   - Keep: all other articles from trusted feeds

3. **Select ~12 candidates for deep review**:
   - Take 1-2 most recent articles from each feed
   - Trust feed curation over keyword matching
   - Goal: diverse coverage across sources

4. **Fetch full articles in parallel** (WebFetch all 12):
   - CRITICAL: Read actual content before judging
   - Don't rely on titles - boring titles often hide best content
   - Extract: key data points, quotes, claims, unique angles

5. **AI curates based on actual article content**:
   - Evaluate each article for:
     - Hard data or specific quotes (not just opinions)
     - [Company] angle potential ([your company's relevant perspective])
     - LinkedIn engagement potential (contrarian, surprising, practical)
   - Select ONLY genuinely interesting ones (may be 3, 4, or 5)
   - REJECT articles that are: fluff, recaps, predictions without data, generic advice

6. **Present curated candidates with informed angles**:
   | # | Title | Source | Why This Works for [Company] |

   Each angle must reference ACTUAL article content:
   - BAD: "CEO: Personal take opportunity" (generic)
   - GOOD: "69% now cite skills > cybersecurity (first time in 9 years) - [Company] angle: [your company's relevant perspective on why this matters]"

7. **User selects which to create** (e.g., "1, 3, 4")

8. **Create idea files for selected** in `content/topics/linkedin/ideas/`:
   - Filename: `[slug]-YYYY-MM-DD.md`
   - Frontmatter: type, source, origin URL, relevance score
   - Core insight: specific data/quotes from article
   - Angle: concrete company positioning based on content

9. **Report results**:
   ```
   Created 4 LinkedIn idea files:

   1. skills-gap-fortra-survey-2026-01-29.md
      "69% cite skills as top concern - dethroned cybersecurity"
      Type: Company (data-driven insight)

   2. ai-mainframe-governance-2026-01-29.md
      "Early productivity without understanding" - governance gap
      Type: CEO (contrarian take)

   [...]

   Next: /linkedin post content/topics/linkedin/ideas/[filename].md
   ```

**Why this approach:**
- Keyword scoring failed: "IBM i Skills Supplant Cybersecurity" scored 0.20 but had best data
- Title-judging failed: "generic" titles often hide substantive content
- Reading before judging catches: boring title + great data, generic title + perfect quote
- Parallel fetching: 12 articles ≈ same time as 4 (runs simultaneously)

---

### Ideas - From URL/Summary (`/linkedin ideas "[content]"`)

Create a single idea file from external content or a summary.

```
/linkedin ideas "https://news.ycombinator.com/item?id=12345"
/linkedin ideas "Summary: AI coding assistants are changing onboarding..."
```

**Process:**

1. **Determine input type**:
   - If starts with `http`: Fetch URL content via WebFetch
   - Otherwise: Treat as manual summary

2. **Extract key points**:
   - Main topic/claim
   - Why it matters to your company's audience
   - Potential angles (contrarian, data-driven, personal experience)

3. **Create idea file** in `content/topics/linkedin/ideas/`:
   - Filename: `[slug]-YYYY-MM-DD.md`
   - Source: `trending` (if URL) or `user` (if summary)
   - Include origin URL if applicable

4. **Report result**:
   ```
   Created idea: content/topics/linkedin/ideas/ai-coding-onboarding-2026-01-29.md

   Review: Read content/topics/linkedin/ideas/ai-coding-onboarding-2026-01-29.md
   Create post: /linkedin post content/topics/linkedin/ideas/ai-coding-onboarding-2026-01-29.md
   ```

---

## Idea File Template

When creating idea files, use this format:

```markdown
---
type: company | ceo | undecided
source: user | content | trending
created: YYYY-MM-DD
origin: "[URL or 'manual']"
---

# [Idea Title]

## Core Insight
[1-2 sentences: What's the key point?]

## Why It Matters
[1 sentence: Why does our audience care?]

## Angle (optional)
[How we'd spin this - contrarian take, personal story, data point, etc.]
```

---

## Post File Format (After Generation)

After `/linkedin post`, the idea file expands with all 4 variations:

```markdown
---
type: company | ceo
source: user | content | trending
created: YYYY-MM-DD
origin: "Hacker News"
posted_to_slack: YYYY-MM-DD (4 options for CEO selection)
---

# [Title]

## Core Insight
[Original insight]

## Why It Matters
[Original]

## Angle
[Original or updated]

---

## LinkedIn Post - Option 1: "[Label]" (XXX chars)

` ` `
[Generated post content]
` ` `

## LinkedIn Post - Option 2: "[Label]" (XXX chars)

` ` `
[Generated post content]
` ` `

## LinkedIn Post - Option 3: "[Label]" (XXX chars)

` ` `
[Generated post content]
` ` `

## LinkedIn Post - Option 4: "[Label]" (XXX chars)

` ` `
[Generated post content]
` ` `
```

---

## Context Files Referenced

- `@context/brand-voice.md` - For company posts
- `@context/ceo-voice.md` - For CEO posts

## Modules Used

- `data_sources/modules/content_scrubber.py` - Remove AI watermarks
- `data_sources/modules/rss_aggregator.py` - Fetch trending topics
- `data_sources/modules/slack_notifier.py` - Send to Slack

## Environment Variables

Required in `data_sources/config/.env`:
```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ
```

**Note:** The .env file is located at `data_sources/config/.env`, not in the project root.

---

## Quality Standards

### Content Quality
- 4 variations generated per idea, each with a distinct angle/hook
- Posts scrubbed of AI watermarks before sending
- Voice matches selected context (no blending)
- Character targets: CEO 500-700, Company 900-1200
- Mobile-friendly formatting with line breaks

### Workflow
- Human in loop: CEO reviews in Slack before posting
- Simple tracking: Move files to `content/published/` or `discarded/`
- No auto-posting: Prepared text for manual LinkedIn entry
