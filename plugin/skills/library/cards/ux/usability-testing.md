---
name: usability-testing
title: Usability Testing
area: ux
tags: [usability, user-research, testing, interviews, product-design]
detect: []
related: [feedback-collection, information-architecture, accessibility-testing, onboarding-flows]
---
Watch 5 real users attempt real tasks, record where they stumble, fix, and repeat: small and often beats big and rare.

## Verify
- `grep -c "^- Task" research/test-plan.md`: the plan lists 3-5 tasks with success criteria.
- `ls research/sessions | wc -l`: at least 5 sessions per round, recorded with consent.
- Task metrics file: completion rate, time on task and error count per task are recorded.
- `npx playwright test --grep "top task"`: top tasks from the study are guarded by automated flow tests afterwards.

## Test first
Write the task and its success criterion before the session, then lock the fixed flow as a regression.
```ts
import { test, expect } from '@playwright/test';

// Study task 2: "Change the email address on your account"
test('task 2: change email in under 6 clicks', async ({ page }) => {
  let clicks = 0;
  page.on('framenavigated', () => clicks++);
  await page.goto('/');
  await page.getByRole('link', { name: 'Account' }).click();
  await page.getByRole('link', { name: 'Email' }).click();
  await page.getByLabel('New email').fill('new@example.com');
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByRole('status')).toContainText(/confirm/i);
  expect(clicks).toBeLessThan(6);
});
```

## Do
- Recruit participants who match the target user, not colleagues; 5 per round finds most major problems (Nielsen), more for distinct segments.
- Write tasks as scenarios without UI words ("Your card expired; make sure the next invoice is paid"), each with a clear end state.
- Think-aloud: ask them to narrate; stay quiet, do not lead, do not help.
- Record screen and audio with written consent; keep notes of observations apart from interpretations.
- Rate each issue by severity (blocker, major, minor) and frequency; fix the top few before the next round.
- Measure: task success, time, errors, and a SUS score (68 is average) to track change.
- Test prototypes early; test remotely or in person; include assistive tech users.

## Avoid
- Asking "Do you like it?" in place of observing behavior.
- Testing with only team members or friends.
- Long reports no one reads; share a 1-page list with clips.
- Changing the product mid-session.
- Treating a single comment as a trend.

## Review
- [ ] Tasks, success criteria and participant profile were written before the session.
- [ ] Findings are rated by severity and linked to tickets.
- [ ] Fixes are re-tested in the next round.
- [ ] Consent and data retention are handled.
