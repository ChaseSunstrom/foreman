---
name: feedback-collection
title: Feedback Collection
area: ux
tags: [feedback, surveys, nps, research, product-design]
detect: []
related: [usability-testing, analytics-events, permission-prompts, forms]
---
Ask at the right moment, ask little, and close the loop: users who give feedback should see it used.

## Verify
- `npx playwright test --grep feedback`: submits a rating with and without a comment and asserts the stored payload.
- `grep -rn "survey" src | grep -i "cooldown\|lastShown"`: a frequency cap exists.
- Check the pipeline: each response carries page, plan, app version and no free-text PII beyond the comment.
- Review the last 50 responses weekly and tag themes; track the share acted on.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('feedback needs only a rating and respects the cooldown', async ({ page }) => {
  await page.goto('/reports/export-done');
  await page.getByRole('radio', { name: '4 out of 5' }).check();
  await page.getByRole('button', { name: 'Send' }).click();
  await expect(page.getByRole('status')).toContainText(/thanks/i);
  await page.reload();
  await expect(page.getByRole('group', { name: /how was/i })).toHaveCount(0);
});
```

## Do
- Trigger on a moment tied to a task (after export, after support chat), not on page load.
- Start with one question (CES, CSAT or thumbs); make the comment optional and short.
- Cap frequency: for example one survey per user per 30-90 days, never during an error or checkout.
- Offer a persistent, low-key "Feedback" entry for self-initiated reports with a screenshot option.
- Tell users what you do with it, and reply or ship a changelog line when you act.
- Segment responses (plan, tenure, platform) before reading averages; keep the comment text searchable.
- Make it keyboard and screen reader operable; scale labels read as text ("4 out of 5").

## Avoid
- Modal surveys that block the task.
- Asking for NPS from a new user who has not yet got value.
- Required comment fields and 10-question forms (completion falls fast).
- Collecting personal data you do not need, or promising anonymity you cannot keep.
- Treating the score as the insight; read the words.

## Review
- [ ] Each prompt has a trigger, a cap and an owner for responses.
- [ ] Feedback is tagged with context and routed to a person.
- [ ] Users see what changed because of it.
- [ ] Privacy notice and consent match what you store.
