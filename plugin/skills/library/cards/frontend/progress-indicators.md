---
name: progress-indicators
title: Progress Indicators
area: frontend
tags: [progress, loading, spinner, aria, ux, animation]
detect: []
related: [skeleton-loading, aria-patterns, animation, accessibility, optimistic-ui]
---
Show progress honestly: determinate bars when known, indeterminate only when not, announced to assistive tech and cheap to render.

## Verify
- `npx playwright test --grep progress`: asserts `role=progressbar` with `aria-valuenow` changing.
- `npx axe-cli http://localhost:3000`: flags progress elements without accessible names.
- Devtools Performance panel: animation uses transform; no layout each frame.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('upload bar exposes progress to assistive tech', async ({ page }) => {
  await page.goto('/upload');
  const bar = page.getByRole('progressbar', { name: 'Upload' });
  await expect(bar).toHaveAttribute('aria-valuemin', '0');
  await expect(bar).toHaveAttribute('aria-valuemax', '100');
});
```

## Do
- Use native `<progress value="40" max="100">` or `role="progressbar"` with `aria-valuenow`, `aria-valuemin`, `aria-valuemax` and a label; drop `aria-valuenow` when indeterminate.
- Choose by wait: under 1 s show nothing; 1-10 s spinner or indeterminate bar; over 10 s determinate bar with percent or step text.
- Animate fill with `transform: scaleX()` and `transform-origin: left`, not `width`.
- Circular spinners: rotate an SVG circle with `stroke-dasharray`; one 1 s linear infinite rotation is enough.
- Delay display about 200-300 ms so fast operations never flash a spinner; once shown, keep it at least 400 ms.
- Announce milestones, not every percent: a polite live region updating at most every few seconds.
- Under reduced motion, replace spinning with a pulsing opacity or static text like "Loading".
- Page-level: for navigation, a thin top bar that moves toward 90% and completes on done.

## Avoid
- Fake progress that stalls at 99%: honesty erodes trust.
- Infinite spinners with no timeout, error or cancel.
- Color alone to show status; add text.
- Width animation on thousands of rows.
- Announcing every tick to screen readers.

## Review
- [ ] Every indicator has a name and correct ARIA value attributes.
- [ ] Failure and cancel paths replace the indicator.
- [ ] Fast operations do not flash a spinner.
- [ ] Reduced-motion users get a non-rotating alternative.
