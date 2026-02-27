# Performance Review Command

Use this command to analyze content performance data and generate a prioritized queue of content tasks.

## Usage
`/performance-review [days]`

## What This Command Does
1. Fetches data from Google Analytics, Google Search Console, and DataForSEO
2. Analyzes performance trends and opportunities
3. Identifies quick wins, declining content, and growth opportunities
4. Scores and prioritizes all opportunities by ROI
5. Creates actionable task queue with specific next steps
6. Generates comprehensive performance report

## Process

### Data Collection
- **Google Analytics 4**: Traffic, engagement, conversions, and trends
- **Google Search Console**: Rankings, impressions, clicks, CTR by page and keyword
- **DataForSEO**: Competitive rankings, SERP features, keyword metrics

### Focus Topics Filter

The report automatically prioritizes content related to strategic topic areas:

**Focus Topics (Full Detailed Analysis):**
- Mainframe & mainframe modernization
- COBOL programming
- Application understanding/comprehension
- AI forward engineering
- Reverse engineering
- Legacy systems & code migration
- Code comprehension & codebase analysis

**Other Topics (Condensed Summary):**
All other /learn content appears in a condensed summary table at the end of the report. This allows quality control to catch items that might be miscategorized due to keyword matching.

**Modifying Focus Topics:**
To update which topics receive full analysis, edit `FOCUS_TOPIC_KEYWORDS` in `data_sources/modules/data_aggregator.py`.

### Opportunity Identification
The Performance Agent automatically identifies:

**Quick Wins** (Highest Priority):
- Keywords ranking positions 11-20 (page 2)
- Closest to page 1 with smallest optimization effort
- Calculated opportunity score based on impressions and position

**Declining Content**:
- Pages losing traffic month-over-month
- Identifies severity and potential causes
- Prioritizes by traffic volume at risk

**Low CTR Opportunities**:
- Pages with high impressions but low click-through rates
- Meta title/description improvements needed
- Calculates potential click gains

**Trending Topics**:
- Queries showing rising search volume
- Early mover advantage opportunities
- Content gaps in growing areas

**Competitor Gaps**:
- Keywords competitors rank for but your company doesn't
- Strategic positioning opportunities
- Estimated traffic potential

### Scoring & Prioritization
Each opportunity receives a score (0-100) based on:
- **Impact** (50%): Potential traffic gain, conversion value, strategic importance
- **Effort** (30%): Time required, difficulty, resources needed
- **Confidence** (20%): Data quality, historical success rate, trend stability

### Report Generation
Creates comprehensive report with:
- Executive summary of performance
- Priority queue (urgent/high/medium)
- Detailed opportunity analysis
- Content health dashboard
- Keyword portfolio status
- Resource allocation recommendations
- Week-by-week implementation roadmap

## Prerequisites

### 1. Configure Data Sources
Before first use, set up API credentials in `data_sources/config/.env`:

```bash
# Copy example config
cp data_sources/config/.env.example data_sources/config/.env

# Edit with your credentials
nano data_sources/config/.env
```

Required credentials:
- Google Analytics 4 property ID and service account JSON
- Google Search Console site URL and credentials
- DataForSEO API login and password

See `data_sources/README.md` for detailed setup instructions.

### 2. Install Python Dependencies
```bash
pip install -r data_sources/requirements.txt
```

### 3. Test Data Connections
```bash
python data_sources/modules/google_analytics.py
python data_sources/modules/google_search_console.py
python data_sources/modules/dataforseo.py
```

## Output

Provides a multi-section performance report:

### 1. Executive Summary
```
Report Date: 2025-10-15
Analysis Period: Last 30 days

Overall Performance:
- Total Pageviews: 125,400
- Total Clicks (GSC): 45,200
- Average Position: 12.3
- Total Keywords Ranking: 3,847

Key Trends:
- Organic traffic up 8% vs. previous period
- 7 articles showing significant decline
- 23 keywords moved to page 2 (quick win opportunities)
```

