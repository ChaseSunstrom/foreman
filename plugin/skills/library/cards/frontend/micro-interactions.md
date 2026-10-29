---
name: micro-interactions
title: Micro-Interactions
area: frontend
tags: [ux, feedback, hover, press, motion, states]
detect: []
related: [animation, easing-curves, haptic-feedback, accessibility, keyboard-navigation]
---
Small feedback on press, hover, toggle and success: fast, purposeful, and never the only signal.

## Verify
- `npx playwright test --grep interaction`: hovers, presses and focuses controls, asserting the computed style change.
- `grep -rn ":hover" src --include=*.css`: hover rules need `:focus-visible` and `:active` counterparts.
- Devtools Performance panel: interaction to next paint (INP) under 200 ms with the effect on.

## Test first
Every visual state must exist for keyboard users and under reduced motion.
```ts
import { test, expect } from '@playwright/test';

test('button shows focus and pressed feedback', async ({ page }) => {
  await page.goto('/');
  const b = page.getByRole('button', { name: 'Save' });
  await b.focus();
  const outline = await b.evaluate(el => getComputedStyle(el).outlineStyle);
  expect(outline).not.toBe('none');
});
```

## Do
- Budget: acknowledge input within 100 ms; press feedback 80-120 ms, state change 150-250 ms.
- Press: `button:active { transform: scale(0.97); }` with a 100 ms transition; release returns with ease-out.
- Style `:hover` inside `@media (hover: hover)` so touch devices do not get stuck hover states.
- Toggle and checkbox: animate `transform` of the thumb and `background-color`; keep the native control or its ARIA role.
- Success confirmation: a short check-draw (stroke-dashoffset) 300 ms plus text; pair with a live region.
- Add `:focus-visible` rings; do not remove outlines.
- Under `prefers-reduced-motion: reduce`, replace movement with color or opacity change.

## Avoid
- Feedback longer than 400 ms on repeated actions: users wait on decoration.
- Hover-only information: invisible to touch and keyboard.
- Motion as the only signal of success or error: add text, icon or color with contrast.
- Bouncy effects on every control: they stop signaling anything.
- Animating `box-shadow` or `width` on hover across large lists; use opacity on a pseudo-element.

## Review
- [ ] Hover, focus-visible, active and disabled states all exist and are distinct.
- [ ] Touch devices show no sticky hover.
- [ ] Reduced-motion users get color or opacity feedback instead of movement.
- [ ] Success and error states are announced, not only animated.
