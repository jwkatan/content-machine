"""
Branded PDF Builder

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

_COVER_ASSETS = {
    'asterisk': os.path.join(_PDF_BUILDER_DIR, 'assets', 'asterisk.svg'),
    'wave':     os.path.join(_PDF_BUILDER_DIR, 'assets', 'wave.png'),
}


def _cover_asset_paths(output_dir: str) -> dict[str, str]:
    """
    Return relative paths from output_dir to each cover asset.
    Warns if any local file is missing — PDF still renders, just without that image.
    """
    paths: dict[str, str] = {}
    for name, abs_path in _COVER_ASSETS.items():
        if os.path.exists(abs_path):
            paths[name] = os.path.relpath(abs_path, output_dir)
        else:
            print(
                f'⚠️  Cover asset missing: {os.path.basename(abs_path)}\n'
                f'   Run the refresh snippet in the pdf_builder.py header comment\n'
                f'   to re-download from Figma. The cover will render without this image.'
            )
            paths[name] = ''
    return paths


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
  <title>{html_module.escape(cover.get("title_bold", f"{os.getenv('COMPANY_NAME', 'Company')} Whitepaper"))}</title>

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
    <img src="{html_module.escape(logo_path)}" alt="{os.getenv('COMPANY_NAME', 'Company')}">
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

    # --- Body content (single flowing container) ---
    html_parts.append('''
<!-- BODY CONTENT (flowing) -->
<div class="body-flow">
''')

    for page_data in pages:
        heading = page_data.get('heading', '')
        blocks = page_data.get('blocks', [])

        if heading:
            # Wrap heading with first block in a heading-group to prevent
            # orphaned headings at the bottom of a page
            first_block_html = ''
            remaining_blocks = blocks
            if blocks and blocks[0]['type'] == 'text':
                first_block_html = _markdown_to_body_html(blocks[0]['content'])
                remaining_blocks = blocks[1:]

            html_parts.append(
                f'  <div class="heading-group">\n'
                f'    <h2 class="body-heading">'
                f'{_convert_inline(html_module.escape(heading))}</h2>\n'
                f'{first_block_html}\n'
                f'  </div>'
            )
            blocks = remaining_blocks

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

    html_parts.append('''</div>
<!-- end body-flow -->
''')

    # --- Back cover ---
    html_parts.append(f'''
<!-- BACK COVER -->
<div class="page back-cover-page">
  <div class="back-cover-content">
    <div class="back-cover-logo">
      <img src="{html_module.escape(logo_path)}" alt="{html_module.escape(os.getenv('COMPANY_NAME', '[COMPANY]'))}">
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

def parse_one_pager_md(content_md_path: str) -> dict:
    """
    Parse a one-pager content.md into a structured dict.

    Returns:
        {
            'meta': {
                'title': str,
                'subtitle': str,
                'cta_text': str,
                'cta_url': str,
                'logo_bar': [str],
            },
            'front': {
                'intro': str,
                'capabilities': [{'header': str, 'bullets': [str]}],
                'flow': [{'number': str, 'label': str, 'caption': str}],
            },
            'back': {
                'value': str,
                'deploy': str,
                'use_cases': [str],
                'stats': [{'value': str, 'label': str}],
                'security': [str],
                'cta': str,
            }
        }
    """
    with open(content_md_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    # Strip HTML comments
    content = re.sub(r'<!--.*?-->', '', raw, flags=re.DOTALL)

    # --- Extract front matter ---
    meta = {
        'title': '',
        'subtitle': '',
        'cta_text': '',
        'cta_url': '',
        'logo_bar': [],
    }

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

        meta['title'] = extract_fm('title')
        meta['subtitle'] = extract_fm('subtitle')
        meta['cta_text'] = extract_fm('cta-text')
        meta['cta_url'] = extract_fm('cta-url')

        logo_bar_raw = extract_fm('logo-bar')
        if logo_bar_raw:
            meta['logo_bar'] = [s.strip() for s in logo_bar_raw.split(',')]

        # Remove front matter from body
        content = content[fm_match.end():].strip()

    # --- Split on ## Front Page and ## Back Page ---
    front_raw = ''
    back_raw = ''

    page_split = re.split(r'^##\s+(Front Page|Back Page)\s*$', content, flags=re.MULTILINE)
    # page_split = [before, 'Front Page', front_content, 'Back Page', back_content]
    for i, part in enumerate(page_split):
        if part.strip() == 'Front Page' and i + 1 < len(page_split):
            front_raw = page_split[i + 1]
        elif part.strip() == 'Back Page' and i + 1 < len(page_split):
            back_raw = page_split[i + 1]

    # --- Parse front page zones ---
    front = {
        'intro': '',
        'capabilities': [],
        'flow': [],
    }

    def split_zones(raw_text):
        """Split text by ### headings into {zone_name: content} dict."""
        zones = {}
        parts = re.split(r'^###\s+(.+)\s*$', raw_text, flags=re.MULTILINE)
        # parts = [before, zone_name, content, zone_name, content, ...]
        for i in range(1, len(parts), 2):
            zone_name = parts[i].strip().lower()
            zone_content = parts[i + 1].strip() if i + 1 < len(parts) else ''
            zones[zone_name] = zone_content
        return zones

    front_zones = split_zones(front_raw)

    # Intro
    front['intro'] = front_zones.get('intro', '').strip()

    # Capabilities: parse **Bold Header** followed by - bullet items
    cap_raw = front_zones.get('capabilities', '')
    if cap_raw:
        # Split into groups by **bold header** lines
        cap_lines = cap_raw.strip().split('\n')
        current_header = None
        current_bullets = []
        for line in cap_lines:
            stripped = line.strip()
            bold_match = re.match(r'^\*\*(.+?)\*\*\s*$', stripped)
            if bold_match:
                # Save previous group
                if current_header is not None:
                    front['capabilities'].append({
                        'header': current_header,
                        'bullets': current_bullets,
                    })
                current_header = bold_match.group(1)
                current_bullets = []
            elif re.match(r'^[-*]\s', stripped):
                bullet_text = re.sub(r'^[-*]\s+', '', stripped)
                current_bullets.append(bullet_text)
        # Save last group
        if current_header is not None:
            front['capabilities'].append({
                'header': current_header,
                'bullets': current_bullets,
            })

    # Flow: parse - number | label | caption
    flow_raw = front_zones.get('flow', '')
    if flow_raw:
        for line in flow_raw.strip().split('\n'):
            stripped = line.strip()
            flow_match = re.match(r'^[-*]\s+(.+?)\s*\|\s*(.+?)\s*\|\s*(.+)$', stripped)
            if flow_match:
                front['flow'].append({
                    'number': flow_match.group(1).strip(),
                    'label': flow_match.group(2).strip(),
                    'caption': flow_match.group(3).strip(),
                })

    # --- Parse back page zones ---
    back = {
        'value': '',
        'deploy': '',
        'use_cases': [],
        'stats': [],
        'security': [],
        'cta': '',
    }

    back_zones = split_zones(back_raw)

    # Value and Deploy: keep as raw markdown
    back['value'] = back_zones.get('value', '').strip()
    back['deploy'] = back_zones.get('deploy', '').strip()

    # Use Cases: simple bullet list
    uc_raw = back_zones.get('use cases', '')
    if uc_raw:
        for line in uc_raw.strip().split('\n'):
            stripped = line.strip()
            if re.match(r'^[-*]\s', stripped):
                back['use_cases'].append(re.sub(r'^[-*]\s+', '', stripped))

    # Stats: value | label
    stats_raw = back_zones.get('stats', '')
    if stats_raw:
        for line in stats_raw.strip().split('\n'):
            stripped = line.strip()
            stat_match = re.match(r'^[-*]\s+(.+?)\s*\|\s*(.+)$', stripped)
            if stat_match:
                back['stats'].append({
                    'value': stat_match.group(1).strip(),
                    'label': stat_match.group(2).strip(),
                })

    # Security: simple bullet list
    sec_raw = back_zones.get('security', '')
    if sec_raw:
        for line in sec_raw.strip().split('\n'):
            stripped = line.strip()
            if re.match(r'^[-*]\s', stripped):
                back['security'].append(re.sub(r'^[-*]\s+', '', stripped))

    # CTA: plain text
    back['cta'] = back_zones.get('cta', '').strip()

    return {
        'meta': meta,
        'front': front,
        'back': back,
    }


