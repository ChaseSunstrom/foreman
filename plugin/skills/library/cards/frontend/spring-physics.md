---
name: spring-physics
title: Spring Physics Motion
area: frontend
tags: [animation, spring, physics, linear-easing, motion]
detect: [dep:@react-spring/web, dep:react-spring, dep:motion, dep:framer-motion]
related: [animation, easing-curves, gesture-input, micro-interactions, accessibility]
---
Springs for natural, interruptible motion: stiffness, damping and mass over fixed durations, with linear() as the CSS option.

## Verify
- `npx playwright test --grep spring`: asserts the settled end state and that reduced motion skips the oscillation.
- `grep -rn "cubic-bezier" src`: curves that overshoot should be springs or `linear()` instead.
- Devtools Performance panel: each frame under 16.7 ms while the spring runs.

## Test first
Test the rest position and reduced-motion behavior, not intermediate frames.
```ts
import { test, expect } from '@playwright/test';

test.use({ reducedMotion: 'reduce' });

test('sheet snaps to open with no bounce under reduced motion', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Open' }).click();
  const t = await page.locator('.sheet').evaluate(el => getComputedStyle(el).transform);
  expect(t).toBe('none');
});
```

## Do
- Start from defaults: stiffness 170, damping 26, mass 1 (react-spring) is a calm settle; raise damping to cut bounce, raise stiffness to speed up.
- Preserve velocity when interrupted or released from a gesture; springs retarget smoothly, tweens do not.
- For CSS-only, use `transition-timing-function: linear(0, 0.5 20%, 1.1 50%, 1 100%)` with sampled points (a generator emits 20-40 points); supported in all current engines.
- Use springs for position, scale and rotation: `transform` stays on the compositor.
- Under `prefers-reduced-motion`, switch to critically damped (no overshoot) or an instant set.
- Stop the loop at rest (velocity and displacement under a threshold, such as 0.01) so it does not keep the main thread awake.
- Pick the library by cost: `motion` is about 5 KB for the mini build; a hand-rolled rAF spring is 20 lines.

## Avoid
- Duration-based springs in one place and physics in another: motion feels inconsistent. Share one config set.
- Overshoot on opacity or color: values outside 0-1 clamp and flicker.
- Heavy bounce on frequent actions like list hovers: tiring.
- Animating `height` or `top` with springs: layout each frame.
- Unbounded simulations with no rest check.

## Review
- [ ] Springs retarget from current velocity when interrupted.
- [ ] Reduced-motion users get no overshoot or oscillation.
- [ ] The simulation stops at rest; no idle rAF in the profile.
- [ ] One shared set of spring presets, named by feel (gentle, snappy).
