---
name: data-tables
title: Data tables
area: frontend
tags: [table, grid, sorting, a11y, pagination]
detect: [dep:@tanstack/react-table]
related: [virtualized-lists, keyboard-navigation, aria-patterns, skeleton-loading]
---
Accessible, sortable, paginated tables on real `<table>` semantics, with state in the URL and stable row ids.

## Verify
- `npx playwright test`: sorts, pages and filters, then asserts the rows and `aria-sort`.
- `npx @axe-core/cli http://localhost:3000`: header associations and captions.
- `npx tsc --noEmit`: column definitions and row types.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('sorting by name sets aria-sort and orders rows', async ({ page }) => {
  await page.goto('/users');
  await page.getByRole('button', { name: 'Name' }).click();
  await expect(page.getByRole('columnheader', { name: 'Name' })).toHaveAttribute('aria-sort', 'ascending');
  const first = page.getByRole('row').nth(1);
  await expect(first).toContainText('Ada');
  await page.getByRole('button', { name: 'Name' }).click();
  await expect(page.getByRole('columnheader', { name: 'Name' })).toHaveAttribute('aria-sort', 'descending');
});
```

## Do
- Use `<table>`, `<caption>`, `<thead>`, `<th scope="col">` and `<th scope="row">`; do not rebuild tables from `div`s.
- Make sortable headers a `<button>` inside `<th>`, and set `aria-sort="ascending|descending|none"` on the `<th>`.
- Give each row a stable `id` (`getRowId`) so selection and expansion survive sort and refetch.
- Keep sort, filter, page and page size in the URL query; debounce text filters.
- Paginate or virtualize anything above a few hundred rows; show "Showing 21 to 40 of 312".
- Select rows with real checkboxes labelled by the row ("Select Ada Lovelace") plus a select-all with indeterminate state.
- Wrap in a focusable scroll container (`tabindex="0"`, labelled) for horizontal overflow; pin the first column with `position: sticky`.
- Provide empty, loading (same-size skeleton rows) and error states inside `<tbody>`.
- Right-align numbers with `font-variant-numeric: tabular-nums`.

## Avoid
- `div` grids with `onClick` rows: no semantics or keyboard. Use a table, and a button or link in the row for the action.
- Sorting only the current page while the label implies all data: server-sort or say so.
- Index-based row keys: selection sticks to positions after sorting. Use ids.
- Click handlers on the whole `<tr>` with nested links: double actions and no keyboard path. Put one link in the primary cell.
- Using `display: block` on table parts to make them responsive: removes table semantics. Use scroll or a card layout at small widths.
- A loading state that replaces the table with a spinner: layout shifts. Keep headers and skeleton rows.

## Review
- [ ] Native table elements with captions and header scopes.
- [ ] Sort state is exposed with `aria-sort` and in the URL.
- [ ] Row ids are stable and selection is labelled.
- [ ] Large data is paginated or virtualized.
- [ ] Empty, loading and error states are visible and sized.
