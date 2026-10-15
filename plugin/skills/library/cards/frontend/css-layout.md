---
name: css-layout
title: CSS Layout
area: frontend
tags: [css, grid, flexbox, layout, container-queries, stylelint]
detect: [ext:.css, ext:.scss, dep:stylelint, dep:sass, dep:postcss]
related: [responsive-design, design-systems, accessibility, animation]
---
Modern CSS layout: Grid for two dimensions, Flexbox for one, logical properties, container queries, no layout hacks.

## Verify
- `npx stylelint "**/*.{css,scss}"`: syntax errors, duplicate or invalid properties, per project config.
- `npx playwright test --grep layout`: screenshot or bounding-box assertions at set viewports.
- `npx prettier --check "**/*.css"`: formatting.
- Browser devtools Layout panel: confirm which grid or flex container owns each item.

## Test first
Assert geometry at fixed viewports instead of eyeballing.
```ts
import { test, expect } from '@playwright/test';

test('cards wrap to one column on phones', async ({ page }) => {
  await page.setViewportSize({ width: 360, height: 800 });
  await page.goto('/');
  const [a, b] = await page.locator('.card').all();
  const A = (await a.boundingBox())!, B = (await b.boundingBox())!;
  expect(B.y).toBeGreaterThan(A.y + A.height - 1);
  const w = await page.evaluate(() => document.documentElement.scrollWidth);
  expect(w).toBeLessThanOrEqual(360);
});
```

## Do
- Grid for page and component structure: `grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr))` gives responsive columns without media queries.
- Flexbox for rows of items; set `gap`, not margins on children.
- Use logical properties (`margin-inline`, `padding-block`, `inset-inline-start`) so RTL works.
- `min-height: 100dvh` for full-height sections on mobile; `svh` or `lvh` when you need a fixed bound.
- `aspect-ratio` for media boxes; `object-fit: cover` for images inside.
- `@container` queries with `container-type: inline-size` for components that depend on their slot, not the viewport.
- `min-width: 0` on flex or grid children that hold long text or code.
- `position: sticky` needs an ancestor without overflow clipping.

## Avoid
- `height: 100vh` on mobile: the address bar causes jump and clipping. Use `dvh`.
- Floats and `clear` for layout, or `position: absolute` centering: use grid `place-items: center`.
- Fixed pixel widths on containers: causes horizontal scroll at 320px. Use `max-width` and `%` or `min()`.
- `z-index: 9999` escalation: create stacking contexts deliberately (`isolation: isolate`) and keep a small scale.
- `overflow: hidden` to hide a layout bug: it clips focus rings and breaks sticky. Find the overflowing child.
- Grid items blowing out with `1fr`: use `minmax(0, 1fr)`.
- Magic negative margins: restructure with gap or grid areas.

## Review
- [ ] No horizontal scroll at 320px width and 200% zoom.
- [ ] Spacing uses `gap` and a token scale, not per-element margins.
- [ ] Logical properties used, layout survives `dir="rtl"`.
- [ ] Long strings (German words, URLs) wrap or truncate intentionally.
- [ ] Stacking contexts and z-index values are documented.
