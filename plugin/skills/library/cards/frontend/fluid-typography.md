---
name: fluid-typography
title: Fluid Typography
area: frontend
tags: [css, clamp, typography, responsive, rem, container-units]
detect: []
related: [typography, responsive-design, container-queries, accessibility, css-custom-properties]
---
Scale type smoothly between two viewport widths with clamp(), keeping rem in the formula so user zoom still works.

## Verify
- `npx playwright test --grep fluid-type`: resizes the viewport (320, 768, 1440 px) and asserts computed font sizes stay within bounds.
- `grep -rnE "font-size: *[0-9.]+vw" src`: pure viewport units that ignore user font settings.
- `npx lighthouse http://localhost:3000 --only-categories=accessibility`: checks zoom is not disabled.

## Test first
```ts
import { test, expect } from '@playwright/test';

for (const [w, min, max] of [[320, 16, 17], [1440, 40, 48]]) {
  test(`h1 size at ${w}px stays in range`, async ({ page }) => {
    await page.setViewportSize({ width: w, height: 800 });
    await page.goto('/');
    const px = await page.locator('h1').evaluate(e => parseFloat(getComputedStyle(e).fontSize));
    expect(px).toBeGreaterThanOrEqual(min);
    expect(px).toBeLessThanOrEqual(max);
  });
}
```

## Do
- Formula: `font-size: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);` where the middle term adds a rem base to a vw slope, so browser zoom and default-size changes still scale it.
- Compute the slope: between 320 px and 1280 px, sizes 16 and 24 px give `slope = (24-16)/(1280-320) = 0.00833` so `0.833vw`, intercept `16 - 320*0.00833 = 13.33 px = 0.833rem`.
- Define a scale as tokens (`--step-0` through `--step-5`) with a ratio of about 1.2 on small screens to 1.333 on large.
- Use container units (`cqi`) inside container-query components so type responds to its box, with a `vw` fallback.
- Line length 45-75 characters via `max-inline-size: 65ch`; line-height 1.4-1.6 for body, 1.1-1.2 for display.
- Apply `text-wrap: balance` to headings and `pretty` to paragraphs.
- Fluid spacing in the same way with `clamp()`.

## Avoid
- `font-size: 5vw` alone: no minimum, no zoom support (WCAG 1.4.4 failure).
- Maximums that make text static at 200% zoom; the user's zoom must change the result.
- Fluid body text across a huge range; body should move at most about 2 px.
- `px` bounds mixed with `vw`: ignores user preferences.
- Fluid sizes on elements with fixed-height boxes; text overflows.

## Review
- [ ] Browser zoom to 200% and text-only zoom both enlarge text.
- [ ] Sizes were checked at 320, 768 and 1440 px for wrapping and overflow.
- [ ] Min and max values come from tokens, in rem.
- [ ] Line length stays within roughly 45-75 characters.
