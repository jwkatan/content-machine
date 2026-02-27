"""
Swimm Branded PDF Builder

Converts a PDF-format content.md into branded HTML, then renders to PDF
via Puppeteer. Completely standalone — does not import or modify any
existing modules (wordpress_client, content_scrubber, etc.).

Usage:
    from data_sources.modules.pdf_builder import generate_pdf
    result = generate_pdf('content.md', 'output.pdf', template_type='whitepaper')

The content.md format uses these conventions:
    - Front matter block (between --- markers): title-bold, title-regular,
      tagline, cta-text, cta-url
    - ## Chapter Heading → new body page
    - ### Callout + blockquote → callout box
    - ### Stats + bullet list (value | label) → stat tiles
    - ### Table + markdown table → data table
    - ### Graphic + [caption](path) → image/placeholder
    - --- horizontal rule → page break
"""

import os
import re
import subprocess
import html as html_module

# ---------------------------------------------------------------------------
# Project root (two levels up from this module file)
# ---------------------------------------------------------------------------
_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_MODULE_DIR, '..', '..'))
_PDF_BUILDER_DIR = os.path.join(_PROJECT_ROOT, 'pdf-builder')


# ---------------------------------------------------------------------------
# 1. INLINE MARKDOWN → HTML (independent of wordpress_client.py)
# ---------------------------------------------------------------------------

def _convert_inline(text: str) -> str:
    """Convert inline markdown (bold, italic, links, code) to HTML."""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def _markdown_to_body_html(text: str) -> str:
    """
    Convert a block of body markdown (paragraphs + lists) to HTML
    wrapped in body-text divs.
    """
    lines = text.strip().split('\n')
    result = []
    current_list = []  # (type, items) where type is 'ul' or 'ol'
    list_type = None
    paragraphs = []

    def flush_list():
        nonlocal current_list, list_type
        if current_list:
            tag = list_type
            items = ''.join(f'<li>{_convert_inline(item)}</li>' for item in current_list)
            paragraphs.append(f'<{tag}>{items}</{tag}>')
            current_list = []
            list_type = None

    def flush_paragraph(text_block):
        text_block = text_block.strip()
        if text_block:
            paragraphs.append(f'<p>{_convert_inline(text_block)}</p>')

    current_para = []

    for line in lines:
        stripped = line.strip()

        # Unordered list item
        if re.match(r'^[-*]\s', stripped):
            if current_para:
                flush_paragraph('\n'.join(current_para))
                current_para = []
            if list_type and list_type != 'ul':
                flush_list()
            list_type = 'ul'
            current_list.append(re.sub(r'^[-*]\s+', '', stripped))
            continue

        # Ordered list item
        if re.match(r'^\d+\.\s', stripped):
            if current_para:
                flush_paragraph('\n'.join(current_para))
                current_para = []
            if list_type and list_type != 'ol':
                flush_list()
            list_type = 'ol'
            current_list.append(re.sub(r'^\d+\.\s+', '', stripped))
            continue

        # Continuation of list item (indented)
        if current_list and stripped and (line.startswith('  ') or line.startswith('\t')):
            current_list[-1] += ' ' + stripped
            continue

        # Empty line = paragraph break
        if not stripped:
            flush_list()
            if current_para:
                flush_paragraph('\n'.join(current_para))
                current_para = []
            continue

        # Regular text
        flush_list()
        current_para.append(stripped)

    flush_list()
    if current_para:
        flush_paragraph('\n'.join(current_para))

    if paragraphs:
        inner = '\n      '.join(paragraphs)
        return f'    <div class="body-text">\n      {inner}\n    </div>'
    return ''


# ---------------------------------------------------------------------------
# 2. PARSE content.md
# ---------------------------------------------------------------------------

