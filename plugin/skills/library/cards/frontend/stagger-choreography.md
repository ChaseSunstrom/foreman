---
name: stagger-choreography
title: Stagger and Choreography
area: frontend
tags: [animation, stagger, sequencing, css, motion]
detect: []
related: [animation, easing-curves, scroll-reveal, css-custom-properties, accessibility]
---
Sequence related elements with short, capped delays so the eye is led through a screen without waiting.

## Verify
- `npx playwright test --grep stagger`: asserts the final state arrives and the last delay is under the cap.
- `grep -rn "animation-delay\|transition-delay" src`: delays set by hand that should come from one index variable.
- Devtools Animations panel: check total duration of the group, under 600 ms.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('last list item delay stays within the cap', async ({ page }) => {
  await page.goto('/');
  const delays = await page.locator('.list > li').evaluateAll(
    els => els.map(e => parseFloat(getComputedStyle(e).animationDelay)));
  expect(Math.max(...delays)).toBeLessThanOrEqual(0.5);
});
```

## Do
- Drive delay from an index: `style="--i: 3"` and `animation-delay: calc(min(var(--i), 8) * 40ms);`.
- Step 30-60 ms between items; cap total stagger at 400-500 ms by capping the index, not by growing the step.
- Animate in reading order; lead with the most important item.
- Use `sibling-index()` where supported, otherwise set `--i` in the template.
- Keep each item's own duration 200-300 ms with ease-out; the group should resolve under 700 ms.
- Use `animation-fill-mode: both` so delayed items stay in their start state before running.
- Under `prefers-reduced-motion: reduce`, set delay and duration to 0 or fade only.
- For long lists, stagger only what is on screen (IntersectionObserver or scroll timelines).

## Avoid
- Linear growth of delay on big lists: item 50 appears after 2 seconds.
- Staggering on every re-render or filter change: repetitive and slow.
- Hidden items before animation starts when JS fails: set the start state in the animation, not the base style.
- Layout-affecting properties in the sequence.
- Competing sequences on the same screen at once.

## Review
- [ ] Total sequence time is capped and tested with the longest realistic list.
- [ ] Reduced-motion users see content at once.
- [ ] Content is visible if animations never run.
- [ ] Stagger only on first meaningful appearance, not each update.
