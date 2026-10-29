---
name: dark-patterns
title: Dark Patterns
area: ux
tags: [dark-patterns, deceptive-design, ethics, consent, product-design]
detect: []
related: [pricing-pages, permission-prompts, checkout-flows, ux-writing]
---
Recognise and refuse deceptive design: it wins a metric, loses trust, and now carries fines (FTC, EU DSA, GDPR).

## Verify
- `grep -rniE "only [0-9]+ left|hurry|ends in|countdown" src`: finds scarcity and urgency copy; each claim must be true and sourced.
- `npx playwright test --grep "cancel"`: cancelling takes no more steps than signing up (click-to-cancel).
- Compare button styles: "Accept" and "Reject" in a consent banner have equal prominence.
- Audit checkbox defaults: `grep -rn "defaultChecked\|checked" src/forms` for pre-ticked marketing or add-ons.

## Test first
Assert symmetry between the way in and the way out.
```ts
import { test, expect } from '@playwright/test';

test('cancel is as short as sign-up and needs no call', async ({ page }) => {
  await page.goto('/account/subscription');
  await page.getByRole('button', { name: 'Cancel subscription' }).click();
  await page.getByRole('button', { name: 'Confirm cancellation' }).click();
  await expect(page.getByText(/cancelled/i)).toBeVisible();
});

test('consent banner offers reject with equal weight', async ({ page }) => {
  await page.goto('/');
  const accept = await page.getByRole('button', { name: 'Accept all' }).boundingBox();
  const reject = await page.getByRole('button', { name: 'Reject all' }).boundingBox();
  expect(reject!.width).toBeGreaterThanOrEqual(accept!.width * 0.9);
});
```

## Do
- Learn the named types: roach motel (easy in, hard out), confirmshaming, forced continuity, hidden costs, sneak into basket, misdirection, fake scarcity, nagging, trick questions.
- Make cancellation and data deletion reachable in the same number of steps as sign-up.
- Show the full price up front; show recurring terms and renewal date before payment.
- Keep options unchecked by default; use plain double-negative-free questions.
- Give accept and reject equal visual weight and the same number of clicks.
- Make countdowns, stock counts and social proof true and verifiable.
- Run a design ethics review in the checklist for pricing, consent and retention flows.

## Avoid
- "No thanks, I hate saving money" style decline copy.
- Hiding the decline link in low-contrast text.
- Auto-renewing a trial with no reminder.
- Pre-selected add-ons, insurance or newsletters.
- A/B tests that optimise conversion without measuring complaints, refunds and churn.

## Review
- [ ] Exit paths are as easy as entry paths.
- [ ] No false urgency, hidden fees or pre-ticked extras.
- [ ] Consent choices are balanced and recorded.
- [ ] Refund and complaint rates are tracked beside conversion.
