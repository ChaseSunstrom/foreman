---
name: scroll-driven-animations
title: Scroll-Driven Animations
area: frontend
tags: [css, scroll, animation-timeline, view-timeline, motion]
detect: []
related: [animation, scroll-reveal, parallax-depth, web-performance, accessibility]
---
Tie animation progress to scroll with animation-timeline: scroll() and view(), off the main thread, with a static fallback.

## Verify
- `npx playwright test --grep scroll-anim`: scrolls the page and asserts computed opacity or transform at set offsets.
- `grep -rn "addEventListener('scroll'" src`: scroll handlers that should now be CSS timelines.
- Devtools Performance panel: no scripting or layout per scroll frame; frames stay under 16.7 ms.

## Test first
Assert the end state at a scroll offset, and that unsupported or reduced-motion users see content.
```ts
import { test, expect } from '@playwright/test';

test.use({ reducedMotion: 'reduce' });

test('hero is visible without scroll animation', async ({ page }) => {
  await page.goto('/');
  const o = await page.locator('.hero').evaluate(el => getComputedStyle(el).opacity);
  expect(o).toBe('1');
});
```

## Do
- Progress bar: `animation: grow linear both; animation-timeline: scroll(root block);` animating `transform: scaleX(0 to 1)`.
- Element reveal: `animation-timeline: view(); animation-range: entry 0% entry 100%;` so progress follows the element crossing the viewport.
- Name timelines (`view-timeline-name: --card`) to drive a child from an ancestor's progress.
- Set `animation-duration: 1ms` as a fallback for older engines that need a duration; use `linear` easing, since scroll position is the timing.
- Gate with `@supports (animation-timeline: view())` and `@media (prefers-reduced-motion: no-preference)`; default styles must be the finished state.
- Animate `transform`, `opacity`, `clip-path`, `filter`: compositor-friendly, so scrolling stays smooth.
- Support: Chromium and Safari 26+; Firefox behind a flag; check caniuse. Treat as progressive enhancement, or use the polyfill only if the effect is essential.

## Avoid
- Scroll listeners that write styles: they run on the main thread and jank under load.
- Hiding content by default and relying on the timeline to reveal it: unsupported browsers show nothing.
- Easing curves on scroll-linked animation: they decouple motion from the finger.
- Long ranges on tall content that make animation crawl; keep ranges to roughly one viewport.
- Animating `width`, `height` or `top` on scroll: layout each frame.

## Review
- [ ] Without `animation-timeline` support the page is complete and readable.
- [ ] Reduced-motion users get no scrubbed movement, only the end state.
- [ ] Only compositor properties animate; the profile shows no layout per frame.
- [ ] Animation ranges are tested at the top, middle and end of the page.
