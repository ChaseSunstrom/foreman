---
name: drag-and-drop
title: Drag and drop
area: frontend
tags: [dnd, sortable, a11y, pointer, keyboard]
detect: [dep:@dnd-kit/core]
related: [keyboard-navigation, aria-patterns, virtualized-lists, file-drop]
---
Reorder and move items with pointer, touch and keyboard, with live announcements and a non-drag alternative.

## Verify
- `npx playwright test`: drives mouse and keyboard reordering and asserts the final order.
- `npx tsc --noEmit`: sensor, id and event types line up.
- `npx @axe-core/cli http://localhost:3000`: handles are named and reachable.

## Test first
Reorder with the keyboard, the path most implementations forget.
```ts
import { test, expect } from '@playwright/test';

test('reorder an item with the keyboard', async ({ page }) => {
  await page.goto('/board');
  const first = page.getByRole('button', { name: /drag.*alpha/i });
  await first.focus();
  await page.keyboard.press('Space');
  await page.keyboard.press('ArrowDown');
  await page.keyboard.press('Space');
  const items = page.getByRole('listitem');
  await expect(items.nth(1)).toContainText('alpha');
});
```

## Do
- Use a library with keyboard sensors (`@dnd-kit` `KeyboardSensor` plus `sortableKeyboardCoordinates`) rather than raw HTML5 drag events.
- Provide a drag handle `<button>` with a name (`aria-label="Drag alpha"`) and `touch-action: none` on it.
- Announce pickup, move and drop in a live region (the library's `announcements` option).
- Offer a non-drag alternative: "Move up" and "Move down" buttons or a move menu.
- Use a `DragOverlay` so the item keeps its size while the list reflows; show a placeholder at the origin.
- Add an activation constraint (distance or delay) so clicks and scrolls are not hijacked.
- Persist the new order optimistically and roll back on failure.
- Use stable ids as sortable keys, not indices.

## Avoid
- Native HTML5 dragstart only: no touch support and no keyboard path. Use pointer sensors plus a keyboard sensor.
- A whole-row drag target that swallows clicks, links and text selection: restrict to a handle.
- Missing `touch-action: none` on the handle: the page scrolls instead of dragging on touch.
- Index keys: items jump or lose state after reorder. Use ids.
- No focus after drop: focus returns to `body`. Refocus the moved item's handle.
- Dragging inside a virtualized list without auto-scroll or measuring: items unmount mid-drag. Pin the active item.
- Reordering with no announcement: screen reader users get no feedback.

## Review
- [ ] Keyboard reordering works and is tested.
- [ ] Handles are buttons with accessible names and visible focus.
- [ ] Pickup, move and drop are announced.
- [ ] A button alternative to dragging exists.
- [ ] Failure of the save reverts the visual order.
