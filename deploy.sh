#!/usr/bin/env bash
# Build the slide deck and publish the site.
#
# GitHub Pages serves this repo from the *gh-pages* branch, not main
# (Settings > Pages: branch gh-pages, path /), so committing to main alone
# changes nothing on the live site. This script builds the Slidev deck,
# refreshes the copy that ships at /version-control-for-researchers/, and
# mirrors everything onto gh-pages minus the sources that should not be
# published.
#
#   ./deploy.sh            build, publish, and push
#   ./deploy.sh --dry-run  build and stage, show the diff, push nothing
set -euo pipefail

cd "$(dirname "$0")"
DECK=git/version-control-for-researchers
OUT=version-control-for-researchers
DRY=${1:-}

# paths that live in the repo but must never reach the published branch
NOT_PUBLISHED=(git tools deploy.sh)

echo "==> building the deck"
( cd "$DECK" && pnpm install && pnpm build )

echo "==> refreshing $OUT/"
rm -rf "$OUT"
cp -r "$DECK/dist" "$OUT"

# gh-pages is mirrored from the committed branch, so anything still sitting in
# the working tree would build here but never actually ship. Stop instead.
if [ -n "$(git status --porcelain)" ]; then
  echo
  echo "The working tree has uncommitted changes:"
  git status --short | sed 's/^/    /'
  echo
  echo "gh-pages is published from the committed branch, so these would not ship."
  echo "Commit them (the rebuilt $OUT/ included), then run ./deploy.sh again."
  [ "$DRY" = "--dry-run" ] || exit 1
fi

echo "==> mirroring onto gh-pages"
WT=$(mktemp -d)
trap 'git worktree remove --force "$WT" >/dev/null 2>&1 || true' EXIT
git worktree add --quiet "$WT" gh-pages
git -C "$WT" pull --quiet --ff-only origin gh-pages 2>/dev/null || true

SRC=$(git rev-parse --abbrev-ref HEAD)
# replace the branch contents wholesale so deletions propagate too
git -C "$WT" rm -rq --ignore-unmatch .
git -C "$WT" checkout "$SRC" -- .
for p in "${NOT_PUBLISHED[@]}"; do
  git -C "$WT" rm -rq --cached --ignore-unmatch "$p"
  rm -rf "${WT:?}/$p"
done
git -C "$WT" add -A

if git -C "$WT" diff --cached --quiet; then
  echo "==> gh-pages already up to date, nothing to publish"
  exit 0
fi

echo "==> changes to publish:"
git -C "$WT" diff --cached --stat | tail -8

if [ "$DRY" = "--dry-run" ]; then
  echo "==> dry run, not committing or pushing"
  exit 0
fi

git -C "$WT" commit -qm "Deploy $(git rev-parse --short "$SRC") from $SRC"
git -C "$WT" push -q origin gh-pages
echo "==> published: https://www.richardpolzin.com/"
