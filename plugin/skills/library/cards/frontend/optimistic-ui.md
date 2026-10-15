---
name: optimistic-ui
title: Optimistic UI
area: frontend
tags: [state, mutations, rollback, react-query, ux]
detect: [dep:@tanstack/react-query]
related: [toasts, error-boundaries, skeleton-loading, forms]
---
Show the result of a mutation immediately, then reconcile with the server and roll back on failure.

## Verify
- `npx vitest run`: mutation tests cover success, failure rollback and concurrent edits.
- `npx playwright test`: routes the API to fail or delay and asserts the UI path.
- `npx tsc --noEmit`: cache shapes and mutation variables.

## Test first
A failed save restores the old value and tells the user.
```ts
import { test, expect } from '@playwright/test';

test('failed rename rolls back and reports', async ({ page }) => {
  await page.route('**/api/projects/1', r => r.fulfill({ status: 500 }));
  await page.goto('/projects/1');
  await page.getByRole('button', { name: 'Rename' }).click();
  await page.getByRole('textbox', { name: 'Name' }).fill('New name');
  await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name: 'New name' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Old name' })).toBeVisible();
  await expect(page.getByRole('alert')).toContainText(/could not save/i);
});
```

## Do
- Apply only to low-risk, highly likely-to-succeed actions (like, rename, reorder, toggle, add comment). Wait for the server on payments, deletes of shared data and permission changes.
- Before the write: cancel in-flight queries for that key, snapshot the previous cache, then set the new value (`onMutate`).
- On error restore the snapshot (`onError`); always refetch to reconcile (`onSettled`).
- Use client-generated temporary ids for created items, mark them pending (reduced opacity, `aria-busy`), and swap to the server id on success.
- Make mutations idempotent (idempotency key) so retries are safe.
- Serialize mutations to the same resource or send a version, so out-of-order responses cannot clobber newer state.
- Surface failure with a message and a retry; keep the user's input available.
- Offer Undo for destructive-looking optimistic actions (delay the real call briefly).

## Avoid
- No rollback path: the UI stays wrong after a failure. Snapshot and restore.
- Skipping `cancelQueries`: an in-flight refetch overwrites the optimistic value. Cancel first.
- Optimistic deletes that hide the item with no recovery: errors silently resurrect it. Show the error and restore it in place.
- Using array index as the key for pending items: the swap to the real id remounts and loses focus. Keep a stable client key.
- Ignoring double submits: disable or dedupe the trigger while pending, or use the key.
- Treating the optimistic value as truth in follow-up logic (totals, permissions): derive from confirmed data where it matters.
- Failing silently: errors appear only in the console.

## Review
- [ ] Each optimistic action has success, failure and rollback tests.
- [ ] Out-of-order and double-submit cases are handled.
- [ ] Pending items are visually and programmatically marked.
- [ ] Errors are reported with a retry path.
- [ ] High-risk actions wait for confirmation.
