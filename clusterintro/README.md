# Getting Started with HPC in Research

Reveal.js presentation introducing High Performance Computing to researchers.

**Live:** [richardpolzin.com/clusterintro](https://richardpolzin.com/clusterintro/)

## Running locally

The presentation requires a local web server (`file://` won't load assets correctly).

```bash
# From the repo root
./serve.sh          # serves on port 3000
./serve.sh 8080     # custom port
```

Then open **http://localhost:3000/clusterintro/**

## Navigation

| Key | Action |
|---|---|
| `→` / `Space` | Next slide |
| `←` | Previous slide |
| `↓` / `↑` | Navigate vertical (sub) slides |
| `Esc` | Overview mode — see all slides at once |
| `F` | Fullscreen |
| `S` | Speaker notes view |
| `B` | Blackout screen |

Slides with **fragments** (bullet points that appear on click) advance with `Space` or `→`.

Code blocks with **step highlighting** also advance on click — lines are highlighted one group at a time.

## Content

1. **Introduction** — What is HPC, RWTH CLAIX cluster, access, file systems, SSH setup
2. **Linux Basics for HPC** — Command line, filesystem, files, text tools, permissions, vim, scripting, environment, SSH
3. **SLURM Job Manager** — Job scripts, submission, monitoring
4. **Compute Time Application** — NHR tiers, core hours, application process

## Attribution

Linux Basics section adapted from [HPC.NRW Competency Network](https://hpc-wiki.info/hpc/HPC_Wiki) under CC-BY-SA.
