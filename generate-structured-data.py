"""
generate-structured-data.py

Quarto post-render script that injects schema.org JSON-LD structured data
and the missing og:type / og:url Open Graph tags into each rendered HTML
page.

All values are read from tags Quarto already emits in the <head>
(canonical, og:title/description/image, author, dcterms.date), so nothing
is duplicated by hand and the structured data can never drift from the
page metadata.

  - Home page    -> Person + WebSite  (@graph)
  - Blog posts   -> BlogPosting
  - Other pages  -> og:type / og:url only

Usage in _quarto.yml:
    project:
      post-render:
        - "python generate-structured-data.py"
"""

import html
import json
import os
import re
from pathlib import Path

OUTPUT_DIR = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs"))

SITE_URL = "https://matthodges.com"
AUTHOR_NAME = "Matt Hodges"
SAME_AS = [
    "https://www.linkedin.com/in/hodgesmr",
    "https://github.com/hodgesmr",
]

CANONICAL_RE = r'<link\s+rel="canonical"\s+href="([^"]+)"'
OG_TITLE_RE = r'<meta\s+property="og:title"\s+content="([^"]*)"'
OG_DESC_RE = r'<meta\s+property="og:description"\s+content="([^"]*)"'
OG_IMAGE_RE = r'<meta\s+property="og:image"\s+content="([^"]*)"'
DESC_RE = r'<meta\s+name="description"\s+content="([^"]*)"'
AUTHOR_RE = r'<meta\s+name="author"\s+content="([^"]*)"'
DATE_RE = r'<meta\s+name="dcterms\.date"\s+content="([^"]*)"'


def meta(html_text: str, pattern: str) -> str | None:
    """Return an unescaped meta/link value, or None if absent."""
    m = re.search(pattern, html_text)
    return html.unescape(m.group(1)) if m else None


def person_node() -> dict:
    return {
        "@type": "Person",
        "name": AUTHOR_NAME,
        "url": f"{SITE_URL}/",
        "sameAs": SAME_AS,
    }


def is_home(canonical: str) -> bool:
    return canonical.rstrip("/") == SITE_URL


def is_post(html_text: str, canonical: str) -> bool:
    return "/posts/" in canonical and re.search(DATE_RE, html_text) is not None


def build_jsonld(html_text: str, canonical: str) -> dict | None:
    """Build the schema.org node appropriate for this page, or None."""
    title = meta(html_text, OG_TITLE_RE)
    desc = meta(html_text, OG_DESC_RE) or meta(html_text, DESC_RE)
    image = meta(html_text, OG_IMAGE_RE)

    if is_home(canonical):
        person = person_node()
        if desc:
            person["description"] = desc
        website = {
            "@type": "WebSite",
            "name": AUTHOR_NAME,
            "url": f"{SITE_URL}/",
        }
        return {"@context": "https://schema.org", "@graph": [person, website]}

    if is_post(html_text, canonical):
        node = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": title,
            "url": canonical,
            "mainEntityOfPage": canonical,
            "datePublished": meta(html_text, DATE_RE),
            "author": person_node(),
        }
        if desc:
            node["description"] = desc
        if image:
            node["image"] = image
        return node

    return None


def build_og_tags(html_text: str, canonical: str) -> str:
    """Build og:type / og:url (+ article:published_time) tags that are
    not already present."""
    post = is_post(html_text, canonical)
    tags = ""
    if 'property="og:type"' not in html_text:
        tags += f'<meta property="og:type" content="{"article" if post else "website"}">\n'
    if 'property="og:url"' not in html_text:
        tags += f'<meta property="og:url" content="{canonical}">\n'
    if post and 'property="article:published_time"' not in html_text:
        date = meta(html_text, DATE_RE)
        if date:
            tags += f'<meta property="article:published_time" content="{date}">\n'
    return tags


def process(html_text: str) -> str | None:
    """Return the modified HTML, or None if nothing was injected."""
    cm = re.search(CANONICAL_RE, html_text)
    if not cm:
        return None
    canonical = html.unescape(cm.group(1))

    additions = build_og_tags(html_text, canonical)

    # Guard against duplicate JSON-LD on re-runs without a fresh render.
    if "application/ld+json" not in html_text:
        node = build_jsonld(html_text, canonical)
        if node:
            additions += (
                '<script type="application/ld+json">\n'
                + json.dumps(node, indent=2)
                + "\n</script>\n"
            )

    if not additions:
        return None
    return html_text.replace("</head>", additions + "</head>", 1)


def main():
    modified = 0
    for html_path in OUTPUT_DIR.rglob("*.html"):
        content = html_path.read_text(encoding="utf-8")
        result = process(content)
        if result:
            html_path.write_text(result, encoding="utf-8")
            modified += 1
    print(f"Injected structured data / OG tags into {modified} HTML files")


if __name__ == "__main__":
    main()
