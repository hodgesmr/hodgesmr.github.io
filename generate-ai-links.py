"""
generate-ai-links.py

Quarto post-render script that injects static ChatGPT and Claude links
into the alternate-formats section of each rendered HTML page, and
inserts a mobile-only duplicate after the title block so the links
appear near the top on small screens without JavaScript.

Usage in _quarto.yml:
    project:
      post-render:
        - "python generate-ai-links.py"
"""

import os
import re
from pathlib import Path
from urllib.parse import quote

OUTPUT_DIR = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs"))

CANONICAL_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"')

# Match the </ul> that closes the alternate-formats list.
# Quarto renders: <div class="quarto-alternate-formats"><h2>…</h2><ul>…</ul></div>
# We insert new <li> items right before the closing </ul>.
CLOSE_UL_RE = re.compile(
    r'(<div\s+class="quarto-alternate-formats">[^<]*<h2>[^<]*</h2>\s*<ul>.*?)(</ul>)',
    re.DOTALL,
)

# Match the closing </header> of the title block. The first </header>
# after id="title-block-header" is the correct one (headers don't nest).
# This replicates where the old JS inserted:
#   titleBlock.insertAdjacentElement('afterend', formats)
TITLE_BLOCK_RE = re.compile(
    r'id="title-block-header".*?(</header>)',
    re.DOTALL,
)


def build_links_html(canonical_url: str) -> str:
    prompt = quote(f"I'd like to discuss the content from {canonical_url}")
    chatgpt_href = f"https://chatgpt.com/?q={prompt}"
    claude_href = f"https://claude.ai/new?q={prompt}"
    return (
        f'<li><a href="{chatgpt_href}" target="_blank" rel="noopener noreferrer">'
        f'<i class="bi bi-openai"></i>Open in ChatGPT</a></li>'
        f'<li><a href="{claude_href}" target="_blank" rel="noopener noreferrer">'
        f'<i class="bi bi-claude"></i>Open in Claude</a></li>'
    )


def build_mobile_block(links_html: str) -> str:
    """Build a standalone mobile-only alternate-formats block."""
    return (
        '<div class="quarto-alternate-formats quarto-alternate-formats-mobile">'
        '<ul>'
        '<li><a href="index.md"><i class="bi bi-file-code"></i>Markdown</a></li>'
        f'{links_html}</ul></div>'
    )


def inject_links(html: str) -> str | None:
    """Inject AI links into the alternate-formats list and add a mobile duplicate."""
    canonical_match = CANONICAL_RE.search(html)
    if not canonical_match:
        return None

    canonical_url = canonical_match.group(1)
    links_html = build_links_html(canonical_url)

    # 1. Inject links into the sidebar alternate-formats
    m = CLOSE_UL_RE.search(html)
    if not m:
        return None
    html = html[: m.end(1)] + links_html + html[m.start(2) :]

    # 2. Insert a mobile-only duplicate right after the title block </header>,
    #    matching where the old JS placed it via insertAdjacentElement('afterend')
    mobile_block = build_mobile_block(links_html)
    tb = TITLE_BLOCK_RE.search(html)
    if tb:
        insert_pos = tb.end(1)
        html = html[:insert_pos] + mobile_block + html[insert_pos:]

    return html


def main():
    html_files = list(OUTPUT_DIR.rglob("*.html"))
    modified = 0

    for html_path in html_files:
        content = html_path.read_text(encoding="utf-8")

        if "quarto-alternate-formats" not in content:
            continue

        result = inject_links(content)
        if result:
            html_path.write_text(result, encoding="utf-8")
            modified += 1

    print(f"Injected AI links into {modified} HTML files")


if __name__ == "__main__":
    main()
