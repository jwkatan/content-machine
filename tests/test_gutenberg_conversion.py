"""
Tests for markdown_to_gutenberg() conversion.

Uses workbench articles as ground truth — each has article.md (markdown)
and original.html (known-good Gutenberg block HTML from WordPress).
"""

import os
import re
import sys
import pytest

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from data_sources.modules.wordpress_client import markdown_to_gutenberg, publish_markdown, WordPressClient

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_block_types(html: str) -> list:
    """Extract ordered list of block type names from Gutenberg HTML (opening comments only)."""
    return re.findall(r'<!-- wp:([a-z][a-z0-9/-]*)', html)


def extract_opening_blocks(html: str) -> list:
    """Extract ordered list of opening block comments (excluding list-item for cleaner comparison)."""
    blocks = re.findall(r'<!-- wp:([a-z][a-z0-9/-]*)', html)
    return [b for b in blocks if b != 'list-item']


def count_blocks(html: str, block_type: str) -> int:
    """Count occurrences of a specific opening block type."""
    return len(re.findall(rf'<!-- wp:{re.escape(block_type)}[\s{{>]', html))


# ---------------------------------------------------------------------------
# Test data paths
# ---------------------------------------------------------------------------

WORKBENCH = os.path.join(PROJECT_ROOT, 'workbench')

ARTICLES = [
    'best-cobol-tools-top-12-tools-to-know-in-2025',
    '10-mainframe-modernization-tools-to-know-in-2025',
    'mainframes-with-ai-3-use-cases-and-5-tools-to-know-in-2025',
    'best-mainframe-modernization-companies-top-8-players-in-2026',
]


def load_article(slug):
    """Load markdown and original HTML for a workbench article."""
    folder = os.path.join(WORKBENCH, slug)
    md_path = os.path.join(folder, 'article.md')
    html_path = os.path.join(folder, 'original.html')
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    return md, html


# ===========================================================================
# Unit Tests — Per Block Type
# ===========================================================================

class TestParagraphBlock:
    def test_simple_paragraph(self):
        result = markdown_to_gutenberg("Hello world.")
        assert '<!-- wp:paragraph -->' in result
        assert '<p>Hello world.</p>' in result
        assert '<!-- /wp:paragraph -->' in result

    def test_paragraph_with_link(self):
        result = markdown_to_gutenberg("Check out [Swimm](https://swimm.io) for more.")
        assert '<!-- wp:paragraph -->' in result
        assert '<a href="https://swimm.io">Swimm</a>' in result

    def test_paragraph_with_bold(self):
        result = markdown_to_gutenberg("This is **important** text.")
        assert '<strong>important</strong>' in result
        assert '<!-- wp:paragraph -->' in result

    def test_paragraph_with_italic(self):
        result = markdown_to_gutenberg("This is *emphasized* text.")
        assert '<em>emphasized</em>' in result

    def test_paragraph_with_inline_code(self):
        result = markdown_to_gutenberg("Use the `print()` function.")
        assert '<code>print()</code>' in result


class TestHeadingBlock:
    def test_h2_default(self):
        result = markdown_to_gutenberg("## My Section")
        assert '<!-- wp:heading -->' in result
        assert '<h2 class="wp-block-heading">My Section</h2>' in result
        assert '<!-- /wp:heading -->' in result
        # H2 should NOT have level attribute (it's the default)
        assert '"level"' not in result

    def test_h3_with_level(self):
        result = markdown_to_gutenberg("### Subsection")
        assert '<!-- wp:heading {"level":3} -->' in result
        assert '<h3 class="wp-block-heading">Subsection</h3>' in result

    def test_h4_with_level(self):
        result = markdown_to_gutenberg("#### Deep Section")
        assert '<!-- wp:heading {"level":4} -->' in result
        assert '<h4 class="wp-block-heading">Deep Section</h4>' in result

    def test_h1_with_level(self):
        result = markdown_to_gutenberg("# Title")
        assert '<!-- wp:heading {"level":1} -->' in result
        assert '<h1 class="wp-block-heading">Title</h1>' in result

    def test_heading_with_bold(self):
        result = markdown_to_gutenberg("## **Bold** Heading")
        assert '<strong>Bold</strong>' in result
        assert 'wp-block-heading' in result


