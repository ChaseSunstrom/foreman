---
name: animated-counters
title: Animated Counters
area: frontend
tags: [animation, numbers, counter, intl, aria-live, property]
detect: []
related: [animation, i18n, accessibility, scroll-reveal, micro-interactions]
---
Count numbers up with @property or rAF, formatted with Intl, announced once, and the final value always in the DOM.

## Verify
- `npx playwright test --grep counter`: waits for the final text and checks it under reduced motion.
- `grep -rn "setInterval" src | grep -i count`: interval counters to replace with rAF or CSS.
- `node -e "console.log(new Intl.NumberFormat('de-DE').format(1234567.8))"`: confirms the locale format you expect.

## Test first
```ts
import { test, expect } from '@playwright/test';

test.use({ reducedMotion: 'reduce' });

test('stat shows the final value immediately', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByTestId('users')).toHaveText('12,480');
});
```

## Do
- CSS-only integers: `@property --n { syntax: '<integer>'; initial-value: 0; inherits: false; }` animate `--n` to the target and print it with `counter-reset: n var(--n); content: counter(n);`. Supported in current Chrome, Safari, Firefox.
- JS version: `requestAnimationFrame`, compute progress from `performance.now()` against a 600-1200 ms duration with ease-out; never accumulate per-frame increments.
- Format each frame with one cached `Intl.NumberFormat(locale, opts)`, using `maximumFractionDigits` fixed to avoid width jitter.
- Prevent layout jitter: `font-variant-numeric: tabular-nums;` and a `min-width` in `ch`.
- Put the real final value in the DOM text (or `aria-label`) at load; the animated number is decoration.
- Start when visible (IntersectionObserver threshold 0.4), run once.
- Live metrics that update continuously: update the text node and throttle announcements with `aria-live="polite"` every several seconds, not per tick.
- Under `prefers-reduced-motion: reduce`, render the final value at once.

## Avoid
- Counting up financial or safety values: users need accuracy at once.
- A screen reader hearing every intermediate value.
- `setInterval` steps at 16 ms: drift and wasted frames.
- Locale-blind `toFixed` and manual comma insertion.
- Animations longer than about 1.5 s; the number becomes a wait.

## Review
- [ ] The final value is present without JavaScript or animation.
- [ ] Digits use tabular figures with no width jitter.
- [ ] Assistive tech receives the final value once.
- [ ] Formatting follows the user locale.
