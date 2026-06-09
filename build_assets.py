"""Prepare web-optimised images for the BMW 540i landing page.

Converts the 6 HEIC ambient shots to JPEG and resizes all 16 source photos from
pics/ into site/assets/ with a friendly name + a smaller gallery thumbnail.

Run:  uv run --with pillow --with pillow-heif python build_assets.py
"""

import os

from PIL import Image, JpegImagePlugin  # noqa: F401  (ensures JPEG save is registered)
import pillow_heif

Image.init()
pillow_heif.register_heif_opener()

SRC = "pics"
OUT = "site/assets"

# (source filename, output base name) — order = gallery order.
MAP = [
    ("photo_2026-06-09_10-55-47.jpg", "hero-front-left"),    # HERO
    ("photo_2026-06-09_10-55-29.jpg", "ext-front-right"),
    ("photo_2026-06-09_10-55-44.jpg", "ext-side"),
    ("photo_2026-06-09_10-55-21.jpg", "ext-front"),
    ("photo_2026-06-09_10-55-25.jpg", "ext-rear-right"),
    ("photo_2026-06-09_10-55-39.jpg", "ext-rear"),
    ("photo_2026-06-09_10-55-35.jpg", "ext-wheel"),
    ("photo_2026-06-09_10-55-51.jpg", "int-leather-detail"),
    ("photo_2026-06-09_10-55-56.jpg", "int-front-door"),
    ("photo_2026-06-09_11-00-20.jpg", "int-rear-door"),
    ("IMG_8390.HEIC", "amb-1"),
    ("IMG_8388.HEIC", "amb-2"),
    ("IMG_8391.HEIC", "amb-3"),
    ("IMG_8389.HEIC", "amb-4"),
    ("IMG_8392.HEIC", "amb-5"),
    ("IMG_8393.HEIC", "amb-6"),
]

FULL_EDGE = 2000
THUMB_EDGE = 1000


def fit(im, edge):
    im = im.copy()
    im.thumbnail((edge, edge), Image.LANCZOS)
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    for src, name in MAP:
        path = os.path.join(SRC, src)
        im = Image.open(path).convert("RGB")
        full = fit(im, FULL_EDGE)
        full.save(os.path.join(OUT, f"{name}.jpg"), "JPEG",
                  quality=82, optimize=True, progressive=True)
        thumb = fit(im, THUMB_EDGE)
        thumb.save(os.path.join(OUT, f"{name}-thumb.jpg"), "JPEG",
                   quality=80, optimize=True, progressive=True)
        print(f"  {src:38} -> {name}.jpg  ({full.width}x{full.height})")
    print(f"\nDone. {len(MAP)} images -> {OUT}/")


if __name__ == "__main__":
    main()