class TestListBlock:
    def test_unordered_list(self):
        md = "- First item\n- Second item\n- Third item"
        result = markdown_to_gutenberg(md)
        assert '<!-- wp:list -->' in result
        assert '<ul class="wp-block-list">' in result
        assert result.count('<!-- wp:list-item -->') == 3
        assert result.count('<!-- /wp:list-item -->') == 3
        assert '<li>First item</li>' in result
        assert '<!-- /wp:list -->' in result

    def test_ordered_list(self):
        md = "1. First\n2. Second\n3. Third"
        result = markdown_to_gutenberg(md)
        assert '<!-- wp:list {"ordered":true} -->' in result
        assert '<ol>' in result
        assert result.count('<!-- wp:list-item -->') == 3

    def test_list_with_bold_items(self):
        md = "- **Feature one**: Description here\n- **Feature two**: Another description"
        result = markdown_to_gutenberg(md)
        assert '<li><strong>Feature one</strong>: Description here</li>' in result
        assert '<li><strong>Feature two</strong>: Another description</li>' in result

    def test_list_with_links(self):
        md = "- [Swimm](https://swimm.io) for docs\n- [GitHub](https://github.com) for code"
        result = markdown_to_gutenberg(md)
        assert '<a href="https://swimm.io">Swimm</a>' in result
        assert '<a href="https://github.com">GitHub</a>' in result

    def test_asterisk_list(self):
        md = "* Item one\n* Item two"
        result = markdown_to_gutenberg(md)
        assert '<!-- wp:list -->' in result
        assert '<li>Item one</li>' in result


class TestImageBlock:
    def test_simple_image(self):
        result = markdown_to_gutenberg("![Alt text](https://example.com/img.png)")
        assert '<!-- wp:image -->' in result
        assert '<figure class="wp-block-image">' in result
        assert '<img src="https://example.com/img.png" alt="Alt text"/>' in result
        assert '<!-- /wp:image -->' in result

    def test_image_empty_alt(self):
        result = markdown_to_gutenberg("![](https://example.com/img.png)")
        assert 'alt=""' in result

    def test_image_between_paragraphs(self):
        md = "Some text.\n\n![Logo](https://example.com/logo.png)\n\nMore text."
        result = markdown_to_gutenberg(md)
        blocks = re.findall(r'<!-- wp:(\w+)', result)
        assert blocks == ['paragraph', 'image', 'paragraph']


class TestCodeBlock:
    def test_code_block(self):
        md = "```python\nprint('hello')\n```"
        result = markdown_to_gutenberg(md)
        assert '<!-- wp:code -->' in result
        assert '<pre class="wp-block-code"><code>' in result
        assert "print(&#x27;hello&#x27;)" in result or "print('hello')" in result
        assert '<!-- /wp:code -->' in result

    def test_code_block_html_escaping(self):
        md = "```\n<div>test</div>\n```"
        result = markdown_to_gutenberg(md)
        assert '&lt;div&gt;' in result
        assert '&lt;/div&gt;' in result

    def test_code_block_no_language(self):
        md = "```\nsome code\n```"
        result = markdown_to_gutenberg(md)
        assert '<!-- wp:code -->' in result
        assert 'some code' in result


class TestBlockquoteBlock:
    def test_simple_blockquote(self):
        result = markdown_to_gutenberg("> This is a quote.")
        assert '<!-- wp:quote -->' in result
        assert '<blockquote class="wp-block-quote">' in result
        assert '<p>This is a quote.</p>' in result
        assert '<!-- /wp:quote -->' in result

    def test_multiline_blockquote(self):
        md = "> Line one\n> Line two"
        result = markdown_to_gutenberg(md)
        assert '<!-- wp:quote -->' in result
        assert 'Line one' in result
        assert 'Line two' in result


