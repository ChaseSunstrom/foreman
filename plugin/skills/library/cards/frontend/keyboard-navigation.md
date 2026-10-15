---
name: keyboard-navigation
title: Keyboard navigation
area: frontend
tags: [a11y, keyboard, roving-tabindex, shortcuts, focus]
detect: []
related: [focus-management, aria-patterns, dialogs, data-tables]
---
Everything reachable and operable by keyboard: sane tab order, roving tabindex for composites, safe shortcuts.

## Verify
- `npx playwright test`: presses real keys and asserts the focused element.
- `npx @axe-core/cli http://localhost:3000`: flags scrollable regions and controls unreachable by keyboard.
- `grep -rnE "onClick" src --include=*.tsx | grep -E "<(div|span)"`: click handlers on non-interactive elements.

## Test first
A toolbar uses one tab stop and arrow keys inside.
```ts
import { test, expect } from '@playwright/test';

test('toolbar is one tab stop with arrow navigation', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Bold' }).focus();
  await page.keyboard.press('ArrowRight');
  await expect(page.getByRole('button', { name: 'Italic' })).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(page.getByRole('button', { name: 'Bold' })).not.toBeFocused();
  await expect(page.getByRole('toolbar')).not.toContainText('focused-escape');
});
```

## Do
- Keep DOM order equal to visual order; never reorder with CSS `order` or absolute positions without fixing the DOM.
- Composites (tabs, toolbars, listbox, grid, tree) use a roving `tabindex`: one item `0`, the rest `-1`, arrows move it, Home and End jump.
- Activate with Enter for links and Enter or Space for buttons: use real elements and you get both free.
- Add a visible "Skip to content" link as the first focusable element, targeting `<main id>`.
- Make single-key shortcuts opt-out or modified (`Ctrl`, `Alt`) and ignore them while typing in inputs and `contenteditable`.
- Make scrollable regions focusable (`tabindex="0"` with a label) when they contain no focusable child.
- Test with the mouse unplugged: complete each core flow using only the keyboard.

## Avoid
- `onClick` on a `div`: no key support. Use `<button>`.
- `keydown` handlers that match `e.key === 'Enter'` but skip IME composition: check `!e.isComposing`.
- Hover-only menus and tooltips: reveal on focus too (`:focus-within`, `onFocus`).
- Global single-letter shortcuts that fire in text fields: guard on `event.target`.
- Tab traps for no reason, or `tabindex="-1"` on controls users must reach.
- Arrow handlers that never `preventDefault()`: the page scrolls while the selection moves.
- Hiding the skip link with `display: none`: it is then unfocusable. Reveal it on `:focus`.

## Review
- [ ] Tab order is logical at every breakpoint.
- [ ] Composite widgets expose one tab stop and arrow, Home, End movement.
- [ ] No interactive `div` or `span`.
- [ ] Shortcuts are documented, modified or scoped, and skip text inputs.
- [ ] Hover content is available on focus.
