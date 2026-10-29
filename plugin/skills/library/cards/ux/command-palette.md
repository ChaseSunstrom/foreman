---
name: command-palette
title: Command Palette
area: ux
tags: [command-palette, shortcuts, power-users, keyboard, product-design]
detect: [dep:cmdk, dep:kbar]
related: [keyboard-navigation, search-ux, dialogs, focus-management]
---
One keystroke to any action or page: fuzzy matched, ranked by recency, keyboard-first and accessible.

## Verify
- `npx playwright test --grep palette`: opens with the shortcut, filters, runs a command, and closes with Esc.
- `npx axe-core-cli http://localhost:3000`: palette is a labelled dialog with a combobox and listbox roles.
- `grep -rn "metaKey\|ctrlKey" src/palette`: both Cmd (macOS) and Ctrl (others) are handled.
- Open in a form field: the shortcut must not fire while typing a literal "k" without the modifier.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('palette opens, runs a command, restores focus', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Settings' }).focus();
  await page.keyboard.press('Control+k');
  const box = page.getByRole('combobox', { name: /command/i });
  await expect(box).toBeFocused();
  await box.fill('new inv');
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/invoices\/new/);
});

test('Esc closes and returns focus', async ({ page }) => {
  await page.goto('/');
  await page.keyboard.press('Control+k');
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog')).toHaveCount(0);
});
```

## Do
- Bind Cmd/Ctrl+K (the convention), and also expose a visible button for discoverability.
- Fuzzy match on label and keywords; rank by recent and frequent use, with groups (Pages, Actions, Recent).
- Show each command's own shortcut on the right so users learn it.
- Use `role="dialog"`, a combobox input, and `aria-activedescendant` on a listbox; trap focus and restore it on close.
- Keep commands context-aware: show only what applies on the current page or selection.
- Confirm destructive commands before running; do not make "Delete all" one Enter away.

## Avoid
- A palette that is the only way to reach a feature; keep normal UI paths.
- Capturing shortcuts inside text inputs, editors and IME composition.
- Results that jump position as async items load.
- Different shortcut on each platform with no display of which applies.

## Review
- [ ] Opens in under 100 ms; results appear on first keystroke.
- [ ] Every item is reachable with arrows, Enter and Esc only.
- [ ] Focus returns to the trigger on close.
- [ ] Destructive commands require confirmation.
