---
name: color-palettes
title: Color Palettes
area: ux
tags: [ux, color, palette, oklch, brand, accessibility]
detect: []
related: [color-contrast, dark-mode, design-tokens, brand-identity, css-custom-properties]
---
A palette is a neutral ramp, one brand hue, and semantic colors, each with fixed lightness steps in OKLCH.

## Verify
- `grep -rnE "#[0-9a-fA-F]{3,8}\b" src --include=*.css --include=*.tsx | grep -v tokens`: raw hex outside the token file.
- `npx playwright test --grep palette`: renders the app in light and dark and runs `new AxeBuilder({ page }).withRules(['color-contrast']).analyze()` (from `@axe-core/playwright`); expect no violations.
- `python3 -m pytest tests/test_palette.py`: the token-file contrast test below.

## Test first
Compute WCAG contrast for text/surface pairs read from the token file (hex values in W3C format, `tokens/tokens.json`).
```python
import json

PAIRS = [("color.text", "color.surface"), ("color.on-action", "color.action")]  # semantic names

def token(tree, path):
    for k in path.split("."):
        tree = tree[k]
    return tree["$value"]

def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def lum(rgb):
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    r, g, b = (f(x / 255) for x in rgb)
    return .2126 * r + .7152 * g + .0722 * b

def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + .05) / (lb + .05)

def test_text_on_surface():
    tree = json.load(open("tokens/tokens.json"))
    for fg, bg in PAIRS:
        r = ratio(rgb(token(tree, fg)), rgb(token(tree, bg)))
        assert r >= 4.5, f"{fg} on {bg}: {r:.2f}"
```

## Do
- Build ramps in OKLCH: steps 50, 100 ... 900 at lightness about 98, 94, 88, 80, 70, 60, 50, 40, 30, 20 percent, with chroma tapering at the ends.
- Use 1 brand hue, 1 optional accent, one neutral ramp (tinted 2-4 percent chroma toward the brand), and four semantics: success, warning, danger, info.
- Follow 60-30-10: 60 percent neutral surface, 30 percent secondary, 10 percent accent.
- Pair steps by distance: a 500 vs 50 gap passes AA for text; check, don't assume.
- Expose semantic tokens (`--color-text`, `--color-surface`, `--color-action`) over raw ramp values; dark mode remaps the semantic layer.
- Never use color alone for meaning: add an icon or text with success and error.
- Check palettes under protanopia and deuteranopia emulation.

## Avoid
- Pure `#000` on `#fff` for body: harsh; use near-black 15-20 percent lightness.
- Equal saturation across all hues in sRGB HSL: perceived brightness varies; use OKLCH.
- More than one accent at full saturation per view.
- Yellow text on white; gray placeholder text under 4.5:1.

## Review
- [ ] Every text and UI pair passes WCAG AA, measured by script.
- [ ] Ramps are generated or documented with lightness steps, not eyeballed hex.
- [ ] Semantic tokens exist; components never use ramp values directly.
- [ ] Meaning is never carried by color alone.
