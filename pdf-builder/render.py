"""
WeasyPrint brand test renderer.

Usage:
    python render.py [input.html] [output.pdf]

Defaults to test.html -> test.pdf in this directory.
"""

import sys
import os
from pathlib import Path

import weasyprint

def render(html_path: str, pdf_path: str) -> None:
    html_path = Path(html_path).resolve()
    pdf_path = Path(pdf_path).resolve()

    if not html_path.exists():
        print(f"Error: {html_path} not found")
        sys.exit(1)

    print(f"Rendering {html_path.name} ...")

    # WeasyPrint uses the HTML file's directory as the base URL for
    # resolving relative paths (images, fonts via url()). Passing
    # base_url=html_path means ../assets/Logo.svg resolves correctly.
    doc = weasyprint.HTML(filename=str(html_path), base_url=str(html_path))
    doc.write_pdf(str(pdf_path))

    size_kb = pdf_path.stat().st_size / 1024
    print(f"✓  PDF saved → {pdf_path}  ({size_kb:.1f} KB)")


if __name__ == "__main__":
    here = Path(__file__).parent
    html = sys.argv[1] if len(sys.argv) > 1 else str(here / "test.html")
    pdf  = sys.argv[2] if len(sys.argv) > 2 else str(here / "test.pdf")
    render(html, pdf)
