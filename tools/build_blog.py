#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown>=3.5", "pygments>=2.17"]
# ///
"""Build the blog from the markdown in posts/.

One post is one file in posts/. Everything the site needs about it lives in a
frontmatter block at the top:

    ---
    title: Why external validation is the only test that counts
    date: 2026-09-14
    summary: A model that works on the ward it was trained on has proved nothing.
    tags: icu, forecasting
    draft: true
    ---

    The body, in ordinary markdown.

Only `title` and `date` are required. The slug comes from the filename with any
leading date stripped (2026-09-14-external-validation.md -> external-validation),
or from an explicit `slug:` if you would rather choose it yourself.

    python3 tools/build_blog.py            # or: uv run tools/build_blog.py
    python3 tools/build_blog.py --drafts   # include drafts, to preview locally
    python3 tools/build_blog.py --check    # fail if the output is out of date

Writes blog/index.html, blog/<slug>/index.html and blog/feed.xml, and refreshes
the short list of recent posts on the homepage between the BLOG:START and
BLOG:END markers. Generated files are checked in, because GitHub Pages serves
this repo as-is — see deploy.sh. This script itself lives in tools/ and never
ships.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import shutil
import sys
import unicodedata
import xml.sax.saxutils as sx
from dataclasses import dataclass, field
from email.utils import format_datetime
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "posts"
OUT = ROOT / "blog"
INDEX = ROOT / "index.html"

SITE = "https://www.richardpolzin.com"
AUTHOR = "Richard Polzin"
EMAIL = "richard.polzin@posteo.de"
BLOG_TITLE = "Writing — Richard Polzin"
BLOG_TAGLINE = "Notes on machine learning in medicine, research computing, and the parts of the work that don’t fit in a paper."
DEFAULT_IMAGE = f"{SITE}/assets/images/my-avatar.png"
HOMEPAGE_POSTS = 4          # how many appear on the homepage
WORDS_PER_MINUTE = 220

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;'
    '9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'
)


# --------------------------------------------------------------------------- #
# reading posts
# --------------------------------------------------------------------------- #

@dataclass
class Post:
    slug: str
    title: str
    date: dt.date
    summary: str
    tags: list[str]
    draft: bool
    image: str
    body: str
    words: int
    source: Path
    toc: str = ""
    prev: "Post | None" = field(default=None, repr=False)
    next: "Post | None" = field(default=None, repr=False)

    @property
    def url(self) -> str:
        return f"/blog/{self.slug}/"

    @property
    def abs_url(self) -> str:
        return f"{SITE}{self.url}"

    @property
    def long_date(self) -> str:
        return f"{self.date.day} {self.date:%B} {self.date.year}"

    @property
    def short_date(self) -> str:
        return f"{self.date:%b} {self.date.year}"

    @property
    def minutes(self) -> int:
        return max(1, round(self.words / WORDS_PER_MINUTE))


FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
LEADING_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}[-_]")
TRUTHY = {"true", "yes", "1", "on"}


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s_-]+", "-", text) or "post"


def parse_frontmatter(raw: str, source: Path) -> tuple[dict[str, str], str]:
    m = FRONTMATTER.match(raw)
    if not m:
        die(f"{source.name}: no frontmatter block. The file must start with a line of ---.")
    meta: dict[str, str] = {}
    for n, line in enumerate(m.group(1).splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            die(f"{source.name}:{n}: expected 'key: value', got {line.strip()!r}")
        key, _, value = line.partition(":")
        value = value.strip()
        # tolerate quoted values, which you want for a title containing a colon
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        meta[key.strip().lower()] = value
    return meta, raw[m.end():]


def make_renderer() -> markdown.Markdown:
    return markdown.Markdown(
        extensions=["extra", "codehilite", "sane_lists", "smarty", "toc"],
        extension_configs={
            # guess_lang off: an unlabelled block is prose or a shell transcript
            # far more often than it is any language Pygments would pick.
            "codehilite": {"guess_lang": False, "linenums": False},
            "toc": {"permalink": "#", "permalink_title": "Link to this section"},
            "smarty": {"smart_dashes": True, "smart_quotes": True, "smart_ellipses": True},
        },
    )


def read_post(path: Path, md: markdown.Markdown) -> Post:
    meta, body_md = parse_frontmatter(path.read_text(encoding="utf-8"), path)

    for required in ("title", "date"):
        if not meta.get(required):
            die(f"{path.name}: frontmatter is missing '{required}'.")

    try:
        date = dt.date.fromisoformat(meta["date"])
    except ValueError:
        die(f"{path.name}: date {meta['date']!r} is not a YYYY-MM-DD date.")

    slug = meta.get("slug") or slugify(LEADING_DATE.sub("", path.stem))

    md.reset()
    body = md.convert(body_md)
    # python-markdown emits a bare <table>; it needs a scroll container so a wide
    # one cannot push the whole page sideways on a phone
    body = re.sub(r"<table>", '<div class="table-wrap"><table>', body)
    body = re.sub(r"</table>", "</table></div>", body)

    summary = meta.get("summary") or first_paragraph(body)

    return Post(
        slug=slug,
        title=meta["title"],
        date=date,
        summary=summary,
        tags=[t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
        draft=meta.get("draft", "").lower() in TRUTHY,
        image=meta.get("image") or DEFAULT_IMAGE,
        body=body,
        words=len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", body))),
        source=path,
        toc=getattr(md, "toc", ""),
    )


def first_paragraph(body_html: str) -> str:
    m = re.search(r"<p>(.*?)</p>", body_html, re.S)
    if not m:
        return ""
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
    return text if len(text) <= 220 else text[:217].rsplit(" ", 1)[0] + "…"


def load_posts(include_drafts: bool) -> list[Post]:
    if not POSTS.is_dir():
        return []
    md = make_renderer()
    posts = [read_post(p, md) for p in sorted(POSTS.glob("*.md"))]

    seen: dict[str, Path] = {}
    for post in posts:
        if post.slug in seen:
            die(f"{post.source.name}: slug {post.slug!r} is already used by {seen[post.slug].name}.")
        seen[post.slug] = post.source

    posts = [p for p in posts if include_drafts or not p.draft]
    posts.sort(key=lambda p: (p.date, p.slug), reverse=True)
    for i, post in enumerate(posts):
        post.next = posts[i - 1] if i > 0 else None          # newer
        post.prev = posts[i + 1] if i + 1 < len(posts) else None  # older
    return posts


# --------------------------------------------------------------------------- #
# rendering
# --------------------------------------------------------------------------- #

def e(text: str) -> str:
    """Escape for an attribute value."""
    return html.escape(text, quote=True)


def t(text: str) -> str:
    """Escape for element text, where a quote or apostrophe is just itself."""
    return html.escape(text, quote=False)


def head(*, title: str, description: str, url: str, image: str,
         css_prefix: str, post: Post | None = None) -> str:
    kind = "article" if post else "website"
    parts = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{e(title)}</title>",
        f'<meta name="description" content="{e(description)}">',
        f'<meta name="author" content="{AUTHOR}">',
        f'<link rel="canonical" href="{e(url)}">',
        f'<link rel="icon" href="{css_prefix}assets/favicon.svg" type="image/svg+xml">',
        '<meta name="theme-color" content="#faf8f5">',
        f'<link rel="alternate" type="application/rss+xml" title="{e(BLOG_TITLE)}" href="{SITE}/blog/feed.xml">',
        "",
        f'<meta property="og:type" content="{kind}">',
        f'<meta property="og:url" content="{e(url)}">',
        f'<meta property="og:title" content="{e(title)}">',
        f'<meta property="og:description" content="{e(description)}">',
        f'<meta property="og:image" content="{e(image)}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{e(title)}">',
        f'<meta name="twitter:description" content="{e(description)}">',
        f'<meta name="twitter:image" content="{e(image)}">',
    ]
    if post:
        parts += [
            f'<meta property="article:published_time" content="{post.date.isoformat()}">',
            f'<meta property="article:author" content="{AUTHOR}">',
        ]
        parts += [f'<meta property="article:tag" content="{e(tag)}">' for tag in post.tags]
        parts.append(json_ld(post))
    parts += [
        "",
        FONTS,
        f'<link rel="stylesheet" href="{css_prefix}assets/css/blog.css">',
        "</head>",
        "<body>",
        '<a class="skip" href="#main">Skip to content</a>',
    ]
    return "\n".join(parts)


def json_ld(post: Post) -> str:
    import json
    data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.title,
        "description": post.summary,
        "datePublished": post.date.isoformat(),
        "url": post.abs_url,
        "image": post.image,
        "keywords": ", ".join(post.tags) or None,
        "author": {
            "@type": "Person",
            "name": AUTHOR,
            "url": SITE,
            "identifier": "https://orcid.org/0000-0001-6831-3001",
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": post.abs_url},
    }
    data = {k: v for k, v in data.items() if v is not None}
    body = json.dumps(data, indent=2, ensure_ascii=False)
    return f'<script type="application/ld+json">\n{body}\n</script>'


def topbar(css_prefix: str, *, on_index: bool) -> str:
    blog_href = "./" if on_index else "../"
    return f"""<header class="top">
  <div class="shell">
    <a class="home" href="{css_prefix}"><span>&larr;</span> Richard Polzin</a>
    <nav aria-label="Site">
      <a href="{blog_href}">Writing</a>
      <a href="{css_prefix}#workshops">Workshops</a>
      <a href="{css_prefix}#contact">Get in touch</a>
    </nav>
  </div>
