#!/usr/bin/env python3
"""Generate the profile header SVGs (dark + light variants).

Text is converted to vector paths with fontTools so the header renders
identically everywhere (GitHub blocks external fonts inside README SVGs).

Requires: pip install fonttools
Fonts:    scripts/fonts/ (IBM Plex, OFL-licensed, vendored)

Usage:    python3 scripts/generate_header.py
"""

import os

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
from fontTools.varLib.instancer import instantiateVariableFont

FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
DIST_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "dist"))

PALETTES = {
    "dark": {"ink": "#E6EDF3", "muted": "#8B949E", "accent": "#E8963A"},
    "light": {"ink": "#1F2328", "muted": "#57606A", "accent": "#B45309"},
}

WIDTH = 880


def load_font(filename, wght=None):
    font = TTFont(os.path.join(FONT_DIR, filename))
    if wght is not None:
        instantiateVariableFont(font, {"wght": wght, "wdth": 100}, inplace=True)
    return font


def text_to_path(font, text, size, tracking_em=0.0):
    """Render a string as a single SVG path `d` string. Returns (d, advance)."""
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    upem = font["head"].unitsPerEm
    scale = size / upem
    tracking_units = tracking_em * upem

    x = 0.0
    parts = []
    for ch in text:
        glyph_name = cmap.get(ord(ch))
        if glyph_name is None:
            x += upem * 0.25  # fallback advance for unmapped chars
            continue
        glyph = glyph_set[glyph_name]
        pen = SVGPathPen(glyph_set)
        # y-flip: font units are y-up, SVG is y-down
        tpen = TransformPen(pen, Transform(scale, 0, 0, -scale, x * scale, 0))
        glyph.draw(tpen)
        d = pen.getCommands()
        if d:
            parts.append(d)
        x += glyph.width + tracking_units
    return " ".join(parts), x * scale


def main():
    sans_semibold = load_font("IBMPlexSans-Var.ttf", wght=600)
    sans_medium = load_font("IBMPlexSans-Var.ttf", wght=500)
    serif_italic = TTFont(os.path.join(FONT_DIR, "IBMPlexSerif-Italic.ttf"))

    pad_x, pad_top = 4, 14

    # Line 1 — name
    name_size = 46
    name_d, _ = text_to_path(sans_semibold, "Anmol Parimoo", name_size, tracking_em=-0.015)
    name_baseline = pad_top + name_size * 0.78

    # Line 2 — the thesis mark: AI over BI ("over" in serif italic, accent)
    mark_size = 30
    ai_d, ai_w = text_to_path(sans_medium, "AI ", mark_size)
    over_d, over_w = text_to_path(serif_italic, "over", mark_size)
    bi_d, bi_w = text_to_path(sans_medium, " BI", mark_size)
    mark_baseline = name_baseline + 46

    # Line 3 — affiliation
    meta_size = 15
    meta_text = "Founder, MLDeep Systems · semantic layers & AI agents in production"
    meta_d, _ = text_to_path(sans_medium, meta_text, meta_size)
    meta_baseline = mark_baseline + 32

    height = int(meta_baseline + 18)

    for variant, colors in PALETTES.items():
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-label="Anmol Parimoo, AI over BI. Founder, MLDeep Systems">
  <g transform="translate({pad_x} {name_baseline})">
    <path d="{name_d}" fill="{colors['ink']}"/>
  </g>
  <g transform="translate({pad_x} {mark_baseline})">
    <path d="{ai_d}" fill="{colors['ink']}"/>
    <g transform="translate({ai_w:.1f} 0)"><path d="{over_d}" fill="{colors['accent']}"/></g>
    <g transform="translate({ai_w + over_w:.1f} 0)"><path d="{bi_d}" fill="{colors['ink']}"/></g>
  </g>
  <g transform="translate({pad_x} {meta_baseline})">
    <path d="{meta_d}" fill="{colors['muted']}"/>
  </g>
</svg>
'''
        path = os.path.join(DIST_DIR, f"header-{variant}.svg")
        with open(path, "w") as f:
            f.write(svg)
        print(f"Generated {path}")


if __name__ == "__main__":
    main()
