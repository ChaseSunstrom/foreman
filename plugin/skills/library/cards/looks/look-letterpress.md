---
name: look-letterpress
title: "Look: Letterpress"
area: looks
tags: [look, style, palette, print, books, craft, publishing, light]
detect: []
related: [look-archive-ledger, look-card-catalogue, design-systems, typography, color-contrast]
---
A job off a hand press: heavy cotton stock, ink-black type pressed slightly into the page, one wine second-colour pass for rules and initials.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #F1EEE6 | 0.949 0.011 90 | page |
| `--sunken` | #E2DED2 | 0.9 0.017 92 | inset blocks |
| `--text` | #1A1F26 | 0.237 0.015 257 | 14.3:1 on surface, 12.3:1 on sunken |
| `--text-muted` | #4D535B | 0.44 0.015 256 | 6.7:1 on surface, 5.8:1 on sunken |
| `--border` | #80858B | 0.614 0.011 253 | 3.2:1 on surface |
| `--accent` | #8A1C58 | 0.431 0.154 353 | 7.6:1 on surface |
| `--on-accent` | #FFFFFF | 1 0.000 90 | 8.8:1 on accent |

Ink black is a blue-leaning near-black; wine is the second pass and is used for rules, drop caps and links only. Accent hue 353, 34° from the nearest status hue.

## Type
Transitional serif at 400 for body at 1.15rem and 1.6 line height; the same face at 700 for titles in small caps; a mono is not used. Drop cap on the first paragraph of a section (three lines tall, in wine). Figures are old-style.

## Layout
A single 34em column centred on the page, wide margins, running heads in small caps above a hairline. Footnotes sit at the foot of the column, not at the end. Ornaments are limited to a centred fleuron between sections (text, `aria-hidden`).

## Motion
Almost none: links underline over `--dur-tap`; a section scrolls in without animation. Reduced motion changes nothing because nothing moves.

## Texture
The impression: text takes a 0.4 px `text-shadow` in `--sunken` offset up and left, which reads as ink pressed into paper. Applied to headings and body only, never to controls.

## Suits
Long reading, essays and books online, press and publisher sites, invitations, poetry and zines for a calm audience.
Not for: data tables, dashboards, tools used all day.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rnE "max-width: *(3[0-9]|4[0-4])em" src --include=*.css`: the measure is declared.
- `grep -rnE "font-variant-numeric: *oldstyle" src --include=*.css`: body figures are old-style.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#1A1F26", "#F1EEE6", 4.5), ("#1A1F26", "#E2DED2", 4.5), ("#4D535B", "#F1EEE6", 4.5),
                          ("#4D535B", "#E2DED2", 4.5), ("#80858B", "#F1EEE6", 3), ("#8A1C58", "#F1EEE6", 4.5),
                          ("#FFFFFF", "#8A1C58", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Hold the measure at 34em and put footnotes at the foot of the column they belong to.

## Avoid
- A second typeface for emphasis: the one serif does it with italics and small caps, and a sans would read as a different job.

## Review
- [ ] The measure never exceeds 34em.
- [ ] Wine is used for rules, initials and links only.
- [ ] The impression shadow is off on controls.
