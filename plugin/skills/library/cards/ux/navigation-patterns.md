---
name: navigation-patterns
title: Navigation Patterns
area: ux
tags: [navigation, menus, wayfinding, breadcrumbs, product-design]
detect: []
related: [information-architecture, mobile-navigation, keyboard-navigation, accessibility]
---
Pick one primary navigation pattern, keep it to 3-7 items, and always show where the user is.

## Verify
- `npx playwright test --grep navigation`: asserts `aria-current="page"` on the active link on every route.
- `grep -rn "<nav" src | wc -l`: each nav landmark exists; multiple navs carry distinct `aria-label`s.
- `npx axe-core-cli http://localhost:3000`: landmark and link-name rules pass.
- Tab through the header: focus order matches visual order and skip link is first.

## Test first
Assert wayfinding, not markup.
```ts
import { test, expect } from '@playwright/test';

test('current section is marked in the nav', async ({ page }) => {
  await page.goto('/billing/invoices');
  const nav = page.getByRole('navigation', { name: 'Main' });
  await expect(nav.getByRole('link', { name: 'Billing' })).toHaveAttribute('aria-current', 'page');
});

test('skip link is first tab stop', async ({ page }) => {
  await page.goto('/');
  await page.keyboard.press('Tab');
  await expect(page.getByRole('link', { name: /skip to content/i })).toBeFocused();
});
```

## Do
- Keep top-level items to 3-7 (Miller-style limit for scanning); group the rest under a clear parent or a "More" menu.
- Label with the user's nouns ("Invoices"), not internal names ("Ledger module").
- Mark the current page visibly and with `aria-current="page"`.
- Use breadcrumbs for hierarchies deeper than 2 levels; the last crumb is the current page, not a link.
- Use top bar for few, flat destinations; a sidebar for many (8+) or deep ones; tabs for views of the same object.
- Keep nav position and order identical on every page.
- Provide a "skip to main content" link and a search entry when content exceeds about 50 pages.

## Avoid
- Hover-only mega menus: unreachable by touch and keyboard.
- Mixing three nav systems on one page (top, side, tabs) with no clear hierarchy.
- Icon-only items without a label or tooltip text.
- Reordering items by usage; it breaks muscle memory.
- Opening external links in the same tab from inside the nav with no cue.

## Review
- [ ] Top level has 7 items or fewer; labels are user words.
- [ ] Current location is visible without color alone.
- [ ] Every item is reachable by keyboard and touch (44 px target).
- [ ] Back button and deep links behave; no trapped state.
- [ ] Mobile pattern is decided (see mobile-navigation).
