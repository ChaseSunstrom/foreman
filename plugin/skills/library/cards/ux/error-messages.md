---
name: error-messages
title: Error Messages
area: ux
tags: [errors, validation, microcopy, recovery, product-design]
detect: []
related: [forms, ux-writing, toasts, accessibility]
---
Say what happened, why, and how to fix it, next to the thing that failed, in words the user would use.

## Verify
- `npx playwright test --grep "error message"`: triggers each failure and asserts text, placement and focus.
- `grep -rnE "Error:|Something went wrong|Invalid input|undefined" src/ui`: finds raw or vague copy.
- `npx axe-core-cli http://localhost:3000/signup`: errors are associated with fields (`aria-describedby`).
- Kill the network in devtools and submit: a recoverable message appears with a retry.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('invalid email explains the fix and moves focus', async ({ page }) => {
  await page.goto('/signup');
  await page.getByLabel('Email').fill('alice@');
  await page.getByRole('button', { name: 'Create account' }).click();
  const field = page.getByLabel('Email');
  await expect(field).toHaveAttribute('aria-invalid', 'true');
  await expect(page.getByText('Enter an email like name@example.com')).toBeVisible();
  await expect(field).toBeFocused();
});
```

## Do
- Use three parts: what happened, why if known, what to do next ("Card declined. Your bank refused it. Try another card.").
- Place field errors directly under the field; summary errors at the top with links to each field.
- Link with `aria-describedby`, set `aria-invalid`, and move focus to the first error on submit.
- Keep the user's input; never clear a form because one field failed.
- Validate on blur or submit, not on every keystroke before the user finishes.
- For system failures give a retry and, where useful, a reference id the user can quote.
- Use text plus an icon; do not rely on red alone (contrast 4.5:1).

## Avoid
- "Something went wrong" with no action, or raw exception text and HTTP codes.
- Blaming ("You entered an invalid value"); say what is expected.
- Toasts for form errors: they vanish before they are read.
- Disabling the submit button without saying why.
- Showing the same error in three places.

## Review
- [ ] Each error names a fix and sits next to its cause.
- [ ] Focus and `aria-live` announce the error to assistive tech.
- [ ] No input is lost on failure; retry works.
- [ ] Server and client validation messages match.
