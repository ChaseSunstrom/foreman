---
name: search-ux
title: Search UX
area: ux
tags: [search, query, results, autocomplete, product-design]
detect: []
related: [filters-and-facets, search-autocomplete, command-palette, empty-states]
---
Make search forgiving and fast: visible box, typo tolerance, ranked results with highlights, and a useful zero-result page.

## Verify
- `npx playwright test --grep search`: types a query, checks results, highlighting, and the zero-result view.
- `grep -rn "debounce" src/search`: input is debounced (150-300 ms) and stale responses are dropped.
- Query log review: list the top 20 zero-result queries weekly and fix synonyms.
- `npx lighthouse http://localhost:3000/search?q=test --only-categories=performance`: results render under 1 s on mid hardware.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('typo still finds the item and highlights the match', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('searchbox').fill('invioce');
  await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name: /results for/i })).toBeVisible();
  await expect(page.locator('mark').first()).toContainText(/invoice/i);
});

test('no results suggests a next step', async ({ page }) => {
  await page.goto('/search?q=qqqqzz');
  await expect(page.getByText(/no results for/i)).toBeVisible();
  await expect(page.getByRole('link', { name: /clear|browse/i })).toBeVisible();
});
```

## Do
- Show a visible search box (a magnifier icon alone is a poor target); `type="search"` with a label and `role="search"`.
- Keep the query in the URL (`?q=`) so results are shareable and Back works.
- Tolerate typos, plurals and synonyms; rank exact title matches first.
- Highlight matched terms and show a snippet, the result count and the active query.
- Support `/` or Cmd/Ctrl+K to focus search; Enter submits, Esc clears.
- Preserve the query and filters when the user returns from a result.
- Show recent searches on focus; offer suggestions after 2-3 characters.

## Avoid
- Clearing the box on submit or on a failed search.
- A dead "No results" with no clear, spell fix or alternate path.
- Firing a request per keystroke with no cancellation: results arrive out of order.
- Autocomplete that steals Enter for a suggestion the user did not choose.
- Infinite scroll for results the user needs to compare or return to.

## Review
- [ ] Query lives in the URL; Back restores results and scroll.
- [ ] Zero-result page offers a way forward and is logged.
- [ ] Keyboard path works end to end; announcements via `aria-live` for counts.
- [ ] Stale responses are ignored.
