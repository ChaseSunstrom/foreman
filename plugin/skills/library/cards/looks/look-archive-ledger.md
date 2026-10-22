---
name: look-archive-ledger
title: "Look: Archive ledger"
area: looks
tags: [look, style, palette, ledger, accounts, records, table, bookkeeping]
detect: []
related: [look-lab-notebook, look-card-catalogue, design-systems, typography, color-contrast]
---
A bound account book: buff paper, blue ruling, amounts in columns, totals under a double rule, losses in parentheses.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #F1EBDB | 0.94 0.022 88 | page |
| `--sunken` | #E4DECE | 0.9 0.022 88 | wells, table heads |
| `--text` | #241F13 | 0.24 0.022 88 | 13.8:1 on surface, 12.2:1 on sunken |
| `--text-muted` | #5A5548 | 0.45 0.022 88 | 6.2:1 on surface, 5.5:1 on sunken |
| `--border` | #837D6F | 0.59 0.022 88 | 3.4:1 on surface |
| `--accent` | #2A497D | 0.41 0.095 260 | 7.5:1 on surface |
| `--on-accent` | #FFFFFF | 1 0.000 88 | 8.9:1 on accent |
| `--hairline` | #A9B8D2 | 0.78 0.040 260 | ruling; decorative, never a control's only edge |

Accent hue 260 (registry ink), 110° from the nearest status hue.

## Type
Transitional serif for headings and descriptions (400 and 600); mono for amounts, dates and references. They differ on classification and stroke contrast. Every figure is tabular and right-aligned.

## Layout
The table is the page. Rows sit on blue ruling (`--hairline` bottom borders) at body line height; vertical hairlines divide the columns; money columns align right with a running-balance column last. Totals sit under a `3px double` rule. Period headings run like folios: the period at the top outer corner, the page number beside it. The selected row takes `--sunken`.

## Motion
Almost none: row highlight on `--dur-small`; a new entry fades in on `--dur-enter`, opacity only, no slide.

## Texture
The ruling and the buff paper are the texture; no grain, no shadows, radius 0.

## Suits
Bookkeeping, inventory, records management, archives and genealogy, audit logs, small-business admin.
Not for: social apps, playful products, image-led galleries.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rn "tabular-nums" src`: on every amount column.
- `grep -rnE "3px double|border-top-style:\s*double" src --include=*.css`: the totals rows.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#241F13", "#F1EBDB", 4.5), ("#241F13", "#E4DECE", 4.5), ("#5A5548", "#F1EBDB", 4.5),
                          ("#5A5548", "#E4DECE", 4.5), ("#837D6F", "#F1EBDB", 3), ("#2A497D", "#F1EBDB", 4.5),
                          ("#FFFFFF", "#2A497D", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Write negatives in parentheses, (1,250.00), right-aligned on tabular figures: a loss is not an error, and red is kept for errors.

## Avoid
- Zebra stripes on top of the ruling: two systems doing one job; keep the ruling.

## Review
- [ ] Amounts align on the decimal point in every column.
- [ ] No amount is red; negatives use parentheses.
- [ ] Totals sit under a double rule.
