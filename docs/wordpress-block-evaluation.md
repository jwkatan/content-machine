# WordPress Gutenberg Block System — Evaluation

## Three Content Flows

### Flow 1: Edit Existing Article

```
checkout(slug) → edit workbench/{slug}/original.html → checkin(slug, push=True)
```

`original.html` contains raw Gutenberg block comments. Edits preserve them verbatim. The push sends the same HTML back. **Perfect round-trip fidelity.**

Safety nets: `push=False` previews without pushing. `push=True` always creates a **draft**, never publishes.

### Flow 2: New Markdown → WordPress

Use the `/wordpress-edit` command with the push subcommand:

```
/wordpress-edit push drafts/26Q1-topic/topic.md article   # learn article (default)
/wordpress-edit push drafts/26Q1-topic/topic.md posts      # blog post
```

Converts markdown to Gutenberg block HTML via `markdown_to_gutenberg()`, then creates a new WordPress draft via the REST API. Extracts title from H1, meta from frontmatter. Always creates a **draft**, never publishes directly.

## What the Converter Handles

| Markdown | Gutenberg Block | Status |
|----------|----------------|--------|
| Paragraphs | `<!-- wp:paragraph -->` | Supported |
| `## H2`, `### H3` | `<!-- wp:heading -->` with level | Supported |
| `- item` lists | `<!-- wp:list -->` + `<!-- wp:list-item -->` | Supported |
| `1. item` lists | `<!-- wp:list {"ordered":true} -->` | Supported |
| `![alt](src)` | `<!-- wp:image -->` with `<figure>` | Supported |
| `` ```code``` `` | `<!-- wp:code -->` | Supported |
| `> quote` | `<!-- wp:quote -->` | Supported |
| Bold, italic, links | Inline `<strong>`, `<em>`, `<a>` inside blocks | Supported |
| Tables | Not yet — would need `<!-- wp:table -->` | Future |
| `gp/*` custom blocks | Cannot generate from markdown | Use WP editor |

## Blog-Relevant Blocks

**Tier 1 — In every article:**
`core/paragraph`, `core/heading`, `core/list` + `core/list-item`, `core/image`

**Tier 2 — In some articles:**
`core/table`, `core/quote`, `core/code`, `core/separator`, `core/buttons` + `core/button`, `core/embed`

**Custom blocks (gp/\*):** Server-side rendered. Content stored as JSON in self-closing comments: `<!-- wp:gp/tips {"data":{...}} /-->`. Can edit existing JSON values, but cannot generate from markdown. Add/remove in WordPress block editor.

## Two Article Formats

Some articles have full Gutenberg block comments. Others — especially older ones — have plain HTML with `wp-block-*` CSS classes but no block comments. The pre-flight check in `/wordpress-edit` detects which format an article uses.

## Test Suite

71 tests in `tests/test_gutenberg_conversion.py`:
- 23 unit tests (one per block type and inline format)
- 5 edge case tests
- 32 integration tests (4 real articles x 8 checks each)
- 4 round-trip tests (html→markdown→gutenberg→verify structure)
- 7 publish_markdown preview tests

Run: `.venv/bin/python -m pytest tests/test_gutenberg_conversion.py -v`

## Known Limitations

1. **Image metadata lost:** Markdown images don't carry WordPress IDs, size slugs, or dimensions. Generated image blocks work but lack `{"id":123,"sizeSlug":"large"}` attributes.
2. **Table conversion:** `markdown_to_gutenberg()` does not yet handle markdown tables. Tables should be added as raw block HTML.
3. **Custom gp/\* blocks:** Cannot be generated from markdown. The block registry lists 91 custom blocks but their `data` attribute schemas are undocumented.
4. **List splitting:** Markdown with blank lines between list items creates separate list blocks. Structurally valid but may differ from the original.
