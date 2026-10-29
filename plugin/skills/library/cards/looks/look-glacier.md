---
name: look-glacier
title: "Look: Glacier"
area: looks
tags: [look, style, palette, climate, monitoring, outdoors, data, dark]
detect: []
related: [look-observatory, look-cartographer, design-systems, typography, color-contrast]
---
A field station on the ice: blue-black slate, cold grey text, one meltwater-cyan accent, long quiet charts.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #0B1117 | 0.174 0.016 249 | page |
| `--raised` | #141C24 | 0.222 0.020 249 | cards, popovers |
| `--text` | #E8EFF5 | 0.949 0.011 244 | 16.4:1 on surface, 14.8:1 on raised |
| `--text-muted` | #A9B8C6 | 0.775 0.026 246 | 9.4:1 on surface, 8.5:1 on raised |
| `--border` | #617080 | 0.539 0.031 250 | 3.7:1 on surface |
| `--accent` | #86D4D6 | 0.82 0.077 198 | 11.2:1 on surface |
| `--on-accent` | #0B1117 | 0.174 0.016 249 | 11.2:1 on accent |

Dark first: body text clears Foreman's 7:1 dark rule. Cyan sits at chroma 0.08, a pale meltwater that reads cold without glowing. Accent hue 198, 48° from the nearest status hue.

## Type
Neo-grotesk at 400 and 600 for body and headings; mono at 12 px for sensor ids and coordinates. Readings are large (2rem, 300 weight) with the unit small and muted beside them.

## Layout
A 12-column dashboard of wide, short charts rather than tall tiles: each chart spans 8 columns with a 4-column readout beside it. Time runs left to right on every chart and shares one x-axis per row. Station names head each row in small caps.

## Motion
Long and quiet: a chart draws its line once on `--dur-stage` with `--ease-enter`; a new reading replaces the old on `--dur-small`. Nothing loops or pulses.

## Texture
A fine 1 px horizontal grid at 6% `--text` behind charts; no texture elsewhere. Cards take a 4 px radius.

## Suits
Climate and weather data, sensor networks, outdoor and expedition logs, energy and water monitoring, long-running research dashboards.
Not for: consumer checkouts, kids' products, marketing sites that need warmth.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rniE "pulse|blink|infinite" src --include=*.css`: returns nothing.
- `grep -rn "tabular-nums" src`: on every reading.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#E8EFF5", "#0B1117", 7), ("#E8EFF5", "#141C24", 7), ("#A9B8C6", "#0B1117", 4.5),
                          ("#A9B8C6", "#141C24", 4.5), ("#617080", "#0B1117", 3), ("#86D4D6", "#0B1117", 4.5),
                          ("#0B1117", "#86D4D6", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- State each reading with its unit, station and time in the readout beside the chart.

## Avoid
- Snowflake, ice-crystal or aurora imagery: the cold comes from the slate and the long charts, and pictures of ice date the page.

## Review
- [ ] Every reading shows unit, station and time.
- [ ] Charts in a row share one x-axis.
- [ ] Reduced motion draws the line at once.
