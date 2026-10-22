---
name: look-ceramic-studio
title: "Look: Ceramic studio"
area: looks
tags: [look, style, palette, craft, studio, shop, handmade, portfolio]
detect: []
related: [look-sewing-pattern, look-night-market, design-systems, typography, color-contrast]
---
A potter's shelf of test tiles: bisque clay surfaces, one cobalt glaze, work captioned like samples, nothing glossy.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #F0E6DB | 0.93 0.018 70 | page |
| `--raised` | #FCF2E7 | 0.965 0.018 70 | cards, popovers |
| `--text` | #2C251D | 0.27 0.018 70 | 12.3:1 on surface, 13.7:1 on raised |
| `--text-muted` | #5C544B | 0.45 0.018 70 | 6.0:1 on surface, 6.7:1 on raised |
| `--border` | #847C72 | 0.59 0.018 70 | 3.3:1 on surface |
| `--accent` | #265399 | 0.45 0.125 259 | 6.1:1 on surface |
| `--on-accent` | #FFFFFF | 1 0.000 70 | 7.6:1 on accent |

Accent hue 259 (cobalt glaze), 109° from the nearest status hue. Terracotta stays a surface tint, never the accent: it sits on error red.

## Type
Old-style serif for headings at 600, humanist sans for body and captions at 400; they differ on classification and stroke contrast. Ratio 1.25. Captions in the sans at step −1, muted.

## Layout
Work is shown as test tiles: square images in a loose grid with wide gutters, a caption under each (name, then clay, glaze and firing in muted text). Pages run asymmetric: text in a narrow left column, tiles to the right; one tile per row on phones. Tiles cycle through three fixed radii (10, 14, 12 px) with `:nth-child(3n…)`, so the shelf looks hand-made but renders the same every time.

## Motion
Soft and short: tiles arrive on `--dur-enter` with `--ease-enter`; on hover the caption's glaze mark deepens over `--dur-small`. No springs, no lift-and-shadow.

## Texture
A clay grain from an SVG `feTurbulence` at 3–4% opacity on `--surface` only, never on raised cards or behind captions.

## Suits
Craft shops, studio and class booking, maker portfolios, food and recipe sites, slow-living products.
Not for: dense dashboards, developer tools, emergency information.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rn "backdrop-filter" src`: returns nothing; glaze is a solid colour, not glass.
- `grep -rnoE "border-radius:\s*[^;]+" src --include=*.css | sort -u`: the three tile radii, plus 0.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#2C251D", "#F0E6DB", 4.5), ("#2C251D", "#FCF2E7", 4.5), ("#5C544B", "#F0E6DB", 4.5),
                          ("#5C544B", "#FCF2E7", 4.5), ("#847C72", "#F0E6DB", 3), ("#265399", "#F0E6DB", 4.5),
                          ("#FFFFFF", "#265399", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Caption every piece like a test tile: its name, then materials and process in muted small text, under the image.

## Avoid
- Glossy glass, gradients or gradient blobs to suggest glaze: glaze is the solid cobalt, on one action per view.

## Review
- [ ] Every image of work has a caption with name and materials.
- [ ] Cobalt marks one action per view and nothing decorative.
- [ ] The grain sits on the page surface only.
