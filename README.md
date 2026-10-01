# Richard Polzin - Portfolio & Teaching

Personal portfolio and teaching materials website for Richard Polzin, AI Researcher at the Joint Research Center of Computational Biomedicine.

**Live site:** [www.richardpolzin.com](https://www.richardpolzin.com)

## Overview

This site combines a personal portfolio showcasing research work with interactive workshop presentations on various topics in AI, HPC, and medical informatics.

## Structure

```
├── index.html                          # Main portfolio page (self-contained: CSS and JS inline)
├── posts/                              # Blog posts, in markdown - the source
├── blog/                               # ...and the pages built from them, which is what ships
├── tools/build_blog.py                 # The generator that turns one into the other
├── tools/og-card.html                  # The social preview card, as a page...
├── tools/make_og_card.mjs              # ...and the script that renders it to a PNG
├── assets/images/                      # Portrait, and the social preview card
├── assets/css/blog.css                 # Stylesheet for the blog pages
├── reveal/                             # Shared Reveal.js library
├── azurellm/                           # LLMs at CCLS workshop
├── clusterintro/                       # HPC in Research workshop
├── syndata/                            # Synthetic Data in Medicine workshop
├── git/version-control-for-researchers/ # Version Control deck (Slidev source)
└── version-control-for-researchers/    # ...and its build output, which is what ships
```

## Blog

Posts are markdown files in `posts/`, one file per post, with a small frontmatter
block on top:

```markdown
---
title: Why external validation is the only test that counts
date: 2026-09-14
summary: A model that works on the ward it was trained on has proved nothing.
tags: icu, forecasting
draft: true
---

The body, in ordinary markdown.
```

Only `title` and `date` are required. The filename sets the URL, with any leading
date stripped: `2026-09-14-external-validation.md` publishes at
`/blog/external-validation/`. `draft: true` keeps a post out of every build that
is not `--drafts`, so you can leave half-written things lying around safely.

```bash
python3 tools/build_blog.py            # build (uv run tools/build_blog.py also works)
python3 tools/build_blog.py --drafts   # include drafts, to preview locally
python3 tools/build_blog.py --check    # exit 1 if blog/ is out of date; writes nothing
```

One markdown quirk worth knowing: nesting a list takes **four** spaces of
indentation, not two. Two flattens the sub-list without complaining.

The build writes `blog/index.html`, `blog/<slug>/index.html` and an RSS feed at
`blog/feed.xml`, and refreshes the recent-posts list on the homepage between the
`BLOG:START` / `BLOG:END` markers - don't edit that block by hand, a rebuild
overwrites it. Renaming or deleting a post removes its old page.

`posts/` is source and is never published; the generated `blog/` is committed,
because GitHub Pages serves this repo as-is. `deploy.sh` rebuilds the blog before
publishing, so a forgotten rebuild stops the deploy rather than shipping stale
pages.

There is a `draft: true` post in `posts/` that renders every markdown feature the
build understands. Build with `--drafts` to look at it, copy it as a starting
point, and delete it when you no longer want it.

## Social preview card

Links to the site and the blog unfurl with `assets/images/og-card.png`. It is
rendered from `tools/og-card.html`, with the forecast chart lifted out of
`index.html` at render time so the two never drift apart. After changing the
chart, the name or the strapline, re-render and commit the PNG:

```bash
node tools/make_og_card.mjs     # needs the playwright package and a Chromium
```

A post can still set its own card with `image:` in its frontmatter.

## Workshops

- **[Version Control for Researchers](https://www.richardpolzin.com/version-control-for-researchers/)** - Git for research code
- **[Synthetic Data](https://www.richardpolzin.com/syndata/)** - Synthetic data generation in healthcare
- **[HPC in Research](https://www.richardpolzin.com/clusterintro/)** - Introduction to High Performance Computing
- **[LLMs at CCLS](https://www.richardpolzin.com/azurellm/)** - Using Azure infrastructure for large language models

## Local Development

The homepage is a single self-contained file, so any static server will do:

```bash
python -m http.server 3000     # then open http://localhost:3000
```

To work on the Version Control deck with live reload:

```bash
cd git/version-control-for-researchers && pnpm install && pnpm dev
```

## Deployment

GitHub Pages serves this repo from the **`gh-pages`** branch, not `main`
(Settings > Pages: branch `gh-pages`, path `/`). Committing to `main` alone
does not change the live site.

```bash
./deploy.sh              # build the deck, mirror onto gh-pages, push
./deploy.sh --dry-run    # build and show what would be published
```

The script publishes what is *committed*, so commit first - including the
rebuilt `version-control-for-researchers/` and `blog/`, which are checked-in
build artifacts. `git/`, `tools/`, `posts/` and `deploy.sh` are never published.

## License

Workshop materials are shared for educational purposes. The HPC workshop includes content adapted from [HPC.NRW](https://hpc-wiki.info/hpc/HPC_Wiki) under CC-BY-SA license.

## Why `.nojekyll`

GitHub Pages runs Jekyll on a branch unless this file exists. That was
applying the default Slate theme (generating a stray
`/assets/css/style.css`) and, more importantly, silently dropping every
path beginning with an underscore - Vite emits assets like
`_plugin-vue_export-helper-*.js`, which would have broken the deck with no
obvious cause. `.nojekyll` publishes the files exactly as built.
