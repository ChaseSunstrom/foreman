---
name: frosted-glass
title: Frosted Glass (backdrop-filter)
area: frontend
tags: [css, backdrop-filter, glassmorphism, blur, effects]
detect: []
related: [color-contrast, dark-mode, shadows-and-elevation, web-performance, accessibility]
---
Translucent blurred panels with backdrop-filter that keep text contrast and degrade to a solid surface.

## Verify
- `npx playwright test --grep glass`: asserts the computed `backdropFilter` and a solid fallback when unsupported.
- `npx @axe-core/cli http://localhost:3000`: color-contrast on text over the panel (sample a busy background).
- Devtools Performance panel: frames under 16.7 ms while scrolling content behind the panel.

## Test first
Contrast is the contract: test the worst backdrop, not the pretty one.
```ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('glass nav text meets contrast over a bright image', async ({ page }) => {
  await page.goto('/?bg=bright');
  const r = await new AxeBuilder({ page }).include('.glass').withRules(['color-contrast']).analyze();
  expect(r.violations).toEqual([]);
});
```

## Do
- Recipe: `background: rgb(255 255 255 / 0.55); backdrop-filter: blur(16px) saturate(140%); border: 1px solid rgb(255 255 255 / 0.3);`.
- Blur radius 8-24 px; larger costs more GPU time with little visible gain.
- Fallback first, then enhance: `@supports (backdrop-filter: blur(1px)) { ... }` and use a near-opaque background (0.9+) otherwise.
- Use `@media (prefers-reduced-transparency: reduce)` to go solid; it is supported in Safari and newer Chromium.
- Dark mode: swap to `rgb(20 20 24 / 0.6)`, and recheck contrast; do not reuse the light alpha.
- Add a thin border or inner highlight so edges read against light backgrounds.
- Apply to few, small, fixed elements (nav, sheets, tooltips). Include `-webkit-backdrop-filter` for older Safari.
- Text should sit on at least 4.5:1 contrast against the worst possible blurred backdrop.

## Avoid
- Glass over images with unpredictable content and no scrim: contrast fails.
- Full-screen blur layers that sit over scrolling content: continuous GPU work and battery drain.
- Nested `backdrop-filter`: the inner one sees nothing useful and costs a lot.
- Animating the blur radius; animate opacity instead.
- Using `filter: blur` on the element itself, which blurs its text.

## Review
- [ ] Contrast is measured over the lightest and darkest backgrounds.
- [ ] Unsupported browsers and reduced-transparency users get a solid surface.
- [ ] Glass is limited to a few small elements; scrolling stays smooth.
- [ ] Dark mode has its own alpha and border values.
