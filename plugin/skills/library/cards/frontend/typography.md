---
name: typography
title: Web typography
area: frontend
tags: [css, fonts, typography, font-display, responsive]
detect: [dep:@fontsource/inter]
related: [layout-shift, css-custom-properties, image-optimization, web-performance]
---
Readable, fast-loading type: fluid scale, relative units, controlled font loading and fallback metrics.

## Verify
- `npx playwright test`: asserts computed font size, line height and no shift when the font swaps.
- `npx lhci autorun`: font-display and layout-shift audits, if configured.
- `grep -rnE "font-size:\s*[0-9.]+px" src`: pixel font sizes that ignore user settings.

## Test first
Text must scale with the user's root font size.
```ts
import { test, expect } from '@playwright/test';

test('body copy follows the root font size', async ({ page }) => {
  await page.setContent(`<style>html{font-size:200%}p{font-size:1rem}</style><p>hello</p>`);
  const px = await page.locator('p').evaluate(e => parseFloat(getComputedStyle(e).fontSize));
  expect(px).toBeGreaterThanOrEqual(32);
});
```

## Do
- Size in `rem`; leave `html` at the default or a percentage, never fixed `px`.
- Build a fluid scale with `clamp(1rem, 0.9rem + 0.5vw, 1.25rem)`; include a `rem` term so zoom still works.
- Body line height 1.4 to 1.6 unitless; measure 45 to 75 characters (`max-width: 65ch`).
- Self-host WOFF2, subset to needed glyphs, `<link rel="preload" as="font" type="font/woff2" crossorigin>` for the one or two critical files.
- Set `font-display: swap` (or `optional` for non-critical) and tune a fallback with `size-adjust`, `ascent-override`, `descent-override` to cut shift.
- Use a system stack fallback; prefer variable fonts over many static weights.
- Use `text-wrap: balance` on headings and `text-wrap: pretty` on paragraphs where supported.
- Set `lang` on `<html>` so hyphenation and quotes work; use `hyphens: auto` with it.

## Avoid
- `user-scalable=no` or `maximum-scale=1`: blocks pinch zoom. Remove them.
- Font preload without `crossorigin`: the file downloads twice. Add the attribute.
- Fixed `px` heights on text containers: scaled text overflows. Use `min-height` or none.
- Loading six weights and italics up front: each is a request. Ship the variable file or two weights.
- Letter-spacing in `px` on body copy and all-caps without spacing: use `em`.
- `font-display: block` on body text: invisible text for seconds on slow networks.

## Review
- [ ] No fixed pixel font sizes; 200% zoom keeps layout usable.
- [ ] Only critical fonts are preloaded, with `crossorigin`.
- [ ] Fallback metrics are tuned so swap causes no visible shift.
- [ ] Line length and height meet readability targets.
- [ ] Fonts are WOFF2, subsetted, self-hosted.
