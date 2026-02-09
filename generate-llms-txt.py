"""
generate-llms-txt.py

Quarto post-render script that generates llms.txt from rendered
markdown files in the output directory.

Usage in _quarto.yml:
    project:
      post-render:
        - "python generate-llms-txt.py"
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

import yaml

# Quarto sets this env var; fall back to "docs" for manual runs
OUTPUT_DIR = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs"))
SOURCE_DIR = Path(".")

POSTS_OUTPUT_DIR = OUTPUT_DIR / "posts"
POSTS_SOURCE_DIR = SOURCE_DIR / "posts"


# ---------------------------------------------------------------------------
# Site config
# ---------------------------------------------------------------------------

def load_site_config() -> dict:
    """Load site metadata from _quarto.yml."""
    quarto_yml = Path("_quarto.yml")
    if quarto_yml.exists():
        config = yaml.safe_load(quarto_yml.read_text(encoding="utf-8"))
        website = config.get("website", {})
        return {
            "title": website.get("title", ""),
            "description": website.get("description", ""),
            "url": website.get("site-url", "").rstrip("/"),
        }
    return {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_frontmatter_from_source(source_path: Path) -> dict:
    """Extract YAML frontmatter from a .qmd or .md source file."""
    text = source_path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            return {}
    return {}


def extract_frontmatter_from_notebook(nb_path: Path) -> dict:
    """Extract frontmatter from a Jupyter notebook's first cell."""
    try:
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
        first_cell = nb.get("cells", [{}])[0]
        if first_cell.get("cell_type") == "raw":
            raw = "".join(first_cell.get("source", []))
            match = re.match(r"^---\s*\n(.*?)\n---", raw, re.DOTALL)
            if match:
                return yaml.safe_load(match.group(1)) or {}
    except (json.JSONDecodeError, yaml.YAMLError, IndexError, KeyError):
        pass
    return {}


def extract_title_from_md(md_path: Path) -> str:
    """Fallback: extract title from the first H1 in a rendered .md file."""
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return md_path.parent.name


def find_source_file(post_dir_name: str) -> Path | None:
    """Find the source .qmd or .ipynb for a given post directory."""
    source_dir = POSTS_SOURCE_DIR / post_dir_name
    if not source_dir.is_dir():
        return None
    for name in ["index.qmd", "index.ipynb", "index.md"]:
        candidate = source_dir / name
        if candidate.exists():
            return candidate
    for pattern in ["*.qmd", "*.ipynb"]:
        matches = list(source_dir.glob(pattern))
        if matches:
            return matches[0]
    return None


def get_post_metadata(md_path: Path, site_url: str) -> dict:
    """Get metadata for a post from source frontmatter or rendered .md."""
    post_dir_name = md_path.parent.name
    metadata = {}

    source = find_source_file(post_dir_name)
    if source:
        if source.suffix == ".ipynb":
            metadata = extract_frontmatter_from_notebook(source)
        else:
            metadata = extract_frontmatter_from_source(source)

    if "title" not in metadata:
        metadata["title"] = extract_title_from_md(md_path)

    # Extract date from directory name (YYYY-MM-DD-slug pattern)
    date_match = re.match(r"(\d{4}-\d{2}-\d{2})", post_dir_name)
    if date_match and "date" not in metadata:
        metadata["date"] = date_match.group(1)

    relative_path = md_path.relative_to(OUTPUT_DIR)
    metadata["md_url"] = f"{site_url}/{relative_path}"

    return metadata


def parse_date(date_val) -> datetime:
    """Parse various date formats from frontmatter."""
    if isinstance(date_val, datetime):
        return date_val
    if isinstance(date_val, str):
        for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%B %d, %Y", "%Y-%m-%dT%H:%M:%S"]:
            try:
                return datetime.strptime(date_val.strip(), fmt)
            except ValueError:
                continue
    return datetime.min


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    site = load_site_config()
    site_title = site.get("title", "My Site")
    site_description = site.get("description", "")
    site_url = site.get("url", "")

    if not POSTS_OUTPUT_DIR.is_dir():
        print(f"Posts output directory not found: {POSTS_OUTPUT_DIR}")
        return

    md_files = sorted(POSTS_OUTPUT_DIR.glob("*/index.md"))

    if not md_files:
        print("No rendered .md files found in posts directory")
        return

    posts = []
    for md_path in md_files:
        meta = get_post_metadata(md_path, site_url)
        posts.append(meta)

    # Sort by date, newest first
    posts.sort(key=lambda p: parse_date(p.get("date", "")), reverse=True)

    # Build llms.txt
    lines = []
    lines.append(f"# {site_title}")
    lines.append("")
    if site_description:
        lines.append(f"> {site_description}")
        lines.append("")
    lines.append("## Posts")
    lines.append("")

    for post in posts:
        title = post.get("title", "Untitled")
        md_url = post["md_url"]
        description = post.get("subtitle", "") or post.get("description", "")
        if description:
            lines.append(f"- [{title}]({md_url}): {description}")
        else:
            lines.append(f"- [{title}]({md_url})")

    llms_txt_path = OUTPUT_DIR / "llms.txt"
    llms_txt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated {llms_txt_path} ({len(posts)} posts)")


if __name__ == "__main__":
    main()