"""
WordPress Client

Imports articles from WordPress and exports local content back to WordPress.
All exports are saved as drafts - never auto-published.

Setup:
1. Go to wp-admin > Users > Profile > Application Passwords
2. Create a new application password named "Claude Code SEO Machine"
3. Add to .env:
   WORDPRESS_SITE_URL=https://yoursite.com
   WORDPRESS_USERNAME=your-username
   WORDPRESS_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
"""

import os
import re
import json
import base64
import mimetypes
from datetime import datetime
from typing import Optional, Tuple, List, Dict, Any
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse, quote
from pathlib import Path
from html import unescape

# Load environment from config/.env
_env_path = Path(__file__).parent.parent / "config" / ".env"
if _env_path.exists():
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                if key not in os.environ:
                    os.environ[key] = value


class WordPressClient:
    """
    Client for WordPress REST API operations.
    Supports importing articles and exporting content as drafts.
    """

    def __init__(
        self,
        site_url: Optional[str] = None,
        username: Optional[str] = None,
        app_password: Optional[str] = None
    ):
        """
        Initialize WordPress client.

        Args:
            site_url: WordPress site URL (e.g., https://yoursite.com)
            username: WordPress username
            app_password: Application password from wp-admin
        """
        self.site_url = (site_url or os.getenv('WORDPRESS_SITE_URL', '')).rstrip('/')
        self.username = username or os.getenv('WORDPRESS_USERNAME', '')
        self.app_password = app_password or os.getenv('WORDPRESS_APP_PASSWORD', '')

        if not self.site_url:
            raise ValueError(
                "WordPress site URL not configured. "
                "Set WORDPRESS_SITE_URL in .env or pass site_url parameter."
            )

    def _get_auth_header(self) -> Dict[str, str]:
        """Get authorization header for API requests."""
        if not self.username or not self.app_password:
            return {}
        credentials = f"{self.username}:{self.app_password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return {'Authorization': f'Basic {encoded}'}

    def _api_request(
        self,
        endpoint: str,
        method: str = 'GET',
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Tuple[bool, Any]:
        """
        Make a request to the WordPress REST API.

        Args:
            endpoint: API endpoint (e.g., /wp-json/wp/v2/posts)
            method: HTTP method
            data: JSON data for POST/PUT requests
            headers: Additional headers

        Returns:
            Tuple of (success, response_data or error_message)
        """
        url = f"{self.site_url}{endpoint}"
        req_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            **self._get_auth_header(),
            **(headers or {})
        }

        try:
            body = json.dumps(data).encode('utf-8') if data else None
            request = Request(url, data=body, headers=req_headers, method=method)

            with urlopen(request, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return True, result

        except HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ''
            try:
                error_json = json.loads(error_body)
                error_msg = error_json.get('message', error_body)
            except:
                error_msg = error_body
            return False, f"API error {e.code}: {error_msg}"
        except URLError as e:
            return False, f"Network error: {e.reason}"
        except Exception as e:
            return False, f"Request error: {str(e)}"

    def extract_slug_from_url(self, url: str) -> str:
        """
        Extract the post slug from a WordPress URL.
        Handles various permalink structures.

        Args:
            url: Full WordPress URL

        Returns:
            Post slug
        """
        parsed = urlparse(url)
        path = parsed.path.strip('/')

        # Remove common prefixes (blog, learn, articles, etc.)
        # Take the last non-empty segment as the slug
        segments = [s for s in path.split('/') if s]
        if segments:
            return segments[-1]
        return ''

    def fetch_post_by_url(self, url: str, post_type: Optional[str] = None) -> Tuple[bool, Dict | str]:
        """
        Fetch a post from WordPress by its URL.

        Args:
            url: Full WordPress URL
            post_type: Optional post type to search (e.g., 'posts', 'article')
                       If not provided, tries common types automatically

        Returns:
            Tuple of (success, post_data or error_message)
        """
        slug = self.extract_slug_from_url(url)
        if not slug:
            return False, f"Could not extract slug from URL: {url}"

        # Post types to try (in order)
        if post_type:
            post_types = [post_type]
        else:
            # Try common types - 'article' is common for /learn/ content
            post_types = ['posts', 'article', 'pages']

        post = None
        found_post_type = None
        for pt in post_types:
            # Use context=edit to get raw content with Gutenberg block comments
            endpoint = f"/wp-json/wp/v2/{pt}?slug={quote(slug)}&context=edit"
            success, result = self._api_request(endpoint)

            if success and result and len(result) > 0:
                post = result[0]
                found_post_type = pt
                break

        if not post:
            return False, f"No post found with slug: {slug} (tried: {', '.join(post_types)})"

        # Get content - prefer raw (with blocks) over rendered
        content_obj = post.get('content', {})
        # Use raw content if available (preserves Gutenberg blocks)
        # Fall back to rendered if raw not available
        content = content_obj.get('raw', '') or content_obj.get('rendered', '')
        block_version = content_obj.get('block_version', 0)

        # Extract relevant data
        post_data = {
            'id': post.get('id'),
            'title': unescape(post.get('title', {}).get('raw', '') or post.get('title', {}).get('rendered', '')),
            'content': content,
            'block_version': block_version,  # Track if content has Gutenberg blocks
            'excerpt': unescape(post.get('excerpt', {}).get('rendered', '')),
            'slug': post.get('slug', ''),
            'url': post.get('link', url),
            'date': post.get('date', ''),
            'modified': post.get('modified', ''),
            'status': post.get('status', ''),
            'author': post.get('author', ''),
            'post_type': found_post_type,
        }

        # Try to get Yoast SEO data if available
        yoast = post.get('yoast_head_json', {})
        if yoast:
            post_data['meta_title'] = yoast.get('title', post_data['title'])
            post_data['meta_description'] = yoast.get('description', '')
        else:
            post_data['meta_title'] = post_data['title']
            post_data['meta_description'] = self._strip_html(post_data['excerpt'])

        return True, post_data

    def fetch_post_by_id(self, post_id: int) -> Tuple[bool, Dict | str]:
        """
        Fetch a post from WordPress by its ID.

        Args:
            post_id: WordPress post ID

        Returns:
            Tuple of (success, post_data or error_message)
        """
        endpoint = f"/wp-json/wp/v2/posts/{post_id}"
        success, result = self._api_request(endpoint)

        if not success:
            return False, result

        post = result
        post_data = {
            'id': post.get('id'),
            'title': unescape(post.get('title', {}).get('rendered', '')),
            'content': post.get('content', {}).get('rendered', ''),
            'excerpt': unescape(post.get('excerpt', {}).get('rendered', '')),
            'slug': post.get('slug', ''),
            'url': post.get('link', ''),
            'date': post.get('date', ''),
            'modified': post.get('modified', ''),
            'status': post.get('status', ''),
        }

        yoast = post.get('yoast_head_json', {})
        if yoast:
            post_data['meta_title'] = yoast.get('title', post_data['title'])
            post_data['meta_description'] = yoast.get('description', '')
        else:
            post_data['meta_title'] = post_data['title']
            post_data['meta_description'] = self._strip_html(post_data['excerpt'])

        return True, post_data

    def get_post_status(self, post_id: int, post_type: str = 'posts') -> Tuple[bool, str]:
        """
        Get the status of a post (draft, publish, pending, etc.).

        Args:
            post_id: WordPress post ID
            post_type: Post type endpoint (e.g., 'posts', 'article')

        Returns:
            Tuple of (success, status or error_message)
        """
        endpoint = f"/wp-json/wp/v2/{post_type}/{post_id}?_fields=status"
        success, result = self._api_request(endpoint)

        if not success:
            # Try 'article' if 'posts' failed
            if post_type == 'posts':
                return self.get_post_status(post_id, 'article')
            return False, result

        return True, result.get('status', 'unknown')

    def upload_media(
        self,
        file_path: str,
        alt_text: str = ""
    ) -> Tuple[bool, Dict | str]:
        """
        Upload an image to WordPress media library.

        Args:
            file_path: Local path to the image file
            alt_text: Alt text for the image

        Returns:
            Tuple of (success, {id, url} or error_message)
        """
        if not self.username or not self.app_password:
            return False, "WordPress credentials not configured for uploads"

        path = Path(file_path)
        if not path.exists():
            return False, f"File not found: {file_path}"

        content_type, _ = mimetypes.guess_type(str(path))
        if not content_type:
            content_type = 'application/octet-stream'

        try:
            with open(path, 'rb') as f:
                file_data = f.read()

            url = f"{self.site_url}/wp-json/wp/v2/media"
            headers = {
                'Content-Type': content_type,
                'Content-Disposition': f'attachment; filename="{path.name}"',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                **self._get_auth_header()
            }

            request = Request(url, data=file_data, headers=headers, method='POST')

            with urlopen(request, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                media_id = result.get('id')
                media_url = result.get('source_url', '')

                # Set alt text if provided
                if alt_text and media_id:
                    self._api_request(
                        f"/wp-json/wp/v2/media/{media_id}",
                        method='POST',
                        data={'alt_text': alt_text}
                    )

                return True, {'id': media_id, 'url': media_url}

        except HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ''
            return False, f"Upload error {e.code}: {error_body}"
        except URLError as e:
            return False, f"Network error: {e.reason}"
        except Exception as e:
            return False, f"Upload error: {str(e)}"

    def update_post_to_draft(
        self,
        post_id: int,
        content: Optional[str] = None,
        title: Optional[str] = None,
        meta_description: Optional[str] = None,
        post_type: str = 'posts',
        new_slug: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Update a post and ensure it's saved as draft.
        If the post is published, it will be moved to draft first.

        Args:
            post_id: WordPress post ID
            content: New HTML content (optional)
            title: New title (optional)
            meta_description: SEO description (included in success message for manual paste)
            post_type: Post type endpoint (e.g., 'posts', 'article')
            new_slug: New URL slug (optional). If provided, the old slug gets a 301 redirect.

        Returns:
            Tuple of (success, preview_url or error_message)
        """
        if not self.username or not self.app_password:
            return False, "WordPress credentials not configured for updates"

        # Check current status
        success, status = self.get_post_status(post_id, post_type)
        if not success:
            return False, f"Could not get post status: {status}"

        # If changing slug, capture the old one first for redirect
        old_slug = None
        if new_slug:
            slug_success, slug_result = self._api_request(
                f"/wp-json/wp/v2/{post_type}/{post_id}",
                method='GET'
            )
            if slug_success:
                old_slug = slug_result.get('slug')
                old_link = slug_result.get('link', '')

        # Build update data - always set to draft, with current date
        update_data = {
            'status': 'draft',
            'date': datetime.now().isoformat(),
        }

        if content:
            update_data['content'] = content
        if title:
            update_data['title'] = title
        if new_slug:
            update_data['slug'] = new_slug

        # Update the post
        endpoint = f"/wp-json/wp/v2/{post_type}/{post_id}"
        success, result = self._api_request(endpoint, method='POST', data=update_data)

        if not success:
            # Try 'article' if 'posts' failed
            if post_type == 'posts':
                return self.update_post_to_draft(post_id, content, title, meta_description, 'article', new_slug)
            return False, result

        # Create redirect from old slug to new slug
        if new_slug and old_slug and old_slug != new_slug and old_link:
            # Extract the path from the old link
            from urllib.parse import urlparse
            old_path = urlparse(old_link).path
            new_link = result.get('link', '')
            if old_path and new_link:
                redirect_ok, redirect_msg = self.create_redirect(old_path, new_link)
                if redirect_ok:
                    print(f"Created 301 redirect: {old_path} → {new_link}")
                else:
                    print(f"Warning: Could not create redirect: {redirect_msg}")

        # Get preview URL
        preview_url = result.get('link', '')
        if 'draft' in result.get('status', ''):
            # For drafts, construct preview URL with post_type for custom types
            if post_type != 'posts':
                preview_url = f"{self.site_url}/?post_type={post_type}&p={post_id}&preview=true"
            else:
                preview_url = f"{self.site_url}/?p={post_id}&preview=true"

        was_published = status == 'publish'
        message = f"{'Moved to draft and updated' if was_published else 'Updated as draft'}. Preview: {preview_url}"

        return True, message

    def create_redirect(self, from_path: str, to_url: str, http_code: int = 301) -> Tuple[bool, str]:
        """
        Create a redirect using the Redirection plugin API.

        Args:
            from_path: Source path (e.g., /learn/category/old-slug)
            to_url: Full destination URL (e.g., https://site.com/learn/category/new-slug)
            http_code: HTTP redirect code (default 301 permanent)

        Returns:
            Tuple of (success, message)
        """
        success, result = self._api_request(
            '/wp-json/redirection/v1/redirect',
            method='POST',
            data={
                'url': from_path,
                'action_data': {'url': to_url},
                'action_type': 'url',
                'action_code': http_code,
                'match_type': 'url',
                'group_id': 1
            }
        )
        if success:
            items = result.get('items', [])
            if items:
                return True, f"Redirect created (ID {items[0].get('id')}): {from_path} → {to_url}"
            return True, f"Redirect created: {from_path} → {to_url}"
        return False, result

    # Cache file for categories and authors (avoids API calls on every push)
    _CACHE_PATH = Path(__file__).parent.parent / 'config' / 'wp_cache.json'

    def _load_cache(self) -> dict:
        """Load the local WordPress cache file."""
        if self._CACHE_PATH.exists():
            with open(self._CACHE_PATH, 'r') as f:
                return json.load(f)
        return {}

    def _save_cache(self, cache: dict):
        """Save the local WordPress cache file."""
        self._CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(self._CACHE_PATH, 'w') as f:
            json.dump(cache, f, indent=2)

    def get_categories(self, post_type: str = 'posts', refresh: bool = False) -> Tuple[bool, list | str]:
        """
        Get available categories. Uses local cache; pass refresh=True to fetch from WordPress.

        Args:
            post_type: Post type ('posts' or 'article')
            refresh: If True, fetch fresh from WordPress and update cache.

        Returns:
            Tuple of (success, [{id, name, slug, count}] or error_message)
        """
        cache_key = f'categories_{post_type}'
        cache = self._load_cache()

        if not refresh and cache_key in cache:
            return True, cache[cache_key]

        # Fetch from WordPress
        if post_type == 'posts':
            endpoint = "/wp-json/wp/v2/categories?per_page=100"
        else:
            endpoint = f"/wp-json/wp/v2/{post_type}-category?per_page=100"

        success, result = self._api_request(endpoint, method='GET')
        if not success:
            # Fall back to cache if available
            if cache_key in cache:
                return True, cache[cache_key]
            return False, result

        categories = sorted(
            [{'id': c['id'], 'name': c['name'], 'slug': c['slug'], 'count': c.get('count', 0)} for c in result],
            key=lambda c: c['name']
        )
        cache[cache_key] = categories
        self._save_cache(cache)
        return True, categories

    def get_authors(self, refresh: bool = False) -> Tuple[bool, list | str]:
        """
        Get available authors. Uses local cache; pass refresh=True to fetch from WordPress.

        Args:
            refresh: If True, fetch fresh from WordPress and update cache.

        Returns:
            Tuple of (success, [{id, name, slug}] or error_message)
        """
        cache_key = 'authors'
        cache = self._load_cache()

        if not refresh and cache_key in cache:
            return True, cache[cache_key]

        success, result = self._api_request('/wp-json/wp/v2/users?per_page=100', method='GET')
        if not success:
            if cache_key in cache:
                return True, cache[cache_key]
            return False, result

        authors = sorted(
            [{'id': u['id'], 'name': u['name'], 'slug': u.get('slug', '')} for u in result],
            key=lambda a: a['name']
        )
        cache[cache_key] = authors
        self._save_cache(cache)
        return True, authors

    def refresh_cache(self) -> str:
        """Refresh all cached data (categories and authors) from WordPress."""
        results = []
        for pt in ['posts', 'article']:
            success, data = self.get_categories(post_type=pt, refresh=True)
            if success:
                results.append(f"  {pt} categories: {len(data)}")
            else:
                results.append(f"  {pt} categories: FAILED ({data})")

        success, data = self.get_authors(refresh=True)
        if success:
            results.append(f"  authors: {len(data)}")
        else:
            results.append(f"  authors: FAILED ({data})")

        return "Cache refreshed:\n" + "\n".join(results)

    def create_draft(
        self,
        title: str,
        content: str,
        post_type: str = 'posts',
        meta_description: Optional[str] = None,
        slug: Optional[str] = None,
        categories: Optional[list] = None,
        author: Optional[int] = None,
        featured_media: Optional[int] = None,
    ) -> Tuple[bool, Dict | str]:
        """
        Create a new WordPress post as a draft.

        Args:
            title: Post title
            content: Post HTML content (ideally Gutenberg block format)
            post_type: WordPress post type ('posts' for blog, 'article' for learn)
            meta_description: SEO description (included in success message for manual paste)
            slug: URL slug (auto-generated from title if not provided)
            categories: List of category IDs to assign
            author: WordPress user ID for the post author
            featured_media: WordPress media ID to set as featured image

        Returns:
            Tuple of (success, {id, url, preview_url, slug} or error_message)
        """
        post_data = {
            'title': title,
            'content': content,
            'status': 'draft',
            'date': datetime.now().isoformat(),
        }
        if slug:
            post_data['slug'] = slug
        if categories:
            cat_key = 'categories' if post_type == 'posts' else f'{post_type}-category'
            post_data[cat_key] = categories
        if author:
            post_data['author'] = author
        if featured_media:
            post_data['featured_media'] = featured_media

        endpoint = f"/wp-json/wp/v2/{post_type}"
        success, result = self._api_request(endpoint, method='POST', data=post_data)

        if not success:
            # Try alternate post type
            if post_type == 'article':
                return self.create_draft(title, content, 'posts', meta_description, slug, categories, author, featured_media)
            return False, result

        post_id = result.get('id')
        post_slug = result.get('slug', '')
        if post_type != 'posts':
            preview_url = f"{self.site_url}/?post_type={post_type}&p={post_id}&preview=true"
        else:
            preview_url = f"{self.site_url}/?p={post_id}&preview=true"

        return True, {
            'id': post_id,
            'slug': post_slug,
            'url': result.get('link', ''),
            'preview_url': preview_url,
            'post_type': post_type,
        }

    def _strip_html(self, html: str) -> str:
        """Remove HTML tags from a string."""
        clean = re.sub(r'<[^>]+>', '', html)
        return unescape(clean).strip()

    def html_to_markdown(self, html: str) -> str:
        """
        Convert WordPress HTML to markdown.

        Args:
            html: WordPress HTML content

        Returns:
            Markdown content
        """
        content = html

        # Remove WordPress block comments
        content = re.sub(r'<!--\s*/?wp:[^>]+-->', '', content)

        # Handle line breaks first
        content = content.replace('<br>', '\n')
        content = content.replace('<br/>', '\n')
        content = content.replace('<br />', '\n')

        # Headings (process h1-h6)
        for i in range(1, 7):
            pattern = rf'<h{i}[^>]*>(.*?)</h{i}>'
            content = re.sub(pattern, r'\n' + '#' * i + r' \1\n', content, flags=re.DOTALL | re.IGNORECASE)

        # Bold
        content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.DOTALL | re.IGNORECASE)

        # Italic
        content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content, flags=re.DOTALL | re.IGNORECASE)

        # Inline code
        content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', content, flags=re.DOTALL | re.IGNORECASE)

        # Links
        content = re.sub(
            r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
            r'[\2](\1)',
            content,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Images
        content = re.sub(
            r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*/?>',
            r'![\2](\1)',
            content,
            flags=re.IGNORECASE
        )
        content = re.sub(
            r'<img\s+[^>]*alt=["\']([^"\']*)["\'][^>]*src=["\']([^"\']+)["\'][^>]*/?>',
            r'![\1](\2)',
            content,
            flags=re.IGNORECASE
        )
        content = re.sub(
            r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*/?>',
            r'![](\1)',
            content,
            flags=re.IGNORECASE
        )

        # Code blocks (pre)
        content = re.sub(
            r'<pre[^>]*>(.*?)</pre>',
            r'\n```\n\1\n```\n',
            content,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Unordered lists
        def process_ul(match):
            items = re.findall(r'<li[^>]*>(.*?)</li>', match.group(1), flags=re.DOTALL | re.IGNORECASE)
            return '\n' + '\n'.join(f'- {self._strip_html(item).strip()}' for item in items) + '\n'

        content = re.sub(r'<ul[^>]*>(.*?)</ul>', process_ul, content, flags=re.DOTALL | re.IGNORECASE)

        # Ordered lists
        def process_ol(match):
            items = re.findall(r'<li[^>]*>(.*?)</li>', match.group(1), flags=re.DOTALL | re.IGNORECASE)
            return '\n' + '\n'.join(f'{i+1}. {self._strip_html(item).strip()}' for i, item in enumerate(items)) + '\n'

        content = re.sub(r'<ol[^>]*>(.*?)</ol>', process_ol, content, flags=re.DOTALL | re.IGNORECASE)

        # Blockquotes
        content = re.sub(
            r'<blockquote[^>]*>(.*?)</blockquote>',
            lambda m: '\n' + '\n'.join(f'> {line}' for line in self._strip_html(m.group(1)).split('\n') if line.strip()) + '\n',
            content,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Paragraphs
        content = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\1\n', content, flags=re.DOTALL | re.IGNORECASE)

        # Divs and other block elements - just add line breaks
        content = re.sub(r'<div[^>]*>(.*?)</div>', r'\n\1\n', content, flags=re.DOTALL | re.IGNORECASE)

        # Remove remaining HTML tags
        content = re.sub(r'<[^>]+>', '', content)

        # Unescape HTML entities
        content = unescape(content)

        # Clean up whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = re.sub(r' +', ' ', content)
        content = content.strip()

        return content

    def save_post_to_published(
        self,
        post_data: Dict,
        published_dir: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Save a WordPress post to a folder with markdown and original HTML.

        Creates a folder structure:
            content/published/{slug}/
                article.md      - Markdown version for editing
                original.html   - Raw WordPress HTML for perfect export
                metadata.json   - Post metadata

        Args:
            post_data: Post data from fetch_post_by_url
            published_dir: Directory to save to (defaults to content/published/)

        Returns:
            Tuple of (success, folder_path or error_message)
        """
        if not published_dir:
            # Default to content/published/ relative to project root
            published_dir = Path(__file__).parent.parent.parent / "content" / "published"

        published_dir = Path(published_dir)
        published_dir.mkdir(parents=True, exist_ok=True)

        # Create folder for this article
        slug = post_data.get('slug', 'untitled')
        article_dir = published_dir / slug
        article_dir.mkdir(parents=True, exist_ok=True)

        # Convert content to markdown for editing
        markdown_content = self.html_to_markdown(post_data.get('content', ''))

        # Build metadata
        date_str = post_data.get('date', '')[:10] or datetime.now().strftime('%Y-%m-%d')

        meta_desc = post_data.get('meta_description', '')
        if not meta_desc:
            meta_desc = markdown_content[:160].replace('\n', ' ').strip()
            if len(markdown_content) > 160:
                meta_desc += '...'

        metadata = {
            'meta_title': post_data.get('meta_title', post_data.get('title', '')),
            'meta_description': meta_desc,
            'url_slug': post_data.get('url', ''),
            'publication_date': date_str,
            'wordpress_post_id': post_data.get('id', ''),
            'wordpress_post_type': post_data.get('post_type', 'posts'),
            'wordpress_status': post_data.get('status', ''),
            'wordpress_block_version': post_data.get('block_version', 0),  # 0=classic, 1+=Gutenberg
            'title': post_data.get('title', 'Untitled'),
        }

        try:
            # Save metadata.json
            with open(article_dir / 'metadata.json', 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            # Save original.html (raw WordPress content for perfect round-trip)
            with open(article_dir / 'original.html', 'w', encoding='utf-8') as f:
                f.write(post_data.get('content', ''))

            # Save article.md (markdown version for editing)
            title = post_data.get('title', 'Untitled')
            markdown_full = f"# {title}\n\n{markdown_content}"
            with open(article_dir / 'article.md', 'w', encoding='utf-8') as f:
                f.write(markdown_full)

            return True, str(article_dir)
        except Exception as e:
            return False, f"Error saving files: {str(e)}"

    def process_content_images(
        self,
        content: str,
        base_path: str
    ) -> Tuple[str, List[str]]:
        """
        Find local images in markdown content, upload to WordPress,
        and replace paths with WordPress URLs.

        Args:
            content: Markdown content
            base_path: Base path for resolving relative image paths

        Returns:
            Tuple of (updated_content, list_of_uploaded_urls)
        """
        uploaded_urls = []
        base_path = Path(base_path)

        # Find all markdown images: ![alt](path)
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

        def replace_image(match):
            alt_text = match.group(1)
            image_path = match.group(2)

            # Skip if already a full URL on WordPress
            if image_path.startswith('http'):
                if self.site_url and self.site_url in image_path:
                    return match.group(0)  # Already on WordPress
                # External URL - leave as-is
                return match.group(0)

            # Resolve local path
            if image_path.startswith('./'):
                image_path = image_path[2:]

            full_path = base_path / image_path
            if not full_path.exists():
                # Try relative to published/images
                alt_path = base_path.parent / "images" / Path(image_path).name
                if alt_path.exists():
                    full_path = alt_path
                else:
                    print(f"Warning: Image not found: {full_path}")
                    return match.group(0)

            # Upload to WordPress
            success, result = self.upload_media(str(full_path), alt_text=alt_text)
            if success:
                uploaded_urls.append(result['url'])
                return f'![{alt_text}]({result["url"]})'
            else:
                print(f"Warning: Failed to upload {full_path}: {result}")
                return match.group(0)

        updated_content = re.sub(image_pattern, replace_image, content)
        return updated_content, uploaded_urls

    def fetch_block_registry(self) -> Tuple[bool, List[Dict] | str]:
        """
        Fetch all available Gutenberg block types from WordPress.

        Returns block definitions including:
        - name: Block identifier (e.g., 'core/paragraph', 'gp/tips')
        - title: Human-readable name
        - description: What the block does
        - attributes: Available attributes and their types
        - supports: Features the block supports

        Returns:
            Tuple of (success, list_of_blocks or error_message)
        """
        endpoint = "/wp-json/wp/v2/block-types"
        success, result = self._api_request(endpoint)

        if not success:
            return False, result

        # Simplify block data for storage
        blocks = []
        for block in result:
            blocks.append({
                'name': block.get('name', ''),
                'title': block.get('title', ''),
                'description': block.get('description', ''),
                'category': block.get('category', ''),
                'attributes': block.get('attributes', {}),
                'supports': block.get('supports', {}),
                'parent': block.get('parent'),
                'ancestor': block.get('ancestor'),
            })

        return True, blocks


def fetch_block_registry(output_path: Optional[str] = None) -> Tuple[bool, str]:
    """
    Fetch WordPress block registry and save to context/wordpress-blocks.json.

    Args:
        output_path: Optional path to save the registry. Defaults to context/wordpress-blocks.json

    Returns:
        Tuple of (success, file_path or error_message)
    """
    try:
        client = WordPressClient()
    except ValueError as e:
        return False, str(e)

    success, blocks = client.fetch_block_registry()
    if not success:
        return False, blocks

    # Default output path
    if not output_path:
        output_path = Path(__file__).parent.parent.parent / "context" / "wordpress-blocks.json"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save with metadata
    registry = {
        'fetched_at': datetime.now().isoformat(),
        'site_url': client.site_url,
        'block_count': len(blocks),
        'blocks': blocks
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    return True, str(output_path)


def regenerate_markdown(folder_path: str) -> Tuple[bool, str]:
    """
    Regenerate article.md from original.html.

    Use this after editing original.html to update the human-readable markdown.

    Args:
        folder_path: Path to article folder containing original.html

    Returns:
        Tuple of (success, message or error)
    """
    folder = Path(folder_path)

    if folder.is_file():
        folder = folder.parent

    original_path = folder / 'original.html'
    article_path = folder / 'article.md'
    metadata_path = folder / 'metadata.json'

    if not original_path.exists():
        return False, f"original.html not found in {folder_path}"

    # Read original HTML
    with open(original_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Get title from metadata
    title = 'Untitled'
    if metadata_path.exists():
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
            title = metadata.get('title', 'Untitled')

    # Convert to markdown
    try:
        client = WordPressClient()
    except ValueError:
        # Create a minimal instance just for conversion
        client = WordPressClient.__new__(WordPressClient)
        client.site_url = ''

    markdown_content = client.html_to_markdown(html_content)

    # Save article.md
    markdown_full = f"# {title}\n\n{markdown_content}"
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(markdown_full)

    return True, f"Regenerated {article_path}"


def import_from_wordpress(url: str, published_dir: Optional[str] = None) -> Tuple[bool, str]:
    """
    Import an article from WordPress to the published folder.

    Args:
        url: WordPress article URL
        published_dir: Optional directory to save to

    Returns:
        Tuple of (success, file_path or error_message)
    """
    try:
        client = WordPressClient()
    except ValueError as e:
        return False, str(e)

    success, post_data = client.fetch_post_by_url(url)
    if not success:
        return False, post_data

    return client.save_post_to_published(post_data, published_dir)


def export_to_wordpress(
    folder_path: str,
    use_edited: bool = False,
    post_id: Optional[int] = None,
    push: bool = False
) -> Tuple[bool, str]:
    """
    Export content from an article folder to WordPress as a draft.

    IMPORTANT: By default (push=False), this only shows what would be pushed.
    You must explicitly pass push=True to actually update WordPress.

    By default, uses original.html for perfect round-trip fidelity.
    Set use_edited=True to export the edited article.md instead.

    Args:
        folder_path: Path to article folder (containing metadata.json, original.html, article.md)
        use_edited: If True, convert article.md to HTML. If False (default), use original.html
        post_id: WordPress post ID (optional, reads from metadata.json if not provided)
        push: If True, actually push to WordPress. If False (default), only show preview.

    Returns:
        Tuple of (success, message describing what was/would be done)
    """
    try:
        client = WordPressClient()
    except ValueError as e:
        return False, str(e)

    folder = Path(folder_path)

    # Handle both folder path and file path for backwards compatibility
    if folder.is_file():
        folder = folder.parent

    if not folder.exists():
        return False, f"Folder not found: {folder_path}"

    metadata_path = folder / 'metadata.json'
    original_path = folder / 'original.html'
    article_path = folder / 'article.md'

    if not metadata_path.exists():
        return False, f"metadata.json not found in {folder_path}"

    # Load metadata
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    # Get post ID
    wp_post_id = post_id or metadata.get('wordpress_post_id')
    if not wp_post_id:
        return False, "No WordPress post ID found in metadata.json"

    wp_post_type = metadata.get('wordpress_post_type', 'posts')
    title = metadata.get('title')
    new_slug = metadata.get('new_slug')
    source_file = None
    html_content = None

    if use_edited:
        # Use edited markdown - convert to HTML
        if not article_path.exists():
            return False, f"article.md not found in {folder_path}"

        source_file = "article.md (converted to HTML)"

        if push:
            with open(article_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()

            # Extract title from markdown if present
            title_match = re.match(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
            if title_match:
                title = title_match.group(1)
                markdown_content = re.sub(r'^#\s+.+\n*', '', markdown_content, count=1)

            # Process images - upload local images to WordPress
            processed_content, uploaded_urls = client.process_content_images(markdown_content, folder)

            if uploaded_urls:
                print(f"Uploaded {len(uploaded_urls)} image(s) to WordPress")

            # Convert markdown to Gutenberg block HTML
            html_content = markdown_to_gutenberg(processed_content)
    else:
        # Use original HTML - perfect round-trip
        if not original_path.exists():
            return False, f"original.html not found in {folder_path}"

        source_file = "original.html (perfect round-trip)"

        if push:
            with open(original_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

    # Build preview URL for display
    if wp_post_type != 'posts':
        preview_url = f"{client.site_url}/?post_type={wp_post_type}&p={wp_post_id}&preview=true"
    else:
        preview_url = f"{client.site_url}/?p={wp_post_id}&preview=true"

    # If not pushing, just show what would happen
    if not push:
        slug_line = f"\nNew Slug: {new_slug} (redirect from old slug will be created)" if new_slug else ""
        summary = f"""
=== EXPORT PREVIEW (not pushed) ===
Folder: {folder}
Title: {title}
Post ID: {wp_post_id}
Post Type: {wp_post_type}
Source: {source_file}{slug_line}
Preview URL: {preview_url}

To actually push to WordPress, run with push=True:
  export_to_wordpress("{folder_path}", use_edited={use_edited}, push=True)
===================================
"""
        return True, summary.strip()

    # Actually push to WordPress
    print(f"Pushing to WordPress using {source_file}...")
    return client.update_post_to_draft(
        post_id=wp_post_id,
        content=html_content,
        title=title,
        meta_description=metadata.get('meta_description'),
        post_type=wp_post_type,
        new_slug=new_slug
    )


def markdown_to_html(markdown: str) -> str:
    """
    Convert markdown to HTML for WordPress.
    Basic conversion - WordPress will handle block formatting.

    Args:
        markdown: Markdown content

    Returns:
        HTML content
    """
    content = markdown

    # Headings
    for i in range(6, 0, -1):
        pattern = r'^' + '#' * i + r'\s+(.+)$'
        content = re.sub(pattern, rf'<h{i}>\1</h{i}>', content, flags=re.MULTILINE)

    # Bold
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)

    # Italic
    content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)

    # Inline code
    content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)

    # Links
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)

    # Images
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" />', content)

    # Code blocks
    content = re.sub(
        r'```(\w*)\n(.*?)\n```',
        r'<pre><code>\2</code></pre>',
        content,
        flags=re.DOTALL
    )

    # Unordered lists
    lines = content.split('\n')
    in_list = False
    result_lines = []
    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            item = line.strip()[2:]
            result_lines.append(f'<li>{item}</li>')
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)
    if in_list:
        result_lines.append('</ul>')
    content = '\n'.join(result_lines)

    # Ordered lists
    lines = content.split('\n')
    in_list = False
    result_lines = []
    for line in lines:
        if re.match(r'^\d+\.\s', line.strip()):
            if not in_list:
                result_lines.append('<ol>')
                in_list = True
            item = re.sub(r'^\d+\.\s', '', line.strip())
            result_lines.append(f'<li>{item}</li>')
        else:
            if in_list:
                result_lines.append('</ol>')
                in_list = False
            result_lines.append(line)
    if in_list:
        result_lines.append('</ol>')
    content = '\n'.join(result_lines)

    # Paragraphs - wrap text blocks in <p> tags
    paragraphs = content.split('\n\n')
    result = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        # Don't wrap if already has block-level tags
        if re.match(r'^<(h[1-6]|ul|ol|pre|blockquote|div)', para):
            result.append(para)
        else:
            result.append(f'<p>{para}</p>')

    return '\n\n'.join(result)


def markdown_to_gutenberg(markdown: str) -> str:
    """
    Convert markdown to Gutenberg-formatted HTML with block comments.

    Produces WordPress-ready HTML where each element is wrapped in
    <!-- wp:block-type --> comments, matching the format WordPress uses
    when fetching content with context=edit.

    Args:
        markdown: Markdown content

    Returns:
        Gutenberg block HTML ready for WordPress
    """
    if not markdown or not markdown.strip():
        return ''

    lines = markdown.split('\n')
    blocks = []
    i = 0

    def convert_inline(text: str) -> str:
        """Convert inline markdown (bold, italic, code, links, images) to HTML."""
        # Inline code (before bold/italic to avoid conflicts)
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        # Images inline (rare but possible)
        text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1"/>', text)
        # Links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        # Bold (must come before italic)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        return text

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            i += 1
            continue

        # Headings
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if heading_match:
            level = len(heading_match.group(1))
            text = convert_inline(heading_match.group(2).strip())
            if level == 2:
                blocks.append(
                    f'<!-- wp:heading -->\n'
                    f'<h2 class="wp-block-heading">{text}</h2>\n'
                    f'<!-- /wp:heading -->'
                )
            else:
                blocks.append(
                    f'<!-- wp:heading {{"level":{level}}} -->\n'
                    f'<h{level} class="wp-block-heading">{text}</h{level}>\n'
                    f'<!-- /wp:heading -->'
                )
            i += 1
            continue

        # Horizontal rules / separators
        if re.match(r'^(-{3,}|\*{3,}|_{3,})$', stripped):
            blocks.append(
                '<!-- wp:separator -->\n'
                '<hr class="wp-block-separator has-alpha-channel-opacity"/>\n'
                '<!-- /wp:separator -->'
            )
            i += 1
            continue

        # Tables (lines starting with |)
        if stripped.startswith('|') and '|' in stripped[1:]:
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            if len(table_lines) >= 2:
                # Parse header row
                header_cells = [convert_inline(c.strip()) for c in table_lines[0].strip('|').split('|')]
                # Skip separator row (the |---|---| line), find body rows
                body_start = 1
                if len(table_lines) > 1 and re.match(r'^[\s|:-]+$', table_lines[1]):
                    body_start = 2
                body_rows = []
                for row_line in table_lines[body_start:]:
                    cells = [convert_inline(c.strip()) for c in row_line.strip('|').split('|')]
                    body_rows.append(cells)
                # Build HTML
                thead = '<thead><tr>' + ''.join(f'<th>{c}</th>' for c in header_cells) + '</tr></thead>'
                tbody_rows = ''.join(
                    '<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>'
                    for row in body_rows
                )
                tbody = f'<tbody>{tbody_rows}</tbody>' if body_rows else ''
                blocks.append(
                    '<!-- wp:table -->\n'
                    f'<figure class="wp-block-table"><table class="has-fixed-layout">{thead}{tbody}</table></figure>\n'
                    '<!-- /wp:table -->'
                )
            continue

        # Images (standalone line)
        image_match = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', stripped)
        if image_match:
            alt = image_match.group(1)
            src = image_match.group(2)
            blocks.append(
                f'<!-- wp:image -->\n'
                f'<figure class="wp-block-image"><img src="{src}" alt="{alt}"/></figure>\n'
                f'<!-- /wp:image -->'
            )
            i += 1
            continue

        # Code blocks
        if stripped.startswith('```'):
            lang = stripped[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            code_content = '\n'.join(code_lines)
            # Escape HTML in code
            code_content = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            blocks.append(
                f'<!-- wp:code -->\n'
                f'<pre class="wp-block-code"><code>{code_content}</code></pre>\n'
                f'<!-- /wp:code -->'
            )
            continue

        # Blockquotes
        if stripped.startswith('> '):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            quote_text = convert_inline(' '.join(quote_lines))
            blocks.append(
                f'<!-- wp:quote -->\n'
                f'<blockquote class="wp-block-quote"><p>{quote_text}</p></blockquote>\n'
                f'<!-- /wp:quote -->'
            )
            continue

        # Unordered lists
        if re.match(r'^[-*]\s', stripped):
            items = []
            while i < len(lines) and re.match(r'^\s*[-*]\s', lines[i]):
                item_text = re.sub(r'^\s*[-*]\s+', '', lines[i])
                items.append(convert_inline(item_text.strip()))
                i += 1
            list_items = ''.join(
                f'<!-- wp:list-item -->\n<li>{item}</li>\n<!-- /wp:list-item -->\n'
                for item in items
            )
            blocks.append(
                f'<!-- wp:list -->\n'
                f'<ul class="wp-block-list">{list_items}</ul>\n'
                f'<!-- /wp:list -->'
            )
            continue

        # Ordered lists
        if re.match(r'^\d+\.\s', stripped):
            items = []
            while i < len(lines) and re.match(r'^\s*\d+\.\s', lines[i]):
                item_text = re.sub(r'^\s*\d+\.\s+', '', lines[i])
                items.append(convert_inline(item_text.strip()))
                i += 1
            list_items = ''.join(
                f'<!-- wp:list-item -->\n<li>{item}</li>\n<!-- /wp:list-item -->\n'
                for item in items
            )
            blocks.append(
                f'<!-- wp:list {{"ordered":true}} -->\n'
                f'<ol>{list_items}</ol>\n'
                f'<!-- /wp:list -->'
            )
            continue

        # Paragraphs (default: collect consecutive non-empty, non-special lines)
        para_lines = []
        while i < len(lines):
            l = lines[i].strip()
            if not l:
                i += 1
                break
            if re.match(r'^#{1,6}\s', l):
                break
            if re.match(r'^!\[', l):
                break
            if l.startswith('```'):
                break
            if l.startswith('> '):
                break
            if re.match(r'^[-*]\s', l):
                break
            if re.match(r'^\d+\.\s', l):
                break
            if re.match(r'^(-{3,}|\*{3,}|_{3,})$', l):
                break
            if l.startswith('|') and '|' in l[1:]:
                break
            para_lines.append(lines[i])
            i += 1
        if para_lines:
            text = convert_inline(' '.join(line.strip() for line in para_lines))
            blocks.append(
                f'<!-- wp:paragraph -->\n'
                f'<p>{text}</p>\n'
                f'<!-- /wp:paragraph -->'
            )
        continue

    return '\n\n'.join(blocks)


def publish_markdown(
    file_path: str,
    post_type: str = 'article',
    title: Optional[str] = None,
    meta_description: Optional[str] = None,
    slug: Optional[str] = None,
    categories: Optional[list] = None,
    author: Optional[int] = None,
    featured_image: Optional[str] = None,
    push: bool = False,
) -> Tuple[bool, str]:
    """
    Convert a markdown file to Gutenberg blocks and create a new WordPress draft.

    Args:
        file_path: Path to the markdown file
        post_type: WordPress post type ('article' for learn, 'posts' for blog)
        title: Post title (extracted from H1 if not provided)
        meta_description: SEO description (included in success message for manual paste)
        slug: URL slug (auto-generated if not provided)
        categories: List of category IDs to assign
        author: WordPress user ID. Defaults to WORDPRESS_DEFAULT_AUTHOR_ID env var (1) for articles.
        featured_image: Local path to featured image (blog posts only). Uploaded to WordPress media library.
        push: If True, actually create on WordPress. If False, show preview.

    Returns:
        Tuple of (success, message)
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return False, f"File not found: {file_path}"

    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    if not markdown_content.strip():
        return False, "File is empty"

    # Strip frontmatter first (before title extraction, since H1 comes after frontmatter)
    content_body = markdown_content
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content_body, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        content_body = content_body[frontmatter_match.end():]

        if not meta_description:
            md = re.search(r'Meta Description:\s*(.+)', frontmatter)
            if md:
                meta_description = md.group(1).strip()
        if not slug:
            s = re.search(r'URL Slug:\s*/?\w+/(.+)', frontmatter)
            if s:
                slug = s.group(1).strip().strip('/')

    # Extract title from H1 if not provided
    if not title:
        title_match = re.search(r'^#\s+(.+)$', content_body, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title = file_path.stem.replace('-', ' ').title()

    # Remove H1 from content (title is set separately in WordPress)
    content_without_h1 = re.sub(r'^#\s+.+\n*', '', content_body, count=1, flags=re.MULTILINE)

    # Convert to Gutenberg blocks
    gutenberg_html = markdown_to_gutenberg(content_without_h1)

    # Default author for articles, caller-specified for blog posts
    if not author and post_type == 'article':
        author = int(os.getenv('WORDPRESS_DEFAULT_AUTHOR_ID', '1'))

    if not push:
        # Preview mode
        block_count = len(re.findall(r'<!-- wp:([a-z])', gutenberg_html))
        summary = (
            f"=== PUBLISH PREVIEW (not pushed) ===\n"
            f"File: {file_path}\n"
            f"Title: {title}\n"
            f"Post Type: {post_type}\n"
            f"Meta Description: {meta_description or '(none)'}\n"
            f"Slug: {slug or '(auto-generated)'}\n"
            f"Author ID: {author or '(WordPress default)'}\n"
            f"Featured Image: {featured_image or '(none)'}\n"
            f"Gutenberg Blocks: {block_count}\n"
            f"\nTo actually create on WordPress, run with push=True\n"
            f"==================================="
        )
        return True, summary

    # Actually create on WordPress
    try:
        client = WordPressClient()
    except ValueError as e:
        return False, str(e)

    # Upload any local images
    processed_content, uploaded_urls = client.process_content_images(
        gutenberg_html, str(file_path.parent)
    )
    if uploaded_urls:
        print(f"Uploaded {len(uploaded_urls)} image(s) to WordPress")

    # Upload featured image if provided
    featured_media_id = None
    if featured_image:
        fi_path = Path(featured_image)
        if not fi_path.exists():
            return False, f"Featured image not found: {featured_image}"
        print(f"Uploading featured image: {fi_path.name}")
        fi_success, fi_result = client.upload_media(str(fi_path), alt_text=title or '')
        if not fi_success:
            return False, f"Failed to upload featured image: {fi_result}"
        featured_media_id = fi_result['id']
        print(f"Featured image uploaded (media ID: {featured_media_id})")

    success, result = client.create_draft(
        title=title,
        content=processed_content,
        post_type=post_type,
        meta_description=meta_description,
        slug=slug,
        categories=categories,
        author=author,
        featured_media=featured_media_id,
    )

    if not success:
        return False, f"Failed to create draft: {result}"

    msg = (
        f"Created new draft on WordPress!\n"
        f"  Post ID: {result['id']}\n"
        f"  Slug: {result['slug']}\n"
        f"  Post Type: {result['post_type']}\n"
        f"  Preview: {result['preview_url']}"
    )
    if meta_description:
        msg += f"\n\n  Meta description (paste into Yoast):\n  {meta_description}"

    return True, msg


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Import: python wordpress_client.py import <url>")
        print("  Export: python wordpress_client.py export <folder_path> [--edited] [--push]")
        print("")
        print("Import creates a folder with:")
        print("  - article.md     (markdown for editing)")
        print("  - original.html  (raw WordPress HTML)")
        print("  - metadata.json  (post metadata)")
        print("")
        print("Export options:")
        print("  --edited    Use article.md instead of original.html")
        print("  --push      Actually push to WordPress (without this, only shows preview)")
        print("")
        print("Requires environment variables:")
        print("  WORDPRESS_SITE_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'import' and len(sys.argv) >= 3:
        url = sys.argv[2]
        print(f"Importing from: {url}")
        success, result = import_from_wordpress(url)
        if success:
            print(f"Success! Saved to: {result}")
        else:
            print(f"Failed: {result}")

    elif command == 'export' and len(sys.argv) >= 3:
        folder_path = sys.argv[2]
        use_edited = '--edited' in sys.argv
        push = '--push' in sys.argv
        print(f"Exporting: {folder_path}")
        success, result = export_to_wordpress(folder_path, use_edited=use_edited, push=push)
        if success:
            print(result)
        else:
            print(f"Failed: {result}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
