---
name: look-darkroom
title: "Look: Darkroom"
area: looks
tags: [look, style, palette, photo, imaging, tools, dark]
detect: []
related: [look-observatory, look-night-market, design-systems, typography, color-contrast]
---
A photographic darkroom: neutral grey-black walls, the image the only bright thing, one warm enlarger-light accent for the controls.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #111111 | 0.178 0.000 90 | page |
| `--raised` | #1B1B1B | 0.222 0.000 90 | panels, dialogs |
| `--text` | #EDEDED | 0.946 0.000 90 | 16.1:1 on surface, 14.7:1 on raised |
| `--text-muted` | #AFAFAF | 0.754 0.000 90 | 8.6:1 on surface, 7.9:1 on raised |
| `--border` | #6E6E6E | 0.538 0.000 90 | 3.7:1 on surface |
| `--accent` | #E9E1D0 | 0.911 0.024 86 | 14.5:1 on surface |
| `--on-accent` | #111111 | 0.178 0.000 90 | 14.5:1 on accent |

Dark first: body text clears Foreman's 7:1 dark rule. The wall is a true neutral so a photograph's colours read unshifted beside it; the accent is a warm off-white (chroma 0.024), a lamp, not a colour. Accent hue 86, 21° from the nearest status hue.

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
    for fg, bg, floor in [("#EDEDED", "#111111", 7), ("#EDEDED", "#1B1B1B", 7), ("#AFAFAF", "#111111", 4.5),
                          ("#AFAFAF", "#1B1B1B", 4.5), ("#6E6E6E", "#111111", 3), ("#E9E1D0", "#111111", 4.5),
                          ("#111111", "#E9E1D0", 4.5)]:
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
