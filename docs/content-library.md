# Content Library

A queryable local mirror of all WordPress articles, with a temporary workbench for editing.

## Architecture

```
WordPress (source of truth)
    ↕ sync
content.db (queryable mirror)
    ↕ checkout / checkin
workbench/{slug}/ (temporary editing files)
```

**Three layers:**

1. **WordPress** — The canonical store. Articles are published and managed here.
2. **Database** (`data_sources/content.db`) — SQLite mirror of all articles. Stores full HTML (Gutenberg blocks), markdown, metadata, and extracted links. Gitignored. Rebuildable from WordPress at any time with `sync_all()`.
3. **Workbench** (`content/workbench/{slug}/`) — Temporary checkout for articles being actively edited. Contains `original.html`, `article.md`, `metadata.json`. Cleaned up after pushing back to WordPress. Gitignored.

## Database Schema

### `articles` table
Core article registry. One row per article.

| Column | Type | Description |
|--------|------|-------------|
| `slug` | TEXT UNIQUE | Article slug (folder name, URL segment) |
| `title` | TEXT | Article title |
| `meta_title` | TEXT | SEO title (from Yoast) |
| `meta_description` | TEXT | SEO description |
| `url` | TEXT | Full WordPress URL |
| `wordpress_post_id` | INTEGER | WordPress post ID |
| `wordpress_post_type` | TEXT | Post type (`article`, `posts`, `pages`) |
| `wordpress_status` | TEXT | `publish`, `draft`, etc. |
| `publication_date` | TEXT | Original publication date |
| `modified_date` | TEXT | Last modified in WordPress |
| `content_html` | TEXT | Raw Gutenberg HTML |
| `content_markdown` | TEXT | Converted markdown |
| `word_count` | INTEGER | Word count from markdown |
| `last_synced_at` | TEXT | When last pulled from WordPress |

### `articles_fts` virtual table
FTS5 full-text search index over `slug`, `title`, `content_markdown`, `meta_title`, `meta_description`. Kept in sync via triggers.

### `article_links` table
Links extracted from article HTML content.

| Column | Type | Description |
|--------|------|-------------|
| `source_article_id` | INTEGER | Article containing the link |
| `target_url` | TEXT | The href URL |
| `target_article_id` | INTEGER | Matched article ID (NULL if external) |
| `anchor_text` | TEXT | Link text |
| `is_internal` | BOOLEAN | Whether the link points to the same site |
| `last_checked_at` | TEXT | When last tested for broken status |
| `last_status_code` | INTEGER | HTTP status from last check |

## Module: `data_sources/modules/content_library.py`

### Sync Functions

| Function | Description |
|----------|-------------|
| `init_db()` | Create database schema (idempotent) |
| `sync_all(post_type='article')` | Pull all articles from WordPress, paginated |
| `sync_article(slug_or_url)` | Pull a single article by slug or URL |

### Query Functions

| Function | Description |
|----------|-------------|
| `search(query, limit=20)` | FTS5 search, returns snippets not full content |
| `list_articles(status, sort_by, limit)` | List articles with metadata (no content) |
| `get_article(slug, include_content=False)` | Get one article, optionally with full content |
| `article_count()` | Count of articles in database |

### Workbench Functions

| Function | Description |
|----------|-------------|
| `checkout(slug, fresh=True)` | Check out article to `content/workbench/{slug}/` |
| `checkin(slug, push=False)` | Check in edits to database, optionally push to WordPress |
| `cleanup(slug)` | Remove workbench folder |
| `workbench_status()` | List currently checked-out articles |

### Link Analysis Functions

| Function | Description |
|----------|-------------|
| `extract_links_for_article(slug)` | Parse HTML for links, store in `article_links` |
| `extract_all_links()` | Extract links from all articles |
| `find_broken_links(max_workers=5)` | Test URLs with HEAD requests, report 404s |
| `find_link_opportunities(slug)` | Find topically related articles for linking |
| `generate_link_map(output_path)` | Auto-generate `internal-links-map.md` |

## Workflows

### Initial Setup
```python
from data_sources.modules.content_library import init_db, sync_all
init_db()
sync_all()  # Pulls all articles from WordPress
```

### Search for Content
```python
from data_sources.modules.content_library import search
results = search('COBOL modernization')
# Returns: [{slug, title, url, snippet, word_count, ...}, ...]
```

### Edit an Article
```python
from data_sources.modules.content_library import checkout, checkin

# 1. Check out (syncs fresh from WordPress)
checkout('article-slug')

# 2. Edit workbench/article-slug/original.html in IDE

# 3. Check in and push
checkin('article-slug', push=True)  # Updates DB + pushes to WordPress + cleans up
```

### Find Broken Links
```python
from data_sources.modules.content_library import find_broken_links
broken = find_broken_links()
# Returns: [{source_slug, target_url, anchor_text, status_code, error}, ...]
```

### Generate Internal Links Map
```python
from data_sources.modules.content_library import generate_link_map
generate_link_map()  # Writes to context/internal-links-map.md
```

## CLI Usage

All functions are also available via command line:

```bash
.venv/bin/python data_sources/modules/content_library.py init
.venv/bin/python data_sources/modules/content_library.py sync
.venv/bin/python data_sources/modules/content_library.py sync article-slug
.venv/bin/python data_sources/modules/content_library.py search "COBOL migration"
.venv/bin/python data_sources/modules/content_library.py list
.venv/bin/python data_sources/modules/content_library.py checkout article-slug
.venv/bin/python data_sources/modules/content_library.py checkin article-slug --push
.venv/bin/python data_sources/modules/content_library.py broken
.venv/bin/python data_sources/modules/content_library.py linkmap
.venv/bin/python data_sources/modules/content_library.py status
.venv/bin/python data_sources/modules/content_library.py count
```

### Optimize a Published Article
```python
from data_sources.modules.content_library import sync_article, checkout

# 1. Sync fresh from WordPress
sync_article('https://yoursite.com/blog/category/article-slug/')

# 2. Check out to workbench (fresh=False since we just synced)
checkout('article-slug', fresh=False)

# 3. Run /optimize on the workbench files
#    Reads workbench/article-slug/article.md + metadata.json
#    Saves optimization-report.md to the same workbench folder
```

The `/optimize` command accepts URLs and slugs directly — it handles steps 1-2 automatically before running the SEO audit.

## Important Notes

- The database is a **mirror**, not the source of truth. WordPress is canonical.
- `checkout()` re-syncs from WordPress before creating files to ensure freshness.
- Search returns **snippets**, not full content — this prevents LLM context overload.
- `content.db` and `content/workbench/` are both gitignored.
- The `content/published/` folder is a legacy system kept alongside. New editing goes through `content/workbench/`.
- The database can always be rebuilt: delete `content.db` and run `sync_all()`.
