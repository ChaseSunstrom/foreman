---
name: progressive-disclosure
title: Progressive Disclosure
area: ux
tags: [progressive-disclosure, complexity, accordions, product-design]
detect: []
related: [settings-pages, forms, multi-step-wizards, accessibility]
---
Show the common path first and reveal advanced options on demand, without hiding what users need.

## Verify
- `npx playwright test --grep disclosure`: expands and collapses sections, checks `aria-expanded` and focus.
- `npx axe-core-cli http://localhost:3000/settings`: disclosure buttons pass role and name rules.
- Task analytics: if more than about 30% of users open a hidden section, promote it.
- `grep -rn "<details" src | wc -l`: native `details` is used where it fits.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('advanced options hidden by default and keyboard operable', async ({ page }) => {
  await page.goto('/export');
  const btn = page.getByRole('button', { name: 'Advanced options' });
  await expect(btn).toHaveAttribute('aria-expanded', 'false');
  await btn.focus();
  await page.keyboard.press('Enter');
  await expect(btn).toHaveAttribute('aria-expanded', 'true');
  await expect(page.getByLabel('Delimiter')).toBeVisible();
});
```

## Do
- Rank features by frequency and importance; defaults visible, rare ones one click away.
- Use native `<details>/<summary>` or a button with `aria-expanded` and `aria-controls`.
- Label the trigger with what is inside ("Advanced options", not "More").
- Keep a disclosed state if the user changed a hidden value, and show a summary of non-default values when collapsed.
- Limit depth to two levels; a third means the information architecture needs rework.
- Use staged forms (one section at a time) for long tasks; see multi-step-wizards.
- Reveal contextually: show the shipping fields only after "Ship to another address".
- Keep disclosure animation short (150-200 ms) and honor reduced motion.

## Avoid
- Hiding primary actions or required fields behind a toggle.
- Collapsed content that search and find-in-page cannot reach (`hidden="until-found"` helps).
- Hover-only reveals, which fail on touch and keyboard.
- Mystery "..." menus carrying key actions.
- Hidden settings that silently change behavior with no summary.

## Review
- [ ] The default view supports the 80% task.
- [ ] Hidden changed values are summarised when collapsed.
- [ ] Triggers are labelled, keyboard operable and expose state.
- [ ] No more than two disclosure levels.
