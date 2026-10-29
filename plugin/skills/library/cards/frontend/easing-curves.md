---
name: easing-curves
title: Easing Curves
area: frontend
tags: [css, easing, timing, cubic-bezier, linear, motion]
detect: []
related: [animation, spring-physics, micro-interactions, stagger-choreography]
---
Pick easing by intent: ease-out to enter, ease-in to exit, ease-in-out to move, linear only for scroll or color; custom curves from tokens.

## Verify
- `grep -rnE "transition(-timing-function)?:.*(ease|linear|cubic)" src`: lists every curve to fold into tokens.
- `npx playwright test --grep easing`: asserts the computed `transitionTimingFunction` on key components.
- Devtools Animations panel: drag the curve editor to see it applied to the timeline.

## Test first
Assert the token is applied, so a refactor cannot silently drop it.
```ts
import { test, expect } from '@playwright/test';

test('menu uses the shared ease-out token', async ({ page }) => {
  await page.goto('/');
  const f = await page.locator('.menu').evaluate(
    el => getComputedStyle(el).transitionTimingFunction);
  expect(f).toBe('cubic-bezier(0.22, 1, 0.36, 1)');
});
```

## Do
- Define tokens once: `--ease-out: cubic-bezier(0.22, 1, 0.36, 1); --ease-in: cubic-bezier(0.64, 0, 0.78, 0); --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);`.
- Enter and appear: ease-out (fast start, soft landing). Exit: ease-in. Moves between two on-screen points: ease-in-out.
- Durations: 100-200 ms small, 200-300 ms medium, 300-500 ms large; shorter for exits than for entrances.
- Overshoot or bounce: use `linear()` with sampled points, e.g. `linear(0, 0.6 25%, 1.08 60%, 1 100%)`; see spring-physics.
- Step animations (sprites, typewriter): `steps(8, end)`.
- Scroll-linked and color animations: `linear`.
- Per-keyframe easing: set `animation-timing-function` inside a keyframe, not just on the rule.

## Avoid
- Default `ease` everywhere: it is a mild ease-in-out that suits nothing in particular.
- Linear easing for UI movement: reads as mechanical.
- Ease-in on entrances: the element feels stuck at the start, the moment users watch.
- Curves that overshoot opacity or color; values clamp.
- Ten bespoke curves; three tokens cover most interfaces.

## Review
- [ ] Easing values come from tokens, not literals scattered through CSS.
- [ ] Entrances ease out, exits ease in; durations match size and distance.
- [ ] Reduced-motion handling still shortens or removes movement.
- [ ] Any `linear()` list is under about 40 points.
