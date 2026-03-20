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
tags: ["nvmc", "nvm", "caching", "benchmarks"]
description: "We benchmarked NVMC against DRAM page cache on a 64-node Ceph cluster. Here's what we found."
---
```

## Deployment

Pushes to `master` trigger an automatic build and deploy to **GitHub Pages** via
GitHub Actions (`.github/workflows/deploy.yml`).

### One-time setup

1. In your repo → **Settings → Pages**, set **Source** to **GitHub Actions**.
2. The custom domain is served via the `static/CNAME` file (`unvertical.com`),
   which Hugo copies to the site root on build. Point your domain's DNS at
   GitHub Pages (`A`/`AAAA` records to GitHub's IPs, or a `CNAME` to
   `<user>.github.io`), then enable **Enforce HTTPS** in Settings → Pages.

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
