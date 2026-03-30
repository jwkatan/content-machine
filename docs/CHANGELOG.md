# Changelog

## 2026-02-25 (b)

### Changed: Asset Builder refactored to agent-per-phase architecture

**Files:**
- `.claude/commands/asset.md` (updated)
- `asset-builder/templates/decisions-template.md` (updated)
- `docs/asset-builder.md` (updated)

**Problem:** The original Asset Builder design used a single orchestrator agent across all 3 phases (Brief, Write, Review). For long assets like whitepapers, this caused context compaction between phases — the conversation accumulated tokens from Phase 1 research and outlining that degraded Phase 2 writing quality, and Phase 2 writing context degraded Phase 3 review quality.

**Fix:** Refactored to an agent-per-phase pattern where each phase runs as its own top-level agent with fresh context. The `/asset new` dispatcher gathers all user input and persists it to a `Project Context` section in `decisions.md`. Each phase agent reads its inputs entirely from disk files (`decisions.md`, `brief.md`, `content.md`) — no conversation history carries between phases. Phase transitions happen via the user running `/asset continue`, which reads `decisions.md` to determine the current phase and spawns the appropriate agent.

**Impact:** Each phase gets a full clean context window. The section-by-section subagent pattern within Phase 2 is unchanged. No changes to existing workflows.

## 2026-02-25

### Added: Asset Builder for deep content creation

**Files:**
- `.claude/commands/asset.md` (new)
- `.claude/agents/asset-reviewer.md` (new)
- `.claude/agents/persona-reviewer.md` (new)
- `asset-builder/asset-types/whitepaper.md` (new)
- `asset-builder/asset-types/primer.md` (new)
- `asset-builder/asset-types/sales-deck.md` (new)
- `asset-builder/templates/decisions-template.md` (new)
- `docs/asset-builder.md` (new)
- `CLAUDE.md`, `docs/COLLABORATOR-ONBOARDING.md`, `data_sources/config/.env` (updated)

**Problem:** The system could produce blog articles, LinkedIn posts, newsletters, and web pages, but had no capability for deeper, potentially gated content like whitepapers, solution guides, primers, or sales decks.

**Fix:** Added the `/asset` command with a 3-phase gated workflow (Brief, Write, Review) and human checkpoints at every transition. Key design decisions:
- Section-by-section writing via subagents to prevent context rot and quality degradation
- Per-section PMM knowledge loading to keep token usage manageable (~15-30K per asset vs 200K+ for all PMM knowledge)
- Writer/reviewer separation (asset-reviewer for quality, persona-reviewer for audience fit using real PMM persona files)
- Scoped revision protocol to prevent drift during feedback loops
- Three starter templates: whitepaper (3000-6000 words), primer (800-1500 words), sales-deck (12-16 slides)

**Impact:** New `/asset` command supports 9 asset types. No changes to existing `/write`, `/research`, `/linkedin`, `/optimize`, or `/webpage` workflows. New asset types can be added by creating a template file in `asset-builder/asset-types/` - no command changes needed.

## 2026-02-22 (c)

### Added: Slug update with automatic 301 redirect

**Files:** `data_sources/modules/wordpress_client.py`

**Problem:** When refreshing listicle articles from 2025 → 2026, changing the URL slug in WordPress left the old URL returning 404 with no redirect. Redirects had to be created manually via the Redirection plugin.

**Fix:** Added `new_slug` support to the publish flow. When `metadata.json` contains a `new_slug` field, `export_to_wordpress()` updates the WordPress slug and automatically creates a 301 redirect from the old URL to the new one via the Redirection plugin API.

**Usage:** Add `"new_slug": "best-article-slug-in-2026"` to `metadata.json` before running `checkin(slug, push=True)`. The redirect is created automatically. The `new_slug` field can be omitted when the slug isn't changing.

## 2026-02-22 (b)

### Fixed: Title duplication on WordPress publish

**File:** `data_sources/modules/content_library.py`

**Problem:** When `checkin()` regenerated HTML from `article.md`, it passed the full markdown including the H1 title to `markdown_to_gutenberg()`. The H1 became a heading block in the body HTML. Then `export_to_wordpress()` also sent the `title` field from `metadata.json` as the WordPress post title — resulting in the title appearing twice on the published page.

**Fix:** `checkin()` now strips the H1 from markdown before converting to HTML, matching the same logic `export_to_wordpress()` already uses in its `use_edited=True` path.

### Added: Table and separator support in `markdown_to_gutenberg()`

**File:** `data_sources/modules/wordpress_client.py`

**Problem:** Markdown tables (`| header | ... |`) and horizontal rules (`---`) had no handler in the Gutenberg converter. Tables rendered as raw pipe text inside `<p>` tags; separators rendered as literal "---" text. Both required manual HTML editing after every article publish.

