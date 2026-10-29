---
name: chart-design
title: Chart Design
area: ux
tags: [ux, charts, data-viz, accessibility, color]
detect: []
related: [d3, recharts, color-palettes, color-contrast, accessibility, data-tables]
---
Charts that answer one question: the right chart type, a zero baseline for bars, direct labels, a color-blind-safe palette.

## Verify
- `npx playwright test --grep chart`: checks each chart has a title, an accessible name and a data table fallback.
- `grep -rn "scaleLinear().domain(\[[1-9]" src`: bar charts whose y domain does not start at 0.
- Colour vision: write a script that applies a deuteranopia matrix to each series colour and fails when two series differ by less than about 20 in CIE76 distance; or emulate it in devtools (Rendering, Emulate vision deficiencies).
- `npx @axe-core/cli http://localhost:3000/reports`: no failures on chart containers.

## Test first
Assert the chart is labeled and has a text equivalent.
```ts
import { test, expect } from '@playwright/test';

test('chart has title, name and data table', async ({ page }) => {
  await page.goto('/reports');
  const fig = page.locator('figure[data-chart]').first();
  await expect(fig.locator('figcaption')).not.toBeEmpty();
  await expect(fig.locator('svg')).toHaveAttribute('role', 'img');
  await expect(fig.locator('svg')).toHaveAttribute('aria-label', /.+/);
  await expect(fig.locator('details table')).toHaveCount(1);
});
```

## Do
- Start from the question; the title states the finding ("Signups doubled in March"), not the field name.
- Match type to task: line for trend, bar for comparison, scatter for relation, table for exact values; sort bars by value.
- Bars start at zero; lines may truncate the axis, with the break visible.
- Label directly at line ends instead of a distant legend; keep gridlines light (about 10 percent ink) and drop chart borders.
- Max 5-6 series; mute the rest in gray and highlight the one that matters.
- Use a sequential palette for ordered data, diverging for around-a-midpoint, qualitative only for categories; use colorblind-safe sets (e.g. Okabe-Ito).
- Add pattern, shape or direct labels as a second channel besides color.
- Wrap in `<figure>` with `<figcaption>`, give the svg `role="img"` and an `aria-label` summary, offer a data table in `<details>`.
- Format numbers with `Intl.NumberFormat` (compact, locale, units); axis ticks 4-7.

## Avoid
- Pie charts above 5 slices, 3D, dual y axes that imply false correlation.
- Rainbow palettes; red/green as the only contrast.
- Tooltips as the only way to read values (no touch or keyboard).
- Animation on every update; respect reduced motion.

## Review
- [ ] The title states the takeaway and units are visible.
- [ ] Bars start at zero; axes and tick counts are readable at 375 px.
- [ ] Series stay distinguishable under color-blind simulation.
- [ ] A text alternative or data table is available.
