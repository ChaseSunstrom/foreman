---
name: layout-shift
title: Layout shift (CLS)
area: frontend
tags: [performance, cls, layout, images, fonts, web-vitals]
detect: [dep:web-vitals]
related: [skeleton-loading, typography, lazy-loading, web-performance]
---
Keep Cumulative Layout Shift near zero by reserving space for everything that loads late.

## Verify
- `npx lhci autorun`: reports CLS per run, if Lighthouse CI is configured.
- `npx playwright test`: observes `layout-shift` entries through `PerformanceObserver`.
- `grep -rnE "<img(?![^>]*(width|height))" -P src`: images with no intrinsic size.

## Test first
Fail when a page shifts after load.
```ts
import { test, expect } from '@playwright/test';

test('home page does not shift', async ({ page }) => {
  await page.addInitScript(() => {
    (window as any).__cls = 0;
    new PerformanceObserver(l => {
      for (const e of l.getEntries() as any[]) if (!e.hadRecentInput) (window as any).__cls += e.value;
    }).observe({ type: 'layout-shift', buffered: true });
  });
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  expect(await page.evaluate(() => (window as any).__cls)).toBeLessThan(0.05);
});
```

## Do
- Give every `<img>` and `<video>` `width` and `height` attributes and `height: auto` in CSS, or use `aspect-ratio`.
- Reserve slots for ads, embeds, banners and async widgets with `min-height` or `aspect-ratio`.
- Render skeletons with the same dimensions as the final content.
- Insert new content below the viewport or in response to a user action, not above existing content.
- Match fallback font metrics (`size-adjust`, `ascent-override`) so font swap does not reflow.
- Animate with `transform` and `opacity`, not `top`, `height` or `margin`.
- Use `scrollbar-gutter: stable` where a scrollbar can appear and change width.
- Put cookie banners in a fixed overlay or a reserved bar, not pushed into the flow.

## Avoid
- Images and iframes without dimensions: the box is zero until loaded. Add `width` and `height`.
- Prepending late-loaded banners or "related" bars at the top: everything below jumps. Reserve space.
- Lazy-loading the LCP image and leaving its size unset: both LCP and CLS suffer. Eager-load it with dimensions.
- Collapsing an empty ad slot to height 0 after load: shift anyway. Keep the reserved height.
- Animating `height: auto` content on expand outside user input: counts as shift. Tie it to a click.
- Web fonts with `font-display: swap` and no metric overrides: text reflows when the font arrives.

## Review
- [ ] All media have intrinsic or `aspect-ratio` sizing.
- [ ] Async regions reserve space or show same-size skeletons.
- [ ] No content is injected above the fold after first paint without user input.
- [ ] Animations use compositor properties only.
- [ ] A test measures CLS under a threshold on key pages.
