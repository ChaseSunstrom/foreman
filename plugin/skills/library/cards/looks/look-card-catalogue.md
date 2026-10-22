---
name: look-card-catalogue
title: "Look: Card catalogue"
area: looks
tags: [look, style, palette, catalogue, search, collection, records, index]
detect: []
related: [look-archive-ledger, look-lab-notebook, design-systems, typography, color-contrast]
---
A library card drawer: typed index cards on card stock, call numbers first, alphabet tabs, "see also" lines between records.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #FAF7EE | 0.975 0.012 90 | page |
| `--sunken` | #E4E1D8 | 0.91 0.012 90 | wells, table heads |
| `--text` | #1F1D17 | 0.23 0.012 90 | 15.7:1 on surface, 12.9:1 on sunken |
| `--text-muted` | #58554E | 0.45 0.012 90 | 6.9:1 on surface, 5.7:1 on sunken |
| `--border` | #86837B | 0.61 0.012 90 | 3.5:1 on surface |
| `--accent` | #1A6976 | 0.48 0.075 212 | 5.9:1 on surface |
| `--on-accent` | #FFFFFF | 1 0.000 90 | 6.3:1 on accent |

Accent hue 212 (stamp-pad teal), 62° from the nearest status hue.

## Type
Mono for the card fields (call number, heading, author line, dates), like a typewriter; transitional serif for any description longer than two lines. They differ on classification and stroke contrast. Weights 400 and 700 only.

## Layout
Results are index cards (`--surface`) on a drawer (`--sunken`): call number top-left, subject heading top-right in small tracked capitals, then title and author lines. A teal top rule marks each card. Navigation is a row of alphabet tabs (A–C, D–F…) like drawer labels. Related records end in "see also" lines that link onward. Cards grow with their content; no fixed heights.

## Motion
The drawer opens on `--dur-move` with `--ease-move`; cards arrive on `--dur-enter`; a selected card lifts 2 px on `--dur-small`. No 3D flips.

## Texture
Card stock against a darker drawer, a 3 px radius on cards, one hairline shadow (0 1px 0) at each card's lower edge.

## Suits
Search results, catalogues and collections, CRMs, bookmarks, reading lists, knowledge bases, museum collection databases.
Not for: chart-heavy dashboards, games, fitness.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rnE "rotate[XY]\(|backface-visibility" src --include=*.css`: returns nothing; no card flips.
- `grep -rnE "(^|[^-])(max-)?height:\s*[0-9.]+(px|rem)" src --include=*.css`: no hit on a card selector (min-height is fine).

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#1F1D17", "#FAF7EE", 4.5), ("#1F1D17", "#E4E1D8", 4.5), ("#58554E", "#FAF7EE", 4.5),
                          ("#58554E", "#E4E1D8", 4.5), ("#86837B", "#FAF7EE", 3), ("#1A6976", "#FAF7EE", 4.5),
                          ("#FFFFFF", "#1A6976", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Lead each record with its call number or ID in mono at top-left, so cards scan by code before title.

## Avoid
- The classic red heading rule on index cards: red is reserved for errors; the rule takes the teal accent.

## Review
- [ ] Every card shows its ID before its title.
- [ ] Long descriptions are in the serif, not the mono.
- [ ] Cards grow with their text at 200% zoom.
