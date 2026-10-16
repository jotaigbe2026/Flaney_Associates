#!/usr/bin/env python3
"""Name the post a publish is about, for publish.sh's commit message.

Called as `.publish_message.py slug` or `.publish_message.py title`.

It reads the files git reports as changed rather than the newest `modified`
stamp in posts.json. The stamp was wrong whenever several posts were queued in
one sitting: they share a timestamp, so `max()` returned whichever sorted last
and the history named an article the commit had not touched. Seen for real on
16 October 2026, when a summary edit to the October post was committed as
"Update: AI-driven materials discovery…", a January post.

Falls back to the stamp when the changed files name no post — an older bundle,
or a change confined to posts.json.
"""

import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

PATTERNS = (
    re.compile(r"blog/([a-z0-9-]+)\.html"),
    re.compile(r"articles/([a-z0-9-]+)\.pdf"),
    re.compile(r"blog/images/([a-z0-9-]+)\.[A-Za-z0-9]+"),
)


def changed_slugs():
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain", "--", "blog", "articles"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except Exception:
        return set()

    slugs = set()
    for line in out.splitlines():
        # "XY path", or "XY old -> new" for a rename; quoted when it has spaces
        path = line[3:].split(" -> ")[-1].strip().strip('"')
        for pattern in PATTERNS:
            m = pattern.fullmatch(path)
            if m and m.group(1) != "index":
                slugs.add(m.group(1))
                break
    return slugs


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else "slug"
    try:
        with open(os.path.join(ROOT, "blog", "data", "posts.json")) as f:
            posts = json.load(f)
    except Exception:
        return

    known = {p["slug"]: p for p in posts}
    named = [known[s] for s in changed_slugs() if s in known]

    if len(named) > 1:
        # Several posts in one publish: no single title would be honest.
        if want == "title":
            print("%d articles" % len(named))
        return

    post = named[0] if named else (
        max(posts, key=lambda p: p.get("modified", "")) if posts else None)
    if not post:
        return
    print(post["slug"] if want == "slug"
          else html.unescape(post["title"]).strip())


if __name__ == "__main__":
    main()
