---
name: blend-modes
title: Blend Modes
area: frontend
tags: [css, mix-blend-mode, background-blend-mode, isolation, effects]
detect: []
related: [grain-and-noise, gradient-design, color-contrast, clip-paths-and-masks, web-performance]
---
mix-blend-mode and background-blend-mode for duotones, overlays and inverted text, scoped with isolation and contrast-checked.

## Verify
- `npx playwright test --grep blend`: asserts computed `mixBlendMode` and that the parent creates an isolated stacking context.
- `npx @axe-core/cli http://localhost:3000`: contrast on blended text over a light and a dark backdrop.
- Devtools Performance panel: scroll with the effect; blending over video or animation costs frames.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('blended title is scoped by isolation', async ({ page }) => {
  await page.goto('/');
  const iso = await page.locator('.hero').evaluate(e => getComputedStyle(e).isolation);
  expect(iso).toBe('isolate');
});
```

## Do
- Scope the effect: add `isolation: isolate` to the container so blending stays inside it and the page background does not leak in.
- Duotone image: `background-color: #1b1464; background-blend-mode: screen; ` on an element with `background-image`, plus `filter: grayscale(1)` on the image.
- Text that inverts over imagery: `color: white; mix-blend-mode: difference;`.
- Choose by intent: `multiply` darkens (shadows, tinted paper), `screen` lightens (glows), `overlay` and `soft-light` add contrast (grain, light), `luminosity` swaps lightness only, `color` recolors.
- Test in dark mode and print; blend results change with the backdrop.
- Provide a fallback color that has proper contrast, declared before the blended value; unsupported blending then still reads.
- Under `forced-colors: active`, disable blending.
- Remember `plus-lighter` composites additive light for glows and cross-fades.

## Avoid
- Blending text over unpredictable imagery for essential content: contrast varies per pixel.
- Full-page blending layers over animation: the compositor must re-blend each frame.
- Stacking contexts from `transform`, `opacity` or `filter` unintentionally cutting off the blend backdrop.
- Using blend modes where a plain color with opacity gets the same result.
- Assuming the result matches design tools exactly; color spaces differ.

## Review
- [ ] Each blend sits in an `isolation: isolate` container.
- [ ] Essential text keeps 4.5:1 contrast on the worst backdrop.
- [ ] Forced-colors and print outputs are readable.
- [ ] No full-viewport blend over animated content.
