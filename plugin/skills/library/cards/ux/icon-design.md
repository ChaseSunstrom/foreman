---
name: icon-design
title: Icon Design
area: ux
tags: [ux, icons, svg, pixel-grid, stroke, accessibility]
detect: []
related: [svg-icon-system, app-icons-and-favicons, logo-design, accessibility, design-systems]
---
A consistent icon set: one grid, one stroke weight, one corner style, labeled or hidden from screen readers.

## Verify
- `npx svgo --multipass -f icons -o dist/icons`: optimizes; each icon should shrink to under about 1 KB.
- `grep -L 'viewBox="0 0 24 24"' icons/*.svg`: lists icons off the 24px grid.
- `grep -LE 'stroke-width="(1.5|2)"' icons/*.svg`: lists icons with an odd stroke.
- `npx playwright screenshot` of an icon sheet at 16, 20, 24 px: visual check.

## Test first
Lint every icon for grid and stroke.
```python
import glob, re

def test_icons_consistent():
    for f in glob.glob("icons/*.svg"):
        s = open(f).read()
        assert 'viewBox="0 0 24 24"' in s, f
        assert not re.search(r'fill="#|stroke="#', s), f"{f}: hard-coded color, use currentColor"
        widths = set(re.findall(r'stroke-width="([\d.]+)"', s))
        assert len(widths) <= 1, f
```

## Do
- Draw on a 24x24 grid with a 2px safe padding (live area 20x20); also supply 16px if the set is used small.
- One stroke width (1.5 or 2px), round or square caps and joins across the whole set, and one corner radius (2px).
- Use `currentColor` so icons inherit text color and theme.
- Align strokes to the pixel grid: even widths on integer coordinates stay crisp.
- Keep a metaphor per meaning; pair ambiguous icons with a text label.
- Decorative icon: `aria-hidden="true"`. Standalone icon button: `aria-label` on the button, not the svg.
- Touch target 44x44 px (24px icon plus padding) on touch UIs.
- Give optical balance: circles slightly larger than squares so they look equal.

## Avoid
- Mixing filled and outline styles in one set without a state meaning (e.g. filled = selected).
- Icon-only buttons for rare actions: users can't guess them.
- Embedded raster or text in SVG; unoptimized exports with editor metadata.
- Colors baked into the file.

## Review
- [ ] Every icon uses the same grid, stroke width, caps and corner radius.
- [ ] Icons render crisp at 16, 20 and 24 px.
- [ ] Meaningful icons have an accessible name; decorative ones are hidden.
- [ ] Touch targets are 44px or more.
