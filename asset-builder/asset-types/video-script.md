a# Video Script — Asset Type Template

## Metadata

- **Format**: script
- **Video type**: [demo / launch / product-overview / hiring / customer-story] — set in decisions.md
- **Target duration**: [60-90s / 2-4 min] — set in decisions.md
- **Scene count**: 4-8 scenes (4 required + up to 4 conditional per video type)
- **Tone**: Set per project. Defaults: demo = direct, confident; launch = energetic; hiring = warm, authentic; customer story = credible, peer-to-peer
- **Brand voice**: Part 1 always. Part 2 always (all video types feature [COMPANY])
- **Primary personas**: The target viewer — set per project. Video audience may differ from the buyer reading a PDF
- **Voiceover style**: [narrator / on-camera talent / customer testimonial / mixed] — set in decisions.md

## Knowledge Sources

Load from `$PMM_KNOWLEDGE_PATH`:

| File | When to Load | Approx Tokens |
|------|-------------|---------------|
| `knowledge_base/messaging/framework.md` | Always | ~5,300 |
| `knowledge_base/messaging/words_that_work.md` | Always | ~3,600 |
| `config/teach_product_output.md` | When product featured (demo, launch, product-overview) | ~8,400 |
| `knowledge_base/personas/[target].md` | When persona-specific (hiring, customer-story) | ~6,000 |

**Per-scene loading**: Each scene writing subagent loads only the files tagged for its scene. Hook and CTA need only messaging/framework. Demo and Proof scenes need teach_product_output. Hiring and customer-story scenes need persona. Total context per subagent: 9-17K tokens.

## Scene Structure

Video scripts follow this arc. Scenes marked (required) appear in every video. Scenes marked (conditional) are activated per video type in the brief phase.

| # | Scene | Job | Viewer's Question | Required? |
|---|-------|-----|-------------------|-----------|
| 1 | **Hook** | Stop the scroll; earn the next 10 seconds | "Is this for me?" | Required |
| 2 | **Problem / Stakes** | Make the pain real and urgent | "Do you understand my world?" | Required |
| 3 | **Context / Why Now** | Establish urgency or timeliness | "Why does this matter right now?" | Conditional |
| 4 | **Solution Reveal** | Introduce the approach or product | "What is this?" | Required |
| 5 | **Demo / Proof of Mechanism** | Show it working, not just describe it | "How does it actually work?" | Conditional |
| 6 | **Outcomes / Proof** | Quantify or socially validate the claim | "Has this worked for others?" | Conditional |
| 7 | **Differentiation** | Why this vs. doing nothing or alternatives | "Why not just use what I have?" | Conditional |
| 8 | **CTA** | One clear next action | "What do I do now?" | Required |

**Video type defaults:**
- **Demo**: Scenes 1, 2, 4, 5 (extended), 8. Scene 5 is the core.
- **Launch**: Scenes 1, 2, 3, 4, 6, 8. Scene 3 carries the timeliness argument.
- **Product overview**: All 8 scenes, each compressed. Scene 5 is a highlight reel, not a walkthrough.
- **Hiring**: Scenes 1, 2 (candidate pain), 4 (role/team reveal), 6 (employee voices), 8. Skip 3, 5, 7.
- **Customer story**: Scenes 1, 2, 5 (before/after as the demo), 6 (customer is the proof), 8. Skip 3, 4, 7.

### Scene Details

**Scene 1: Hook** (5-10s / 12-23 words of voiceover)
- Opens with the viewer's world, not [COMPANY]. Start with a question, a bold claim, or a scene from their day.
- Visual: high-energy, immediate. No logos, no title cards in the first 3 seconds.
- On-screen text: optional — a provocative question or short stat works. If used, max 6 words.
- Transition: smash cut or quick cut to Scene 2.
- Knowledge: messaging/framework (for approved problem framing and language)

**Scene 2: Problem / Stakes** (10-20s / 23-47 words of voiceover)
- Articulate the pain in the viewer's own language. Use `words_that_work.md` for approved phrasing.
- Do not solve the problem here. Let the tension sit.
- Visual: illustrate the consequence of the problem — a fragmented screen, a frustrated team, a legacy system.
- On-screen text: one quantified pain point if available (e.g., "73% of engineers can't explain the code they maintain").
- Knowledge: messaging/framework, words_that_work

**Scene 3: Context / Why Now** (10-15s / 23-35 words of voiceover — conditional)
- Active for: launch, product-overview.
- Connect to a market trigger, organizational moment, or technology shift.
- Frame urgency factually, not with fear.
- Visual: timeline, trend graphic, or a moment of organizational change.
- Knowledge: messaging/framework

