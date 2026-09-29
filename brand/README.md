# Unvertical wordmark — vector masters

Source files for the `unvertical` wordmark, kept here for trademark filing and
other off-site use. Hugo does not publish this directory; nothing here is served
from unvertical.com.

## Files

| File | Use |
| --- | --- |
| `unvertical-wordmark-black.svg` | Solid black. The drawing for a black-and-white filing (no colour claimed). |
| `unvertical-wordmark-color-light.svg` | Two-colour, dark `un`. Legible on white/light grounds. |
| `unvertical-wordmark-color-dark-panel.svg` | **The mark exactly as it appears on the site** — light `un` and teal `vertical` on the `#0a0c10` ground, with the ground included in the image. |
| `unvertical-wordmark-color-dark.svg` | The same two colours on a transparent ground, for placing over an existing dark background. Invisible on white. |
| `raster/*-944.{jpg,png}` | 944 px wide renders of each, flattened onto white (the dark variants onto `#0a0c10`). |

The panel variant carries its ground as a `<rect>`, with clear space on all four
sides equal to the font's x-height (550/1000 em). That ground is part of the
image: filing it claims the dark background as part of the mark.

## Construction

Letterforms are outlined from **JetBrains Mono Bold** (v2.304), matching the
site's nav logo: 700 weight, `-0.5px` letter-spacing at `18px` (`-27.78`/1000 em
units), applied between letters only. `brand/build-wordmark.py` regenerates
everything; it needs `fonttools` and the upstream JetBrains Mono release.

The SVGs contain **only `<path>` elements** — no `<text>`, no embedded or
referenced font, no background rectangle. They render identically regardless of
what fonts the viewer has. The `viewBox` is the tight ink bounding box
(`0 0 5634 796`, aspect 7.0779:1), so there is no surrounding whitespace to crop.

Colours used for these renders (live values live in `static/css/main.css`; the
hex below is the snapshot these files were built from and should not drift
without regenerating them):

- `un` on dark — `#e8eaf0` (`--text-primary`)
- `un` on light — `#0a0c10` (`--bg-primary`)
- `vertical` — `#4ecdc4` (`--accent`)

## Font licence

JetBrains Mono is licensed under the SIL Open Font License 1.1, included as
`JetBrainsMono-OFL.txt`. The OFL governs the font software; it does not restrict
the design of artwork produced with it, and outlines converted into a logo are
not themselves subject to the OFL. No font software is redistributed here — only
the converted outlines.