def parse_content_md(content_md_path: str) -> dict:
    """
    Parse a PDF-format content.md file into a structured dict.

    Returns:
        {
            'cover': {
                'title_bold': str,
                'title_regular': str,
            },
            'back_cover': {
                'tagline': str,
                'cta_text': str,
                'cta_url': str,
            },
            'pages': [
                {
                    'heading': str,
                    'blocks': [
                        {'type': 'text', 'content': str},
                        {'type': 'callout', 'content': str},
                        {'type': 'stats', 'items': [{'value': str, 'label': str}]},
                        {'type': 'table', 'headers': [str], 'rows': [[str]]},
                        {'type': 'graphic', 'caption': str, 'path': str},
                    ]
                }
            ]
        }
    """
    with open(content_md_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    # Strip HTML comments
    content = re.sub(r'<!--.*?-->', '', raw, flags=re.DOTALL)

    # --- Extract front matter ---
    cover = {'title_bold': '', 'title_regular': ''}
    back_cover = {'tagline': '', 'cta_text': '', 'cta_url': ''}

    # Front matter is between the first two --- markers
    fm_match = re.search(
        r'^---\s*\n(.*?)\n---\s*$',
        content,
        flags=re.MULTILINE | re.DOTALL
    )
    if fm_match:
        fm_block = fm_match.group(1)

        def extract_fm(key):
            m = re.search(rf'^{key}:\s*"?(.+?)"?\s*$', fm_block, re.MULTILINE)
            return m.group(1).strip().strip('"') if m else ''

        cover['title_bold'] = extract_fm('title-bold')
        cover['title_regular'] = extract_fm('title-regular')
        back_cover['tagline'] = extract_fm('tagline')
        back_cover['cta_text'] = extract_fm('cta-text')
        back_cover['cta_url'] = extract_fm('cta-url')

        # Remove front matter from body
        content = content[fm_match.end():].strip()

    # --- Split body into pages ---
    # Split on ## headings and --- horizontal rules
    # Each ## starts a new page; --- also forces a page break
    pages = []
    current_page = None

    # Split by lines, track page boundaries
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]

        # --- = page break (only if it's a standalone rule, not front matter)
        if re.match(r'^---+\s*$', line) and current_page is not None:
            # Force a page break: close current page and start a continuation
            if current_page:
                pages.append(current_page)
            current_page = {'heading': '', 'blocks': []}
            i += 1
            continue

        # ## heading = new page
        heading_match = re.match(r'^##\s+(.+)$', line)
        if heading_match:
            if current_page is not None:
                pages.append(current_page)
            current_page = {'heading': heading_match.group(1).strip(), 'blocks': []}
            i += 1
            continue

        # ### special blocks
        special_match = re.match(r'^###\s+(.+)$', line)
        if special_match and current_page is not None:
            block_type = special_match.group(1).strip().lower()
            i += 1

            if block_type == 'callout':
                # Skip blank lines before blockquote
                while i < len(lines) and not lines[i].strip():
                    i += 1
                # Collect blockquote lines
                callout_lines = []
                while i < len(lines):
                    if lines[i].strip().startswith('>'):
                        callout_lines.append(
                            re.sub(r'^>\s*', '', lines[i].strip())
                        )
                        i += 1
                    elif not lines[i].strip() and callout_lines:
                        i += 1
                        break
                    elif not lines[i].strip():
                        i += 1  # skip blank lines before content
                    else:
                        break
                callout_text = ' '.join(callout_lines).strip().strip('"')
                current_page['blocks'].append({
                    'type': 'callout',
                    'content': callout_text
                })

            elif block_type == 'stats':
                # Skip blank lines before bullet items
                while i < len(lines) and not lines[i].strip():
                    i += 1
                # Collect bullet items with value | label
                stats = []
                while i < len(lines):
                    stat_match = re.match(
                        r'^[-*]\s+(.+?)\s*\|\s*(.+)$', lines[i].strip()
                    )
                    if stat_match:
                        stats.append({
                            'value': stat_match.group(1).strip(),
                            'label': stat_match.group(2).strip()
                        })
                        i += 1
                    elif not lines[i].strip() and stats:
                        i += 1
                        break
                    elif not lines[i].strip():
                        i += 1  # skip blank lines before content
                    else:
                        break
                current_page['blocks'].append({
                    'type': 'stats',
                    'items': stats
                })

            elif block_type == 'table':
                # Collect markdown table
                headers = []
                rows = []
                # Skip blank lines
                while i < len(lines) and not lines[i].strip():
                    i += 1
                # Header row
                if i < len(lines) and '|' in lines[i]:
                    headers = [
                        c.strip() for c in lines[i].strip().strip('|').split('|')
                    ]
                    i += 1
                # Separator row
                if i < len(lines) and re.match(r'^[\s|:-]+$', lines[i]):
                    i += 1
                # Data rows
                while i < len(lines) and '|' in lines[i]:
                    row = [
                        c.strip()
                        for c in lines[i].strip().strip('|').split('|')
                    ]
                    rows.append(row)
                    i += 1
                current_page['blocks'].append({
                    'type': 'table',
                    'headers': headers,
                    'rows': rows
                })

            elif block_type == 'graphic':
                # [caption](path)
                while i < len(lines) and not lines[i].strip():
                    i += 1
                caption = ''
                img_path = 'placeholder'
                if i < len(lines):
                    gfx_match = re.match(
                        r'^\[(.+?)\]\((.+?)\)', lines[i].strip()
                    )
                    if gfx_match:
                        caption = gfx_match.group(1)
                        img_path = gfx_match.group(2)
                        i += 1
                current_page['blocks'].append({
                    'type': 'graphic',
                    'caption': caption,
                    'path': img_path
                })

            else:
                # Unknown ### block — treat as text
                pass
            continue

        # Regular body text — accumulate
        if current_page is not None:
            text_lines = []
            while i < len(lines):
                if re.match(r'^##\s+', lines[i]):
                    break
                if re.match(r'^###\s+', lines[i]):
                    break
                if re.match(r'^---+\s*$', lines[i]):
                    break
                text_lines.append(lines[i])
                i += 1
            text_block = '\n'.join(text_lines).strip()
            if text_block:
                current_page['blocks'].append({
                    'type': 'text',
                    'content': text_block
                })
            continue

        i += 1

    if current_page is not None:
        pages.append(current_page)

    # Drop empty pages (no heading and no blocks) — caused by ---
    # immediately before a ## heading
    pages = [p for p in pages if p.get('heading') or p.get('blocks')]

    return {
        'cover': cover,
        'back_cover': back_cover,
        'pages': pages,
    }


