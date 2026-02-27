# Review Conent Command

Use this command to conduct a content quality review of either the outline or full content

## Usage
`/review-content [topic]`

## Overview

This command evaluates the factual integrity of content by analyzing claims, verifying sources, and assessing whether statements match their sources in both wording and intent. It's designed for final content review before publication and outline review before writing begins.

The command catches five critical issues:

1. **Factual claims that don't match sources** — Claims quoted, paraphrased, or cited inaccurately
2. **Assertions without proper sourcing** — Unsupported claims presented as fact
3. **Context drift and scope creep** — Claims generalized beyond what sources actually support (especially vendor marketing claims)
4. **Content drift from intent** — Content that doesn't match the expected experience a reader would have based on the title
5. **Structural redundancy** — Sections that repeat the same facts, arguments, or overlapping scope under different headings

**Important:** This command never modifies source content. It identifies issues and provides guidance for improvement only.

## Evaluation Process

**Step 1: Content Alignment Check**
1. **Extract the title** — Identify the intended learning goal a reader would expect
2. **Examine section titles** — Does the narrative fit the expected learning goal?
3. **Flag vendor emphasis** — Is vendor/product information overemphasized in ways that don't serve reader intent?

**Step 2: Structural Redundancy Check**
Review the outline or full content for overlapping sections:
1. **Map each section's core claims** — For every H2/H3, list the key facts, arguments, and concepts it covers
2. **Cross-compare sections** — Identify any fact, statistic, or argument that appears in more than one section
3. **Check scope overlap** — Flag sections whose topic scope substantially overlaps (e.g., two sections both covering "deterministic + AI" from different angles)
4. **Evaluate necessity** — For each overlap, determine: Is the repetition intentional reinforcement, or structural redundancy from competitive research surfacing the same topic multiple times?
5. **Recommend consolidation** — For true redundancies, recommend which section should own the content and what the other section should cover instead

**Step 3: Claim Verification**
For each factual claim:
1. **Extract the claim** — Identify factual statements, statistics, assertions
2. **Search for sources** — Web search to find what the actual source says
3. **Compare intent and context** — Verify the article's usage preserves original meaning
4. **Assess source quality** — Rate credibility using the quality tiers below
5. **Flag vendor/competitor claims** — Apply extra scrutiny to marketing claims and generalizations

### Output

Generate a comprehensive markdown report (as new file or artifact) with:

- **Summary** (total claims evaluated, verification %, critical issues, key recommendations)
- **Structural Redundancy Findings** (sections with overlapping scope, repeated facts/arguments, consolidation recommendations)
- **Claim Evaluation Table** (detailed assessment of each claim with status)
- **Critical Issues** (false claims, significant discrepancies)
- **Improvement Opportunities** (unverified assertions, weak sources, priority fixes)
- **Source Quality Assessment** (gold/silver/bronze tier sources identified)
- **Vendor & Competitor Claim Assessment** (Swimm positioning, competitor claims, balance check)
- **Notes** (timing issues, hallucination risks, strengths, citation practices)
- **Recommended Action Plan** (before-publication checklist)

At the end, ask:

**"Would you like me to generate fix prompts for any of these issues?"**

[If issues exist, provide numbered list:]
1. **[Issue Title]** | Why: [Brief explanation] | Suggested change: [Concrete fix]
2. **[Issue Title]** | Why: [Brief explanation] | Suggested change: [Concrete fix]

Respond with numbers (e.g., "yes for 1, 3, 5") and I'll provide prompts to guide Claude in fixing each.

---

## Evaluation Frameworks

### Source Quality Tiers

Apply this framework consistently to evaluate source credibility:

| Tier | Examples | Treatment |
|------|----------|-----------|
| **Gold** | Peer-reviewed research papers (published in established venues), government/official data, academic institutions, published case studies | Trust the source; verify it's from an established academic publisher or institution, not a student project or small-scale school paper |
| **Silver** | Established independent publications (tech blogs, industry analysts), academic experts, Swimm whitepapers/positions | Verify with second source if the claim is novel or contradicts other sources |
| **Bronze** | Industry blogs from known experts, company whitepapers, analyst reports (Gartner, Forrester), vendor case studies | Treat as supporting evidence; search for independent corroboration before relying solely |
| **Copper** | Marketing content, unvetted blogs, social media, vendor announcements without third-party validation | Require independent verification; flag claims as suspect unless corroborated |
| **Lead** | Unverifiable sources, anonymous sources, claims contradicted by higher-tier sources | Flag as unreliable; do not cite without substantial corroboration |

### Vendor/Competitor Detection & Extra Skepticism

**Auto-flag claims about these vendors/competitors for extra scrutiny:**

Common modernization space vendors: AWS, Microsoft (Azure/Copilot), Mechanical Orchard, Cast Software, Rocket Software, Google Cloud, IBM, Databricks, Salesforce, Oracle, HashiCorp, Atlassian, ServiceNow, Informatica, MuleSoft, Talend, Boomi, Apptio

**Common patterns to watch for (source assertion → article assertion):**
- **Generalization from one case:** "AWS saved 50% on modernization timeline" → Article claims "AI agents save 50% of modernization time"
- **Scope creep:** "70% of applications will include agentic workflows" → Article claims "70% of enterprises are using agents"
- **Unverified capability claims:** "Product X enables AI agents to handle context" without third-party validation
- **Marketing as fact:** Vendor claims presented as established truth rather than marketing assertion
- **Missing circumstances:** Claims without context about sample size, conditions, or applicability

### Common Claim Patterns to Watch

These patterns often indicate problematic claims:

1. **Statistic without timeframe** — "70% of enterprises use agents" without clarifying when this was measured
2. **Benchmark from undisclosed conditions** — "Saved 50% of time" without explaining context (sample size, specific use case, circumstances)
3. **Product capability claims without proof** — "Graph databases enable AI agents to handle context" without citing how or where this was demonstrated
4. **Competitor claims lacking source** — Assertions about what competitors do or their market position without third-party verification
5. **Definitional claims presented as universal** — Framing industry definitions or interpretations as objective truth
6. **Out-of-context quotes** — Quotes that are technically accurate but imply something different in the original context
