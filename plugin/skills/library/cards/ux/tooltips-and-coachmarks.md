---
name: tooltips-and-coachmarks
title: Tooltips and Coachmarks
area: ux
tags: [tooltip, coachmark, hints, popover, product-design]
detect: []
related: [onboarding-flows, accessibility, focus-management, keyboard-navigation]
---
Tooltips name or briefly explain a control; coachmarks introduce one new thing once. Both are dismissible and keyboard reachable.

## Verify
- `npx playwright test --grep tooltip`: hovers and focuses the trigger, asserts text, and Esc dismisses.
- `npx axe-core-cli http://localhost:3000`: tooltip uses `role="tooltip"` and `aria-describedby`.
- `grep -rn "title=" src | wc -l`: native `title` attributes are not the only source of essential info.
- Zoom to 400% and use a touch emulation profile: the hint is still reachable without hover.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('tooltip shows on focus, persists on hover, closes on Escape', async ({ page }) => {
  await page.goto('/');
  const btn = page.getByRole('button', { name: 'Export' });
  await btn.focus();
  const tip = page.getByRole('tooltip');
  await expect(tip).toHaveText(/download as csv/i);
  await page.keyboard.press('Escape');
  await expect(tip).toHaveCount(0);
});

test('coachmark shows once and stays dismissed', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Got it' }).click();
  await page.reload();
  await expect(page.getByRole('button', { name: 'Got it' })).toHaveCount(0);
});
```

## Do
- Show tooltips on hover and keyboard focus, with a 300-500 ms open delay and no delay on focus.
- Meet WCAG 1.4.13: dismissible (Esc), hoverable (pointer can move onto it) and persistent.
- Keep text to one short sentence (under about 80 characters); no links or buttons inside a tooltip, use a popover instead.
- Connect with `aria-describedby`; do not hide an essential label in a tooltip.
- Coachmarks: one at a time, anchored to the real element, with Next/Skip, at the moment the feature becomes relevant.
- Store "seen" per user server-side so it does not return on a new device.
- Limit a tour to 3-5 steps and let it be replayed from Help.

## Avoid
- Tooltips as the only way to know what an icon does on touch screens.
- Auto-opening several coachmarks on first load.
- Blocking overlays that trap focus with no Esc.
- Showing the same hint after the user used the feature.
- Tooltip positions that clip at viewport edges.

## Review
- [ ] Hover, focus and Esc all work; content is not hover-only.
- [ ] Touch users have another route to the information.
- [ ] Coachmarks fire once, skippable, per user not per device.
- [ ] Tour is 5 steps or fewer and replayable.
