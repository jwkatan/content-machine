"""
Content Library

A queryable SQLite mirror of all WordPress articles. WordPress is the source of truth;
this database is a derived index that can be rebuilt from WordPress at any time.

Architecture:
- Library (content.db): All articles with full content, metadata, and extracted links.
- Workbench (content/workbench/{slug}/): Temporary checkout for articles being actively edited.

Usage:
    from data_sources.modules.content_library import (
        init_db, sync_all, sync_article, search, list_articles, get_article,
        checkout, checkin, cleanup,
        extract_links, extract_all_links, find_broken_links,
        find_link_opportunities, generate_link_map
    )

    # Initial sync
    init_db()
    sync_all()

    # Search
    results = search('COBOL modernization')

    # Edit workflow
    checkout('article-slug')
    # ... edit content/workbench/article-slug/original.html ...
    checkin('article-slug', push=True)
"""

import os
import re
import json
import sqlite3
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from html import unescape
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed

import sys

# Support both package import and direct script execution
try:
    from data_sources.modules.wordpress_client import WordPressClient
except ModuleNotFoundError:
    # When run directly as a script, add project root to path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from data_sources.modules.wordpress_client import WordPressClient


# --- Paths ---

_PROJECT_ROOT = Path(__file__).parent.parent.parent
_DB_PATH = _PROJECT_ROOT / "data_sources" / "db" / "content.db"
_WORKBENCH_DIR = _PROJECT_ROOT / "content" / "workbench"


# --- Schema ---

_SCHEMA = """
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    meta_title TEXT,
    meta_description TEXT,
    url TEXT,
    wordpress_post_id INTEGER UNIQUE,
    wordpress_post_type TEXT DEFAULT 'article',
    wordpress_status TEXT,
    publication_date TEXT,
    modified_date TEXT,
    content_html TEXT,
    content_markdown TEXT,
    word_count INTEGER,
    last_synced_at TEXT,
    synced_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_articles_status ON articles(wordpress_status);
CREATE INDEX IF NOT EXISTS idx_articles_post_id ON articles(wordpress_post_id);

CREATE TABLE IF NOT EXISTS article_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_article_id INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    target_url TEXT NOT NULL,
    target_article_id INTEGER REFERENCES articles(id),
    anchor_text TEXT,
    is_internal BOOLEAN DEFAULT 0,
    last_checked_at TEXT,
    last_status_code INTEGER
);

CREATE INDEX IF NOT EXISTS idx_links_source ON article_links(source_article_id);
CREATE INDEX IF NOT EXISTS idx_links_target ON article_links(target_article_id);
CREATE INDEX IF NOT EXISTS idx_links_url ON article_links(target_url);
"""

_FTS_SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS articles_fts USING fts5(
    slug,
    title,
    content_markdown,
    meta_title,
    meta_description,
    content='articles',
    content_rowid='id'
);
"""

# FTS triggers to keep the index in sync with the articles table
_FTS_TRIGGERS = """
CREATE TRIGGER IF NOT EXISTS articles_ai AFTER INSERT ON articles BEGIN
    INSERT INTO articles_fts(rowid, slug, title, content_markdown, meta_title, meta_description)
    VALUES (new.id, new.slug, new.title, new.content_markdown, new.meta_title, new.meta_description);
END;

CREATE TRIGGER IF NOT EXISTS articles_ad AFTER DELETE ON articles BEGIN
    INSERT INTO articles_fts(articles_fts, rowid, slug, title, content_markdown, meta_title, meta_description)
    VALUES ('delete', old.id, old.slug, old.title, old.content_markdown, old.meta_title, old.meta_description);
END;

CREATE TRIGGER IF NOT EXISTS articles_au AFTER UPDATE ON articles BEGIN
    INSERT INTO articles_fts(articles_fts, rowid, slug, title, content_markdown, meta_title, meta_description)
    VALUES ('delete', old.id, old.slug, old.title, old.content_markdown, old.meta_title, old.meta_description);
    INSERT INTO articles_fts(rowid, slug, title, content_markdown, meta_title, meta_description)
    VALUES (new.id, new.slug, new.title, new.content_markdown, new.meta_title, new.meta_description);
