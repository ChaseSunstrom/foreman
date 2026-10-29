---
name: svg-animation
title: SVG Animation
area: frontend
tags: [svg, animation, stroke-dashoffset, smil, lottie, motion]
detect: [dep:lottie-web, dep:@lottiefiles/dotlottie-web, dep:svgator]
related: [svg-canvas, animation, progress-indicators, accessibility, web-performance]
---
Animate SVG with CSS and WAAPI: stroke drawing, transform-box fixes, morphing paths, and when Lottie is worth its weight.

## Verify
- `npx svgo --multipass icon.svg -o icon.min.svg`: shrinks the file and keeps IDs you animate by config.
- `npx playwright test --grep svg`: asserts the end-state attributes under reduced motion.
- `ls -l public/*.json public/*.svg`: Lottie JSON beyond about 100 KB deserves a second look.

## Test first
```ts
import { test, expect } from '@playwright/test';

test.use({ reducedMotion: 'reduce' });

test('checkmark is fully drawn without animation', async ({ page }) => {
  await page.goto('/');
  const off = await page.locator('#check path').evaluate(
    el => getComputedStyle(el).strokeDashoffset);
  expect(parseFloat(off)).toBe(0);
});
```

## Do
- Draw a line: `pathLength="1"` on the path, `stroke-dasharray: 1; stroke-dashoffset: 1;` then animate offset to 0. It works for any path length.
- Rotate or scale around the element's own center: `transform-box: fill-box; transform-origin: center;`.
- Animate `transform` and `opacity` for smooth results; `stroke-dashoffset` repaints but is cheap for small icons.
- Morph paths only between paths with the same command structure; CSS `d: path(...)` transitions work in Chromium, elsewhere use a library.
- Inline critical SVG so CSS can reach it; use `<img>` for decorative files, which cannot be styled but cache well.
- Set `role="img"` with `<title>` when meaningful; `aria-hidden="true"` when decorative.
- Pick Lottie only for designer-made multi-layer scenes; the player costs about 50 KB gzip. Use dotLottie for smaller files.
- Pause when off-screen (IntersectionObserver) and under `prefers-reduced-motion`.

## Avoid
- SMIL for new work as the sole mechanism: deprecation talk resurfaces, and CSS and WAAPI cover it.
- Animating filters or blur on large SVGs per frame: repaint heavy.
- Thousands of animated nodes; move to canvas.
- Missing `viewBox`, which breaks scaling.
- Autoplay loops with no pause.

## Review
- [ ] Reduced-motion users see the final drawn state.
- [ ] Meaningful graphics have a text alternative; decorative ones are hidden.
- [ ] SVGs were optimized and animated nodes are few.
- [ ] Lottie or library cost justified against CSS.
