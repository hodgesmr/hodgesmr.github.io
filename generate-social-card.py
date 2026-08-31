#!/usr/bin/env python
"""Generate the sitewide social preview card, img/social.jpg (1200x630).

The design is the site's masthead as an image: a white left panel with the
name set large in Newsreader Italic (the navbar/favicon face), the red
structural accent rule, DM Mono metadata lines, and the img/photo.jpg
headshot full-bleed on the right. Every page that lacks its own image
serves this card via og:image / twitter:image.

Outputs (written under the site root, and mirrored into docs/ so a
card-only change deploys without a full render):
  img/social.jpg

Usage:
  python generate-social-card.py                 rebuild unconditionally
  python generate-social-card.py --if-changed    rebuild only if the inputs changed

Change detection: the inputs are this file's source (which carries the font
pins, palette, and layout) plus img/photo.jpg. Their SHA-256 is stamped into
the JPEG as a COM (comment) segment; --if-changed parses that marker with the
standard library and exits in a few milliseconds when nothing changed.
_quarto.yml runs this as a pre-render hook alongside generate-favicons.py.

Rebuilding needs Pillow (in .venv; run with .venv/bin/python). Fonts are
pinned to google/fonts commits and verified by digest; they are cached under
.cache/fonts/ (gitignored) so repeat builds are offline.

Gotcha for future edits: Pillow's set_variation_by_axes takes values in the
font's own fvar order. For Newsreader that is (wght, opsz), not the
(opsz, wght) the filename suggests; a swapped pair silently clamps both axes.
"""

import argparse
import hashlib
import json
import os
import shutil
import struct
import sys
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(ROOT, ".cache", "fonts")

# Newsreader Italic: same pin as generate-favicons.py (shares its cache file).
NEWSREADER_COMMIT = "991ce1de6075188e6b8977a5aa9fcd3610a4e946"
# DM Mono: pinned to the google/fonts commit that last touched ofl/dmmono.
DMMONO_COMMIT = "bfb7c046dea572dca9fdd435481ba2f36b0a1ebc"

FONTS = {
    "newsreader": (
        f"https://raw.githubusercontent.com/google/fonts/{NEWSREADER_COMMIT}/ofl/newsreader/"
        "Newsreader-Italic%5Bopsz%2Cwght%5D.ttf",
        "796668611f80b64d5adf182fde3b6f29ed83b4e7cbec7b96937e84ac01364792",
        f"Newsreader-Italic-{NEWSREADER_COMMIT[:12]}.ttf",
    ),
    "dmmono-medium": (
        f"https://raw.githubusercontent.com/google/fonts/{DMMONO_COMMIT}/ofl/dmmono/DMMono-Medium.ttf",
        "fd327daf461db87b44a87def475d251bf03b997f7c07d9680592d75dbbfaad0b",
        f"DMMono-Medium-{DMMONO_COMMIT[:12]}.ttf",
    ),
    "dmmono-regular": (
        f"https://raw.githubusercontent.com/google/fonts/{DMMONO_COMMIT}/ofl/dmmono/DMMono-Regular.ttf",
        "55b4c98f123daebb3ed27947ba47b2af00554fc6284d639a540bcef5e6258ad2",
        f"DMMono-Regular-{DMMONO_COMMIT[:12]}.ttf",
    ),
}

PHOTO = "img/photo.jpg"
OUT = "img/social.jpg"

# styles.scss palette
GRAY_500 = "#6B7280"
GRAY_700 = "#374151"
GRAY_900 = "#111827"
RED = "#B91C1C"
WHITE = "#FFFFFF"

W, H = 1200, 630
S = 2                     # render at 2x, downsample for anti-aliasing
LEFT = 84                 # left margin of the text block
Y_NAME = 228              # baseline of "Matt"; "Hodges" sits 150 below
NAME_SIZE = 148           # Newsreader Italic, wght 500, opsz 72
PHOTO_W = 480             # right-side photo panel width
PHOTO_FOCUS = (470, 285)  # face center in img/photo.jpg coordinates
JPEG_QUALITY = 92         # subsampling 4:4:4 keeps the type and rule clean

STAMP = "generate-social-card.py inputs sha256:{}"


# --- change detection (standard library only) --------------------------------

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def input_digest():
    """Hash of everything that determines the output: this script's source
    (font pins, palette, layout, quality) plus the headshot."""
    h = hashlib.sha256()
    with open(os.path.abspath(__file__), "rb") as fh:
        h.update(fh.read())
    h.update(json.dumps({"photo": sha256_file(os.path.join(ROOT, PHOTO))}).encode())
    return h.hexdigest()


def jpeg_comments(path):
    """Return the COM segment payloads of a JPEG, without Pillow."""
    comments = []
    with open(path, "rb") as fh:
        if fh.read(2) != b"\xff\xd8":
            return comments
        while True:
            byte = fh.read(1)
            if not byte:
                return comments
            if byte != b"\xff":
                continue
            marker = fh.read(1)
            if not marker or marker in b"\xff\x00\x01" or b"\xd0" <= marker <= b"\xd9":
                continue
            if marker == b"\xda":  # start of scan: no more metadata segments
                return comments
            (length,) = struct.unpack(">H", fh.read(2))
            payload = fh.read(length - 2)
            if marker == b"\xfe":
                comments.append(payload)


