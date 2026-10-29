---
name: look-saltpan
title: "Look: Saltpan"
area: looks
tags: [look, style, palette, coastal, wellness, travel, hospitality, light]
detect: []
related: [look-lido, look-ceramic-studio, design-systems, typography, color-contrast]
---
A salt flat at dusk: a bleached pink-white ground, long flat horizons, slate-blue water as the one deep colour.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #FBF3F1 | 0.97 0.009 34 | page |
| `--sunken` | #EEE2DF | 0.921 0.014 34 | wells, table heads |
| `--text` | #2B2326 | 0.266 0.013 353 | 14.0:1 on surface, 12.1:1 on sunken |
| `--text-muted` | #665A5D | 0.48 0.016 1 | 6.0:1 on surface, 5.2:1 on sunken |
| `--border` | #8E8083 | 0.613 0.018 3 | 3.4:1 on surface |
| `--accent` | #2F5C86 | 0.463 0.085 249 | 6.4:1 on surface |
| `--on-accent` | #FFFFFF | 1 0.000 90 | 7.0:1 on accent |

The pale ground carries a trace of rose (chroma 0.012) so large areas feel warm; the blue is slate, not sky. Accent hue 249, 99° from the nearest status hue.

## Type
Humanist sans at 400 for body and 600 for headings; a wide geometric sans in capitals at 12 px, tracked +0.12em, for labels and eyebrows. Headings are sentence case. Line height 1.65.

## Layout
Horizontal bands of unequal height stacked like a horizon: a 40vh hero, thin bands for facts, then wide image strips (21:9). Text sits in a 60ch column offset to the left; the right is air. Cards are full-width rows, not tiles.

## Motion
Drift, not bounce: bands fade and rise 8 px on `--dur-enter` with `--ease-enter`, staggered by 60 ms at most; hover changes colour over `--dur-small`.

## Texture
A 1 px `--border` hairline between bands; image strips take a 2 px radius. No grain or gradient.

## Suits
Hospitality and travel, spas and retreats, coastal and desert regions, calm brochures, wellbeing and sleep products.
Not for: dense admin tools, alerts and incident pages, anything urgent.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rnE "aspect-ratio: *21 */ *9" src`: image strips declare it.
- `grep -rnE "stagger|delay" src --include=*.css`: no stagger above 60 ms.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#2B2326", "#FBF3F1", 4.5), ("#2B2326", "#EEE2DF", 4.5), ("#665A5D", "#FBF3F1", 4.5),
                          ("#665A5D", "#EEE2DF", 4.5), ("#8E8083", "#FBF3F1", 3), ("#2F5C86", "#FBF3F1", 4.5),
                          ("#FFFFFF", "#2F5C86", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Stack the page as horizontal bands of unequal height so the eye travels across it like a horizon.

## Avoid
- Wave, sand-dune or sun imagery: the flat bands are the landscape and pictures of it undercut them.

## Review
- [ ] No stagger exceeds 60 ms.
- [ ] Body text stays in a 60ch column.
- [ ] Every image strip keeps its 21:9 ratio.
