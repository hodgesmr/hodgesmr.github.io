#!/usr/bin/env python
"""Generate the site favicon set from the Newsreader Italic "M" glyph.

The mark is the same italic serif the navbar brand uses, converted to a path so
it renders identically everywhere (no font dependency), on a full-bleed
gray-900 disc that fills the circular badge Google draws around favicons.

Outputs (written under the site root, and mirrored into docs/ so an icon-only
change deploys without a full render):
  img/favicon.svg            circle, dark-mode aware (browser tabs)
  img/favicon-96x96.png      circle (Google Search wants a raster >= 48px)
  img/icon-192.png           circle (web manifest, purpose "any")
  img/icon-512.png           circle (web manifest, purpose "any")
  img/icon-maskable-512.png  full-bleed square (web manifest, purpose "maskable")
  favicon.ico                16 + 32 + 48 circle layers
  apple-touch-icon.png       180px full-bleed square (iOS rounds the corners)

Usage:
  python generate-favicons.py                 rebuild unconditionally
  python generate-favicons.py --if-changed    rebuild only if the inputs changed
  python generate-favicons.py --wght 600 --opsz 8 --margin 8   try other settings

Change detection: the inputs are this file's source (which carries the font
pin and the defaults) plus the effective parameters. Their SHA-256 is stamped
into img/favicon.svg as a comment; --if-changed compares that stamp and checks
that every output exists, then exits in a few milliseconds. _quarto.yml runs
this as a pre-render hook, so `quarto render` rebuilds the icons exactly when
this script changes. The fast path needs only the standard library.

Rebuilding needs fontTools (in .venv) and ImageMagick's `magick` on PATH. The
font is pinned to a google/fonts commit and verified by digest; it is cached
under .cache/fonts/ (gitignored) so repeat builds are offline.
"""

import argparse
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))

# Newsreader Italic, variable (opsz 6..72, wght 200..800), OFL 1.1.
# Pinned to the google/fonts commit that last touched the file (v1.003).
FONT_COMMIT = "991ce1de6075188e6b8977a5aa9fcd3610a4e946"
FONT_URL = (
    f"https://raw.githubusercontent.com/google/fonts/{FONT_COMMIT}/ofl/newsreader/"
    "Newsreader-Italic%5Bopsz%2Cwght%5D.ttf"
)
FONT_SHA256 = "796668611f80b64d5adf182fde3b6f29ed83b4e7cbec7b96937e84ac01364792"
FONT_CACHE = os.path.join(ROOT, ".cache", "fonts", f"Newsreader-Italic-{FONT_COMMIT[:12]}.ttf")

CANVAS = 512
BG = "#111827"       # $gray-900
FG = "#FFFFFF"
BG_DARK = "#F9FAFB"  # $gray-100, used when the tab strip is dark
FG_DARK = "#111827"

# Output paths relative to the site root (and to the docs/ mirror).
SVG = "img/favicon.svg"
OUTPUTS = [
    SVG,
    "img/favicon-96x96.png",
    "img/icon-192.png",
    "img/icon-512.png",
    "img/icon-maskable-512.png",
    "favicon.ico",
    "apple-touch-icon.png",
]
STAMP = "<!-- generate-favicons.py inputs sha256:{} -->"


# --- change detection (standard library only) --------------------------------

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def input_digest(params):
    """Hash of everything that determines the outputs: this script's source
    (defaults, palette, geometry, font pin) plus the effective parameters."""
    h = hashlib.sha256()
    with open(os.path.abspath(__file__), "rb") as fh:
        h.update(fh.read())
    h.update(json.dumps(params, sort_keys=True).encode())
    return h.hexdigest()


def is_current(out_root, digest):
    svg = os.path.join(out_root, SVG)
    if not os.path.exists(svg):
        return False
    with open(svg, encoding="utf-8") as fh:
        if STAMP.format(digest) not in fh.read():
            return False
    return all(os.path.exists(os.path.join(out_root, rel)) for rel in OUTPUTS)


