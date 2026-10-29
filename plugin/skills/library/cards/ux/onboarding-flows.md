---
name: onboarding-flows
title: Onboarding Flows
area: ux
tags: [onboarding, activation, first-run, product-design]
detect: []
related: [empty-states, progressive-disclosure, tooltips-and-coachmarks, analytics-events]
---
Get a new user to their first real result fast: one activation event, skippable steps, no tour before value.

## Verify
- `npx playwright test --grep onboarding`: walks sign-up to the first success state and asserts it is reached in the step budget.
- `grep -rn "onboarding_" src | grep -c track`: every step emits an analytics event, so drop-off is measurable.
- `npx playwright test --grep "skip onboarding"`: a skipped flow still lands on a usable screen.
- Funnel query on the step events: each step's completion rate is known before and after a change.

## Test first
Define the activation event, then assert a new account reaches it without optional steps.
```ts
import { test, expect } from '@playwright/test';

test('new user reaches first project with every step skipped', async ({ page }) => {
  await page.goto('/signup-complete');
  await page.getByRole('button', { name: /skip/i }).click();
  await expect(page.getByRole('heading', { name: /create your first project/i })).toBeVisible();
  await page.getByRole('button', { name: /create project/i }).click();
  await expect(page.getByTestId('activated')).toBeVisible();
});
```

## Do
- Name one activation event (the first moment of value, such as "sent first invoice") and shorten the path to it.
- Ask at most 3 questions up front, and only those that change what you show next.
- Show a progress cue ("2 of 4") and let the user skip or come back; persist answers per step.
- Use real sample data or a template so the product is never blank on first view.
- Teach by doing: a checklist of 3-5 tasks that tick off as the user performs them.
- Resume where the user stopped on the next login, on any device.
- Send one welcome email that links to the next incomplete step, not a feature list.

## Avoid
- A 6-screen carousel before any value: most users tap through and learn nothing.
- Forced profile fields (company size, phone) that do not affect the experience.
- Blocking the app behind a tour with no close button.
- Marking onboarding done by time elapsed rather than by the activation event.
- Different flows per segment before you have data that one flow fails.

## Review
- [ ] The activation event is defined, tracked, and reachable in under 5 minutes.
- [ ] Every step is skippable and resumable; no dead end.
- [ ] Each question changes something the user sees afterward.
- [ ] Keyboard and screen reader users can finish the flow.
- [ ] Drop-off per step is visible in analytics.
