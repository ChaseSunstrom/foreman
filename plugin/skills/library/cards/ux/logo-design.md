---
name: logo-design
title: Logo Design
area: ux
tags: [ux, logo, brand, svg, legibility]
detect: []
related: [brand-identity, app-icons-and-favicons, icon-design, svg-icon-system, color-palettes]
---
A logo that survives 16 px, one color, and a dark background, delivered as optimized SVG in set variants.

## Verify
- `npx svgo logo/*.svg`: optimized; a logo should be under about 5 KB.
- `convert -background none -resize 16x16 logo/mark.svg /tmp/mark16.png`: view it; the shape must still read.
- `convert logo/mark.svg -colorspace Gray -threshold 50% /tmp/mono.png`: the one-color check.
- `grep -c "<text" logo/*.svg`: wordmarks must be outlined paths (0 text elements).

## Test first
Render at the smallest size and compare ink coverage so the mark does not vanish.
```python
import subprocess
from PIL import Image

def test_mark_visible_at_16px(tmp_path):
    out = tmp_path / "m.png"
    subprocess.run(["convert", "-background", "white", "-resize", "16x16", "logo/mark.svg", str(out)], check=True)
    px = Image.open(out).convert("L").getdata()
    dark = sum(1 for p in px if p < 128)
    assert 30 <= dark <= 200, dark  # not blank, not a blob
```

## Do
- Design in black and white first; add color after the form works.
- Deliver variants: primary lockup, stacked, icon-only mark, monochrome, reversed (for dark backgrounds).
- Set clear space equal to the mark's cap height on all sides; minimum size 16 px for the mark, 80 px wide for the lockup.
- Outline text to paths; keep a single `viewBox` tightly cropped, no stray artboard padding.
- Keep it to 2-3 colors and few shapes; avoid thin strokes under 2 px at 32 px size.
- Make the mark work as a square crop for avatars and favicons.
- Check on light, dark and photographic backgrounds.

## Avoid
- Gradients, shadows, fine detail that vanish when small or printed in one color.
- Fonts that are not licensed for logos.
- Raster-only deliverables; a PNG logo as the only source.
- Trendy effects that date the mark; stretched or recolored use of the logo outside the guide.

## Review
- [ ] Mark reads at 16 px and in one color.
- [ ] Variants exist: lockup, stacked, mark, mono, reversed, as SVG.
- [ ] Clear space and minimum size are written down.
- [ ] Text is outlined, and the font license covers logo use.
