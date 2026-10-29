---
name: look-swiss-poster
title: "Look: Swiss poster"
area: looks
tags: [look, style, palette, grid, editorial, cultural, light]
detect: []
related: [look-card-catalogue, look-archive-ledger, design-systems, typography, color-contrast]
---
An exhibition poster from Zurich: an off-white sheet, one flush-left column of black type, one cobalt block, a visible 12-column grid.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #F4F2EE | 0.962 0.006 85 | page |
| `--sunken` | #E6E3DC | 0.916 0.010 87 | wells, table heads |
| `--text` | #111111 | 0.178 0.000 90 | 16.9:1 on surface, 14.7:1 on sunken |
| `--text-muted` | #4F4D49 | 0.421 0.007 85 | 7.5:1 on surface, 6.6:1 on sunken |
| `--border` | #85817A | 0.605 0.011 82 | 3.5:1 on surface |
| `--accent` | #0B5CAD | 0.478 0.147 254 | 6.0:1 on surface |
| `--on-accent` | #FFFFFF | 1 0.000 90 | 6.7:1 on accent |

Black on warm paper at near-maximum contrast; cobalt appears once per screen, as a block or a rule, never as scattered links. Accent hue 254, 104° from the nearest status hue.

## Type
Neo-grotesk at 700 for headings set tight (line height 1.05) and flush left, ragged right; the same family at 400 for body. One family, two weights; hierarchy comes from size steps of 1.5x, not from a second face. Numbers on tabular figures.

## Layout
A 12-column grid with a 24 px gutter; text sits on columns 1-7 and the rest stays empty on purpose. Headings hang in the left margin. One cobalt rectangle per view, aligned to the grid, carries the primary action or the one fact that matters.

## Motion
Hard and brief: elements arrive on `--dur-enter` with `--ease-enter` by sliding along a grid line, no fades. Hover moves a 2 px cobalt rule under the item over `--dur-small`.

## Texture
None. Flat fills, 1 px `--border` rules, square corners (radius 0).

## Suits
Cultural programmes, festival and exhibition sites, studios and portfolios, annual reports, editorial landing pages.
Not for: dense data tools, anything with many controls on one screen, children's products.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rnE "border-radius: *[1-9]|box-shadow" src --include=*.css`: returns nothing.
- `grep -rn "grid-template-columns: *repeat(12" src`: the page grid is declared once.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#111111", "#F4F2EE", 4.5), ("#111111", "#E6E3DC", 4.5), ("#4F4D49", "#F4F2EE", 4.5),
                          ("#4F4D49", "#E6E3DC", 4.5), ("#85817A", "#F4F2EE", 3), ("#0B5CAD", "#F4F2EE", 4.5),
                          ("#FFFFFF", "#0B5CAD", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Leave columns 8-12 empty beside body text and let one cobalt block carry the page's single action.

## Avoid
- Rounded corners, shadows and gradients: they break the sheet into cards and the poster into an app.

## Review
- [ ] Cobalt fills at most one block per view.
- [ ] Text never runs wider than seven columns.
- [ ] Every heading is flush left on a grid line.