class TestSeparatorBlock:
    def test_triple_dash(self):
        result = markdown_to_gutenberg("---")
        assert '<!-- wp:separator -->' in result
        assert '<hr class="wp-block-separator has-alpha-channel-opacity"/>' in result
        assert '<!-- /wp:separator -->' in result

    def test_triple_asterisk(self):
        result = markdown_to_gutenberg("***")
        assert '<!-- wp:separator -->' in result

    def test_triple_underscore(self):
        result = markdown_to_gutenberg("___")
        assert '<!-- wp:separator -->' in result

    def test_separator_not_in_paragraph(self):
        """--- should NOT end up as literal text in a paragraph block."""
        result = markdown_to_gutenberg("Some text.\n\n---\n\nMore text.")
        # Should have separator block, not a paragraph containing "---"
        assert '<!-- wp:separator -->' in result
        assert '<p>---</p>' not in result

    def test_separator_between_sections(self):
        md = "## Section 1\n\nContent.\n\n---\n\n## Section 2\n\nMore content."
        result = markdown_to_gutenberg(md)
        blocks = extract_opening_blocks(result)
        assert 'separator' in blocks


class TestTableBlock:
    def test_basic_table(self):
        md = "| Name | Role |\n|---|---|\n| Alice | Engineer |\n| Bob | Designer |"
        result = markdown_to_gutenberg(md)
        assert '<!-- wp:table -->' in result
        assert '<thead>' in result
        assert '<th>Name</th>' in result
        assert '<th>Role</th>' in result
        assert '<tbody>' in result
        assert '<td>Alice</td>' in result
        assert '<td>Designer</td>' in result
        assert '<!-- /wp:table -->' in result

    def test_table_not_in_paragraph(self):
        """Table rows should NOT end up as raw pipe text in a paragraph."""
        md = "| A | B |\n|---|---|\n| 1 | 2 |"
        result = markdown_to_gutenberg(md)
        assert '<!-- wp:table -->' in result
        assert '<p>|' not in result

    def test_table_with_inline_formatting(self):
        md = "| Tool | Description |\n|---|---|\n| **Swimm** | [Application understanding](https://swimm.io) |"
        result = markdown_to_gutenberg(md)
        assert '<strong>Swimm</strong>' in result
        assert '<a href="https://swimm.io">Application understanding</a>' in result

    def test_table_between_content(self):
        md = "Intro paragraph.\n\n| H1 | H2 |\n|---|---|\n| A | B |\n\nClosing paragraph."
        result = markdown_to_gutenberg(md)
        blocks = extract_opening_blocks(result)
        assert blocks == ['paragraph', 'table', 'paragraph']

    def test_five_column_table(self):
        """Regression: the comparison table from listicle articles has 5 columns."""
        md = (
            "| Solution | Category | Strength | Model | Entry |\n"
            "|---|---|---|---|---|\n"
            "| Swimm | Platform | Analysis | Software | Before planning |\n"
            "| IBM | Services | Delivery | Consulting | Execution |"
        )
        result = markdown_to_gutenberg(md)
        assert result.count('<th>') == 5
        assert result.count('<tr>') == 3  # 1 header + 2 body


class TestCheckinH1Stripping:
    """Verify that checkin's HTML regeneration strips the H1 title."""

    def test_h1_stripped_from_regenerated_html(self, tmp_path):
        """When article.md has an H1, regenerated HTML should NOT contain an H1 block.
        The title goes to WordPress via metadata.json title field, not as body content."""
        # Create a minimal workbench structure
        article_md = "# My Article Title\n\nFirst paragraph.\n\n## Section One\n\nContent here."
        (tmp_path / 'article.md').write_text(article_md, encoding='utf-8')
        # No original.html — forces regeneration

        # Simulate what checkin does: strip H1 then convert
        import re as _re
        md_content = article_md
        md_content = _re.sub(r'^#\s+.+\n*', '', md_content, count=1)
        html_content = markdown_to_gutenberg(md_content)

        # Should NOT have an H1 heading block
        assert '<!-- wp:heading {"level":1} -->' not in html_content
        assert '<h1' not in html_content
        # Should still have the H2 and paragraph
        assert '<!-- wp:heading -->' in html_content
        assert '<!-- wp:paragraph -->' in html_content


