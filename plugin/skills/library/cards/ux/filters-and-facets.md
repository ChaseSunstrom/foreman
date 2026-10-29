---
name: filters-and-facets
title: Filters and Facets
area: ux
tags: [filters, facets, faceted-search, sorting, product-design]
detect: []
related: [search-ux, data-tables, pagination, empty-states]
---
Let users narrow a large set with visible, reversible, countable filters whose state lives in the URL.

## Verify
- `npx playwright test --grep filter`: applies a filter, checks the count, reloads, and expects the same state.
- `grep -rn "useSearchParams\|URLSearchParams" src/filters`: filter state is serialised to the URL.
- `npx axe-core-cli http://localhost:3000/products`: filter groups are labelled and operable by keyboard.
- Throttle to Slow 3G: applying a filter shows progress, not a frozen list.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('filter persists in URL and can be cleared', async ({ page }) => {
  await page.goto('/products');
  await page.getByRole('checkbox', { name: /in stock/i }).check();
  await expect(page).toHaveURL(/inStock=true/);
  await page.reload();
  await expect(page.getByRole('checkbox', { name: /in stock/i })).toBeChecked();
  await page.getByRole('button', { name: /clear all/i }).click();
  await expect(page).not.toHaveURL(/inStock/);
});
```

## Do
- Show active filters as removable chips above the results, with a "Clear all".
- Show counts per option ("Blue (12)") and disable or hide options with zero.
- Apply instantly on desktop; on mobile use a sheet with an explicit "Show 48 results" apply button.
- OR within a group (colors), AND across groups (color and size); say so if unclear.
- Put the 3-5 most used filters first; collapse the rest with progressive disclosure.
- Offer sort separately from filter; default sort should be stated.
- Reset to page 1 when filters change; keep the sort.

## Avoid
- Filters that apply silently with no result count change or loading cue.
- Combinations that lead to zero results without telling which filter caused it.
- Hiding active filters inside a closed panel.
- Storing filter state only in component memory: reload and share both break.
- Dozens of facets shown at once; users do not read them.

## Review
- [ ] State is URL-driven, shareable and restored by Back.
- [ ] Counts update and match the real result set.
- [ ] Chips, labels and groups are accessible by keyboard and screen reader.
- [ ] Zero-result state explains and offers to remove a filter.