END;
"""


# --- Database Connection ---

def _get_db() -> sqlite3.Connection:
    """Get a database connection with row factory enabled."""
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def init_db():
    """
    Create the database schema. Idempotent — safe to call multiple times.
    """
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = _get_db()
    try:
        conn.executescript(_SCHEMA)
        conn.executescript(_FTS_SCHEMA)
        conn.executescript(_FTS_TRIGGERS)
        conn.commit()
        print(f"Database initialized at {_DB_PATH}")
    finally:
        conn.close()


# --- Sync ---

def sync_all(post_type: str = 'article') -> Dict[str, Any]:
    """
    Fetch all articles from WordPress and upsert into the database.
    Paginates through the REST API. Prints progress.

    Args:
        post_type: WordPress post type to sync (default: 'article')

    Returns:
        Dict with 'synced', 'errors', 'total' counts
    """
    init_db()
    client = WordPressClient()

    synced = 0
    errors = []
    page = 1
    total_pages = None

    print(f"Syncing all '{post_type}' posts from {client.site_url}...")

    while True:
        endpoint = f"/wp-json/wp/v2/{post_type}?context=edit&per_page=100&page={page}"
        success, result = client._api_request(endpoint)

        if not success:
            # If first page fails, try alternate post type
            if page == 1 and post_type == 'article':
                print(f"Post type '{post_type}' not found, trying 'posts'...")
                return sync_all(post_type='posts')
            errors.append(f"Page {page}: {result}")
            break

        if not result:
            break

        for post in result:
            try:
                post_data = _extract_post_data(post, client, post_type)
                _upsert_article(post_data)
                synced += 1
                print(f"  Synced {synced}: {post_data['slug']}")
            except Exception as e:
                slug = post.get('slug', 'unknown')
                errors.append(f"{slug}: {str(e)}")
                print(f"  Error syncing {slug}: {e}")

        # Check if there are more pages
        if len(result) < 100:
            break
        page += 1

    # Extract links for all synced articles
    print("Extracting links from all articles...")
    extract_all_links()

    summary = {'synced': synced, 'errors': len(errors), 'total': synced + len(errors)}
    print(f"\nSync complete: {synced} articles synced, {len(errors)} errors")
    if errors:
        for err in errors[:5]:
            print(f"  Error: {err}")
        if len(errors) > 5:
            print(f"  ... and {len(errors) - 5} more errors")

    return summary


def sync_article(slug_or_url: str) -> Tuple[bool, str]:
    """
    Fetch and upsert a single article from WordPress.

    Args:
        slug_or_url: Article slug or full WordPress URL

    Returns:
        Tuple of (success, message)
    """
    init_db()
    client = WordPressClient()

    # If it looks like a URL, use fetch_post_by_url
    if slug_or_url.startswith('http'):
        success, post_data = client.fetch_post_by_url(slug_or_url)
        if not success:
            return False, post_data
    else:
        # Try as slug across post types
        post_data = None
        for pt in ['article', 'posts', 'pages']:
            endpoint = f"/wp-json/wp/v2/{pt}?slug={quote(slug_or_url)}&context=edit"
            success, result = client._api_request(endpoint)
            if success and result and len(result) > 0:
                post_data = _extract_post_data(result[0], client, pt)
                break

        if not post_data:
            return False, f"No article found with slug: {slug_or_url}"

    # If we got post_data from fetch_post_by_url, normalize it
    if 'content_html' not in post_data:
        # post_data came from fetch_post_by_url — normalize field names
        normalized = {
            'slug': post_data.get('slug', ''),
            'title': post_data.get('title', 'Untitled'),
            'meta_title': post_data.get('meta_title', ''),
            'meta_description': post_data.get('meta_description', ''),
            'url': post_data.get('url', ''),
            'wordpress_post_id': post_data.get('id'),
            'wordpress_post_type': post_data.get('post_type', 'article'),
            'wordpress_status': post_data.get('status', ''),
            'publication_date': post_data.get('date', '')[:10],
            'modified_date': post_data.get('modified', ''),
            'content_html': post_data.get('content', ''),
            'content_markdown': client.html_to_markdown(post_data.get('content', '')),
        }
        post_data = normalized

    _upsert_article(post_data)
    extract_links_for_article(post_data['slug'])
    return True, f"Synced: {post_data['slug']}"


def _extract_post_data(post: Dict, client: WordPressClient, post_type: str) -> Dict:
    """Extract normalized article data from a WordPress API response."""
    content_obj = post.get('content', {})
    content_html = content_obj.get('raw', '') or content_obj.get('rendered', '')
    content_markdown = client.html_to_markdown(content_html)

    title = unescape(
        post.get('title', {}).get('raw', '') or
        post.get('title', {}).get('rendered', 'Untitled')
    )

    # Yoast SEO meta
    yoast = post.get('yoast_head_json', {})
    meta_title = yoast.get('title', title) if yoast else title
    meta_description = ''
    if yoast:
        meta_description = yoast.get('description', '')
    if not meta_description:
        excerpt = unescape(post.get('excerpt', {}).get('rendered', ''))
        meta_description = re.sub(r'<[^>]+>', '', excerpt).strip()[:160]

    return {
        'slug': post.get('slug', ''),
        'title': title,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'url': post.get('link', ''),
        'wordpress_post_id': post.get('id'),
        'wordpress_post_type': post_type,
        'wordpress_status': post.get('status', ''),
        'publication_date': post.get('date', '')[:10],
        'modified_date': post.get('modified', ''),
        'content_html': content_html,
        'content_markdown': content_markdown,
    }


def _upsert_article(post_data: Dict):
    """Insert or update an article in the database."""
    word_count = len(post_data.get('content_markdown', '').split())
    now = datetime.now().isoformat()

    conn = _get_db()
    try:
        conn.execute("""
            INSERT INTO articles (
                slug, title, meta_title, meta_description, url,
                wordpress_post_id, wordpress_post_type, wordpress_status,
                publication_date, modified_date,
                content_html, content_markdown, word_count,
                last_synced_at, synced_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(slug) DO UPDATE SET
                title=excluded.title,
                meta_title=excluded.meta_title,
                meta_description=excluded.meta_description,
                url=excluded.url,
                wordpress_post_id=excluded.wordpress_post_id,
                wordpress_post_type=excluded.wordpress_post_type,
                wordpress_status=excluded.wordpress_status,
                publication_date=excluded.publication_date,
                modified_date=excluded.modified_date,
                content_html=excluded.content_html,
                content_markdown=excluded.content_markdown,
                word_count=excluded.word_count,
                last_synced_at=excluded.last_synced_at
        """, (
            post_data['slug'], post_data['title'],
            post_data.get('meta_title', ''), post_data.get('meta_description', ''),
            post_data.get('url', ''),
            post_data.get('wordpress_post_id'),
            post_data.get('wordpress_post_type', 'article'),
            post_data.get('wordpress_status', ''),
            post_data.get('publication_date', ''),
            post_data.get('modified_date', ''),
            post_data.get('content_html', ''),
            post_data.get('content_markdown', ''),
            word_count, now, now
        ))
        conn.commit()
    finally:
        conn.close()


# --- Search ---

def search(query: str, limit: int = 20) -> List[Dict]:
    """
    Full-text search across all articles. Returns snippets, not full content.

    Args:
        query: Search query (supports FTS5 syntax: phrases, AND, OR, NOT)
        limit: Max results to return

    Returns:
        List of dicts with slug, title, url, snippet, word_count, last_synced_at
    """
    conn = _get_db()
    try:
        rows = conn.execute("""
            SELECT
                a.slug, a.title, a.url, a.word_count,
                a.wordpress_status, a.publication_date, a.last_synced_at,
                snippet(articles_fts, 2, '**', '**', '...', 50) as snippet
            FROM articles_fts
            JOIN articles a ON a.id = articles_fts.rowid
            WHERE articles_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (query, limit)).fetchall()

        return [dict(row) for row in rows]
    finally:
        conn.close()


