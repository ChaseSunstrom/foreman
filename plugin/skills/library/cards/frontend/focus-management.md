---
name: focus-management
title: Focus management
area: frontend
tags: [a11y, focus, keyboard, dom, routing]
detect: [dep:focus-trap-react]
related: [dialogs, keyboard-navigation, aria-patterns, accessibility]
---
Move, trap and restore keyboard focus deliberately on route changes, overlays, deletes and async updates.

## Verify
- `npx playwright test`: drives Tab, Shift+Tab and Escape and asserts `document.activeElement`.
- `npx @axe-core/cli http://localhost:3000`: finds missing names and `tabindex` misuse.
- `grep -rnE "outline:\s*(none|0)" src`: every hit needs a `:focus-visible` replacement.

## Test first
Closing a menu returns focus to its trigger.
```ts
import { test, expect } from '@playwright/test';

test('focus returns to the trigger after Escape', async ({ page }) => {
  await page.goto('/');
  const trigger = page.getByRole('button', { name: 'Options' });
  await trigger.focus();
  await page.keyboard.press('Enter');
  await expect(page.getByRole('menu')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(trigger).toBeFocused();
});
```

## Do
- Save `document.activeElement` before opening an overlay and call `.focus()` on it after close, if it is still in the DOM.
- On open, move focus into the overlay: first control, or the container with `tabindex="-1"` and a label.
- After an SPA navigation, focus the new page `<h1>` (`tabindex="-1"`) or a main landmark, and update `document.title`.
- After deleting an item, focus the next item, else the previous, else the list heading.
- Use the `inert` attribute on the background while a modal is open.
- Style `:focus-visible` with a 2px outline and `outline-offset`; keep it on high-contrast backgrounds.
- Use `focus({ preventScroll: true })` when scrolling is handled separately.
- Announce async results in a persistent `role="status"` region instead of stealing focus.

## Avoid
- `outline: none` with no replacement: keyboard users lose their place. Use `:focus-visible`.
- Positive `tabindex` values: they override document order. Use `0` or `-1` only.
- Focusing an element before it is rendered or visible: the call silently fails. Focus after layout (effect or `requestAnimationFrame`).
- Removing the focused element with no handoff: focus falls back to `body`. Move it first.
- Clickable `div`s with `tabindex="0"` and a key handler: use `<button>` or `<a>`.
- Trapping focus with no Escape or close control: it is a keyboard trap. Provide both.

## Review
- [ ] Every overlay saves and restores focus.
- [ ] Route changes move focus and the title changes.
- [ ] Deletes and removals never leave focus on `body`.
- [ ] No `tabindex` above 0 and no bare `outline: none`.
- [ ] Focus order matches reading order at every breakpoint.
