---
name: css-3d-transforms
title: CSS 3D Transforms
area: frontend
tags: [css, 3d, transform, perspective, flip, motion]
detect: []
related: [parallax-depth, animation, accessibility, web-performance, shadows-and-elevation]
---
Cards, flips and tilts with perspective and preserve-3d, backface handling and a flat fallback.

## Verify
- `npx playwright test --grep flip`: asserts computed `transform` after interaction and that back content is reachable.
- Devtools Layers panel: confirm the 3D element is a composited layer; check memory.
- Devtools Rendering panel: paint flashing should stay quiet during the transform.

## Test first
```ts
import { test, expect } from '@playwright/test';

test.use({ reducedMotion: 'reduce' });

test('card reveals its back without a 3D spin under reduced motion', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Flip card' }).click();
  await expect(page.getByText('Back side')).toBeVisible();
  const t = await page.locator('.card-inner').evaluate(e => getComputedStyle(e).transform);
  expect(t).toBe('none');
});
```

## Do
- Perspective on the parent: `perspective: 800px` (600-1200 px reads natural); smaller gives dramatic distortion.
- Children that stay in 3D: `transform-style: preserve-3d;` on every ancestor in the chain up to the perspective parent.
- Flip: front and back stacked, back `transform: rotateY(180deg)`, both with `backface-visibility: hidden`.
- Tilt on hover: `rotateX()` and `rotateY()` up to about 8-12 degrees from pointer position, with a transition of 150-250 ms.
- Move with `translate3d` and `rotate3d`; individual `translate`, `rotate` and `scale` properties also work in current engines.
- Hide the inactive face from assistive tech: set `inert` or `aria-hidden` on the face not shown.
- Under `prefers-reduced-motion`, swap faces with a fade or an instant change.
- Add the shadow on a sibling layer so it does not tilt with the card.

## Avoid
- `overflow: hidden`, `filter`, `opacity < 1`, or `clip-path` on a `preserve-3d` element: each flattens it.
- Text on rotated surfaces at awkward angles; it blurs on some GPUs.
- Many large 3D layers: texture memory grows quickly on phones.
- `perspective` on the same element you transform; it needs to be on the parent (or use `perspective()` in the function).
- Back content that keyboard users cannot reach.

## Review
- [ ] Both faces are reachable by keyboard and the hidden face is inert.
- [ ] Reduced-motion users get a non-spinning swap.
- [ ] No ancestor flattens `preserve-3d`.
- [ ] Layer count and memory checked on a mid-range phone.
