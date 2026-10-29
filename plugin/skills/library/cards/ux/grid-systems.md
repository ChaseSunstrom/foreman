---
name: grid-systems
title: Layout Grid Systems
area: ux
tags: [ux, grid, layout, css-grid, columns, baseline]
detect: []
related: [css-layout, responsive-design, container-queries, spacing-scales, bento-grids]
---
A 12-column grid with fixed gutters and margins, built on CSS Grid, so every edge lines up at every breakpoint.

## Verify
- `grep -rnE "grid-template-columns: *repeat\((12|4|8)" src`: the grid is defined once, in tokens or a layout component.
- `npx playwright test --grep grid`: asserts column edges at 375, 768 and 1280 px.
- Devtools Grid overlay on the page: items snap to tracks, none float between.

## Test first
Assert that content left edges land on shared x positions.
```ts
import { test, expect } from '@playwright/test';

for (const w of [375, 768, 1280]) {
  test(`cards align to the grid at ${w}px`, async ({ page }) => {
    await page.setViewportSize({ width: w, height: 900 });
    await page.goto('/');
    const xs = await page.$$eval('[data-card]', els =>
      [...new Set(els.map(e => Math.round(e.getBoundingClientRect().x)))]);
    expect(xs.length).toBeLessThanOrEqual(w < 768 ? 1 : w < 1100 ? 2 : 4);
  });
}
```

## Do
- Columns: 4 below 640px, 8 at 640-1023px, 12 from 1024px. Gutter 16px on mobile, 24px on desktop; margins 16 / 32 / auto.
- Cap the container at 1200-1280px; let text columns span 6-8 of 12 for a readable measure.
- Use `display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: var(--gutter)` and place with `grid-column: span N`.
- Use `repeat(auto-fit, minmax(16rem, 1fr))` for card lists that need no fixed count.
- Nest with `subgrid` so inner rows align with the outer tracks.
- Keep vertical rhythm on a 4 or 8px baseline (see spacing-scales).

## Avoid
- Magic widths (`width: 487px`) and negative margins to fake alignment.
- Different gutters per component: edges drift off the grid.
- Flexbox percentage columns with margins: wrap bugs; use grid gap.
- Breaking the grid on purpose without a reason a reviewer can state.

## Review
- [ ] Every element's left and right edge sits on a column line at 3 widths.
- [ ] Gutter and margin values come from tokens, defined once.
- [ ] Container is capped and centered; no horizontal scroll at 320px.
- [ ] Any off-grid element is deliberate and noted in a comment.
