---
name: information-architecture
title: Information Architecture
area: ux
tags: [information-architecture, card-sorting, taxonomy, sitemap, product-design]
detect: []
related: [navigation-patterns, usability-testing, search-ux, mobile-navigation]
---
Organise content around how users think: test the structure with card sorting and tree testing before building navigation.

## Verify
- `npx playwright test --grep sitemap`: crawls the nav and asserts no page is deeper than 3 clicks from home.
- `npx broken-link-checker http://localhost:3000 -ro`: finds dead links; cross-check the sitemap against nav links to find orphan pages.
- Tree test (Optimal Workshop or Maze): target at least 70% direct success on top tasks.
- Compare search queries to labels: frequent queries that miss mean a label mismatch.

## Test first
```ts
import { test, expect } from '@playwright/test';
test('every internal page is within 3 clicks of home', async ({ page }) => {
  const seen = new Map<string, number>([['/', 0]]);
  let frontier = ['/'];
  for (let depth = 1; depth <= 4; depth++) {
    const next: string[] = [];
    for (const path of frontier) {
      await page.goto(path);
      const hrefs = await page.locator('a[href^="/"]').evaluateAll(
        as => as.map(a => new URL((a as HTMLAnchorElement).href).pathname));
      for (const h of hrefs) if (!seen.has(h)) { seen.set(h, depth); next.push(h); }
    }
    frontier = next;
  }
  const deep = [...seen].filter(([, d]) => d > 3);
  expect(deep).toEqual([]);
});

test('top task is reachable from home', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('link', { name: 'Billing' }).click();
  await page.getByRole('link', { name: 'Download invoice' }).click();
  await expect(page).toHaveURL(/invoices/);
});
```

## Do
- List the top 10 user tasks from research and analytics; the structure must serve them first.
- Run an open card sort (15-30 participants) to learn groupings, then a closed sort or tree test to validate labels.
- Use broad and shallow over narrow and deep, but keep each level to about 7 items.
- Name categories with user vocabulary, mutually exclusive where possible, and give each page one home with cross-links for the rest.
- Make URLs mirror the hierarchy (`/billing/invoices/42`), stable and human readable; keep redirects for moves.
- Provide multiple routes: navigation, search, related links, breadcrumbs.
- Keep a sitemap and content inventory document and review it every release or quarter.

## Avoid
- Mirroring the org chart or the codebase modules in the menu.
- Catch-all buckets such as "Resources" or "Misc".
- Moving pages without redirects.
- Deciding structure by internal vote instead of user testing.
- Burying a top task at depth 4 or more.

## Review
- [ ] Top tasks are within 3 clicks and tested by tree test.
- [ ] Labels use user language, and each item has one canonical home.
- [ ] URLs are stable; moves are redirected.
- [ ] Search logs feed back into labels.
