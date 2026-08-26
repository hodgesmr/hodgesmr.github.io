"""
generate-structured-data.py

Quarto post-render script that injects schema.org JSON-LD structured data
and the missing og:type / og:url Open Graph tags into each rendered HTML
page.

Values are read from tags Quarto already emits in the <head> (canonical,
og:title/description/image, author, dcterms.date) or parsed from the
rendered page body (the homepage press list), so the structured data
cannot drift from the page content. The only hand-maintained values are
the PERSON_FACTS block below -- biographical facts that appear nowhere
in machine-readable form.

  - Home page    -> ProfilePage (mainEntity: Person, incl. press
                    coverage as subjectOf) + WebSite  (@graph)
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

import yaml

OUTPUT_DIR = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs"))


def load_site_config() -> dict:
    """Pull site identity from _quarto.yml so nothing is duplicated here.

    - url     <- website.site-url
    - name    <- website.title
    - sameAs  <- the external (http) links in the navbar (LinkedIn, GitHub)
    """
    config = yaml.safe_load(Path("_quarto.yml").read_text(encoding="utf-8"))
    website = config.get("website", {})

    same_as = []
    navbar = website.get("navbar", {}) or {}
    for section in ("left", "right"):
        for item in navbar.get(section, []) or []:
            href = (item or {}).get("href", "")
            if href.startswith("http"):
                same_as.append(href)

    return {
        "url": website.get("site-url", "").rstrip("/"),
        "name": website.get("title", ""),
        "same_as": same_as,
    }


_SITE = load_site_config()
SITE_URL = _SITE["url"]
AUTHOR_NAME = _SITE["name"]
SAME_AS = _SITE["same_as"]

# Biographical facts for the Person entity that exist nowhere in the
# rendered metadata. Everything else (name, url, sameAs, description,
# press coverage) is derived; edit here only when the biography changes.
PERSON_FACTS = {
    "jobTitle": "Political Technologist",
    "disambiguatingDescription": (
        "American political technologist; founder of Ilium Strategies "
        "and former Director of Engineering for Biden for President 2020."
    ),
    "image": f"{SITE_URL}/img/photo.jpg",
    "worksFor": {
        "@type": "Organization",
        "@id": "https://iliumstrategies.com/#organization",
        "name": "Ilium Strategies",
        "url": "https://iliumstrategies.com/",
        "founder": {"@id": f"{SITE_URL}/#person"},
    },
    "alumniOf": {
        "@type": "CollegeOrUniversity",
        "name": "Miami University",
    },
    "knowsAbout": [
        "Political technology",
        "AI strategy",
        "Political strategy",
        "Software engineering",
        "Campaign cybersecurity",
        "Democratic campaign infrastructure",
        "Democratic party politics",
    ],
}

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
        "@id": f"{SITE_URL}/#person",
        "name": AUTHOR_NAME,
        "url": f"{SITE_URL}/",
        "sameAs": SAME_AS,
        **PERSON_FACTS,
    }


MEDIA_SECTION_RE = r'<section id="media-appearances".*?</section>'
MEDIA_ITEM_RE = r'<dt><a href="([^"]+)">(.*?)</a></dt>\s*<dd>\s*(.*?)\s*</dd>'


def strip_tags(fragment: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def collect_press(html_text: str) -> list[dict]:
    """Parse the homepage Media & Appearances list into CreativeWork
    nodes, so the press coverage in the graph always matches the page."""
    section = re.search(MEDIA_SECTION_RE, html_text, re.S)
    if not section:
        return []
    works = []
    for url, title, byline in re.findall(MEDIA_ITEM_RE, section.group(0), re.S):
        work = {
            "@type": "CreativeWork",
            "name": strip_tags(title),
            "url": html.unescape(url),
        }
        m = re.match(r"(.+),\s*(\d{4})$", strip_tags(byline))
        if m:
            work["publisher"] = {"@type": "Organization", "name": m.group(1).strip()}
            work["datePublished"] = m.group(2)
        works.append(work)
    return works


def is_home(canonical: str) -> bool:
    return canonical.rstrip("/") == SITE_URL


def is_post(html_text: str, canonical: str) -> bool:
    return "/posts/" in canonical and re.search(DATE_RE, html_text) is not None


def is_listing(canonical: str) -> bool:
    return canonical.rstrip("/") in (f"{SITE_URL}/posts", f"{SITE_URL}/posts.html")


def collect_posts() -> list[dict]:
    """Gather BlogPosting nodes (newest first) from the rendered post pages,
    for the Blog listing's blogPost array."""
    posts = []
    for path in (OUTPUT_DIR / "posts").glob("*/index.html"):
        text = path.read_text(encoding="utf-8")
        canonical = meta(text, CANONICAL_RE)
        date = meta(text, DATE_RE)
        if not canonical or not date:
            continue
        posts.append(
            {
                "@type": "BlogPosting",
                "@id": f"{canonical}#article",
                "headline": meta(text, OG_TITLE_RE),
                "url": canonical,
                "datePublished": date,
            }
        )
    posts.sort(key=lambda p: p["datePublished"], reverse=True)
    return posts


def build_jsonld(html_text: str, canonical: str) -> dict | None:
    """Build the schema.org node appropriate for this page, or None."""
    title = meta(html_text, OG_TITLE_RE)
    desc = meta(html_text, OG_DESC_RE) or meta(html_text, DESC_RE)
    image = meta(html_text, OG_IMAGE_RE)

    if is_home(canonical):
        person = person_node()
        if desc:
            person["description"] = desc
        press = collect_press(html_text)
        if press:
            person["subjectOf"] = press
        website = {
            "@type": "WebSite",
            "@id": f"{SITE_URL}/#website",
            "name": AUTHOR_NAME,
            "url": f"{SITE_URL}/",
        }
        profile = {
            "@type": "ProfilePage",
            "@id": f"{SITE_URL}/#profilepage",
            "url": f"{SITE_URL}/",
            "isPartOf": {"@id": f"{SITE_URL}/#website"},
            "mainEntity": person,
        }
        return {"@context": "https://schema.org", "@graph": [profile, website]}

    if is_post(html_text, canonical):
        node = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "@id": f"{canonical}#article",
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

    if is_listing(canonical):
        return {
            "@context": "https://schema.org",
            "@type": "Blog",
            "name": title,
            "url": canonical,
            "author": person_node(),
            "blogPost": collect_posts(),
        }

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
