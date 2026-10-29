---
name: multi-step-wizards
title: Multi-step Wizards
area: ux
tags: [wizard, stepper, forms, flows, product-design]
detect: []
related: [forms, progressive-disclosure, onboarding-flows, checkout-flows]
---
Split a long task into short, validated steps with visible progress, safe Back, and a review before commit.

## Verify
- `npx playwright test --grep wizard`: completes the flow, goes Back, reloads mid-way and expects state kept.
- `grep -rn "aria-current=\"step\"" src | wc -l`: the stepper marks the current step.
- `npx @axe-core/cli http://localhost:3000/setup`: step headings, errors and focus pass.
- Step count check: more than 5-7 steps usually means the flow should be split.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('Back keeps entered data and reload resumes', async ({ page }) => {
  await page.goto('/setup/1');
  await page.getByLabel('Team name').fill('Acme');
  await page.getByRole('button', { name: 'Next' }).click();
  await page.getByRole('button', { name: 'Back' }).click();
  await expect(page.getByLabel('Team name')).toHaveValue('Acme');
  await page.reload();
  await expect(page.getByLabel('Team name')).toHaveValue('Acme');
});

test('invalid step blocks Next with a message', async ({ page }) => {
  await page.goto('/setup/1');
  await page.getByRole('button', { name: 'Next' }).click();
  await expect(page.getByText('Enter a team name')).toBeVisible();
});
```

## Do
- Give each step one purpose and a heading; move focus to it on step change.
- Show "Step 2 of 4" with step names; allow jumping back to completed steps.
- Validate each step on Next; keep data on Back; save a draft per step server-side or in storage.
- Give each step its own URL (`/setup/2`) so Back, refresh and links work.
- End with a review screen that lists the answers, each with an Edit link, then one Confirm.
- Mark optional steps and allow skipping them.
- Use a stable primary button position; "Next" on the right, "Back" as a secondary action.

## Avoid
- A wizard for a form of five fields; use one page.
- Resetting data on refresh or Back.
- Hiding the step count, so users cannot judge effort.
- Letting users reach a later step by URL that depends on earlier unvalidated data.
- Changing the number of steps mid-flow without saying why.

## Review
- [ ] Each step validates and persists; refresh resumes.
- [ ] The stepper is accessible with `aria-current="step"`.
- [ ] A review step precedes the final commit.
- [ ] Browser Back does not lose work.
