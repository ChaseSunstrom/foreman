---
name: look-observatory
title: "Look: Observatory"
area: looks
tags: [look, style, palette, science, astronomy, monitoring, data, dark]
detect: []
related: [look-cartographer, look-night-market, design-systems, typography, color-contrast]
---
A star atlas beside an observing log: deep blue-black, pale cyan reticles, coordinates in mono, a still field of view.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #0C1220 | 0.185 0.030 265 | page |
| `--raised` | #161D2B | 0.23 0.030 265 | cards, popovers |
| `--text` | #E9EDF5 | 0.945 0.012 265 | 15.9:1 on surface, 14.4:1 on raised |
| `--text-muted` | #ABB4C8 | 0.77 0.030 265 | 9.0:1 on surface, 8.1:1 on raised |
| `--border` | #636C7E | 0.53 0.030 265 | 3.5:1 on surface |
| `--accent` | #8FD0E1 | 0.82 0.070 215 | 10.9:1 on surface |
| `--on-accent` | #0C1220 | 0.185 0.030 265 | 10.9:1 on accent |

Dark first: body text clears Foreman's 7:1 dark rule. Accent hue 215, 65° from the nearest status hue, at chroma 0.07 so it reads as starlight, not neon.

## Type
Geometric sans for headings and body (400 and 600; nothing thinner on dark); mono for coordinates, times and magnitudes. They differ on classification and width. Ratio 1.25.

## Layout
The key view sits in a field of view: a round or square frame with reticle ticks and a scale, coordinates in mono beside it. A log runs alongside: timestamped entries, newest first. Wide dark margins; the data never crowds the frame.

## Motion
Panning the view on `--dur-move` with `--ease-move`; readings update on `--dur-small`. One `--dur-stage` moment per view: the field resolves when it first loads. Nothing twinkles.

## Texture
A sparse, static star field (tiny radial-gradient dots at 20–40% opacity) on the page background only; reticle hairlines in `--border`.

## Suits
Astronomy and space data, science dashboards, night-shift monitoring, sleep and time apps, network maps, research instruments.
Not for: bright retail, children's apps, print-first documents.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor, body text at 7:1.
- `grep -rnE "@keyframes[^{]*(twinkle|drift|float)" src`: returns nothing.
- `grep -rnE "font-weight:\s*[1-3]00" src --include=*.css`: returns nothing; thin weights bleed on dark.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#E9EDF5", "#0C1220", 7), ("#E9EDF5", "#161D2B", 7), ("#ABB4C8", "#0C1220", 4.5),
                          ("#ABB4C8", "#161D2B", 4.5), ("#636C7E", "#0C1220", 3), ("#8FD0E1", "#0C1220", 4.5),
                          ("#0C1220", "#8FD0E1", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Frame the key view with a reticle: thin crosshair ticks and a scale, its coordinates in mono beside it.

## Avoid
- Twinkling or drifting stars: motion with no cause that pulls the eye from the data; the field is still.

## Review
- [ ] Every reading shows its unit and time.
- [ ] The star field never sits behind text.
- [ ] Reduced motion leaves the stage moment as a fade.
