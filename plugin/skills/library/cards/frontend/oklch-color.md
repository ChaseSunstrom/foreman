---
name: oklch-color
title: OKLCH and color-mix
area: frontend
tags: [css, oklch, color-mix, relative-color, color, gamut]
detect: []
related: [color-contrast, dark-mode, gradient-design, design-systems, css-custom-properties]
---
Define palettes in oklch(), derive shades with color-mix() and relative color syntax, and fall back for older browsers.

## Verify
- `npx playwright test --grep palette`: asserts computed colors resolve and contrast ratios hold.
- `npx culori --help` or a small script: converts oklch to sRGB and flags out-of-gamut values.
- `grep -rnE "#[0-9a-fA-F]{3,8}\b" src --include=*.css`: hard-coded hex values to fold into tokens.

## Test first
Test the contract that matters, contrast of token pairs.
```ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('button palette meets AA in light and dark', async ({ page }) => {
  for (const scheme of ['light', 'dark'] as const) {
    await page.emulateMedia({ colorScheme: scheme });
    await page.goto('/');
    const r = await new AxeBuilder({ page }).withRules(['color-contrast']).analyze();
    expect(r.violations).toEqual([]);
  }
});
```

## Do
- Write colors as `oklch(L C H)`: L 0-100% perceptual lightness, C chroma (0 to about 0.37), H hue 0-360. Same L gives similar perceived brightness across hues.
- Build a scale by stepping L (95, 85, 75 ... 25%) with a roughly constant hue and chroma tapering at the ends.
- Derive states: `color-mix(in oklch, var(--brand) 85%, black)` for hover; `color-mix(in oklch, var(--brand) 12%, transparent)` for tints.
- Relative colors: `oklch(from var(--brand) calc(l - 0.1) c h)` makes a darker sibling from one token; supported in current Chrome, Safari and Firefox.
- Fallback first: declare a hex value, then the oklch line; or `@supports (color: oklch(0 0 0))`.
- Wide gamut: high chroma values map to display-p3 where available and clip in sRGB; check both.
- Dark mode: lower L and chroma by a few points rather than inverting.
- Name tokens by role (`--color-accent`) not hue.

## Avoid
- Using HSL lightness as if it were perceptual: yellow and blue at 50% differ hugely.
- Chroma above gamut: browsers clip unpredictably, shifting the hue.
- Skipping the fallback for browsers older than 2023.
- Interpolating in sRGB when mixing; specify `in oklch` or `in oklab`.
- Palette only validated by eye; run contrast numbers.

## Review
- [ ] Every text and background pair meets 4.5:1 (3:1 for large text) in both schemes.
- [ ] Hex fallbacks exist where older browsers matter.
- [ ] Hover and tint states derive from the base token.
- [ ] Out-of-gamut colors were checked on an sRGB display.
