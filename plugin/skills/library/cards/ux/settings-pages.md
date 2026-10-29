---
name: settings-pages
title: Settings Pages
area: ux
tags: [settings, preferences, account, product-design]
detect: []
related: [forms, information-architecture, destructive-actions, undo-patterns]
---
Group settings by the user's mental model, save safely, and keep dangerous actions apart.

## Verify
- `npx playwright test --grep settings`: changes a value, reloads, and expects it persisted.
- `grep -rn "autoSave\|onBlur" src/settings`: the saving model is one chosen pattern, applied consistently.
- `npx axe-core-cli http://localhost:3000/settings`: every control has a label and group `legend`.
- Count top-level sections: 5-8 is the target; more needs search.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('toggle persists and confirms', async ({ page }) => {
  await page.goto('/settings/notifications');
  const t = page.getByRole('switch', { name: 'Email digests' });
  await t.click();
  await expect(page.getByRole('status')).toHaveText(/saved/i);
  await page.reload();
  await expect(t).toHaveAttribute('aria-checked', 'true');
});

test('unsaved text changes warn on leave', async ({ page }) => {
  await page.goto('/settings/profile');
  await page.getByLabel('Display name').fill('New name');
  page.once('dialog', d => d.dismiss());
  await page.getByRole('link', { name: 'Billing' }).click();
});
```

## Do
- Organise by task (Profile, Security, Notifications, Billing, Team), not by database table.
- Pick one saving model per page: instant for toggles with a "Saved" status; explicit Save/Cancel for text and multi-field forms.
- Describe each setting in one line of helper text, with the default and the effect.
- Choose safe defaults; most users never open settings.
- Put destructive and irreversible actions (delete account, export data) last in a separate "Danger zone".
- Add a setting search when there are more than about 30 options.
- Use a labelled switch for immediate on/off, a checkbox for batch-saved choices.

## Avoid
- Mixing auto-save and Save buttons on the same page.
- A setting for every design disagreement: decide instead.
- Toggles whose label does not say the state ("Dark mode" vs "Enable dark mode").
- Silent failure on save; surface the error and keep the old value displayed accurately.
- Settings that need a restart with no notice.

## Review
- [ ] Save model is consistent and the user sees confirmation.
- [ ] Defaults are safe; each option has helper text.
- [ ] Danger zone is separated and confirmed.
- [ ] Deep links to a section work (`/settings/security`).