### 2. Priority Queue
```
🔥 URGENT (Do This Week)

1. Optimize for "podcast analytics dashboard"
   Type: Quick Win
   Current Position: 12
   Monthly Impressions: 5,400
   Potential Impact: Move to position 7, gain +450 clicks/month
   Estimated Effort: 3 hours
   Action: Update content, improve internal linking, refresh meta

   Opportunity Score: 87/100
```

### 3. Detailed Analysis
- Quick Win Opportunities table
- Declining Content analysis
- Low CTR pages with meta recommendations
- Trending topics to target
- Competitor gap analysis

### 4. Implementation Roadmap
Week-by-week task breakdown with specific actions

### 5. Success Metrics
Goals and measurement criteria for next review period

## File Management
After generating the report, automatically saves to:
- **File Location**: `content/research/performance-review-[YYYY-MM-DD].md`
- **File Format**: Markdown with tables, metrics, and action items
- **Naming Convention**: `performance-review-` + ISO date

Example: `content/research/performance-review-2025-10-15.md`

## Integration with Other Commands

The Performance Agent output directly informs other commands:

**From Performance Review → Next Actions**:

1. **Quick Win Identified**: "podcast monetization" at position 13
   ```
   /analyze-existing /blog/podcast-monetization-guide
   /optimize content/drafts/podcast-monetization-guide.md
   ```

2. **Declining Content**: Article lost 35% traffic
   ```
   /analyze-existing /blog/podcast-equipment-guide
   /rewrite podcast equipment guide
   ```

3. **Low CTR**: High impressions, 2.5% CTR
   ```
   # Use Meta Creator agent output from Performance Report
   # Update meta title and description manually or via CMS
   ```

4. **Trending Topic**: "AI podcast tools" +150% growth
   ```
   /research AI podcast tools
   /write AI podcast tools
   ```

5. **Competitor Gap**: competitor.com ranks #3, your company not ranking
   ```
   /research podcast editing workflow
   /write podcast editing workflow
   ```

## Frequency Recommendations

**Weekly** (Quick Check):
- Review top 3 urgent priorities
- Monitor critical metrics (declining pages, position changes)
- Adjust current work based on new data

**Monthly** (Full Review):
- Complete `/performance-review` analysis
- Assess previous month's actions and results
- Plan next month's content priorities
- Adjust strategy based on trends

**Quarterly** (Strategic Review):
- Long-term trend analysis
- Competitive landscape shifts
- Content portfolio health assessment
- Resource allocation strategy

## Best Practices

### 1. Act on Data Quickly
The biggest gains come from quick wins - prioritize position 11-20 optimizations.

### 2. Track Results
Document what you implement and measure results:
```markdown
## Action Taken (2025-10-15)
- Optimized "podcast analytics" article
- Target: Move from position 13 → 8
- Changes: Added 500 words, improved meta, 3 internal links

## Results (2025-11-15)
- New Position: 9 (improved 4 positions)
- Traffic: +35% (+420 pageviews/month)
- Clicks: +18% (+89 clicks/month)
```

### 3. Don't Ignore Declining Content
Revenue leakage compounds - stop declines before creating new content.

### 4. Balance Quick Wins vs. Strategic Projects
**80/20 rule**: 80% effort on quick wins and optimization, 20% on new strategic content.

### 5. Review Data Freshness
- GA4: Usually next-day data
- GSC: 2-3 day delay typical
- DataForSEO: Real-time API data

Plan reviews accounting for data lag.

## Troubleshooting

### "No data returned"
- Check API credentials in `.env`
- Verify property IDs and site URLs
- Ensure service accounts have proper access
- Check date ranges (some metrics have minimum history)

### "DataForSEO budget exceeded"
- Check `DATAFORSEO_DAILY_BUDGET_LIMIT` in `.env`
- Reduce frequency of checks
- Use cached data when possible (set `CACHE_ENABLED=true`)

### "Performance report too long"
- Reduce `days` parameter for shorter period
- Focus on top opportunities only
- Export to separate file for detailed analysis