def mirror(out_root, mirror_root):
    """Copy outputs into the mirror (docs/) when missing or different."""
    copied = 0
    for rel in OUTPUTS:
        src = os.path.join(out_root, rel)
        dst = os.path.join(mirror_root, rel)
        if os.path.exists(dst) and sha256_file(src) == sha256_file(dst):
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        copied += 1
    return copied


# --- building ----------------------------------------------------------------

def fetch_font(explicit_path):
    if explicit_path:
        return explicit_path
    if os.path.exists(FONT_CACHE) and sha256_file(FONT_CACHE) == FONT_SHA256:
        return FONT_CACHE
    os.makedirs(os.path.dirname(FONT_CACHE), exist_ok=True)
    print(f"downloading {FONT_URL}")
    tmp = FONT_CACHE + ".part"
    urllib.request.urlretrieve(FONT_URL, tmp)
    got = sha256_file(tmp)
    if got != FONT_SHA256:
        os.remove(tmp)
        sys.exit(f"font digest mismatch: expected {FONT_SHA256}, got {got}")
    os.replace(tmp, FONT_CACHE)
    return FONT_CACHE


def glyph_path(font, char, canvas, radius, x_nudge=0.0):
    """Return the SVG path `d` for `char`, scaled so the glyph's ink bounding
    box fits inside a circle of `radius` px centered on a `canvas` px square.

    The italic M is much wider than it is tall (its serifs splay well past the
    stems), so fitting by cap height overflows a disc; fitting the bbox corner
    to the circle is what keeps the serifs inside it."""
    from fontTools.misc.transform import Transform
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen

    glyph_set = font.getGlyphSet()
    name = font.getBestCmap()[ord(char)]
    glyph = glyph_set[name]

    bp = BoundsPen(glyph_set)
    glyph.draw(bp)
    x_min, y_min, x_max, y_max = bp.bounds
    w, h = x_max - x_min, y_max - y_min
    # Half-diagonal of the ink box must equal the radius.
    scale = radius / (0.5 * math.hypot(w, h))

    tx = (canvas - w * scale) / 2 - x_min * scale + x_nudge
    ty = (canvas - h * scale) / 2 + y_max * scale  # y flips: font y-up, SVG y-down

    svg_pen = SVGPathPen(glyph_set, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    glyph.draw(TransformPen(svg_pen, Transform(scale, 0, 0, -scale, tx, ty)))
    return svg_pen.getCommands()


def circle_svg(d, stamp=None, dark_mode=True):
    style = ""
    if dark_mode:
        style = (
            "<style>@media (prefers-color-scheme: dark){"
            f".bg{{fill:{BG_DARK}}}.fg{{fill:{FG_DARK}}}"
            "}</style>"
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS} {CANVAS}">'
        f"{stamp or ''}{style}"
        f'<circle class="bg" cx="{CANVAS/2:g}" cy="{CANVAS/2:g}" r="{CANVAS/2:g}" fill="{BG}"/>'
        f'<path class="fg" fill="{FG}" d="{d}"/>'
        "</svg>\n"
    )


def square_svg(d):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS} {CANVAS}">'
        f'<rect width="{CANVAS}" height="{CANVAS}" fill="{BG}"/>'
        f'<path fill="{FG}" d="{d}"/>'
        "</svg>\n"
    )


def rasterize(svg_path, out_png, size):
    # Render at 4x and downsample for clean anti-aliasing at small sizes.
    subprocess.run(
        [
            "magick", "-background", "none", "-density", "384", svg_path,
            "-filter", "Lanczos", "-resize", f"{size}x{size}",
            "-strip", "-depth", "8", "-define", "png:compression-level=9", out_png,
        ],
        check=True,
    )


