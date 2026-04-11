"""
fix-sitemap-urls.py

Quarto post-render script that strips trailing "index.html" from sitemap
URLs so they match the canonical URLs (clean directory paths).

Usage in _quarto.yml:
    project:
      post-render:
        - "python fix-sitemap-urls.py"
"""

import os
from pathlib import Path

OUTPUT_DIR = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs"))
SITEMAP = OUTPUT_DIR / "sitemap.xml"


def main():
    if not SITEMAP.exists():
        return

    content = SITEMAP.read_text(encoding="utf-8")
    fixed = content.replace("/index.html</loc>", "/</loc>")

    if fixed != content:
        SITEMAP.write_text(fixed, encoding="utf-8")
        print("Cleaned sitemap URLs: removed index.html suffixes")
    else:
        print("Sitemap URLs already clean")


if __name__ == "__main__":
    main()