# --- List and Get ---

def list_articles(
    status: Optional[str] = None,
    sort_by: str = 'title',
    limit: int = 500
) -> List[Dict]:
    """
    List all articles with metadata (no content). For displaying article inventory.

    Args:
        status: Filter by wordpress_status (e.g., 'publish', 'draft')
        sort_by: Column to sort by ('title', 'publication_date', 'word_count', 'modified_date')
        limit: Max results

    Returns:
        List of dicts with slug, title, url, word_count, status, dates
    """
    allowed_sorts = {'title', 'publication_date', 'word_count', 'modified_date', 'slug'}
    if sort_by not in allowed_sorts:
        sort_by = 'title'

    conn = _get_db()
    try:
        query = """
            SELECT slug, title, url, word_count,
                   wordpress_status, wordpress_post_type,
                   publication_date, modified_date, last_synced_at
            FROM articles
        """
        params = []

        if status:
            query += " WHERE wordpress_status = ?"
            params.append(status)

        query += f" ORDER BY {sort_by}"
        query += " LIMIT ?"
        params.append(limit)

        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_article(slug: str, include_content: bool = False) -> Optional[Dict]:
    """
    Get a single article by slug.

    Args:
        slug: Article slug
        include_content: If True, include full content_html and content_markdown

    Returns:
        Article dict or None if not found
    """
    conn = _get_db()
    try:
        if include_content:
            row = conn.execute(
                "SELECT * FROM articles WHERE slug = ?", (slug,)
            ).fetchone()
        else:
            row = conn.execute("""
                SELECT slug, title, meta_title, meta_description, url,
                       wordpress_post_id, wordpress_post_type, wordpress_status,
                       publication_date, modified_date, word_count, last_synced_at
                FROM articles WHERE slug = ?
            """, (slug,)).fetchone()

        return dict(row) if row else None
    finally:
        conn.close()


