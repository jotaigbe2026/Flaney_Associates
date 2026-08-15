#!/usr/bin/env python3
"""Pull the blog archive off flaneyassociates.com into blog/data/posts.json.

The live site is WordPress and exposes an open REST API, so posts are read from
there rather than scraped. Featured images are downloaded into blog/images/.

Posts sitting behind the site's Simple Membership plugin return a
"You need to be logged in..." stub instead of a body. Those are recorded with
`gated: true` and keep their title, date, categories, image and published
abstract — no body text is invented for them.

    python3 extract_blog.py       # refresh content, then run generate_blog.py

Requires curl (the host's WAF rejects urllib's default client).
"""
import json
import os
import re
import subprocess
import time

BASE = "https://flaneyassociates.com/wp-json/wp/v2"
ROOT = os.path.dirname(os.path.abspath(__file__))
BLOG = os.path.join(ROOT, "blog")
IMGDIR = os.path.join(BLOG, "images")
DATA = os.path.join(BLOG, "data", "posts.json")

GATE_MARKER = "swpm-post-not-logged-in-msg"
PREFERRED_SIZES = ["medium_large", "large", "full"]


def curl_json(url, tries=3):
    for attempt in range(tries):
        r = subprocess.run(["curl", "-sS", "--fail", "--max-time", "90", url],
                           capture_output=True, text=True)
        if r.returncode == 0:
            try:
                return json.loads(r.stdout)
            except json.JSONDecodeError:
                pass
        if attempt == tries - 1:
            raise RuntimeError("fetch failed: %s\n%s" % (url, r.stderr[:400]))
        time.sleep(2)


def fetch_posts():
    cats = {c["id"]: c["name"]
            for c in curl_json(BASE + "/categories?per_page=100&_fields=id,name")}

    raw, page = [], 1
    while True:
        batch = curl_json("%s/posts?per_page=50&page=%d&_embed=wp:featuredmedia,author"
                          "&orderby=date&order=desc" % (BASE, page))
        if not isinstance(batch, list) or not batch:
            break
        raw.extend(batch)
        print("  page %d: +%d (total %d)" % (page, len(batch), len(raw)))
        if len(batch) < 50:
            break
        page += 1

    posts = []
    for p in raw:
        content = p["content"]["rendered"]
        gated = GATE_MARKER in content
        emb = p.get("_embedded", {})
        media = (emb.get("wp:featuredmedia") or [{}])[0]
        author = (emb.get("author") or [{}])[0]
        sizes = (media.get("media_details", {}) or {}).get("sizes", {}) or {}

        src = ""
        for size in PREFERRED_SIZES:
            if sizes.get(size, {}).get("source_url"):
                src = sizes[size]["source_url"]
                break

        posts.append({
            "id": p["id"],
            "slug": p["slug"],
            "date": p["date"],
            "modified": p["modified"],
            "link": p["link"],
            "title": p["title"]["rendered"],
            "excerpt": p["excerpt"]["rendered"],
            "content": "" if gated else content,
            "gated": gated,
            "words": 0 if gated else len(
                re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", content)).split()),
            "categories": [cats[c] for c in p.get("categories", []) if c in cats],
            "author": author.get("name", ""),
            "image": media.get("source_url", ""),
            "image_alt": media.get("alt_text", "") or "",
            "_download": src or media.get("source_url", ""),
        })
    return posts


def fetch_images(posts):
    os.makedirs(IMGDIR, exist_ok=True)
    ok = missing = 0
    for p in posts:
        src = p.pop("_download", "")
        p["local_image"] = ""
        if not src:
            missing += 1
            continue

        ext = os.path.splitext(src.split("?")[0])[1].lower()
        if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
            ext = ".jpg"
        fname = p["slug"][:80] + ext
        dest = os.path.join(IMGDIR, fname)

        if not (os.path.exists(dest) and os.path.getsize(dest) > 1000):
            r = subprocess.run(["curl", "-sS", "--fail", "-L", "--max-time", "90",
                                "-o", dest, src], capture_output=True, text=True)
            if r.returncode != 0 or not os.path.exists(dest) or os.path.getsize(dest) <= 1000:
                if os.path.exists(dest):
                    os.remove(dest)
                print("  image failed: %s" % p["slug"])
                missing += 1
                continue
        p["local_image"] = fname
        ok += 1
    return ok, missing


def local_posts():
    """Posts written in publisher/ rather than imported from WordPress.

    They exist only in posts.json, so a refresh that rewrote the file from the
    API alone would delete them. They are flagged `local: true` and carried
    across untouched.
    """
    try:
        existing = json.load(open(DATA))
    except (OSError, ValueError):
        return []
    return [p for p in existing if p.get("local")]


def main():
    print("fetching posts…")
    posts = fetch_posts()

    print("fetching featured images…")
    ok, missing = fetch_images(posts)

    kept = local_posts()
    if kept:
        remote = {p["slug"] for p in posts}
        kept = [p for p in kept if p["slug"] not in remote]
        posts.extend(kept)
        posts.sort(key=lambda p: p["date"], reverse=True)
        print("  keeping %d locally authored post(s)" % len(kept))

    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    json.dump(posts, open(DATA, "w"), indent=1)

    gated = sum(1 for p in posts if p["gated"])
    print("\n%d posts -> blog/data/posts.json" % len(posts))
    print("  full text %d | gated %d" % (len(posts) - gated, gated))
    print("  images %d | without image %d" % (ok, missing))
    print("\nNow run: python3 generate_blog.py")


if __name__ == "__main__":
    main()
