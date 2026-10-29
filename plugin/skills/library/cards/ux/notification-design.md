---
name: notification-design
title: Notification Design
area: ux
tags: [notifications, email, push, in-app, preferences, product-design]
detect: []
related: [toasts, permission-prompts, settings-pages, analytics-events]
---
Notify only when it is timely, relevant and actionable; give users channel and frequency control.

## Verify
- `npx playwright test --grep notification`: triggers an event and checks the in-app item, badge and mark-as-read.
- `grep -rn "unsubscribe" src/email templates | wc -l`: every marketing and digest email has a working unsubscribe.
- Count notifications per active user per week from the event log; investigate anything above about 5 push per week.
- `npx @axe-core/cli http://localhost:3000/notifications`: the list is a labelled region with live updates polite.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('muted channel sends nothing and preference persists', async ({ page }) => {
  await page.goto('/settings/notifications');
  await page.getByRole('switch', { name: 'Push: mentions' }).click();
  await page.reload();
  await expect(page.getByRole('switch', { name: 'Push: mentions' })).toHaveAttribute('aria-checked', 'false');
});

test('opening an item marks it read and clears the badge', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: /notifications \(1\)/i }).click();
  await page.getByRole('link', { name: /commented on/i }).click();
  await expect(page.getByRole('button', { name: /notifications$/i })).toBeVisible();
});
```

## Do
- Classify: transactional (always), social or activity (user choice), marketing (opt-in).
- Offer a preference matrix by type and channel (in-app, email, push), with sensible defaults and a digest option.
- Write each message to carry who, what and the action, and link straight to the object.
- Batch and dedupe bursts ("5 people commented") and respect quiet hours and time zones.
- Keep a read/unread state in sync across devices; the badge shows a count, capped (9+).
- Ask for push permission in context, after value; see permission-prompts.
- Make every email unsubscribable in one click (RFC 8058 `List-Unsubscribe-Post`).

## Avoid
- Pinging for every event, or re-sending the same alert across all channels at once.
- Red badges that never clear.
- Notifications that only say "You have an update".
- Using notifications to pull lapsed users back with false urgency.
- Sending marketing through the transactional channel.

## Review
- [ ] Each type has an owner, a default and a user control.
- [ ] Items deep link, dedupe and sync read state.
- [ ] Volume per user per week is measured and capped.
- [ ] Unsubscribe and quiet hours work.
