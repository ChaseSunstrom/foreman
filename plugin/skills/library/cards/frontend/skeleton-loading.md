---
name: skeleton-loading
title: Skeleton loading
area: frontend
tags: [loading, skeleton, suspense, a11y, layout-shift]
detect: [dep:react-loading-skeleton]
related: [layout-shift, infinite-scroll, data-tables, error-boundaries]
---
Placeholder UI shaped like the final content: same dimensions, announced politely, and never stuck.

## Verify
- `npx playwright test`: delays the API, asserts the skeleton, then asserts no shift on swap.
- `npx @axe-core/cli http://localhost:3000`: contrast and region semantics in the loading state.
- `npx vitest run`: loading, loaded, empty and error branches render.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('skeleton occupies the final height and then swaps', async ({ page }) => {
  await page.route('**/api/profile', async r => {
    await new Promise(res => setTimeout(res, 500));
    await r.continue();
  });
  await page.goto('/profile');
  const card = page.getByTestId('profile-card');
  const h1 = (await card.boundingBox())!.height;
  await expect(card.getByRole('heading')).toBeVisible();
  const h2 = (await card.boundingBox())!.height;
  expect(Math.abs(h1 - h2)).toBeLessThan(2);
});
```

## Do
- Match the final layout: same container, grid, line counts, image aspect ratio and row heights.
- Mark the region `aria-busy="true"` while loading, and flip it to `false` when content arrives; add a visually hidden "Loading" status text.
- Use a subtle shimmer via `background-position` or `transform` animation and disable it under `prefers-reduced-motion: reduce`.
- Show skeletons only after a short delay (about 150 to 300 ms) and keep them at least a moment (about 300 ms) to avoid flashes on fast loads.
- Keep real, stable parts (headings, nav, filters) rendered and skeletonize only the data.
- Handle the other three states: empty, error with retry, and stale-while-revalidate (keep old data, show a small busy indicator).
- Use Suspense boundaries (or equivalent) at meaningful section level, not per element.
- Set a timeout path: if loading exceeds a limit, show an error or "taking longer than usual".

## Avoid
- A centered spinner replacing the whole page: it jumps layout and hides context. Skeleton the content only.
- Skeleton heights that differ from content: shift on swap. Measure and match.
- Animating `width` or `height` for the shimmer: layout cost. Animate `transform` or background position.
- Infinite shimmer with no error path: users wait forever on failure. Add timeout and retry.
- Per-line skeleton nodes in lists of hundreds: heavy DOM. Use a few rows or CSS gradients.
- Low-contrast skeletons invisible in dark mode: define tokens for both themes.
- Skeletons for sub-100 ms loads: flash. Apply the delay.

## Review
- [ ] Skeleton geometry matches loaded content (verified by measurement).
- [ ] Busy state is exposed to assistive tech.
- [ ] Reduced motion disables animation.
- [ ] Empty, error and stale states exist.
- [ ] A load that never finishes surfaces an error.
