---
name: parallax-depth
title: Parallax and Depth
area: frontend
tags: [parallax, depth, scroll, css, 3d, motion]
detect: []
related: [scroll-driven-animations, css-3d-transforms, accessibility, web-performance, animation]
---
Layered scroll depth with transform only, small ranges, and a still version for motion-sensitive users.

## Verify
- `npx playwright test --grep parallax`: asserts layers hold their rest position under reduced motion.
- Devtools Layers panel: count composited layers; keep them to a handful on a page.
- Devtools Performance panel: scroll the page; frames under 16.7 ms with no main-thread scripting.

## Test first
```ts
import { test, expect } from '@playwright/test';

test.use({ reducedMotion: 'reduce' });

test('background layer does not move on scroll', async ({ page }) => {
  await page.goto('/');
  const before = await page.locator('.bg').boundingBox();
  await page.mouse.wheel(0, 600);
  await page.waitForTimeout(100);
  const after = await page.locator('.bg').boundingBox();
  expect(after!.y - before!.y).toBe(-600);
});
```

## Do
- Use a view or scroll timeline: `animation: drift linear both; animation-timeline: view();` moving `transform: translateY(-40px to 40px)`.
- CSS-only depth: a `perspective: 1px` scroller with `translateZ(-1px) scale(2)` children; test in Safari, which handles it differently.
- Rate rule: background moves at 0.2-0.5 times the scroll speed, foreground at 1. Keep total offset under about 80 px.
- Promote only moving layers (`will-change: transform` while in view).
- Large images behind parallax: oversize by the travel distance so no edge shows.
- Under `prefers-reduced-motion: reduce`, drop to static layers; disable on small screens when it hurts battery.
- Use `object-fit: cover` and image sizes from the image-optimization card.

## Avoid
- Moving `background-position` or `top`: repaints every frame.
- Scroll listeners setting transforms: jank, and desync from the compositor.
- Large offsets and fast movement: nausea and vestibular harm.
- Text over moving layers without checking contrast at every position.
- Dozens of full-viewport layers.

## Review
- [ ] Reduced-motion users get a fixed, fully legible page.
- [ ] Only transforms move; the profile shows no paint per frame.
- [ ] Text contrast holds over every layer position.
- [ ] Layer count is small and tested on a mid-range phone.
