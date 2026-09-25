#!/usr/bin/env python3
"""One-shot (2026-09-24): copy the article photos still hot-linked from Squarespace
(thecybrtrkguy.com is being shut down) into assets/img/articles/ as WebP, and point
the article pages at the local copies. Idempotent: pages with no Squarespace URLs are skipped.

Only swaps URLs (and adds width/height to those <img> tags). No other text changes.
"""
import io, os, re, sys, urllib.request
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/img/articles"
PREFIX = {
    "install-a-starlink-mini-on-a-cybertruck-48v": "starlink",
    "driving-cybertruck-from-michigan-to-montana": "montana",
    "guide-to-driving-cybertruck-in-extreme-cold": "cold",
    "cybertruck-winter-tire-range-test-at-70-mph": "winter-tire",
    "cybertruck-7500-ev-tax-credit": "tax-credit",
}
# One URL on the live page was truncated when it was copied over; this is the real file.
FIX = {
    "https://images.squarespace-cdn.com/content/v1/6588487a366b5a6bfef0f90e/1726883122750-0H3NRILUUW1P/GXZB2U9bwAA9knz.jpeg":
    "https://images.squarespace-cdn.com/content/v1/6588487a366b5a6bfef0f90e/1726883122750-0H3NRILUUW1PH5YJW00I/GXZB2U9bwAA9knz.jpeg",
}
SQ = re.compile(r'https://images\.squarespace-cdn\.com/[^"\'\s<>]+')


def local_name(url, prefix):
    base = os.path.basename(url).replace("+", "-")
    base = re.sub(r"\.(jpe?g|png|jpg\.png)$", "", base, flags=re.I).lower()
    base = re.sub(r"[^a-z0-9-]+", "-", base).strip("-")
    return "%s-%s.webp" % (prefix, base)


def fetch(url):
    req = urllib.request.Request(FIX.get(url, url) + "?format=2500w", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for slug, prefix in PREFIX.items():
        page = ROOT / "articles" / slug / "index.html"
        text = page.read_text(encoding="utf-8")
        urls = sorted(set(SQ.findall(text)))
        if not urls:
            continue
        new = text
        for url in urls:
            name = local_name(url, prefix)
            dst = OUT / name
            im = ImageOps.exif_transpose(Image.open(io.BytesIO(fetch(url)))).convert("RGB")
            im.thumbnail((1600, 1600), Image.LANCZOS)
            im.save(dst, "WEBP", quality=80, method=6)
            w, h = im.size
            local = "/assets/img/articles/" + name
            n_src = new.count('src="%s"' % url)
            n_href = new.count('href="%s"' % url)
            if n_src + n_href != new.count(url):
                sys.exit("%s: %s appears outside src/href; not touching it" % (page, url))
            new = new.replace('src="%s"' % url, 'src="%s" width="%d" height="%d"' % (local, w, h))
            new = new.replace('href="%s"' % url, 'href="%s"' % local)
            total += 1
            print("%-60s %dx%d %6d KB  (%d src, %d href)" % (name, w, h, dst.stat().st_size // 1024, n_src, n_href))
        if SQ.search(new):
            sys.exit("%s still has Squarespace URLs" % page)
        page.write_text(new, encoding="utf-8")
    print("done: %d images" % total)


if __name__ == "__main__":
    main()
