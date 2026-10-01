"""Genererer responsive WebP-bilder og delingsbilde (og-image) fra originalfotoene.

Bruk:  python3 tools/build_images.py <mappe med 01.jpg ... 25.jpg>
Krever Pillow (pip install pillow).
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "assets" / "img"
WIDTHS = [480, 800, 1200, 1600]
PREFIX = "sandertunet-27-ski"


def main(src_dir: Path) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = json.loads((ROOT / "tools" / "images.json").read_text(encoding="utf-8"))
    for item in meta:
        im = ImageOps.exif_transpose(Image.open(src_dir / f"{item['n']:02d}.jpg")).convert("RGB")
        for w in WIDTHS:
            if w > im.width:
                continue
            h = round(im.height * w / im.width)
            im.resize((w, h), Image.LANCZOS).save(
                OUT / f"{PREFIX}-{item['slug']}-{w}.webp", "WEBP", quality=78, method=6
            )
        item["width"], item["height"] = im.size

    # Delingsbilde 1200x630 (Facebook, Messenger, LinkedIn, Slack, iMessage)
    hero = Image.open(src_dir / "03.jpg").convert("RGB")
    ImageOps.fit(hero, (1200, 630), Image.LANCZOS, centering=(0.5, 0.55)).save(
        OUT / "og-image.jpg", "JPEG", quality=82, optimize=True, progressive=True
    )
    (ROOT / "tools" / "images.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main(Path(sys.argv[1]))
