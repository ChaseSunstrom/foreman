---
name: look-shipping-manifest
title: "Look: Shipping manifest"
area: looks
tags: [look, style, palette, logistics, orders, tracking, inventory, forms]
detect: []
related: [look-archive-ledger, look-transit-signage, design-systems, typography, color-contrast]
---
A freight manifest on a kraft envelope: boxed fields with tiny capital labels, carbon-black ink, rubber stamps, perforated edges.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #E3D0B2 | 0.865 0.045 78 | page |
| `--raised` | #F4E0C2 | 0.915 0.045 78 | cards, popovers |
| `--text` | #1E1A13 | 0.22 0.014 78 | 11.5:1 on surface, 13.4:1 on raised |
| `--text-muted` | #4A4134 | 0.38 0.025 78 | 6.6:1 on surface, 7.8:1 on raised |
| `--border` | #6F5E43 | 0.49 0.045 78 | 4.1:1 on surface |
| `--accent` | #1E1A13 | 0.22 0.014 78 | 11.5:1 on surface |
| `--on-accent` | #F4E0C2 | 0.915 0.045 78 | 13.4:1 on accent |

The accent is the ink itself, achromatic, so it is far from every status hue and the status colours stand out. Because the accent is the text colour, links carry an underline and the primary action is a solid ink block.

## Type
One grotesk family with a width axis: condensed capitals for labels and headings, normal width for body; a mono for codes, weights and counts. They differ on classification and width. Labels at step −1, tracked +0.08em.

## Layout
Each record opens with a field grid: boxes with 2 px ink borders, a tiny capital label above each value (FROM, TO, REF, DATE). Line items follow in a table with quantity and weight right-aligned. A stamp (a word with an icon in an ink outline, rotated at most 4°) marks the record's stage at top-right. Sections are torn apart by a perforated edge.

## Motion
Mechanical and brief: a stamp lands on `--dur-small` (scale 1.04 to 1, opacity); rows arrive on `--dur-enter`; nothing else moves.

## Texture
The kraft is the colour; perforation from a dotted `radial-gradient` row between sections; radius 0.

## Suits
Logistics and order tracking, inventory and warehouses, procurement, ticketing, job and build manifests in developer tools.
Not for: luxury, wellness, children's apps, romance.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rn "text-decoration" src --include=*.css`: links keep their underline.
- `grep -rniE "font-family:[^;]*stencil" src`: returns nothing.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#1E1A13", "#E3D0B2", 4.5), ("#1E1A13", "#F4E0C2", 4.5), ("#4A4134", "#E3D0B2", 4.5),
                          ("#4A4134", "#F4E0C2", 4.5), ("#6F5E43", "#E3D0B2", 3), ("#F4E0C2", "#1E1A13", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Show a record's key fields in a boxed grid with tiny capital labels above the values, like a form someone filled in.

## Avoid
- A stencil typeface: the broken strokes cost legibility; caps, tracking and boxes give the feel.

## Review
- [ ] Every stamp carries a word and an icon, not colour alone.
- [ ] Links are underlined.
- [ ] Quantities and weights align on tabular figures.
