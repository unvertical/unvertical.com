# Unvertical Website

Hugo-based website for [unvertical.com](https://unvertical.com).

## Local Development

```bash
# Install Hugo: https://gohugo.io/installation/
# Then:
hugo server -D
```

Site will be available at `http://localhost:1313/`.

## Writing Blog Posts

```bash
hugo new blog/my-post-title.md
```

This creates `content/blog/my-post-title.md` with front matter. Write in Markdown, set `draft: false` when ready to publish.

### Front matter example

```yaml
---
title: "Why NVM-First Caching Changes the Economics of Disaggregated Storage"
date: 2026-03-20
draft: false
tags: ["nvmcc", "nvm", "caching", "benchmarks"]
description: "We benchmarked NVMCC against DRAM page cache on a 64-node Ceph cluster. Here's what we found."
---
```

## Deployment

Pushes to `main` trigger automatic deployment to Zenbox via GitHub Actions.

### Required GitHub Secrets

Set these in your repo → Settings → Secrets and variables → Actions:

| Secret | Description | Example |
|--------|-------------|---------|
| `FTP_SERVER` | Zenbox FTP hostname | `ftp.zenbox.pl` or your server's FTP address |
| `FTP_USERNAME` | FTP username | (from Zenbox panel) |
| `FTP_PASSWORD` | FTP password | (from Zenbox panel) |
| `FTP_SERVER_DIR` | Remote directory | `/public_html/` or `/domains/unvertical.com/public_html/` |

### Formspree

Replace `YOUR_FORMSPREE_ID` in `hugo.toml` with your actual Formspree form endpoint ID (the part after `https://formspree.io/f/`).

## Project Structure

```
├── archetypes/blog.md          # Template for new blog posts
├── content/
│   ├── _index.md               # Homepage content marker
│   └── blog/
│       ├── _index.md           # Blog list page
│       └── *.md                # Blog posts
├── layouts/
│   ├── _default/baseof.html    # Base template (head, body wrapper)
│   ├── index.html              # Homepage layout (all sections)
│   ├── blog/
│   │   ├── list.html           # Blog listing page
│   │   └── single.html         # Individual blog post
│   └── partials/
│       ├── nav.html            # Navigation bar
│       └── footer.html         # Footer
├── static/
│   ├── css/main.css            # All styles
│   └── images/                 # Static assets (logo, etc.)
├── hugo.toml                   # Site configuration
└── .github/workflows/deploy.yml
```
