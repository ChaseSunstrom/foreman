---
name: checkout-flows
title: Checkout Flows
area: ux
tags: [checkout, payments, conversion, forms, product-design]
detect: []
related: [forms, pricing-pages, error-messages, sign-up-flows]
---
A short, honest path to paid: guest checkout, autofill, visible totals, and recoverable errors.

## Verify
- `npx playwright test --grep checkout`: completes an order with the test card, and a declined card path.
- `npx axe-core-cli http://localhost:3000/checkout`: labels, errors and focus pass.
- `grep -rn "autocomplete=" src/checkout | wc -l`: fields carry `autocomplete` tokens (`cc-number`, `postal-code`, `email`).
- Run the flow on a real phone; check the numeric keyboard appears for card and postal fields.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('declined card keeps the cart and explains the fix', async ({ page }) => {
  await page.goto('/checkout');
  await page.getByLabel('Email').fill('buyer@example.com');
  await page.getByLabel('Card number').fill('4000000000000002');
  await page.getByRole('button', { name: /pay \$/i }).click();
  await expect(page.getByRole('alert')).toContainText(/declined.*another card/i);
  await expect(page.getByTestId('order-total')).toBeVisible();
});

test('double click pays once', async ({ page }) => {
  await page.goto('/checkout');
  const pay = page.getByRole('button', { name: /pay \$/i });
  await pay.dblclick();
  await expect(pay).toBeDisabled();
});
```

## Do
- Offer guest checkout; ask for an account after the purchase.
- Show the cart summary, shipping, tax and total on every step before the pay button.
- Use correct `autocomplete`, `inputmode="numeric"` and wallet buttons (Apple Pay, Google Pay).
- Ask only what you need: one address field set, billing same as shipping by default.
- Keep one pay action idempotent: send an idempotency key and disable the button while pending.
- Show a progress indicator for multi-step checkout, 3 steps or fewer when you can.
- Confirm with an order number, receipt email and next steps on the success page.

## Avoid
- Forcing account creation before payment.
- Surprise costs at the final step; they cause the most abandonment.
- Clearing the card form after a decline.
- Validating only after submit when format hints can help early (card Luhn, expiry).
- Redirecting away to a page that looks unrelated, without explanation.

## Review
- [ ] Total is visible and identical at every step.
- [ ] Payment is idempotent; refresh does not double charge.
- [ ] Errors keep entered data and tell the user what to try.
- [ ] Tested with keyboard, screen reader and a phone.