# ---------------------------------------------------------------------------
# 3. RENDER HTML
# ---------------------------------------------------------------------------

def render_html(
    parsed: dict,
    template_type: str = 'whitepaper',
    output_path: str | None = None,
) -> str:
    """
    Generate a complete branded HTML document from parsed content.

    Args:
        parsed: Output of parse_content_md()
        template_type: Template directory name (e.g., 'whitepaper')
        output_path: Where the HTML will be saved (needed for relative CSS path)

    Returns:
        Complete HTML string
    """
    template_dir = os.path.join(_PDF_BUILDER_DIR, 'templates', template_type)
    assets_dir = os.path.join(_PDF_BUILDER_DIR, 'assets')

    # Compute relative paths from output location to assets dir
    if output_path:
        output_dir = os.path.dirname(os.path.abspath(output_path))
    else:
        output_dir = _PROJECT_ROOT

    logo_path = os.path.relpath(
        os.path.join(assets_dir, 'Logo.svg'), output_dir
    )
    hand_icon_path = os.path.relpath(
        os.path.join(assets_dir, 'Hand icon.svg'), output_dir
    )

    # Read CSS to inline it (brand checker needs to see font/page declarations
    # in the HTML source, and inlining makes the HTML self-contained/portable)
    css_file = os.path.join(template_dir, 'styles.css')
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()

    cover = parsed['cover']
    back = parsed['back_cover']
    pages = parsed['pages']

    # --- Build HTML ---
    html_parts = []

    # Document head
    html_parts.append(f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_module.escape(cover.get("title_bold", "Swimm Whitepaper"))}</title>

  <!-- Roc Grotesk via Adobe Fonts / TypeKit -->
  <link rel="stylesheet" href="https://use.typekit.net/ghp6lrn.css">

  <!-- Mulish via Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Mulish:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
{css_content}
  </style>
