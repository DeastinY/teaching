---
title: A sample post, for checking the layout
date: 2026-09-05
summary: Not a real post — a stand-in with enough headings, code, tables and quotations in it to see whether the blog reads well before there is anything worth reading.
tags: sample, delete me
---

This post exists so there is something on the page. Delete `posts/2026-09-05-sample-post.md`
once you have looked at it and the archive goes quiet again.

Everything below is here to occupy the layout the way real writing would: a few
paragraphs of ordinary prose, long enough to see the measure and the line height
doing their job, broken up by the things a technical post tends to need.

## A heading, and the prose under it

The column is set to 68 characters, which is a little wider than the homepage's
card copy and about right for sustained reading. Hover a heading and an anchor
appears to its left, so a paragraph can be linked to directly rather than
gestured at.

Inline things behave: **bold**, *italic*, `inline code`, and
[a link](https://www.richardpolzin.com/) that underlines by default and drops the
underline on hover, which is the opposite of the usual convention and reads
better against warm paper.

### A sub-heading

Lists sit close under their introduction:

- Something observed
- Something measured
- Something that turned out to be a logging bug
    - as these things often do

Numbered, when order matters:

1. Fit on the development cohort
2. Freeze everything
3. Only then look at the held-out site

> Withholding the test set is easy. Withholding it from yourself, over eighteen
> months, while a reviewer asks why the numbers are not better — that is the part
> nobody writes a method section about.

## Code

A labelled block gets syntax colours tuned to this palette rather than a stock
theme, so it reads as part of the page:

```python
def windows(series, hours=72, stride=6):
    """Slice a record into the windows the model forecasts from."""
    for start in range(0, len(series) - hours, stride):
        yield series[start:start + hours]
```

```bash
#!/usr/bin/env bash
#SBATCH --job-name=sample
#SBATCH --time=00:30:00

srun python train.py --seed "$SLURM_ARRAY_TASK_ID"
```

Leave the language off and the block stays plain, which is what you want for a
log or a terminal transcript:

```
2026-09-05 10:14:02  fold 3/5  auroc 0.871  auprc 0.412
2026-09-05 10:19:47  fold 4/5  auroc 0.864  auprc 0.398
```

## A table

Wide tables scroll inside their own container rather than pushing the page
sideways on a phone.

| Cohort | Patients | AUROC | Notes |
| --- | --- | --- | --- |
| Development | 4,182 | 0.871 | Single centre, five-fold CV |
| Internal held-out | 1,044 | 0.858 | Same centre, later admissions |
| External site A | 913 | 0.792 | Different ventilator protocol |
| External site B | 671 | 0.744 | Sparser labs, more imputation[^1] |

[^1]: Footnotes collect at the foot of the post with a link back to where you were reading.

---

A horizontal rule marks a break in thought without needing a heading. After it,
one more paragraph, so the article footer is not sitting immediately under a
line, and the whole thing ends the way a real post would — with something a
little quieter than it started.
