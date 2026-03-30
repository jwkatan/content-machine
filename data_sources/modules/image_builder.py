"""
Image Builder — Deterministic branded image generation from templates.

Renders HTML templates with Puppeteer + sharp to produce lossless-compressed,
web-ready PNG/WebP images for landing pages, banners, social media, etc.

Templates are stored in image-builder/templates/{template-id}/ with:
  - template.html: HTML/CSS layout with {{PLACEHOLDER}} tokens
  - template.yaml: Metadata, output specs, input requirements

Usage:
  from data_sources.modules.image_builder import render_image, list_templates

  # List all templates
  templates = list_templates()

  # Render an image
  result = render_image(
      template_id='gated-document',
      inputs={'pdf_path': 'path/to/file.pdf'},
      output_path='output/image.webp'
  )
"""

import os
import json
import subprocess
import yaml
from pathlib import Path

# Directories
_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_MODULE_DIR, '..', '..'))
_IMAGE_BUILDER_DIR = os.path.join(_PROJECT_ROOT, 'image-builder')


def list_templates():
    """
    Return all registered templates.

    Returns:
        list of dicts: [
            {
                'id': 'gated-document',
                'name': 'Gated Document Landing Page',
                'description': '...',
                'use_cases': ['landing-page', 'whitepaper', ...],
                'output': {'width': 1206, 'height': 1562, 'format': 'webp', ...}
            }
        ]
    """
    templates = []
    templates_dir = os.path.join(_IMAGE_BUILDER_DIR, 'templates')

    if not os.path.isdir(templates_dir):
        return []

    for template_id in os.listdir(templates_dir):
        template_path = os.path.join(templates_dir, template_id)
        if not os.path.isdir(template_path):
            continue

        metadata_file = os.path.join(template_path, 'template.yaml')
        if not os.path.exists(metadata_file):
            continue

        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = yaml.safe_load(f)

            templates.append({
                'id': template_id,
                'name': metadata.get('name'),
                'description': metadata.get('description'),
                'use_cases': metadata.get('use_cases', []),
                'output': metadata.get('output', {}),
                'inputs': metadata.get('inputs', {}),
                'figma': metadata.get('figma', {})
            })
        except Exception as e:
            print(f"Warning: Failed to read template {template_id}: {e}")

    return templates


def get_template(template_id):
    """
    Get metadata and path for a template.

    Args:
        template_id: e.g., 'gated-document'

    Returns:
        dict with 'id', 'metadata', 'html_path', 'yaml_path'
    """
    template_dir = os.path.join(_IMAGE_BUILDER_DIR, 'templates', template_id)

    if not os.path.isdir(template_dir):
        raise ValueError(f"Template not found: {template_id}")

    metadata_file = os.path.join(template_dir, 'template.yaml')
    html_file = os.path.join(template_dir, 'template.html')

    if not os.path.exists(metadata_file):
        raise ValueError(f"Template metadata not found: {metadata_file}")
    if not os.path.exists(html_file):
        raise ValueError(f"Template HTML not found: {html_file}")

    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = yaml.safe_load(f)

    return {
        'id': template_id,
        'metadata': metadata,
        'html_path': html_file,
        'yaml_path': metadata_file
    }


def get_landing_page_image_path(asset_slug):
    """
    Get the standard output path for a landing page image.

    Args:
        asset_slug: Asset directory name, e.g., '26Q1-competitive-comparison-claude-cobol'

    Returns:
        str: content/assets/{asset_slug}/images/lp-image-{asset_slug}.webp
    """
    images_dir = os.path.join(_PROJECT_ROOT, 'content', 'assets', asset_slug, 'images')
    os.makedirs(images_dir, exist_ok=True)
    return os.path.join(images_dir, f'lp-image-{asset_slug}.webp')


