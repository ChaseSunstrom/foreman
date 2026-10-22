---
name: look-sewing-pattern
title: "Look: Sewing pattern"
area: looks
tags: [look, style, palette, tutorial, steps, instructions, diy, craft]
detect: []
related: [look-ceramic-studio, look-cartographer, design-systems, typography, color-contrast]
---
A dressmaker's pattern on tissue: dashed cutting lines, lettered pieces, numbered steps each keyed to its diagram.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #F5EEDE | 0.95 0.022 85 | page |
| `--sunken` | #E6DFD0 | 0.905 0.022 85 | wells, table heads |
| `--text` | #2B261A | 0.27 0.022 85 | 13.0:1 on surface, 11.3:1 on sunken |
| `--text-muted` | #5E574A | 0.46 0.022 85 | 6.2:1 on surface, 5.4:1 on sunken |
| `--border` | #867F72 | 0.6 0.022 85 | 3.4:1 on surface |
| `--accent` | #A2316E | 0.5 0.160 351 | 5.7:1 on surface |
| `--on-accent` | #FFFFFF | 1 0.000 85 | 6.6:1 on accent |
| `--hairline` | #A79D8A | 0.7 0.030 85 | cut lines; decorative, never a control's only edge |

Accent hue 351 (printed magenta), 36° from error red: keep it toward purple when adapting, never toward red.

## Type
Condensed grotesk in capitals for piece letters, step numbers and labels; humanist sans for instructions. They differ on classification and width. Step numbers at step 3 of the scale, 700.

## Layout
Instructions are numbered steps, each a pair: the diagram and its text side by side on wide screens, diagram first on phones. Parts are lettered (A, B, C) and the same letters label the diagram and the text. A materials table (the yardage chart) opens the page. Sections are cut apart by a dashed `--hairline` line with a small scissors icon at its start, marked `aria-hidden`.

## Motion
A finished step ticks over on `--dur-small`; moving to the next step scrolls and highlights it on `--dur-move` with `--ease-move`. No drawing or marching-ants effects.

## Texture
Dashed cut lines and notch triangles on section edges; the tissue colour is the surface. Radius 2 px.

## Suits
Tutorials and how-to guides, assembly instructions, onboarding checklists, DIY and craft kits, recipes with steps.
Not for: finance, emergency information, live data.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rn "dashed" src --include=*.css`: hits on dividers and diagrams only, none on input or button selectors.
- `grep -rn "<ol" src`: the steps are an ordered list, so their numbers reach assistive tech.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#2B261A", "#F5EEDE", 4.5), ("#2B261A", "#E6DFD0", 4.5), ("#5E574A", "#F5EEDE", 4.5),
                          ("#5E574A", "#E6DFD0", 4.5), ("#867F72", "#F5EEDE", 3), ("#A2316E", "#F5EEDE", 4.5),
                          ("#FFFFFF", "#A2316E", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Number each step and key it to its diagram with the same piece letters, so text and picture name the same parts.

## Avoid
- Dashed borders on controls: dashed means "cut here"; inputs and buttons keep a solid `--border` edge.

## Review
- [ ] Every step has a diagram, and its letters match the text.
- [ ] No control has a dashed edge.
- [ ] The materials list comes before step 1.
