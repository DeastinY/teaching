# Richard Polzin - Portfolio & Teaching

Personal portfolio and teaching materials website for Richard Polzin, AI Researcher at the Joint Research Center of Computational Biomedicine.

**Live site:** [www.richardpolzin.com](https://www.richardpolzin.com)

## Overview

This site combines a personal portfolio showcasing research work with interactive workshop presentations on various topics in AI, HPC, and medical informatics.

## Structure

```
├── index.html                          # Main portfolio page (self-contained: CSS and JS inline)
├── assets/images/                      # The two images the homepage uses
├── reveal/                             # Shared Reveal.js library
├── azurellm/                           # LLMs at CCLS workshop
├── clusterintro/                       # HPC in Research workshop
├── syndata/                            # Synthetic Data in Medicine workshop
├── git/version-control-for-researchers/ # Version Control deck (Slidev source)
└── version-control-for-researchers/    # ...and its build output, which is what ships
```

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
rebuilt `version-control-for-researchers/`, which is a checked-in build
artifact. `git/`, `tools/` and `deploy.sh` are never published.

## License

Workshop materials are shared for educational purposes. The HPC workshop includes content adapted from [HPC.NRW](https://hpc-wiki.info/hpc/HPC_Wiki) under CC-BY-SA license.

## Why `.nojekyll`

GitHub Pages runs Jekyll on a branch unless this file exists. That was
applying the default Slate theme (generating a stray
`/assets/css/style.css`) and, more importantly, silently dropping every
path beginning with an underscore - Vite emits assets like
`_plugin-vue_export-helper-*.js`, which would have broken the deck with no
obvious cause. `.nojekyll` publishes the files exactly as built.
