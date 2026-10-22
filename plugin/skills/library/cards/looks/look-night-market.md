---
name: look-night-market
title: "Look: Night market"
area: looks
tags: [look, style, palette, food, menu, events, nightlife, dark]
detect: []
related: [look-ceramic-studio, look-observatory, design-systems, typography, color-contrast]
---
A street-food market after dark: warm brown-black, stalls under strung lights, prices on painted boards, one dragon-fruit pink.

## Palette
| Role | Hex | OKLCH | Measured |
|---|---|---|---|
| `--surface` | #1B1410 | 0.2 0.014 50 | page |
| `--raised` | #261F1B | 0.245 0.014 50 | cards, popovers |
| `--text` | #F3E9E3 | 0.94 0.014 50 | 15.2:1 on surface, 13.6:1 on raised |
| `--text-muted` | #BFB5B0 | 0.78 0.014 50 | 9.1:1 on surface, 8.1:1 on raised |
| `--border` | #736A65 | 0.53 0.014 50 | 3.4:1 on surface |
| `--accent` | #DB6BAF | 0.68 0.160 345 | 5.8:1 on surface |
| `--on-accent` | #1B1410 | 0.2 0.014 50 | 5.8:1 on accent |

Dark first: body text clears Foreman's 7:1 dark rule. Accent hue 345, 42° from error red; lantern orange stays out of the accent because it sits on warning amber.

## Type
Slab at 700 for stall names and prices, like a painted board; humanist sans at 400 for descriptions. They differ on classification and stroke weight. Prices take tabular figures and run larger than the dish's description.

## Layout
Stalls are cards in a two- or three-column grid on `--raised`, each headed by its board: name in slab, price at the right. Sections are split by a string of lights, a row of small `--text-muted` dots marked `aria-hidden`. Filters sit in one sticky row of chips at the top.

## Motion
Warm and still: cards arrive on `--dur-enter` with `--ease-enter`; hovering a stall raises a soft accent-tinted glow behind the card on `--dur-small`. Nothing flickers or loops.

## Texture
One warm radial glow behind the header (the surface 0.03 L lighter at its centre); the rest is flat. Radius 8 px on stalls, chips fully round.

## Suits
Food ordering and menus, night events and festivals, bars and restaurants, community markets, nightlife listings.
Not for: daytime enterprise tools, banking, medical, long documentation.

## Verify
- `pytest -q test_look_contrast.py`: every pair holds its floor, body text at 7:1.
- `grep -rnE "@keyframes[^{]*(flicker|glitch|neon)" src`: returns nothing.
- `grep -rn "text-shadow" src --include=*.css`: returns nothing; glow is on surfaces, never on text.

## Test first
Commit the look's pairs before styling; when you adapt a hex, change its pair and rerun.
```python
# test_look_contrast.py
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def test_pairs():
    for fg, bg, floor in [("#F3E9E3", "#1B1410", 7), ("#F3E9E3", "#261F1B", 7), ("#BFB5B0", "#1B1410", 4.5),
                          ("#BFB5B0", "#261F1B", 4.5), ("#736A65", "#1B1410", 3), ("#DB6BAF", "#1B1410", 4.5),
                          ("#1B1410", "#DB6BAF", 4.5)]:
        hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
        assert (hi + 0.05) / (lo + 0.05) >= floor, (fg, bg, floor)
```

## Do
- Price like a painted board: dish name in slab, the price larger than the description, on tabular figures.

## Avoid
- Neon tubes, flicker or glitch: that is the Night arcade direction; here the light is warm and still.

## Review
- [ ] Each stall shows name and price before anything else.
- [ ] The string-of-lights dividers are hidden from screen readers.
- [ ] Pink marks one action per view; no text glows.