### "Recommendations don't match business goals"
- Adjust scoring weights in Performance Agent
- Filter opportunities by topic/keyword
- Manually override priority based on strategy

## Advanced Usage

### Custom Analysis Period
```
/performance-review 90  # Last 90 days for long-term trends
/performance-review 7   # Last 7 days for recent changes
```

### Focus on Specific Content
After full review, drill into specific pages:
```
# From performance review, identify problem page
/analyze-existing /blog/specific-article
/rewrite specific article
```

### Compare Periods
```
# Run monthly to track changes
/performance-review 30   # This month
# Compare to previous report from 30 days ago
```

## Expected Impact

Based on typical results:

**Quick Wins** (Position 11-20 → 5-10):
- Average traffic increase: 40-80%
- Timeframe: 2-8 weeks
- Success rate: 60-70% move to page 1

**Declining Content Updates**:
- Average recovery: 50-90% of lost traffic
- Timeframe: 2-4 weeks
- Often exceeds original performance with refresh

**Low CTR Meta Improvements**:
- Average CTR increase: 30-60%
- Timeframe: Immediate (1-2 weeks)
- Easiest wins with guaranteed impact

**New Trending Content**:
- Variable based on competition
- First-mover advantage significant
- Build authority before competition heats up

## Success Criteria

A successful performance review should:
- ✅ Identify 10+ actionable opportunities
- ✅ Prioritize work by ROI, not just volume
- ✅ Provide specific next steps for each opportunity
- ✅ Estimate impact and effort for resource planning
- ✅ Create clear roadmap for next 30 days
- ✅ Set measurable goals for tracking progress

## Example Workflow

```bash
# Month start: Run performance review
/performance-review 30

# Review report: content/research/performance-review-2025-10-15.md
# Identify top 5 priorities

# Week 1: Quick wins
/analyze-existing /blog/top-quick-win-article
/optimize content/drafts/top-quick-win-article.md

# Week 2: Declining content
/analyze-existing /blog/declining-article
/rewrite declining article

# Week 3: Meta improvements
# Update meta elements for 5 low-CTR pages

# Week 4: Trending topic
/research [trending topic from report]
/write [trending topic]

# Month end: Review results, run new performance review
/performance-review 30
# Compare to previous month, adjust strategy
```

## Integration with Performance Agent

The Performance Agent (`.claude/agents/performance.md`) provides the intelligence behind this command. It:
- Analyzes all data sources comprehensively
- Applies scoring and prioritization logic
- Generates detailed opportunity analysis
- Creates actionable recommendations
- Estimates impact and effort
- Builds implementation roadmap

The command acts as the interface to trigger this analysis and format results for action.

---

## IMPORTANT: Report Generation Rules

When generating the performance review report, you MUST:

1. **Follow the format in `.claude/agents/performance.md`** - This is the authoritative source for report structure

2. **Priority Queue = FOCUS TOPICS ONLY**
   - Use ONLY the `focus` data from categorized opportunities
   - Focus keywords: mainframe, COBOL, legacy, modernization, reverse-engineer, code-comprehension, application-understanding, forward-engineer, migration
   - Non-focus topics do NOT appear in Priority Queue sections

3. **Other Opportunities = Non-Focus Topics**
   - Use the `other` data from categorized opportunities
   - Present in condensed table format only (Type | Item | Key Metric | Score)
   - No detailed analysis for non-focus topics
   - Place at the END of the report for quality control

4. **Match detailed report structure**
   - Include Opportunity Score breakdowns (Impact/Effort/Confidence)
   - Include estimated effort hours for each action
   - Include specific action steps (numbered lists)
   - Include week-by-week implementation roadmap
   - Include success metrics and goals

**Self-Check**: If you find yourself listing Confluence, GitHub Copilot, Mermaid.js, word2vec, or other non-focus topics as top priorities - STOP and reorganize. Those belong in the "Other Opportunities (Quality Control)" table at the end, not in the Priority Queue.

---

**Remember**: Data without action is just noise. Use this report to drive actual content work, measure results, and continuously improve your SEO strategy.
