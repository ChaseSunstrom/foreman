---
name: animation
title: Web Animation
area: frontend
tags: [animation, css, motion, transitions, view-transitions, gsap]
detect: [dep:framer-motion, dep:motion, dep:gsap, dep:animejs, dep:@react-spring/web, dep:lottie-web, dep:@formkit/auto-animate]
related: [accessibility, web-performance, css-layout, svg-canvas]
---
Purposeful motion: CSS first, compositor-only properties, reduced-motion respected, interruptible.

## Verify
- `npx playwright test --grep motion`: runs with `reducedMotion: 'reduce'` emulation and checks end state.
- `npx lighthouse http://localhost:3000 --only-categories=performance`: flags non-composited animations in the audit list.
- Devtools Performance panel: record the animation and look for Layout or Paint on each frame.
- `grep -rn "transition: *all" src`: finds blanket transitions to narrow.

## Test first
Assert the reduced-motion contract and the final state, not frame timing.
```ts
import { test, expect } from '@playwright/test';

test.use({ reducedMotion: 'reduce' });

test('menu opens without transition under reduced motion', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Menu' }).click();
  const d = await page.getByRole('navigation').evaluate(
    el => getComputedStyle(el).transitionDuration);
  expect(d).toBe('0s');
});
```

## Do
- Animate `transform` and `opacity` only; they run on the compositor.
- Prefer CSS transitions and `@keyframes`; use the Web Animations API (`el.animate()`) for sequencing; reach for a library only for physics, timelines or scroll scrubbing.
- Wrap non-essential motion in `@media (prefers-reduced-motion: no-preference)`, or set durations near zero under `reduce`.
- Durations: 100-200ms for feedback, 200-400ms for transitions; ease-out on enter, ease-in on exit.
- Use `@starting-style` and `transition-behavior: allow-discrete` to animate `display` and `dialog` entry.
- Use `view-transition-name` and `document.startViewTransition` for page or list transitions, with a fallback when absent.
- Use `will-change` briefly on the element about to animate, then remove it.
- Make animations interruptible; reversing mid-way should not jump.

## Avoid
- Animating `width`, `height`, `top`, `left`, `margin`: triggers layout each frame. Use `transform: scale/translate`, or `grid-template-rows` 0fr to 1fr for height.
- `transition: all`: animates unintended properties and costs. List the properties.
- Parallax or autoplay motion with no way to stop: vestibular harm; WCAG requires pause for motion over 5 seconds.
- `setInterval` or `setTimeout` driven animation: drifts and janks. Use `requestAnimationFrame` or CSS.
- Permanent `will-change: transform` on many elements: wastes memory. Apply on demand.
- Flashing more than three times per second: seizure risk. Remove it.
- Animating on load for every element: slows perceived speed. Animate only meaningful changes.

## Review
- [ ] Reduced-motion users get a calm equivalent, not a broken layout.
- [ ] Only compositor properties animate; no layout thrash in the profile.
- [ ] Motion explains a state change; none is decorative-only on critical paths.
- [ ] Focus and screen reader state stay correct during and after animation.
- [ ] Library added only if CSS or WAAPI cannot do the job; bundle cost checked.
