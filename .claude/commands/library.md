# Content Library

Manage the local content library — a queryable mirror of all WordPress articles.

## Argument: $ARGUMENTS

The argument specifies the operation. Supported operations:

### `sync`
Sync all articles from WordPress into the local database.

```python
from data_sources.modules.content_library import init_db, sync_all
init_db()
result = sync_all()
print(f"Synced {result['synced']} articles, {result['errors']} errors")
```

### `sync <slug-or-url>`
Sync a single article by slug or WordPress URL.

```python
from data_sources.modules.content_library import sync_article
success, msg = sync_article('<slug-or-url>')
print(msg)
```

### `search <query>`
Full-text search across all articles. Returns snippets, not full content.

```python
from data_sources.modules.content_library import search
results = search('<query>')
```

Present results as a table: title, URL, word count, snippet.

### `list`
List all articles in the database with metadata.

```python
from data_sources.modules.content_library import list_articles
articles = list_articles()
```

Present as a table: slug, title, word count, status, publication date.

### `checkout <slug>`
Check out an article to `content/workbench/{slug}/` for editing. Syncs fresh from WordPress first.

```python
from data_sources.modules.content_library import checkout
success, path = checkout('<slug>')
print(path)
```

After checkout, edit `content/workbench/{slug}/original.html` to preserve Gutenberg blocks. Use the `/wordpress-edit` workflow for block-level editing.

### `checkin <slug>`
Check in an edited article. Updates the database. Does NOT push to WordPress unless told to.

```python
from data_sources.modules.content_library import checkin
success, msg = checkin('<slug>')  # database only
# or
success, msg = checkin('<slug>', push=True)  # push to WordPress + cleanup
print(msg)
```

### `status`
Show what's currently checked out in the workbench.

```python
from data_sources.modules.content_library import workbench_status, article_count
checked_out = workbench_status()
count = article_count()
```

### `links`
Extract and analyze links across all articles.

```python
from data_sources.modules.content_library import extract_all_links, find_broken_links
extract_all_links()
broken = find_broken_links()
```

Present broken links grouped by source article.

### `link-opportunities <slug>`
Find articles that should link to/from a specific article.

```python
from data_sources.modules.content_library import find_link_opportunities
opportunities = find_link_opportunities('<slug>')
```

Present as a table with title, URL, relevance snippet, and whether already linked.

### `find-outdated`
Search for articles with potentially outdated content. Search for year references, known deprecated terms, etc.

```python
from data_sources.modules.content_library import search
# Search for specific year references
for year in ['2022', '2023', '2024']:
    results = search(year)
    if results:
        print(f"\nArticles mentioning {year}:")
        for r in results:
            print(f"  {r['title']} — {r['snippet']}")
```

The user may also specify custom terms to search for.

### `linkmap`
Auto-generate the internal links map from the database.

```python
from data_sources.modules.content_library import generate_link_map
success, msg = generate_link_map()
print(msg)
```

## Important Notes

- The database (`data_sources/content.db`) is a **mirror** of WordPress, not the source of truth.
- Search returns **snippets**, not full article content. Load full content only for specific articles.
- `checkout()` syncs fresh from WordPress before creating workbench files.
- Workbench files are temporary — clean them up after editing with `checkin(push=True)`.
- Run `sync` periodically to keep the database current with WordPress.
