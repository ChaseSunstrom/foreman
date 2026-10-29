---
name: variable-fonts
title: Variable Fonts
area: frontend
tags: [fonts, variable-fonts, font-variation-settings, woff2, typography]
detect: [ext:.woff2, dep:@fontsource-variable/inter, dep:@fontsource/inter]
related: [typography, fluid-typography, kinetic-typography, web-performance, layout-shift]
---
One variable file for many weights and widths: axis ranges in @font-face, high-level properties first, subset and preload.

## Verify
- `fonttools varLib.instancer --help` (pip install fonttools) or `pyftsubset font.woff2 --unicodes=U+0020-007F --flavor=woff2`: subsets and instances to cut size.
- `ls -l public/fonts/*.woff2`: a Latin variable file is typically 30-100 KB; investigate bigger.
- `npx playwright test --grep font`: asserts `document.fonts.check` and computed weight.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('heading uses the variable weight axis', async ({ page }) => {
  await page.goto('/');
  await page.evaluate(() => document.fonts.ready);
  const w = await page.locator('h1').evaluate(e => getComputedStyle(e).fontWeight);
  expect(w).toBe('750');
  expect(await page.evaluate(() => document.fonts.check('750 1em Inter'))).toBe(true);
});
```

## Do
- Declare ranges: `@font-face { font-family: Inter; src: url(inter.woff2) format('woff2'); font-weight: 100 900; font-stretch: 75% 125%; font-display: swap; }`.
- Use high-level properties: `font-weight: 650`, `font-stretch`, `font-style: oblique 10deg`, `font-optical-sizing: auto`; use `font-variation-settings: "wght" 650` only for custom axes (for example `"GRAD"`, `"slnt"`), because it overrides everything and does not cascade by axis.
- Animate weight with `transition: font-weight 200ms`; reserve space or use `font-variation-settings` carefully to avoid reflow of neighbors.
- Preload the main file: `<link rel="preload" as="font" type="font/woff2" href="/fonts/inter.woff2" crossorigin>`; the crossorigin attribute is required.
- Reduce layout shift with `size-adjust`, `ascent-override` and `descent-override` on a local fallback face.
- Subset by unicode-range; split Latin and extended files.
- Self-host; one variable file generally replaces 4+ static files.

## Avoid
- Variable files with unused axes: each axis adds size; instance the ones you need.
- `font-display: block` on body text: invisible text up to 3 s.
- Setting `font-variation-settings` on a parent: it resets each axis not listed on children.
- Preloading many fonts: they compete with critical resources.
- Relying on weights the file range does not contain; browsers synthesize bold.

## Review
- [ ] The weight and width ranges in @font-face match the file's axes.
- [ ] Fallback metrics keep CLS near zero when the font swaps.
- [ ] Only needed subsets and axes ship.
- [ ] Preload has `crossorigin` and applies to above-the-fold text only.
