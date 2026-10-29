---
name: empty-states
title: Empty States
area: ux
tags: [empty-state, zero-data, first-use, product-design]
detect: []
related: [onboarding-flows, skeleton-loading, error-messages, ux-writing]
---
Treat "nothing here" as a screen to design: say why it is empty, and offer the one next action.

## Verify
- `npx playwright test --grep "empty state"`: renders each list with zero rows and asserts the message and primary action.
- `grep -rn "No data\|No results\|Nothing found" src`: finds bare, unhelpful empty text to rewrite.
- Seed the dev database empty and click through every list, table and chart once.
- `npx @axe-core/cli http://localhost:3000/projects`: the empty view has a heading and a reachable action.

## Test first
Separate the four empties and assert each has different copy.
```ts
import { test, expect } from '@playwright/test';

test('first-use empty state offers a create action', async ({ page }) => {
  await page.goto('/projects');
  await expect(page.getByRole('heading', { name: /no projects yet/i })).toBeVisible();
  await page.getByRole('button', { name: /create project/i }).click();
  await expect(page).toHaveURL(/projects\/new/);
});

test('empty search result names the query and offers clear', async ({ page }) => {
  await page.goto('/projects?q=zzzz');
  await expect(page.getByText(/no results for .zzzz./i)).toBeVisible();
  await expect(page.getByRole('link', { name: /clear search/i })).toBeVisible();
});
```

## Do
- Distinguish first-use (nothing created), no-results (filter or search), cleared (user finished, such as inbox zero) and error (load failed); each gets its own copy.
- Use a short headline, one sentence of benefit, and a single primary button.
- Keep the layout of the populated state visible (column headers, filters) so the page does not jump when data arrives.
- For no-results, echo the query and offer to clear filters or widen the search.
- Use a small illustration or icon only if it is `aria-hidden`; the text carries the meaning.
- Pre-fill sample data or a template link when the product is hard to judge empty.

## Avoid
- A blank panel or a lone "No data" string.
- Showing an empty state while data is still loading: use a skeleton, then switch.
- Two equal-weight buttons; the user should see one next step.
- Blaming the user ("You have not added anything").
- A giant illustration that pushes the action below the fold at 375 px width.

## Review
- [ ] All four empty kinds are distinct and tested.
- [ ] The primary action works and is keyboard reachable.
- [ ] No flash of empty state before the loading state resolves.
- [ ] Copy reads well at 320 px width.
