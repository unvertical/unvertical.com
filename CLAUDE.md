# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Unvertical — a Hugo-based marketing site for a high-performance block storage caching company. Two product lines: Unvertical OpenCAS (open-core caching framework) and Unvertical NVMC — Non-Volatile Memory Cache (early access). Statically hosted on GitHub Pages.

**Naming:** Unvertical is the single brand (the trademark); product names are plain descriptors, not separate trademarks. Use the full `Unvertical <Product>` form in product headings and first mentions; bare `OpenCAS` / `NVMC` is fine in running prose, nav, and section labels. Never reintroduce the old `NVMCC` / "NVM Cache for Compute" naming.

## Build & Development Commands

- **Dev server**: `hugo server -D` (includes draft content)
- **Production build**: `hugo --minify` (output to `public/`)
- **New blog post**: `hugo new blog/my-post-title.md`

No Node.js dependencies — pure Hugo site with vanilla CSS.

## Architecture

- **Single-page marketing site**: The homepage (`layouts/index.html`, ~500 lines) contains all product sections (Hero, About, OpenCAS, NVMC, Why Unvertical, Contact)
- **Base template**: `layouts/_default/baseof.html` provides head/meta, nav partial, footer partial, and OG/Twitter meta tags
- **Partials**: `nav.html` (fixed header with mobile toggle) and `footer.html`
- **Blog**: Scaffolded with `layouts/blog/list.html` and `single.html` but no published posts yet. Archetype at `archetypes/blog.md`
- **CSS**: Single file `static/css/main.css` (~1350 lines) with CSS custom properties for theming (dark theme, `--accent: #4ecdc4` teal, `--accent-secondary: #f7b731` amber)
- **Fonts**: JetBrains Mono (monospace) and Source Serif 4 (serif) via Google Fonts CDN

## Configuration

- `hugo.toml`: Base URL `https://unvertical.com/`, Goldmark with unsafe HTML enabled, Dracula code highlighting, tags taxonomy
- Contact form uses Formspree (form ID configured in `hugo.toml`)
- Menu items configured in `hugo.toml` params

## Deployment

Statically hosted on **GitHub Pages**. `.github/workflows/deploy.yml` builds with Hugo extended and publishes via `actions/deploy-pages` — see that file for the trigger branch and step details. No deployment secrets are needed; it authenticates with the workflow's `GITHUB_TOKEN`.

The custom domain is served from `static/CNAME`, which Hugo copies to the site root on build.