def build(args, params, digest):
    try:
        from fontTools.ttLib import TTFont
        from fontTools.varLib.instancer import instantiateVariableFont
    except ImportError:
        sys.exit("fontTools not importable; run with the .venv python (.venv/bin/python generate-favicons.py)")
    if shutil.which("magick") is None:
        sys.exit("ImageMagick `magick` not found on PATH")

    font = TTFont(fetch_font(args.font))
    if "fvar" in font:
        font = instantiateVariableFont(font, {"wght": args.wght, "opsz": args.opsz})

    d_circle = glyph_path(font, "M", CANVAS, CANVAS / 2 - args.margin, args.x_nudge)
    # Maskable safe zone: a centered disc with diameter 80% of the canvas.
    d_square = glyph_path(font, "M", CANVAS, CANVAS * 0.4 - args.margin_square, args.x_nudge)

    out = args.out
    os.makedirs(os.path.join(out, "img"), exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="favicons-")
    try:
        # Plain rasterization sources (ImageMagick doesn't need the style block).
        circle_plain = os.path.join(tmp, "circle.svg")
        square_plain = os.path.join(tmp, "square.svg")
        with open(circle_plain, "w") as fh:
            fh.write(circle_svg(d_circle, dark_mode=False))
        with open(square_plain, "w") as fh:
            fh.write(square_svg(d_square))

        rasterize(circle_plain, os.path.join(out, "img/favicon-96x96.png"), 96)
        rasterize(circle_plain, os.path.join(out, "img/icon-192.png"), 192)
        rasterize(circle_plain, os.path.join(out, "img/icon-512.png"), 512)
        rasterize(square_plain, os.path.join(out, "img/icon-maskable-512.png"), 512)
        rasterize(square_plain, os.path.join(out, "apple-touch-icon.png"), 180)

        ico_layers = []
        for size in (16, 32, 48):
            p = os.path.join(tmp, f"ico-{size}.png")
            rasterize(circle_plain, p, size)
            ico_layers.append(p)
        subprocess.run(["magick", *ico_layers, os.path.join(out, "favicon.ico")], check=True)

        # The published SVG carries the dark-mode swap and the input stamp.
        # Written last so an interrupted build can't leave a fresh stamp on stale rasters.
        with open(os.path.join(out, SVG), "w") as fh:
            fh.write(circle_svg(d_circle, stamp=STAMP.format(digest)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"wrote favicon set to {out} (wght={args.wght:g} opsz={args.opsz:g} margin={args.margin:g})")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--if-changed", action="store_true",
                    help="Skip the build when the stamp in img/favicon.svg matches the current inputs")
    ap.add_argument("--font", help="Path to a local Newsreader-Italic[opsz,wght].ttf (default: pinned download)")
    ap.add_argument("--out", default=ROOT, help="Site root to write into (default: this script's directory)")
    ap.add_argument("--mirror", default=None,
                    help="Directory to mirror the outputs into (default: <out>/docs when it exists)")
    ap.add_argument("--no-mirror", action="store_true", help="Don't mirror into docs/")
    ap.add_argument("--wght", type=float, default=700)
    ap.add_argument("--opsz", type=float, default=18)
    ap.add_argument("--margin", type=float, default=12,
                    help="Clearance in canvas px between the glyph's ink box and the disc edge")
    ap.add_argument("--margin-square", type=float, default=4,
                    help="Clearance inside the maskable safe zone (a disc 80%% of the canvas)")
    ap.add_argument("--x-nudge", type=float, default=0.0,
                    help="Optical horizontal nudge in canvas px (italic M leans right)")
    args = ap.parse_args()

    params = {
        "wght": args.wght, "opsz": args.opsz, "margin": args.margin,
        "margin_square": args.margin_square, "x_nudge": args.x_nudge,
        "font": sha256_file(args.font) if args.font else FONT_SHA256,
    }
    digest = input_digest(params)

    mirror_root = None
    if not args.no_mirror:
        mirror_root = args.mirror or os.path.join(args.out, "docs")
        if not os.path.isdir(mirror_root):
            mirror_root = None

    if args.if_changed and is_current(args.out, digest):
        msg = "favicons up to date"
        if mirror_root:
            n = mirror(args.out, mirror_root)
            if n:
                msg += f" (synced {n} file{'s' if n != 1 else ''} into {os.path.relpath(mirror_root, args.out)}/)"
        print(msg)
        return

    build(args, params, digest)
    if mirror_root:
        n = mirror(args.out, mirror_root)
        print(f"mirrored {n} file{'s' if n != 1 else ''} into {os.path.relpath(mirror_root, args.out)}/")


if __name__ == "__main__":
    main()
