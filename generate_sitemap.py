#!/usr/bin/env python3
"""Write sitemap.xml from the pages this site actually serves.

The file used to be maintained by hand. It was written once in September 2026
and by the middle of October it was missing three articles, still listed a
deleted one, and told Google every page was last changed on the day the file
was created. Everything else on this site is generated; this now is too.

What is kept from the hand-written version: the priority and changefreq for
each kind of page. Those are editorial judgements — the homepage matters more
than a 2024 archive post — so they live in PAGES and POST_* below rather than
being invented per run.

What is computed: which URLs exist, and when each last actually changed.

    python3 generate_sitemap.py            # write sitemap.xml
    python3 generate_sitemap.py --dry-run  # print it, write nothing

Also called at the end of generate_blog.py, so a publish keeps it current
without anyone remembering.
"""

import json
import os
import subprocess
import sys
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT, "site.json")) as _f:
    BASE_URL = json.load(_f)["base_url"].rstrip("/")

# Static pages, in the order they appear in the file, with the weighting the
# hand-written sitemap gave them. The first element is the URL path as it is
# served; the second is the file whose change date it reflects.
PAGES = [
    ("/",                          "index.html",                 "weekly",  "1.0"),
    ("/contact.html",              "contact.html",               "monthly", "0.9"),
    ("/attorney-inquiry.html",     "attorney-inquiry.html",      "monthly", "0.9"),
    ("/services/failure-analysis.html",       "services/failure-analysis.html",       "monthly", "0.8"),
    ("/services/materials-selection.html",    "services/materials-selection.html",    "monthly", "0.8"),
    ("/services/product-development.html",    "services/product-development.html",    "monthly", "0.8"),
    ("/services/process-optimization.html",   "services/process-optimization.html",   "monthly", "0.8"),
    ("/services/technical-due-diligence.html", "services/technical-due-diligence.html", "monthly", "0.8"),
    ("/services/expert-witness.html",         "services/expert-witness.html",         "monthly", "0.8"),
    ("/blog/",                     "blog/index.html",            "weekly",  "0.8"),
    ("/about.html",                "about.html",                 "monthly", "0.7"),
    ("/industries.html",           "industries.html",            "monthly", "0.7"),
    ("/guides.html",               "guides.html",                "monthly", "0.7"),
    ("/checklist.html",            "checklist.html",             "monthly", "0.7"),
    ("/featured.html",             "featured.html",              "monthly", "0.7"),
]

POST_CHANGEFREQ = "yearly"
POST_PRIORITY = "0.6"


def git_date(path):
    """The date of the last commit touching this file.

    Falls back to today when the file has uncommitted changes, which is the
    case during a publish: the generator runs before publish.sh commits, and
    reporting the previous commit's date for a file being changed right now
    would be wrong in the one direction that matters.
    """
    try:
        dirty = subprocess.run(["git", "status", "--porcelain", "--", path],
                               cwd=ROOT, capture_output=True, text=True, check=True)
        if dirty.stdout.strip():
            return date.today().isoformat()
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path],
                             cwd=ROOT, capture_output=True, text=True, check=True)
        if out.stdout.strip():
            return out.stdout.strip()
    except Exception:
        pass
    try:
        return date.fromtimestamp(os.path.getmtime(os.path.join(ROOT, path))).isoformat()
    except OSError:
        return date.today().isoformat()


def posts_for_sitemap(today):
    """Published, non-gated posts that have a page on this site.

    Future-dated posts are left out. Their pages are reachable — scheduling
    here is presentation, not embargo — but the archive and homepage hide them
    until the day, and a search result for a post the site is still hiding
    reads as a mistake. The first rebuild on or after the date adds it.

    Gated posts have no page here at all; `blog/<slug>.html` is checked rather
    than assumed, because posts.json carries records the site does not render.
    """
    with open(os.path.join(ROOT, "blog", "data", "posts.json")) as f:
        posts = json.load(f)

    out = []
    for p in posts:
        if p.get("gated"):
            continue
        published = str(p["date"])[:10]
        if published > today:
            continue
        rel = "blog/%s.html" % p["slug"]
        if not os.path.exists(os.path.join(ROOT, rel)):
            continue
        # The later of the two: when it was published, and when the page was
        # last actually edited. A 2024 post whose references were fixed this
        # week has changed, and saying so is the point of lastmod.
        out.append((rel, max(published, git_date(rel))))
    out.sort(key=lambda r: r[0])
    return out


def build(today=None):
    today = today or date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
             '']

    def url(loc, lastmod, changefreq, priority):
        lines.extend([
            '  <url>',
            '    <loc>%s%s</loc>' % (BASE_URL, loc),
            '    <lastmod>%s</lastmod>' % lastmod,
            '    <changefreq>%s</changefreq>' % changefreq,
            '    <priority>%s</priority>' % priority,
            '  </url>',
        ])

    lines.append('  <!-- Pages -->')
    for loc, src, freq, pri in PAGES:
        if not os.path.exists(os.path.join(ROOT, src)):
            print("  skipped (no such file): %s" % src)
            continue
        url(loc, git_date(src), freq, pri)

    lines.extend(['', '  <!-- Articles -->'])
    for rel, lastmod in posts_for_sitemap(today):
        url("/" + rel, lastmod, POST_CHANGEFREQ, POST_PRIORITY)

    lines.extend(['', '</urlset>', ''])
    return "\n".join(lines)


def main():
    xml = build()
    count = xml.count("<loc>")
    if "--dry-run" in sys.argv:
        print(xml)
        print("  %d URLs (nothing written)" % count, file=sys.stderr)
        return
    path = os.path.join(ROOT, "sitemap.xml")
    before = open(path).read() if os.path.exists(path) else ""
    if before == xml:
        print("sitemap.xml           already current (%d URLs)" % count)
        return
    with open(path, "w") as f:
        f.write(xml)
    print("sitemap.xml           wrote %d URLs" % count)


if __name__ == "__main__":
    main()
