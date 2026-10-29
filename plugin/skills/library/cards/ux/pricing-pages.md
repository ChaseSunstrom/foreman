---
name: pricing-pages
title: Pricing Pages
area: ux
tags: [pricing, conversion, plans, saas, product-design]
detect: []
related: [checkout-flows, dark-patterns, ux-writing, responsive-design]
---
Make the choice easy: 3 plans, a recommended one, honest totals, and a comparison that fits a phone.

## Verify
- `npx playwright test --grep pricing`: toggles billing period and asserts the price text and the CTA target.
- `grep -rn "pricing" src/analytics`: plan views and CTA clicks are tracked.
- `npx lighthouse http://localhost:3000/pricing --only-categories=accessibility,performance`: scores at least 90.
- Resize to 375 px: the table collapses to stacked cards with no horizontal scroll.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('annual toggle shows the real total and savings', async ({ page }) => {
  await page.goto('/pricing');
  await page.getByRole('switch', { name: /annual/i }).click();
  const pro = page.getByRole('article', { name: 'Pro' });
  await expect(pro).toContainText('$190 billed yearly');
  await expect(pro).toContainText(/save 20%/i);
});

test('every plan CTA carries the plan to sign-up', async ({ page }) => {
  await page.goto('/pricing');
  await page.getByRole('link', { name: /start pro/i }).click();
  await expect(page).toHaveURL(/plan=pro/);
});
```

## Do
- Offer 3 tiers (3-4 at most); highlight the one you want most buyers on and say who each is for.
- Show the total charged and the billing period, tax or "plus tax" status, and what renews when.
- Lead each plan with outcomes and limits in plain words; list only differences below the first tier.
- Use one clear CTA per plan with a different verb from a free trial ("Start free trial").
- State the refund, trial and cancellation terms next to the button.
- Add a short FAQ and one social proof element (logos, quote) near the decision.
- Keep currency and units localized; show price before the user scrolls.

## Avoid
- Hidden fees revealed at checkout, or "from" prices that nobody gets.
- A 15-row feature matrix on mobile as a scrolling table.
- Default selection of the most expensive option with a hard-to-find downgrade.
- Fake countdowns or scarcity; see dark-patterns.
- "Contact us" as the only path for a price anyone could compute.

## Review
- [ ] Price shown equals price charged, including period and tax note.
- [ ] Recommended plan is clear; no more than 4 tiers.
- [ ] Works at 375 px and with a screen reader (headings per plan).
- [ ] Cancellation and trial terms are visible near the CTA.
