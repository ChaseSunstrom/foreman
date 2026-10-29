---
name: undo-patterns
title: Undo Patterns
area: ux
tags: [undo, redo, soft-delete, reversibility, product-design]
detect: []
related: [destructive-actions, toasts, optimistic-ui, keyboard-navigation]
---
Prefer undo to confirmation: make actions reversible, say how long, and make the undo path real.

## Verify
- `npx playwright test --grep undo`: performs the action, presses undo, and asserts the data is restored.
- `grep -rn "deleted_at\|softDelete" src db | wc -l`: deletes are soft or recoverable in the backing store.
- Wait out the undo window and assert the action is final (hard delete or purge job ran).
- `npx axe-core-cli http://localhost:3000/inbox`: the undo toast is announced and focusable.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('archive can be undone from the toast', async ({ page }) => {
  await page.goto('/inbox');
  await page.getByRole('button', { name: 'Archive message 1' }).click();
  await expect(page.getByText('Message 1')).toHaveCount(0);
  await page.getByRole('button', { name: 'Undo' }).click();
  await expect(page.getByText('Message 1')).toBeVisible();
});

test('Ctrl+Z restores the last deletion', async ({ page }) => {
  await page.goto('/inbox');
  await page.getByRole('button', { name: 'Delete message 2' }).click();
  await page.keyboard.press('Control+z');
  await expect(page.getByText('Message 2')).toBeVisible();
});
```

## Do
- Do the action at once, show "Archived. Undo" for about 5-10 seconds (longer for assistive users: pause on hover and focus).
- Make the backend match: soft delete or delayed commit, and purge after the window or a retention period.
- Support Cmd/Ctrl+Z for in-document edits, with a bounded history (say 100 steps) and Shift+Z for redo.
- Name what was affected ("3 files moved to Trash") and offer the restore where it is.
- Offer a Trash or history for the longer term (30 days) for content with value.
- For bulk actions, undo the whole batch as one unit.
- Keep undo idempotent: a double click on Undo restores once.

## Avoid
- Undo that only hides the item in the UI while the server already deleted it.
- A toast that disappears while the user is reading or has focus on it.
- Confirmation dialogs for routine, reversible actions: they train click-through.
- Undo for actions that cannot be reversed (sent email, payment); use delay-send or confirmation instead.
- Undo stacks that mix unrelated scopes.

## Review
- [ ] Each undoable action is truly reversible server-side in the window.
- [ ] The window is stated, pausable and accessible.
- [ ] Irreversible actions use a different pattern.
- [ ] Bulk undo restores everything or nothing.