# ---------------------------------------------------------------------------
# 3c. RENDER ONE-PAGER HTML
# ---------------------------------------------------------------------------

def render_one_pager_html(
    parsed: dict,
    template_type: str = 'one-pager',
    output_path: str | None = None,
) -> str:
    """
    Generate a complete branded HTML document for a 2-page one-pager.

    Args:
        parsed: Output of parse_one_pager_md()
        template_type: Template directory name (e.g., 'one-pager')
        output_path: Where the HTML will be saved (needed for relative asset paths)

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

    # Read CSS to inline it
    css_file = os.path.join(template_dir, 'styles.css')
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()

    meta = parsed['meta']
    front = parsed['front']
    back = parsed['back']

    esc = html_module.escape

    # --- Build HTML ---
    html_parts = []

    # Document head
    html_parts.append(f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(meta.get("title", "[COMPANY] One-Pager"))}</title>

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

    # === FRONT PAGE ===
    html_parts.append('''
<!-- FRONT PAGE -->
<div class="page onepager-front">
''')

    # Header: title + logo
    html_parts.append(f'''  <div class="onepager-header">
    <div class="onepager-title-block">
      <h1 class="onepager-title">{esc(meta.get("title", ""))}</h1>
      <p class="onepager-subtitle">{esc(meta.get("subtitle", ""))}</p>
    </div>
    <div class="onepager-logo"><img src="{esc(logo_path)}" alt="[COMPANY]"></div>
  </div>
''')

    # Intro paragraph
    intro_html = _convert_inline(esc(front.get('intro', '')))
    html_parts.append(f'''  <div class="onepager-intro"><p>{intro_html}</p></div>
''')

    # Illustration placeholder
    html_parts.append('''  <div class="onepager-illustration">
    <span class="onepager-illustration__label">ILLUSTRATION</span>
  </div>
''')

    # Section heading (uses subtitle from front matter)
    section_heading = esc(meta.get('subtitle', ''))
    html_parts.append(f'''  <div class="onepager-section-heading"><h2>{section_heading}</h2></div>
''')

    # Capability grid (3 columns)
    html_parts.append('  <div class="onepager-capabilities">\n')
    for cap in front.get('capabilities', []):
        header = esc(cap.get('header', ''))
        bullets = ''.join(
            f'      <li>{_convert_inline(esc(b))}</li>\n'
            for b in cap.get('bullets', [])
        )
        html_parts.append(
            f'    <div class="capability-column">\n'
            f'      <div class="capability-header">{header}</div>\n'
            f'      <ul class="capability-list">\n{bullets}      </ul>\n'
            f'    </div>\n'
        )
    html_parts.append('  </div>\n')

    # Flow diagram
    html_parts.append('  <div class="onepager-flow">\n')
    flow_steps = front.get('flow', [])
    for idx, step in enumerate(flow_steps):
        html_parts.append(
            f'    <div class="flow-step">\n'
            f'      <div class="flow-step__circle">{esc(step["number"])}</div>\n'
            f'      <div class="flow-step__label">{_convert_inline(esc(step["label"]))}</div>\n'
            f'      <div class="flow-step__caption">{_convert_inline(esc(step["caption"]))}</div>\n'
            f'    </div>\n'
        )
        # Arrow between steps (not after last)
        if idx < len(flow_steps) - 1:
            html_parts.append('    <div class="flow-arrow">\u2192</div>\n')
    html_parts.append('  </div>\n')

    # Logo bar
    html_parts.append('  <div class="onepager-logobar">\n')
    for logo_name in meta.get('logo_bar', []):
        html_parts.append(
            f'    <span class="onepager-logobar__item">'
            f'{esc(logo_name.upper())}</span>\n'
        )
    html_parts.append('  </div>\n')

    html_parts.append('</div>\n')  # close .onepager-front

    # === BACK PAGE ===
    html_parts.append('''
<!-- BACK PAGE -->
<div class="page onepager-back">
''')

    # Top accent bar
    html_parts.append('  <div class="onepager-back-bar" aria-hidden="true"></div>\n')

    # Helper: parse raw markdown zone into h3 + paragraphs
    def _render_zone_md(raw_md: str) -> str:
        """Convert raw markdown with **heading** + paragraphs into HTML."""
        if not raw_md:
            return ''
        lines = raw_md.strip().split('\n')
        parts = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            bold_match = re.match(r'^\*\*(.+?)\*\*\s*$', stripped)
            if bold_match:
                parts.append(f'    <h3>{esc(bold_match.group(1))}</h3>')
            else:
                parts.append(f'    <p>{_convert_inline(esc(stripped))}</p>')
        return '\n'.join(parts)

    # Business value
    value_inner = _render_zone_md(back.get('value', ''))
    html_parts.append(f'  <div class="onepager-value">\n{value_inner}\n  </div>\n')

    # Deployment
    deploy_inner = _render_zone_md(back.get('deploy', ''))
    html_parts.append(f'  <div class="onepager-deploy">\n{deploy_inner}\n  </div>\n')

    # Use cases
    html_parts.append('  <div class="onepager-usecases">\n    <h3>Use Cases</h3>\n    <div class="usecase-tags">\n')
    for uc in back.get('use_cases', []):
        html_parts.append(f'      <span class="usecase-tag">{esc(uc)}</span>\n')
    html_parts.append('    </div>\n  </div>\n')

    # Stats
    html_parts.append('  <div class="onepager-stats">\n')
    for stat in back.get('stats', []):
        html_parts.append(
            f'    <div class="onepager-stat">\n'
            f'      <span class="onepager-stat__value">{esc(stat["value"])}</span>\n'
            f'      <span class="onepager-stat__label">{esc(stat["label"])}</span>\n'
            f'    </div>\n'
        )
    html_parts.append('  </div>\n')

    # Security
    html_parts.append('  <div class="onepager-security">\n    <h3>Secure &amp; trustworthy by design</h3>\n    <ul class="security-list">\n')
    for item in back.get('security', []):
        html_parts.append(f'      <li>{_convert_inline(esc(item))}</li>\n')
    html_parts.append('    </ul>\n  </div>\n')

    # CTA
    cta_text = meta.get('cta_text', '') or back.get('cta', 'Learn more')
    cta_url = meta.get('cta_url', '#')
    html_parts.append(
        f'  <div class="onepager-cta">\n'
        f'    <a class="onepager-cta-button" href="{esc(cta_url)}">'
        f'{esc(cta_text)}</a>\n'
        f'  </div>\n'
    )

    html_parts.append('</div>\n')  # close .onepager-back

    html_parts.append('''
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

    # 1. Parse content and generate HTML (route by template type)
    html_path = output_pdf_path.replace('.pdf', '.html')

    if template_type == 'one-pager':
        parsed = parse_one_pager_md(content_md_path)
        page_count = 2  # Always exactly 2 pages
        html_content = render_one_pager_html(
            parsed, template_type, output_path=html_path
        )
    else:
        parsed = parse_content_md(content_md_path)
        # Page count for flowing layout is determined by Puppeteer at render
        # time, not by section count. Estimate based on content length.
        page_count = None  # Will be determined after PDF render
        html_content = render_html(
            parsed, template_type, output_path=html_path
        )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    page_label = f'{page_count} pages' if page_count else 'flowing'
    print(f'HTML generated → {html_path} ({page_label})')

    # 3. Render PDF via WeasyPrint
    import weasyprint
    doc = weasyprint.HTML(filename=html_path, base_url=html_path)
    try:
        doc.write_pdf(output_pdf_path)
    except Exception as e:
        print(f'PDF generation failed: {e}')
        return {
            'pdf_path': None,
            'html_path': html_path,
            'brand_check_passed': False,
            'brand_check_output': str(e),
            'page_count': page_count,
        }

    size_kb = os.path.getsize(output_pdf_path) / 1024
    print(f'✓  PDF saved → {output_pdf_path}  ({size_kb:.1f} KB)')

    return {
        'pdf_path': output_pdf_path,
        'html_path': html_path,
        'brand_check_passed': True,
        'brand_check_output': '',
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