def render_image(template_id, inputs, output_path=None, asset_slug=None):
    """
    Render an image from a template.

    Args:
        template_id: e.g., 'gated-document'
        inputs: dict with input values, e.g., {'pdf_path': '...'}
        output_path: where to save the rendered image (or use asset_slug for auto-path)
        asset_slug: asset directory name for auto-path generation (e.g., '26Q1-...')

    Returns:
        dict: {
            'success': bool,
            'path': output_path,
            'size': file_size_bytes,
            'format': 'webp' or 'png',
            'error': str (if success=False)
        }
    """
    try:
        # Generate output path from asset_slug if not provided
        if asset_slug and not output_path:
            output_path = get_landing_page_image_path(asset_slug)

        if not output_path:
            return {
                'success': False,
                'error': 'Either output_path or asset_slug must be provided'
            }

        template = get_template(template_id)
        html_path = template['html_path']

        # Resolve paths to absolute
        output_path = os.path.abspath(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Build command for Node.js renderer
        cmd = [
            'node',
            os.path.join(_IMAGE_BUILDER_DIR, 'render.js'),
            html_path,
            output_path
        ]

        # Add PDF path if required and provided
        if template['metadata'].get('inputs', {}).get('pdf_first_page') and inputs.get('pdf_path'):
            pdf_path = os.path.abspath(inputs['pdf_path'])
            cmd.extend(['--pdf', pdf_path])

        # Add format if specified
        output_format = template['metadata'].get('output', {}).get('format', 'webp')
        cmd.extend(['--format', output_format])

        # Run renderer
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=_IMAGE_BUILDER_DIR,
            timeout=120
        )

        if result.returncode != 0:
            return {
                'success': False,
                'error': f"Renderer failed: {result.stderr}"
            }

        # Parse output
        try:
            render_result = json.loads(result.stdout)
            if render_result.get('success'):
                return {
                    'success': True,
                    'path': output_path,
                    'size': render_result.get('size'),
                    'format': render_result.get('format', 'webp')
                }
            else:
                return {
                    'success': False,
                    'error': render_result.get('error', 'Unknown error')
                }
        except json.JSONDecodeError:
            return {
                'success': False,
                'error': f"Invalid renderer output: {result.stdout}"
            }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def register_template(figma_file, figma_node, template_id, metadata, html_content):
    """
    Register a new template (for future use — adds a template to the registry).

    Args:
        figma_file: Figma file key
        figma_node: Figma node ID
        template_id: unique identifier
        metadata: dict with template metadata
        html_content: HTML template string

    Returns:
        dict: {'success': bool, 'path': template_dir, 'error': str}
    """
    try:
        template_dir = os.path.join(_IMAGE_BUILDER_DIR, 'templates', template_id)

        # Check if already exists
        if os.path.exists(template_dir):
            return {'success': False, 'error': f'Template already exists: {template_id}'}

        # Create directory
        os.makedirs(template_dir, exist_ok=True)

        # Write HTML
        html_path = os.path.join(template_dir, 'template.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Write YAML metadata
        metadata['figma'] = {
            'file': figma_file,
            'node': figma_node,
            'last_synced': __import__('datetime').datetime.now().strftime('%Y-%m-%d')
        }

        yaml_path = os.path.join(template_dir, 'template.yaml')
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(metadata, f, default_flow_style=False)

        return {
            'success': True,
            'path': template_dir,
            'files': {
                'html': html_path,
                'yaml': yaml_path
            }
        }

    except Exception as e:
        return {'success': False, 'error': str(e)}


# CLI entry point
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('Usage: python image_builder.py <command> [args]')
        print('  list - List all templates')
        print('  render <template_id> <output_path> [--pdf <pdf_path>] - Render image')
        sys.exit(1)

    command = sys.argv[1]

    if command == 'list':
        templates = list_templates()
        print(json.dumps(templates, indent=2))

    elif command == 'render':
        if len(sys.argv) < 4:
            print('Usage: python image_builder.py render <template_id> <output_path> [--pdf <pdf_path>]')
            sys.exit(1)

        template_id = sys.argv[2]
        output_path = sys.argv[3]

        # Parse optional PDF path
        pdf_path = None
        if '--pdf' in sys.argv:
            pdf_idx = sys.argv.index('--pdf')
            if pdf_idx + 1 < len(sys.argv):
                pdf_path = sys.argv[pdf_idx + 1]

        inputs = {'pdf_path': pdf_path} if pdf_path else {}
        result = render_image(template_id, inputs, output_path)
        print(json.dumps(result, indent=2))

    else:
        print(f'Unknown command: {command}')
        sys.exit(1)
