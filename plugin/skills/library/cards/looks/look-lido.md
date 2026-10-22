---
name: look-lido
title: "Look: Lido"
area: looks
tags: [look, style, palette, booking, timetable, leisure, sport, friendly]
detect: []
related: [look-transit-signage, look-ceramic-studio, design-systems, typography, color-contrast]
---
An open-air public pool: white tiles, lane ropes, big painted depth numbers, a timetable you can read from the water.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #F0F9FA | 0.975 0.010 210 | page |
| `--sunken` | #E2EBED | 0.935 0.010 210 | wells, table heads |
| `--text` | #262D2E | 0.29 0.010 210 | 13.1:1 on surface, 11.6:1 on sunken |
| `--text-muted` | #555C5E | 0.47 0.010 210 | 6.4:1 on surface, 5.6:1 on sunken |
| `--border` | #808889 | 0.62 0.010 210 | 3.4:1 on surface |
| `--accent` | #076E87 | 0.5 0.090 221 | 5.5:1 on surface |
| `--on-accent` | #FFFFFF | 1 0.000 210 | 5.9:1 on accent |

Accent hue 221 (deep-end blue), 71° from the nearest status hue.

## Type
Geometric sans at 700 for section numbers and headings, like painted depth markings; humanist sans at 400 for body. They differ on classification and width (round and wide against narrow and open). Times and slots on tabular figures.

## Layout
Content runs in lanes: full-width bands separated by a lane-rope divider (a dotted row alternating accent and `--border` dots, `aria-hidden`). Each section starts with a big numeral at the lane's start and its label beside it. Timetables are lanes too: one row per lane, bookable slots as tiles along it, 44 px tall at least.

## Motion
Clear and calm: slots select on `--dur-small`; a booking panel arrives on `--dur-enter` with `--ease-enter` and leaves on `--dur-exit`. No ripples.

## Texture
A tile grid (1 px `--sunken` lines every 1.5rem) on hero panels only; tiles and slots take a 6 px radius.

## Suits
Leisure and class booking, pools, gyms and sports clubs, public services with a friendly voice, summer events, activity booking for parents.
Not for: finance, legal, nightlife, enterprise analytics.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rniE "ripple|caustic|wave" src --include=*.css --include=*.svg`: returns nothing.
- `grep -rn "tabular-nums" src`: on the timetable.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#262D2E", "#F0F9FA", 4.5), ("#262D2E", "#E2EBED", 4.5), ("#555C5E", "#F0F9FA", 4.5),
                          ("#555C5E", "#E2EBED", 4.5), ("#808889", "#F0F9FA", 3), ("#076E87", "#F0F9FA", 4.5),
                          ("#FFFFFF", "#076E87", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Number each section like a depth marking: a big geometric numeral at the lane's start, its label beside it.

## Avoid
- Water effects (ripples, caustics, wave dividers): the tiles and lanes carry the look; water is a costume.

## Review
- [ ] Every bookable slot is at least 44 px tall and shows its time.
- [ ] The tile grid stays on hero panels.
- [ ] Section numerals are real text, not images.