# ===========================================================================
# Edge Case Tests
# ===========================================================================

class TestEdgeCases:
    def test_empty_input(self):
        assert markdown_to_gutenberg('') == ''
        assert markdown_to_gutenberg('   ') == ''
        assert markdown_to_gutenberg('\n\n') == ''

    def test_consecutive_headings(self):
        md = "## First\n\n## Second"
        result = markdown_to_gutenberg(md)
        assert result.count('<!-- wp:heading -->') == 2
        assert 'First' in result
        assert 'Second' in result

    def test_heading_then_paragraph(self):
        md = "## Title\n\nSome paragraph text."
        result = markdown_to_gutenberg(md)
        assert '<!-- wp:heading -->' in result
        assert '<!-- wp:paragraph -->' in result

    def test_multiple_block_types(self):
        md = "## Heading\n\nA paragraph.\n\n- Item 1\n- Item 2\n\nAnother paragraph."
        result = markdown_to_gutenberg(md)
        top_level = extract_opening_blocks(result)
        assert top_level == ['heading', 'paragraph', 'list', 'paragraph']

    def test_bold_italic_combined(self):
        result = markdown_to_gutenberg("This has **bold** and *italic* text.")
        assert '<strong>bold</strong>' in result
        assert '<em>italic</em>' in result


# ===========================================================================
# Integration Tests — Full Article Conversion
# ===========================================================================

