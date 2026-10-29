---
name: look-darkroom
title: "Look: Darkroom"
area: looks
tags: [look, style, palette, photo, imaging, tools, dark]
detect: []
related: [look-observatory, look-night-market, design-systems, typography, color-contrast]
---
A photographic darkroom: near-black walls with a red cast, the image the only bright thing, one pale-yellow stop-bath accent for the controls.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #120B0B | 0.159 0.012 19 | page |
| `--raised` | #1D1313 | 0.2 0.017 19 | panels, dialogs |
| `--text` | #F0E4E0 | 0.927 0.014 39 | 15.7:1 on surface, 14.6:1 on raised |
| `--text-muted` | #BBA59F | 0.739 0.027 36 | 8.3:1 on surface, 7.8:1 on raised |
| `--border` | #7A6560 | 0.526 0.028 34 | 3.6:1 on surface |
| `--accent` | #D4D06F | 0.841 0.120 107 | 12.1:1 on surface |
| `--on-accent` | #120B0B | 0.159 0.012 19 | 12.1:1 on accent |

Dark first: body text clears Foreman's 7:1 dark rule. The surface leans warm so a photograph's neutrals stay neutral beside it; the accent is a dull chartreuse, never a glowing one. Accent hue 107, 42° from the nearest status hue.

## Type
Humanist sans at 400 for labels and body, 600 for panel titles; a mono for exposure values (f-stop, shutter, ISO, 12 px at least) with tabular figures. Small caps tracked +0.06em for panel names.

## Layout
The image fills the centre and nothing overlaps it. Controls live in two narrow rails left and right; each is a stack of panels with a title row and a hairline. Histograms and readouts sit in the right rail, aligned to a 4 px baseline.

## Motion
Near still: sliders respond at once; panels collapse on `--dur-small`, and an image change cross-fades on `--dur-stage` with `--ease-enter`. Nothing animates while the user is dragging.

## Texture
None on the chrome; the photograph supplies all texture. Panels take a 2 px radius and a 1 px `--border`.

## Suits
Photo and video editors, galleries of work, scanners and cameras, colour tools, image review queues.
Not for: text-heavy reading, finance, kids' products.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rnE "#(fff|ffffff)\b" src --include=*.css`: pure white appears only on the image canvas, if at all.
- `grep -rniE "glow|neon" src --include=*.css`: returns nothing.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#F0E4E0", "#120B0B", 7), ("#F0E4E0", "#1D1313", 7), ("#BBA59F", "#120B0B", 4.5),
                          ("#BBA59F", "#1D1313", 4.5), ("#7A6560", "#120B0B", 3), ("#D4D06F", "#120B0B", 4.5),
                          ("#120B0B", "#D4D06F", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Keep the chrome darker than the darkest tone in the image so the picture, not the interface, is the brightest thing.

## Avoid
- Red safelight theming (red text or red panels): it fails the status-colour rule and tints the photograph the user is judging.

## Review
- [ ] No chrome element is brighter than the image.
- [ ] Exposure values are in mono on tabular figures.
- [ ] A dragged slider updates the image on the same frame.
