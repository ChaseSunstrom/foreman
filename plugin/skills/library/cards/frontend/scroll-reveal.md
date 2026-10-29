---
name: scroll-reveal
title: Scroll Reveal
area: frontend
tags: [scroll, intersection-observer, reveal, animation, css]
detect: [dep:aos, dep:scrollreveal]
related: [scroll-driven-animations, animation, stagger-choreography, layout-shift, accessibility]
---
Reveal content as it enters the viewport with IntersectionObserver or view timelines, only as an enhancement over visible content.

## Verify
- `npx playwright test --grep reveal`: scrolls an item into view and asserts opacity reaches 1; also runs with JavaScript disabled.
- `npx lighthouse http://localhost:3000 --only-categories=performance`: watch CLS and total blocking time.
- `grep -rn "scroll'" src | grep -v passive`: scroll listeners to replace with an observer.

## Test first
```ts
import { test, expect } from '@playwright/test';

test.use({ javaScriptEnabled: false });

test('content is visible with scripting off', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('.reveal').first()).toBeVisible();
  const o = await page.locator('.reveal').first().evaluate(e => getComputedStyle(e).opacity);
  expect(o).toBe('1');
});
```

## Do
- Hide only under a class JS adds first: `<html class="js">` then `.js .reveal:not(.in) { opacity: 0; transform: translateY(16px); }`.
- Use `new IntersectionObserver(cb, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 })`, add `.in`, then `unobserve`: animate once.
- Prefer CSS `animation-timeline: view()` where supported (see scroll-driven-animations), with the observer as fallback.
- Distance 12-24 px, duration 300-500 ms, ease-out; opacity and transform only.
- Do not reveal above-the-fold content; the largest contentful paint element must be visible at load, so LCP is not delayed.
- Under `prefers-reduced-motion: reduce`, show everything immediately.
- Anchor links and find-in-page must land on visible content: reveal the target when hash navigation occurs.

## Avoid
- Scroll event handlers calling `getBoundingClientRect` on every item: layout thrash.
- Hiding in base CSS with no no-JS fallback.
- Re-animating each time an element leaves and enters.
- Large translations that shift layout boxes; transforms avoid it.
- Revealing form fields or critical controls late.

## Review
- [ ] With JavaScript off, or if the observer fails, all content shows.
- [ ] Above-the-fold content is never hidden; LCP is unchanged.
- [ ] Reduced-motion users get content with no movement.
- [ ] Hash links and find-in-page reveal their target.