def is_current(out_root, digest):
    out = os.path.join(out_root, OUT)
    if not os.path.exists(out):
        return False
    stamp = STAMP.format(digest).encode()
    return any(stamp in c for c in jpeg_comments(out))


def mirror(out_root, mirror_root):
    src = os.path.join(out_root, OUT)
    dst = os.path.join(mirror_root, OUT)
    if os.path.exists(dst) and sha256_file(src) == sha256_file(dst):
        return 0
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    return 1


# --- building ----------------------------------------------------------------

def fetch_font(key):
    url, digest, name = FONTS[key]
    path = os.path.join(FONT_DIR, name)
    if os.path.exists(path) and sha256_file(path) == digest:
        return path
    os.makedirs(FONT_DIR, exist_ok=True)
    print(f"downloading {url}")
    tmp = path + ".part"
    urllib.request.urlretrieve(url, tmp)
    got = sha256_file(tmp)
    if got != digest:
        os.remove(tmp)
        sys.exit(f"font digest mismatch for {name}: expected {digest}, got {got}")
    os.replace(tmp, path)
    return path


def build(out_root, digest):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        sys.exit("Pillow not importable; run with the .venv python (.venv/bin/python generate-social-card.py)")

    def newsreader(px, wght, opsz):
        f = ImageFont.truetype(fetch_font("newsreader"), px * S)
        f.set_variation_by_axes([wght, opsz])  # fvar order: (wght, opsz)
        return f

    def dm_mono(px, medium):
        return ImageFont.truetype(fetch_font("dmmono-medium" if medium else "dmmono-regular"), px * S)

    def tracked(draw, xy, text, font, fill, tracking):
        x, y = xy[0] * S, xy[1] * S
        for ch in text:
            draw.text((x, y), ch, font=font, fill=fill, anchor="ls")
            x += draw.textlength(ch, font=font) + tracking * S

    img = Image.new("RGB", (W * S, H * S), WHITE)
    draw = ImageDraw.Draw(img)

    # Right panel: the headshot, cropped to keep the face centered.
    photo = Image.open(os.path.join(out_root, PHOTO)).convert("RGB")
    sw, sh = photo.size
    scale = max(PHOTO_W * S / sw, H * S / sh)
    crop_w, crop_h = PHOTO_W * S / scale, H * S / scale
    x0 = min(max(PHOTO_FOCUS[0] - crop_w / 2, 0), sw - crop_w)
    y0 = min(max(PHOTO_FOCUS[1] - crop_h / 2, 0), sh - crop_h)
    photo = photo.crop((int(x0), int(y0), int(x0 + crop_w), int(y0 + crop_h)))
    photo = photo.resize((PHOTO_W * S, H * S), Image.LANCZOS)
    img.paste(photo, ((W - PHOTO_W) * S, 0))

    # Left panel: name, rule, metadata.
    name_font = newsreader(NAME_SIZE, wght=500, opsz=72)
    draw.text((LEFT * S, Y_NAME * S), "Matt", font=name_font, fill=GRAY_900, anchor="ls")
    draw.text((LEFT * S, (Y_NAME + 150) * S), "Hodges", font=name_font, fill=GRAY_900, anchor="ls")

    rule_y = Y_NAME + 150 + 54
    draw.rectangle([LEFT * S, rule_y * S, (LEFT + 56) * S, (rule_y + 4) * S], fill=RED)

    tracked(draw, (LEFT, rule_y + 62), "POLITICAL TECHNOLOGIST", dm_mono(25, medium=True), GRAY_700, 5)
    tracked(draw, (LEFT, rule_y + 62 + 42), "MATTHODGES.COM", dm_mono(21, medium=False), GRAY_500, 4)

    out = os.path.join(out_root, OUT)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.resize((W, H), Image.LANCZOS).save(
        out, "JPEG",
        quality=JPEG_QUALITY, subsampling=0, optimize=True,
        comment=STAMP.format(digest).encode(),
    )
    print(f"wrote {out} ({W}x{H}, quality {JPEG_QUALITY})")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--if-changed", action="store_true",
                    help="Skip the build when the stamp in img/social.jpg matches the current inputs")
    ap.add_argument("--out", default=ROOT, help="Site root to write into (default: this script's directory)")
    ap.add_argument("--mirror", default=None,
                    help="Directory to mirror the output into (default: <out>/docs when it exists)")
    ap.add_argument("--no-mirror", action="store_true", help="Don't mirror into docs/")
    args = ap.parse_args()

    digest = input_digest()

    mirror_root = None
    if not args.no_mirror:
        mirror_root = args.mirror or os.path.join(args.out, "docs")
        if not os.path.isdir(mirror_root):
            mirror_root = None

    if args.if_changed and is_current(args.out, digest):
        msg = "social card up to date"
        if mirror_root and mirror(args.out, mirror_root):
            msg += f" (synced into {os.path.relpath(mirror_root, args.out)}/)"
        print(msg)
        return

    build(args.out, digest)
    if mirror_root and mirror(args.out, mirror_root):
        print(f"mirrored into {os.path.relpath(mirror_root, args.out)}/")


if __name__ == "__main__":
    main()