class TestFullArticleConversion:
    """Compare markdown_to_gutenberg() output against known-good original.html."""

    @pytest.fixture(params=ARTICLES)
    def article_data(self, request):
        slug = request.param
        folder = os.path.join(WORKBENCH, slug)
        if not os.path.exists(folder):
            pytest.skip(f"Workbench article not found: {slug}")
        return slug, *load_article(slug)

    def test_block_types_match(self, article_data):
        """Verify the set of block types in converted output matches original."""
        slug, md, original_html = article_data
        converted = markdown_to_gutenberg(md)

        original_types = set(extract_opening_blocks(original_html))
        converted_types = set(extract_opening_blocks(converted))

        # Converted should have the same core block types
        # (may not have image IDs or other WordPress-specific attributes)
        expected_core = {'paragraph', 'heading', 'list'}
        assert expected_core.issubset(converted_types), \
            f"[{slug}] Missing core block types. Got: {converted_types}"

    def test_block_sequence_starts_correctly(self, article_data):
        """Verify the first few blocks match the original sequence."""
        slug, md, original_html = article_data
        converted = markdown_to_gutenberg(md)

        original_blocks = extract_opening_blocks(original_html)[:10]
        converted_blocks = extract_opening_blocks(converted)[:10]

        # First block should match (typically heading)
        assert original_blocks[0] == converted_blocks[0], \
            f"[{slug}] First block mismatch: {original_blocks[0]} vs {converted_blocks[0]}"

    def test_heading_count_matches(self, article_data):
        """Verify heading count is similar between original and converted."""
        slug, md, original_html = article_data
        converted = markdown_to_gutenberg(md)

        original_count = len(re.findall(r'<!-- wp:heading', original_html))
        converted_count = len(re.findall(r'<!-- wp:heading', converted))

        # Should be within 20% (markdown may lose H1 or have slight differences)
        assert abs(original_count - converted_count) <= max(3, original_count * 0.2), \
            f"[{slug}] Heading count mismatch: original={original_count}, converted={converted_count}"

    def test_paragraph_count_similar(self, article_data):
        """Verify paragraph count is in the right ballpark."""
        slug, md, original_html = article_data
        converted = markdown_to_gutenberg(md)

        original_count = len(re.findall(r'<!-- wp:paragraph', original_html))
        converted_count = len(re.findall(r'<!-- wp:paragraph', converted))

        # Paragraph count can vary more due to markdown formatting differences
        assert converted_count > 0, f"[{slug}] No paragraphs in converted output"
        assert converted_count >= original_count * 0.5, \
            f"[{slug}] Too few paragraphs: original={original_count}, converted={converted_count}"

    def test_list_count_matches(self, article_data):
        """Verify list block count matches."""
        slug, md, original_html = article_data
        converted = markdown_to_gutenberg(md)

        original_count = len(re.findall(r'<!-- wp:list[\s{>]', original_html))
        converted_count = len(re.findall(r'<!-- wp:list[\s{>]', converted))

        # Tolerance is generous because markdown formatting can split/merge lists
        # (e.g., blank lines between list items create separate lists in markdown)
        assert abs(original_count - converted_count) <= max(5, original_count * 0.5), \
            f"[{slug}] List count mismatch: original={original_count}, converted={converted_count}"

    def test_image_blocks_present(self, article_data):
        """Verify images are converted to image blocks."""
        slug, md, original_html = article_data
        converted = markdown_to_gutenberg(md)

        original_images = len(re.findall(r'<!-- wp:image', original_html))
        converted_images = len(re.findall(r'<!-- wp:image', converted))

        if original_images > 0:
            assert converted_images > 0, \
                f"[{slug}] Original has {original_images} images but converted has none"

    def test_all_blocks_properly_closed(self, article_data):
        """Verify every opening block comment has a matching close."""
        slug, md, original_html = article_data
        converted = markdown_to_gutenberg(md)

        opening = re.findall(r'<!-- wp:([a-z][a-z0-9/-]*)', converted)
        closing = re.findall(r'<!-- /wp:([a-z][a-z0-9/-]*)', converted)

        # Count each block type
        for block_type in set(opening):
            open_count = opening.count(block_type)
            close_count = closing.count(block_type)
            assert open_count == close_count, \
                f"[{slug}] Block '{block_type}' has {open_count} opens but {close_count} closes"

    def test_no_bare_html(self, article_data):
        """Verify no HTML content exists outside of block comments."""
        slug, md, original_html = article_data
        converted = markdown_to_gutenberg(md)

        # Every <p>, <h2-6>, <ul>, <ol>, <figure>, <pre>, <blockquote> should be inside a block
        # Simple check: all <p> tags should have a <!-- wp:paragraph --> somewhere before them
        paragraphs = list(re.finditer(r'<p>', converted))
        for p in paragraphs:
            # Look backwards for a block comment
            before = converted[:p.start()]
            last_open = before.rfind('<!-- wp:')
            last_close = before.rfind('<!-- /wp:')
            assert last_open > last_close, \
                f"[{slug}] Found <p> tag outside of block comment at position {p.start()}"


class TestRoundTrip:
    """Test that html_to_markdown → markdown_to_gutenberg preserves structure."""

    @pytest.fixture(params=ARTICLES[:2])  # Test with first 2 articles for speed
    def article_html(self, request):
        slug = request.param
        folder = os.path.join(WORKBENCH, slug)
        if not os.path.exists(folder):
            pytest.skip(f"Workbench article not found: {slug}")
        with open(os.path.join(folder, 'original.html'), 'r', encoding='utf-8') as f:
            return slug, f.read()

    def test_roundtrip_block_types_preserved(self, article_html):
        """original.html → html_to_markdown → markdown_to_gutenberg should have same block types."""
        slug, html = article_html
        client = WordPressClient.__new__(WordPressClient)
        md = client.html_to_markdown(html)
        reconverted = markdown_to_gutenberg(md)

        original_types = set(extract_opening_blocks(html))
        reconverted_types = set(extract_opening_blocks(reconverted))

        # Core types should survive the round trip
        core_types = original_types & {'paragraph', 'heading', 'list'}
        assert core_types.issubset(reconverted_types), \
            f"[{slug}] Lost block types in round trip. Original: {original_types}, Reconverted: {reconverted_types}"

    def test_roundtrip_first_block_matches(self, article_html):
        """First block type should be the same after round trip."""
        slug, html = article_html
        client = WordPressClient.__new__(WordPressClient)
        md = client.html_to_markdown(html)
        reconverted = markdown_to_gutenberg(md)

        original_first = extract_opening_blocks(html)[0] if extract_opening_blocks(html) else None
        reconverted_first = extract_opening_blocks(reconverted)[0] if extract_opening_blocks(reconverted) else None

        assert original_first == reconverted_first, \
            f"[{slug}] First block changed: {original_first} → {reconverted_first}"


