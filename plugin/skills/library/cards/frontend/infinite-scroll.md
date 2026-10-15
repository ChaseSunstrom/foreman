---
name: infinite-scroll
title: Infinite scroll
area: frontend
tags: [pagination, intersection-observer, scroll, lists, a11y]
detect: [dep:react-infinite-scroll-component]
related: [virtualized-lists, skeleton-loading, error-boundaries, keyboard-navigation]
---
Load more on scroll with an IntersectionObserver sentinel, bounded memory, restorable position and a keyboard path.

## Verify
- `npx playwright test`: scrolls to the end and asserts pages append once each.
- `npx tsc --noEmit`: cursor and page types.
- `npx vitest run`: the fetch-more guard logic (no duplicate or concurrent fetches).

## Test first
Reaching the sentinel loads exactly one next page.
```ts
import { test, expect } from '@playwright/test';

test('scrolling to the sentinel fetches one more page', async ({ page }) => {
  let calls = 0;
  await page.route('**/api/items?*', r => { calls++; r.continue(); });
  await page.goto('/feed');
  await expect(page.getByRole('article')).toHaveCount(20);
  await page.getByTestId('sentinel').scrollIntoViewIfNeeded();
  await expect(page.getByRole('article')).toHaveCount(40);
  expect(calls).toBe(2);
});
```

## Do
- Observe a sentinel element after the list with `IntersectionObserver` (`rootMargin: '400px'`), not a scroll listener.
- Use cursor pagination from the API; keep `isFetching` and `hasNextPage` guards so one trigger fires one request.
- Provide a visible "Load more" button as a fallback and for keyboard users; auto-load only on top of it.
- Reserve space for the next page with skeleton rows to avoid shift.
- Show loading, end-of-list ("You are all caught up") and error with retry states; announce them in a `role="status"` region.
- Keep the footer reachable: do not load content under it, or use a button.
- Store scroll offset and loaded pages (URL cursor or cache) so Back restores position.
- Cap memory: virtualize or drop far-off pages from a very long feed.

## Avoid
- A `scroll` listener reading `scrollTop` and `offsetHeight` per event: layout thrash, duplicate fetches. Use the observer.
- Triggering while a request is in flight: duplicate pages. Guard on in-flight state.
- Silent failure: the list just stops. Show an error row with retry.
- Infinite scroll with a footer the user needs: it is unreachable. Use a button or sticky footer.
- Offset pagination for feeds that change: items repeat or skip. Use cursors and dedupe by id.
- Appending above the viewport: content jumps. Only append below, or compensate scroll.
- No keyboard access: an observer-only design strands keyboard users. Keep the button focusable.

## Review
- [ ] One trigger produces one fetch; the guard is tested.
- [ ] Loading, empty, end and error states exist and are announced.
- [ ] A button path exists for keyboard and no-observer cases.
- [ ] Back navigation restores position.
- [ ] Items dedupe by id and memory is bounded.
