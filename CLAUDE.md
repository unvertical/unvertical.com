# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Unvertical — a Hugo-based marketing site for a high-performance block storage caching company. Two product lines: OpenCAS (open-core caching framework) and NVMCC (NVM-based cache, early access). Deploys via FTP to Zenbox hosting.

## Build & Development Commands

- **Dev server**: `hugo server -D` (includes draft content)
- **Production build**: `hugo --minify` (output to `public/`)
- **New blog post**: `hugo new blog/my-post-title.md`

No Node.js dependencies — pure Hugo site with vanilla CSS.

## Architecture

- **Single-page marketing site**: The homepage (`layouts/index.html`, ~500 lines) contains all product sections (Hero, About, OpenCAS, NVMCC, Why Unvertical, Contact)
- **Base template**: `layouts/_default/baseof.html` provides head/meta, nav partial, footer partial, and OG/Twitter meta tags
- **Partials**: `nav.html` (fixed header with mobile toggle) and `footer.html`
- **Blog**: Scaffolded with `layouts/blog/list.html` and `single.html` but no published posts yet. Archetype at `archetypes/blog.md`
- **CSS**: Single file `static/css/main.css` (~1350 lines) with CSS custom properties for theming (dark theme, `--accent: #4ecdc4` teal, `--accent-secondary: #f7b731` amber)
- **Fonts**: JetBrains Mono (monospace) and Source Serif 4 (serif) via Google Fonts CDN

## Configuration

- `hugo.toml`: Base URL `https://unvertical.com/`, Goldmark with unsafe HTML enabled, Dracula code highlighting, tags taxonomy
- Contact form uses Formspree (ID: `mzdjwgrq`)
- Menu items configured in `hugo.toml` params

## Deployment

GitHub Actions (`.github/workflows/deploy.yml`) triggers on push to `main`:
1. Setup Hugo (extended)
2. `hugo --minify`
3. FTP deploy via SamKirkland/FTP-Deploy-Action to Zenbox

Required GitHub secrets: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`, `FTP_SERVER_DIR`.

## Branch Notes

- `main` branch triggers deployment
- Development happens on `master`