# ===========================================================================
# Publish Markdown Tests (preview mode only — no WordPress API calls)
# ===========================================================================

class TestPublishMarkdownPreview:
    """Test publish_markdown() in preview mode (push=False). No API calls made."""

    def test_preview_from_workbench_article(self):
        """Preview converting a real workbench article.md."""
        md_path = os.path.join(WORKBENCH, ARTICLES[0], 'article.md')
        if not os.path.exists(md_path):
            pytest.skip("Workbench article not found")
        success, result = publish_markdown(md_path, push=False)
        assert success
        assert 'PUBLISH PREVIEW' in result
        assert 'Gutenberg Blocks:' in result
        assert 'not pushed' in result

    def test_preview_extracts_title_from_h1(self):
        """Title should be extracted from the first H1 in the markdown."""
        md_path = os.path.join(WORKBENCH, ARTICLES[0], 'article.md')
        if not os.path.exists(md_path):
            pytest.skip("Workbench article not found")
        success, result = publish_markdown(md_path, push=False)
        assert success
        # The COBOL article has an H1 title
        assert 'COBOL' in result or 'Mainframe' in result or 'Title:' in result

    def test_preview_with_explicit_title(self):
        """Explicit title should override H1."""
        md_path = os.path.join(WORKBENCH, ARTICLES[0], 'article.md')
        if not os.path.exists(md_path):
            pytest.skip("Workbench article not found")
        success, result = publish_markdown(md_path, title="Custom Title", push=False)
        assert success
        assert 'Custom Title' in result

    def test_preview_shows_post_type(self):
        """Preview should show the post type."""
        md_path = os.path.join(WORKBENCH, ARTICLES[0], 'article.md')
        if not os.path.exists(md_path):
            pytest.skip("Workbench article not found")

        success1, result1 = publish_markdown(md_path, post_type='article', push=False)
        assert 'Post Type: article' in result1

        success2, result2 = publish_markdown(md_path, post_type='posts', push=False)
        assert 'Post Type: posts' in result2

    def test_preview_nonexistent_file(self):
        """Should fail gracefully for missing files."""
        success, result = publish_markdown('/nonexistent/file.md', push=False)
        assert not success
        assert 'not found' in result.lower()

    def test_preview_has_block_count(self):
        """Preview should report how many Gutenberg blocks were generated."""
        md_path = os.path.join(WORKBENCH, ARTICLES[0], 'article.md')
        if not os.path.exists(md_path):
            pytest.skip("Workbench article not found")
        success, result = publish_markdown(md_path, push=False)
        assert success
        # Extract block count from preview
        import re as _re
        count_match = _re.search(r'Gutenberg Blocks: (\d+)', result)
        assert count_match, "Block count not found in preview"
        assert int(count_match.group(1)) > 10, "Expected at least 10 blocks for a full article"

    def test_preview_with_meta(self):
        """Preview should show meta title and description when provided."""
        md_path = os.path.join(WORKBENCH, ARTICLES[0], 'article.md')
        if not os.path.exists(md_path):
            pytest.skip("Workbench article not found")
        success, result = publish_markdown(
            md_path,
            meta_description="A great description.",
            push=False,
        )
        assert success
        assert 'A great description.' in result