**Scene 4: Solution Reveal** (10-20s / 23-47 words of voiceover)
- Introduce the approach or product by name. Lead with the outcome the viewer cares about, not the feature name.
- One-sentence principle before the product name if possible.
- Visual: product logo reveal, interface first look, or conceptual motion graphic.
- On-screen text: product name + one-phrase value statement.
- Knowledge: messaging/framework, teach_product_output (if product is named)

**Scene 5: Demo / Proof of Mechanism** (15-40s / 35-93 words of voiceover — conditional)
- Active for: demo (extended), product-overview (compressed), customer-story (reframed as before/after).
- Show the product doing the thing, not the marketing promise of the thing.
- Voiceover narrates what the viewer is seeing — not more information than the screen shows.
- Visual: screen recording or live product UI. Zoom on the specific moment of value.
- On-screen text: label the key interaction (e.g., "[COMPANY] finds the entry point in 4 seconds").
- Knowledge: teach_product_output

**Scene 6: Outcomes / Proof** (10-20s / 23-47 words of voiceover — conditional)
- Active for: launch, product-overview, hiring (employee voices), customer-story (customer is the proof).
- One specific outcome with a number, or one named customer/employee reference.
- Do not list multiple outcomes — pick the one that will land with THIS viewer.
- Visual: customer quote card, stat tile, or employee speaking on camera.
- On-screen text: the headline number or quote attribution.
- Knowledge: teach_product_output (for approved stats), persona file (for segment-appropriate proof)

**Scene 7: Differentiation** (10-15s / 23-35 words of voiceover — conditional)
- Active for: product-overview. Optional for launch and demo if time permits.
- One clear contrast: what [COMPANY] does that alternatives cannot, framed structurally not competitively.
- Do not name competitors. Frame as a capability distinction ("deterministic vs. probabilistic").
- Visual: simple two-column contrast or conceptual diagram.
- Knowledge: messaging/framework

**Scene 8: CTA** (5-10s / 12-23 words of voiceover)
- One action. One URL. One verb. Not "learn more, book a demo, or follow us."
- The action must match the viewer's likely next step given the video type (demo viewers want to try it; hiring viewers want to apply; launch viewers want early access).
- Visual: clean product logo, CTA text prominent. No clutter.
- On-screen text: URL displayed. Must match the voiceover destination exactly.
- Transition: hold on CTA for 2-3 seconds after voiceover ends.
- Knowledge: none

## A+ Agency Output Style

A production-ready video script reads like it was handed off to a director — not reviewed by a committee. The complete document has three parts: a production header, the scene sequence, and a totals summary.

### What A+ Looks Like

**Voiceover that sounds written-to-be-heard, not read.** Short sentences. Active verbs. Natural pauses built into the rhythm. Read it aloud — if you stumble, rewrite it. The narrator should never sound like they're reading marketing copy.

**Visual directions specific enough to execute cold.** A motion designer receives this script without a briefing call. "Show the [COMPANY] interface with a COBOL file open, cursor moving automatically to the function entry point — zoom in over 2 seconds" is a direction. "Demonstrate the product" is not.

**Music continuity that builds intentionally.** The opening scene establishes the audio identity. Every subsequent scene either continues it or makes a deliberate change. A script where every scene says "continue ambient track" is not directing the video — it's delegating.

**A hook that opens on a specific, vivid moment.** Not "Are you tired of bad code documentation?" — that's a survey question. Instead: "You just inherited a 40,000-line COBOL system. Your manager asks how long it'll take to onboard. You have no idea." Specificity earns the next 10 seconds.

**A CTA that names the destination and the action.** Not "Learn more at [your-domain.com]." Instead: "Start your free trial at [your-domain.com]/[cta-path] — onboard your first teammate today." One URL. One verb. One outcome the viewer can visualize.

### Complete Document Structure

The full script file follows this order:

```markdown
# [Video Title]

**Video type:** [demo / launch / product-overview / hiring / customer-story]
**Target duration:** [60-90s / 2-4 min]
**Voiceover style:** [narrator / on-camera talent / customer testimonial / mixed]
**Version:** 1.0

---

## Production Overview

**Music direction:** [Opening genre, tempo, energy — e.g., "Driving electronic, 120 BPM, builds through Scene 4, resolves to clean ambient for CTA"]
**Talent notes:** [Delivery guidance — pacing, tone, emotional register. E.g., "Conversational authority. No corporate polish. Slight urgency in Scenes 1-2, confident ease from Scene 4 onward."]
**Voiceover word count target:** [N–N words at 140 wpm for target duration]

---

[Scene blocks — see Scene Block Format below]

---

## Script Totals

| Metric | Target | Actual |
|--------|--------|--------|
| Total voiceover words | [140–210 for 60-90s / 280–560 for 2-4 min] | [N] |
| Scene count | 4–8 | [N] |
| Duration estimate at 140 wpm | [60-90s / 2-4 min] | ~[N]s |
| Required scenes present | Hook, Problem, Reveal, CTA | ✓ / ✗ per scene |
```

