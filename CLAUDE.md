# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is [matthodges.com](https://matthodges.com), a personal blog and portfolio site built with [Quarto](https://quarto.org/). Posts are authored as `.qmd` files or Jupyter notebooks (`.ipynb`), rendered to HTML and GFM Markdown, and deployed to GitHub Pages via the `docs/` output directory.

## Build Commands

```bash
# Render the full site (outputs to docs/)
quarto render

# Preview with live reload
quarto preview

# Render a single post
quarto render posts/YYYY-MM-DD-slug/index.qmd
```

A post-render hook runs automatically (configured in `_quarto.yml`):
- `generate-llms-txt.py` -- generates `docs/llms.txt` from rendered markdown files for LLM consumption

Canonical URLs are handled natively via `canonical-url: true` in `_quarto.yml`.

## Architecture

- `_quarto.yml` -- site-wide Quarto configuration (metadata, navbar, theme, format options, post-render hooks, inline JS for LLM agent links)
- `index.qmd` -- homepage / about page (uses the `trestles` about template)
- `posts.qmd` -- post listing page (grid layout, sorted by date descending)
- `styles.scss` -- custom SCSS overrides on top of the Cosmo Bootswatch theme
- `posts/` -- blog post source files
- `posts/_metadata.yml` -- shared post metadata (freeze: true, format settings, footer include)
- `posts/post-footer.html` -- HTML footer appended to every post
- `posts/_code-license.qmd` -- BSD license partial included in code-heavy posts
- `docs/` -- rendered output (committed to git, served by GitHub Pages)
- `_freeze/` -- Quarto freeze directory storing cached computation results from notebooks
- `img/` -- site-wide images (photo, favicon SVG, social card)

## Post Conventions

Posts live in `posts/YYYY-MM-DD-slug/` with an `index.qmd` or `index.ipynb` entry point. Each post directory may also contain images and data files.

Frontmatter fields typically used: `author`, `title`, `pagetitle`, `subtitle`, `image`, `date`, and optionally format-specific overrides.

Computation is frozen (`execute: freeze: true` in `posts/_metadata.yml`), so notebook outputs are cached in `_freeze/` and not re-executed on every render.

Each post renders to both HTML and GFM Markdown (configured in `posts/_metadata.yml`).

## Python Environment

A `.venv` exists with Python 3.13 and data science packages (numpy, pandas, matplotlib, scipy, etc.). There is no `requirements.txt`; dependencies are managed inside the venv directly.

## Design System

The site uses an editorial aesthetic with three typefaces loaded from Google Fonts:
- **Inter** -- body text and UI (`$font-family-sans-serif`)
- **Newsreader** -- italic serif used only for the navbar brand
- **DM Mono** -- code, dates, and metadata

Color palette is a gray scale (`$gray-100` through `$gray-900`) with blue (`$link-color: #1D4ED8`) for links and interactive elements, and red (`$accent-red: #B91C1C`) as a subtle structural accent (code block borders, active TOC indicator). The `.color-accent` spans on the about page use the blue to highlight organization/entity names.

All interactive elements (links, navbar, TOC, cards) use `$transition-speed: 0.15s` transitions.

## Render Configuration

`_quarto.yml` explicitly renders `*.qmd` and `*.ipynb` files, and excludes `CLAUDE.md`. Both file types must be included since several posts are Jupyter notebooks.

## Inline JavaScript

Two scripts are embedded in `_quarto.yml` via `header-includes`:
1. **LLM agent link injection** -- appends "Open in ChatGPT" and "Open in Claude" links to the `.quarto-alternate-formats ul` list (labeled "For LLM Agents:")
2. **Mobile format repositioning** -- moves the alternate-formats section under the title block on viewports below 767.98px, restoring on resize

## Deployment

The site is deployed to GitHub Pages. The `CNAME` file maps to `matthodges.com`. The `docs/` directory is the publish source. The `.nojekyll` file disables Jekyll processing on GitHub Pages.
