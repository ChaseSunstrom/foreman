---
name: dashboard-design
title: Dashboard Design
area: ux
tags: [dashboard, data-visualization, metrics, kpi, product-design]
detect: []
related: [data-tables, skeleton-loading, empty-states, color-contrast]
---
A dashboard answers a question at a glance: few metrics, clear comparisons, honest charts, drill-down on demand.

## Verify
- `npx playwright test --grep dashboard`: loads with seeded data and asserts each KPI, its delta and the date range label.
- `npx lighthouse http://localhost:3000/dashboard --only-categories=performance`: LCP under 2.5 s with data.
- `grep -rn "toFixed\|Intl.NumberFormat" src/dashboard`: numbers use one formatter, with units.
- Squint test: blur the screenshot; the most important number should still stand out.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('KPI shows value, comparison and period', async ({ page }) => {
  await page.goto('/dashboard?range=30d');
  const card = page.getByRole('group', { name: 'Revenue' });
  await expect(card).toContainText('$12,400');
  await expect(card).toContainText(/\+8% vs previous 30 days/);
});

test('chart has a table alternative', async ({ page }) => {
  await page.goto('/dashboard');
  await page.getByRole('button', { name: /view as table/i }).first().click();
  await expect(page.getByRole('table')).toBeVisible();
});
```

## Do
- Start from the user's top 3 questions; put the answer to the first at top left.
- Show 4-6 KPIs, each with value, unit, comparison to a prior period and the time range.
- Pick the chart for the question: line for trend, bar for comparison, table for exact lookup; avoid pie beyond 3-4 slices.
- Start bar axes at zero; label axes and units; keep the same color for the same series everywhere.
- Offer a shared date range, with a stated default, and keep it in the URL.
- Drill from a number to the rows behind it.
- Provide a table or text alternative for each chart, and do not use color as the only encoding (contrast 3:1 for graphics).
- Load each widget independently with a skeleton, with stale-data timestamps.

## Avoid
- Twenty tiles with equal weight; nothing wins attention.
- 3D charts, dual axes that mislead, truncated bar axes.
- Real-time updates that move numbers under the cursor.
- Metrics with no definition; add a tooltip with the formula.
- Auto-refreshing with no pause, which hurts readers using assistive tech.

## Review
- [ ] Each widget answers a named question and cites its period.
- [ ] Charts have accessible alternatives and pass color contrast.
- [ ] Loading, empty and error states exist per widget.
- [ ] Numbers format by locale and agree with the source of truth.
