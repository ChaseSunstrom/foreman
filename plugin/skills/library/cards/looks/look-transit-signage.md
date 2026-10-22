---
name: look-transit-signage
title: "Look: Transit signage"
area: looks
tags: [look, style, palette, wayfinding, signage, timetable, status-board]
detect: []
related: [look-lido, look-broadcast-graphics, design-systems, typography, color-contrast]
---
Platform wayfinding read at walking pace: dark enamel panels, one line colour, destination first, arrows that point.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #15191D | 0.21 0.010 250 | page |
| `--raised` | #1E2226 | 0.25 0.010 250 | cards, popovers |
| `--text` | #F0F6FC | 0.97 0.010 250 | 16.2:1 on surface, 14.7:1 on raised |
| `--text-muted` | #B9BEC4 | 0.8 0.010 250 | 9.4:1 on surface, 8.6:1 on raised |
| `--border` | #70757A | 0.56 0.010 250 | 3.8:1 on surface |
| `--accent` | #26BDAE | 0.72 0.120 185 | 7.5:1 on surface |
| `--on-accent` | #101418 | 0.19 0.010 250 | 7.9:1 on accent |

Dark first, so body text clears Foreman's 7:1 dark rule. Accent hue 185 (line teal), 35° from success green.

## Type
One neo-grotesk does everything: 600 for sign bands and destinations, 400 for detail, ratio 1.333, sentence case (capitals slow reading at a distance). Times, platforms and codes take tabular figures. A second family adds nothing here.

## Layout
A sign band heads each view: the destination word left at the largest size, the time right. Rows are at least 48 px, strictly left-aligned, each with a 6 px accent bar at its leading edge and a square code badge (accent fill, `--on-accent` text). Direction is drawn with real SVG arrows beside the label they point from.

## Motion
Rows update in place on `--dur-small` (colour, opacity); a new departure arrives on `--dur-enter`; a reorder runs on `--dur-move` with `--ease-move`. No flip-board animation and nothing that loops.

## Texture
Flat enamel: no gradients, no shadows. Panels square; only badges take a 4 px radius. A 1 px `--border` between bands.

## Suits
Route planners, departure and status boards, venue wayfinding, building directories, queue screens, ops boards read from across a room.
Not for: long-form reading, luxury, playful or children's products.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor, body text at 7:1.
- `grep -rn "tabular-nums" src`: on every time and platform column.
- `grep -rnE "(linear|radial)-gradient" src --include=*.css`: returns nothing; the enamel is flat.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#F0F6FC", "#15191D", 7), ("#F0F6FC", "#1E2226", 7), ("#B9BEC4", "#15191D", 4.5),
                          ("#B9BEC4", "#1E2226", 4.5), ("#70757A", "#15191D", 3), ("#26BDAE", "#15191D", 4.5),
                          ("#101418", "#26BDAE", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Put the most important word first and largest: destination, then time, then platform, then detail.

## Avoid
- A colour per route: one accent, with routes told apart by code badge and name (red and green lines would also collide with status).

## Review
- [ ] Times and platform numbers align on tabular figures.
- [ ] Every route has a code badge and a name; colour never tells two routes apart alone.
- [ ] Every arrow sits beside the label it belongs to and points the way the person goes.
