---
name: gradient-design
title: Gradient Design
area: frontend
tags: [css, gradient, color, oklch, banding, mesh]
detect: []
related: [oklch-color, color-contrast, grain-and-noise, dark-mode, css-custom-properties]
---
Smooth, intentional gradients: interpolate in oklch, avoid banding and muddy midpoints, and keep text legible on top.

## Verify
- `npx playwright test --grep gradient`: asserts computed `backgroundImage` includes the oklab or oklch interpolation.
- `npx @axe-core/cli http://localhost:3000`: contrast of text over gradient samples at both ends and the middle.
- `grep -rnE "linear-gradient\(" src | grep -v " in "`: gradients still using the default sRGB interpolation.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('hero gradient interpolates in oklch', async ({ page }) => {
  await page.goto('/');
  const bg = await page.locator('.hero').evaluate(e => getComputedStyle(e).backgroundImage);
  expect(bg).toMatch(/oklch|oklab/);
});
```

## Do
- Choose the space: `linear-gradient(in oklch, oklch(70% 0.2 30), oklch(70% 0.2 250))` avoids the grey dead zone of sRGB; add `longer hue` to go the long way round.
- Use perceptually even lightness; keep the two stops within about 20-30 hue degrees for calm results, wider for loud ones.
- Add easing: extra stops (3-6) or the `linear()` ramp approach, since linear stops show visible bands at the ends.
- Soften banding: low-contrast gradients over large areas need noise of about 2-4% (see grain-and-noise) or dithering from an SVG filter.
- Mesh looks: stack 3-5 `radial-gradient()` layers with `at X% Y%`, then blur lightly with a pseudo-element.
- Animation: register colors with `@property --c1 { syntax: '<color>'; inherits: false; initial-value: #09f; }` and animate the property; gradients themselves do not transition.
- Keep gradients in custom properties; fall back to a solid `background-color` declared first.
- For text: a scrim or `background-clip: text` only for large display type with 3:1 contrast.

## Avoid
- Default sRGB between complementary hues: muddy grey midpoint.
- Rainbow stacks with no hierarchy.
- Placing body text across the gradient's mid-tone without checking contrast.
- Animating `background-position` of a huge gradient; it repaints each frame. Animate opacity of layers instead.
- Gradient text with transparent fill and no color fallback.

## Review
- [ ] Interpolation space is explicit, and the midpoint looks clean.
- [ ] Banding was checked on a large, low-contrast area.
- [ ] Text contrast holds at every sampled position.
- [ ] A solid fallback color is declared before the gradient.