</header>"""


def site_footer(css_prefix: str) -> str:
    year = dt.date.today().year
    return f"""<footer class="site shell">
  <span>{AUTHOR} — Aachen, Germany · &copy; {year}</span>
  <span><a href="{css_prefix}blog/feed.xml">RSS</a> · <a href="https://github.com/DeastinY/teaching">source on GitHub</a></span>
</footer>
</body>
</html>"""


def render_index(posts: list[Post]) -> str:
    if posts:
        items = "\n".join(
            f"""      <li>
        <a class="post-link" href="./{p.slug}/">
          <span class="when">{t(p.long_date)}</span>
          <div>
            <h2>{t(p.title)}</h2>
            <p>{t(p.summary)}</p>
            <p class="meta">{p.minutes} min read{tag_suffix(p)}</p>
          </div>
        </a>
      </li>"""
            for p in posts
        )
        body = f'    <ul class="posts">\n{items}\n    </ul>'
    else:
        body = '    <p class="empty">Nothing published yet.</p>'

    count = f"{len(posts)} post{'s' if len(posts) != 1 else ''}" if posts else "In progress"

    return f"""{head(title=BLOG_TITLE, description=BLOG_TAGLINE,
                     url=f"{SITE}/blog/", image=DEFAULT_IMAGE, css_prefix="../")}

