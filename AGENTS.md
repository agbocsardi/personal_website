# AGENTS.md — Personal Website

Quarto website for agbocsardi.com — personal portfolio with blog, research, and photography.

## How Quarto Websites Work

A Quarto website is a collection of `.qmd` (Quarto Markdown) files rendered to static HTML. The site is configured through `_quarto.yml`, which controls layout, navigation, theme, and build behavior.

**Docs:** https://quarto.org/docs/websites/

**Key concepts:**
- `.qmd` files are Markdown with YAML frontmatter (metadata at the top between `---` delimiters)
- `_quarto.yml` defines the site structure, navbar, sidebar, theme, and global settings
- `quarto render` builds everything into `_site/` (the deployable output)
- `quarto preview` runs a live-reload dev server for editing
- Files prefixed with `_` or `.` are ignored by the renderer
- `AGENTS.md` is explicitly excluded from rendering by Quarto
- Listings (like the blog) auto-discover posts from a directory — no manual registration needed
- Links between pages use source files: `[about](my-story.qmd)` not `.html`

## Commands

```bash
quarto preview        # Live reload server (localhost)
quarto render         # Build site to _site/
quarto render blog.qmd  # Render a single file
```

Always `quarto render` locally to verify before pushing — preview doesn't catch all global config changes.

## Project Structure

```
_quarto.yml           # Site config (structure, theme, navbar, sidebar)
index.qmd             # Homepage
blog.qmd              # Blog listing (auto-discovers posts/)
research.qmd          # Research page
photography.qmd       # Photography page
my-story.qmd          # About/bio page
coffee.qmd            # (commented out in sidebar)
posts/                # Blog posts, each in its own subdirectory
  _metadata.yml       # Shared metadata for all posts
  <post-name>/
    index.qmd         # Post content
    *.png, *.jpg      # Post images
resources/            # Theme files, logos, profile pic, SCSS
  style/styles.css    # Custom CSS
  everforest-*.scss   # Light/dark theme
_site/                # Built output (gitignored, don't edit)
_freeze/              # Quarto cache (gitignored)
deploy.sh             # Deployment script
```

## YAML Templates

### Blog Post (new post)

Create `posts/<post-name>/index.qmd`:

```yaml
---
title: "Post Title"
description: "Short description for listing cards and SEO."
date: "YYYY-MM-DD"
date-modified: "YYYY-MM-DD"   # optional, update when editing

categories:
  - tag1
  - tag2

format:
  html:
    code-overflow: wrap        # optional: wrap long code lines

image: preview.png             # optional: shown in listing grid
---
```

Blog posts are auto-discovered by `blog.qmd`'s listing config — no need to register them manually.

### Standalone Page

```yaml
---
title: "Page Title"
description: "Brief description."
---
```

### Page with Custom Layout

```yaml
---
title: "Page Title"
page-layout: full       # full-width, no sidebar
format:
  html:
    toc: true            # table of contents
    code-overflow: wrap
---
```

### Draft Post

Same as a blog post, but with `draft: true`. Drafts are excluded from the live site — only visible when previewing with `--drafts`.

```yaml
---
title: "Half-baked idea about X"
description: "TODO."
date: "YYYY-MM-DD"
draft: true

categories:
  - idea

format:
  html:
    code-overflow: wrap
---
```

**Draft workflow:**
- Throw ideas up with `draft: true` — they stay out of the deployed site
- Preview drafts locally: `quarto preview --drafts`
- Ready to publish → remove `draft: true` (or set to `false`)
- Only non-draft posts appear on the live site

### Shared Post Metadata

`posts/_metadata.yml` applies to all posts in the directory. Currently contains shared defaults — check it before adding per-post overrides.

## Current Site Config

- **Theme:** Everforest light/dark (SCSS in `resources/`)
- **Fonts:** Roboto Slab (main), Roboto Mono (code) — loaded via Google Fonts
- **Sidebar:** floating style, search enabled
- **Draft mode:** `unlinked` — posts exist but aren't linked in navigation until ready
- **Listing:** blog uses grid layout, sorted by date descending, shows categories

## Adding a Post (Step by Step)

1. `mkdir posts/<post-name>`
2. Create `posts/<post-name>/index.qmd` with frontmatter (see template above)
3. Write content in Markdown below the frontmatter
4. Add images to the post directory or `resources/`
5. Preview: `quarto preview` — check localhost
6. The blog listing auto-picks it up from `posts/`

## Deployment

Push to `main` — GitHub Actions handles the rest automatically.

**What happens on push:**
1. GitHub Action checks out the repo
2. Sets up Quarto
3. Renders the site to HTML
4. Deploys `_site/` via FTP to `public_html/` on the hosting server

FTP credentials are stored as GitHub secrets (`FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`).

No manual steps needed — just commit and push to `main`.

## Obsidian Sync

This vault is synced to phone via `ob-sync-personal-website.service` (systemd user service). Edits on phone sync back to homelab automatically.

**Sync excludes:** `.git`, `.github`, `_freeze`, `_site`
**File types:** image, audio, video, pdf, unsupported (for .qmd)

## Conventions

- Don't edit `_quarto.yml` unless changing site structure or theme
- Don't edit `_freeze/` or `_site/` — build artifacts
- Use kebab-case for post directory names
- Images: either in the post directory or shared `resources/`
- Quarto ignores `_` and `.` prefixed files/dirs
- Cross-link pages with source files: `[link text](page.qmd)`
- YAML date format: `"YYYY-MM-DD"` (quoted)
