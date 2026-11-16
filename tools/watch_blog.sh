#!/usr/bin/env bash
# Rebuild the blog whenever a post changes.
#
# No watcher binary needed: this polls posts/ once a second and runs the same
# build deploy.sh does, with --drafts, so unfinished posts show up in the
# preview at localhost:3000/blog/. Ctrl-C to stop.
#
# What it leaves in blog/ therefore *includes* drafts. Before committing, build
# once more without the flag so the draft pages come back out:
#
#     uv run tools/build_blog.py
#
# A post that fails to build leaves the previous output in place and prints the
# error; fix it and save again, the watcher keeps running.
set -uo pipefail

cd "$(dirname "$0")/.."

build() {
  if python3 -c 'import markdown' >/dev/null 2>&1; then
    python3 tools/build_blog.py --drafts
  else
    uv run tools/build_blog.py --drafts
  fi
}

# name, mtime and size of every post — enough to notice an edit, a new file or
# a deletion without needing fswatch or entr installed
signature() {
  find posts -type f -name '*.md' -exec stat -f '%N %m %z' {} + 2>/dev/null | sort
}

echo "==> watching posts/ for changes — Ctrl-C to stop"
build || echo "!! build failed"
last=$(signature)

while true; do
  sleep 1
  now=$(signature)
  if [ "$now" != "$last" ]; then
    last=$now
    printf '\n==> %s  change detected\n' "$(date +%H:%M:%S)"
    build || echo "!! build failed — fix the post and save again"
  fi
done
