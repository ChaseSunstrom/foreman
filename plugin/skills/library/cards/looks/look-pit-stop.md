---
name: look-pit-stop
title: "Look: Pit stop"
area: looks
tags: [look, style, palette, racing, live, timing, sport, dark]
detect: []
related: [look-broadcast-graphics, look-transit-signage, design-systems, typography, color-contrast]
---
A timing screen on the pit wall: graphite panels, tight rows of numbers, one signal-blue marker for the car you are watching.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #0E0F12 | 0.169 0.006 271 | page |
| `--raised` | #181A1F | 0.218 0.010 268 | timing rows, panels |
| `--text` | #ECEDF0 | 0.946 0.004 271 | 16.4:1 on surface, 14.9:1 on raised |
| `--text-muted` | #A9ADB8 | 0.748 0.016 270 | 8.5:1 on surface, 7.8:1 on raised |
| `--border` | #656A76 | 0.524 0.020 268 | 3.5:1 on surface |
| `--accent` | #4DA3FF | 0.705 0.159 252 | 7.3:1 on surface |
| `--on-accent` | #0E0F12 | 0.169 0.006 271 | 7.3:1 on accent |

Dark first: body text clears Foreman's 7:1 dark rule. Blue is reserved for the followed car or the selected row; faster and slower use the up and down arrows with text, never a colour pair. Accent hue 252, 102° from the nearest status hue.

## Type
Mono at 500 for every number (13 px at least) on tabular figures; grotesk at 700 in capitals for driver and team codes. Gaps are signed (+0.312) and always show the sign.

## Layout
A leaderboard as dense 32 px rows: position, code, gap, last lap, sectors. The selected row takes a 4 px blue bar on its start edge and a `--raised` fill. A side panel with the selected car's lap chart sits to the right on wide screens and under the board on narrow ones.

## Motion
Fast and exact: a row that changes place slides to its new slot on `--dur-move` with `--ease-enter`; a new value flashes its background once on `--dur-tap`. Updates batch to one per second.

## Texture
None. Rows are separated by 1 px `--border`; panels take a 2 px radius.

## Suits
Live timing and scoring, motorsport and cycling, esports, trading-floor style boards, delivery fleet trackers.
Not for: long reading, onboarding, calm brochure pages.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rn "tabular-nums" src`: on every numeric cell.
- `grep -rnE "setInterval\([^)]*, *[0-9]{1,3}\)" src`: no update loop faster than 1 s.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#ECEDF0", "#0E0F12", 7), ("#ECEDF0", "#181A1F", 7), ("#A9ADB8", "#0E0F12", 4.5),
                          ("#A9ADB8", "#181A1F", 4.5), ("#656A76", "#0E0F12", 3), ("#4DA3FF", "#0E0F12", 4.5),
                          ("#0E0F12", "#4DA3FF", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Mark the followed row with the blue bar on its start edge and keep its gap and position readable without colour.

## Avoid
- Flashing every changed cell at once: a board where everything blinks tells the viewer nothing; flash only the cell that changed, once.

## Review
- [ ] Every numeric cell is mono on tabular figures.
- [ ] Gaps always show their sign.
- [ ] Reduced motion replaces row slides with a plain swap.
