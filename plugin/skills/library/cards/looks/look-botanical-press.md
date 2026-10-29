---
name: look-botanical-press
title: "Look: Botanical press"
area: looks
tags: [look, style, palette, nature, herbarium, reference, collection, light]
detect: []
related: [look-lab-notebook, look-card-catalogue, design-systems, typography, color-contrast]
---
A pressed-flower herbarium sheet: cream paper, one specimen mounted per page, a typed label in the corner, olive ink for the rules.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #F6F1E4 | 0.958 0.018 89 | page |
| `--sunken` | #E8E1CF | 0.91 0.025 89 | specimen cards, wells |
| `--text` | #2A2A1F | 0.281 0.019 108 | 12.8:1 on surface, 11.1:1 on sunken |
| `--text-muted` | #5A5846 | 0.457 0.028 102 | 6.4:1 on surface, 5.5:1 on sunken |
| `--border` | #8A8670 | 0.617 0.032 99 | 3.3:1 on surface |
| `--accent` | #5E6B1E | 0.501 0.101 119 | 5.2:1 on surface |
| `--on-accent` | #FFFFFF | 1 0.000 90 | 5.8:1 on accent |

Olive is a dark, low-chroma green-yellow, well clear of the success green; it reads as plant ink, not as a status. Accent hue 119, 31° from the nearest status hue.

## Type
Old-style serif at 400 for body and 400 italic for Latin names; small caps at 600 tracked +0.08em for labels. The label block uses a mono at 12 px. Latin names are always italic.

## Layout
Each item is a sheet: the picture takes two thirds of the width, a typed label (mono, boxed with a 1 px `--accent` rule) sits bottom right with accession number, place and date. Lists are rows of sheets on a 3-column grid with a 24 px gutter.

## Motion
Slow and papery: a sheet lifts 2 px on hover over `--dur-small`; a page turn between sheets is a 12 px slide on `--dur-move`. Nothing bounces.

## Texture
A faint paper fibre (an SVG noise at 4% opacity) on the page only, never behind text; the specimen photo casts a 1 px inner edge, no drop shadow.

## Suits
Collections and catalogues of living things, seed libraries, field notes, museum and garden sites, recipe archives.
Not for: real-time dashboards, high-speed workflows, anything that must feel technical.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rniE "font-style: *italic" src --include=*.css`: the Latin-name class carries it.
- `grep -rn "box-shadow" src --include=*.css`: returns nothing.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#2A2A1F", "#F6F1E4", 4.5), ("#2A2A1F", "#E8E1CF", 4.5), ("#5A5846", "#F6F1E4", 4.5),
                          ("#5A5846", "#E8E1CF", 4.5), ("#8A8670", "#F6F1E4", 3), ("#5E6B1E", "#F6F1E4", 4.5),
                          ("#FFFFFF", "#5E6B1E", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Give every item a boxed typed label with accession number, place and date, in mono at 12 px.

## Avoid
- Leaf, vine or flower ornaments around the content: the specimen is the picture; the frame stays plain.

## Review
- [ ] Latin names are italic everywhere they appear.
- [ ] The paper noise sits under no text.
- [ ] Every sheet shows its label block.