{topbar("../", on_index=True)}

<main id="main">

<section class="masthead">
  <div class="shell">
    <p class="eyebrow">{t(count)} · <a href="./feed.xml">RSS</a></p>
    <h1>Writing<em>.</em></h1>
    <p>{t(BLOG_TAGLINE)}</p>
  </div>
</section>

<section class="listing">
  <div class="shell">
{body}
  </div>
</section>

</main>

{site_footer("../")}
"""


def tag_suffix(post: Post) -> str:
    return (" · " + " · ".join(t(x) for x in post.tags)) if post.tags else ""


def render_post(post: Post) -> str:
    tags = ""
    if post.tags:
        tags = ('<ul class="tags">' + "".join(f"<li>{t(x)}</li>" for x in post.tags) + "</ul>")

    nearby = ""
    cards = []
    if post.next:
        cards.append(f'<a href="../{post.next.slug}/"><span class="dir">Newer</span>'
                     f'<strong>{t(post.next.title)}</strong></a>')
    if post.prev:
        cards.append(f'<a href="../{post.prev.slug}/"><span class="dir">Older</span>'
                     f'<strong>{t(post.prev.title)}</strong></a>')
    if cards:
        nearby = '\n  <div class="nearby">\n    ' + "\n    ".join(cards) + "\n  </div>"

    standfirst = f'\n    <p class="standfirst">{t(post.summary)}</p>' if post.summary else ""

    return f"""{head(title=f"{post.title} — {AUTHOR}", description=post.summary or post.title,
                     url=post.abs_url, image=post.image, css_prefix="../../", post=post)}

{topbar("../../", on_index=False)}

<main id="main">

<article class="article">
  <header class="article-head">
    <time class="when" datetime="{post.date.isoformat()}">{t(post.long_date)}</time>
    <h1>{t(post.title)}</h1>{standfirst}
    <div class="about">
      <span>{post.minutes} min read</span>
      {tags}
    </div>
  </header>

  <div class="prose">
{post.body}
  </div>
</article>

<div class="article-foot">
  <a class="back" href="../"><span>&larr;</span> All writing</a>{nearby}
</div>

</main>

