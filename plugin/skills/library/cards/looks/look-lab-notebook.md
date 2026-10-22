---
name: look-lab-notebook
title: "Look: Lab notebook"
area: looks
tags: [look, style, palette, notebook, research, log, journal]
detect: []
related: [look-archive-ledger, look-card-catalogue, design-systems, typography, color-contrast]
---
A bound, quad-ruled lab notebook: dated entries in ballpoint blue on cool paper, numbered pages, nothing erased.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #F1F8FD | 0.975 0.010 240 | page |
| `--sunken` | #E5ECF1 | 0.94 0.010 240 | wells, table heads |
| `--text` | #202528 | 0.26 0.010 240 | 14.4:1 on surface, 13.0:1 on sunken |
| `--text-muted` | #565C60 | 0.47 0.010 240 | 6.3:1 on surface, 5.7:1 on sunken |
| `--border` | #7B8186 | 0.6 0.010 240 | 3.7:1 on surface |
| `--accent` | #1C508D | 0.43 0.115 255 | 7.6:1 on surface |
| `--on-accent` | #FFFFFF | 1 0.000 240 | 8.1:1 on accent |
| `--hairline` | #BFD6D6 | 0.86 0.025 195 | the grid; decorative, never a control's only edge |

Accent hue 255 (ballpoint), 105° from the nearest status hue.

## Type
Humanist sans for body and headings (400 and 600, ratio 1.25); mono for dates, entry numbers, sample IDs and measurements, with tabular figures. They differ on classification and width. No handwriting face: the blue ink is the hand.

## Layout
Each record is a dated entry. A margin column of about 10ch carries the mono date and running entry number; the content column stays under 68ch. Entries end with a muted "recorded by" line and a 1 px rule. Figures and pasted output sit in `--sunken` boxes with a 1 px `--border`, like a printout taped in.

## Motion
Functional only: state changes on `--dur-small` with `--ease-move`; a new entry arrives on `--dur-enter` (opacity and 2 px). No `--dur-stage` moment.

## Texture
A 1.25rem quad grid in `--hairline`, two `repeating-linear-gradient`s on the page background only; entries sit on solid `--surface`. Radius 2 px, no shadows.

## Suits
Experiment logs, research tools, electronic lab notebooks, incident timelines, dev diaries, changelogs.
Not for: luxury retail, children's apps, glamour launches, grief or care products.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rniE "font-family:[^;]*(cursive|script|hand)" src`: returns nothing.
- `grep -rnE "box-shadow:\s*[^n;]" src --include=*.css`: returns nothing; the notebook is flat.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#202528", "#F1F8FD", 4.5), ("#202528", "#E5ECF1", 4.5), ("#565C60", "#F1F8FD", 4.5),
                          ("#565C60", "#E5ECF1", 4.5), ("#7B8186", "#F1F8FD", 3), ("#1C508D", "#F1F8FD", 4.5),
                          ("#FFFFFF", "#1C508D", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Stamp every entry with a mono date and running number in the margin, so the page reads as a chronological record.

## Avoid
- Handwriting or script fonts to fake the pen: they cost legibility and read as a costume.

## Review
- [ ] Every entry shows its date and number in the margin column.
- [ ] The grid stays on the page background; body text sits on solid `--surface`.
- [ ] With the name hidden, the screen reads as a notebook page, not a dashboard.
