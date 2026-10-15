---
name: dialogs
title: Dialogs and modals
area: frontend
tags: [dialog, modal, a11y, focus, popover]
detect: [dep:@radix-ui/react-dialog]
related: [focus-management, aria-patterns, keyboard-navigation, toasts]
---
Modal dialogs on native `<dialog>` or a vetted primitive: labelled, focus-trapped, dismissible, focus restored.

## Verify
- `npx playwright test`: opens by click, checks focus in, Escape closes, focus returns.
- `npx @axe-core/cli http://localhost:3000`: dialog has a name, no aria-hidden misuse.
- `npx vitest run`: Testing Library `getByRole('dialog', { name })` specs.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('modal traps, closes, restores focus', async ({ page }) => {
  await page.goto('/');
  const open = page.getByRole('button', { name: 'Delete project' });
  await open.click();
  const dlg = page.getByRole('dialog', { name: 'Delete project?' });
  await expect(dlg).toBeVisible();
  await expect(dlg.getByRole('button', { name: 'Cancel' })).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(dlg).toBeHidden();
  await expect(open).toBeFocused();
});
```

## Do
- Prefer `<dialog>` with `showModal()`: it gives top layer, inert background, Escape and focus handling. Style `::backdrop`.
- Name it: `aria-labelledby` pointing at the heading, optional `aria-describedby` for the body.
- Put initial focus on the least destructive control, or the heading for long content (`autofocus` on that element).
- Return focus to the trigger on close; if the trigger is gone, to a sensible container.
- Close on Escape, on the close button, and on backdrop click only when no unsaved data is at risk.
- Lock background scroll (`overflow: hidden` on `html` while open, or `overscroll-behavior: contain` on the dialog).
- Use `role="alertdialog"` for confirmations that need an immediate decision.
- Keep dialog content scrollable inside with a max-height (`max-height: 90dvh`), header and footer visible.

## Avoid
- A `div` with `position: fixed` and no `role`, trap or `inert`: screen readers and Tab walk behind it. Use `<dialog>`.
- Calling `dialog.show()` for a modal: no backdrop and no trap. Use `showModal()`.
- Opening with `open` attribute toggled directly: skips modal behavior. Call the method.
- No focus return: users restart at the top of the page. Store and restore the trigger.
- Z-index battles with portals: the top layer removes them; do not stack another overlay beneath.
- Closing on backdrop click for a form with typed data: silent data loss. Confirm or ignore.
- Nested modals with no stack plan: avoid, or close the first before opening the second.

## Review
- [ ] Role, accessible name and modal state are correct.
- [ ] Focus moves in, is contained, and returns on close.
- [ ] Escape and an explicit close control work.
- [ ] Background is inert and does not scroll.
- [ ] Tall content scrolls inside the dialog on small screens.
