# Web Copy Style — Punchy Writing for Enterprise Pages

Compact reference for web page copywriting. Loaded alongside `@context/brand-voice.md` during Phases 1-2. Brand voice governs tone, terminology, and messaging sequence. This document adds **web-specific tests and structural discipline** that make copy land on a page.

Source methodology: Emma Stratton, *Make It Punchy* (Punchy.co) — adapted for B2B enterprise technical audiences.

---

## The Two-Pass Rule

Every piece of web copy passes through two registers:

1. **Draft pass (BBQ test)**: Write as if explaining to a smart peer at a BBQ. If they wouldn't understand it, rewrite it. This tests *clarity*.
2. **Edit pass (Boardroom test)**: Tighten as if presenting to a Fortune 500 CTO approving a multi-million dollar program. This tests *precision and weight*.

The draft pass prevents insider jargon. The edit pass prevents casualness. Both passes are mandatory for every section.

---

## Five Mandatory Tests

Run these on every section before accepting it. A section that fails any test goes back for revision.

### 1. Refrigerator Test (anti-vagueness)
Could this headline describe a refrigerator? "Reduce risk." "Increase efficiency." "Enterprise-grade solution." All fail — they could describe anything. Rewrite until only your target buyer recognizes themselves.

**Fail**: "Reduce modernization risk with trusted insights."
**Pass**: "Extract business rules from 2 million lines of COBOL in hours, not months."

### 2. "So What?" Test (value ladder)
Start with the feature. Ask "So what?" repeatedly until you reach the outcome the buyer actually cares about. Lead with that outcome.

**Feature**: Deterministic static analysis.
**So what?** It produces code-derived understanding.
**So what?** Teams can verify application behavior without relying on senior engineers.
**So what?** Modernization programs start on time instead of stalling on knowledge gaps.
**Lead with**: "Start modernization on time. Get verified application behavior without waiting for senior engineers."

### 3. SMIT Test (Single Most Important Thing)
Each section conveys exactly one message. If a section makes two points, split it. If you can't name the one thing a reader takes away, the section isn't focused enough.

### 4. Outside-in Check
Does the sentence start from the buyer's world or the product's world? The first words of every section headline must reflect what the buyer experiences, not what the product does.

**Inside-out**: "[Company Name]'s deterministic analysis extracts business rules..."
**Outside-in**: "Get verified business rules extracted in hours..."

### 5. Altitude Check
Match specificity to the audience reading this page:

| Audience | Altitude | Example |
|----------|----------|---------|
| CIO / SVP | Higher — business outcomes, risk, timelines | "De-risk your next modernization program with verified application understanding." |
| Architect / Tech Lead | Medium — technical outcomes with business context | "Trace execution paths across 15 interconnected programs to verify business logic before migration." |
| Developer / Engineer | Lower — technical specifics, concrete capabilities | "Map call hierarchies, data flows, and variable usage across your entire COBOL codebase." |

Homepage copy typically targets CIO/SVP altitude with enough specificity to pass the Refrigerator Test.

---

## Web Copy Structure Rules

### VBF Hierarchy (Value → Benefits → Features)

Every section follows this order:
1. **Value** (headline): The outcome the buyer cares about
2. **Benefits** (supporting line): How their world changes
3. **Features** (proof): What makes it possible — only if needed

Do NOT invert this. Feature-first copy ("Our deterministic engine...") loses readers before they understand why they should care.

### Headline Story Arc

Reading only the section headlines should tell the full value proposition as a narrative. Test by extracting all H2s and reading them in sequence. If the story doesn't hold, the headlines need work.

### One Idea Per Block

Web copy is not prose. Each block (headline + 1-2 supporting sentences) delivers one idea. If you need a second idea, start a new block. Readers scan — give them clean entry points.

### No Throat-Clearing

The first sentence of every section does real work. No "In today's rapidly evolving landscape..." No "When it comes to modernization..." Open with the point.

**Throat-clearing**: "When enterprises embark on modernization journeys, they often face the challenge of..."
**Direct**: "Modernization stalls when teams can't describe what their applications actually do."

---

## Sentence-Level Discipline

These rules supplement (not replace) the sentence-level guidelines in brand voice.

### Rhythm Pattern
Short declaration + substantive supporting sentence. Avoid three or more consecutive short sentences (choppy) or three or more consecutive long sentences (dense).

**Good rhythm**: "Knowledge fragments. As senior engineers leave and systems evolve, understanding scatters across people, tools, and outdated documents — leaving modernization programs without the foundation they need."

### Numbers Beat Adjectives
| Weak | Strong |
|------|--------|
| "Dramatically faster" | "90% faster" |
| "Comprehensive coverage" | "Across 2M+ lines of code" |
| "Rapid analysis" | "Business rules extracted in hours" |
| "Trusted by leading enterprises" | "Deployed at 4 of the top 10 US banks" |

### Curse of Knowledge Checklist
Before finalizing any section, check these terms. If they appear without expansion or context, they likely need rewriting for the target audience:

- Deterministic static analysis → explain the outcome, not the technique
- Application behavior → expand for business audiences per brand voice rules
- Code-derived understanding → ground in what it produces (e.g., "business rules traceable to source code")
- Execution risk → specific to what: missed dependencies? Late scope changes? Name it.

---

## CTA Copy

### Rule: Benefit-first, action-second
**Weak**: "Request a demo"
**Strong**: "See your business rules extracted — request a demo"

### CTA progression across the page
1. **Hero CTA** (high commitment): "See [Company Name] on your code" / "Request a demo"
2. **Mid-page CTA** (after proof): "See how it works" / "Explore the platform"
3. **Final CTA** (after full narrative): Restate core value + primary action. Friction reducer underneath.

---

## Quick Reference: Web Copy vs. Article Copy

| Dimension | Web page copy | Blog/article copy |
|-----------|--------------|-------------------|
| Sentence length | Shorter (avg 12-18 words) | Medium (avg 15-25 words) |
| Paragraph length | 1-2 sentences | 2-3 sentences |
| Tone | Elevated (Authority Under Scrutiny) | Default (Confident Expert Colleague) |
| Structure | Headline carries meaning, body supports | Body carries argument, headline frames |
| Proof | Numbers, logos, badges inline | Examples, case studies, extended reasoning |
| CTA | Explicit button with clear next step | Implicit or soft (read more, try it) |
| Jargon tolerance | Near zero — every term must be immediately clear | Moderate — can define and build on terms |
