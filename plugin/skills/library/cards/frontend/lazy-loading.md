---
name: lazy-loading
title: Lazy loading
area: frontend
tags: [performance, images, intersection-observer, lazy, loading]
detect: [dep:react-lazy-load-image-component]
related: [layout-shift, image-optimization, code-splitting, web-performance]
---
Defer offscreen images, iframes and heavy widgets without delaying the largest paint or shifting layout.

## Verify
- `npx playwright test`: counts network requests before and after scrolling.
- `npx lhci autorun`: LCP and offscreen-images audits, if configured.
- `grep -rn 'loading="lazy"' src`: review that none sit on above-the-fold media.

## Test first
Offscreen images must not load until scrolled near.
```ts
import { test, expect } from '@playwright/test';

test('below-the-fold image loads on scroll only', async ({ page }) => {
  const reqs: string[] = [];
  page.on('request', r => r.url().includes('/gallery/9.jpg') && reqs.push(r.url()));
  await page.goto('/gallery');
  await page.waitForLoadState('networkidle');
  expect(reqs).toHaveLength(0);
  await page.locator('img[src*="/gallery/9.jpg"]').scrollIntoViewIfNeeded();
  await expect.poll(() => reqs.length).toBe(1);
});
```

## Do
- Use native `loading="lazy"` on `<img>` and `<iframe>` below the fold, with `width` and `height` set.
- Mark the LCP image `loading="eager"` with `fetchpriority="high"`; never lazy-load it.
- For custom widgets use `IntersectionObserver` with `rootMargin: '200px'` so work starts before visibility, and `disconnect()` after the first hit.
- Replace heavy embeds (video, maps) with a click-to-load facade of the same size.
- Provide `<noscript>` fallbacks only when content truly needs it for SEO or no-JS use.
- Use `decoding="async"` on large images.
- Prefetch the next likely chunk on hover or idle, not on mount.

## Avoid
- `loading="lazy"` on hero or first-screen images: delays LCP. Set eager and high priority.
- Lazy images with no dimensions: each load shifts the page. Reserve space with attributes or `aspect-ratio`.
- A scroll listener with `getBoundingClientRect` per event: layout thrash. Use `IntersectionObserver`.
- Never disconnecting observers: leaks per item. Unobserve on first intersect and on unmount.
- Lazy content that crawlers or print never see: render critical text server-side.
- Tabs and accordions that lazy-mount with no loading state: a blank panel. Show a skeleton the same size.

## Review
- [ ] The LCP element is eager with high fetch priority.
- [ ] All lazy media have reserved dimensions.
- [ ] Observers are cleaned up on unmount.
- [ ] A test asserts nothing offscreen is fetched at load.
- [ ] Facades are keyboard operable buttons, not clickable divs.
