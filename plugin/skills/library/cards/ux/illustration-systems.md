---
name: illustration-systems
title: Illustration Systems
area: ux
tags: [ux, illustration, svg, brand, empty-states, style-guide]
detect: []
related: [brand-identity, color-palettes, svg-icon-system, image-direction, art-direction, dark-mode]
---
A product illustration set drawn from one grid, palette and line rule, delivered as small recolorable SVG.

## Verify
- `npx svgo -f illustrations --multipass`: optimizes; target under 30 KB per spot illustration.
- `grep -rhoE 'fill="#[0-9a-fA-F]+"' illustrations | sort | uniq -c | sort -rn`: colors used; all should map to palette tokens.
- `grep -L "<title>\|aria-hidden" illustrations/*.svg`: files with no accessibility decision.
- `ls illustrations | wc -l`: the set stays inventory-controlled.

## Test first
Check that every illustration uses only palette colors.
```python
import glob, re
PALETTE = {"#1a1a1f", "#3b5bdb", "#dbe4ff", "#f8f9fa", "#ffd43b"}

def test_illustrations_use_palette():
    for f in glob.glob("illustrations/*.svg"):
        used = {c.lower() for c in re.findall(r'#[0-9a-fA-F]{6}', open(f).read())}
        assert used <= PALETTE, (f, used - PALETTE)
```

## Do
- Set the rules once: a 4-5 color palette taken from the brand, one stroke weight (2px) or none, one corner style, one level of detail, one perspective (flat or isometric, not both).
- Build on a fixed artboard (e.g. 480x360 spot, 1200x600 hero) with a safe margin of 24px.
- Use CSS custom properties in inline SVG (`fill: var(--illo-accent)`) so dark mode and themes recolor it.
- Reserve illustration for empty states, onboarding, errors and marketing; use icons for controls.
- Keep people diverse in skin tone, body and context without stereotypes; avoid faces if you can't do them consistently.
- Decorative: `alt=""` or `aria-hidden`; informative: concise alt text.
- Lazy-load below the fold; set `width` and `height` to avoid layout shift.

## Avoid
- Mixing stock illustration styles: the set looks stitched together.
- Text inside the image: not translatable or accessible.
- Raster exports of line art: blurry on HiDPI and bigger.
- Heavy gradients and meshes that bloat the SVG past 100 KB.

## Review
- [ ] Palette, line weight and perspective are written down and every file follows them.
- [ ] Illustrations recolor for dark mode.
- [ ] Each has an alt decision and fixed dimensions.
- [ ] Each file is small and optimized.