</head>
<body>
''')

    # --- Cover page ---
    # Figma asset URLs (expire ~7 days — refresh via Figma MCP node 3614:4
    # in file UYfMt04X79c7y7YXAhy3DI if they stop loading)
    asterisk_url = 'https://www.figma.com/api/mcp/asset/4d1b0b54-56f4-4d92-8a83-afe9061f547d'
    wave_url = 'https://www.figma.com/api/mcp/asset/45b20551-f063-4f36-94e7-bf0049e0df72'

    html_parts.append(f'''
<!-- COVER PAGE -->
<div class="page cover-page">
  <div class="cover-fade--top" aria-hidden="true"></div>
  <div class="cover-fade--bottom" aria-hidden="true"></div>

  <div class="cover-logo">
    <img src="{html_module.escape(logo_path)}" alt="Swimm">
  </div>

  <div class="cover-content">
    <div class="cover-title-block">
      <p class="cover-title-bold">{html_module.escape(cover.get("title_bold", ""))}</p>
      {'<p class="cover-title-regular">' + html_module.escape(cover.get("title_regular", "")) + '</p>' if cover.get("title_regular") else ''}
    </div>
    <div class="cover-asterisk" aria-hidden="true">
      <img src="{asterisk_url}" alt="">
    </div>
  </div>

  <div class="cover-wave" aria-hidden="true">
    <img src="{wave_url}" alt="">
  </div>
</div>
''')

    # --- Body pages ---
    page_num = 2  # Page 1 is cover

    for page_data in pages:
        heading = page_data.get('heading', '')
        blocks = page_data.get('blocks', [])

        html_parts.append(f'''
<!-- BODY PAGE {page_num} -->
<div class="page body-page">
  <div class="body-bar" aria-hidden="true"></div>
  <div class="body-content">
''')

        if heading:
            html_parts.append(
                f'    <h2 class="body-heading">'
                f'{_convert_inline(html_module.escape(heading))}</h2>'
            )

        for block in blocks:
            btype = block['type']

            if btype == 'text':
                html_parts.append(_markdown_to_body_html(block['content']))

            elif btype == 'callout':
                text = _convert_inline(html_module.escape(block['content']))
                html_parts.append(f'''    <div class="body-callout">
      <p>{text}</p>
    </div>''')

            elif btype == 'stats':
                tiles = []
                for stat in block['items'][:3]:  # Max 3 per row
                    val = html_module.escape(stat['value'])
                    label = html_module.escape(stat['label'])
                    tiles.append(
                        f'      <div class="body-stat">\n'
                        f'        <span class="body-stat__value">{val}</span>\n'
                        f'        <span class="body-stat__label">{label}</span>\n'
                        f'      </div>'
                    )
                html_parts.append(
                    '    <div class="body-stats">\n'
                    + '\n'.join(tiles) + '\n'
                    + '    </div>'
                )

            elif btype == 'table':
                headers = block.get('headers', [])
                rows = block.get('rows', [])
                th_cells = ''.join(
                    f'<th>{_convert_inline(html_module.escape(h))}</th>'
                    for h in headers
                )
                tr_rows = []
                for row in rows:
                    cells = ''.join(
                        f'<td>{_convert_inline(html_module.escape(c))}</td>'
                        for c in row
                    )
                    tr_rows.append(f'      <tr>{cells}</tr>')

                html_parts.append(
                    f'    <table class="body-table">\n'
                    f'      <thead><tr>{th_cells}</tr></thead>\n'
                    f'      <tbody>\n'
                    + '\n'.join(tr_rows) + '\n'
                    + '      </tbody>\n'
                    + '    </table>'
                )

            elif btype == 'graphic':
                caption = html_module.escape(block.get('caption', ''))
                img_path = block.get('path', 'placeholder')
                if img_path == 'placeholder' or not img_path:
                    html_parts.append(
                        f'    <div class="body-graphic">\n'
                        f'      <span class="body-graphic__label">'
                        f'{caption or "Image / Diagram placeholder"}'
                        f'</span>\n'
                        f'    </div>'
                    )
                else:
                    html_parts.append(
                        f'    <div class="body-graphic">\n'
                        f'      <img src="{html_module.escape(img_path)}" '
                        f'alt="{caption}" style="width:100%;height:auto">\n'
                        f'      <span class="body-graphic__label">{caption}</span>\n'
                        f'    </div>'
                    )

        html_parts.append(f'''  </div>
  <div class="body-divider" aria-hidden="true"></div>
  <div class="body-footer-logo">
    <img src="{html_module.escape(logo_path)}" alt="Swimm">
  </div>
  <span class="body-page-num">{page_num}</span>