The Production Overview is written **before** the scenes. It is not a summary added afterward — it is a director's brief that shapes every scene that follows. Music direction and talent notes written here must be consistent with the Music/Sound field in Scene 1.

The Script Totals are populated **after** all scenes are written and reviewed. Count voiceover words only — not stage directions or field labels.

---

## Scene Block Format

Each scene follows this format. The `---` separator creates a clean boundary between scenes in the production document.

```markdown
---

## Scene [N]: [Scene Title]

**Type**: [Hook / Problem / Context / Reveal / Demo / Proof / Differentiation / CTA]
**Duration target**: [Xs]

**Voiceover:**
[Script text exactly as the narrator speaks it. No stage directions. No brackets. Clean prose, teleprompter-ready. At 140 wpm: 10s = ~23 words, 15s = ~35 words, 20s = ~47 words, 30s = ~70 words.]

**Visual direction:**
[What is on screen. Specific enough for a motion designer to execute without a follow-up call. One sentence per visual beat. Camera angle, motion type, subject, product interface reference.]

**On-screen text:**
[Any text overlaid on the video. Format each as: "Text content" — position (lower-third / center / corner / full-screen). Use "None" if no overlay.]

**Transition:**
[Cut / dissolve / wipe / smash cut / hold on black / fade. Include duration if relevant: "dissolve, 0.5s".]

**Music / Sound:**
[Audio texture for this scene. "Continue ambient track," "Sound effect: [description]," "Music swells," "Silence." For Scene 1, describe the full music direction: genre, tempo, energy.]
```

## Formatting Rules

- **Scene count**: 4-8 scenes. Fewer than 4 is a promo clip. More than 8 is an explainer — reconsider the format.
- **Duration discipline**: Count only voiceover words. Total must fit target duration at 140 wpm. For 60-90s: 140-210 words total. For 2-4 min: 280-560 words total.
- **Voiceover is prose**: Write exactly what the narrator says. No parentheticals, stage directions, or "cut to" instructions in this field.
- **Visual direction is literal**: "Show the [COMPANY] interface with a COBOL file open, cursor moving to the entry point" — not "demonstrate the product experience."
- **On-screen text is sparse**: 1-2 overlays per scene maximum. If a scene needs more text on screen, it is trying to be a slide.
- **One scene, one idea**: If a scene is handling the problem AND introducing the solution, split it.
- **CTA is singular**: One URL. One action. One destination. No secondary options.
- **No "Visit our website" CTAs**: The CTA must be a specific destination with a specific verb.
- **Music continuity**: The Music/Sound field must be populated for every scene. Silence is a valid value but must be explicit.

## Post-Write Agents

| Agent | Required? | Notes |
|-------|-----------|-------|
| `video-script-editor` | Yes | Full script review: timing, speakability, remote control test, visual-audio sync, music architecture, scene completeness, hook, CTA, claims specificity, voiceover patterns. |
| content scrubber | Yes | Universal post-processor. Run last. |

**Note**: PDF output is not applicable for video scripts. Skip the optional PDF generation step in Phase 3.

## Quality Checklist

- [ ] Total voiceover word count fits within target duration at 140 wpm (60-90s = 140-210 words; 2-4 min = 280-560 words)
- [ ] Scene count is 4-8; all required scenes (Hook, Problem, Solution Reveal, CTA) are present
- [ ] Conditional scenes match the video type recorded in decisions.md
- [ ] Hook opens with the viewer's world, not [COMPANY] — no company intro or logo in the first 3 seconds
- [ ] Voiceover fields contain clean teleprompter prose (no brackets, stage directions, or placeholder text)
- [ ] Every visual direction is specific enough for a motion designer to execute without a follow-up call
- [ ] On-screen text per scene is 1-2 overlays maximum
- [ ] Transition and Music/Sound fields are populated for every scene (no empty or "TBD" values)
- [ ] CTA scene has exactly one action, one URL, one verb
- [ ] Product claims in Demo and Proof scenes verified against `teach_product_output.md`
- [ ] Differentiation scene (if present) frames the contrast structurally, not by naming competitors
- [ ] Proof scene (if present) has a specific number or named reference — not "teams like yours"
- [ ] Voiceover uses approved language from `words_that_work.md`, not internal jargon or feature names
- [ ] No scene restates what a prior scene already established
- [ ] Content scrubber has been run
