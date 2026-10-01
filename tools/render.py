"""Genererer galleri, sitemap.xml og robots.txt – og bytter domene ved behov.

Bruk:
  python3 tools/render.py                              # bygg på nytt med nåværende adresse
  python3 tools/render.py --site-url https://sandertunet27.no/   # bytt til eget domene
  python3 tools/render.py --lastmod 2026-10-12         # sett «sist oppdatert» etter en innholdsendring
"""
import argparse
import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
CONFIG = ROOT / "tools" / "site.json"
PREFIX = "sandertunet-27-ski"
MONTHS = ["januar", "februar", "mars", "april", "mai", "juni", "juli",
          "august", "september", "oktober", "november", "desember"]

# Første bilde vises stort i galleriet. Plantegningen (5) vises i egen seksjon.
GALLERY_ORDER = [7, 1, 3, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 2, 18, 19, 20, 21, 22, 23, 24, 25]


def img(item, w):
    return f"assets/img/{PREFIX}-{item['slug']}-{w}.webp"


def render_gallery(images):
    by_n = {i["n"]: i for i in images}
    rows = []
    for idx, n in enumerate(GALLERY_ORDER):
        it = by_n[n]
        if idx == 0:
            sizes = "(min-width:1160px) 750px, (min-width:760px) 66vw, 100vw"
        elif idx == len(GALLERY_ORDER) - 1:  # siste flis går over hele bredden på mobil (se CSS)
            sizes = "(min-width:1160px) 370px, (min-width:760px) 32vw, 100vw"
        else:
            sizes = "(min-width:1160px) 370px, (min-width:760px) 32vw, 50vw"
        widths = [w for w in (480, 800, 1200, 1600) if w <= it["width"]]
        srcset = ", ".join(f"{img(it, w)} {w}w" for w in widths)
        alt = html.escape(it["alt"], quote=True)
        rows.append(
            f'        <a href="{img(it, 1600)}"><img src="{img(it, 800)}" srcset="{srcset}" sizes="{sizes}" '
            f'width="{it["width"]}" height="{it["height"]}" loading="lazy" decoding="async" alt="{alt}"></a>'
        )
    return "\n".join(rows)


def render_sitemap(images, url, lastmod):
    parts = []
    for it in images:
        w = 1600 if it["width"] >= 1600 else 1200
        parts.append(
            "    <image:image>\n"
            f"      <image:loc>{url}{img(it, w)}</image:loc>\n"
            "    </image:image>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
        "  <url>\n"
        f"    <loc>{url}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        + "\n".join(parts)
        + "\n  </url>\n</urlset>\n"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-url", help="Full adresse til siden, f.eks. https://sandertunet27.no/")
    ap.add_argument("--lastmod", help="Dato for siste innholdsendring, YYYY-MM-DD")
    args = ap.parse_args()

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    if args.lastmod:
        date.fromisoformat(args.lastmod)
        cfg["lastmod"] = args.lastmod
        CONFIG.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    lastmod = cfg["lastmod"]
    d = date.fromisoformat(lastmod)
    old = cfg["site_url"]
    new = args.site_url or old
    if not new.endswith("/"):
        new += "/"

    if new != old:
        for f in list(SITE.glob("*.html")) + list(SITE.glob("*.txt")) + list(SITE.glob("*.webmanifest")):
            f.write_text(f.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
        cfg["site_url"] = new
        CONFIG.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")

    # GitHub Pages trenger CNAME-fil når siden ligger på eget domene.
    host = urlparse(new).hostname or ""
    cname = SITE / "CNAME"
    if host.endswith("github.io"):
        cname.unlink(missing_ok=True)
    else:
        cname.write_text(host + "\n", encoding="utf-8")

    images = json.loads((ROOT / "tools" / "images.json").read_text(encoding="utf-8"))

    index = SITE / "index.html"
    page = index.read_text(encoding="utf-8")
    page = re.sub(
        r"(<!-- galleri:start -->\n).*?(<!-- galleri:slutt -->)",
        lambda m: m.group(1) + render_gallery(images) + "\n" + m.group(2),
        page,
        flags=re.S,
    )
    page = re.sub(r'"dateModified": "[0-9-]+"', f'"dateModified": "{lastmod}"', page)
    page = re.sub(r"Sist oppdatert [0-9]{1,2}\. [a-zæøå]+ [0-9]{4}", f"Sist oppdatert {d.day}. {MONTHS[d.month - 1]} {d.year}", page)
    index.write_text(page, encoding="utf-8")

    (SITE / "sitemap.xml").write_text(render_sitemap(images, new, lastmod), encoding="utf-8")
    (SITE / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {new}sitemap.xml\n", encoding="utf-8"
    )
    print(f"Ferdig: {new}")


if __name__ == "__main__":
    main()
