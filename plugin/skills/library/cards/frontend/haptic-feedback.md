---
name: haptic-feedback
title: Haptic Feedback
area: frontend
tags: [haptics, vibration, mobile, feedback, navigator.vibrate, pwa]
detect: []
related: [micro-interactions, gesture-input, accessibility, pwa, toasts]
---
Short vibration cues through navigator.vibrate where available, optional, rate-limited and never the only signal.

## Verify
- `npx playwright test --grep haptic`: stubs `navigator.vibrate` and asserts calls and patterns.
- `grep -rn "navigator.vibrate" src`: every call must route through one guarded helper.
- Manual: test on a real Android device; emulators do not vibrate.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('confirm tap vibrates once with buzz(10)', async ({ page }) => {
  await page.addInitScript(() => {
    (window as any).__v = [];
    navigator.vibrate = (p: any) => ((window as any).__v.push(p), true);
  });
  await page.goto('/');
  await page.getByRole('button', { name: 'Confirm' }).click();
  expect(await page.evaluate(() => (window as any).__v)).toEqual([10]);
});

test('missing API does not throw', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.addInitScript(() => { delete (Navigator.prototype as any).vibrate; });
  await page.goto('/');
  await page.getByRole('button', { name: 'Confirm' }).click();
  expect(errors).toEqual([]);
});
```

## Do
- One helper: `const buzz = (p: number | number[]) => { if ('vibrate' in navigator && !reduce.matches && userEnabled()) navigator.vibrate(p); };`.
- Durations: 10-20 ms tick for selection, `[15, 40, 15]` for success, `[40, 60, 40, 60, 40]` for error; keep total under about 200 ms.
- Call only inside a user gesture handler; browsers ignore or block it without a recent tap (sticky user activation).
- Pair with a visual or text signal so deaf-blind, desktop and iOS users get the same information.
- Provide a setting to turn haptics off; honor `prefers-reduced-motion` as a conservative signal.
- Support: Android Chrome and Firefox implement `navigator.vibrate`; Safari on iOS does not. On iOS Safari 17.4+, a hidden `<input type="checkbox" switch>` toggled by user tap produces a system haptic.
- Cancel with `navigator.vibrate(0)` when the state changes or the page is hidden.

## Avoid
- Vibration on every scroll step or hover: battery drain and annoyance.
- Long patterns (over 1 s): browsers may cap them, and users find them alarming.
- Using haptics as the only confirmation or error signal.
- Unguarded calls; the method is absent on desktop and iOS and throws in older code paths.
- Vibrating on page load or from background timers.

## Review
- [ ] Missing API, reduced motion and user opt-out all result in silence, with no errors.
- [ ] Every haptic cue also has a visible or textual cue.
- [ ] Patterns are short, from a small named set.
- [ ] Calls only occur in response to user input.