{site_footer("../../")}
"""


def render_feed(posts: list[Post]) -> str:
    # the newest post rather than "now", so rebuilding without writing anything
    # leaves the file byte-identical and out of the diff
    newest = dt.datetime.combine(
        posts[0].date if posts else dt.date(2026, 1, 1), dt.time(9, 0), tzinfo=dt.timezone.utc
    )
    items = []
    for post in posts[:20]:
        published = dt.datetime.combine(post.date, dt.time(9, 0), tzinfo=dt.timezone.utc)
        items.append(f"""    <item>
      <title>{sx.escape(post.title)}</title>
      <link>{post.abs_url}</link>
      <guid isPermaLink="true">{post.abs_url}</guid>
      <pubDate>{format_datetime(published)}</pubDate>
      <description>{sx.escape(post.summary)}</description>
{chr(10).join(f"      <category>{sx.escape(t)}</category>" for t in post.tags)}
      <content:encoded><![CDATA[{post.body.replace("]]>", "]]&gt;")}]]></content:encoded>
    </item>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"
     xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>{sx.escape(BLOG_TITLE)}</title>
    <link>{SITE}/blog/</link>
    <atom:link href="{SITE}/blog/feed.xml" rel="self" type="application/rss+xml"/>
    <description>{sx.escape(BLOG_TAGLINE)}</description>
    <language>en</language>
    <managingEditor>{EMAIL} ({AUTHOR})</managingEditor>
    <lastBuildDate>{format_datetime(newest)}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""


# --------------------------------------------------------------------------- #
# the homepage list
# --------------------------------------------------------------------------- #

START = "<!-- BLOG:START -->"
END = "<!-- BLOG:END -->"


def render_homepage_block(posts: list[Post]) -> str:
    if not posts:
        return '      <p class="sign-off" style="margin:0">Nothing published yet.</p>'

    items = "\n".join(
        f"""        <li>
          <span class="yr">{t(p.short_date)}</span>
          <strong><a href="./blog/{p.slug}/">{t(p.title)}</a></strong>
          <p>{t(p.summary)}</p>
        </li>"""
        for p in posts[:HOMEPAGE_POSTS]
    )
    # always link the archive: with few enough posts to fit here, this is
    # otherwise the only way onto /blog/ from the homepage
    label = f"All {len(posts)} posts" if len(posts) > HOMEPAGE_POSTS else "The archive, and the feed"
    more = (f'\n      <p class="orcid-note rise"><a href="./blog/">'
            f'{label} &rarr;</a></p>')
    return f"""      <ul class="entries writing rise">
{items}
      </ul>{more}"""


def update_homepage(posts: list[Post]) -> str:
    text = INDEX.read_text(encoding="utf-8")
    if START not in text or END not in text:
        die(f"index.html has no {START} / {END} markers — cannot place the recent posts.")
    before, _, rest = text.partition(START)
    _, _, after = rest.partition(END)
    return f"{before}{START}\n{render_homepage_block(posts)}\n{END}{after}"


# --------------------------------------------------------------------------- #
# driver
# --------------------------------------------------------------------------- #

def die(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def write(path: Path, content: str, *, check: bool, changed: list[str]) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == content:
        return
    changed.append(str(path.relative_to(ROOT)))
    if not check:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--drafts", action="store_true", help="include posts marked draft: true")
    ap.add_argument("--check", action="store_true", help="report what would change, write nothing (exit 1 if stale)")
    args = ap.parse_args()

    posts = load_posts(include_drafts=args.drafts)
    changed: list[str] = []

    write(OUT / "index.html", render_index(posts), check=args.check, changed=changed)
    write(OUT / "feed.xml", render_feed(posts), check=args.check, changed=changed)
    for post in posts:
        write(OUT / post.slug / "index.html", render_post(post), check=args.check, changed=changed)
    write(INDEX, update_homepage(posts), check=args.check, changed=changed)

    # a renamed or deleted post must not leave its page live
    keep = {p.slug for p in posts}
    for entry in sorted(OUT.glob("*/")) if OUT.is_dir() else []:
        if entry.is_dir() and entry.name not in keep:
            changed.append(f"{entry.relative_to(ROOT)} (removed)")
            if not args.check:
                shutil.rmtree(entry)

    drafts = sum(1 for p in POSTS.glob("*.md")) - len(posts) if POSTS.is_dir() else 0
    noun = "post" if len(posts) == 1 else "posts"
    print(f"{len(posts)} {noun} built" + (f", {drafts} draft(s) skipped" if drafts and not args.drafts else ""))

    if args.check:
        if changed:
            print("out of date, run tools/build_blog.py:", file=sys.stderr)
            for c in changed:
                print(f"    {c}", file=sys.stderr)
            return 1
        print("up to date")
        return 0

    for c in changed:
        print(f"    {c}")
    if not changed:
        print("    (nothing changed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
