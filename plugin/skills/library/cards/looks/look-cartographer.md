---
name: look-cartographer
title: "Look: Cartographer"
area: looks
tags: [look, style, palette, map, legend, geography, outdoor, travel]
detect: []
related: [look-observatory, look-sewing-pattern, design-systems, typography, color-contrast]
---
A survey map sheet: cream paper, contour hairlines, a boxed legend, a scale bar and grid references on the frame.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #F2EFE0 | 0.95 0.020 95 | page |
| `--sunken` | #E5E1D3 | 0.91 0.020 95 | wells, table heads |
| `--text` | #2C291E | 0.28 0.020 95 | 12.6:1 on surface, 11.1:1 on sunken |
| `--text-muted` | #5E5B4E | 0.47 0.020 95 | 5.9:1 on surface, 5.2:1 on sunken |
| `--border` | #817D70 | 0.59 0.020 95 | 3.6:1 on surface |
| `--accent` | #1C688B | 0.49 0.090 233 | 5.3:1 on surface |
| `--on-accent` | #FFFFFF | 1 0.000 95 | 6.2:1 on accent |
| `--hairline` | #D1C3A0 | 0.82 0.050 90 | contours; decorative, never a control's only edge |

Accent hue 233 (water), 83° from the nearest status hue.

## Type
Humanist sans for interface and body; a transitional serif in italic for named things (places, projects, people), the way maps letter water and features. They differ on classification and stroke contrast. Section labels in the sans, small and tracked +0.08em in capitals.

## Layout
The view is a sheet inside a neat line: a 1 px frame, a 4 px gap, a second 1 px frame. Grid references (A–H across, 1–8 down) run along the frame edges and double as anchors. Every chart or diagram has a boxed legend in a corner and a scale bar beneath. Details open as insets: a bordered box with a leader line to what it enlarges.

## Motion
Panning and zooming insets on `--dur-move` with `--ease-move`; tooltips arrive on `--dur-enter`. No parallax, no scroll-linked effects.

## Texture
Contour lines in `--hairline`, as a static SVG behind the header and empty margins only. Radius 0 throughout.

## Suits
Outdoor and trail apps, travel itineraries, property and land, field research, logistics regions, roadmaps drawn as terrain.
Not for: trading floors, children's apps, nightlife.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rln "legend" src/components`: each chart component appears.
- `grep -rnE "border-radius:\s*[1-9]" src --include=*.css`: returns nothing; the sheet is square.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#2C291E", "#F2EFE0", 4.5), ("#2C291E", "#E5E1D3", 4.5), ("#5E5B4E", "#F2EFE0", 4.5),
                          ("#5E5B4E", "#E5E1D3", 4.5), ("#817D70", "#F2EFE0", 3), ("#1C688B", "#F2EFE0", 4.5),
                          ("#FFFFFF", "#1C688B", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Give every visual a legend and a scale: symbols keyed in a boxed legend, a distance or time bar beneath.

## Avoid
- Contours behind body text: they lower the effective contrast; keep them to headers and empty margins.

## Review
- [ ] Every chart has a legend and a scale bar.
- [ ] Named things, and only named things, are set in the serif italic.
- [ ] Contour texture never sits behind a paragraph.
