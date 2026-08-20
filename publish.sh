#!/bin/bash
# Publish whatever the dashboard just produced.
#
#   ./publish.sh
#
# Works for a new post and for an edit, and for both routes the dashboard
# offers: files written straight into this folder, or a downloaded .zip that
# still needs unpacking. It figures out which by looking at the repository.
#
# Deliberately does its own `cd`: Terminal opens in your home folder, and the
# single most common way to get nowhere is to run git commands there.

set -u
cd "$(dirname "$0")" || exit 1

say()  { printf '  %s\n' "$1"; }
fail() { printf '\n  ✗ %s\n\n' "$1"; exit 1; }

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || fail "This folder is not a git repository."

printf '\nPublishing from %s\n\n' "$(pwd)"

# ---- 1. unpack a downloaded bundle, if one is newer than what we already have
# Finder cannot do this: double-clicking a zip expands it into a new folder
# rather than merging it into the repository.
ZIP=$(ls -t ~/Downloads/flaney-*.zip 2>/dev/null | head -1)
if [ -n "$ZIP" ] && [ -z "$(git status --porcelain)" ]; then
    say "No pending changes, but found a bundle: $(basename "$ZIP")"
    say "Unpacking it…"
    unzip -o -q "$ZIP" || fail "Could not unpack that bundle."
fi

if [ -z "$(git status --porcelain)" ]; then
    printf '\n  Nothing to publish — no changed files.\n'
    printf '  Press Generate in the dashboard first.\n\n'
    exit 0
fi

# ---- 2. work out what this publish is about
SLUG=$(python3 - <<'PY' 2>/dev/null
import json
try:
    posts = json.load(open('blog/data/posts.json'))
    print(max(posts, key=lambda p: p.get('modified', ''))['slug'])
except Exception:
    pass
PY
)

TITLE=$(python3 - <<'PY' 2>/dev/null
import json, html
try:
    posts = json.load(open('blog/data/posts.json'))
    p = max(posts, key=lambda x: x.get('modified', ''))
    print(html.unescape(p['title']).strip())
except Exception:
    pass
PY
)

if [ -n "$SLUG" ] && git ls-files --error-unmatch "blog/$SLUG.html" >/dev/null 2>&1; then
    VERB="Update"
else
    VERB="Publish"
fi
[ -n "$TITLE" ] || TITLE="site update"
MESSAGE="$VERB: $TITLE"

say "Changed files:"
git status --porcelain | sed 's/^/    /'
printf '\n'

# ---- 3. commit and push
git add -A || fail "git add failed."
git commit -q -m "$MESSAGE" || fail "git commit failed."
say "✓ committed — $MESSAGE"

if git push -q origin main 2>/dev/null; then
    say "✓ pushed to GitHub"
    printf '\n  Live in about a minute:\n'
    [ -n "$SLUG" ] && printf '  https://jotaigbe2026.github.io/Flaney_Associates/blog/%s.html\n\n' "$SLUG"
else
    printf '\n  ✗ Push failed — the commit is saved locally and nothing is lost.\n'
    printf '    Run:  git push origin main\n'
    printf '    and copy me whatever it says.\n\n'
    exit 1
fi
