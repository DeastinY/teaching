# Richard Polzin - Portfolio & Teaching

Personal portfolio and teaching materials website for Richard Polzin, AI Researcher at the Joint Research Center of Computational Biomedicine.

**Live site:** [richardpolzin.com](https://richardpolzin.com)

## Overview

This site combines a personal portfolio showcasing research work with interactive workshop presentations on various topics in AI, HPC, and medical informatics.

## Structure

```
├── index.html              # Main portfolio page
├── assets/                 # Portfolio assets (CSS, JS, images)
├── reveal/                 # Shared Reveal.js library
├── azurellm/               # LLMs at CCLS workshop
├── clusterintro/           # HPC in Research workshop
└── syndata/                # Synthetic Data in Medicine workshop
```

## Workshops

- **[LLMs at CCLS](https://richardpolzin.com/azurellm/)** - Using Azure infrastructure for large language models
- **[HPC in Research](https://richardpolzin.com/clusterintro/)** - Introduction to High Performance Computing
- **[Synthetic Data](https://richardpolzin.com/syndata/)** - Synthetic data generation in healthcare

## Local Development

```bash
# With npm
npm install
npm run dev

# Without npm
python -m http.server 3000
```

Then open http://localhost:3000

## Building

```bash
npm run build
```

Creates minified versions of CSS and JS files for production.

## Deployment

The site is deployed via GitHub Pages from the `gh-pages` branch. Push changes to `gh-pages` to deploy.

## License

Workshop materials are shared for educational purposes. The HPC workshop includes content adapted from [HPC.NRW](https://hpc-wiki.info/hpc/HPC_Wiki) under CC-BY-SA license.
