#!/usr/bin/env python3
"""Outline the Unvertical wordmark from JetBrains Mono Bold into filing-grade SVGs.

Produces pure-path SVGs (no <text>, no font dependency, no background) sized
from the tight ink bounding box, plus rasters for trademark office upload.
"""

import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

FONT = "jbm/fonts/ttf/JetBrainsMono-Bold.ttf"
WORD = "unvertical"
SPLIT = 2                      # "un" | "vertical"
FONT_SIZE = 18.0               # .nav-logo font-size
TRACKING_PX = -0.5             # .nav-logo letter-spacing
OUT = "out"

INK_DARK = "#0a0c10"           # --bg-primary, used as ink on light ground
INK_LIGHT = "#e8eaf0"          # --text-primary, the "un" as used on the site
ACCENT = "#4ecdc4"             # --accent

font = TTFont(FONT)
upm = font["head"].unitsPerEm
glyphset = font.getGlyphSet()
cmap = font.getBestCmap()
tracking = TRACKING_PX / FONT_SIZE * upm

# ---- lay the string out on the baseline -------------------------------------
pen_x = 0.0
placed = []
for i, ch in enumerate(WORD):
    g = glyphset[cmap[ord(ch)]]
    placed.append((ch, pen_x, g))
    pen_x += g.width
    if i < len(WORD) - 1:                    # tracking between letters only
        pen_x += tracking

bp = BoundsPen(glyphset)
for ch, x, g in placed:
    g.draw(TransformPen(bp, Transform().translate(x, 0)))
xmin, ymin, xmax, ymax = bp.bounds           # true ink bounds, y up

vb_w, vb_h = xmax - xmin, ymax - ymin
# flip y about the baseline (SVG grows downward) and pull ink to the origin
flip = Transform(1, 0, 0, -1, 0, 0).translate(-xmin, -ymax)

def path_for(chunk):
    spen = SVGPathPen(glyphset, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    for ch, x, g in chunk:
        g.draw(TransformPen(spen, flip.translate(x, 0)))
    return spen.getCommands()

d_un, d_vertical, d_all = path_for(placed[:SPLIT]), path_for(placed[SPLIT:]), path_for(placed)

WIDTH_PX = 2832.0                            # nominal size; vector, so arbitrary
scale = WIDTH_PX / vb_w

def write_svg(name, paths, note):
    body = "\n".join(f'  <path fill="{fill}" d="{d}"/>' for fill, d in paths)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH_PX:.0f}" height="{vb_h * scale:.0f}" viewBox="0 0 {vb_w:.0f} {vb_h:.0f}">
  <title>Unvertical</title>
  <desc>{note} Letterforms outlined from JetBrains Mono Bold (SIL Open Font License 1.1); no live text, no embedded font.</desc>
{body}
</svg>
'''
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(svg)
    return path

def write_panel_svg(name, ground, paths, note):
    """Same wordmark, but on its own ground — clear space all round = the font's x-height."""
    pad = font["OS/2"].sxHeight                  # 550 units
    pw, ph = vb_w + 2 * pad, vb_h + 2 * pad
    body = "\n".join(f'    <path fill="{fill}" d="{d}"/>' for fill, d in paths)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH_PX:.0f}" height="{ph / pw * WIDTH_PX:.0f}" viewBox="0 0 {pw:.0f} {ph:.0f}">
  <title>Unvertical</title>
  <desc>{note} Letterforms outlined from JetBrains Mono Bold (SIL Open Font License 1.1); no live text, no embedded font.</desc>
  <rect width="{pw:.0f}" height="{ph:.0f}" fill="{ground}"/>
  <g transform="translate({pad:.0f} {pad:.0f})">
{body}
  </g>
</svg>
'''
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(svg)
    return path


os.makedirs(OUT, exist_ok=True)
files = [
    write_panel_svg("unvertical-wordmark-color-dark-panel.svg", INK_DARK,
                    [(INK_LIGHT, d_un), (ACCENT, d_vertical)],
                    f"Unvertical wordmark exactly as it appears on unvertical.com: {INK_LIGHT} and {ACCENT} "
                    f"on a {INK_DARK} ground, which is part of the image."),
    write_svg("unvertical-wordmark-black.svg", [("#000000", d_all)],
              "Unvertical wordmark, solid black for a black-and-white drawing (no colour claimed)."),
    write_svg("unvertical-wordmark-color-light.svg", [(INK_DARK, d_un), (ACCENT, d_vertical)],
              f"Unvertical wordmark in colour for a light ground: {INK_DARK} and {ACCENT}."),
    write_svg("unvertical-wordmark-color-dark.svg", [(INK_LIGHT, d_un), (ACCENT, d_vertical)],
              f"Unvertical wordmark as used on the dark site ground: {INK_LIGHT} and {ACCENT}. Requires a dark background to be legible."),
]

print(f"upm={upm}  tracking={tracking:.2f}u  aspect={vb_w / vb_h:.4f}:1")
print(f"ink bounds x[{xmin:.0f},{xmax:.0f}] y[{ymin:.0f},{ymax:.0f}] -> viewBox 0 0 {vb_w:.0f} {vb_h:.0f}")
for p in files:
    print(f"  {p}  {os.path.getsize(p)} bytes")
