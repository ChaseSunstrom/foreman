---
name: permission-prompts
title: Permission Prompts
area: ux
tags: [permissions, notifications, location, camera, consent, product-design]
detect: []
related: [notification-design, onboarding-flows, dark-patterns, error-messages]
---
Browsers and OSes let you ask once. Explain first, ask in context, and design the denied path.

## Verify
- `npx playwright test --grep permission`: uses `context.grantPermissions` and a denied context to run both paths.
- `grep -rn "requestPermission\|getCurrentPosition\|getUserMedia" src`: each call sits behind a user gesture.
- Query state first: `navigator.permissions.query({name:'notifications'})` decides which UI shows.
- Check the settings fallback: denied users see steps to re-enable for their browser or OS.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('pre-prompt appears and denial leaves the app usable', async ({ page, context }) => {
  await context.clearPermissions();
  await page.goto('/map');
  await page.getByRole('button', { name: 'Use my location' }).click();
  await expect(page.getByRole('region', { name: /find stores near you/i })).toBeVisible();
});

test('granted location centres the map', async ({ page, context }) => {
  await context.grantPermissions(['geolocation']);
  await context.setGeolocation({ latitude: 52.52, longitude: 13.4 });
  await page.goto('/map');
  await page.getByRole('button', { name: 'Use my location' }).click();
  await expect(page.getByText('Berlin')).toBeVisible();
});
```

## Do
- Ask on a user gesture, at the moment the feature is needed, never on page load.
- Show your own pre-prompt first: what you will do with it and the benefit; the system prompt is a one-shot, a "Not now" on yours costs nothing.
- Request the narrowest permission and scope (approximate location, a single file, `<input type=file>` over broad access).
- Handle three states: prompt, granted, denied; denied must degrade gracefully (manual address entry, upload instead of camera).
- Remember a decline and wait before asking again (weeks, not minutes).
- When blocked, explain how to re-enable in the browser or OS settings.
- Release the camera, mic and location when done; show an active indicator.

## Avoid
- Asking for notifications on the first visit; grant rates are low and denial is near permanent.
- Dark-pattern "Allow" dialogs that mimic system prompts.
- Making the app unusable on denial.
- Asking for many permissions in a row.
- Keeping a stream or a watcher running in the background.

## Review
- [ ] Each ask follows a gesture and a clear reason.
- [ ] Denied and revoked states have a working fallback.
- [ ] Scope is minimal; resources are released.
- [ ] Re-ask frequency is capped.
