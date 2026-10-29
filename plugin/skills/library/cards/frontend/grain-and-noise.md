---
name: grain-and-noise
title: Grain and Noise Textures
area: frontend
tags: [css, svg-filter, noise, texture, feTurbulence, effects]
detect: []
related: [gradient-design, svg-canvas, web-performance, blend-modes, dark-mode]
---
Add film grain and noise with a tiny tiled image or SVG feTurbulence, static, low opacity and cheap to paint.

## Verify
- `ls -l public/noise.*`: a tiled noise PNG or WebP should be under about 10 KB.
- `npx playwright test --grep grain`: asserts the overlay ignores pointer events and is hidden from assistive tech.
- Devtools Performance panel: no per-frame paint from the overlay while scrolling.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('grain overlay never blocks clicks', async ({ page }) => {
  await page.goto('/');
  const pe = await page.locator('.grain').evaluate(e => getComputedStyle(e).pointerEvents);
  expect(pe).toBe('none');
  await page.getByRole('button', { name: 'Buy' }).click();
});
```

## Do
- Preferred: a 128-256 px seamless noise tile as a background image on a fixed `::before`, `opacity: 0.04-0.08`, `pointer-events: none`.
- Inline SVG alternative as a data URI: `<filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" stitchTiles="stitch"/></filter>` applied to a `<rect>`; render once.
- Blend: `mix-blend-mode: overlay` or `soft-light` on the overlay for light and dark backgrounds alike.
- Use grain to break gradient banding (about 2-4% strength).
- Put the overlay at a low z-index above backgrounds and below content, not over text where it lowers contrast.
- Animate grain, if at all, with `steps(6)` shifting `transform: translate` of a larger tile at 8-12 fps; stop it under `prefers-reduced-motion`.
- Add `aria-hidden="true"` for elements, or use only a pseudo-element.

## Avoid
- A live `feTurbulence` filter on a large element that repaints: the filter recomputes and costs frames.
- Full-viewport `mix-blend-mode` over scrolling video or animation: forces expensive blending every frame.
- High opacity: dirty screens, lower text contrast, and bigger PNGs.
- Raster noise without seamless edges; seams show on large displays.
- Overlays that capture pointer events or focus.

## Review
- [ ] The overlay is under about 10 KB, tiled and non-interactive.
- [ ] Text contrast is rechecked with grain on.
- [ ] No animated grain for reduced-motion users.
- [ ] No continuous repaint in the profile.
