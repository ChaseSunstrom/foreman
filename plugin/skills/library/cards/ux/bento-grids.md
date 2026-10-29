---
name: bento-grids
title: Bento Grids
area: ux
tags: [ux, bento, css-grid, layout, cards, responsive]
detect: []
related: [grid-systems, css-layout, container-queries, responsive-design, visual-hierarchy, spacing-scales]
---
A bento layout: mixed-size tiles in one CSS grid, a clear lead tile, equal gaps and a single-column mobile fallback.

## Verify
- `grep -rn "grid-template-areas\|grid-auto-flow: dense" src`: the layout is declared in grid, not positioned by hand.
- `npx playwright test --grep bento`: no overlaps, no gaps, tiles stay inside the container at 375, 768, 1280.
- Devtools Grid overlay: every tile spans whole tracks.

## Test first
```ts
import { test, expect } from '@playwright/test';

for (const w of [375, 768, 1280]) {
  test(`bento tiles do not overlap at ${w}px`, async ({ page }) => {
    await page.setViewportSize({ width: w, height: 900 });
    await page.goto('/features');
    const boxes = await page.$$eval('[data-tile]', els =>
      els.map(e => { const r = e.getBoundingClientRect(); return [r.x, r.y, r.right, r.bottom]; }));
    for (let i = 0; i < boxes.length; i++)
      for (let j = i + 1; j < boxes.length; j++) {
        const [a, b] = [boxes[i], boxes[j]];
        const overlap = a[0] < b[2] - 1 && b[0] < a[2] - 1 && a[1] < b[3] - 1 && b[1] < a[3] - 1;
        expect(overlap).toBe(false);
      }
  });
}
```

## Do
- Use a 4-column grid on desktop, 2 on tablet, 1 on mobile; tiles span 1x1, 2x1, 1x2 or 2x2; the lead tile is the 2x2.
- Declare with `grid-template-columns: repeat(4, 1fr)`, `grid-auto-rows: minmax(12rem, auto)`, `gap: 1rem`; use `grid-template-areas` for fixed compositions.
- Give each tile one idea: a headline, a small visual, at most one line of text.
- Use equal padding (24 px), one radius (16-24 px), and a consistent surface color step so tiles read as one family.
- Let tiles own their layout with `container-type: inline-size` and container queries.
- Order the DOM for reading and keyboard (reading order = visual order on mobile); do not rely on `order` or `dense` to reshuffle meaning.
- Make clickable tiles a single link with a visible focus ring.

## Avoid
- Twelve tiles of equal weight: the pattern becomes noise; cap at 5-7 tiles.
- Fixed pixel heights that clip text on zoom or translation.
- Decorative tiles with no content.
- Hover-only content, and motion in every tile.

## Review
- [ ] Layout is pure grid and has no overlaps at three widths.
- [ ] One lead tile, 5-7 tiles in total, equal gaps and radii.
- [ ] DOM order matches reading order; focus order is sensible.
- [ ] Text reflows at 200% zoom without clipping.