**Fix:** Added `wp:table` block support (with `<thead>/<tbody>` structure and inline formatting in cells) and `wp:separator` block support. Also added break conditions in the paragraph collector so these elements aren't swallowed into paragraphs.

### Added: Tests for tables, separators, and H1 stripping

**File:** `tests/test_gutenberg_conversion.py`

Added 11 new tests: `TestSeparatorBlock` (5 tests), `TestTableBlock` (5 tests), `TestCheckinH1Stripping` (1 test). All 82 tests pass.

## 2026-02-22

### Fixed: `checkin()` now auto-regenerates Gutenberg HTML from markdown

**File:** `data_sources/modules/content_library.py`

**Problem:** When publishing a rewritten article via `checkin()`, the function always used `original.html` from the workbench — which contained the OLD WordPress content from `checkout()`, not the updated rewrite. This caused the old article version to be pushed to WordPress instead of the new one.

**Fix:** `checkin()` now compares timestamps on `article.md` and `original.html`. If `article.md` is newer (or `original.html` is missing), it auto-regenerates the Gutenberg HTML via `markdown_to_gutenberg()` before pushing.

**Impact:** The rewrite-to-WordPress publishing flow is now:
1. `checkout('slug')`
2. Overwrite `article.md` with new content, update `metadata.json`
3. `checkin('slug', push=True)`

No manual `original.html` deletion or regeneration needed.

### Changed: WordPress pushes now set publication date to current date

**File:** `data_sources/modules/wordpress_client.py`

**Change:** Both `update_post_to_draft()` (for article updates) and `create_draft()` (for new articles) now include `date: datetime.now().isoformat()` in the WordPress API payload. This ensures the publication date is updated to the current date whenever an article is pushed, whether it's a new draft or an update to an existing article.

---

## 2026-03-15: Feature parity sync with source project

### Added: Launch Orchestrator

**Files:** `.claude/commands/launch.md`, `.claude/launch/` (10 files), `.claude/agents/cmo-reviewer.md`, `.claude/agents/cross-pillar-linker.md`, `.claude/agents/messaging-drift-checker.md`

**Change:** Added full launch orchestration system — cornerstone-first workflow with human-in-the-loop checkpoints, messaging propagation, and multi-pillar dispatch. Outputs centralized in `content/launches/`.

---

### Added: HubSpot Client module

**File:** `data_sources/modules/hubspot_client.py`

**Change:** Added full HubSpot marketing automation: form creation, email creation (DnD modules), workflow creation, file upload, contact lists, and end-to-end `setup_landing_page_pipeline()` orchestrator. All sensitive IDs and credentials are env-var driven (see `.env.example` for new vars). Workflows are always created disabled.

---

### Added: Image Builder system

**Files:** `data_sources/modules/image_builder.py`, `image-builder/` directory, `.claude/commands/image.md`, `.claude/agents/image-designer.md`

**Change:** Added deterministic branded image generation from HTML/CSS templates. Pre-built `gated-document` template produces 1206×1562px landing page banners from PDF first pages. Uses Puppeteer + sharp + ImageMagick.

---

### Added: Landing page support (download + webinar)

**Files:** `data_sources/modules/wordpress_client.py`, `docs/landing-pages.md`

**Change:** Added `_build_download_blocks()`, `_build_webinar_blocks()`, and `publish_landing_page()` to `wordpress_client.py`. Supports gated document and webinar landing page post types with full Gutenberg block construction.

---

### Added: PDF builder WeasyPrint migration

**Files:** `pdf-builder/render.py`, `pdf-builder/INSTRUCTION.md`, `pdf-builder/templates/whitepaper/styles.css`, `pdf-builder/assets/`

**Change:** Migrated PDF builder from Puppeteer (Node.js) to WeasyPrint (Python). Added one-pager template support in `pdf_builder.py`. CSS variables renamed to `--brand-primary` / `--brand-secondary` for easier customization. Old Node.js files removed.

---

### Added: 12 new asset types

**Files:** `asset-builder/asset-types/` (battle-card, discovery-guide, email-campaign, gated-download, objection-guide, one-pager, partner-brief, press-release, talk-track, video-script, webinar-deck, webinar-landing)

**Change:** Expanded asset type library from 4 to 16 types covering the full content spectrum. Updated `competitive-comparison.md` with improved structure.

---

### Added: 5 new agents, 2 updated agents

**Files:** `.claude/agents/`

**Change:** Added `cmo-reviewer.md`, `cross-pillar-linker.md`, `messaging-drift-checker.md`, `video-script-editor.md`, `image-designer.md`. Updated `asset-reviewer.md` and `editor.md` with improvements.

---

### Added: 3 new commands

**Files:** `.claude/commands/image.md`, `.claude/commands/launch.md`, `.claude/commands/update-email.md`

**Change:** Added `/image` (branded image generation), `/launch` (launch orchestrator), and `/update-email` (HubSpot email template updates).

