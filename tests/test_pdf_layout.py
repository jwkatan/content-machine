"""
Test suite for PDF builder layout behavior.

Tests that the whitepaper PDF builder produces flowing body content
instead of fixed-height page boxes, while preserving cover and back
cover as fixed pages.

Layout rules:
1. Content flows continuously across pages (no forced page breaks per section)
2. Page breaks only to prevent orphans (heading alone at bottom, or 1-2 lines on next page)
3. Tables, callouts, and stats never split across pages
4. Cover page is a fixed-size page
5. Back cover is a fixed-size page
6. Body content is NOT clipped by overflow:hidden
"""

import os
import re
import sys
import pytest

# Add project root to path
_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_TEST_DIR, '..'))
sys.path.insert(0, _PROJECT_ROOT)

from data_sources.modules.pdf_builder import parse_content_md, render_html


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_CONTENT_MD = """\
---
title-bold: "Test Title"
title-regular: "Subtitle"
tagline: "Test Tagline"
cta-text: "Click here"
cta-url: "https://example.com"
---

## Section One

First section paragraph one.

First section paragraph two.

### Table

| Col A | Col B |
|---|---|
| val1 | val2 |

### Callout

> This is a callout quote.

More text after callout.

## Section Two

Second section paragraph one.

### Stats

- 100 | items counted
- 50 | things measured

Second section continued text.

## Section Three

Third section only paragraph.

### Callout

> Final callout here.
"""


@pytest.fixture
def sample_md_path(tmp_path):
    """Write sample content.md to a temp file and return path."""
    md_file = tmp_path / "content-pdf.md"
    md_file.write_text(SAMPLE_CONTENT_MD)
    return str(md_file)


@pytest.fixture
def parsed(sample_md_path):
    """Parse the sample content.md."""
    return parse_content_md(sample_md_path)


@pytest.fixture
def html_output(parsed, tmp_path):
    """Render HTML from parsed content."""
    output_path = str(tmp_path / "output.html")
    return render_html(parsed, 'whitepaper', output_path=output_path)


# ---------------------------------------------------------------------------
# Test: Cover and back cover are fixed pages
# ---------------------------------------------------------------------------

class TestCoverPages:
    def test_cover_is_fixed_page(self, html_output):
        """Cover page must be a fixed-size .page div."""
        assert 'class="page cover-page"' in html_output

    def test_back_cover_is_fixed_page(self, html_output):
        """Back cover must be a fixed-size .page div."""
        assert 'class="page back-cover-page"' in html_output

    def test_cover_has_title(self, html_output):
        """Cover page shows the title from front matter."""
        assert 'Test Title' in html_output

    def test_back_cover_has_cta(self, html_output):
        """Back cover shows CTA text."""
        assert 'Click here' in html_output


# ---------------------------------------------------------------------------
# Test: Body uses single flowing container (NOT multiple fixed pages)
# ---------------------------------------------------------------------------

class TestBodyFlowLayout:
    def test_body_uses_flow_container(self, html_output):
        """Body content must be in a single .body-flow container, not
        multiple .body-page divs."""
        assert 'class="body-flow"' in html_output

    def test_no_body_page_divs(self, html_output):
        """There must be NO .body-page divs — content flows freely."""
        # The old pattern wrapped each section in <div class="page body-page">
        assert 'class="page body-page"' not in html_output

    def test_all_sections_in_one_container(self, html_output):
        """All section headings must appear inside the single body-flow div."""
        # Extract body-flow content
        flow_match = re.search(
            r'class="body-flow"[^>]*>(.*?)</div>\s*<!--\s*end body-flow',
            html_output,
            re.DOTALL
        )
        assert flow_match is not None, "body-flow container not found"
        flow_content = flow_match.group(1)

        # All three section headings should be inside the flow container
        assert 'Section One' in flow_content
        assert 'Section Two' in flow_content
        assert 'Section Three' in flow_content

    def test_headings_rendered_as_h2(self, html_output):
        """Section headings from ## must render as <h2> tags."""
        h2_matches = re.findall(r'<h2[^>]*>.*?</h2>', html_output)
        heading_texts = [re.sub(r'<[^>]+>', '', h) for h in h2_matches]
        assert 'Section One' in heading_texts
        assert 'Section Two' in heading_texts
        assert 'Section Three' in heading_texts


# ---------------------------------------------------------------------------
# Test: Block elements have break protection
# ---------------------------------------------------------------------------

class TestOrphanProtection:
    """Verify that the generated HTML includes CSS classes or inline styles
    that prevent orphaned content across page breaks."""

    def test_tables_have_no_break_class(self, html_output):
        """Tables must have a class that maps to break-inside: avoid."""
        # Every <table> should have the body-table class
        tables = re.findall(r'<table[^>]*class="([^"]*)"', html_output)
        for cls in tables:
            assert 'body-table' in cls

    def test_callouts_have_no_break_class(self, html_output):
        """Callout boxes must not be split across pages."""
        callouts = re.findall(r'<div[^>]*class="([^"]*body-callout[^"]*)"', html_output)
        assert len(callouts) > 0, "No callouts found in output"

    def test_stats_have_no_break_class(self, html_output):
        """Stat tile rows must not be split across pages."""
        stats = re.findall(r'<div[^>]*class="([^"]*body-stats[^"]*)"', html_output)
        assert len(stats) > 0, "No stats found in output"


