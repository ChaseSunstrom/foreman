---
name: look-broadcast-graphics
title: "Look: Broadcast graphics"
area: looks
tags: [look, style, palette, live, scores, results, ticker, events]
detect: []
related: [look-transit-signage, look-observatory, design-systems, typography, color-contrast]
---
Live television graphics: dark straps with a lime tab, a ticker that pauses, score bugs in the corner, names read in a second.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #EDF0F6 | 0.955 0.008 255 | page |
| `--strap` | #16191C | 0.21 0.008 255 | lower-third straps, ticker |
| `--text` | #16191C | 0.21 0.008 255 | 15.5:1 on surface |
| `--text-muted` | #4D5054 | 0.43 0.008 255 | 7.1:1 on surface |
| `--on-strap` | #F3F7FC | 0.975 0.008 255 | 16.4:1 on strap |
| `--border` | #777B7F | 0.58 0.008 255 | 3.7:1 on surface |
| `--accent` | #C8D72A | 0.84 0.180 115 | 11.1:1 on strap |
| `--on-accent` | #16191C | 0.21 0.008 255 | 11.1:1 on accent |

Accent hue 115 (lime), 35° from success green and 50° from warning amber. On the light page it measures 1.4:1, so it lives on straps and as a fill under dark text; the focus ring on the page is `--text`.

## Type
Condensed grotesk at 700 for straps, names and scores; humanist sans at 400 for body. They differ on classification and width. Scores and clocks take tabular figures.

## Layout
Section heads are straps: a dark band, a 4 px lime tab at its leading edge holding the category, the title in condensed caps beside it. Over media, a lower third: name on the first line, role or score on the second. Live updates run in a one-line ticker with a visible pause button; a score bug sits top-right of the view it belongs to.

## Motion
Straps wipe in with `clip-path` on `--dur-enter` and `--ease-enter`, and out on `--dur-exit`. A changed score flashes lime behind the number once, on `--dur-small`. The ticker scrolls only without reduced motion, and pauses on hover, focus and its button.

## Texture
Flat and hard-edged: radius 0, no shadows, no gloss. The lime tab is the only colour.

## Suits
Live scores, results nights, event schedules, stream overlays, newsroom tools, conference programmes.
Not for: calm reading, healthcare, meditation, archives.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rnE "animation-play-state|aria-live" src`: the ticker pauses, and its updates are announced politely.
- `grep -rnE "color:\s*var\(--accent\)" src --include=*.css`: each hit sits under a strap selector.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#16191C", "#EDF0F6", 4.5), ("#4D5054", "#EDF0F6", 4.5), ("#F3F7FC", "#16191C", 4.5),
                          ("#777B7F", "#EDF0F6", 3), ("#C8D72A", "#16191C", 4.5), ("#16191C", "#C8D72A", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Lead with the strap: the name in condensed 700, the role or score beneath in body type, the lime tab at the edge.

## Avoid
- Lime as text or a link on the light page: it measures 1.4:1 there; page links use `--text` and an underline.

## Review
- [ ] The ticker has a pause control and stops under reduced motion.
- [ ] Lime appears only on straps and as fills under dark text.
- [ ] Scores and clocks are on tabular figures.