def article_count() -> int:
    """Return the number of articles in the database."""
    conn = _get_db()
    try:
        return conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    finally:
        conn.close()


# --- Workbench (Checkout / Checkin) ---

def checkout(slug: str, fresh: bool = True) -> Tuple[bool, str]:
    """
    Check out an article to the workbench for editing.
    Creates content/workbench/{slug}/ with original.html, article.md, metadata.json.

    Args:
        slug: Article slug
        fresh: If True (default), re-sync from WordPress before checkout

    Returns:
        Tuple of (success, workbench_path or error_message)
    """
    # Optionally re-sync from WordPress for freshness
    if fresh:
        success, msg = sync_article(slug)
        if not success:
            # If sync fails, try to use existing database data
            print(f"Warning: Could not sync from WordPress ({msg}). Using cached data.")

    article = get_article(slug, include_content=True)
    if not article:
        return False, f"Article not found in database: {slug}. Run sync_all() first."

    # Create workbench folder
    workbench_path = _WORKBENCH_DIR / slug
    workbench_path.mkdir(parents=True, exist_ok=True)

    try:
        # Write original.html
        with open(workbench_path / 'original.html', 'w', encoding='utf-8') as f:
            f.write(article.get('content_html', ''))

        # Write article.md
        title = article.get('title', 'Untitled')
        markdown = article.get('content_markdown', '')
        with open(workbench_path / 'article.md', 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n{markdown}")

        # Write metadata.json
        metadata = {
            'meta_title': article.get('meta_title', ''),
            'meta_description': article.get('meta_description', ''),
            'url_slug': article.get('url', ''),
            'publication_date': article.get('publication_date', ''),
            'wordpress_post_id': article.get('wordpress_post_id'),
            'wordpress_post_type': article.get('wordpress_post_type', 'article'),
            'wordpress_status': article.get('wordpress_status', ''),
            'title': article.get('title', 'Untitled'),
        }
        with open(workbench_path / 'metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return True, str(workbench_path)

    except Exception as e:
        return False, f"Error creating workbench files: {e}"


def checkin(slug: str, push: bool = False) -> Tuple[bool, str]:
    """
    Check in an edited article from the workbench. Updates the database
    and optionally pushes to WordPress.

    Args:
        slug: Article slug
        push: If True, push to WordPress as draft. If False, only update database.

    Returns:
        Tuple of (success, message)
    """
    workbench_path = _WORKBENCH_DIR / slug

    if not workbench_path.exists():
        return False, f"No workbench folder found for: {slug}"

    original_path = workbench_path / 'original.html'
    article_path = workbench_path / 'article.md'
    metadata_path = workbench_path / 'metadata.json'

    # If article.md is newer than original.html (or original.html is missing),
    # regenerate Gutenberg HTML from the markdown before pushing.
    if article_path.exists():
        regen_needed = (
            not original_path.exists()
            or article_path.stat().st_mtime > original_path.stat().st_mtime
        )
        if regen_needed:
            import re as _re
            from data_sources.modules.wordpress_client import markdown_to_gutenberg
            with open(article_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            # Strip H1 title from markdown before converting — the title is sent
            # separately via metadata.json 'title' field in export_to_wordpress().
            # Including H1 in the body HTML causes title duplication on the page.
            md_content = _re.sub(r'^#\s+.+\n*', '', md_content, count=1)
            html_content = markdown_to_gutenberg(md_content)
            with open(original_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("Regenerated original.html from article.md (article.md was newer)")

    if not original_path.exists():
        return False, f"Neither original.html nor article.md found in content/workbench/{slug}/"

    # Read edited content
    with open(original_path, 'r', encoding='utf-8') as f:
        content_html = f.read()

    # Read metadata
    metadata = {}
    if metadata_path.exists():
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

    # Convert HTML to markdown
    client = WordPressClient.__new__(WordPressClient)
    client.site_url = ''
    content_markdown = client.html_to_markdown(content_html)

    # Update database
    now = datetime.now().isoformat()
    conn = _get_db()
    try:
        conn.execute("""
            UPDATE articles SET
                content_html = ?,
                content_markdown = ?,
                word_count = ?,
                last_synced_at = ?
            WHERE slug = ?
        """, (content_html, content_markdown, len(content_markdown.split()), now, slug))
        conn.commit()
    finally:
        conn.close()

    # Re-extract links from updated content
    extract_links_for_article(slug)

    # Optionally push to WordPress
    if push:
        from data_sources.modules.wordpress_client import export_to_wordpress
        success, result = export_to_wordpress(str(workbench_path), push=True)
        if not success:
            return False, f"Database updated but WordPress push failed: {result}"

        # Update sync timestamp
        conn = _get_db()
        try:
            conn.execute(
                "UPDATE articles SET last_synced_at = ? WHERE slug = ?",
                (datetime.now().isoformat(), slug)
            )
            conn.commit()
        finally:
            conn.close()

        # Clean up workbench
        cleanup(slug)
        return True, f"Checked in and pushed to WordPress. {result}"

    return True, f"Checked in to database (not pushed to WordPress). Workbench files kept at content/workbench/{slug}/"


def cleanup(slug: str) -> Tuple[bool, str]:
    """
    Remove workbench files for an article.

    Args:
        slug: Article slug

    Returns:
        Tuple of (success, message)
    """
    workbench_path = _WORKBENCH_DIR / slug
    if workbench_path.exists():
        shutil.rmtree(workbench_path)
        return True, f"Cleaned up content/workbench/{slug}/"
    return True, f"No workbench folder to clean up for {slug}"


def workbench_status() -> List[Dict]:
    """
    List articles currently checked out in the workbench.

    Returns:
        List of dicts with slug and file info
    """
    if not _WORKBENCH_DIR.exists():
        return []

    checked_out = []
    for item in _WORKBENCH_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            files = [f.name for f in item.iterdir() if f.is_file()]
            checked_out.append({
                'slug': item.name,
                'files': files,
                'path': str(item),
            })
    return checked_out


# --- Link Extraction ---

def extract_links_for_article(slug: str):
    """Extract and store all links from a single article's HTML content."""
    conn = _get_db()
    try:
        row = conn.execute(
            "SELECT id, content_html, url FROM articles WHERE slug = ?", (slug,)
        ).fetchone()
        if not row:
            return

        article_id = row['id']
        content_html = row['content_html'] or ''
        article_url = row['url'] or ''

        # Delete existing links for this article
        conn.execute("DELETE FROM article_links WHERE source_article_id = ?", (article_id,))

        # Parse links from HTML
        link_pattern = r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>'
        links = re.findall(link_pattern, content_html, re.DOTALL | re.IGNORECASE)

        # Determine site URL for internal link detection
        site_url = ''
        if article_url:
            from urllib.parse import urlparse
            parsed = urlparse(article_url)
            site_url = f"{parsed.scheme}://{parsed.netloc}"

        for href, anchor in links:
            anchor_text = re.sub(r'<[^>]+>', '', anchor).strip()
            is_internal = bool(site_url and href.startswith(site_url))

            # Try to match target to a known article
            target_article_id = None
            if is_internal:
                # Extract slug from URL
                segments = [s for s in href.rstrip('/').split('/') if s]
                if segments:
                    target_slug = segments[-1]
                    target = conn.execute(
                        "SELECT id FROM articles WHERE slug = ?", (target_slug,)
                    ).fetchone()
                    if target:
                        target_article_id = target['id']

            conn.execute("""
                INSERT INTO article_links (source_article_id, target_url, target_article_id, anchor_text, is_internal)
                VALUES (?, ?, ?, ?, ?)
            """, (article_id, href, target_article_id, anchor_text, is_internal))

        conn.commit()
    finally:
        conn.close()


def extract_all_links():
    """Extract links from all articles in the database."""
    conn = _get_db()
    try:
        slugs = [row['slug'] for row in conn.execute("SELECT slug FROM articles").fetchall()]
    finally:
        conn.close()

    for slug in slugs:
        extract_links_for_article(slug)


# --- Link Analysis ---

def find_broken_links(max_workers: int = 5, timeout: int = 10) -> List[Dict]:
    """
    Test all extracted links for broken URLs (404s, timeouts, etc.).
    Uses HEAD requests with concurrency limits.

    Args:
        max_workers: Number of concurrent HTTP workers
        timeout: Request timeout in seconds

    Returns:
        List of dicts with source_slug, target_url, anchor_text, status_code, error
    """
    conn = _get_db()
    try:
        rows = conn.execute("""
            SELECT al.id, al.target_url, al.anchor_text, al.is_internal,
                   a.slug as source_slug, a.title as source_title
            FROM article_links al
            JOIN articles a ON a.id = al.source_article_id
            WHERE al.last_checked_at IS NULL
               OR al.last_checked_at < datetime('now', '-7 days')
            ORDER BY al.is_internal DESC
        """).fetchall()
    finally:
        conn.close()

    if not rows:
        print("No links to check (all checked within the last 7 days).")
        return []

    # Deduplicate URLs for checking
    url_to_rows = {}
    for row in rows:
        url = row['target_url']
        if url not in url_to_rows:
            url_to_rows[url] = []
        url_to_rows[url].append(dict(row))

    unique_urls = list(url_to_rows.keys())
    print(f"Checking {len(unique_urls)} unique URLs from {len(rows)} total links...")

    broken = []
    checked = 0

    def check_url(url):
        try:
            req = Request(url, method='HEAD', headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            with urlopen(req, timeout=timeout) as resp:
                return url, resp.status, None
        except HTTPError as e:
            return url, e.code, None
        except URLError as e:
            return url, None, str(e.reason)
        except Exception as e:
            return url, None, str(e)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_url, url): url for url in unique_urls}
        for future in as_completed(futures):
            url, status_code, error = future.result()
            checked += 1

            if checked % 20 == 0:
                print(f"  Checked {checked}/{len(unique_urls)} URLs...")

            # Update all link records for this URL
            now = datetime.now().isoformat()
            conn = _get_db()
            try:
                conn.execute("""
                    UPDATE article_links SET last_checked_at = ?, last_status_code = ?
                    WHERE target_url = ?
                """, (now, status_code, url))
                conn.commit()
            finally:
                conn.close()

            # Report broken links
            is_broken = (
                (status_code and status_code >= 400) or
                (error and 'timeout' not in str(error).lower())
            )
            if is_broken:
                for link_row in url_to_rows[url]:
                    broken.append({
                        'source_slug': link_row['source_slug'],
                        'source_title': link_row['source_title'],
                        'target_url': url,
                        'anchor_text': link_row['anchor_text'],
                        'status_code': status_code,
                        'error': error,
                    })

    print(f"\nDone. {len(broken)} broken links found across {len(unique_urls)} unique URLs.")
    return broken


def find_link_opportunities(slug: str, limit: int = 10) -> List[Dict]:
    """
    Find articles that are topically related and could link to/from this article.
    Uses FTS5 to match on keywords from the article's title and meta description.

    Args:
        slug: Article slug to find opportunities for
        limit: Max suggestions

    Returns:
        List of dicts with slug, title, url, relevance snippet
    """
    article = get_article(slug)
    if not article:
        return []

    # Build a search query from the article's title words (skip common words)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                  'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                  'should', 'may', 'might', 'can', 'how', 'what', 'why', 'when', 'where',
                  'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'it', 'its',
                  'not', 'no', 'nor', 'if', 'then', 'than', 'so', 'as', 'from', 'into',
                  'top', 'best', 'vs', 'key', 'tips', 'guide', 'your'}
    title_words = [w.lower() for w in re.findall(r'\b\w+\b', article['title'])]
    keywords = [w for w in title_words if w not in stop_words and len(w) > 2]

    if not keywords:
        return []

    # Use OR for broader matching
    fts_query = ' OR '.join(keywords[:8])

    conn = _get_db()
    try:
        rows = conn.execute("""
            SELECT
                a.slug, a.title, a.url, a.word_count,
                snippet(articles_fts, 2, '**', '**', '...', 30) as relevance_snippet
            FROM articles_fts
            JOIN articles a ON a.id = articles_fts.rowid
            WHERE articles_fts MATCH ?
            AND a.slug != ?
            ORDER BY rank
            LIMIT ?
        """, (fts_query, slug, limit)).fetchall()

        # Check which of these already link to/from this article
        article_full = get_article(slug, include_content=False)
        existing_links = set()
        if article_full:
            article_id_row = conn.execute(
                "SELECT id FROM articles WHERE slug = ?", (slug,)
            ).fetchone()
            if article_id_row:
                for link in conn.execute(
                    "SELECT target_url FROM article_links WHERE source_article_id = ?",
                    (article_id_row['id'],)
                ).fetchall():
                    existing_links.add(link['target_url'])

        results = []
        for row in rows:
            row_dict = dict(row)
            row_dict['already_linked'] = row_dict.get('url', '') in existing_links
            results.append(row_dict)

        return results
    finally:
        conn.close()


def generate_link_map(output_path: Optional[str] = None) -> Tuple[bool, str]:
    """
    Auto-generate internal-links-map.md from the database.
    Groups articles by URL path categories (topic clusters).

    Args:
        output_path: Where to write the map. Defaults to context/internal-links-map.md

    Returns:
        Tuple of (success, message)
    """
    if not output_path:
        output_path = str(_PROJECT_ROOT / "context" / "internal-links-map.md")

    conn = _get_db()
    try:
        articles = conn.execute("""
            SELECT slug, title, url, meta_description, wordpress_status
            FROM articles
            WHERE wordpress_status = 'publish'
            ORDER BY url
        """).fetchall()
    finally:
        conn.close()

    if not articles:
        return False, "No published articles in database. Run sync_all() first."

    # Group by URL path category
    categories = {}
    for article in articles:
        url = article['url'] or ''
        # Extract category from URL path: /learn/{category}/{slug}
        segments = [s for s in url.rstrip('/').split('/') if s]
        category = 'Uncategorized'
        for i, seg in enumerate(segments):
            if seg == 'learn' and i + 1 < len(segments) - 1:
                category = segments[i + 1].replace('-', ' ').title()
                break

        if category not in categories:
            categories[category] = []
        categories[category].append(dict(article))

    # Build markdown
    lines = [
        "# Internal Links Map",
        "",
        "Auto-generated from the content library database. "
        f"Last updated: {datetime.now().strftime('%Y-%m-%d')}.",
        "",
        f"**Total published articles: {len(articles)}**",
        "",
        "---",
        "",
    ]

    for category in sorted(categories.keys()):
        arts = categories[category]
        lines.append(f"## {category}")
        lines.append("")
        for art in sorted(arts, key=lambda a: a['title']):
            lines.append(f"### {art['title']}")
            lines.append(f"- **URL**: {art['url']}")
            if art['meta_description']:
                lines.append(f"- **When to Link**: {art['meta_description'][:200]}")
            lines.append("")
        lines.append("---")
        lines.append("")

    # Best practices section
    lines.extend([
        "## Internal Linking Best Practices",
        "",
        "1. **Link Naturally**: Only link when genuinely relevant and helpful to the reader",
        "2. **Vary Anchor Text**: Use different phrases for the same destination URL",
        "3. **3-5 Links Per Post**: Aim for 3-5 strategic internal links in each blog post",
        "4. **Deep Linking**: Link to specific relevant pages, not just the homepage",
        "5. **Early Links Matter**: Links in the first few paragraphs carry more weight",
        "",
        "---",
        "",
        "*Auto-generated by content_library.py. Regenerate with `generate_link_map()`.*",
    ])

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return True, f"Generated link map with {len(articles)} articles at {output_path}"


# --- CLI ---

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python content_library.py init          - Initialize database")
        print("  python content_library.py sync          - Sync all articles from WordPress")
        print("  python content_library.py sync <slug>   - Sync a single article")
        print("  python content_library.py search <q>    - Full-text search")
        print("  python content_library.py list          - List all articles")
        print("  python content_library.py checkout <s>  - Check out article to workbench")
        print("  python content_library.py checkin <s>   - Check in from workbench")
        print("  python content_library.py links         - Extract all links")
        print("  python content_library.py broken        - Find broken links")
        print("  python content_library.py linkmap       - Generate internal links map")
        print("  python content_library.py status        - Show workbench status")
        print("  python content_library.py count         - Show article count")
        sys.exit(0)

    command = sys.argv[1]

    if command == 'init':
        init_db()

    elif command == 'sync':
        if len(sys.argv) >= 3:
            success, msg = sync_article(sys.argv[2])
            print(msg)
        else:
            sync_all()

    elif command == 'search' and len(sys.argv) >= 3:
        query = ' '.join(sys.argv[2:])
        results = search(query)
        if results:
            for r in results:
                print(f"\n{r['title']}")
                print(f"  URL: {r['url']}")
                print(f"  Words: {r['word_count']} | Status: {r['wordpress_status']}")
                print(f"  Snippet: {r['snippet']}")
        else:
            print("No results found.")

    elif command == 'list':
        articles = list_articles()
        for a in articles:
            print(f"  {a['slug']} — {a['title']} ({a['word_count']} words, {a['wordpress_status']})")
        print(f"\nTotal: {len(articles)} articles")

    elif command == 'checkout' and len(sys.argv) >= 3:
        success, msg = checkout(sys.argv[2])
        print(msg)

    elif command == 'checkin' and len(sys.argv) >= 3:
        push = '--push' in sys.argv
        success, msg = checkin(sys.argv[2], push=push)
        print(msg)

    elif command == 'links':
        extract_all_links()
        print("Links extracted for all articles.")

    elif command == 'broken':
        broken = find_broken_links()
        if broken:
            for b in broken:
                status = b['status_code'] or b['error']
                print(f"  [{status}] {b['target_url']}")
                print(f"    In: {b['source_slug']} — anchor: \"{b['anchor_text']}\"")
        else:
            print("No broken links found.")

    elif command == 'linkmap':
        success, msg = generate_link_map()
        print(msg)

    elif command == 'status':
        items = workbench_status()
        if items:
            for item in items:
                print(f"  {item['slug']} — files: {', '.join(item['files'])}")
        else:
            print("No articles checked out.")

    elif command == 'count':
        print(f"{article_count()} articles in database")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
