---
name: destructive-actions
title: Destructive Actions
area: ux
tags: [destructive, confirmation, delete, safety, product-design]
detect: []
related: [undo-patterns, dialogs, settings-pages, ux-writing]
---
When an action cannot be undone, make it deliberate: name the target and consequence, add friction in proportion to the damage.

## Verify
- `npx playwright test --grep destructive`: tries to delete, cancels, then confirms and checks the outcome.
- `grep -rnE "window\.confirm|confirm\(" src`: finds browser-native confirms to replace with a real dialog.
- `npx axe-core-cli http://localhost:3000/settings/danger`: dialog role, label and focus pass.
- Check the API: a delete endpoint requires auth, the right role and rejects replay (idempotency).

## Test first
```ts
import { test, expect } from '@playwright/test';

test('deleting a project requires typing its name', async ({ page }) => {
  await page.goto('/projects/acme/settings');
  await page.getByRole('button', { name: 'Delete project' }).click();
  const confirm = page.getByRole('button', { name: 'Delete Acme permanently' });
  await expect(confirm).toBeDisabled();
  await page.getByLabel('Type acme to confirm').fill('acme');
  await expect(confirm).toBeEnabled();
});

test('Cancel is the default focus', async ({ page }) => {
  await page.goto('/projects/acme/settings');
  await page.getByRole('button', { name: 'Delete project' }).click();
  await expect(page.getByRole('button', { name: 'Cancel' })).toBeFocused();
});
```

## Do
- Match friction to cost: undo toast for reversible; confirm dialog for irreversible; type the name for catastrophic (delete project, account).
- Title the dialog with the verb and object ("Delete Acme?"); state what is lost and the count of items affected.
- Label the destructive button with the action, not "OK" or "Yes"; style it as danger (red plus text, contrast 4.5:1).
- Focus Cancel by default; Esc cancels; Enter must not trigger the danger action.
- Offer a safer alternative when one exists (archive, export first, transfer ownership).
- Separate dangerous controls from routine ones with spacing and a "Danger zone".
- Log who did it and when; send an email for account-level deletion with a grace period (7-30 days).

## Avoid
- Confirming everything: dialog fatigue makes users click through the one that matters.
- "Are you sure?" with Yes/No.
- Placing Delete next to Save with equal weight.
- Deleting immediately on the first click of an icon-only button.
- Doing the work client-side only; the server must authorize and verify.

## Review
- [ ] Friction level matches reversibility and blast radius.
- [ ] Dialog names the object and consequence; safe option has initial focus.
- [ ] Server authorizes, logs, and survives a double submit.
- [ ] A grace period or export exists for account-level loss.
