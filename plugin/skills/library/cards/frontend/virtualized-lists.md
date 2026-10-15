---
name: virtualized-lists
title: Virtualized lists
area: frontend
tags: [performance, virtualization, lists, scroll, a11y]
detect: [dep:@tanstack/react-virtual, dep:react-window]
related: [infinite-scroll, data-tables, drag-and-drop, web-performance]
---
Render only visible rows of long lists, with stable keys, measured sizes, and accessibility preserved.

## Verify
- `npx playwright test`: asserts DOM row count stays small while scrolling through thousands.
- `npx tsc --noEmit`: item and size callback types.
- `npx vitest run`: row renderers and index math are covered.

## Test first
Ten thousand items must not produce ten thousand nodes.
```ts
import { test, expect } from '@playwright/test';

test('only visible rows are in the DOM', async ({ page }) => {
  await page.goto('/big-list');
  const rows = page.getByRole('listitem');
  expect(await rows.count()).toBeLessThan(100);
  await page.getByTestId('scroller').evaluate(e => (e.scrollTop = e.scrollHeight));
  await expect(page.getByText('Item 9999')).toBeVisible();
  expect(await rows.count()).toBeLessThan(100);
});
```

## Do
- Give the scroll container a fixed height or `flex: 1; min-height: 0`; the virtualizer needs a measured viewport.
- Use `getItemKey` or stable ids, not the index, so measured heights and state follow the item.
- For variable heights use measurement (`measureElement` on each row) and a good `estimateSize`.
- Set `overscan` (about 5 to 10) to avoid blank flashes on fast scroll.
- Put `role="list"`, `role="listitem"`, and `aria-setsize` and `aria-posinset` on rows so the full count is exposed.
- Keep row components memoized and free of per-row subscriptions to global state.
- Preserve scroll position on navigation back by storing the offset, and restore with `scrollToOffset`.
- Provide search or jump controls: keyboard users cannot Tab through thousands of rows.

## Avoid
- Rendering the full array "because it is only 2000 items": layout and memory cost hit mid-range phones. Virtualize.
- No container height: the virtualizer renders everything or nothing. Constrain it.
- Index keys with reordering or inserts: row state and heights mismatch. Use ids.
- Estimating height as a wrong constant with images: the scrollbar jumps. Reserve image space or measure.
- Using `Ctrl+F`-reliant UX: off-screen rows are not in the DOM. Offer in-app search.
- Focusable rows that unmount while focused: focus drops to `body`. Keep the active row mounted or restore focus by id.
- Animating row insertion with layout properties: janky and shifts. Use transforms.

## Review
- [ ] DOM node count stays bounded while scrolling.
- [ ] Keys are stable ids and heights are measured or reserved.
- [ ] Semantics expose set size and position.
- [ ] Focused rows survive scrolling.
- [ ] There is an in-app way to find and jump to an item.
