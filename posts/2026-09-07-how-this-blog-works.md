---
title: How this blog works
date: 2026-09-07
summary: A template and a rendering test in one — every markdown feature the build understands, on a page you can look at before you delete it.
tags: meta, tooling
draft: true
---

This post is marked `draft: true`, so it never reaches the live site. Build with
`--drafts` to see it, copy it as the starting point for a real post, and delete it
when you've stopped needing it.

## Adding a post

Drop a markdown file in `posts/`. The name sets the slug, and a leading date is
stripped: `2026-09-14-external-validation.md` publishes at `/blog/external-validation/`.
Then rebuild:

```bash
python3 tools/build_blog.py     # or: uv run tools/build_blog.py
python3 -m http.server 3000     # then open localhost:3000/blog/
```

Commit the markdown **and** the regenerated files under `blog/`, then run `./deploy.sh`
as usual. The generated pages are checked in on purpose — GitHub Pages serves this repo
as-is, so anything not committed does not exist as far as the live site is concerned.

### The frontmatter

Only `title` and `date` are required; the rest have sensible defaults.

| Key | What it does |
| --- | --- |
| `title` | The headline, the `<title>`, and the link text everywhere |
| `date` | `YYYY-MM-DD`. Sorts the archive and stamps the feed |
| `summary` | The standfirst, the listing blurb, the meta description. Falls back to the first paragraph |
| `tags` | Comma-separated. Shown under the title and in the feed |
| `draft` | `true` keeps it out of every build that isn't `--drafts` |
| `slug` | Override the filename-derived URL |
| `image` | Override the social preview card image |

Wrap a value in quotes if it contains a colon: `title: "Validation: the only test that counts"`.

## What the markdown gets you

The usual inline things work — **bold**, *italic*, `inline code`, [links](https://www.richardpolzin.com),
and footnotes[^1] — plus a few extras worth knowing about.

[^1]: Footnotes collect themselves at the bottom of the post, with a link back to where you were.

Lists, nested as deep as you like:

- Fenced code blocks, with syntax colouring tuned to this palette
- Tables, which scroll sideways on a phone rather than squashing the page
- Blockquotes, footnotes, horizontal rules
    - and sub-lists — indent these by **four** spaces, which is what
      python-markdown wants; two silently flattens them

Quotations get the accent rule:

> A model that performs well on the ward it was trained on has demonstrated
> that the ward is consistent with itself. That is all.

Code blocks take a language tag:

```python
def horizon_windows(series, hours=72, stride=6):
    """Slice a patient's record into the windows the model forecasts from."""
    for start in range(0, len(series) - hours, stride):
        yield series[start:start + hours]
```

```bash
#!/usr/bin/env bash
#SBATCH --job-name=ards-forecast
#SBATCH --time=04:00:00
#SBATCH --gres=gpu:1

srun python train.py --horizon 72 --seed "$SLURM_ARRAY_TASK_ID"
```

Leave the tag off and the block renders plainly, which is what you want for a
terminal transcript or a chunk of log output:

```
2026-09-07 10:14:02  fold 3/5  auroc 0.871  auprc 0.412
2026-09-07 10:19:47  fold 4/5  auroc 0.864  auprc 0.398
```

---

Headings from `##` down get a link anchor that appears on hover, so you can point
someone at one paragraph instead of the whole post. Images work the ordinary way:

![The forecast fan on the homepage](/assets/images/coffee-stain.png)

And that is the whole system. No front-end framework, no content model, no admin
panel — a folder of markdown and a script that turns it into HTML.
