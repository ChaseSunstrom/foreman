---
name: gesture-input
title: Gesture and Pointer Input
area: frontend
tags: [pointer-events, touch, swipe, gestures, touch-action, input]
detect: [dep:@use-gesture/react, dep:hammerjs, dep:@use-gesture/vanilla]
related: [drag-and-drop, keyboard-navigation, spring-physics, accessibility, haptic-feedback]
---
Swipe, drag and pinch via Pointer Events and touch-action, with a button or key path for every gesture.

## Verify
- `npx playwright test --grep gesture`: dispatches pointer sequences with `page.mouse` and `page.touchscreen`, asserts the result.
- `grep -rn "touchstart\|touchmove" src`: legacy touch handlers to move to pointer events.
- Devtools Performance panel: pointer handlers under 50 ms; interaction latency (INP) under 200 ms.

## Test first
Every gesture needs a non-gesture equivalent; test that one first.
```ts
import { test, expect } from '@playwright/test';

test('card can be dismissed by keyboard as well as swipe', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Dismiss card' }).focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('.card')).toHaveCount(0);
});
```

## Do
- Use Pointer Events (`pointerdown`, `pointermove`, `pointerup`, `pointercancel`) for mouse, touch and pen together.
- Call `el.setPointerCapture(e.pointerId)` on down so moves continue outside the element.
- Set `touch-action: pan-y` (or `none` for full control) so the browser does not claim the gesture; this is required for horizontal swipes.
- Listen with `{ passive: true }` where you do not prevent default.
- Add a threshold (8-10 px) before treating movement as a drag, so taps still work.
- Decide on release from velocity as well as distance (for example more than 0.5 px/ms) and animate with a spring from that velocity.
- Handle `pointercancel` and `lostpointercapture` by restoring the rest state.
- Offer visible alternatives (buttons, arrow keys); WCAG 2.5.1 requires single-pointer alternatives to path-based gestures.
- Apply updates in `requestAnimationFrame` using `transform`.

## Avoid
- Touch and mouse event pairs: double-fires and ghost clicks.
- `preventDefault` on passive listeners; it logs errors and does nothing.
- Hit targets under 24 by 24 CSS px (WCAG 2.5.8); aim for 44.
- Gestures that conflict with system edges (browser back swipe, iOS home).
- Multi-finger-only features with no fallback.

## Review
- [ ] Each gesture has a keyboard and single-tap alternative.
- [ ] Cancel, scroll and multi-touch interruptions leave a sane state.
- [ ] `touch-action` matches the gesture; page scroll still works elsewhere.
- [ ] Input handlers measured under 50 ms on a mid-range phone.
