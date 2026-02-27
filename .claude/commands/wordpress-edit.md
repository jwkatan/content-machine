# WordPress Block Editor

Edit existing WordPress content or push new markdown files to WordPress.

## Two Workflows

**Determine which workflow to use based on the user's request:**

1. **Push new article** — User provides a markdown file path and wants it uploaded to WordPress → Go to [Push New Article](#push-new-article)
2. **Edit existing article** — User provides a slug and wants to edit content already on WordPress → Go to [Edit Existing Article](#edit-existing-article)

---

## Push New Article

Upload a markdown file to WordPress as a new draft with correct Gutenberg blocks.

**Usage:** `/wordpress-edit push path/to/file.md [type]`

- `type` is optional: `article` (learn article, default) or `posts` (blog post)

### Step 1: Preview

```python
from data_sources.modules.wordpress_client import publish_markdown

# Preview — no API call, just shows what would be created
publish_markdown('{path}')
```

Show the preview output to the user.

### Step 2: Ask for Category and Author

Categories and authors are cached locally in `data_sources/config/wp_cache.json`. No API call needed unless the user asks to refresh.

**Categories** — always ask the user which category:

```python
from data_sources.modules.wordpress_client import WordPressClient
client = WordPressClient()
success, categories = client.get_categories(post_type='{type}')
if success:
    for c in categories:
        print(f"  {c['id']}: {c['name']} ({c['count']} posts)")
```

Ask the user to pick a category. If no categories exist for the post type, skip this step.

**Author:**
- **Learn articles (`article`)**: Defaults to [Company] Team (author ID 1). No need to ask.
- **Blog posts (`posts`)**: Always ask the user who the author should be:

```python
success, authors = client.get_authors()
if success:
    for a in authors:
        print(f"  {a['id']}: {a['name']}")
```

**Refresh cache** — if the user says "refresh" or lists seem stale:

```python
print(client.refresh_cache())
```

**Featured Image (blog posts only):**

Blog posts require a featured image. Ask the user:
1. **"I have one locally"** — ask for the file path
2. **"I'll upload it later"** — skip, no featured image set

Learn articles (`article`) do NOT have featured images — skip this step for articles.

### Step 3: Push to WordPress

```python
# Create as learn article (author defaults to [Company] Team, no featured image)
publish_markdown('{path}', post_type='article', categories=[{category_id}], push=True)

# Create as blog post (specify author and featured image)
publish_markdown('{path}', post_type='posts', categories=[{category_id}], author={author_id}, featured_image='{image_path}', push=True)

# Create as blog post (no featured image — user will upload later)
publish_markdown('{path}', post_type='posts', categories=[{category_id}], author={author_id}, push=True)
```

Returns the draft URL. The post is always created as a **draft** — never published directly.

### What publish_markdown Does

1. Reads the markdown file
2. Extracts H1 as title, frontmatter as meta (if present)
3. Converts markdown → Gutenberg block HTML via `markdown_to_gutenberg()`
4. Creates a new WordPress draft via the REST API

### Supported Conversions

| Markdown | Gutenberg Block |
|----------|----------------|
| Paragraphs | `<!-- wp:paragraph -->` |
| `## H2`, `### H3` | `<!-- wp:heading -->` with level |
| `- item` lists | `<!-- wp:list -->` + `<!-- wp:list-item -->` |
| `1. item` lists | `<!-- wp:list {"ordered":true} -->` |
| `![alt](src)` | `<!-- wp:image -->` |
| `` ```code``` `` | `<!-- wp:code -->` |
| `> quote` | `<!-- wp:quote -->` |
| Bold, italic, links | Inline HTML inside blocks |

**Not supported from markdown:** Tables (use raw block HTML), `gp/*` custom blocks (add in WordPress editor).

---

## Edit Existing Article

### Pre-Flight Check

Before editing, determine the article's format:

1. Check out the article and look at `original.html`
2. Search for `<!-- wp:` in the file
   - **Found:** Article uses Gutenberg blocks. Follow the block editing rules below.
   - **Not found:** Article uses classic HTML (no block comments). Edit the HTML directly — do not add block comments to a classic article.

### Setup

```python
# Check out article to workbench (syncs fresh from WordPress)
from data_sources.modules.content_library import checkout
success, path = checkout('{slug}')

# Read the article to edit
folder = 'content/workbench/{slug}/'
with open(folder + 'original.html') as f:
    content = f.read()
with open(folder + 'metadata.json') as f:
    metadata = json.load(f)
```

## Understanding Gutenberg Blocks

Blocks are HTML wrapped in special comments:

```html
<!-- wp:block-type {"attribute": "value"} -->
<html-content>
<!-- /wp:block-type -->
```

### Common Block Types

| Block | Purpose | HTML Element |
|-------|---------|--------------|
| `core/paragraph` | Regular text | `<p>` |
| `core/heading` | Sections (use level attr) | `<h2>`, `<h3>`, etc. |
| `core/list` | Bullet/numbered lists | `<ul>` or `<ol>` |
| `core/list-item` | List items (nested in list) | `<li>` |
| `core/image` | Images | `<figure><img></figure>` |
| `core/quote` | Blockquotes | `<blockquote>` |
| `core/code` | Code blocks | `<pre><code>` |
| `core/table` | Tables | `<figure><table></figure>` |
| `core/separator` | Horizontal rule | `<hr>` |
| `core/buttons` + `core/button` | CTA buttons | `<div><a>` |

### Site-Specific Blocks

| Block | Purpose | Notes |
|-------|---------|-------|
| `gp/tips` | Expert tips section | Server-rendered — data stored as JSON in comment, not editable as HTML. Edit in WordPress block editor. |
| `gp/accordion` | Accordion sections | Server-rendered |
| `gp/article-posts` | Related articles | Server-rendered |

**Note:** All `gp/*` blocks are server-rendered. Their content is stored as JSON in a self-closing comment like `<!-- wp:gp/tips {"data":{...}} /-->`. You can edit the JSON values, but adding new `gp/*` blocks should be done in the WordPress block editor.

## Editing Rules

### 1. Preserve Block Comments
ALWAYS keep the opening and closing comments:
```html
<!-- wp:paragraph -->  ← KEEP
<p>Your edited text here</p>
<!-- /wp:paragraph --> ← KEEP
```

### 2. Preserve Attributes
Keep attributes in the opening comment:
```html
<!-- wp:heading {"level":2} -->  ← Keep {"level":2}
<h2 class="wp-block-heading">Updated Title</h2>
<!-- /wp:heading -->
```

### 3. Preserve Class Names
WordPress adds class names to elements — keep them:
```html
<p class="has-large-font-size">Text</p>  ← Keep class
<ul class="wp-block-list">Items</ul>     ← Keep class
```

### 4. Handle Nested Blocks
Lists have nested list-item blocks:
```html
<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item -->
<li>Item one</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li>Item two</li>
<!-- /wp:list-item -->
</ul>
<!-- /wp:list -->
```

## Adding New Blocks

### New Paragraph
```html
<!-- wp:paragraph -->
<p>Your new paragraph text here.</p>
<!-- /wp:paragraph -->
```

### New Heading
```html
<!-- wp:heading {"level":2} -->
<h2 class="wp-block-heading">New Section Title</h2>
<!-- /wp:heading -->
```

### New Heading (H3)
```html
<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">Subsection Title</h3>
<!-- /wp:heading -->
```

### New List
```html
<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item -->
<li>First item</li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li>Second item</li>
<!-- /wp:list-item -->
</ul>
<!-- /wp:list -->
```

### New Image
```html
<!-- wp:image {"sizeSlug":"large"} -->
<figure class="wp-block-image size-large">
<img src="https://example.com/image.jpg" alt="Description"/>
</figure>
<!-- /wp:image -->
```

### New Table
```html
<!-- wp:table -->
<figure class="wp-block-table"><table class="has-fixed-layout"><thead><tr><th>Header 1</th><th>Header 2</th></tr></thead><tbody><tr><td>Cell 1</td><td>Cell 2</td></tr></tbody></table></figure>
<!-- /wp:table -->
```

### New Separator
```html
<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->
```

### New Button
```html
<!-- wp:buttons -->
<div class="wp-block-buttons">
<!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="https://example.com">Button Text</a></div>
<!-- /wp:button -->
</div>
<!-- /wp:buttons -->
```

## Deleting Blocks

Remove the ENTIRE block including:
- Opening comment: `<!-- wp:type -->`
- HTML content
- Closing comment: `<!-- /wp:type -->`

Do NOT leave orphaned tags or comments.

## After Editing

After making changes to `original.html`, regenerate the markdown:

```python
from data_sources.modules.wordpress_client import regenerate_markdown

success, message = regenerate_markdown('content/workbench/{slug}/')
print(message)
```

This updates `article.md` for human readability.

## Check In and Push to WordPress

When ready to push changes, use checkin which updates the database and pushes to WordPress:

```python
from data_sources.modules.content_library import checkin

# Preview what will be pushed (check in to database only, no WordPress push)
success, result = checkin('{slug}')
print(result)

# Actually push to WordPress and clean up workbench
success, result = checkin('{slug}', push=True)
print(result)
```

## Validation Checklist

Before exporting, verify:
- [ ] All blocks have matching open/close comments
- [ ] Attributes in comments match HTML elements (e.g., level matches heading tag)
- [ ] No orphaned HTML tags outside blocks
- [ ] Nested blocks are properly contained (list-items inside lists)
- [ ] Class names are preserved

## Fixing Slug Redirects

When a post's slug is changed in WordPress (e.g., fixing a typo), the old URL may still redirect via WordPress's built-in `_wp_old_slug` mechanism. To create a reliable 301 redirect, add it to the **Redirection plugin** via the API and update the content library.

### Step 1: Find the Post

```python
from data_sources.modules.wordpress_client import WordPressClient
wp = WordPressClient()

# Confirm the post exists at the new slug
for ptype in ['posts', 'article']:
    ok, data = wp._api_request(f'/wp-json/wp/v2/{ptype}?slug={new_slug}')
    if ok and data:
        print(f'Found: id={data[0]["id"]}, slug={data[0]["slug"]}, link={data[0]["link"]}')
```

### Step 2: Create the Redirect

```python
ok, data = wp._api_request(
    '/wp-json/redirection/v1/redirect',
    method='POST',
    data={
        'url': '/{path_prefix}/{old_slug}',
        'action_data': {'url': 'https://[your-domain.com]/{path_prefix}/{new_slug}'},
        'action_type': 'url',
        'action_code': 301,
        'match_type': 'url',
        'group_id': 1
    }
)
```

- `path_prefix` is `blog` for blog posts, `learn/{category}` for learn articles
- Always use 301 (permanent redirect) for slug fixes

### Step 3: Verify

```python
ok, data = wp._api_request('/wp-json/redirection/v1/redirect?search={old_slug}')
if ok:
    for item in data.get('items', []):
        print(f'id={item["id"]}, from={item["url"]} -> to={item.get("action_data", {}).get("url", "")}')
```

### Step 4: Fix the Content Library

If the article was synced under the old slug, delete the old entry and re-sync:

```python
import sqlite3
conn = sqlite3.connect('data_sources/db/content.db')
conn.execute("DELETE FROM articles WHERE slug = '{old_slug}'")
conn.commit()
conn.close()

from data_sources.modules.content_library import init_db, sync_article
init_db()
sync_article('{new_slug}')
```

## Reference

- Block registry: `context/wordpress-blocks.json`
- Article files: `content/workbench/{slug}/original.html`, `article.md`, `metadata.json`
- WordPress client: `data_sources/modules/wordpress_client.py`
- Redirection plugin API: `/wp-json/redirection/v1/redirect`
