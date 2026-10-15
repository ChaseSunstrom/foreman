---
name: responsive-design
title: Responsive Design
area: frontend
tags: [responsive, mobile-first, media-queries, viewport, fluid-type]
detect: [file:tailwind.config.*, file:postcss.config.*, dep:tailwindcss, dep:bootstrap]
related: [css-layout, image-optimization, accessibility, web-performance]
---
Mobile-first fluid layouts that hold from 320px to wide desktop and across touch and pointer inputs.

## Verify
- `npx playwright test --project=mobile`: suite on a phone device profile (define `devices['Pixel 7']` in config).
- `npx lighthouse http://localhost:3000 --preset=desktop --view`: compare against the default mobile run.
- Devtools device toolbar at 320, 375, 768, 1024, 1440: no overflow, no clipped controls.
- `grep -rn "max-width: *[0-9]*px" src`: finds desktop-first queries to review.

## Test first
Cover the smallest viewport and a touch device.
```ts
import { test, expect, devices } from '@playwright/test';
test.use({ ...devices['iPhone 13'] });

test('nav collapses and nothing overflows', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('button', { name: 'Menu' })).toBeVisible();
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth > innerWidth);
  expect(overflow).toBe(false);
});
```

## Do
- Include `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- Write base styles for the narrow case; add `@media (min-width: …)` upward.
- Pick breakpoints where the content breaks, not by device name.
- Fluid type and spacing with `clamp(1rem, 0.9rem + 0.5vw, 1.25rem)`; sizes in `rem`.
- Tap targets of at least 44px, spaced apart; put hover-only content behind `@media (hover: hover)`.
- Use `srcset` and `sizes` for images; `picture` for art direction.
- Make tables scroll inside a wrapper (`overflow-x: auto`) or reflow to cards.
- Test with `@media (pointer: coarse)` and landscape phones.

## Avoid
- `user-scalable=no` or `maximum-scale=1`: blocks zoom, fails accessibility. Remove it.
- Device-specific breakpoints (iPhone widths): they age. Use content-driven ones.
- Hiding content with `display: none` on mobile: it still downloads. Restructure or lazy load.
- `px` font sizes: ignores user settings. Use `rem`.
- Hover as the only way to reach a menu: unreachable on touch. Use click or focus.
- Forgetting `min-width: 0` on flex children: long text forces page scroll.
- Input `font-size` below 16px: iOS Safari zooms on focus. Set 16px or larger.

## Review
- [ ] Verified at 320px, tablet and wide, in portrait and landscape.
- [ ] Zoom to 200% and larger default font keep layout usable.
- [ ] Touch targets and spacing adequate; no hover dependency.
- [ ] Images sized per viewport, no oversized downloads on phones.
- [ ] Safe areas handled (`env(safe-area-inset-bottom)`) for fixed bars.
