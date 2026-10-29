---
name: clip-paths-and-masks
title: Clip Paths and Masks
area: frontend
tags: [css, clip-path, mask, shapes, reveal, effects]
detect: []
related: [svg-animation, animation, blend-modes, scroll-driven-animations, accessibility]
---
Non-rectangular shapes and reveals with clip-path and mask-image, animated on the compositor where possible.

## Verify
- `npx playwright test --grep clip`: asserts computed `clipPath` and that clicks inside the clipped-out area do not hit the element.
- Devtools Rendering panel: paint flashing during a clip reveal.
- `grep -rn "\-webkit-mask" src`: prefixed masks that need the unprefixed twin.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('clipped corner is not clickable', async ({ page }) => {
  await page.goto('/');
  const box = (await page.locator('.badge').boundingBox())!;
  const hit = await page.evaluate(([x, y]) => document.elementFromPoint(x, y)?.className,
    [box.x + 1, box.y + 1]);
  expect(hit).not.toContain('badge');
});
```

## Do
- Shapes: `clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%)`, `circle(50% at 50% 50%)`, `inset(0 round 12px)`, or `path()` for custom outlines.
- Reveal animation: transition between shapes with the same function and point count, e.g. `inset(0 100% 0 0)` to `inset(0)`; ease-out, 300-600 ms.
- Soft edges: `mask-image: linear-gradient(to bottom, #000 80%, transparent)` for fade-outs on scroll containers.
- Include `-webkit-mask-image` alongside `mask-image` for older Safari and Chromium; `mask-size`, `mask-repeat` and `mask-composite` are interoperable in current engines.
- Icon recoloring: `mask: url(icon.svg) center / contain no-repeat; background: currentColor;`; the mask SVG must be same-origin.
- Clip removes hit-testing outside the shape, while masks do not clip pointer events; test both when interactivity matters.
- Under reduced motion, show the final shape immediately.
- Pair with scroll-driven reveals for the unfold effect.

## Avoid
- Clipping away focus rings: set `clip-path` on a wrapper, not the focusable element, or inset the outline.
- Animating between shapes with different point counts: no interpolation.
- Clip-path to hide content from users: it stays in the accessibility tree.
- Large masks with gradients animated each frame; repaint heavy.
- Mask images from other origins: blocked without CORS.

## Review
- [ ] Focus outlines and hit areas remain usable after clipping.
- [ ] Hidden clipped content is not wrongly exposed to or hidden from assistive tech.
- [ ] Prefixed masks have unprefixed twins.
- [ ] Reduced-motion users get the final shape without wipes.
