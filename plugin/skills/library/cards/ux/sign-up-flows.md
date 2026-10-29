---
name: sign-up-flows
title: Sign-up Flows
area: ux
tags: [signup, authentication, passwords, passkeys, product-design]
detect: []
related: [forms, onboarding-flows, error-messages, checkout-flows]
---
Ask for as little as possible, show password rules up front, support passkeys and social login, and verify gently.

## Verify
- `npx playwright test --grep signup`: creates an account, hits a duplicate email, and a weak password.
- `grep -rn "autocomplete=\"new-password\"" src`: password managers can fill and save.
- `npx axe-core-cli http://localhost:3000/signup`: labels and errors pass.
- Paste a long password with spaces: it must be accepted (no paste block, 64+ characters allowed).

## Test first
```ts
import { test, expect } from '@playwright/test';

test('duplicate email offers sign in, not a dead end', async ({ page }) => {
  await page.goto('/signup');
  await page.getByLabel('Email').fill('existing@example.com');
  await page.getByLabel('Password').fill('correct horse battery staple');
  await page.getByRole('button', { name: 'Create account' }).click();
  await expect(page.getByRole('link', { name: /sign in/i })).toBeVisible();
});

test('show password toggle works', async ({ page }) => {
  await page.goto('/signup');
  await page.getByRole('button', { name: /show password/i }).click();
  await expect(page.getByLabel('Password')).toHaveAttribute('type', 'text');
});
```

## Do
- Start with email and password (or passkey, or one social button); defer name, company and phone.
- Show the password rule before typing (minimum 8-12 characters, length over complexity) and a show/hide toggle.
- Allow paste and password managers; use `autocomplete="email"` and `new-password`.
- Offer passkeys or magic link where your risk allows; keep one primary path visually dominant.
- Verify email after sign-in so the user already sees the product; allow resend with a limit.
- Handle an existing account by linking to sign in, with care not to leak existence if your policy forbids it.
- State terms and privacy briefly near the button; do not pre-check marketing consent.

## Avoid
- Confirm-password and confirm-email fields; use a show toggle instead.
- Blocking paste, or composition rules like "one symbol, one capital".
- Long forms and CAPTCHAs before value; use invisible risk checks first.
- Clearing the form on error.
- Emailing a plaintext password.

## Review
- [ ] At most 2-3 fields on first screen; rest deferred.
- [ ] Password managers and paste work; rules shown before submit.
- [ ] Duplicate, weak and unverified states have clear next steps.
- [ ] Rate limits on resend and attempts are in place.