# ---------------------------------------------------------------------------
# Test: CSS rules for flow layout
# ---------------------------------------------------------------------------

class TestFlowCSS:
    """Verify the CSS file contains required flow-mode rules."""

    @pytest.fixture(autouse=True)
    def load_css(self):
        css_path = os.path.join(
            _PROJECT_ROOT, 'pdf-builder', 'templates', 'whitepaper', 'styles.css'
        )
        with open(css_path, 'r') as f:
            self.css = f.read()

    def test_body_flow_no_fixed_height(self):
        """The .body-flow class must NOT have a fixed height like 297mm."""
        # Extract all .body-flow rules
        flow_rules = re.findall(
            r'\.body-flow\s*\{([^}]*)\}', self.css
        )
        for rule in flow_rules:
            assert '297mm' not in rule, \
                ".body-flow must not have fixed 297mm height"

    def test_body_flow_no_overflow_hidden(self):
        """The .body-flow content area must NOT clip content."""
        flow_rules = re.findall(
            r'\.body-flow[^{]*\{([^}]*)\}', self.css
        )
        for rule in flow_rules:
            assert 'overflow: hidden' not in rule.replace(' ', '').lower(), \
                ".body-flow must not use overflow:hidden"
            assert 'overflow:hidden' not in rule.replace(' ', '').lower(), \
                ".body-flow must not use overflow:hidden"

    def test_tables_break_inside_avoid(self):
        """CSS must set break-inside: avoid on .body-table."""
        assert re.search(
            r'\.body-table[^{]*\{[^}]*break-inside:\s*avoid',
            self.css
        ), ".body-table must have break-inside: avoid"

    def test_callouts_break_inside_avoid(self):
        """CSS must set break-inside: avoid on .body-callout."""
        assert re.search(
            r'\.body-callout[^{]*\{[^}]*break-inside:\s*avoid',
            self.css
        ), ".body-callout must have break-inside: avoid"

    def test_stats_break_inside_avoid(self):
        """CSS must set break-inside: avoid on .body-stats."""
        assert re.search(
            r'\.body-stats[^{]*\{[^}]*break-inside:\s*avoid',
            self.css
        ), ".body-stats must have break-inside: avoid"

    def test_headings_break_after_avoid(self):
        """CSS must set break-after: avoid on .body-heading to prevent
        orphaned headings at the bottom of a page."""
        assert re.search(
            r'\.body-heading[^{]*\{[^}]*break-after:\s*avoid',
            self.css
        ), ".body-heading must have break-after: avoid"

    def test_body_text_has_orphan_widow_rules(self):
        """Body text should have orphans/widows set to prevent
        1-2 line fragments."""
        assert re.search(
            r'\.body-text[^{]*\{[^}]*orphans:\s*[3-9]',
            self.css
        ), ".body-text should set orphans >= 3"
        assert re.search(
            r'\.body-text[^{]*\{[^}]*widows:\s*[3-9]',
            self.css
        ), ".body-text should set widows >= 3"


# ---------------------------------------------------------------------------
# Test: Page count is not hardcoded from sections
# ---------------------------------------------------------------------------

class TestPageCount:
    def test_page_count_not_section_count(self, parsed):
        """The page count should NOT simply be len(pages) + 2.
        With flow layout, the builder can't know exact page count
        until Puppeteer renders. The parsed data should still contain
        sections but they shouldn't dictate page boundaries."""
        sections = parsed['pages']
        assert len(sections) == 3, "Should parse 3 sections from sample"
        # Each section has content — this verifies parsing still works
        assert sections[0]['heading'] == 'Section One'
        assert sections[1]['heading'] == 'Section Two'
        assert sections[2]['heading'] == 'Section Three'


# ---------------------------------------------------------------------------
# Test: Content integrity (blocks parsed correctly)
# ---------------------------------------------------------------------------

class TestContentIntegrity:
    def test_tables_rendered(self, html_output):
        """Tables from ### Table blocks must appear in output."""
        assert '<table class="body-table">' in html_output
        assert 'Col A' in html_output
        assert 'val1' in html_output

    def test_callouts_rendered(self, html_output):
        """Callouts from ### Callout blocks must appear in output."""
        assert 'body-callout' in html_output
        assert 'This is a callout quote.' in html_output

    def test_stats_rendered(self, html_output):
        """Stats from ### Stats blocks must appear in output."""
        assert 'body-stats' in html_output
        assert '100' in html_output
        assert 'items counted' in html_output

    def test_body_text_rendered(self, html_output):
        """Regular paragraphs must appear in body-text divs."""
        assert 'First section paragraph one.' in html_output
        assert 'Second section paragraph one.' in html_output
        assert 'Third section only paragraph.' in html_output

    def test_text_between_blocks_rendered(self, html_output):
        """Text that appears after special blocks (like after a callout)
        must still be rendered."""
        assert 'More text after callout.' in html_output
        assert 'Second section continued text.' in html_output