</div>
''')
        page_num += 1

    # --- Back cover ---
    html_parts.append(f'''
<!-- BACK COVER -->
<div class="page back-cover-page">
  <div class="back-cover-content">
    <div class="back-cover-logo">
      <img src="{html_module.escape(logo_path)}" alt="Swimm">
    </div>
    <p class="back-cover-tagline">{html_module.escape(back.get("tagline", ""))}</p>
    <a class="back-cover-cta" href="{html_module.escape(back.get("cta_url", "#"))}">
      {html_module.escape(back.get("cta_text", "Learn more"))}
    </a>
  </div>
</div>

</body>
</html>
''')

    return '\n'.join(html_parts)


# ---------------------------------------------------------------------------
# 4. GENERATE PDF (end-to-end pipeline)
# ---------------------------------------------------------------------------

def generate_pdf(
    content_md_path: str,
    output_pdf_path: str,
    template_type: str = 'whitepaper',
) -> dict:
    """
    End-to-end pipeline: content.md → HTML → PDF with brand verification.

    Args:
        content_md_path: Path to the PDF-format content.md file
        output_pdf_path: Where to save the final PDF
        template_type: Template to use (default: 'whitepaper')

    Returns:
        {
            'pdf_path': str,
            'html_path': str,
            'brand_check_passed': bool,
            'brand_check_output': str,
            'page_count': int,
        }
    """
    content_md_path = os.path.abspath(content_md_path)
    output_pdf_path = os.path.abspath(output_pdf_path)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

    # 1. Parse content
    parsed = parse_content_md(content_md_path)
    page_count = len(parsed['pages']) + 2  # +2 for cover and back cover

    # 2. Generate HTML
    html_path = output_pdf_path.replace('.pdf', '.html')
    html_content = render_html(parsed, template_type, output_path=html_path)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f'HTML generated → {html_path} ({page_count} pages)')

    # 3. Render PDF via Puppeteer
    generate_script = os.path.join(_PDF_BUILDER_DIR, 'generate-pdf.js')
    pdf_result = subprocess.run(
        ['node', generate_script, html_path, output_pdf_path],
        capture_output=True,
        text=True,
        cwd=_PDF_BUILDER_DIR,
    )

    if pdf_result.returncode != 0:
        print(f'PDF generation failed:\n{pdf_result.stderr}')
        return {
            'pdf_path': None,
            'html_path': html_path,
            'brand_check_passed': False,
            'brand_check_output': pdf_result.stderr,
            'page_count': page_count,
        }

    print(pdf_result.stdout)

    # 4. Brand verification
    brand_check_script = os.path.join(_PDF_BUILDER_DIR, 'verify', 'brand-check.js')
    check_result = subprocess.run(
        ['node', brand_check_script, html_path],
        capture_output=True,
        text=True,
        cwd=_PDF_BUILDER_DIR,
    )

    brand_passed = check_result.returncode == 0
    print(check_result.stdout)
    if not brand_passed:
        print(f'Brand check issues:\n{check_result.stderr}')

    return {
        'pdf_path': output_pdf_path,
        'html_path': html_path,
        'brand_check_passed': brand_passed,
        'brand_check_output': check_result.stdout,
        'page_count': page_count,
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: python pdf_builder.py <content.md> <output.pdf> [template_type]')
        sys.exit(1)

    content_path = sys.argv[1]
    output_path = sys.argv[2]
    tpl_type = sys.argv[3] if len(sys.argv) > 3 else 'whitepaper'

    result = generate_pdf(content_path, output_path, tpl_type)
    print(f'\nResult: {result}')
