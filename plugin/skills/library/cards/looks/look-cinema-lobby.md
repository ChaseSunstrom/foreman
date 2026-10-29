---
name: look-cinema-lobby
title: "Look: Cinema lobby"
area: looks
tags: [look, style, palette, film, theatre, ticketing, events, dark]
detect: []
related: [look-night-market, look-broadcast-graphics, design-systems, typography, color-contrast]
---
A single-screen picture house at night: oxblood-black walls, a warm cream marquee, one brass accent for the ticket counter.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #17090C | 0.162 0.025 6 | page |
| `--raised` | #241216 | 0.209 0.031 6 | posters, panels |
| `--text` | #F3E6D8 | 0.931 0.023 70 | 15.8:1 on surface, 14.6:1 on raised |
| `--text-muted` | #C4AB9B | 0.759 0.037 55 | 8.9:1 on surface, 8.2:1 on raised |
| `--border` | #85686A | 0.547 0.037 14 | 3.9:1 on surface |
| `--accent` | #D2C06A | 0.805 0.109 98 | 10.6:1 on surface |
| `--on-accent` | #17090C | 0.162 0.025 6 | 10.6:1 on accent |

Dark first: body text clears Foreman's 7:1 dark rule. Brass is a pale yellow-olive at chroma 0.11, readable on the dark wall without glowing; the red walls stay in the background and carry no meaning. Accent hue 98, 33° from the nearest status hue.

## Type
Didone at 700 for show titles in capitals, tracked +0.04em; humanist sans at 400 for times, prices and body. Showtimes use tabular figures at 1.125rem so a column of times lines up.

## Layout
Posters in a row of 2:3 tiles with the title under each; a day strip of showtimes as brass-outlined pills (44 px tall at least) beneath. The seat map is a centred grid on `--raised` with a curved screen line above it. One column on a phone.

## Motion
Curtain-slow: the page enters on `--dur-stage` with `--ease-enter`; a selected seat fills on `--dur-small`. Posters never autoplay trailers.

## Texture
A soft vignette on the hero poster only (a radial gradient from clear to `--surface` at 30%); tiles take a 2 px radius.

## Suits
Cinemas and theatres, film festivals, ticketing and seat selection, event listings, streaming-night picks.
Not for: finance, health, productivity tools.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor.
- `grep -rn "tabular-nums" src`: on showtimes, prices and seat labels.
- `grep -rniE "autoplay" src`: returns nothing.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#F3E6D8", "#17090C", 7), ("#F3E6D8", "#241216", 7), ("#C4AB9B", "#17090C", 4.5),
                          ("#C4AB9B", "#241216", 4.5), ("#85686A", "#17090C", 3), ("#D2C06A", "#17090C", 4.5),
                          ("#17090C", "#D2C06A", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Show each film's showtimes as brass-outlined pills under its poster, with the sold-out ones struck and labelled in text.

## Avoid
- Red velvet or curtain imagery as decoration: the dark wall is the room; extra costume turns a ticket counter into a theme park.

## Review
- [ ] Every showtime pill is at least 44 px tall.
- [ ] A sold-out time is labelled in text, not colour alone.
- [ ] The vignette sits only on the hero poster.
