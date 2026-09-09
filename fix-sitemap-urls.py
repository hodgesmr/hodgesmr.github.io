"""
fix-sitemap-urls.py

Quarto post-render script that strips trailing "index.html" from sitemap
URLs so they match the canonical URLs (clean directory paths), then
collapses duplicate entries.

Duplicates arise because Quarto's incremental sitemap update (single-document
render, `quarto preview`) matches existing entries by the raw output path,
which still ends in index.html. Once this script has cleaned that suffix,
Quarto no longer finds the entry and appends a fresh one on every render.
Collapsing by URL and keeping the newest lastmod keeps the sitemap idempotent.

Usage in _quarto.yml:
    project:
      post-render:
        - "python fix-sitemap-urls.py"
"""

import os
import re
from pathlib import Path

OUTPUT_DIR = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs"))
SITEMAP = OUTPUT_DIR / "sitemap.xml"

URL_BLOCK = re.compile(
    r"\s*<url>\s*<loc>(?P<loc>[^<]*)</loc>\s*<lastmod>(?P<lastmod>[^<]*)</lastmod>\s*</url>"
)


def clean_loc(loc: str) -> str:
    return loc[: -len("index.html")] if loc.endswith("/index.html") else loc


def rebuild(content: str) -> tuple[str, int, int]:
    """Return (new content, suffixes stripped, duplicates removed)."""
    start = content.find("<url>")
    end = content.rfind("</url>")
    if start == -1 or end == -1:
        return content, 0, 0
    end += len("</url>")

    entries: dict[str, str] = {}
    stripped = 0
    duplicates = 0
    for match in URL_BLOCK.finditer(content, start, end):
        loc = clean_loc(match["loc"])
        if loc != match["loc"]:
            stripped += 1
        lastmod = match["lastmod"]
        if loc in entries:
            duplicates += 1
            entries[loc] = max(entries[loc], lastmod)
        else:
            entries[loc] = lastmod

    body = "\n".join(
        f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n  </url>"
        for loc, lastmod in entries.items()
    )
    head = content[:start].rstrip() + "\n"
    tail = "\n" + content[end:].lstrip()
    return head + body + tail, stripped, duplicates


def main():
    if not SITEMAP.exists():
        return

    content = SITEMAP.read_text(encoding="utf-8")
    fixed, stripped, duplicates = rebuild(content)

    if fixed != content:
        SITEMAP.write_text(fixed, encoding="utf-8")
        print(
            f"Cleaned sitemap: removed {stripped} index.html suffixes, "
            f"collapsed {duplicates} duplicate URLs"
        )
    else:
        print("Sitemap already clean")


if __name__ == "__main__":
    main()
