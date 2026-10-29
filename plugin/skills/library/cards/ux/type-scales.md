---
name: type-scales
title: Modular Type Scales
area: ux
tags: [ux, typography, modular-scale, fluid-type, line-height, measure]
detect: []
related: [typography, type-pairing, spacing-scales, responsive-design, css-custom-properties]
---
Font sizes from one ratio (1.2, 1.25 or 1.333), fluid with `clamp()`, body measure 45-75 characters.

## Verify
- `grep -rnoE "font-size: *[0-9.]+(px|rem)" src --include=*.css | grep -v "var(--"`: finds sizes outside the scale.
- `npx playwright test --grep measure`: checks line length of paragraphs.
- Devtools computed pane at 320 and 1440 px: headings scale, body stays 16-18px.

## Test first
Assert the measure and body size.
```ts
import { test, expect } from '@playwright/test';

test('body text is 16px+ with a 45-75 char measure', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto('/article');
  const p = page.locator('article p').first();
  const px = await p.evaluate(e => parseFloat(getComputedStyle(e).fontSize));
  expect(px).toBeGreaterThanOrEqual(16);
  const ch = await p.evaluate(e => {
    const c = parseFloat(getComputedStyle(e).fontSize) * 0.5;
    return e.getBoundingClientRect().width / c;
  });
  expect(ch).toBeLessThanOrEqual(80);
});
```

## Do
- Pick the ratio by density: 1.2 minor third for apps and dashboards, 1.25 major third for content, 1.333 perfect fourth for marketing.
- Base 1rem (16px); steps: 0.833, 1, 1.25, 1.563, 1.953, 2.441 rem for ratio 1.25.
- Make headings fluid: `font-size: clamp(2rem, 1.2rem + 3vw, 3.5rem)`; keep body fixed.
- Use `rem`, so user font settings scale the page; never set root size in px.
- Body line-height 1.5-1.6; headings 1.1-1.25; tighten letter-spacing slightly (-0.01em to -0.02em) on large headings.
- Limit measure with `max-width: 65ch` on prose.
- Set `text-wrap: balance` on headings and `text-wrap: pretty` on paragraphs.

## Avoid
- A size per component picked by eye: the scale decays.
- Viewport units alone for size (`3vw`): breaks zoom accessibility; mix with rem in `clamp()`.
- Line-height in px: wrong once the size changes.
- Body text under 16px on mobile, or all-caps paragraphs.

## Review
- [ ] Every `font-size` is a scale token; the ratio is named in the token file.
- [ ] Prose measure is 45-75 characters at desktop width.
- [ ] Text scales to 200% zoom without clipping or overlap.
- [ ] Line-heights are unitless.
